from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import (
    Software,
    Sede,
    Ciudad,
    Propietario
)

from .serializers import (
    SoftwareSerializer,
    SedeSerializer,
    CiudadSerializer,
    PropietarioSerializer,
)


# GET simples para selects
@api_view(['GET'])
def lista_software(request):

    datos = Software.objects.all().order_by('nombre')

    serializer = SoftwareSerializer(datos, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def lista_sedes(request):

    datos = Sede.objects.all().order_by('nombre')

    serializer = SedeSerializer(datos, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def lista_ciudades(request):

    datos = Ciudad.objects.all().order_by('nombre')

    serializer = CiudadSerializer(datos, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def lista_propietarios(request):

    datos = Propietario.objects.all().order_by('nombre')

    serializer = PropietarioSerializer(datos, many=True)

    return Response(serializer.data)


# CRUD completo
class SoftwareViewSet(viewsets.ModelViewSet):

    queryset = Software.objects.all().order_by('nombre')
    serializer_class = SoftwareSerializer
    permission_classes = [IsAuthenticated]


class SedeViewSet(viewsets.ModelViewSet):

    queryset = Sede.objects.all().order_by('nombre')
    serializer_class = SedeSerializer
    permission_classes = [IsAuthenticated]


class CiudadViewSet(viewsets.ModelViewSet):

    queryset = Ciudad.objects.all().order_by('nombre')
    serializer_class = CiudadSerializer
    permission_classes = [IsAuthenticated]


class PropietarioViewSet(viewsets.ModelViewSet):

    queryset = Propietario.objects.all().order_by('nombre')
    serializer_class = PropietarioSerializer
    permission_classes = [IsAuthenticated]
