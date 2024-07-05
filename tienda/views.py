from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Game, Cliente, Pedido, Record, Contact
from django.http import HttpResponse
import json
import requests
import http.client
import random
from .personal_f import get_generos
from datetime import date

# Create your views here.


def load_to_db(request):

    url = "https://rawg-video-games-database.p.rapidapi.com/games?key=5d2d49ee1c9a492383db4a282bf3d3de"

    headers = {
        "x-rapidapi-key": "9435183804msh6c9379f949be408p1466dbjsn0c1f158cd172",
        "x-rapidapi-host": "rawg-video-games-database.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    for i in range(20):
        resultados = data.get('results')[i]
        precio = random.randint(25990, 79990)
        Game.objects.create(
            id=i,
            nombre=resultados.get('name'),
            precio=precio,
            genero=get_generos(resultados.get('genres')),
            fecha_lanzamiento=resultados.get('released'),
            imagen=resultados.get('background_image')
        )
    context = {"data": data.get('results')}
    return render(request, "tienda/test.html", context)


@login_required(login_url='/tienda/login')
def cart(request):
    if request.method== "POST":
        if 'plus-btn' in request.POST:
            user= request.user
            cli= user.cliente
            game_id= request.POST.get("plus-btn")
            game= Game.objects.get(id= game_id)
            pedido= Pedido.objects.get(f_cliente= cli, current= True)
            record= Record.objects.get(pedido_FK= pedido, f_game= game)
            pedido.nro_productos= pedido.nro_productos + 1
            record.cant= record.cant +1
            record.precio_total= record.precio_total + game.precio
            pedido.total_precio= pedido.total_precio + game.precio
            pedido.save()
            record.save()
        if 'minus-btn' in request.POST:
            user= request.user
            cli= user.cliente
            game_id= request.POST.get("minus-btn")
            game= Game.objects.get(id= game_id)
            pedido= Pedido.objects.get(f_cliente= cli, current= True)
            record= Record.objects.get(pedido_FK= pedido, f_game= game)
            record.cant= record.cant - 1
            pedido.nro_productos= pedido.nro_productos - 1
            record.precio_total= record.precio_total - game.precio
            pedido.total_precio= pedido.total_precio - game.precio
            pedido.save()
            record.save()
        return redirect('cart')
    else:
        user = User.objects.get(username=request.user)
        cli = user.cliente
        try:
            pedido = Pedido.objects.get(f_cliente=cli, current=True)
            records = Record.objects.filter(pedido_FK= pedido)
            for i in records:
                if i.cant<1:
                    i.delete()
            context = {
                "records": records,
                "pedido": pedido,
                "current": "carro",
                "flag": "flag"
            }
        except:
            context = {
                "message": "Su carrito esta vacio",
                "current": "carro"
            }
        return render(request, "tienda/carrito.html", context)

def contactar(request):
    if request.method== "POST":
        email= request.POST["email"]
        asunto= request.POST["asunto"]
        mensaje= request.POST["mensaje"]  
        if request.user.is_authenticated:
            user= request.user
            cli= user.cliente
            contacto= Contact.objects.create(
                f_cliente= cli,
                asunto= asunto,
                mensaje= mensaje,
                email_emisor= email
            )
            contacto.save()
        else:
            contacto= Contact.objects.create(
                asunto= asunto,
                mensaje= mensaje,
                email_emisor= email
            )
            contacto.save()
        return redirect('home')
    else:
        context={"current": "contacto"}
        return render(request, "tienda/contactar.html", context) 

def base(request):
    context = {}
    return render(request, "tienda/base.html", context)

def crud_contact(request):
    if request.method== "POST":
        id_c= request.POST["boton_id"]
        request.session["id_c"]= id_c
        solicitud= Contact.objects.get(id= id_c)
        resuelta= solicitud.resuelta
        if resuelta:
            res= "Si"
        else:
            res= "No"
        try:
            cliente= solicitud.f_cliente
            context={"cliente": cliente,
                     "solicitud": solicitud,
                     "res": res}

            request.method= None
            return contact_details(request, context)
        except:
            context={"solicitud": solicitud,
                     "no_cli": "Cliente no Registrado",
                     "res": res}
            request.method= None
            return contact_details(request, context)
    else :
        contactos= Contact.objects.all()
        context={"contact": contactos}
        return render(request, "tienda/crud_contact.html", context)

def contact_details(request, contexto):
    if request.method== "POST":
        try:

            id_c= request.POST["boton_id"]
            respuesta= request.POST["respuesta"]
            if respuesta== "" | respuesta is None:
                contexto["mensaje"]= "Arriba"
                return render(request, "tienda/contact_det.html", contexto)
            else:
                solicitud= Contact.objects.get(id= contexto.get("solicitud").get("id"))
                solicitud.respuesta= respuesta
                solicitud.resuelta= True
                solicitud.save()
                return redirect('crud_contact')
        except:
            contexto["mensaje"]= "Por aquí va la ruta"
            return render(request, "tienda/contact_det.html", contexto)
    else:
        return render(request, "tienda/contact_det.html", contexto)
    
    

def crud_boleta(request):
    if request.method== "POST":
        id_p= request.POST.get("id_boton")
        pedido= Pedido.objects.get(id= id_p)
        cliente= pedido.f_cliente
        context={
            "pedido": pedido,
            "cliente": cliente
        }
        return render(request, "tienda/pedido_det.html", context)
    else:
        pedidos= Pedido.objects.all()
        context={"pedidos": pedidos}
        return render(request, "tienda/crud_boleta.html", context)

def pedido_details(request):
    return render(request, "tienda/pedido_det.html", {})

def perfil(request):
    user= request.user
    cli= user.cliente
    context = {"cliente": cli,
               "usuario": user}
    return render(request, "tienda/perfil.html", context)


def home(request):
    if request.user.is_superuser:
        context= {"current": "home",}
        return render(request, "tienda/index.html", context)
    else:
        context = {"current": "home"}
    return render(request, "tienda/index.html", context)


def tienda(request):
    context = {"current": "tienda"}
    return render(request, "tienda/tienda.html", context)


def about(request):
    context = {"current": "about"}
    return render(request, "tienda/about.html", context)


def novedades(request):
    context = {"current": "novedades"}
    return render(request, "tienda/novedades.html", context)


def prueba(request):
    if request.method== "POST":
        respuesta= request.POST["respuesta"]
        context = {
            "uno": respuesta
        }
        return render(request, "tienda/test.html", context)
    else:
        context={"res": "No"}
        return render(request, "tienda/contact_det.html", context)


def producto(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            cli = user.cliente
            game_cant = request.POST.get("prod-cantidad")
            game_id = request.POST.get("prod-add-btn")
            game = Game.objects.get(id=game_id)
            try:
                pedido = Pedido.objects.get(f_cliente=cli, current=True)
                pedido.nro_productos = pedido.nro_productos + int(game_cant)
                pedido.total_precio = pedido.total_precio + (int(game_cant) * game.precio)
                pedido.save()
                try:
                    registro_same_game= Record.objects.get(pedido_FK= pedido, f_game= game)
                    registro_same_game.cant= registro_same_game.cant + int(game_cant)
                    registro_same_game.precio_total= registro_same_game.precio_total + (game.precio + int(game_cant))
                    registro_same_game.save()
                except:
                    registro = Record.objects.create(
                        f_game=game,
                        pedido_FK=pedido,
                        cant=game_cant,
                        precio_uni=game.precio,
                        precio_total=int(game.precio) * int(game_cant)
                    )
                    registro.save()
                    context = {"cli": cli,
                           "pedido": pedido,
                           }
                    return redirect('cart')
            except:
                # Si nunca ha tenido un pedido se hace ahora
                pedido = Pedido.objects.create(
                    nro_productos= game_cant,
                    f_cliente=cli,
                )
                pedido.save()
                registro = Record.objects.create(
                    f_game=game,
                    pedido_FK=pedido,
                    cant=game_cant,
                    precio_uni=game.precio,
                    precio_total= game.precio * int(game_cant)
                )
                pedido.total_precio= registro.precio_total
                pedido.save()
                registro.save()
                context = {"cli": cli,
                           "pedido": pedido}
            
            return redirect('cart')
        else:
            return     redirect('login_t')
    else:

        context = {"current": "tienda"}
        return render(request, "tienda/producto.html", context)


def logout_t(request):
    logout(request)
    return redirect('home')


def login_t(request):
    if request.method == "POST":
        usuario = request.POST["nombre_user"]
        contrasena = request.POST["contra_user"]
        user = authenticate(request, username=usuario, password=contrasena)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context = {"mensaje": "El nombre de usuario o contraseña no es valido",
                       "current": "login"}
            return render(request, "tienda/login.html", context)
    else:
        context = {"current": "login"}
        return render(request, "tienda/login.html", context)

@login_required
def pago(request):
    if request.method== "POST":
        user= request.user 
        cliente= user.cliente
        pedido= Pedido.objects.get(f_cliente= cliente, current= True)
        pedido.current= False
        pedido.fecha_compra= date.today()
        envio= request.POST["customRadio"]
        if envio== False:
            pedido.envio= False
        pedido.save()
        return redirect('home')
    else:
        user= request.user 
        cliente= user.cliente
        pedido= Pedido.objects.get(f_cliente= cliente, current= True)
        registros= Record.objects.filter(pedido_FK= pedido)
        context = {"cliente": cliente,
                "pedido": pedido,
                "records": registros}
        return render(request, "tienda/pago.html", context)


def registro(request):
    if request.method == "POST":
        user_name = request.POST["nombre_user"]
        nombre = request.POST["nombre"]
        p_apellido = request.POST["pri_apellido"]
        s_apellido = request.POST["seg_apellido"]
        contrasena = request.POST["contra_user"]
        email = request.POST["email"]
        try:

            usuario = User.objects.get(username=user_name)

            mensaje = "Este nombre de usuario ya está siendo ocupado"
            context = {
                "mensaje": mensaje
            }
            return render(request, "tienda/registro.html", context)
        except:
            user = User.objects.create_user(user_name, email, contrasena)
            user.save()
            cliente = Cliente.objects.create(
                user=user,
                nombre=nombre,
                primer_apellido=p_apellido,
                segundo_apellido=s_apellido,
                direccion=None,
                telefono=None

            )
            cliente.save()
            login(request, user)
            return redirect('home')
    else:
        return render(request, "tienda/registro.html", {})
