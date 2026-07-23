from rest_framework import serializers
import re
from ..models import Extension

# =========================
# VALIDADORES REUTILIZABLES
# =========================

def clean_str(value: str) -> str:
    return " ".join((value or "").strip().split())


def validate_extension(value: str, digits: int = 5) -> str:
    value = clean_str(value)

    if not value.isdigit():
        raise serializers.ValidationError("La extensión debe contener solo números.")

    if len(value) != digits:
        raise serializers.ValidationError(f"La extensión debe tener exactamente {digits} dígitos.")

    return value 

def validate_ticket(value: str, field_name: str, max_digits: int = 10) -> str:
    value = clean_str(value)

    if not value.isdigit():
        raise serializers.ValidationError({field_name: "Debe contener solo números."})

    if len(value) > max_digits:
        raise serializers.ValidationError({field_name: f"No puede tener más de {max_digits} dígitos."})

    return value 

def validate_regex(value: str, field_name: str, pattern: str, msg: str) -> str:
    value = clean_str(value)

    if not re.match(pattern, value, re.IGNORECASE):
        raise serializers.ValidationError({field_name: msg})

    return value

# =========================
# SERIALIZERS ESPECÍFICOS
# =========================

class ExtensionCreateSerializer(serializers.ModelSerializer):
    
    extension = serializers.CharField(write_only=True)
    tipo = serializers.CharField(write_only=True)
    division = serializers.CharField(write_only=True)
    plataforma = serializers.CharField(write_only=True)
    
    class Meta:
        model = Extension
        fields = ["extension", "tipo", "division", "plataforma"]
        
    def validate_extension(self, value):
        return validate_extension(value, digits=5)

    def validate(self, data):
        # Solo limpieza de forma
        return {
            key: clean_str(value) if isinstance(value, str) else value
            for key, value in data.items()
        }

class ExtensionAsignarSerializer(serializers.Serializer):
    
    extension = serializers.CharField()
    
    usuario = serializers.CharField()
    direccion = serializers.CharField()
    campana = serializers.CharField()
    sede = serializers.CharField()
    cliente2 = serializers.CharField()
    codigoceco = serializers.CharField()
    ceco = serializers.CharField()
    
    puesto_trabajo = serializers.CharField()
    ticket_solicitud = serializers.CharField()
    observacion = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="")
    
    def validate(self, data):

        # Limpieza general
        data = {
            key: clean_str(value) if isinstance(value, str) else value
            for key, value in data.items()
        }
        
        # EXTENSION: solo números y 5 dígitos
        data["extension"] = validate_extension(data.get("extension"), digits=5)
        
        # PUESTO TRABAJO: letras, números y -, no solo números
        data["puesto_trabajo"] = validate_regex(
            value=data.get("puesto_trabajo"),
            field_name="puesto_trabajo",
            pattern=r"^[a-z0-9áéíóúñ\-\s]+$",
            msg="El puesto de trabajo solo puede contener letras, números y guion (-)."
        ).upper()
        
        if data["puesto_trabajo"].isdigit():
            raise serializers.ValidationError({
                "puesto_trabajo": "El puesto de trabajo no puede contener solo números."
            })
        
        # TICKET SOLICITUD: solo números <= 10
        data["ticket_solicitud"] = validate_ticket(
            value=data.get("ticket_solicitud"),
            field_name="ticket_solicitud",
            max_digits=10
        )    
        
        return data

class ExtensionLiberarSerializer(serializers.Serializer):
    
    extension = serializers.CharField()
    ticket_eliminacion = serializers.CharField()
    observacion = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="")
    
    def validate(self, data):
        # Limpieza general
        data = {
            key: clean_str(value) if isinstance(value, str) else value
            for key, value in data.items()
        }
        
        # EXTENSION: solo números y 5 dígitos
        data["extension"] = validate_extension(data.get("extension"), digits=5) 
        
        data["ticket_eliminacion"] = validate_ticket(
            value=data.get("ticket_eliminacion"),
            field_name="ticket_eliminacion",
            max_digits=10
        )

        return data   
    
         
class ExtensionDatosAsignacionSerializer(serializers.Serializer):    
    
    direccion = serializers.CharField()
    campana = serializers.CharField()
    sede = serializers.CharField()
    cliente2 = serializers.CharField()
    codigoceco = serializers.CharField()
    ceco = serializers.CharField()
    puesto_trabajo = serializers.CharField()
    observacion = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="")
    
    def validate(self, data):
    
    # Limpieza general
        data = {
            key: clean_str(value) if isinstance(value, str) else value
            for key, value in data.items()
        }
    
    # PUESTO TRABAJO: letras, números y -, no solo números
        data["puesto_trabajo"] = validate_regex(
            value=data.get("puesto_trabajo"),
            field_name="puesto_trabajo",
            pattern=r"^[a-z0-9áéíóúñ\-\s]+$",
            msg="El puesto de trabajo solo puede contener letras, números y guion (-)."
        )  
        
        if data["puesto_trabajo"].isdigit():
            raise serializers.ValidationError({
                "puesto_trabajo": "El puesto de trabajo no puede contener solo números."
            })
            
        
        return data    
    
class ExtensionTrasladoModificarSerializer(serializers.Serializer):

    extension1 = serializers.CharField()
    extension2 = serializers.CharField()   
    
    ticket = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    
    datos_extension1 = ExtensionDatosAsignacionSerializer()
    datos_extension2 = ExtensionDatosAsignacionSerializer()
    
    
    
    def validate(self, data):

        data = {
            key: clean_str(value) if isinstance(value, str) else value
            for key, value in data.items()
        }
        
        # TICKET SOLICITUD: solo números <= 10
        data["ticket"] = validate_ticket(
            value=data.get("ticket"),
            field_name="ticket",
            max_digits=10
        )    
        
        return data    
        
class ExtensionReadSerializer(serializers.ModelSerializer):
    
    tipo = serializers.CharField(source="id_tipo.tipo", read_only=True)
    direccion = serializers.CharField(source="id_direccion.direccion", read_only=True)
    division = serializers.CharField(source="id_division.division", read_only=True)
    campana = serializers.CharField(source="id_campana.campana", read_only=True)
    cliente2 = serializers.CharField(source="id_cliente2.cliente2", read_only=True)
    plataforma = serializers.CharField(source="id_plataforma.plataforma", read_only=True)
    sede = serializers.CharField(source="id_sede.sede", read_only=True)
    ceco = serializers.CharField(source="id_ceco.ceco", read_only=True)
    codigoceco = serializers.CharField(source="id_codigoceco.codigoceco", read_only=True)
    
    cargo = serializers.CharField(source="id_usuario.cargo", read_only=True)
    cliente = serializers.CharField(source="id_usuario.cliente", read_only=True)
    usuario = serializers.CharField(source="id_usuario.usuario", read_only=True)
    cedula = serializers.CharField(source="id_usuario.cedula", read_only=True)

    class Meta:
        model = Extension
        fields = [
            "tipo","direccion","division","campana","cliente2",
            "plataforma","sede","cargo","extension","cliente",
            "codigoceco","ceco","cedula","usuario","puesto_trabajo",
            "fecha_ultima_modificacion","ticket_solicitud","ticket_eliminacion",
            "estado","observacion",
        ]