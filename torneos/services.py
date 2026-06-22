import random
from .models import Fase
from encuentros.models import Encuentro


def verificar_y_avanzar_fase(torneo):
    """
    Verifica si todos los encuentros de la fase actual están finalizados.
    Si es así, genera automáticamente la siguiente ronda con los ganadores.
    """
    fase_actual = torneo.fases.order_by('-orden').first()

    if not fase_actual:
        return

    encuentros = Encuentro.objects.filter(fase=fase_actual)

    if not encuentros.exists():
        return

    todos_finalizados = not encuentros.filter(estado='PEN').exists()

    if not todos_finalizados:
        return

    ganadores = [e.ganador for e in encuentros if e.ganador is not None]

    if len(ganadores) < 2:
        torneo.estado = torneo.Estado.FINALIZADO
        torneo.save()
        return

    random.shuffle(ganadores)

    nombre_fase = _nombre_siguiente_fase(len(ganadores))
    nueva_fase = Fase.objects.create(
        torneo=torneo,
        nombre=nombre_fase,
        orden=fase_actual.orden + 1,
        estado='En curso'
    )

    for i in range(0, len(ganadores) - 1, 2):
        Encuentro.objects.create(
            torneo=torneo,
            fase=nueva_fase,
            jugador1=ganadores[i],
            jugador2=ganadores[i + 1],
        )


def _nombre_siguiente_fase(cantidad_jugadores):
    """
    Devuelve el nombre de la fase según la cantidad de jugadores que quedan.
    Evita magic numbers usando un diccionario de mapeo.
    """
    nombres = {
        2: 'Final',
        4: 'Semifinal',
        8: 'Cuartos de Final',
        16: 'Octavos de Final',
    }
    return nombres.get(cantidad_jugadores, f'Ronda - {cantidad_jugadores} jugadores')