from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Correo electrónico'
            }),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['foto_perfil', 'bio', 'telefono', 'pais', 'fecha_nacimiento']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Contá algo sobre vos...',
                'rows': 3
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Ej: +54 11 1234-5678'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Tu país'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control form-control-dark',
                'type': 'date'
            }),
        }
