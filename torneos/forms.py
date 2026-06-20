from django import forms
from .models import Torneo

class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['nombre', 'descripcion', 'videojuego', 'fecha_inicio', 'cupo_maximo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Nombre del torneo'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Descripción, reglas, premios...',
                'rows': 3
            }),
            'videojuego': forms.Select(attrs={
                'class': 'form-select form-control-dark',
            }),
            'fecha_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control form-control-dark',
                'type': 'datetime-local'
            }),
            'cupo_maximo': forms.NumberInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Ej: 16'
            }),
        }