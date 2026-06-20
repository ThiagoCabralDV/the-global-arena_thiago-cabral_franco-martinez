from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Torneo
from .forms import TorneoForm
from .singleton.tournament_manager import TournamentManager

def index(request):
    torneos_recientes = Torneo.objects.all().order_by('-fecha_inicio')[:3]
    return render(request, 'index.html', {'torneos_recientes': torneos_recientes})

def lista_torneos(request):
    torneos = Torneo.objects.all().order_by('-fecha_inicio')
    return render(request, 'torneos/lista_torneos.html', {'torneos': torneos})

def detalle_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    return render(request, 'torneos/detalle_torneo.html', {'torneo': torneo})

@login_required
def crear_torneo(request):
    if request.method == 'POST':
        form = TorneoForm(request.POST)
        if form.is_valid():
            torneo = form.save(commit=False)
            torneo.organizador = request.user
            torneo.save()
            messages.success(request, '¡Torneo creado exitosamente!')
            return redirect('lista_torneos')
        else:
            messages.error(request, 'Corregí los errores del formulario.')
    else:
        form = TorneoForm()
    return render(request, 'torneos/crear_torneo.html', {'form': form})

@login_required
def inscribir_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    manager = TournamentManager()
    exito, mensaje = manager.validar_y_registrar_jugador(torneo, request.user)
    if exito:
        messages.success(request, mensaje)
    else:
        messages.error(request, mensaje)
    return redirect('detalle_torneo', torneo_id=torneo_id)