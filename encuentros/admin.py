from django.contrib import admin
from .models import Encuentro

@admin.register(Encuentro)
class EncuentroAdmin(admin.ModelAdmin):
    list_display = ('torneo', 'fase', 'jugador1', 'jugador2', 'puntaje_j1', 'puntaje_j2', 'ganador', 'estado')
    list_filter = ('estado',)