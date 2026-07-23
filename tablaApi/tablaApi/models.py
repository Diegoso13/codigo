# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from rest_framework import serializers


class Ofimatica1(models.Model):
    nombre_equipo = models.CharField(max_length=17, blank=True, null=True)
    serial = models.CharField(max_length=54, blank=True, null=True)
    usuario = models.CharField(max_length=57, blank=True, null=True)
    software = models.CharField(max_length=85, blank=True, null=True)
    propietario = models.CharField(max_length=10, blank=True, null=True)
    sede = models.CharField(max_length=22, blank=True, null=True)
    ciudad = models.CharField(max_length=47, blank=True, null=True)
    ticket_asignacion = models.CharField(max_length=37, blank=True, null=True)
    ticket_traslado = models.CharField(max_length=75, blank=True, null=True)
    ticket_retiro = models.CharField(max_length=21, blank=True, null=True)
    fecha = models.CharField(max_length=20, blank=True, null=True)
    nueva = models.CharField(max_length=72, blank=True, null=True)
    estado = models.CharField(max_length=289, blank=True, null=True)
    notes = models.CharField(max_length=271, blank=True, null=True)
    observacion = models.CharField(max_length=81, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofimatica1'


class Usuario(AbstractUser):

    ROLES = (
        ('admin', 'Administrador'),
        ('licenciamiento', 'Licenciamiento'),
        ('consulta', 'Consulta'),
        ('mesa', 'Mesa'),
    )

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='consulta'
    )


# --------------------------------------------------------------------------------
# calendario
class Actividad(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()  # Formato YYYY-MM-DD
    color = models.CharField(max_length=50, default='Normal')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"
    
class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__' # Enviamos todos los campos a Vue


# --------------------------------------------------------------------------------
#               Selects

class Software(models.Model):

    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
class Sede(models.Model):

    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):

    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Propietario(models.Model):

    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre