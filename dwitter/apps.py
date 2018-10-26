from django.apps import AppConfig


class DwitterConfig(AppConfig):
    name = 'dwitter'

    def ready(self):
        # Register signals
        import dwitter.signals  # noqa: F401
