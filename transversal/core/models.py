from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=11)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    comuna = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=6)
    comentario = models.CharField(max_length=500, null=True)


class Mascota(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre


class TipoProducto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    imagen = models.CharField(max_length=500)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    tipo_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    precio = models.IntegerField()
    precio_oferta = models.IntegerField(default=0)
    stock = models.IntegerField()
    ingreso = models.DateTimeField(
        editable=False, default=timezone.now)
    actualizacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class Promocion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    combo = models.IntegerField(null=True, blank=True)
    imagen = models.CharField(null=True, blank=True, max_length=500)
    minimo = models.IntegerField(null=True, blank=True)
    maximo = models.IntegerField(null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre


class Carro(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creacion = models.DateTimeField(editable=False, default=timezone.now)
    activo = models.IntegerField(default=1)


class CarroProducto(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.IntegerField(blank=True)
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class EstadoDespacho(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500, default='Preparando')

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now, editable=False)
    monto = models.IntegerField()
    productos = models.ForeignKey(Carro, on_delete=models.CASCADE)
    descuento = models.FloatField()

    def __str__(self):
        return self.usuario


class Despacho(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(default=timezone.now)
    origen = models.CharField(max_length=500)
    ubicacion = models.CharField(blank=True, max_length=500)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, default=0)
    estado = models.ForeignKey(EstadoDespacho, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
