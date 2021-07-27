
from django.forms import ModelForm, widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CarroProducto, Perfil
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name",
                  "last_name", "password1", "password2"]


class InsertProductForm(ModelForm):
    class Meta:
        model = CarroProducto
        fields = ["producto", "cantidad"]


class ProfileSendFrom(ModelForm):
    class Meta:
        model = Perfil
        fields = ['usuario', 'telefono', 'direccion',
                  'ciudad', 'comuna', 'codigo_postal', 'comentario']
        widgets = {'usuario': forms.HiddenInput()}
