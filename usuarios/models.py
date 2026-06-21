from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    pais = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


@receiver(post_save, sender=User)
def crear_o_guardar_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(usuario=instance)
    instance.profile.save()


class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrador')
    nivel_permiso = models.PositiveIntegerField(default=1)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin: {self.usuario.username}"