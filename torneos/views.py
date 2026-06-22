from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.utils import timezone
from .models import Torneo
from .forms import TorneoForm
from .singleton.tournament_manager import TournamentManager
from .strategies import SingleEliminationStrategy
from inscripciones.models import Inscripcion
from reportes.models import Reporte
from usuarios.models import Profile
from notificaciones.notificador import notificador

def index(request):
    torneos_recientes = Torneo.objects.all().order_by('-fecha_inicio')[:3]
    return render(request, 'index.html', {'torneos_recientes': torneos_recientes})

def lista_torneos(request):
    torneos = Torneo.objects.all().order_by('-fecha_inicio')
    return render(request, 'torneos/lista_torneos.html', {'torneos': torneos})


def lista_jugadores(request):
    query = request.GET.get('q', '').strip()
    jugadores = User.objects.all().order_by('username')

    if query:
        jugadores = jugadores.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'torneos/lista_jugadores.html', {
        'jugadores': jugadores,
        'query': query,
    })

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
        notificador.notificar(request.user, mensaje, 'INS')
        notificador.notificar(torneo.organizador, f"{request.user.username} se inscribió en {torneo.nombre}", 'INS')
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
        notificador.notificar(request.user, mensaje, 'DES')
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


def es_admin(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(es_admin)
def panel_admin(request):
    total_usuarios = User.objects.count()
    total_torneos = Torneo.objects.count()
    reportes_pendientes = Reporte.objects.filter(estado='PEN').count()
    baneados = Profile.objects.filter(baneado=True).count()
    return render(request, 'admin/panel.html', {
        'total_usuarios': total_usuarios,
        'total_torneos': total_torneos,
        'reportes_pendientes': reportes_pendientes,
        'baneados': baneados,
    })


@login_required
@user_passes_test(es_admin)
def admin_usuarios(request):
    query = request.GET.get('q', '').strip()
    usuarios = User.objects.all().order_by('username')
    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, 'admin/usuarios.html', {'usuarios': usuarios, 'query': query})


@login_required
@user_passes_test(es_admin)
def admin_banear_usuario(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        motivo = request.POST.get('motivo', '')
        usuario.profile.baneado = True
        usuario.profile.motivo_ban = motivo
        usuario.profile.fecha_ban = timezone.now()
        usuario.profile.save()
        usuario.is_active = False
        usuario.save()
        messages.success(request, f'Usuario {usuario.username} baneado correctamente.')
        notificador.notificar(usuario, f"Fuiste baneado. Motivo: {motivo}", 'BAN')
    return redirect('admin_usuarios')


@login_required
@user_passes_test(es_admin)
def admin_desbanear_usuario(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    usuario.profile.baneado = False
    usuario.profile.motivo_ban = ''
    usuario.profile.fecha_ban = None
    usuario.profile.save()
    usuario.is_active = True
    usuario.save()
    messages.success(request, f'Usuario {usuario.username} desbaneado correctamente.')
    notificador.notificar(usuario, "Tu cuenta fue desbaneada.", 'UNB')
    return redirect('admin_usuarios')


@login_required
@user_passes_test(es_admin)
def admin_reportes(request):
    reportes = Reporte.objects.all().order_by('-fecha').select_related('denunciante', 'denunciado', 'torneo')
    return render(request, 'admin/reportes.html', {'reportes': reportes})


@login_required
@user_passes_test(es_admin)
def admin_resolver_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)
    reporte.estado = 'RES'
    reporte.save()
    messages.success(request, 'Reporte resuelto correctamente.')
    notificador.notificar(reporte.denunciante, f"Tu reporte contra {reporte.denunciado.username} fue resuelto.", 'REP')
    return redirect('admin_reportes')


@login_required
@user_passes_test(es_admin)
def admin_desestimar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)
    reporte.estado = 'DES'
    reporte.save()
    messages.success(request, 'Reporte desestimado.')
    notificador.notificar(reporte.denunciante, f"Tu reporte contra {reporte.denunciado.username} fue desestimado.", 'REP')
    return redirect('admin_reportes')


@login_required
@user_passes_test(es_admin)
def admin_torneos(request):
    query = request.GET.get('q', '').strip()
    torneos = Torneo.objects.all().order_by('-fecha_inicio')
    if query:
        torneos = torneos.filter(nombre__icontains=query)
    return render(request, 'admin/torneos.html', {'torneos': torneos, 'query': query})


@login_required
@user_passes_test(es_admin)
def admin_cancelar_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    torneo.estado = Torneo.Estado.CANCELADO
    torneo.save()
    inscriptos = Inscripcion.objects.filter(torneo=torneo).exclude(estado='CAN').select_related('usuario')
    for insc in inscriptos:
        notificador.notificar(insc.usuario, f"El torneo {torneo.nombre} fue cancelado.", 'CAN')
    notificador.notificar(torneo.organizador, f"Tu torneo {torneo.nombre} fue cancelado.", 'CAN')
    messages.success(request, f'Torneo "{torneo.nombre}" cancelado.')
    return redirect('admin_torneos')


@login_required
@user_passes_test(es_admin)
def admin_editar_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    if request.method == 'POST':
        form = TorneoForm(request.POST, instance=torneo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Torneo actualizado correctamente.')
            return redirect('admin_torneos')
        else:
            messages.error(request, 'Corregí los errores del formulario.')
    else:
        form = TorneoForm(instance=torneo)
    return render(request, 'admin/editar_torneo.html', {'form': form, 'torneo': torneo})
