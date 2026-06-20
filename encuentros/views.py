from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Encuentro
from .forms import ResultadoForm

@login_required
def cargar_resultado(request, encuentro_id):
    encuentro = get_object_or_404(Encuentro, pk=encuentro_id)

    if request.user != encuentro.torneo.organizador:
        messages.error(request, 'Solo el organizador del torneo puede cargar resultados.')
        return redirect('ver_bracket', torneo_id=encuentro.torneo.id)

    if encuentro.estado == 'FIN':
        messages.warning(request, 'Este encuentro ya fue finalizado.')
        return redirect('ver_bracket', torneo_id=encuentro.torneo.id)

    if request.method == 'POST':
        form = ResultadoForm(request.POST, instance=encuentro)
        if form.is_valid():
            if form.cleaned_data['puntaje_j1'] == form.cleaned_data['puntaje_j2']:
                messages.error(request, 'No puede haber empate, tiene que haber un ganador.')
            else:
                encuentro = form.save(commit=False)
                encuentro.save()
                encuentro.determinar_ganador()
                messages.success(request, f'Resultado cargado. Ganador: {encuentro.ganador.username}')
                return redirect('ver_bracket', torneo_id=encuentro.torneo.id)
    else:
        form = ResultadoForm(instance=encuentro)

    return render(request, 'encuentros/cargar_resultado.html', {'form': form, 'encuentro': encuentro})