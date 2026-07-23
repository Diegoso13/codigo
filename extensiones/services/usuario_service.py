from rest_framework.exceptions import ValidationError
from django.db import  transaction
from ..models import Usuario, Extension

class UsuarioService:
    
    # -------------------------------------------------------------------------
    # Helpers privados
    # -------------------------------------------------------------------------
    
    @staticmethod
    def _validar_unicos(data, usuario_actual=None):

        usuario = data.get("usuario")
        cedula = data.get("cedula")

        qs_usuario = Usuario.objects.filter(usuario=usuario)
        qs_cedula = Usuario.objects.filter(cedula=cedula)

        # Si es update, excluir el mismo registro
        if usuario_actual:
            qs_usuario = qs_usuario.exclude(pk=usuario_actual.pk)
            qs_cedula = qs_cedula.exclude(pk=usuario_actual.pk)

        if usuario and qs_usuario.exists():
            raise ValidationError({"usuario": "Ya existe un usuario con ese nombre de usuario."})

        # Si cedula es PENDIENTE no se valida unique
        if cedula and cedula != "PENDIENTE" and qs_cedula.exists():
            raise ValidationError({"cedula": "Ya existe un usuario con esa cédula."})
        
    # -------------------------------------------------------------------------
    # Servicios
    # -------------------------------------------------------------------------    
        
    @staticmethod
    @transaction.atomic
    def crear_usuario(data):
        UsuarioService._validar_unicos(data)
        return Usuario.objects.create(**data)
    
    @staticmethod
    def editar_usuario(usuario_obj, data):
        
        UsuarioService._validar_unicos(data, usuario_actual=usuario_obj)

        for key, value in data.items():
            setattr(usuario_obj, key, value)
            usuario_obj.save()
        
        return usuario_obj
    @staticmethod
    @transaction.atomic
    def eliminar_usuario(usuario_obj):

        # Validación de negocio: no eliminar si tiene extensiones asociadas
        if Extension.objects.filter(id_usuario=usuario_obj).exists():
            raise ValidationError({
                "usuario": "No se puede eliminar el usuario porque tiene extensiones asociadas."
            })

        usuario_obj.delete()