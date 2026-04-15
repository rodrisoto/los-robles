from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.utils import timezone

from .models import Pacientes, Medicamentos, LotesMedicamento, Administraciones
from .forms import PacienteForm


# 🏠 Dashboard
@login_required
def dashboard(request):

    total_pacientes = Pacientes.objects.count()
    total_medicamentos = Medicamentos.objects.count()

    stock_bajo = LotesMedicamento.objects.filter(
        stock_actual__lte=F('stock_minimo')
    ).count()

    dosis_qs = Administraciones.objects.filter(
        estado='pendiente'
    )

    alertas = dosis_qs.count()

    ultimas_dosis = dosis_qs.select_related(
        'id_historial_dosis__id_tratamiento__id_paciente'
    ).order_by('fecha_hora_programada')[:5]

    return render(request, 'dashboard.html', {
        'total_pacientes': total_pacientes,
        'total_medicamentos': total_medicamentos,
        'stock_bajo': stock_bajo,
        'alertas': alertas,
        'ultimas_dosis': ultimas_dosis
    })


# 💊 Dosis pendientes
@login_required
def dosis_pendientes(request):

    dosis = Administraciones.objects.filter(
        estado='pendiente'
    ).select_related(
        'id_historial_dosis__id_tratamiento__id_paciente'
    ).order_by('fecha_hora_programada')

    return render(request, 'dosis.html', {
        'dosis': dosis
    })


# ✅ ADMINISTRAR DOSIS
@login_required
def administrar_dosis(request, id):

    dosis = get_object_or_404(Administraciones, id_administracion=id)

    dosis.estado = 'administrada'
    dosis.fecha_hora_administrada = timezone.now()
    dosis.id_usuario = request.user

    dosis.save()

    return redirect('dosis')


# 👤 LISTAR PACIENTES
@login_required
def pacientes_list(request):

    pacientes = Pacientes.objects.all().order_by('nombres')

    return render(request, 'pacientes.html', {
        'pacientes': pacientes
    })


# ➕ CREAR PACIENTE
@login_required
def paciente_create(request):

    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pacientes')
    else:
        form = PacienteForm()

    return render(request, 'paciente_form.html', {
        'form': form
    })


# ✏️ EDITAR PACIENTE
@login_required
def paciente_update(request, id):

    paciente = get_object_or_404(Pacientes, id_paciente=id)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('pacientes')
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'paciente_form.html', {
        'form': form
    })


# 🗑️ ELIMINAR PACIENTE
@login_required
def paciente_delete(request, id):

    paciente = get_object_or_404(Pacientes, id_paciente=id)
    paciente.delete()

    return redirect('pacientes')


# 💊 LISTAR MEDICAMENTOS
@login_required
def medicamentos_list(request):

    medicamentos = Medicamentos.objects.all().order_by('nombre_generico')

    return render(request, 'medicamentos.html', {
        'medicamentos': medicamentos
    })