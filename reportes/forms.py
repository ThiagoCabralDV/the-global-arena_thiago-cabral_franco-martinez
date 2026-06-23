from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control form-control-dark',
                'rows': 4,
                'placeholder': 'Describí el motivo del reporte...',
            }),
        }
        labels = {
            'descripcion': 'Motivo del reporte',
        }
