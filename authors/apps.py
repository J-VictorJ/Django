from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    name = 'authors'

    
    def ready(self):
        import authors.signals
        return super().ready()