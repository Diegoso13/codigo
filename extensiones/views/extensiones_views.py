from openpyxl import Workbook
from openpyxl.styles import Font

from rest_framework import status, filters
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers.movimientos_serializer import MovimientoExtensionSerializer

from ..models import Extension
from ..serializers.extensiones_serializer import(
    ExtensionReadSerializer, 
    ExtensionCreateSerializer, 
    ExtensionAsignarSerializer, 
    ExtensionLiberarSerializer,
    ExtensionTrasladoModificarSerializer
)
from ..filters import ExtensionFilter
from ..services.extensiones_service import ExtensionService

class ExtensionViewSet(ModelViewSet):
    
    queryset = Extension.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExtensionFilter
    search_fields = ["extension", "id_usuario__usuario", "id_usuario__cedula", "estado", "id_usuario__cliente", "id_usuario__cargo", "id_codigoceco__codigoceco", "id_ceco__ceco", "puesto_trabajo", "ticket_solicitud", "ticket_eliminacion", "observacion", "id_tipo__tipo", "id_direccion__direccion", "id_division__division", "id_campana__campana", "id_cliente2__cliente2", "id_plataforma__plataforma", "id_sede__sede"]
    ordering_fields = ["extension", "fecha_ultima_modificacion"]
    
    SERIALIZER_MAP = {
        "list": ExtensionReadSerializer,
        "retrieve": ExtensionReadSerializer,
        "create": ExtensionCreateSerializer,
        "asignar": ExtensionAsignarSerializer,
        "reasignar": ExtensionAsignarSerializer,
        "liberar": ExtensionLiberarSerializer,
        "trasladar_modificar": ExtensionTrasladoModificarSerializer
    }
    
    def get_serializer_class(self):
        return self.SERIALIZER_MAP.get(self.action, ExtensionReadSerializer)
    
    def _execute_action(self, service_fn, response_status=status.HTTP_200_OK, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        result = service_fn(serializer.validated_data, **kwargs)

         # Caso 1: retorna (Extension, Movimiento)
        if isinstance(result, tuple) and len(result) == 2:
            obj1, obj2 = result

            # Si es traslado: ((ext1, ext2), (mov1, mov2))
            if isinstance(obj1, tuple) and isinstance(obj2, tuple):
                extensiones = obj1
                movimientos = obj2

                return Response(
                    {
                        "extensiones": ExtensionReadSerializer(extensiones, many=True).data,
                        "movimientos": MovimientoExtensionSerializer(movimientos, many=True).data
                    },
                    status=response_status
                )

            # Si es asignar/liberar normal: (extension, movimiento)
            extension_obj = obj1
            movimiento_obj = obj2

            return Response(
                {
                    "extension": ExtensionReadSerializer(extension_obj).data,
                    "movimiento": MovimientoExtensionSerializer(movimiento_obj).data
                },
                status=response_status
            )

        # Caso 2: retorna solo Extension
        return Response(
            ExtensionReadSerializer(result).data,
            status=response_status
        )
        
    def create(self, request, *args, **kwargs):
        return self._execute_action(ExtensionService.crear_extension, status.HTTP_201_CREATED)
        
    @action(detail=False, methods=["patch"], url_path="asignar")
    def asignar(self, request, *args, **kwargs):
         return self._execute_action(ExtensionService.asignar_extension, validar_disponible=True)
        
     
    @action(detail=False, methods=["patch"], url_path="liberar")
    def liberar(self, request,*args, **kwargs):
        return self._execute_action(ExtensionService.liberar_extension)
        
    @action(detail=False, methods=["patch"], url_path="reasignar")
    def reasignar(self, request,*args, **kwargs):
        return self._execute_action(ExtensionService.asignar_extension, validar_disponible=False)
 
    @action(detail=False, methods=["patch"], url_path="trasladar_modificar")
    def trasladar_modificar(self, request, *args, **kwargs):
        return self._execute_action(ExtensionService.trasladar_modificando)
    
    
    
    
    @action(detail=False, methods=["get"], url_path="export-excel")
    def export_excel(self, request, *args, **kwargs):
        
        queryset = self.filter_queryset(self.get_queryset()).select_related(
            "id_tipo", "id_direccion", "id_division", "id_campana",
            "id_cliente2", "id_plataforma", "id_sede", "id_usuario"
        )
        
        wb = Workbook()
        
        # ==================================================
        # HOJA 1: EXTENSIONES
        # ==================================================
        ws = wb.active
        ws.title = "Extensiones"

        headers = [
            "Extension", "Tipo", "Direccion", "Division", "Campana",
            "Cliente2", "Plataforma", "Sede",
            "Cliente", "Cedula", "Usuario", "Cargo",
            "Codigo CECO", "CECO", "Puesto Trabajo",
            "Fecha Ultima Modificacion",
            "Ticket Solicitud", "Ticket Eliminacion",
            "Estado", "Observacion"
        ]

        ws.append(headers)

        # Estilo encabezados
        for cell in ws[1]:
            cell.font = Font(bold=True)
            
        # Datos
        for ext in queryset:
            ws.append([
                ext.extension,
                ext.id_tipo.tipo if ext.id_tipo else "",
                ext.id_direccion.direccion if ext.id_direccion else "",
                ext.id_division.division if ext.id_division else "",
                ext.id_campana.campana if ext.id_campana else "",
                ext.id_cliente2.cliente2 if ext.id_cliente2 else "",
                ext.id_plataforma.plataforma if ext.id_plataforma else "",
                ext.id_sede.sede if ext.id_sede else "",

                ext.id_usuario.cliente if ext.id_usuario else "",
                ext.id_usuario.cedula if ext.id_usuario else "",
                ext.id_usuario.usuario if ext.id_usuario else "",
                ext.id_usuario.cargo if ext.id_usuario else "",

                ext.id_codigoceco.codigoceco if ext.id_codigoceco else "",
                ext.id_ceco.ceco if ext.id_ceco else "",
                ext.puesto_trabajo or "",

                ext.fecha_ultima_modificacion.strftime("%Y-%m-%d %H:%M:%S")
                if ext.fecha_ultima_modificacion else "",

                ext.ticket_solicitud or "",
                ext.ticket_eliminacion or "",
                ext.estado,
                ext.observacion or "",
            ])

        # Ajustar ancho automático de columnas
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter

            for cell in col:
                try:
                    max_length = max(max_length, len(str(cell.value)))
                except:
                    pass

            ws.column_dimensions[col_letter].width = max_length + 3    
            
        # ==================================================
        # RESPUESTA COMO ARCHIVO
        # ==================================================
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="extensiones.xlsx"'

        wb.save(response)
        return response     