from django.urls import path
from .views import (
    dashboard,
    dosis_pendientes,
    administrar_dosis,
    pacientes_list,
    medicamentos_list,
    paciente_create,
    paciente_update,
    paciente_delete
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('dosis/', dosis_pendientes, name='dosis'),

    path('pacientes/', pacientes_list, name='pacientes'),
    path('pacientes/crear/', paciente_create, name='paciente_create'),
    path('pacientes/editar/<int:id>/', paciente_update, name='paciente_update'),
    path('pacientes/eliminar/<int:id>/', paciente_delete, name='paciente_delete'),

    path('medicamentos/', medicamentos_list, name='medicamentos'),

    path('administrar/<int:id>/', administrar_dosis, name='administrar_dosis'),
]