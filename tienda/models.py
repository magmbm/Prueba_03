from django.db import models 

from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    id= models.IntegerField(db_column= 'game_id', primary_key= True)
    nombre= models.CharField(max_length= 60)
    precio= models.IntegerField()
    genero= models.CharField(max_length= 100)
    fecha_lanzamiento= models.DateField()
    imagen= models.CharField(max_length= 1000, default= "https://github.com/magmbm/SQL_img/blob/main/control-del-juego.png")
def __init__(self):
    return "Nombre del juego: " + str(self.nombre)

class Cliente(models.Model):

    user= models.OneToOneField(User, null= True, on_delete=models.CASCADE)
    nombre= models.CharField(max_length= 50)
    primer_apellido= models.CharField(max_length= 50)
    segundo_apellido= models.CharField(max_length= 50)
    direccion= models.CharField(max_length= 60, null= True)
    telefono= models.IntegerField(null=True)
def __init__(self):
    return "Nombre del Cliente: " + str(self.nombre)


class Pedido(models.Model):
    id= models.AutoField(db_column= 'pedido_id', primary_key= True)
    nro_productos= models.IntegerField()
    f_cliente= models.ForeignKey(Cliente, db_column='cli_FK', on_delete=models.CASCADE)
    envio= models.BooleanField(default= True)
    fecha_compra= models.DateField(null= True)
    current= models.BooleanField(default= True)
def __init__(self):
    return "Numero de pedido: " + str(self.id)

class Record(models.Model):
    f_game= models.ForeignKey(Game, db_column='game_FK', on_delete= models.CASCADE)
    pedido_FK= models.ForeignKey(Pedido, on_delete= models.CASCADE)
    cant= models.IntegerField()
    precio= models.IntegerField()