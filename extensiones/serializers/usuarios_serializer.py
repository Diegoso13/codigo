from rest_framework import serializers
import re
from ..models import Usuario

# =========================
# VALIDADORES REUTILIZABLES
# =========================

def clean_str(value: str) -> str:
    return " ".join((value or "").strip().split())

def validate_regex(value: str, field_name: str, pattern: str, msg: str) -> str:
    value = clean_str(value)

    if not re.match(pattern, value, re.IGNORECASE):
        raise serializers.ValidationError({field_name: msg})

    return value

# =========================
# SERIALIZER
# =========================

class UsuarioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Usuario
        fields = [ "cliente","cedula" ,"usuario","cargo"]
        
    def validate(self, data):
        
        # Limpieza general
        data = {
            key: clean_str(value) if isinstance(value, str) else value
            for key, value in data.items()
        }

        # -------------------------
        # CLIENTE
        # -------------------------
        
        cliente = data.get("cliente")
        data["cliente"] = validate_regex(
            cliente,
            "cliente",
            r"^[a-z0-9áéíóúñ_\-\s]+$",
            "El cliente solo puede contener letras, números, espacios, guion (-) y guion bajo (_)."
        )
        
        # No solo números
        if data["cliente"].isdigit():
            raise serializers.ValidationError({"cliente": "El cliente no puede contener solo números."})

        # -------------------------
        # CEDULA
        # -------------------------    
           
        cedula = data.get("cedula")
        
        if cedula.upper() == "PENDIENTE":
            data["cedula"] = "PENDIENTE"
        else:
            if not cedula.isdigit():
                raise serializers.ValidationError({
                    "cedula": "La cédula debe contener solo números o la palabra PENDIENTE."
                })

            if len(cedula) > 10:
                raise serializers.ValidationError({
                    "cedula": "La cédula no puede tener más de 10 dígitos."
                })
                
            if cedula == "0" * len(cedula):
                raise serializers.ValidationError({"cedula": "La cédula no puede ser solo ceros."})  
              
            data["cedula"] = cedula    
        # -------------------------
        # USUARIO
        # -------------------------
        
        usuario = data.get("usuario")
        usuario = validate_regex(
            usuario,
            "usuario",
            r"^[a-záéíóúñ]+$",
            "El usuario solo puede contener letras (sin números ni caracteres especiales)."
        )
        
        data["usuario"] = usuario.lower()
            
        # -------------------------
        # CARGO
        # -------------------------
        
        cargo = data.get("cargo")
        data["cargo"] = validate_regex(
            cargo,
            "cargo",
            r"^[a-záéíóúñ\s]+$",
            "El cargo solo puede contener letras y espacios."
        )  

        return data        
        
  

        