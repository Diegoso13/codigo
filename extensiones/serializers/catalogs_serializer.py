import re
from rest_framework import serializers
from ..models import(
    Campana, Cliente2, Direccion, 
    Division, Plataforma, Sede, 
    Tipo,Ceco,Codigoceco
)

class BaseCatalogSerializer(serializers.ModelSerializer):
    
    catalog_field = None

    # Configuración (se sobreescribe en hijos)
    min_length = 3
    allow_only_digits = False   # si False => no permite "123"
    pattern = r"^[a-z0-9áéíóúñ\s\-_]+$"
    error_msg = "Contiene caracteres no permitidos."

    def validate(self, data):

        field_name = self.catalog_field
        if not field_name:
            raise Exception("Debes definir catalog_field en el serializer hijo.")

        value = (data.get(field_name) or "").strip()
        value = " ".join(value.split())  # normalizar espacios

        # longitud mínima
        if len(value) < self.min_length:
            raise serializers.ValidationError({
                field_name: f"Debe tener mínimo {self.min_length} caracteres."
            })

        # no solo números
        if not self.allow_only_digits and value.isdigit():
            raise serializers.ValidationError({
                field_name: "No puede contener solo números."
            })
            
        # caracteres permitidos
        if not re.match(self.pattern, value, re.IGNORECASE):
            raise serializers.ValidationError({
                field_name: self.error_msg
            })
    
        # duplicado ignorando mayúsculas/minúsculas
        model = self.Meta.model
        qs = model.objects.filter(**{f"{field_name}__iexact": value})

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError({
                field_name: "Ya existe un registro con ese nombre."
            })

        data[field_name] = value
        return data

################################ TIPO ###############################        
class TipoSerializer(BaseCatalogSerializer):
    catalog_field = "tipo"
    pattern = r"^[a-záéíóúñ\s]+$"
    error_msg = "El tipo solo puede contener letras."

    class Meta:
        model = Tipo
        fields = ["tipo"]    
################################ DIRECCION ###############################
class DireccionSerializer(BaseCatalogSerializer):
    catalog_field = "direccion"
    pattern = r"^[a-z0-9áéíóúñ\s\-_]+$"
    error_msg = "La dirección solo puede contener letras, números, espacios, guion (-) y guion bajo (_)."

    class Meta:
        model = Direccion
        fields = ["direccion"]
################################ DIVISION ###############################
class DivisionSerializer(BaseCatalogSerializer):
    catalog_field = "division"
    pattern = r"^[a-záéíóúñ\s]+$"
    error_msg = "La división solo puede contener letras."

    class Meta:
        model = Division
        fields = ["division"] 
################################ SEDE ###############################                
class SedeSerializer(BaseCatalogSerializer):
    catalog_field = "sede"
    pattern = r"^[a-záéíóúñ\s]+$"
    error_msg = "La sede solo puede contener letras."

    class Meta:
        model = Sede
        fields = ["sede"] 
################################ CAMPANA ###############################        
class CampanaSerializer(BaseCatalogSerializer):
    catalog_field = "campana"
    pattern = r"^[a-z0-9áéíóúñ\s\-_]+$"
    error_msg = "La campaña solo puede contener letras, números, espacios, guion (-) y guion bajo (_)."

    class Meta:
        model = Campana
        fields = ["campana"]  
################################ PLATAFORMA ###############################             
class PlataformaSerializer(BaseCatalogSerializer):
    catalog_field = "plataforma"
    pattern = r"^[a-záéíóúñ\s]+$"
    error_msg = "La plataforma solo puede contener letras."

    class Meta:
        model = Plataforma
        fields = ["plataforma"]               
################################ CLIENTE2 ###############################
class Cliente2Serializer(BaseCatalogSerializer):
    catalog_field = "cliente2"
    pattern = r"^[a-z0-9áéíóúñ\s\-_]+$"
    error_msg = "El cliente2 solo puede contener letras, números, espacios, guion (-) y guion bajo (_)."

    class Meta:
        model = Cliente2
        fields = ["cliente2"]
################################ CECO ###############################
class CecoSerializer(BaseCatalogSerializer):
    catalog_field = "ceco"
    pattern = r"^[a-z0-9áéíóúñ\s]+$"
    error_msg = "El código CECO solo puede contener letras, números y espacios."

    class Meta:
        model = Ceco
        fields = ["ceco"]
        
################################ CODIGO CECO ###############################
class CodigocecoSerializer(BaseCatalogSerializer):
    catalog_field = "codigoceco"
    pattern = r"^[a-z0-9áéíóúñ\s\-_]+$"
    error_msg = "El CECO solo puede contener letras, números, espacios, guion (-) y guion bajo (_)."

    class Meta:
        model = Codigoceco
        fields = ["codigoceco"]                