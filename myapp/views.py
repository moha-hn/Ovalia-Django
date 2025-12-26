from decimal import Decimal, ROUND_HALF_UP

import stripe

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.urls import reverse

from gestion.models import Order, Sales


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


def _absolute_payment_url(request, settings_attr, view_name):
    configured_url = getattr(settings, settings_attr, '')
    if configured_url:
        return configured_url
    return request.build_absolute_uri(reverse(view_name))


def checkout(request):
    cart_items, total = _cart_items_with_totals(request)

    if request.method == 'POST':
        if not cart_items:
            messages.info(request, "Votre panier est vide. Ajoutez des articles avant de payer.")
            return redirect('cart')

        if not settings.STRIPE_SECRET_KEY or settings.STRIPE_SECRET_KEY == 'your-stripe-secret-key':
            messages.error(request, "Configurez votre clé Stripe secrète avant de lancer un paiement.")
            return redirect('checkout')

        stripe.api_key = settings.STRIPE_SECRET_KEY
        line_items = []
        for item in cart_items:
            unit_amount = int((item['sale'].price * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['sale'].name,
                        'description': item['sale'].description[:200],
                    },
                    'unit_amount': unit_amount,
                },
                'quantity': item['quantity'],
            })

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items,
                success_url=_absolute_payment_url(request, 'PAYMENT_SUCCESS_URL', 'checkout_success'),
                cancel_url=_absolute_payment_url(request, 'PAYMENT_CANCEL_URL', 'checkout_cancel'),
            )
        except stripe.error.StripeError as exc:
            error_message = getattr(exc, 'user_message', None) or str(exc)
            messages.error(request, f"Impossible de créer la session de paiement : {error_message}")
            return redirect('checkout')

        order = Order.objects.create(
            total=total,
            stripe_payment_id=getattr(session, 'payment_intent', '') or session.id,
            status='Pending'
        )
        request.session['latest_order_id'] = order.id
        return redirect(session.url)

    context = {
        'cart_items': cart_items,
        'total': total,
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'user/sales/checkout.html', context)


def checkout_success(request):
    order_id = request.session.pop('latest_order_id', None)
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'Paid'
            order.save(update_fields=['status'])
        except Order.DoesNotExist:
            pass

    request.session['cart'] = {}
    request.session.modified = True
    return render(request, 'user/sales/checkout_success.html')


def checkout_cancel(request):
    order_id = request.session.pop('latest_order_id', None)
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'Canceled'
            order.save(update_fields=['status'])
        except Order.DoesNotExist:
            pass

    return render(request, 'user/sales/checkout_cancel.html')
