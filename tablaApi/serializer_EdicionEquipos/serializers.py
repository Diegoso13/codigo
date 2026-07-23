from rest_framework import serializers
from ..models import Ofimatica1

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ofimatica1
        # Solo exponemos los campos que nos interesan para agregar/editar
        fields = ['nombre_equipo', 'serial']

    # Aquí podemos poner validaciones personalizadas
    def validate_nombre_equipo(self, value):
        # Esta validación reemplaza tu "if Ofimatica1.objects.filter(...).exists()"
        # Solo se dispara al CREAR (si el nombre ya existe en la DB)
        if self.instance is None and Ofimatica1.objects.filter(nombre_equipo=value).exists():
            raise serializers.ValidationError("El equipo ya existe en el sistema")
        return value