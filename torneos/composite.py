from abc import ABC, abstractmethod


class NodoBracket(ABC):
    """Componente base del patrón Composite."""

    @abstractmethod
    def obtener_ganadores(self):
        pass

    @abstractmethod
    def esta_completo(self):
        pass


class EncuentroLeaf(NodoBracket):
    """Hoja del árbol: representa un encuentro individual."""

    def __init__(self, encuentro):
        self.encuentro = encuentro

    def obtener_ganadores(self):
        if self.encuentro.ganador:
            return [self.encuentro.ganador]
        return []

    def esta_completo(self):
        return self.encuentro.estado == 'FIN'


class FaseComposite(NodoBracket):
    """Nodo compuesto: representa una fase que agrupa encuentros."""

    def __init__(self, nombre_fase):
        self.nombre_fase = nombre_fase
        self.hijos = []

    def agregar(self, componente: NodoBracket):
        self.hijos.append(componente)

    def obtener_ganadores(self):
        ganadores = []
        for hijo in self.hijos:
            ganadores.extend(hijo.obtener_ganadores())
        return ganadores

    def esta_completo(self):
        return all(hijo.esta_completo() for hijo in self.hijos)


class TorneoComposite(NodoBracket):
    """Nodo raíz: representa el torneo completo con todas sus fases."""

    def __init__(self, torneo):
        self.torneo = torneo
        self.fases = []

    def agregar(self, fase: FaseComposite):
        self.fases.append(fase)

    def obtener_ganadores(self):
        if not self.fases:
            return []
        ultima_fase = self.fases[-1]
        return ultima_fase.obtener_ganadores()

    def esta_completo(self):
        return all(fase.esta_completo() for fase in self.fases)

    def obtener_campeon(self):
        ganadores = self.obtener_ganadores()
        if self.esta_completo() and len(ganadores) == 1:
            return ganadores[0]
        return None