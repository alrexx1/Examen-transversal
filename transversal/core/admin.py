from django.contrib import admin
from django.contrib.admin.helpers import AdminReadonlyField
from .models import Producto, TipoProducto, Mascota, EstadoDespacho
from rest_fundacion.models import Subscripcion

# Register your models here.
admin.site.register(Producto)
admin.site.register(TipoProducto)
admin.site.register(Mascota)
admin.site.register(Subscripcion)
admin.site.register(EstadoDespacho)
