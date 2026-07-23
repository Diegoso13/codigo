from rest_framework import viewsets, filters,status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.deletion import ProtectedError
from rest_framework.response import Response
from ..models import (
    Tipo, Campana, Cliente2, 
    Direccion, Division, Plataforma, 
    Sede, Ceco, Codigoceco
    )
from ..serializers.catalogs_serializer import (
    TipoSerializer, CampanaSerializer,  Cliente2Serializer, 
    DireccionSerializer, DivisionSerializer, PlataformaSerializer, 
    SedeSerializer, CecoSerializer, CodigocecoSerializer
    )

class BaseCatalogViewSet(viewsets.ModelViewSet):
    
    protected_message = "No se puede eliminar porque este registro está asociado a extensiones."
    lookup_field = None  # obligatorio en hijos
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    def get_queryset(self):
        return super().get_queryset().order_by(self.lookup_field)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ProtectedError:
            return Response(
                {"detail": self.protected_message},
                status=status.HTTP_400_BAD_REQUEST
            )
    @property
    def search_fields(self):
        return [self.lookup_field]

    @property
    def ordering_fields(self):
        return [self.lookup_field]
    
    @property
    def filterset_fields(self):
        return [self.lookup_field]        

############################### TIPO ###############################
class TipoViewSet(BaseCatalogViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer
    lookup_field = "tipo"
    protected_message = "No se puede eliminar este tipo porque está asociada a una o más extensiones."
################################ CAMPANA ###############################    
class CampanaViewSet(BaseCatalogViewSet):
    queryset = Campana.objects.all()
    serializer_class = CampanaSerializer
    lookup_field = "campana"    
    protected_message = "No se puede eliminar esta campaña porque está asociada a una o más extensiones."
############################### CLIENTE2 ###############################
class Cliente2ViewSet(BaseCatalogViewSet):
    queryset = Cliente2.objects.all()
    serializer_class = Cliente2Serializer
    lookup_field = "cliente2"
    protected_message = "No se puede eliminar este cliente porque está asociado a una o más extensiones."
################################ DIRECCION ###############################    
class DireccionViewSet(BaseCatalogViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer
    lookup_field = "direccion"
    protected_message = "No se puede eliminar esta dirección porque está asociada a una o más extensiones."
################################ DIVISION ###############################    
class DivisionViewSet(BaseCatalogViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    lookup_field = "division"   
    protected_message = "No se puede eliminar esta división porque está asociada a una o más extensiones."
################################ PLATAFORMA ###############################    
class PlataformaViewSet(BaseCatalogViewSet):
    queryset = Plataforma.objects.all()
    serializer_class = PlataformaSerializer
    lookup_field = "plataforma" 
    protected_message = "No se puede eliminar esta plataforma porque está asociada a una o más extensiones."
################################ SEDE ###############################    
class SedeViewSet(BaseCatalogViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer
    lookup_field = "sede"   
    protected_message = "No se puede eliminar esta sede porque está asociada a una o más extensiones."
################################ CECO ###############################    
class CecoViewSet(BaseCatalogViewSet):
    queryset = Ceco.objects.all()
    serializer_class = CecoSerializer
    lookup_field = "ceco"   
    protected_message = "No se puede eliminar este ceco porque está asociado a una o más extensiones."  
################################ CODIGO CECO ###############################
class CodigocecoViewSet(BaseCatalogViewSet):
    queryset = Codigoceco.objects.all()
    serializer_class = CodigocecoSerializer
    lookup_field = "codigoceco"
    protected_message = "No se puede eliminar este código de ceco porque está asociado a una o más extensiones."
