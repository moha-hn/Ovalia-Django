from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from gestion.models import Sales, CartItem, Order
from django.template.loader import render_to_string
import stripe
import io
from datetime import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    latest_products = Sales.objects.filter(available=True).order_by('-created')[:3]
    context = {'latest_products': latest_products}
    return render(request, 'user/index.html', context)

def faq(request):
    return render(request, 'user/faq.html')

def condition(request):
    return render(request, 'Conditions_utilisation.html')

def service(request):
    return render(request, 'user/service.html')

def event(request):
    return render(request, 'user/event.html')

def contact(request):
    return render(request, 'user/contact.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def login(request):
    return render(request, 'user/login.html')

def member(request):
    return render(request, 'user/members.html')

def shop(request):
    return render(request, 'user/shop/shop.html')

def shop_14k(request):
    products = Sales.objects.filter(available=True, materiaux='Or massif 14k')
    return render(request, 'user/shop/or_massif.html', {'products': products})

def shop_10k(request):
    products = Sales.objects.filter(available=True, materiaux='Or massif 10k')
    return render(request, 'user/shop/or_massif_10k.html', {'products': products})

def shop_rempli(request):
    products = Sales.objects.filter(available=True, materiaux='Or rempli')
    return render(request, 'user/shop/or_rempli.html', {'products': products})

def shop_argent(request):
    products = Sales.objects.filter(available=True, materiaux='Argent sterling')
    return render(request, 'user/shop/argent.html', {'products': products})

def charms(request):
    return render(request, 'user/shop/charms.html')




#boutique related views
def boutique(request):
    sales = Sales.objects.filter(available=True)
    context = {'sales': sales}
    return render(request, 'user/sales/boutique.html', context)

def boutique_bague(request):
    products = Sales.objects.filter(available=True, category='Bague')
    return render(request, 'user/sales/bague.html', {'products': products})

def boutique_collier(request):
    products = Sales.objects.filter(available=True, category='Collier')
    return render(request, 'user/sales/collier.html', {'products': products})

def boutique_cheville(request):
    products = Sales.objects.filter(available=True, category='Bracelet de cheville')
    return render(request, 'user/sales/cheville.html', {'products': products})

def boutique_bracelet(request):
    products = Sales.objects.filter(available=True, category='Bracelet')
    return render(request, 'user/sales/bracelet.html', {'products': products})

def boutique_bijouxdemain(request):
    products = Sales.objects.filter(available=True, category='Bijou de main')
    return render(request, 'user/sales/bijoux_main.html', {'products': products})

def boutique_boucledoreille(request):
    products = Sales.objects.filter(available=True, category='Boucle doreille')
    return render(request, 'user/sales/oreille.html', {'products': products})


def cart(request):
    return render(request, 'user/sales/cart.html')


def add_to_cart(request, sale_id, wear_type):
    sale = get_object_or_404(Sales, id=sale_id)
    if wear_type not in ['collier', 'poignee', 'cheville']:
        return redirect('boutique')
    cart_item, created = CartItem.objects.get_or_create(user=request.user, sale=sale, wear_type=wear_type)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart')
    total = sum(get_sale_price(item.sale, item.wear_type) * item.quantity for item in cart_items)
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(get_sale_price(item.sale, item.wear_type) * 100),
                    'product_data': {
                        'name': f"{item.sale.name} ({item.wear_type.capitalize()})",
                    },
                },
                'quantity': item.quantity,
            } for item in cart_items
        ],
        mode='payment',
        success_url=settings.PAYMENT_SUCCESS_URL,
        cancel_url=settings.PAYMENT_CANCEL_URL,
    )
    order = Order.objects.create(user=request.user, total=total, stripe_payment_id=checkout_session.id)
    cart_items.delete()  # Clear cart after creating order
    return JsonResponse({'sessionId': checkout_session.id})

def success(request):
    return render(request, 'user/sales/success.html')

def cancel(request):
    return render(request, 'user/sales/cancel.html')

def stripe_config(request):
    return JsonResponse({'publicKey': settings.STRIPE_PUBLISHABLE_KEY})

def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    cart_items = CartItem.objects.filter(user=request.user)
    context = {
        'order': order,
        'cart_items': cart_items,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'get_sale_price': get_sale_price,
    }
    latex_content = render_to_string('user/sales/invoice.tex', context)
    return HttpResponse(latex_content, content_type='text/latex')