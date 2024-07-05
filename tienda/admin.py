from django.contrib import admin
from .models import Cliente, Pedido, Game, Record, Contact

# Register your models here.

admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Record)
admin.site.register(Game)
admin.site.register(Contact)