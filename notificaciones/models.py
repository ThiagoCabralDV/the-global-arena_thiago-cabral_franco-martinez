from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Notificacion(models.Model):
    class Tipo(models.TextChoices):
        INSCRIPCION = 'INS', 'Inscripción'
        DESINSCRIPCION = 'DES', 'Desinscripción'
        BAN = 'BAN', 'Baneo'
        UNBAN = 'UNB', 'Desbaneo'
        REPORTE = 'REP', 'Reporte'
        TORNEO_CANCELADO = 'CAN', 'Torneo Cancelado'
        TORNEO_EDITADO = 'EDI', 'Torneo Editado'

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    tipo = models.CharField(max_length=3, choices=Tipo.choices)
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.usuario.username}: {self.mensaje[:50]}"