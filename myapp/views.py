from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render

from gestion.models import Sales


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


def boutique(request):
    sales = Sales.objects.filter(available=True).order_by('-created')
    context = {'sales': sales}
    return render(request, 'user/sales/boutique.html', context)


def sale_detail(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    return render(request, 'user/sales/sale_detail.html', {'sale': sale})


def _get_cart(request):
    return request.session.setdefault('cart', {})


def _cart_items_with_totals(request):
    cart = _get_cart(request)
    sales = Sales.objects.filter(id__in=cart.keys())
    items = []
    total = Decimal('0.00')
    for sale in sales:
        quantity = int(cart.get(str(sale.id), 0))
        subtotal = sale.price * quantity
        total += subtotal
        items.append({'sale': sale, 'quantity': quantity, 'subtotal': subtotal})
    return items, total


def add_to_cart(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    cart = _get_cart(request)
    cart[str(sale_id)] = cart.get(str(sale_id), 0) + 1
    request.session.modified = True
    messages.success(request, f"{sale.name} a été ajouté à votre panier.")
    return redirect('sale_detail', sale_id=sale_id)


def update_cart(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    cart = _get_cart(request)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity > 0:
        cart[str(sale_id)] = quantity
        messages.info(request, f"Quantité mise à jour pour {sale.name}.")
    else:
        cart.pop(str(sale_id), None)
        messages.info(request, f"{sale.name} a été retiré du panier.")
    request.session.modified = True
    return redirect('cart')


def remove_from_cart(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    cart = _get_cart(request)
    cart.pop(str(sale_id), None)
    request.session.modified = True
    messages.info(request, f"{sale.name} a été retiré du panier.")
    return redirect('cart')


def cart(request):
    items, total = _cart_items_with_totals(request)
    return render(request, 'user/sales/cart.html', {'cart_items': items, 'total': total})
