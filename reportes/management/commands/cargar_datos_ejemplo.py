from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from torneos.models import Videojuego, Torneo, Fase
from inscripciones.models import Inscripcion
from encuentros.models import Encuentro
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Carga datos de ejemplo para probar los reportes'

    def handle(self, *args, **options):
        if User.objects.filter(username__startswith='jugador').exists():
            self.stdout.write(self.style.WARNING('Ya hay datos cargados. No se hace nada.'))
            return

        # Crear videojuegos
        sf6 = Videojuego.objects.create(nombre='Street Fighter 6', genero='Lucha')
        tk8 = Videojuego.objects.create(nombre='Tekken 8', genero='Lucha')
        ggst = Videojuego.objects.create(nombre='Guilty Gear Strive', genero='Lucha')

        # Crear organizador
        admin = User.objects.create_user(username='admin', password='admin123', email='admin@arena.com')

        # Crear jugadores
        jugadores = []
        nombres = ['ShadowKing', 'FenixFGC', 'NeonBlade', 'ViperQueen', 'DragonSlayer',
                   'ThunderFist', 'CyberWolf', 'IcePhoenix', 'StormRider', 'BlazeMaster']
        for n in nombres:
            u = User.objects.create_user(username=n, password='pass123', email=f'{n.lower()}@arena.com')
            jugadores.append(u)

        # Crear torneo 1: Street Fighter 6 - Finalizado
        t1 = Torneo.objects.create(
            nombre='SF6 World Cup',
            descripcion='Torneo internacional de Street Fighter 6',
            fecha_inicio=datetime(2026, 5, 1, 14, 0),
            estado=Torneo.Estado.FINALIZADO,
            cupo_maximo=8,
            videojuego=sf6,
            organizador=admin,
        )

        # Fases del torneo 1
        f1_cuartos = Fase.objects.create(torneo=t1, nombre='Cuartos de Final', orden=1, esta_completa=True, estado='Completada')
        f1_semis = Fase.objects.create(torneo=t1, nombre='Semifinales', orden=2, esta_completa=True, estado='Completada')
        f1_final = Fase.objects.create(torneo=t1, nombre='Final', orden=3, esta_completa=True, estado='Completada')

        # Encuentros SF6 World Cup
        e1 = Encuentro.objects.create(
            torneo=t1, fase=f1_cuartos, jugador1=jugadores[0], jugador2=jugadores[1],
            puntaje_j1=3, puntaje_j2=1, estado=Encuentro.Estado.FINALIZADO
        )
        e1.determinar_ganador()

        e2 = Encuentro.objects.create(
            torneo=t1, fase=f1_cuartos, jugador1=jugadores[2], jugador2=jugadores[3],
            puntaje_j1=2, puntaje_j2=3, estado=Encuentro.Estado.FINALIZADO
        )
        e2.determinar_ganador()

        e3 = Encuentro.objects.create(
            torneo=t1, fase=f1_cuartos, jugador1=jugadores[4], jugador2=jugadores[5],
            puntaje_j1=3, puntaje_j2=0, estado=Encuentro.Estado.FINALIZADO
        )
        e3.determinar_ganador()

        e4 = Encuentro.objects.create(
            torneo=t1, fase=f1_cuartos, jugador1=jugadores[6], jugador2=jugadores[7],
            puntaje_j1=1, puntaje_j2=3, estado=Encuentro.Estado.FINALIZADO
        )
        e4.determinar_ganador()

        e5 = Encuentro.objects.create(
            torneo=t1, fase=f1_semis, jugador1=jugadores[0], jugador2=jugadores[3],
            puntaje_j1=3, puntaje_j2=2, estado=Encuentro.Estado.FINALIZADO
        )
        e5.determinar_ganador()

        e6 = Encuentro.objects.create(
            torneo=t1, fase=f1_semis, jugador1=jugadores[4], jugador2=jugadores[7],
            puntaje_j1=1, puntaje_j2=3, estado=Encuentro.Estado.FINALIZADO
        )
        e6.determinar_ganador()

        e7 = Encuentro.objects.create(
            torneo=t1, fase=f1_final, jugador1=jugadores[0], jugador2=jugadores[7],
            puntaje_j1=4, puntaje_j2=2, estado=Encuentro.Estado.FINALIZADO
        )
        e7.determinar_ganador()

        # Inscripciones torneo 1
        for j in jugadores[:8]:
            Inscripcion.objects.create(usuario=j, torneo=t1, estado=Inscripcion.Estado.CONFIRMADO)

        # Crear torneo 2: Tekken 8 - En Vivo
        t2 = Torneo.objects.create(
            nombre='Iron Fist Championship',
            descripcion='El torneo definitivo de Tekken 8',
            fecha_inicio=datetime(2026, 6, 15, 18, 0),
            estado=Torneo.Estado.EN_VIVO,
            cupo_maximo=16,
            videojuego=tk8,
            organizador=admin,
        )

        f2_grupos = Fase.objects.create(torneo=t2, nombre='Fase de Grupos', orden=1, esta_completa=True, estado='Completada')
        f2_octavos = Fase.objects.create(torneo=t2, nombre='Octavos', orden=2, esta_completa=True, estado='Completada')
        f2_cuartos = Fase.objects.create(torneo=t2, nombre='Cuartos', orden=3, esta_completa=False, estado='En curso')

        Encuentro.objects.create(
            torneo=t2, fase=f2_grupos, jugador1=jugadores[0], jugador2=jugadores[2],
            puntaje_j1=2, puntaje_j2=0, estado=Encuentro.Estado.FINALIZADO
        ).determinar_ganador()
        Encuentro.objects.create(
            torneo=t2, fase=f2_grupos, jugador1=jugadores[1], jugador2=jugadores[3],
            puntaje_j1=2, puntaje_j2=1, estado=Encuentro.Estado.FINALIZADO
        ).determinar_ganador()
        Encuentro.objects.create(
            torneo=t2, fase=f2_octavos, jugador1=jugadores[0], jugador2=jugadores[1],
            puntaje_j1=3, puntaje_j2=1, estado=Encuentro.Estado.FINALIZADO
        ).determinar_ganador()
        Encuentro.objects.create(
            torneo=t2, fase=f2_octavos, jugador1=jugadores[2], jugador2=jugadores[3],
            puntaje_j1=3, puntaje_j2=2, estado=Encuentro.Estado.FINALIZADO
        ).determinar_ganador()
        Encuentro.objects.create(
            torneo=t2, fase=f2_cuartos, jugador1=jugadores[0], jugador2=jugadores[2],
            puntaje_j1=2, puntaje_j2=1, estado=Encuentro.Estado.FINALIZADO
        ).determinar_ganador()
        Encuentro.objects.create(
            torneo=t2, fase=f2_cuartos, jugador1=jugadores[1], jugador2=jugadores[3],
            puntaje_j1=0, puntaje_j2=0, estado=Encuentro.Estado.PENDIENTE
        )

        for j in jugadores[:6]:
            Inscripcion.objects.create(usuario=j, torneo=t2, estado=Inscripcion.Estado.CONFIRMADO)

        # Crear torneo 3: GGST - Próximo
        t3 = Torneo.objects.create(
            nombre='Strive Championship Series #3',
            descripcion='Torneo mensual de Guilty Gear Strive',
            fecha_inicio=datetime(2026, 7, 1, 16, 0),
            estado=Torneo.Estado.PROXIMO,
            cupo_maximo=8,
            videojuego=ggst,
            organizador=admin,
        )

        Fase.objects.create(torneo=t3, nombre='Semifinales', orden=1, esta_completa=False, estado='Pendiente')
        Fase.objects.create(torneo=t3, nombre='Final', orden=2, esta_completa=False, estado='Pendiente')

        for j in jugadores[:4]:
            Inscripcion.objects.create(usuario=j, torneo=t3, estado=Inscripcion.Estado.PENDIENTE)

        self.stdout.write(self.style.SUCCESS(f'Datos cargados exitosamente.'))
        self.stdout.write(f'  - {User.objects.count()} usuarios')
        self.stdout.write(f'  - {Videojuego.objects.count()} videojuegos')
        self.stdout.write(f'  - {Torneo.objects.count()} torneos')
        self.stdout.write(f'  - {Fase.objects.count()} fases')
        self.stdout.write(f'  - {Inscripcion.objects.count()} inscripciones')
        self.stdout.write(f'  - {Encuentro.objects.count()} encuentros')
