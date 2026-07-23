from .extensiones_serializer import ExtensionReadSerializer, ExtensionCreateSerializer
from.usuarios_serializer import UsuarioSerializer
from .catalogs_serializer import(
    TipoSerializer,
    DireccionSerializer,
    DivisionSerializer,
    SedeSerializer,
    CampanaSerializer,
    PlataformaSerializer,
    Cliente2Serializer,
    CecoSerializer,
    CodigocecoSerializer)

__all__ = [
    "TipoSerializer",
    "DireccionSerializer",
    "DivisionSerializer",
    "SedeSerializer",
    "CampanaSerializer",
    "PlataformaSerializer",
    "Cliente2Serializer",
    "UsuarioSerializer",
    "ExtensionSerializer",
    "ExtensionReadSerializer",
    "ExtensionCreateSerializer",
    "CecoSerializer",
    "CodigocecoSerializer"
]