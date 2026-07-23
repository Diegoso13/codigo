from functools import wraps

from django.http import JsonResponse
from rest_framework import permissions, viewsets

from .models import Actividad
from .serializers import ActividadSerializer


def role_required(allowed_roles=None):
    allowed_roles = allowed_roles or []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                return JsonResponse({'error': 'No autenticado o Token invalido'}, status=401)

            user_role = getattr(request.user, 'rol', None)

            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)

            return JsonResponse({
                'error': f'Acceso denegado. Tu rol es "{user_role}" y se requiere uno de {allowed_roles}'
            }, status=403)

        return _wrapped_view

    return decorator


class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all().order_by('fecha')
    serializer_class = ActividadSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
