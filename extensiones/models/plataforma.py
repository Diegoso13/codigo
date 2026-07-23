from django.db import models
import uuid
 
 
class Plataforma(models.Model):
    id_plataforma = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plataforma = models.CharField(max_length=20, unique=True, blank=False)
 
    class Meta:
        db_table = "plataformas"
 
    def __str__(self):
        return self.plataforma
    
    