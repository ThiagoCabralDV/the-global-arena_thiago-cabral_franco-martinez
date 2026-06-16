from django.contrib import admin
from .models import Videojuego, Torneo, Fase

@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'genero')
    search_fields = ('nombre',)

@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'videojuego', 'organizador', 'fecha_inicio', 'estado', 'cupo_maximo')
    list_filter = ('estado', 'videojuego')
    search_fields = ('nombre',)

@admin.register(Fase)
class FaseAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'torneo', 'orden', 'esta_completa', 'estado')
    list_filter = ('esta_completa',)