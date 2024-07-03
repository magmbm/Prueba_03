from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path("base", views.base, name= "base"),
    path("perfil", views.perfil, name="perfil"),
    path("home", views.home, name="home"),
    path("tienda", views.tienda, name="tienda"),
    path("about", views.about, name="about"),
    path("novedades", views.novedades, name="novedades"),
    path("producto", views.producto ,name="producto"),
    path("login", views.login_t, name="login_t"),
    path("logout_t", views.logout_t, name="logout_t"),
    path("pago", views.pago, name="pago"),
    path("cart", views.cart, name="cart"),
    path("registro", views.registro, name="registro"),
    path("contactar", views.contactar, name="contactar"),
]