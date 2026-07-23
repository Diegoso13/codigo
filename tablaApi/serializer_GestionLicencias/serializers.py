from rest_framework import serializers

class LicenciaBaseSerializer(serializers.Serializer):
    """Base para validaciones comunes"""
    nombre_equipo = serializers.CharField(max_length=100)
    usuario_licenciamiento = serializers.CharField(max_length=100)
    software = serializers.CharField(max_length=100)

class AsignarLicenciaSerializer(LicenciaBaseSerializer):
    usuario = serializers.CharField(max_length=100)
    propietario = serializers.CharField(max_length=100)
    sede = serializers.CharField(max_length=100)
    ciudad = serializers.CharField(max_length=100)
    ticket_asignacion = serializers.CharField(max_length=50)

class RecuperarLicenciaSerializer(serializers.Serializer):
    nombre_equipo = serializers.CharField(max_length=100)
    software = serializers.CharField(max_length=100)
    ticket_retiro = serializers.CharField(max_length=50)
    usuario_licenciamiento = serializers.CharField(max_length=100)

class TrasladoLicenciaSerializer(serializers.Serializer):
    equipo_origen = serializers.CharField(max_length=100)
    equipo_destino = serializers.CharField(max_length=100)
    ticket = serializers.CharField(max_length=50)
    usuario_destino = serializers.CharField(max_length=100)
    usuario_licenciamiento = serializers.CharField(max_length=100)
