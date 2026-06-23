from django.apps import AppConfig


class ReportesConfig(AppConfig):
    name = 'reportes'

    def ready(self):
        import reportes.signals
