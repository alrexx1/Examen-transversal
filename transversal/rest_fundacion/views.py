from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Subscripcion
from django.contrib.auth.models import User
from .serializers import SubscripcionSerializer
# Create your views here.


@csrf_exempt
@api_view(['GET', 'POST'])
def lista_subcriptores(request):
    """
    Lista todos los subcriptores
    """
    if request.method == 'GET':
        subcriptor = Subscripcion.objects.all()
        serializer = SubscripcionSerializer(subcriptor, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SubscripcionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
