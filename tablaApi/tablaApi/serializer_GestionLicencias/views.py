from django.utils import timezone
from django.db import transaction
from django.utils.decorators import method_decorator
from typing import Optional, cast

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Ofimatica1
from .serializers import (
    AsignarLicenciaSerializer, 
    RecuperarLicenciaSerializer, 
    TrasladoLicenciaSerializer
)
from ..views import role_required 


def append_value(current_value: Optional[str], new_value: str) -> str:
    return f"{current_value or ''}{new_value}"


class LicenciaViewSet(viewsets.ViewSet):
    
    @method_decorator(role_required(allowed_roles=['admin', 'licenciamiento']))
    @action(detail=False, methods=['post'])
    def asignar(self, request):
        serializer = AsignarLicenciaSerializer(data=request.data)
        if serializer.is_valid():
            d = cast(dict[str, str], serializer.validated_data)
            try:
                equipo = Ofimatica1.objects.get(nombre_equipo=d['nombre_equipo'])
                equipo.usuario = d['usuario']
                equipo.software = d['software']
                equipo.propietario = d['propietario']
                equipo.sede = d['sede']
                equipo.ciudad = d['ciudad']
                equipo.ticket_asignacion = append_value(
                    equipo.ticket_asignacion,
                    f"-{d['ticket_asignacion']}"
                )
                equipo.fecha = str(timezone.localdate())
                equipo.notes = append_value(
                    equipo.notes,
                    f"-A-{d['software']}-TK{d['ticket_asignacion']}-{d['usuario_licenciamiento']}"
                )
                equipo.nueva = "Nueva"
                equipo.estado = "Asignada"
                equipo.save()
                return Response({"status": "ok", "mensaje": "Licencia asignada correctamente"})
            except Ofimatica1.DoesNotExist:
                return Response({"status": "error", "mensaje": "Equipo no encontrado"}, status=404)
        return Response(serializer.errors, status=400)

    @method_decorator(role_required(allowed_roles=['admin', 'licenciamiento']))
    @action(detail=False, methods=['post'])
    def recuperar(self, request):
        serializer = RecuperarLicenciaSerializer(data=request.data)
        if serializer.is_valid():
            d = cast(dict[str, str], serializer.validated_data)
            try:
                equipo = Ofimatica1.objects.get(nombre_equipo=d['nombre_equipo'])
                equipo.usuario = ""
                equipo.ticket_retiro = append_value(
                    equipo.ticket_retiro,
                    f"-{d['ticket_retiro']}"
                )
                equipo.fecha = str(timezone.localdate())
                equipo.notes = append_value(
                    equipo.notes,
                    f"-R-{d['software']}-TK{d['ticket_retiro']}-{d['usuario_licenciamiento']}"
                )
                equipo.nueva = ""
                equipo.estado = "Recuperada"
                equipo.save()
                return Response({"status": "ok", "mensaje": "Licencia recuperada correctamente"})
            except Ofimatica1.DoesNotExist:
                return Response({"status": "error", "mensaje": "Equipo no encontrado"}, status=404)
        return Response(serializer.errors, status=400)

    @method_decorator(role_required(allowed_roles=['admin', 'licenciamiento']))
    @action(detail=False, methods=['post'])
    def trasladar(self, request):
        serializer = TrasladoLicenciaSerializer(data=request.data)
        if serializer.is_valid():
            d = cast(dict[str, str], serializer.validated_data)
            
            if d['equipo_origen'] == d['equipo_destino']:
                return Response({"status": "error", "mensaje": "Origen y destino no pueden ser iguales"}, status=400)

            try:
                with transaction.atomic():
                    origen = Ofimatica1.objects.select_for_update().get(nombre_equipo=d['equipo_origen'])
                    destino = Ofimatica1.objects.select_for_update().get(nombre_equipo=d['equipo_destino'])

                    if not origen.software or origen.estado != "Asignada":
                        return Response({"status": "error", "mensaje": "El origen no tiene licencia activa"}, status=400)

                    # Guardamos datos para el destino
                    software_temp = origen.software
                    propietario_temp = origen.propietario
                    sede_temp = origen.sede
                    ciudad_temp = origen.ciudad

                    # Actualizar ORIGEN
                    origen.ticket_traslado = f"-{d['ticket']}"
                    origen.fecha = str(timezone.localdate())
                    origen.nueva = ""
                    origen.estado = "Trasladada"
                    origen.notes = append_value(
                        origen.notes,
                        f"-T-{software_temp}-TK{d['ticket']}-{d['usuario_licenciamiento']}"
                    )
                    origen.save()

                    # Actualizar DESTINO
                    destino.usuario = d['usuario_destino']
                    destino.software = software_temp
                    destino.propietario = propietario_temp
                    destino.sede = sede_temp
                    destino.ciudad = ciudad_temp
                    destino.ticket_asignacion = append_value(
                        destino.ticket_asignacion,
                        d['ticket']
                    )
                    destino.fecha = str(timezone.localdate())
                    destino.nueva = "Trasladada"
                    destino.estado = "Asignada"
                    destino.notes = append_value(
                        destino.notes,
                        f"-A-{software_temp}-TK{d['ticket']}-{d['usuario_licenciamiento']}"
                    )
                    destino.save()

                return Response({"status": "ok", "mensaje": "Traslado exitoso"})
            except Ofimatica1.DoesNotExist:
                return Response({"status": "error", "mensaje": "Uno de los equipos no existe"}, status=404)
        return Response(serializer.errors, status=400)
