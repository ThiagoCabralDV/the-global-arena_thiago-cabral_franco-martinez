from django.db import models
from django.contrib.auth.models import User
from torneos.models import Torneo

class Inscripcion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'PEN', 'Pendiente'
        CONFIRMADO = 'CON', 'Confirmado'
        CANCELADO = 'CAN', 'Cancelado'

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=3, choices=Estado.choices, default=Estado.PENDIENTE)

    class Meta:
        unique_together = ('usuario', 'torneo')

    def __str__(self):
        return f"{self.usuario.username} - {self.torneo.nombre}"