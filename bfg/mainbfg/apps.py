from django.apps import AppConfig


class MainbfgConfig(AppConfig):
    name = 'mainbfg'

    def ready(self):
        import mainbfg.signals.handlers
