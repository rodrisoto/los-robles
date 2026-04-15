from django import forms
from .models import Pacientes

class PacienteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="Fecha de Nacimiento"
    )

    class Meta:
        model = Pacientes
        fields = [
            'rut',
            'nombres',
            'apellidos',
            'habitacion',
            'fecha_nacimiento'
        ]
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'habitacion': forms.TextInput(attrs={'class': 'form-control'}),
        }