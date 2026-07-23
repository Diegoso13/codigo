from rest_framework import serializers

from ..models import (
    Software,
    Sede,
    Ciudad,
    Propietario
)


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
