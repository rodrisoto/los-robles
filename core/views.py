from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Pacientes, Medicamentos, LotesMedicamento, Administraciones


# 🏠 Dashboard
@login_required
def dashboard(request):

    total_pacientes = Pacientes.objects.count()
    total_medicamentos = Medicamentos.objects.count()
    stock_bajo = LotesMedicamento.objects.filter(stock_actual__lt=10).count()
    alertas = Administraciones.objects.filter(estado='pendiente').count()

    return render(request, 'dashboard.html', {
        'total_pacientes': total_pacientes,
        'total_medicamentos': total_medicamentos,
        'stock_bajo': stock_bajo,
        'alertas': alertas
    })


# 💊 Dosis pendientes
@login_required
def dosis_pendientes(request):
    dosis = Administraciones.objects.filter(estado='pendiente')

    return render(request, 'dosis.html', {
        'dosis': dosis
    })