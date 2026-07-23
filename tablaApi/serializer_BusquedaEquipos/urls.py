from django.urls import path
from . import views

urlpatterns = [
    path('select/', views.buscar_equipos),      
    path('info_licencia/', views.licencia_equipo),       
    path('busqueda/', views.api_buscar_equipo),
    path('exportar/', views.api_exportar_todo), 
]