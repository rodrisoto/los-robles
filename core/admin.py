from django.contrib import admin
from .models import *

admin.site.register(Usuarios)
admin.site.register(Pacientes)
admin.site.register(Medicamentos)
admin.site.register(LotesMedicamento)
admin.site.register(Tratamientos)
admin.site.register(HistorialDosis)
admin.site.register(Administraciones)
admin.site.register(MovimientosStock)
admin.site.register(Alertas)

