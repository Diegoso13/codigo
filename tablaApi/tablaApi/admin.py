from django.contrib import admin
from .models import Usuario
from .models import Software, Sede, Ciudad, Propietario

admin.site.register(Usuario)
admin.site.register(Software)
admin.site.register(Sede)
admin.site.register(Ciudad)
admin.site.register(Propietario)