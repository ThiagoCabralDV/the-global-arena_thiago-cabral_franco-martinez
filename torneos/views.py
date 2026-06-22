from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Torneo
from .forms import TorneoForm
from .singleton.tournament_manager import TournamentManager
from .strategies import SingleEliminationStrategy
from inscripciones.models import Inscripcion

def index(request):
    torneos_recientes = Torneo.objects.all().order_by('-fecha_inicio')[:3]
    return render(request, 'index.html', {'torneos_recientes': torneos_recientes})

def lista_torneos(request):
    torneos = Torneo.objects.all().order_by('-fecha_inicio')
    return render(request, 'torneos/lista_torneos.html', {'torneos': torneos})

def detalle_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    inscripciones = Inscripcion.objects.filter(torneo=torneo).exclude(estado='CAN').select_related('usuario')
    inscripto = False

    if request.user.is_authenticated:
        inscripto = inscripciones.filter(usuario=request.user).exists()

    return render(request, 'torneos/detalle_torneo.html', {
        'torneo': torneo,
        'inscripciones': inscripciones,
        'inscripto': inscripto,
        'cupos_disponibles': torneo.cupo_maximo - inscripciones.count(),
    })

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

# ==========================================
# GESTIÓN DE INSCRIPCIONES (SINGLETON)
# ==========================================

@login_required
def inscribir_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    manager = TournamentManager()  # Uso de tu patrón Singleton
    exito, mensaje = manager.validar_y_registrar_jugador(torneo, request.user)
    if exito:
        messages.success(request, mensaje)
    else:
        messages.error(request, mensaje)
    return redirect('detalle_torneo', torneo_id=torneo_id)

@login_required
def desinscribir_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    manager = TournamentManager()
    exito, mensaje = manager.desinscribir_jugador(torneo, request.user)
    if exito:
        messages.success(request, mensaje)
    else:
        messages.error(request, mensaje)
    return redirect('detalle_torneo', torneo_id=torneo_id)


@login_required
def generar_bracket(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)

    if request.user != torneo.organizador:
        messages.error(request, 'Solo el organizador puede generar el bracket.')
        return redirect('detalle_torneo', torneo_id=torneo_id)

    if torneo.fases.exists():
        messages.warning(request, 'El bracket ya fue generado para este torneo.')
        return redirect('detalle_torneo', torneo_id=torneo_id)

    inscritos = Inscripcion.objects.filter(torneo=torneo).exclude(estado='CAN')

    if inscritos.count() < 2:
        messages.error(request, 'Se necesitan al menos 2 jugadores inscritos para generar el bracket.')
        return redirect('detalle_torneo', torneo_id=torneo_id)

    estrategia = SingleEliminationStrategy()
    fase, jugador_libre = estrategia.generar_bracket(torneo, inscritos)

    if jugador_libre:
        messages.info(request, f'{jugador_libre.username} pasa directo a la siguiente ronda por número impar.')

    torneo.estado = Torneo.Estado.EN_VIVO
    torneo.save()

    messages.success(request, '¡Bracket generado exitosamente con la estrategia de Eliminación Directa!')
    return redirect('ver_bracket', torneo_id=torneo_id)


def ver_bracket(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    fases = torneo.fases.all().order_by('orden').prefetch_related('encuentros')
    return render(request, 'torneos/bracket.html', {'torneo': torneo, 'fases': fases})
