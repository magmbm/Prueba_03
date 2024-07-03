from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Game, Cliente, Pedido
from django.http import HttpResponse
import json
import requests
import http.client
import random
from .personal_f import get_generos

# Create your views here.

def load_to_db(request):

    url = "https://rawg-video-games-database.p.rapidapi.com/games?key=5d2d49ee1c9a492383db4a282bf3d3de"

    headers = {
        "x-rapidapi-key": "9435183804msh6c9379f949be408p1466dbjsn0c1f158cd172",
        "x-rapidapi-host": "rawg-video-games-database.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data= response.json()
    for i in range(20):
        resultados= data.get('results')[i]
        precio= random.randint(25990, 79990)
        Game.objects.create(
            id= i,
            nombre= resultados.get('name'),
            precio= precio, 
            genero= get_generos(resultados.get('genres')),
            fecha_lanzamiento= resultados.get('released'),
            imagen= resultados.get('background_image')
        )
    context={"data": data.get('results')}
    return render(request, "tienda/test.html", context)

@login_required(login_url= '/tienda/login')
def cart(request):
    context={"current": "carro"}
    return render(request, "tienda/carrito.html", context)

def base(request):
    context={}
    return render(request, "tienda/base.html", context)

def perfil(request):
    context={}
    return render(request, "tienda/perfil.html", context)

def home(request):
    context={"current": "home"}
    return render(request, "tienda/index.html", context)

def tienda(request):
    context={"current": "tienda"}
    return render(request, "tienda/tienda.html", context)

def about(request):
    context={"current": "about"}
    return render(request, "tienda/about.html", context)

def novedades(request):
    context={"current": "novedades"}
    return render(request, "tienda/novedades.html", context)

def producto(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user= User.objects.get(username= request.user)
            cli= user.cliente
            nombre= cli.nombre
            gen= request.POST['genero']
            context={"usuario": user, 
                     "nombre": nombre,
                     "genero": gen}
            return render(request, "tienda/test.html", context)
        else:
            return render(request, "tienda/login.html", context)
    else:
        context={"current": "tienda"}
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
            context={"mensaje": "El nombre de usuario o contraseña no es valido",
                     "current": "login"} 
            return render(request, "tienda/login.html", context)
    else:
        context={"current" : "login"}
        return render(request, "tienda/login.html", context)
    
def pago(request):
    context={}
    return render(request, "tienda/pago.html", context) 

def registro(request):
    if request.method== "POST":
        user_name= request.POST["nombre_user"]
        nombre= request.POST["nombre"]
        p_apellido= request.POST["pri_apellido"]
        s_apellido= request.POST["seg_apellido"]
        contrasena= request.POST["contra_user"]
        email= request.POST["email"]
        try:

            usuario= User.objects.get(username= user_name)

            mensaje= "Este nombre de usuario ya está siendo ocupado"
            context={
                "mensaje": mensaje
            }
            return render(request, "tienda/registro.html", context)
        except:
            user= User.objects.create_user(user_name, email, contrasena)
            user.save()
            cliente= Cliente.objects.create(
                user= user,
                nombre= nombre,
                primer_apellido= p_apellido,
                segundo_apellido= s_apellido,
                direccion= None,
                telefono= None

            )
            cliente.save()
            login(request, user)
            return redirect('home')
    else:
        return render(request, "tienda/registro.html", {})
    
def contactar(request):
    context={}
    return render(request, "tienda/contactar.html", context) 