import django_filters
from .models import Extension
from .models import Usuario

class UsuarioFilter(django_filters.FilterSet):
    cliente = django_filters.CharFilter(field_name="cliente", lookup_expr="icontains")
    usuario = django_filters.CharFilter(field_name="usuario", lookup_expr="icontains")
    cargo = django_filters.CharFilter(field_name="cargo", lookup_expr="icontains")
    cedula = django_filters.CharFilter(field_name="cedula", lookup_expr="icontains")

    class Meta:
        model = Usuario
        fields = ["cliente", "usuario", "cargo", "cedula"]

class ExtensionFilter(django_filters.FilterSet):
    
    plataforma = django_filters.CharFilter(field_name="id_plataforma__plataforma", lookup_expr="icontains")
    campana = django_filters.CharFilter(field_name="id_campana__campana", lookup_expr="icontains")
    cliente2 = django_filters.CharFilter(field_name="id_cliente2__cliente2", lookup_expr="icontains")
    cargo = django_filters.CharFilter(field_name="id_usuario__cargo", lookup_expr="icontains")
    sede = django_filters.CharFilter(field_name="id_sede__sede", lookup_expr="icontains")
    direccion = django_filters.CharFilter(field_name="id_direccion__direccion", lookup_expr="icontains")
    division = django_filters.CharFilter(field_name="id_division__division", lookup_expr="icontains")
    tipo = django_filters.CharFilter(field_name="id_tipo__tipo", lookup_expr="icontains")
    
    usuario = django_filters.CharFilter(field_name="id_usuario__usuario", lookup_expr="icontains")
    estado = django_filters.CharFilter(lookup_expr="icontains")
    extension = django_filters.CharFilter(lookup_expr="icontains")
    cedula = django_filters.CharFilter(field_name="id_usuario__cedula", lookup_expr="icontains")
    cliente = django_filters.CharFilter(field_name="id_usuario__cliente", lookup_expr="icontains")
    codigoceco = django_filters.CharFilter(field_name="id_codigoceco__codigoceco", lookup_expr="icontains")
    ceco = django_filters.CharFilter(field_name="id_ceco__ceco", lookup_expr="icontains")
    puesto_trabajo = django_filters.CharFilter(lookup_expr="icontains")
    ticket_solicitud = django_filters.CharFilter(lookup_expr="icontains")
    ticket_eliminacion = django_filters.CharFilter(lookup_expr="icontains")
    observacion = django_filters.CharFilter(lookup_expr="icontains")
    fecha_ultima_modificacion = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Extension
        fields = [
            "usuario","estado","extension",
            "cedula","cliente","codigoceco",
            "ceco","puesto_trabajo","fecha_ultima_modificacion",
            "ticket_solicitud","ticket_eliminacion","observacion",
        ]