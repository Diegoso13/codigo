from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ActividadViewSet
from .serializer_GestionLicencias.views import LicenciaViewSet
from .serializer_EdicionEquipos.views import EquipoViewSet

# Los views de catálogos aqui
from .serializer_Catalogos.views import SoftwareViewSet, SedeViewSet, CiudadViewSet, PropietarioViewSet

router = DefaultRouter()
router.register(r'actividades', ActividadViewSet)
router.register(r'gestion_licencias', LicenciaViewSet, basename='licencias_licencias')
router.register(r'edicion_equipos', EquipoViewSet, basename='edicion_equipos')

# 2. REGISTRA los catálogos directamente en este router central:
router.register(r'catalogos/software', SoftwareViewSet, basename='cat_software')
router.register(r'catalogos/sedes', SedeViewSet, basename='cat_sedes')
router.register(r'catalogos/ciudades', CiudadViewSet, basename='cat_ciudades')
router.register(r'catalogos/propietarios', PropietarioViewSet, basename='cat_propietarios')

urlpatterns = [
    path('api/busqueda/', include('tablaApi.serializer_BusquedaEquipos.urls')),
    path('api/auth/', include('tablaApi.serializer_LogIn.urls')),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Este se encarga de meter el "api/" a todo lo que esté en el router de arriba
    path('api/', include(router.urls)),
]