import uuid
from django.db import models
 
class Campana(models.Model):
    id_campana = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campana = models.CharField(max_length=20, unique=True, blank=False)
 
    class Meta:
        db_table = "campana"
 
    def __str__(self):
        return self.campana
    

 