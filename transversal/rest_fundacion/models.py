from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.


class Subscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=200)
    vigencia = models.DateField(default=timezone.now)

    def __str__(self):
        return self.usuario.username
