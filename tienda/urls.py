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
    path("prueba", views.prueba, name="prueba"),
    path("contactar", views.contactar, name="contactar"),
    path("crud_c", views.crud_contact, name="crud_c"),
    path("crud_b", views.crud_boleta, name="crud_b"),
    path("contact_details", views.contact_details, name="contact_details"),
    path("pedido_details", views.pedido_details, name="pedido_details"),

]