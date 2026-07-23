from rest_framework import serializers
from .models import Actividad, Usuario # Importamos tus modelos
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # Para personalizar el token JWT
from .models import Software, Sede, Ciudad, Propietario
from rest_framework import serializers

# Serializador para el modelo Actividad del calendario
class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'  # Esto incluye id, titulo, descripcion, fecha, color, etc.

# Serializer para el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol'] # Solo los campos que necesites mostrar


class SoftwareSerializer(serializers.ModelSerializer):

    class Meta:
        model = Software
        fields = '__all__'


class SedeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sede
        fields = '__all__'


class CiudadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ciudad
        fields = '__all__'


class PropietarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Propietario
        fields = '__all__'