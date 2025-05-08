
from django.contrib import admin
from django.urls import path

from . import views;
urlpatterns = [
   path("", views.index, name="index"),
   path("faq/", views.faq, name="contact"),
   path("member/", views.member, name="member"),
   path("faq/", views.faq, name="faq"),
   path('logout/',views.logout_view ,name='logout'),

   #shop 
   path('shop/',views.shop ,name='shop'),
   path('shop/or14k',views.shop_14k ,name='or14k'),
   path('shop/or10k',views.shop_10k ,name='or10k'),
   path('shop/argent',views.shop_argent ,name='argent'),
   path('shop/orRempli',views.shop_rempli ,name='orrempli'),
   path('shop/charms',views.charms ,name='charms'),

   path('cart/', views.cart, name='cart'),
]
