from django.contrib import admin
from .models import Inscripcion

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'torneo', 'fecha_inscripcion', 'estado')
    list_filter = ('estado',)
    search_fields = ('usuario__username', 'torneo__nombre')