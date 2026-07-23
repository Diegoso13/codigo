import uuid
from django.db import models

class Direccion(models.Model):
    id_direccion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    direccion = models.CharField(max_length=60,unique=True, blank=False)
 
    class Meta:
        db_table = "direcciones"
 
    def __str__(self):
        return self.direccion
    
