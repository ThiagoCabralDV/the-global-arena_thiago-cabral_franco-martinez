from django.contrib import admin
from .models import Reporte

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('denunciante', 'denunciado', 'torneo', 'fecha', 'estado')
    list_filter = ('estado',)