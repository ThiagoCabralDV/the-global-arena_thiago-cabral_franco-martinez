from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Max, Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from torneos.models import Torneo
from encuentros.models import Encuentro
from .models import Reporte
from .forms import ReporteForm

def resultados_torneos(request):
    torneos = Torneo.objects.annotate(
        total_inscripciones=Count('inscripciones', distinct=True),
        total_encuentros=Count('encuentros', distinct=True),
    ).order_by('-fecha_inicio')

    data = []
    for t in torneos:
        fases = t.fases.all().order_by('orden')
        fases_data = []
        for f in fases:
            encuentros = f.encuentros.all()
            encuentros_data = []
            for e in encuentros:
                encuentros_data.append({
                    'jugador1': e.jugador1,
                    'jugador2': e.jugador2,
                    'puntaje_j1': e.puntaje_j1,
                    'puntaje_j2': e.puntaje_j2,
                    'estado': e.get_estado_display(),
                    'ganador': e.ganador,
                    'fecha': e.fecha_programada,
                })
            fases_data.append({
                'nombre': f.nombre,
                'orden': f.orden,
                'esta_completa': f.esta_completa,
                'estado': f.estado,
                'encuentros': encuentros_data,
            })
        data.append({
            'torneo': t,
            'total_inscripciones': t.total_inscripciones,
            'total_encuentros': t.total_encuentros,
            'fases': fases_data,
        })

    return render(request, 'reportes/resultados.html', {'torneos_data': data})


def rendimiento_jugadores(request):
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
            'total': total_fin,
            'wins': wins,
            'losses': losses,
            'win_pct': win_pct,
        })

    stats.sort(key=lambda x: (-x['wins'], -x['win_pct']))
    return render(request, 'reportes/rendimiento.html', {'stats': stats})


@login_required
def reportar_usuario(request, username):
    denunciado = get_object_or_404(User, username=username)

    if request.user == denunciado:
        messages.error(request, 'No podés reportarte a vos mismo.')
        return redirect('perfil_publico', username=username)

    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.denunciante = request.user
            reporte.denunciado = denunciado
            reporte.save()

            messages.success(request, f'Reportaste a {denunciado.username}. Un administrador lo revisará.')
            return redirect('perfil_publico', username=username)
        else:
            messages.error(request, 'Corregí los errores del formulario.')
    else:
        form = ReporteForm()

    return render(request, 'reportes/reportar.html', {
        'form': form,
        'denunciado': denunciado,
    })
