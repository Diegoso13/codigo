from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
# Importa tu decorador (ajusta la ruta según tu estructura)
from ..views import role_required 

from ..models import Ofimatica1
from .serializers import EquipoSerializer

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Ofimatica1.objects.all()
    serializer_class = EquipoSerializer

    @method_decorator(role_required(allowed_roles=['admin', 'licenciamiento']))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Al guardar, pasamos todos los valores por defecto
            serializer.save(
                usuario="", software="", propietario="", sede="", 
                ciudad="", ticket_asignacion="", ticket_traslado="",
                ticket_retiro="", fecha="", nueva="", estado="",
                notes="", observacion=""
            )
            return Response({
                "status": "ok",
                "mensaje": "Equipo agregado correctamente"
            }, status=status.HTTP_201_CREATED)
        
        return Response({"status": "error", "mensaje": serializer.errors}, status=400)

    @method_decorator(role_required(allowed_roles=['admin', 'licenciamiento']))
    @action(detail=False, methods=['post'])
    def editar_nombre(self, request):
        nombre_actual = request.data.get("nombre_actual")
        nombre_nuevo = request.data.get("nombre_nuevo")
        serial_nuevo = request.data.get("serial_nuevo") # <--- CAPTURAMOS EL SERIAL

        try:
            # Buscamos el equipo por su nombre actual
            equipo = Ofimatica1.objects.get(nombre_equipo=nombre_actual)
            
            # Preparamos los datos para actualizar
            datos_actualizar = {
                "nombre_equipo": nombre_nuevo,
                "serial": serial_nuevo 
            }

            # partial=True permite que si algún dato no viene, no de error
            serializer = self.get_serializer(equipo, data=datos_actualizar, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "ok", 
                    "mensaje": "Equipo actualizado correctamente (Nombre y Serial)"
                })
            
            return Response({"status": "error", "mensaje": serializer.errors}, status=400)
            
        except Ofimatica1.DoesNotExist:
            return Response({"status": "error", "mensaje": "Equipo no encontrado"}, status=404)