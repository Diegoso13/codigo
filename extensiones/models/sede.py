import uuid
from django.db import models
 
 
class Sede(models.Model):
    id_sede = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sede = models.CharField(max_length=20,unique=True, blank=False)
 
    class Meta:
        db_table = "sedes"
 
    def __str__(self):
        return self.sede
    
    