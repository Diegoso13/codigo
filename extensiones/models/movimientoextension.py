import uuid
from django.db import models

class MovimientoExtension(models.Model):
    
    TIPO_CHOICES = [
        ("ASIGNACION", "ASIGNACION"),
        ("REASIGNACION", "REASIGNACION"),
        ("TRASLADO", "TRASLADO"),
        ("LIBERACION", "LIBERACION"),
    ]

    MARCA_CHOICES = [
        ("CREAR", "CREAR"),
        ("TRASLADAR", "TRASLADAR"),
        ("LIBERAR", "LIBERAR"),
    ]
    
    id_movimiento = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.TextField(null=True, blank=True)
    extension = models.CharField(max_length=10)
    cliente = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=50, null=True, blank=True)
    division = models.CharField(max_length=50, null=True, blank=True)
    plataforma = models.CharField(max_length=50, null=True, blank=True)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    usuario = models.CharField(max_length=50, null=True, blank=True)
    cargo = models.CharField(max_length=50, null=True, blank=True)
    
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_CHOICES)
    marca = models.CharField(max_length=20, choices=MARCA_CHOICES)

    fecha = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        db_table = "movimientos_extensiones"
        ordering = ["-fecha"]
 
    def __str__(self):
        return f"{self.extension} - {self.tipo_movimiento} - {self.marca}"
    
