from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from ..models import MovimientoExtension
from ..serializers.movimientos_serializer import MovimientoExtensionSerializer


class MovimientoExtensionViewSet(ReadOnlyModelViewSet):

    queryset = MovimientoExtension.objects.all()
    serializer_class = MovimientoExtensionSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ["tipo_movimiento", "marca", "usuario", "extension",]
    search_fields = ["ticket", "extension", "usuario", "cliente", "cedula"]
    ordering_fields = ["fecha"]
    ordering = ["-fecha"]