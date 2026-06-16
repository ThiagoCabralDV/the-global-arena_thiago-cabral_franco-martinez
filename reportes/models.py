from django.db import models
from django.contrib.auth.models import User
from torneos.models import Torneo

class Reporte(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'PEN', 'Pendiente'
        RESUELTO = 'RES', 'Resuelto'
        DESESTIMADO = 'DES', 'Desestimado'

    denunciante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reportes_emitidos')
    denunciado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reportes_recibidos')
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='reportes')
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=3, choices=Estado.choices, default=Estado.PENDIENTE)

    def __str__(self):
        return f"Reporte de {self.denunciante} contra {self.denunciado}"