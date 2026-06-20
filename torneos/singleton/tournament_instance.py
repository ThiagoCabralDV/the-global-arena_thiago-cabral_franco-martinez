class TournamentInstance(type):
    """
    Metaclase Singleton que garantiza que solo exista una instancia
    del controlador en todo el ciclo de vida de la aplicación.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]