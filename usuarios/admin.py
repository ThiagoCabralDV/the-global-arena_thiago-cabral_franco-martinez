from django.contrib import admin
from .models import Administrador, Profile

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nivel_permiso', 'fecha_asignacion')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pais', 'telefono')