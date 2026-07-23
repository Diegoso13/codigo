import uuid
from django.db import models
 
class Division(models.Model):
    id_division = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    division = models.CharField(max_length=20,unique=True, blank=False)
 
    class Meta:
        db_table = "division"
 
    def __str__(self):
        return self.division
    
    