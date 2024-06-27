from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


# Create your views here.

def base(request):
    context={}
    return render(request, "tienda/base.html", context)

def perfil(request):
    context={}
    return render(request, "tienda/perfil.html", context)

def home(request):
    context={}
    return render(request, "tienda/index.html", context)

def tienda(request):
    context={}
    return render(request, "tienda/tienda.html", context)

def about(request):
    context={}
    return render(request, "tienda/about.html", context)

def novedades(request):
    context={}
    return render(request, "tienda/novedades.html", context)

def producto(request):
    context={}
    return render(request, "tienda/producto.html", context)

def logout_t(request):
    logout(request)
    return redirect('home')


def login_t(request):
    if request.method== "POST": 
        usuario= request.POST["nombre_user"]
        contrasena= request.POST["contra_user"]
        user= authenticate(request, username= usuario, password= contrasena)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login_t')
    else:
        context={}
        return render(request, "tienda/login.html", context)
    

def pago(request):
    context={}
    return render(request, "tienda/pago.html", context) 