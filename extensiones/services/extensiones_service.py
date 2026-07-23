from django.db import transaction
from rest_framework.exceptions import ValidationError
from ..models import Extension

from ..models import (
    Extension, Tipo, Direccion,
    Division, Sede, Campana, Plataforma, 
    Cliente2, Usuario,MovimientoExtension, Ceco, Codigoceco
)

class ExtensionService:
    
    # -------------------------------------------------------------------------
    # Helpers privados
    # -------------------------------------------------------------------------

    @staticmethod
    def _get_or_error(model, field_name, value, lock: bool = False):
        """
        Busca un objeto por campo exacto (case-insensitive si es string).
        Si lock=True usa select_for_update() para bloquear la fila.
        """
        if isinstance(value, str):
            lookup = {f"{field_name}__iexact": value.strip()}
        else:
            lookup = {field_name: value}

        qs = model.objects.all()
        
        if lock:
            qs = qs.select_for_update()

        try:
            return qs.get(**lookup)
        except model.DoesNotExist:
            raise ValidationError({field_name: f"'{value}' no existe."})

    @staticmethod
    def _acumular_ticket(actual, nuevo, campo):
        """Concatena tickets con separador."""
        return f"{actual} - {nuevo}" if actual else nuevo
    
    @staticmethod
    def _aplicar_datos_asignacion(extension_obj, data,ticket):
        """
        Reutiliza la lógica de asignación para actualizar campos de una extensión.
        (esto es lo que te evita duplicar código)
        """
        
        extension_obj.id_direccion = ExtensionService._get_or_error(Direccion, "direccion", data["direccion"])
        extension_obj.id_campana = ExtensionService._get_or_error(Campana, "campana", data["campana"])
        extension_obj.id_cliente2 = ExtensionService._get_or_error(Cliente2, "cliente2", data["cliente2"])
        extension_obj.id_sede = ExtensionService._get_or_error(Sede, "sede", data["sede"])
        extension_obj.id_codigoceco = ExtensionService._get_or_error(Codigoceco, "codigoceco", data["codigoceco"])
        extension_obj.id_ceco = ExtensionService._get_or_error(Ceco, "ceco", data["ceco"])
        
        extension_obj.puesto_trabajo = data["puesto_trabajo"]
        extension_obj.observacion = data.get("observacion") or ""
        
        # Ticket solicitud acumulativo
        extension_obj.ticket_solicitud = ExtensionService._acumular_ticket(
            extension_obj.ticket_solicitud,ticket,
            "ticket_solicitud"
        )
        
        return extension_obj
    
    @staticmethod
    def _registrar_movimiento(extension_obj, tipo_movimiento: str, marca: str, ticket: str = None):

        movimiento = MovimientoExtension.objects.create(
            
            ticket=ticket,
            extension=extension_obj.extension,
            cliente=extension_obj.id_usuario.cliente if extension_obj.id_usuario else None,
            cedula=extension_obj.id_usuario.cedula if extension_obj.id_usuario else None,
            usuario=extension_obj.id_usuario.usuario if extension_obj.id_usuario else None,
            cargo=extension_obj.id_usuario.cargo if extension_obj.id_usuario else None,

            direccion=extension_obj.id_direccion.direccion if extension_obj.id_direccion else None,
            tipo=extension_obj.id_tipo.tipo if extension_obj.id_tipo else None,
            division=extension_obj.id_division.division if extension_obj.id_division else None,
            plataforma=extension_obj.id_plataforma.plataforma if extension_obj.id_plataforma else None,

            tipo_movimiento=tipo_movimiento,
            marca=marca
        )
        
        return movimiento
    
    # -------------------------------------------------------------------------
    # Servicios
    # -------------------------------------------------------------------------
    
    @staticmethod
    @transaction.atomic
    def crear_extension(data: dict) -> Extension:
        extension_num = data["extension"]

        if Extension.objects.filter(extension=extension_num).exists():
            raise ValidationError({"extension": "Ya existe esa extensión."})

        # Resolución de FKs
        tipo = ExtensionService._get_or_error(Tipo, "tipo", data["tipo"])
        division = ExtensionService._get_or_error(Division, "division", data["division"])
        plataforma = ExtensionService._get_or_error(Plataforma, "plataforma", data["plataforma"])

        return Extension.objects.create(
            extension=extension_num,
            id_tipo=tipo,
            id_division=division,
            id_plataforma=plataforma,
            estado="DISPONIBLE",
        )
    
    @staticmethod
    @transaction.atomic
    def asignar_extension(data: dict, validar_disponible: bool = True) -> Extension:
        
        # Bloquea el registro para evitar asignaciones dobles simultáneas
        extension_obj = ExtensionService._get_or_error(
            Extension, "extension", data["extension"], lock=True
        )
        
        # =============================
        # VALIDACIÓN SEGÚN OPERACIÓN
        # =============================
        if validar_disponible:
            if extension_obj.estado != "DISPONIBLE":
                raise ValidationError({"estado": "Solo se puede asignar una extensión en estado DISPONIBLE."})
        else:
            if extension_obj.estado != "CREADA":
                raise ValidationError({"estado": "Solo se puede reasignar una extensión en estado CREADA."})

        usuario_obj = ExtensionService._get_or_error(Usuario, "usuario", data["usuario"])

        # =============================
        # SI EL USUARIO YA TIENE EXTENSION CREADA → LIBERARLA AUTOMÁTICAMENTE
        # =============================
        extension_creada_usuario = Extension.objects.filter(
            id_usuario=usuario_obj,
            estado="CREADA"
        ).first()
        
        # Solo libera si la extensión creada es distinta a la que se va a asignar/reasignar
        if extension_creada_usuario and extension_creada_usuario.extension != extension_obj.extension:
            ExtensionService.liberar_extension({
                "extension": extension_creada_usuario.extension,
                "ticket_eliminacion": data["ticket_solicitud"],
                "observacion": ""
            })
        
        # ===========
        # Asignar
        # ===========
        extension_obj.id_usuario = usuario_obj
        
         # ===========
        # campos foraneos
        # ===========
        
        extension_obj.id_direccion = ExtensionService._get_or_error(Direccion, "direccion", data["direccion"])
        extension_obj.id_campana = ExtensionService._get_or_error(Campana, "campana", data["campana"])
        extension_obj.id_cliente2 = ExtensionService._get_or_error(Cliente2, "cliente2", data["cliente2"])
        extension_obj.id_sede = ExtensionService._get_or_error(Sede, "sede", data["sede"])
        extension_obj.id_codigoceco = ExtensionService._get_or_error(Codigoceco, "codigoceco", data["codigoceco"])
        extension_obj.id_ceco = ExtensionService._get_or_error(Ceco, "ceco", data["ceco"])
        
        # ===========
        # campos directos
        # ===========
        
        extension_obj.puesto_trabajo = data["puesto_trabajo"]
        extension_obj.observacion = data.get("observacion", "")
        extension_obj.ticket_solicitud = ExtensionService._acumular_ticket(extension_obj.ticket_solicitud, data["ticket_solicitud"], "ticket_solicitud")
        
        extension_obj.estado = "CREADA"
        extension_obj.save()
        
        # ======================================================
        # MOVIMIENTO
        # ======================================================
        
        tipo_movimiento = "ASIGNACION" if validar_disponible else "REASIGNACION"
        
        movimiento = ExtensionService._registrar_movimiento(
            extension_obj,
            tipo_movimiento=tipo_movimiento,
            marca="CREAR",
            ticket=data.get("ticket_solicitud")
        )
        return extension_obj, movimiento
    
    
    @staticmethod
    @transaction.atomic
    def liberar_extension(data: dict) -> Extension:
        
        extension_obj = ExtensionService._get_or_error(
            Extension, "extension", data["extension"], lock=True
        )
        
        if extension_obj.estado != "CREADA":
            raise ValidationError({"estado": "Solo se puede liberar una extensión en estado CREADA."})

        extension_obj.ticket_eliminacion = ExtensionService._acumular_ticket(
            extension_obj.ticket_eliminacion,
            data["ticket_eliminacion"],
            "ticket_eliminacion"
        )
        
        extension_obj.observacion = data.get("observacion") or ""
        extension_obj.estado = "DISPONIBLE"
    
        extension_obj.save()
        
        movimiento = ExtensionService._registrar_movimiento(
            extension_obj,
            tipo_movimiento="LIBERACION",
            marca="LIBERAR",
            ticket=data.get("ticket_eliminacion")
        )
        return extension_obj, movimiento
    
    @staticmethod
    @transaction.atomic
    def trasladar_modificando(data: dict) -> tuple[Extension, Extension]:    
        
        ticket = data.get("ticket")
        
        extension1_num = data["extension1"]
        extension2_num = data["extension2"]

        datos_ext1 = data["datos_extension1"]
        datos_ext2 = data["datos_extension2"]
        
        # =========================
        # Obtener extensiones bloqueadas
        # =========================
        ext1 = Extension.objects.select_for_update().get(extension=extension1_num)
        ext2 = Extension.objects.select_for_update().get(extension=extension2_num)
        
        ext1.id_usuario, ext2.id_usuario = ext2.id_usuario, ext1.id_usuario
        
        # =========================
        # Aplicar datos por extensión
        # (IMPORTANTE: respetando cada una)
        # =========================
        ext1 = ExtensionService._aplicar_datos_asignacion(ext1, datos_ext1,ticket)
        ext2 = ExtensionService._aplicar_datos_asignacion(ext2, datos_ext2,ticket)
        
        # =========================
        # Guardar
        # =========================
        ext1.save()
        ext2.save()
        
        mov1 = ExtensionService._registrar_movimiento(ext1,tipo_movimiento="TRASLADO",marca="CREAR",ticket=ticket)
        mov2 = ExtensionService._registrar_movimiento(ext2,tipo_movimiento="TRASLADO",marca="CREAR",ticket=ticket)

        return (ext1, ext2), (mov1, mov2)
    
   
   