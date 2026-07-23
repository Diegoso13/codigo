from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Ofimatica1
from .serializers import EquipoSimpleSerializer, EquipoLicenciaSerializer, EquipoFullSerializer
from ..views import role_required 

# --- FUNCIÓN 1: Búsqueda para Selects (Uso general) ---
@api_view(['GET'])
def buscar_equipos(request):
    q = request.GET.get("q", "")
    equipos = Ofimatica1.objects.filter(nombre_equipo__icontains=q)[:10]
    serializer = EquipoSimpleSerializer(equipos, many=True)
    return Response(serializer.data)

# --- FUNCIÓN 2: Info de licencia para mostrar en Front ---
@api_view(['GET'])
def licencia_equipo(request):
    nombre = request.GET.get("equipo")
    try:
        equipo = Ofimatica1.objects.get(nombre_equipo=nombre)
        serializer = EquipoLicenciaSerializer(equipo)
        return Response(serializer.data)
    except Ofimatica1.DoesNotExist:
        return Response({"error": "Equipo no encontrado"}, status=404)

# --- FUNCIÓN 3: Búsqueda avanzada / Descarga (Con Roles) ---
@api_view(['GET'])
@role_required(allowed_roles=['admin', 'licenciamiento', 'consulta', 'mesa'])
def api_buscar_equipo(request):
    q = request.GET.get("q")
    user_rol = getattr(request.user, 'rol', None)

    # Bloqueo si intentan listar todo sin ser admin/licenciamiento
    if not q and user_rol == 'consulta':
        return Response({'error': 'No tienes permisos para descargar la base de datos.'}, status=403)

    if q:
        equipos = Ofimatica1.objects.filter(nombre_equipo__icontains=q)
    else:
        equipos = Ofimatica1.objects.all()

    serializer = EquipoFullSerializer(equipos, many=True)
    return Response(serializer.data)

# --- FUNCIÓN 4: Exportación total (Solo Admin) ---
@api_view(['GET'])
@role_required(allowed_roles=['admin', 'licenciamiento'])
def api_exportar_todo(request):
    try:
        equipos = Ofimatica1.objects.all()
        serializer = EquipoFullSerializer(equipos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)