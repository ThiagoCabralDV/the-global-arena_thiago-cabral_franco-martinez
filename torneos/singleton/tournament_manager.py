from .tournament_instance import TournamentInstance

class TournamentManager(metaclass=TournamentInstance):
    """
    Controlador centralizado (Singleton) para manejar las reglas
    de negocio de los torneos en The Global Arena.
    """

    def validar_y_registrar_jugador(self, torneo, usuario):
        if torneo.cupo_maximo <= 0:
            return False, "El torneo alcanzó el cupo máximo de participantes."

        if usuario in torneo.jugadores.all():
            return False, "Ya estás inscrito en este torneo."

        torneo.jugadores.add(usuario)
        torneo.cupo_maximo -= 1
        torneo.save()

        return True, f"Inscripción exitosa al torneo {torneo.nombre}."