from rest_framework import serializers
from .models import Subscripcion


class SubscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscripcion
        fields = ['usuario', 'vigencia', 'estado']
