import uuid
from django.db import models
 
class Cliente2(models.Model):
    id_cliente2 = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente2 = models.CharField(max_length=60,unique=True, blank=False)
 
    class Meta:
        db_table = "clientes2"
 
    def __str__(self):
        return self.cliente2
    
