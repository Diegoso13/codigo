from rest_framework import serializers
from ..models import Ofimatica1

# 1. Para el buscador del Select (Ligero)
class EquipoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ofimatica1
        fields = ['id', 'nombre_equipo']

# 2. Para la info de licencia en componentes (Específico)
class EquipoLicenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ofimatica1
        fields = ['software', 'propietario', 'sede', 'ciudad', 'estado']

# 3. Para ver todo o exportar (Completo)
class EquipoFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ofimatica1
        fields = '__all__'