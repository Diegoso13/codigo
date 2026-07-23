import uuid
from django.db import models
 
class Codigoceco(models.Model):
    id_codigoceco = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigoceco = models.CharField(max_length=60,unique=True, blank=False)
 
    class Meta:
        db_table = "codigoscecos"
 
    def __str__(self):
        return self.codigoceco