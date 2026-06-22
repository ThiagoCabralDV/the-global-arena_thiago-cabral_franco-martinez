from abc import ABC, abstractmethod
from .models import Notificacion


class Observador(ABC):
    @abstractmethod
    def actualizar(self, usuario, mensaje, tipo):
        pass


class NotificadorDB(Observador):
    def actualizar(self, usuario, mensaje, tipo):
        Notificacion.objects.create(
            usuario=usuario,
            mensaje=mensaje,
            tipo=tipo,
        )


class Notificador:
    _instance = None
    _observers = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._observers = []
        return cls._instance

    def suscribir(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def desuscribir(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notificar(self, usuario, mensaje, tipo):
        for observer in self._observers:
            observer.actualizar(usuario, mensaje, tipo)


notificador = Notificador()
notificador.suscribir(NotificadorDB())