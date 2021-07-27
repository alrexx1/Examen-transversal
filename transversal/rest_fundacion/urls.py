from django.urls import path
from .views import lista_subcriptores

urlpatterns = [
    path('lista_subcriptores', lista_subcriptores, name="lista_subcriptor")
]
