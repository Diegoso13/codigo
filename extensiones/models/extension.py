import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator 

from .tipo import Tipo
from .direccion import Direccion
from .division import Division
from .campana import Campana
from .cliente2 import Cliente2
from .plataforma import Plataforma
from .sede import Sede
from.usuario import Usuario
from .ceco import Ceco
from .codigoceco import Codigoceco

class Extension(models.Model):
    
    id_extension = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    extension = models.CharField(max_length=6, unique=True, blank=False,
                                 validators=[RegexValidator(regex=r'^\d+$', message='La extensión debe ser numérica')])
    id_usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, null=True, blank=True,
        db_column="id_usuario", related_name="extensiones",
    )
    
    id_direccion = models.ForeignKey(
        Direccion, on_delete=models.PROTECT, null=True, blank=True,
        db_column="id_direccion", related_name="extensiones",
    )
    id_tipo = models.ForeignKey(
        Tipo, on_delete=models.PROTECT, null=True, blank=True,
        db_column="id_tipo", related_name="extensiones",
    )
    id_division = models.ForeignKey(
        Division, on_delete=models.PROTECT, null=True, blank=True,
        db_column="id_division", related_name="extensiones",
    )
    id_campana = models.ForeignKey(
        Campana, on_delete=models.PROTECT, null=True, blank=True,
        db_column="id_campana", related_name="extensiones",
    )
    id_codigoceco = models.ForeignKey(
        Codigoceco, on_delete=models.PROTECT, null=True, blank=True,
        db_column="id_codigoceco", related_name="extensiones",
    )
    id_ceco = models.ForeignKey(
        Ceco, on_delete=models.PROTECT, null=True, blank=True,
        db_column="id_ceco", related_name="extensiones",
    )
    
    id_cliente2 = models.ForeignKey(
        Cliente2, on_delete=models.PROTECT, null=True, blank=True,
        db_column="id_cliente2", related_name="extensiones",
    )
    id_plataforma = models.ForeignKey(
        Plataforma, on_delete=models.PROTECT, null=True, blank=True,
        db_column="id_plataforma", related_name="extensiones",
    )
    
    puesto_trabajo = models.CharField(max_length=15, blank=True, null=True)
    
    id_sede = models.ForeignKey(
        Sede, on_delete=models.PROTECT, null=True, blank=True,
        db_column="id_sede", related_name="extensiones",
    )
    
    fecha_ultima_modificacion = models.DateField(auto_now=True)
    ticket_solicitud = models.TextField( blank=True, null=True)
    ticket_eliminacion = models.TextField( blank=True, null=True)
    estado = models.CharField(max_length=15,  blank=True, null=True)
    observacion = models.TextField( blank=True, null=True)
    
    class Meta:
        db_table = "extensiones"
        
    def __str__(self):
        return f"{self.extension}"
    
    def clean(self):
        # Ejemplo de validación universal
        if Extension.objects.filter(extension=self.extension).exclude(pk=self.pk).exists():
            raise ValidationError("Ya existe una extensión con este número.")
        
        if not self.extension.strip():
            raise ValidationError("El número de extensión no puede estar vacio.")

    
    


 
