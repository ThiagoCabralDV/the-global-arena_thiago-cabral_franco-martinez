from .tournament_instance import TournamentInstance

class TournamentManager(metaclass=TournamentInstance):
    """
    Controlador centralizado (Singleton) para manejar las reglas
    de negocio de los torneos en ArenaFGC.
    """

    def validar_y_registrar_jugador(self, torneo, usuario):
        from inscripciones.models import Inscripcion

        # 1. Contamos solo las inscripciones activas o pendientes (no canceladas)
        inscriptos = Inscripcion.objects.filter(torneo=torneo).exclude(estado='CAN').count()
        if inscriptos >= torneo.cupo_maximo:
            return False, "El torneo alcanzó el cupo máximo de participantes."

        # 2. Buscamos si el usuario ya tiene un registro histórico en este torneo
        inscripcion_previa = Inscripcion.objects.filter(torneo=torneo, usuario=usuario).first()

        if inscripcion_previa:
            if inscripcion_previa.estado != 'CAN':
                return False, "Ya estás inscrito en este torneo."
            else:
                # Si estaba cancelado, reactivamos su registro original para no violar el unique_together
                inscripcion_previa.estado = 'CON'
                inscripcion_previa.save()
                return True, f"Re-inscripción exitosa al torneo {torneo.nombre}."
        
        # 3. Si nunca se había anotado, creamos el registro limpio
        Inscripcion.objects.create(torneo=torneo, usuario=usuario, estado='CON')
        return True, f"Inscripción exitosa al torneo {torneo.nombre}."

    def desinscribir_jugador(self, torneo, usuario):
        from inscripciones.models import Inscripcion

        inscripcion = Inscripcion.objects.filter(torneo=torneo, usuario=usuario).exclude(estado='CAN').first()
        if not inscripcion:
            return False, "No estás inscrito en este torneo."

        inscripcion.estado = 'CAN'
        inscripcion.save()
        return True, f"Te desinscribiste del torneo {torneo.nombre}."