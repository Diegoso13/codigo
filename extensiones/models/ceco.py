import uuid
from django.db import models
 
class Ceco(models.Model):
    id_ceco = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ceco = models.CharField(max_length=60,unique=True, blank=False)
 
    class Meta:
        db_table = "cecos"
 
    def __str__(self):
        return self.ceco