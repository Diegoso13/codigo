from django.urls import path
from .views import login_view  # Importa tu nueva vista con serializador

urlpatterns = [
    # Esta será la ruta final: /api/auth/login/
    path('login/', login_view, name='login_api'),
]