from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Reporte
from notificaciones.notificador import notificador


@receiver(post_save, sender=Reporte)
def notificar_admin_nuevo_reporte(sender, instance, created, **kwargs):
    if not created:
        return

    admins = User.objects.filter(is_staff=True)
    for admin in admins:
        notificador.notificar(
            admin,
            f'Nuevo reporte de {instance.denunciante.username} contra {instance.denunciado.username}: {instance.descripcion[:100]}',
            'REP'
        )
