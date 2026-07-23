from django.urls import path, include
from rest_framework.routers import DefaultRouter

from extensiones.views.extensiones_views import ExtensionViewSet
from extensiones.views.movimientos_views import MovimientoExtensionViewSet
from ..views.catalogs_views import TipoViewSet
from ..views.catalogs_views import CampanaViewSet,Cliente2ViewSet, DireccionViewSet, DivisionViewSet, PlataformaViewSet, SedeViewSet, CecoViewSet, CodigocecoViewSet
from ..views.usuarios_views import UsuarioViewSet
    
router = DefaultRouter()

router.register(r'tipo', TipoViewSet, basename='tipo')
router.register(r'campana', CampanaViewSet, basename='campana')
router.register(r'cliente2', Cliente2ViewSet, basename='cliente2')
router.register(r'direccion', DireccionViewSet, basename='direccion')
router.register(r'division', DivisionViewSet, basename='division')
router.register(r'plataforma', PlataformaViewSet, basename='plataforma')
router.register(r'codigoceco', CodigocecoViewSet, basename='codigoceco')
router.register(r'ceco', CecoViewSet, basename='ceco')
router.register(r'sede', SedeViewSet, basename='sede')
router.register(r'usuario', UsuarioViewSet, basename='usuario')
router.register(r'extensiones', ExtensionViewSet, basename='extensiones')
router.register(r'movimientos', MovimientoExtensionViewSet, basename='movimientos')


urlpatterns = [
    path('', include(router.urls)),
]
