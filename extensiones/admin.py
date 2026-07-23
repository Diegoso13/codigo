from django.contrib import admin

from extensiones.models import (
    Tipo,
    Direccion,
    Division,
    Sede,
    Campana,
    Plataforma,
    Cliente2,
    Usuario,
    Ceco,
    Codigoceco,
    Extension,
    MovimientoExtension,
)

admin.site.register(Tipo)
admin.site.register(Direccion)
admin.site.register(Division)
admin.site.register(Sede)
admin.site.register(Campana)
admin.site.register(Plataforma)
admin.site.register(Cliente2)
admin.site.register(Usuario)
admin.site.register(Ceco)
admin.site.register(Codigoceco)
admin.site.register(Extension)
admin.site.register(MovimientoExtension)