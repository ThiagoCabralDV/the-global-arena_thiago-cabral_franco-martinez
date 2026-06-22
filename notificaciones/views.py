from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notificacion


@login_required
def lista_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    no_leidas = notificaciones.filter(leida=False).count()
    return render(request, 'notificaciones/lista.html', {
        'notificaciones': notificaciones,
        'no_leidas': no_leidas,
    })


@login_required
def marcar_leida(request, notif_id):
    notif = get_object_or_404(Notificacion, pk=notif_id, usuario=request.user)
    notif.leida = True
    notif.save()
    return redirect('lista_notificaciones')


@login_required
def marcar_todas_leidas(request):
    Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
    messages.success(request, 'Todas las notificaciones marcadas como leídas.')
    return redirect('lista_notificaciones')