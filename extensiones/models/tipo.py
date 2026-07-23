import uuid
from django.db import models


class Tipo(models.Model):
    id_tipo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=40,unique=True, blank=False)
    
    class Meta:
        db_table = 'tipos'
        
    def __str__(self):
        return self.tipo
    
    