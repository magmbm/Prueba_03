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
from django.core.paginator import Paginator


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
        cantidad= random.randint(3, 31)
        game= Game.objects.create(
            id=i,
            nombre=resultados.get('name'),
            precio=precio,
            genero=get_generos(resultados.get('genres')),
            fecha_lanzamiento=resultados.get('released'),
            cantidad= cantidad,
            valoracion= resultados.get('rating'),
            imagen=resultados.get('background_image')
        )
        game.save()
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
            if record.cant== 1:
                pedido.nro_productos= pedido.nro_productos - 1 
                pedido.total_precio= pedido.total_precio - game.precio
                record.delete()
                pedido.save()
            else:
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
        #variables en las sessiones para tener control de los registros
        if 'boton_id' in request.POST:
            id_c= request.POST["boton_id"]
            request.session["id"]= id_c
            solicitud= Contact.objects.get(id= id_c)
            return redirect('contact_details')

        elif 'boton-si' in request.POST:
            contactos= Contact.objects.filter(resuelta= True).order_by('id')
            if request.session["asunto-filtro"]!= "limpio":
                input= request.session["asunto-filtro"]
                contactos= contactos.filter(asunto__startswith= input)
            if request.session["email-filtro"]!= "limpio":
                contactos= contactos.filter(email_emisor__startswith= request.session["email-filtro"])
            if request.session["fecha-filtro"]!= "limpio":
                contactos= contactos.filter(fecha_emision__contains= request.session["fecha-filtro"])
            pagina = Paginator(contactos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            request.session["resuelta-filtro"]= True 
            context={"contact": contactos,
                     "pagina": pagina}
            return render(request, "tienda/crud_contact.html", context)
        elif 'boton-no' in request.POST:
            contactos= Contact.objects.filter(resuelta= False).order_by('id')
            if request.session["asunto-filtro"]!= "limpio":
                input= request.session["asunto-filtro"]
                contactos= contactos.filter(asunto__startswith= input)
            if request.session["email-filtro"]!= "limpio":
                contactos= contactos.filter(email_emisor__startswith= request.session["email-filtro"])
            if request.session["fecha-filtro"]!= "limpio":
                contactos= contactos.filter(fecha_emision__contains= request.session["fecha-filtro"])
            pagina = Paginator(contactos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            request.session["resuelta-filtro"]= True 
            context={"contact": contactos,
                     "pagina": pagina}
            return render(request, "tienda/crud_contact.html", context)
        elif 'search-asunto' in request.POST:
            input= request.POST["input-asunto"]
            request.session["asunto-filtro"]= input
            if request.session["id-filtro"]!= "limpio":
                contactos= Contact.objects.filter(id= request.session["id-filtro"])
                pagina = Paginator(contactos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                        "contact": contactos}
                return render(request, "tienda/crud_contact.html", context)
            contactos= Contact.objects.filter(asunto__startswith= input)
            if request.session["resuelta-filtro"]!= "limpio":
                contactos= contactos.filter(resuelta= request.session["resuelta-filtro"])
            if request.session["email-filtro"]!= "limpio":
                contactos= contactos.filter(email_emisor__startswith= request.session["email-filtro"])
            if request.session["fecha-filtro"]!= "limpio":
                contactos= contactos.filter(fecha_emision__contains= request.session["fecha-filtro"])
            pagina = Paginator(contactos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"contact": contactos,
                     "pagina": pagina}
            return render(request, "tienda/crud_contact.html", context)
        
        elif 'search-email' in request.POST:
            if request.session["id-filtro"]!= "limpio":
                contactos= Contact.objects.filter(id= request.session["id-filtro"])
                pagina = Paginator(contactos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                        "contact": contactos}
                return render(request, "tienda/crud_contact.html", context)
            input= request.POST["input-email"]
            request.session["email-filtro"]= input
            contactos= Contact.objects.filter(email_emisor__startswith= input)
            if request.session["asunto-filtro"]!= "limpio":
                input_asunto= request.session["asunto-filtro"]
                contactos= contactos.filter(asunto__startswith= input_asunto)
            if request.session["resuelta-filtro"]!= "limpio":
                contactos= contactos.filter(resuelta= request.session["resuelta-filtro"]) 
            if request.session["fecha-filtro"]!= "limpio":
                contactos= contactos.filter(fecha_emision__contains= request.session["fecha-filtro"])
            pagina = Paginator(contactos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"pagina": pagina,
                    "contact": contactos}
            return render(request, "tienda/crud_contact.html", context)
        elif 'search-id' in request.POST:
            input= request.POST["input-id"]
            request.session["id-filtro"]= input
            contactos= Contact.objects.filter(id= input)
            pagina = Paginator(contactos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"contact": contactos,
                     "pagina": pagina}
            return render(request, "tienda/crud_contact.html", context)
        elif 'search-fecha' in request.POST:
            if request.session["id-filtro"]!= "limpio":
                contactos= Contact.objects.filter(id= request.session["id-filtro"])
                pagina = Paginator(contactos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                        "contact": contactos}
                return render(request, "tienda/crud_contact.html", context)
            fecha= request.POST["input-fecha"]
            request.session["fecha-filtro"]= fecha
            contactos= Contact.objects.filter(fecha_emision__contains= fecha)
            if request.session["asunto-filtro"]!= "limpio":
                input_asunto= request.session["asunto-filtro"]
                contactos= contactos.filter(asunto__startswith= input_asunto)
            if request.session["resuelta-filtro"]!= "limpio":
                contactos= contactos.filter(resuelta= request.session["resuelta-filtro"]) 
            if request.session["email-filtro"]!= "limpio":
                contactos= contactos.filter(email_emisor__startswith= request.session["email-filtro"])
            pagina = Paginator(contactos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"contact": contactos,
                     "pagina": pagina}
            return render(request, "tienda/crud_contact.html", context)

        elif 'limpiar-filtro-resuelta' in request.POST:
            request.session["resuelta-filtro"]= "limpio"
            return redirect('crud_contact')
    else:
        if 'limpiar-filtros' in request.GET:
            request.session["asunto-filtro"]= "limpio"
            request.session["resuelta-filtro"]= "limpio"
            request.session["email-filtro"]= "limpio" 
            request.session["id-filtro"]= "limpio"
            request.session["fecha-filtro"]= "limpio"
            contactos= Contact.objects.get_queryset().order_by('id')
            pagina = Paginator(contactos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"pagina": pagina,
            "contact": contactos,
            }
            return render(request, "tienda/crud_contact.html", context)
        try:
            if request.session["asunto-filtro"]!= "limpio":
                input= request.session["asunto-filtro"]
                contactos= Contact.objects.filter(asunto__startswith= input) 
                if request.session["resuelta-filtro"]!= "limpio":
                    contactos= contactos.filter(resuelta= request.session["resuelta-filtro"])
                if request.session["email-filtro"]!= "limpio":
                    contactos= contactos.filter(email_emisor__startswith= request.session["email-filtro"]) 
                if request.session["fecha-filtro"]!= "limpio":
                    contactos= contactos.filter(fecha_emision__contains= request.session["fecha-filtro"])
                pagina = Paginator(contactos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                        "contact": contactos}
                return render(request, "tienda/crud_contact.html", context)
            elif request.session["resuelta-filtro"]!= "limpio":
                contactos= Contact.objects.filter(resuelta= request.session["resuelta-filtro"])
                if request.session["email-filtro"]!= "limpio":
                    contactos= contactos.filter(email_emisor__startswith= request.session["email-filtro"]) 
                if request.session["fecha-filtro"]!= "limpio":
                    contactos= contactos.filter(fecha_emision__contains= request.session["fecha-filtro"])
                if request.session["asunto-filtro"]!= "limpio":
                    input_asunto= request.session["asunto-filtro"]
                    contactos= contactos.filter(asunto__startswith= input_asunto)
                pagina = Paginator(contactos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                        "contact": contactos}
                context={}
                return render(request, "tienda/crud_contact.html", context)
            elif request.session["email-filtro"]!= "limpio":
                input= request.session["email-filtro"]
                contactos= Contact.objects.filter(email_emisor__startswith= input)
                if request.session["resuelta-filtro"]!= "limpio":
                    contactos= contactos.filter(resuelta= request.session["resuelta-filtro"])
                if request.session["fecha-filtro"]!= "limpio":
                    contactos= contactos.filter(fecha_emision__contains= request.session["fecha-filtro"])
                if request.session["asunto-filtro"]!= "limpio":
                    input_asunto= request.session["asunto-filtro"]
                    contactos= contactos.filter(asunto__startswith= input_asunto)
                pagina = Paginator(contactos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                         "contact": contactos}
                return render(request, "tienda/crud_contact.html", context)
            elif request.session["fecha-filtro"]!= "limpio":
                fecha= request.session["fecha-filtro"]
                contactos= Contact.objects.filter(fecha_emision__contains= fecha)
                if request.session["resuelta-filtro"]!= "limpio":
                    contactos= contactos.filter(resuelta= request.session["resuelta-filtro"])
                if request.session["email-filtro"]!= "limpio":
                    contactos= contactos.filter(email_emisor__startswith= request.session["email-filtro"]) 
                if request.session["asunto-filtro"]!= "limpio":
                    contactos= contactos.filter(asunto__startswith= request.session["asunto-filtro"])
                pagina = Paginator(contactos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                         "contact": contactos}
                return render(request, "tienda/crud_contact.html", context)
            else:
                contactos= Contact.objects.get_queryset().order_by('id')
                pagina = Paginator(contactos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                "contact": contactos,
                }
                return render(request, "tienda/crud_contact.html", context)
        except:
            contactos= Contact.objects.get_queryset().order_by('id')
            pagina = Paginator(contactos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"pagina": pagina,
            "contact": contactos,
            }
            return render(request, "tienda/crud_contact.html", context)

def contact_details(request ):
    if request.method== "POST":
        respuesta= request.POST["respuesta"]
        id_c= request.session["id"]
        solicitud= Contact.objects.get(id= id_c)
        solicitud.respuesta= respuesta
        solicitud.resuelta= True
        solicitud.save()
        return redirect('crud_contact')
    else:
        id_c= request.session["id"]
        solicitud= Contact.objects.get(id= id_c)
        solicitud.resuelta
        if solicitud.f_cliente== None:
            cli= True
            cliente= None
        else:
            cli= False
            cliente= solicitud.f_cliente
        context= {"solicitud": solicitud,
                  "cli": cli,
                  "cliente": cliente}
        return render(request, "tienda/contact_det.html", context)
    
    

def crud_pedido(request):
    if request.method== "POST":
        if 'id_boton' in request.POST:
            id_p= request.POST.get("id_boton")
            request.session["id"]= id_p
            return redirect('pedido_details')
        elif 'search-cliente' in request.POST:
            if request.session["id-filtro"]!= "limpio":
                pedidos= Pedido.objects.filter(id= request.session["id-filtro"])
                pagina = Paginator(pedidos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                        "pedidos": pedidos}
                return render(request, "tienda/crud_boleta.html", context)
            input_cli= request.POST["cliente-id"]
            request.session["cliente-filtro"]= input_cli
            cli= Cliente.objects.filter(name__startswith= input_cli)
            pedidos= Pedido.objects.filter(f_cliente= cli)
            if request.session["min-monto-filtro"]!= "limpio" & request.session["max-monto-filtro"]:
                min_val= request.session["min-monto-filtro"]
                max_val= request.session["max-monto-filtro"]
                pedidos= pedidos.filter(total_precio__range=(min_val, max_val)) 
            if request.session["productos-filtro"]!= "limpio":
                pedidos= pedidos.filter(nro_productos= request.session["productos-filtro"])
            if request.session["fecha-filtro"]!= "limpio":
                pedidos= pedidos.filter(fecha_compra__contains= request.session["fecha-filtro"])
            pagina = Paginator(pedidos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"pagina": pagina,
            "pedidos": pedidos,
            }
            return render(request, "tienda/crud_boleta.html", context)
        elif 'search-id' in request.POST:
            input_id= request.POST["pedido-id"]
            request.session["id-filtro"]= input_id
            pedidos= Pedido.objects.filter(id= int(input_id))
            pagina = Paginator(pedidos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"pagina": pagina,
            "pedidos": pedidos,
            }
            return render(request, "tienda/crud_boleta.html", context)
        elif 'search-productos' in request.POST:
            if request.session["id-filtro"]!= "limpio":
                pedidos= Pedido.objects.filter(id= request.session["id-filtro"])
                pagina = Paginator(pedidos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                        "pedidos": pedidos}
                return render(request, "tienda/crud_boleta.html", context)
            input_prod= request.POST["productos-id"]
            request.session["productos-filtro"]= input_prod
            pedidos= Pedido.objects.filter(nro_productos= input_prod)
            if request.session["min-monto-filtro"]!= "limpio":
                min_val= request.session["min-monto-filtro"]
                max_val= request.session["max-monto-filtro"]
                pedidos= pedidos.filter(total_precio__range=(min_val, max_val)) 
            if request.session["cliente-filtro"]!= "limpio":
                cli= Cliente.objects.filter(name__startswith= input_cli)
                pedidos= pedidos.filter(f_cliente= cli)
            if request.session["fecha-filtro"]!= "limpio":
                pedidos= pedidos.filter(fecha_compra__contains= request.session["fecha-filtro"])
            pagina = Paginator(pedidos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"pagina": pagina,
            "pedidos": pedidos,
            }
            return render(request, "tienda/crud_boleta.html", context)
        elif 'search-monto' in request.POST:
            if request.session["id-filtro"]!= "limpio":
                pedidos= Pedido.objects.filter(id= request.session["id-filtro"])
                pagina = Paginator(pedidos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                        "pedidos": pedidos}
                return render(request, "tienda/crud_boleta.html", context)
            min_val= request.POST["min-val"]
            max_val= request.POST["max-val"]
            request.session["min-monto-filtro"]= min_val
            request.session["max-monto-filtro"]= max_val
            pedidos= Pedido.objects.filter(total_precio__range=(min_val, max_val))
            if request.session["cliente-filtro"]!= "limpio":
                cli= Cliente.objects.filter(name__startswith= input_cli)
                pedidos= pedidos.filter(f_cliente= cli)
            if request.session["productos-filtro"]!= "limpio":
                pedidos= pedidos.filter(nro_productos= request.session["productos-filtro"])
            if request.session["fecha-filtro"]!= "limpio":
                pedidos= pedidos.filter(fecha_compra__contains= request.session["fecha-filtro"])
            pagina = Paginator(pedidos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"pagina": pagina,
            "pedidos": pedidos,
            }
            return render(request, "tienda/crud_boleta.html", context)
        elif 'search-fecha' in request.POST:
            if request.session["id-filtro"]!= "limpio":
                pedidos= Pedido.objects.filter(id= request.session["id-filtro"])
                pagina = Paginator(pedidos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                        "pedidos": pedidos}
                return render(request, "tienda/crud_boleta.html", context)
            fecha= request.POST["fecha-id"]
            request.session["fecha-filtro"]= fecha
            pedidos= Pedido.objects.filter(fecha_compra__contains= fecha) 
            if request.session["cliente-filtro"]!= "limpio":
                cli= Cliente.objects.filter(name__startswith= input_cli)
                pedidos= pedidos.filter(f_cliente= cli)
            if request.session["productos-filtro"]!= "limpio":
                pedidos= pedidos.filter(nro_productos= request.session["productos-filtro"])
            if request.session["min-monto-filtro"]!= "limpio":
                min_val= request.session["min-monto-filtro"]
                max_val= request.session["max-monto-filtro"]
                pedidos= pedidos.filter(total_precio__range=(min_val, max_val)) 
            pagina = Paginator(pedidos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"pagina": pagina,
            "pedidos": pedidos,
            }
            return render(request, "tienda/crud_boleta.html", context)

    else:
        if 'limpiar-filtros' in request.GET:
            request.session["monto-filtro"]= "limpio"
            request.session["cliente-filtro"]= "limpio"
            request.session["id-filtro"]= "limpio" 
            request.session["productos-filtro"]= "limpio"
            request.session["min-monto-filtro"]= "limpio"
            request.session["max-monto-filtro"]= "limpio"
            request.session["fecha-filtro"]= "limpio"
            pedidos= Pedido.objects.get_queryset().order_by('id')
            pagina = Paginator(pedidos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"pagina": pagina,
            "pedidos": pedidos,
            }
            return render(request, "tienda/crud_boleta.html", context)
        try:
            if request.session["monto-filtro"]!= "limpio":
                if request.session["id-filtro"]!= "limpio":
                    pedidos= Pedido.objects.filter(id= request.session["id-filtro"])
                    pagina = Paginator(pedidos, 5)
                    lista_pagina = request.GET.get('pagina')
                    pagina = pagina.get_page(lista_pagina)
                    context={"pagina": pagina,
                            "pedidos": pedidos}
                    return render(request, "tienda/crud_boleta.html", context)
                min_val= request.session["min-monto-filtro"]
                max_val= request.session["max-monto-filtro"]
                pedidos= Pedido.objects.filter(total_precio__range=(min_val, max_val)) 
                if request.session["cliente-filtro"]!= "limpio":
                    cli= Cliente.objects.filter(name__startswith= input_cli)
                    pedidos= pedidos.filter(f_cliente= cli)
                pagina = Paginator(pedidos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                        "pedidos": pedidos}
                return render(request, "tienda/crud_boleta.html", context)
            elif request.session["cliente-filtro"]!= "limpio":
                if request.session["id-filtro"]!= "limpio":
                    pedidos= Pedido.objects.filter(id= request.session["id-filtro"])
                    pagina = Paginator(pedidos, 5)
                    lista_pagina = request.GET.get('pagina')
                    pagina = pagina.get_page(lista_pagina)
                    context={"pagina": pagina,
                            "pedidos": pedidos}
                    return render(request, "tienda/crud_boleta.html", context)
                cliente= Cliente.objects.filter(nombre= request.session["cliente-filtro"])
                pedidos= Pedido.objects.filter(f_cliente= cliente)
                pagina = Paginator(pedidos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                        "pedidos": pedidos}
                return render(request, "tienda/crud_boleta.html", context)
            elif request.session["productos-filtro"]!= "limpio":
                if request.session["id-filtro"]!= "limpio":
                    pedidos= Pedido.objects.filter(id= request.session["id-filtro"])
                    pagina = Paginator(pedidos, 5)
                    lista_pagina = request.GET.get('pagina')
                    pagina = pagina.get_page(lista_pagina)
                    context={"pagina": pagina,
                            "pedidos": pedidos}
                    return render(request, "tienda/crud_boleta.html", context)
                pedidos= Pedido.objects.filter(nro_productos= request.session["productos-filtro"])
                pagina = Paginator(pedidos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                         "pedidos": pedidos}
                return render(request, "tienda/crud_boleta.html", context)
            elif request.session["fecha-filtro"]!= "limpio":
                fecha= request.session["fecha-filtro"]
                pedidos= Pedido.objects.filter(fecha_compra__contains= fecha) 
                pagina = Paginator(pedidos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                "pedidos": pedidos,
                }
                return render(request, "tienda/crud_boleta.html", context)
            else:
                pedidos= Pedido.objects.get_queryset().order_by('id')
                pagina = Paginator(pedidos, 5)
                lista_pagina = request.GET.get('pagina')
                pagina = pagina.get_page(lista_pagina)
                context={"pagina": pagina,
                "pedidos": pedidos,
                }
                return render(request, "tienda/crud_boleta.html", context)
        except:
            pedidos= Pedido.objects.get_queryset().order_by('id')
            pagina = Paginator(pedidos, 5)
            lista_pagina = request.GET.get('pagina')
            pagina = pagina.get_page(lista_pagina)
            context={"pedidos": pedidos,
                    "pagina": pagina}
            return render(request, "tienda/crud_boleta.html", context)

def pedido_details(request):
    pedido_id= request.session["id"]
    pedido= Pedido.objects.get(id= pedido_id)
    cliente= pedido.f_cliente
    context={"pedido": pedido,
             "cliente": cliente}
    return render(request, "tienda/pedido_det.html", context)

def change_pass(request):
    if request.method== "POST":
        try:
            usuario = request.user
            old_password= request.POST["old-pass"]
            user = authenticate(request, username=usuario, password=old_password)
        except:
            context={"mensaje": "No puede dejar ninguno de los campos vacios"}
            return render(request, "tienda/change_pass.html", context)
        if user is not None:
            new_password= request.POST["new-pass"]
            new_password_rep= request.POST["new-pass-rep"]
            if new_password== "" or new_password== " " or new_password_rep=="" or new_password==" ":
                context={"mensaje": "Debe ingresar las nuevas contraseñas para proceder"}
                return render(request, "tienda/change_pass.html", context)
            elif new_password_rep== new_password:
                user.set_password(new_password)
                user.save()
                return redirect('home') 
            else:
                context={"mensaje": "Las nuevas contraseñas no coinciden"}
                return render(request, "tienda/change_pass.html", context)
        else:
            context={"mensaje": "La contraseña antigua no es correcta"}
            return render(request, "tienda/change_pass.html", context)
    else:
        return render(request, "tienda/change_pass.html")

def perfil(request):
    if request.method== "POST":
        user= request.user
        cli= user.cliente
        try:
            if 'edit-btn' in request.POST:
                context = {"cliente": cli,
                        "usuario": user,
                        "mode": "edit"}
                return render(request, "tienda/perfil.html", context)
            
            elif 'guardar-btn' in request.POST:
                try:
                    nombre= request.POST["nombre"]
                    pri_apellido= request.POST["pri_apellido"]
                    seg_apellido= request.POST["seg_apellido"]
                    telefono= request.POST["telefono"]
                    direccion= request.POST["direccion"]
                    email= request.POST["email"]
                    username= request.POST["nombre_usuario"]

                    cli.nombre= nombre
                    cli.primer_apellido= pri_apellido
                    cli.segundo_apellido= seg_apellido
                    cli.telefono= telefono
                    cli.direccion= direccion
                    user.email= email
                    user.username= username
                    user.save()
                    cli.save()
                    
                    context = {"cliente": cli,
                            "usuario": user,
                            "mode": "no-edit"}
                    return render(request, "tienda/perfil.html", context)
                except: 
                    user= request.user
                    cli= user.cliente
                    context = {"cliente": cli,
                            "usuario": user,
                            "flag": "dos",
                            "mode": "edit"}
                    return render(request, "tienda/perfil.html", context)     
        except:
            return redirect('perfil')
    else:
        user= request.user
        cli= user.cliente
        context = {"cliente": cli,
                "usuario": user,
                "mode": "no-edit"}

        return render(request, "tienda/perfil.html", context)


def home(request):
    if request.user.is_superuser:
        context= {"current": "home",}
        return render(request, "tienda/index.html", context)
    else:
        context = {"current": "home"}
    return render(request, "tienda/index.html", context)


def tienda(request):
    if request.method== "POST":
        if 'game_id' in request.POST:
            request.session["id"]= request.POST["game_id"]
            return redirect('producto')
        elif 'boton-busqueda' in request.POST:
            input= request.POST["input-busqueda"]
            games= Game.objects.filter(nombre__startswith= input) 
            context={"games": games,
                     "current": "tienda",
                     "input": input}
            return render(request, "tienda/tienda.html", context)
    else:
        games= Game.objects.all()
        context = {"current": "tienda",
                "games": games,
                "input": ""}
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
            game_id = request.session["id"]
            game = Game.objects.get(id=game_id)
            game_cant = request.POST["prod-cantidad"]
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
            return redirect('login_t')
    else:
        game_id = request.session["id"]
        game = Game.objects.get(id= int(game_id))
        context = {"current": "tienda",
                   "game": game}
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
