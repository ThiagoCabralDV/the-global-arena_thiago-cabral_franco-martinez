import random
from abc import ABC, abstractmethod
from encuentros.models import Encuentro
from .models import Fase

class BracketStrategy(ABC):
    @abstractmethod
    def generar_bracket(self, torneo, inscritos):
        pass

class SingleEliminationStrategy(BracketStrategy):
    def generar_bracket(self, torneo, inscritos):
        # Mezclamos los inscriptos de forma aleatoria (Sembrado aleatorio)
        list_inscritos = list(inscritos)
        random.shuffle(list_inscritos)
        jugadores = [i.usuario for i in list_inscritos]

        # Creamos la Ronda 1 usando los modelos existentes
        fase = Fase.objects.create(
            torneo=torneo,
            nombre='Ronda 1',
            orden=1,
            estado='En curso'
        )

        # Emparejamos de a dos
        for i in range(0, len(jugadores) - 1, 2):
            Encuentro.objects.create(
                torneo=torneo,
                fase=fase,
                jugador1=jugadores[i],
                jugador2=jugadores[i + 1],
                estado='PEN'
            )

        # Si hay un número impar, el último jugador queda libre (BYE) y pasa directo
        jugador_libre = jugadores[-1] if len(jugadores) % 2 != 0 else None
        
        return fase, jugador_libre