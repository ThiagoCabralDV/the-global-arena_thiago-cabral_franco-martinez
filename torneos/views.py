# torneos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Torneo

# Importamos el controlador Singleton personalizado desde la estructura de carpetas de la cátedra
from torneos.singleton.tournament_manager import TournamentManager

def index(request):
    """
    Vista que renderiza la página de inicio (Home) de The Global Arena.
    """
    return render(request, 'index.html')

@login_required
def inscribir_a_torneo(request, torneo_id):
    """
    Vista (MVC) que actúa como interfaz entre el cliente (template) 
    y el controlador de negocio único (Singleton).
    """
    # 1. Buscamos el torneo en la Base de Datos o tiramos un error 404 si no existe
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    
    # 2. Recuperamos la INSTANCIA ÚNICA del manager (Singleton)
    manager = TournamentManager()
    
    # 3. Delegamos las reglas de negocio al mánager único
    exito, mensaje = manager.validar_y_registrar_jugador(torneo, request.user)
    
    # 4. Enviamos alertas visuales a la UI básica usando el framework de mensajes de Django
    if exito:
        messages.success(request, mensaje)
    else:
        messages.error(request, mensaje)
        
    # 5. Redireccionamos al usuario de vuelta al inicio
    return redirect('index')