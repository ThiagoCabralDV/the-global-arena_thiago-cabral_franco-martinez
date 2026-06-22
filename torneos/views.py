from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q                 # <- NUEVOS IMPORTS PARA LOS CONTADORES Y FILTROS
from django.contrib.auth.models import User           # <- NUEVO IMPORT PARA EL TOP DE JUGADORES
from .models import Torneo
from .forms import TorneoForm
from .singleton.tournament_manager import TournamentManager
from .strategies import SingleEliminationStrategy  # Patrón Strategy
from inscripciones.models import Inscripcion
from encuentros.models import Encuentro               # <- NUEVO IMPORT PARA TRAER LOS COMBATES

# ==========================================
# VISTAS BASE DE TORNEOS
# ==========================================

def index(request):
    # 1. Contadores dinámicos para el Hero
    total_torneos = Torneo.objects.count()
    total_jugadores = User.objects.count()
    total_combates = Encuentro.objects.count()

    # 2. Torneos Destacados: Traemos los 3 más recientes/próximos
    # Anotamos el conteo de inscripciones para mostrar cuántos jugadores van dinámicamente
    torneos_destacados = Torneo.objects.annotate(
        total_inscritos=Count('inscripciones', distinct=True)
    ).order_by('-fecha_inicio')[:3]

    # 3. Top Jugadores: Adaptamos la lógica de Franco para sacar el Top 4
    jugadores = User.objects.filter(
        Q(encuentros_j1__isnull=False) | Q(encuentros_j2__isnull=False)
    ).distinct()

    stats = []
    for j in jugadores:
        total_fin = Encuentro.objects.filter(
            Q(jugador1=j) | Q(jugador2=j), estado=Encuentro.Estado.FINALIZADO
        ).count()
        wins = Encuentro.objects.filter(ganador=j, estado=Encuentro.Estado.FINALIZADO).count()
        losses = total_fin - wins
        win_pct = round((wins / total_fin * 100), 1) if total_fin > 0 else 0
        
        stats.append({
            'jugador': j,
            'wins': wins,
            'losses': losses,
            'win_pct': win_pct,
        })

    # Ordenamos por más victorias y mejor winrate (igual que Franco) y agarramos los 4 mejores
    stats.sort(key=lambda x: (-x['wins'], -x['win_pct']))
    top_jugadores = stats[:4]

    context = {
        'total_torneos': total_torneos,
        'total_jugadores': total_jugadores,
        'total_combates': total_combates,
        'torneos_destacados': torneos_destacados,
        'top_jugadores': top_jugadores,
    }

    return render(request, 'index.html', context)

def lista_torneos(request):
    torneos = Torneo.objects.all().order_by('-fecha_inicio')
    return render(request, 'torneos/lista_torneos.html', {'torneos': torneos})

def detalle_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    inscripciones = Inscripcion.objects.filter(torneo=torneo).exclude(estado='CAN').select_related('usuario')
    ya_inscrito = False
    
    if request.user.is_authenticated:
        ya_inscrito = inscripciones.filter(usuario=request.user).exists()
        
    return render(request, 'torneos/detalle_torneo.html', {
        'torneo': torneo,
        'inscripciones': inscripciones,
        'ya_inscrito': ya_inscrito,
        'inscripto': ya_inscrito,  # Clonamos la variable como salvavidas por si Franco la usa así en otra vista
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
    manager = TournamentManager()  # Acoplado al Singleton correctamente
    exito, mensaje = manager.desinscribir_jugador(torneo, request.user)
    if exito:
        messages.success(request, mensaje)
    else:
        messages.error(request, mensaje)
    return redirect('detalle_torneo', torneo_id=torneo_id)

# ==========================================
# LÓGICA DE BRACKETS (PATRÓN STRATEGY)
# ==========================================

@login_required
def generar_bracket(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)

    # Validar que solo el dueño ejecute esto
    if request.user != torneo.organizador:
        messages.error(request, 'Solo el organizador puede generar el bracket.')
        return redirect('detalle_torneo', torneo_id=torneo_id)

    # Validar que no existan brackets previos
    if torneo.fases.exists():
        messages.warning(request, 'El bracket ya fue generado para este torneo.')
        return redirect('detalle_torneo', torneo_id=torneo_id)

    # Traer inscriptos válidos
    inscritos = Inscripcion.objects.filter(torneo=torneo).exclude(estado='CAN')

    if inscritos.count() < 2:
        messages.error(request, 'Se necesitan al menos 2 jugadores inscritos para generar el bracket.')
        return redirect('detalle_torneo', torneo_id=torneo_id)

    # Ejecución del Patrón Strategy delegando la lógica algorítmica
    estrategia = SingleEliminationStrategy()
    fase, jugador_libre = estrategia.generar_bracket(torneo, inscritos)

    if jugador_libre:
        messages.info(request, f'{jugador_libre.username} pasa directo a la siguiente ronda por número impar.')

    # Cambio de estado limpio
    torneo.estado = Torneo.Estado.EN_VIVO
    torneo.save()

    messages.success(request, '¡Bracket generado exitosamente con la estrategia de Eliminación Directa!')
    return redirect('ver_bracket', torneo_id=torneo_id)

def ver_bracket(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    fases = torneo.fases.all().order_by('orden').prefetch_related('encuentros')
    return render(request, 'torneos/bracket.html', {'torneo': torneo, 'fases': fases})