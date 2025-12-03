


from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('member/', views.member, name='member'),
    path('faq/', views.faq, name='faq'),
    path('event/', views.event, name='event'),
    path('service/', views.service, name='service'),
    path('condition/', views.condition, name='condition'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart, name='cart'),
    
    #shop 
    path('shop/', views.shop, name='shop'),
    path('shop/or14k', views.shop_14k, name='or14k'),
    path('shop/or10k', views.shop_10k, name='or10k'),
    path('shop/argent', views.shop_argent, name='argent'),
    path('shop/orRempli', views.shop_rempli, name='orrempli'),
    path('shop/charms', views.charms, name='charms'),

    # boutique 
    path('boutique/', views.boutique, name='boutique'),
    path('boutique/bagues', views.boutique_bague, name='bague'),
    path('boutique/collier', views.boutique_collier, name='collier'),
    path('boutique/bijou_de_main', views.boutique_bijouxdemain, name='bijouxdemain'),
    path('boutique/boucle_doreille', views.boutique_boucledoreille, name='boucledoreille'),
    path('boutique/bracelet', views.boutique_bracelet, name='bracelet'),
    path('boutique/bracelet_de_cheville', views.boutique_cheville, name='braceletdecheville'),

]