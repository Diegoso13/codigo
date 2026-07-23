from rest_framework import serializers
from ..models import MovimientoExtension

class MovimientoExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoExtension
        fields = [
            "ticket",
            "extension",
            "cliente",
            "direccion",
            "tipo",
            "division",
            "plataforma",
            "cedula",
            "usuario",
            "cargo",
            "tipo_movimiento",
            "marca",
            "fecha"
        ]