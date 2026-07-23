from rest_framework import viewsets, filters,status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from extensiones.filters import UsuarioFilter
from ..models import Usuario,Extension
from ..serializers.usuarios_serializer import UsuarioSerializer
from ..services.usuario_service import UsuarioService

class UsuarioViewSet(viewsets.ModelViewSet):
    
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UsuarioFilter
    search_fields = ["cliente", "cedula", "usuario", "cargo"]
    ordering_fields = ["usuario", "cliente", "cargo", "cedula"]
    ordering = ["usuario"]

    lookup_field = "usuario"
    
    def get_queryset(self):
        queryset = super().get_queryset()

        disponibles = self.request.query_params.get("disponibles")
        ocupados = self.request.query_params.get("ocupados")

        if disponibles == "true":
         queryset = queryset.exclude(extensiones__estado="CREADA")

        if ocupados == "true":
            queryset = queryset.filter(extensiones__estado="CREADA").distinct()
            
        return queryset
    
    def _execute_action(self, service_fn, instance=None, partial=False, response_status=status.HTTP_200_OK):
        """
        Ejecuta acciones create/update reutilizando validación y respuesta.
        """

        if instance:
            serializer = self.get_serializer(instance, data=self.request.data, partial=partial)
        else:
            serializer = self.get_serializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)

        if instance:
            result = service_fn(instance, serializer.validated_data)
        else:
            result = service_fn(serializer.validated_data)

        return Response(
            self.get_serializer(result).data,
            status=response_status
        )

    def create(self, request, *args, **kwargs):
        return self._execute_action(
            UsuarioService.crear_usuario,
            response_status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        usuario_obj = self.get_object()
        partial = kwargs.pop("partial", False)

        return self._execute_action(
            UsuarioService.editar_usuario,
            instance=usuario_obj,
            partial=partial,
            response_status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        usuario_obj = self.get_object()
        UsuarioService.eliminar_usuario(usuario_obj)

        return Response(
            {"mensaje": "Usuario eliminado correctamente."},
            status=status.HTTP_200_OK
        )                