from django import forms
from .models import Encuentro

class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Encuentro
        fields = ['puntaje_j1', 'puntaje_j2']
        widgets = {
            'puntaje_j1': forms.NumberInput(attrs={
                'class': 'form-control form-control-dark',
                'min': 0
            }),
            'puntaje_j2': forms.NumberInput(attrs={
                'class': 'form-control form-control-dark',
                'min': 0
            }),
        }