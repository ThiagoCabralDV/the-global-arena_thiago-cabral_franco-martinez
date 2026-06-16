from django.db import models
from django.contrib.auth.models import User

class Videojuego(models.Model):
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Torneo(models.Model):
    class Estado(models.TextChoices):
        PROXIMO = 'PRX', 'Próximo'
        EN_VIVO = 'LIV', 'En Vivo'
        FINALIZADO = 'FIN', 'Finalizado'
        CANCELADO = 'CAN', 'Cancelado'

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateTimeField()
    estado = models.CharField(max_length=3, choices=Estado.choices, default=Estado.PROXIMO)
    cupo_maximo = models.PositiveIntegerField(default=16)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.PROTECT)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='torneos_organizados')

    def __str__(self):
        return self.nombre

class Fase(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='fases')
    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField()
    esta_completa = models.BooleanField(default=False)
    estado = models.CharField(max_length=50, default='Pendiente')

    def __str__(self):
        return f"{self.torneo.nombre} - {self.nombre}"