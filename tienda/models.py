from django.db import models 

# Create your models here.

class Game(models.Model):
    id= models.AutoField(db_column= 'game_id', primary_key= True)
    nombre= models.CharField(max_length= 60)
    precio= models.IntegerField()
    genero= models.CharField(max_length= 100)
    fecha_lanzamiento= models.DateField()
    descripcion= models.CharField(max_length= 120)
def __init__(self):
    return "Nombre del juego: " + str(self.nombre)

class Cliente(models.Model):
    id= models.AutoField(db_column= 'cli_id', primary_key= True)
    nombre= models.CharField(max_length= 50)
    rut= models.CharField(max_length= 12)
    primer_apellido= models.CharField(max_length= 50)
    segundo_apellido= models.CharField(max_length= 50)
    telefono= models.IntegerField()
def __init__(self):
    return "Nombre del Cliente: " + str(self.nombre)

class Pedido(models.Model):
    id= models.AutoField(db_column= 'pedido_id', primary_key= True)
    nro_productos= models.IntegerField()
    f_producto= models.ManyToManyField(Game, db_column='game_FK')
    f_cliente= models.ForeignKey(Cliente, db_column='cli_FK', on_delete=models.CASCADE)
    valor_total= models.IntegerField()
    envio= models.BooleanField(default= True)
def __init__(self):
    return "Numero de pedido: " + str(self.id)