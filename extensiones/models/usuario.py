import uuid
from django.db import models


class Usuario(models.Model):
    id_usuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    cliente = models.CharField(max_length=40, blank=False)
    cedula = models.CharField(max_length=15, blank= False)
    usuario = models.CharField(max_length=20, blank=False)
    cargo = models.CharField(max_length=40, blank=False)
    
    class Meta:
        db_table = 'usuarios'
        
    def __str__(self):
        return self.usuario
    