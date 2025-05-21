from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from gestion.models import *
from .filters import *
# Create your views here.


def index(request):
    latest_products = Product.objects.filter(available=True).order_by('-created')[:3]
    print(latest_products )
    context={
        'latest_products':latest_products,
    }
    return render(request,"user/index.html",context)

def faq(request):
    return render(request,"user/faq.html")

def service(request):
    return render(request,"user/service.html")

def event(request):
    return render(request,"user/event.html")

def contact(request):
    return render(request,"user/contact.html")

def cart(request):
    return render(request,"user/cart.html")

def logout_view(request):
    logout(request)
    return redirect('index') 

def login(request):
    return render(request,"user/login.html")

def member(request):
    return render(request,"user/members.html")


def shop(request):
    context={

    }
    return render(request,"user/shop/shop.html",context)

def shop_14k(request):
    product = Product.objects.filter(available=True, materiaux='Or massif 14k')
    context={
        'products':product
    }
    return render(request,"user/shop/or_massif.html",context)

def shop_10k(request):
    product = Product.objects.filter(available=True, materiaux='Or massif 10k')
    context={
        'products':product
    }
    return render(request,"user/shop/or_massif_10k.html",context)

def shop_rempli(request):
    product = Product.objects.filter(available=True, materiaux='Or rempli')
    context={
        'products':product
    }
    return render(request,"user/shop/or_rempli.html",context)

def shop_argent(request):
    product = Product.objects.filter(available=True, materiaux='Argent sterling')
    context={
        'products':product
    }
    return render(request,"user/shop/argent.html",context)

def charms(request):
    context={

    }
    return render(request,"user/shop/charms.html",context)

