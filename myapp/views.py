from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.template.loader import render_to_string
from gestion.models import Sales
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
