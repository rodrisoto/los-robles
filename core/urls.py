from django.urls import path
from .views import dashboard, dosis_pendientes

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('dosis/', dosis_pendientes, name='dosis'),
]