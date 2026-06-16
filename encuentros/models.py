from django.db import models
from django.contrib.auth.models import User
from torneos.models import Torneo, Fase

class Encuentro(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'PEN', 'Pendiente'
        FINALIZADO = 'FIN', 'Finalizado'

    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='encuentros')
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, related_name='encuentros')
    jugador1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='encuentros_j1')
    jugador2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='encuentros_j2')
    puntaje_j1 = models.PositiveIntegerField(default=0)
    puntaje_j2 = models.PositiveIntegerField(default=0)
    fecha_programada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=3, choices=Estado.choices, default=Estado.PENDIENTE)
    ganador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='encuentros_ganados')

    def determinar_ganador(self):
        if self.puntaje_j1 > self.puntaje_j2:
            self.ganador = self.jugador1
        elif self.puntaje_j2 > self.puntaje_j1:
            self.ganador = self.jugador2
        self.estado = Encuentro.Estado.FINALIZADO
        self.save()

    def __str__(self):
        return f"{self.jugador1} vs {self.jugador2} - {self.torneo.nombre}"