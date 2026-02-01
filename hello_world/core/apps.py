from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hello_world.core'

    def ready(self):
        """Initialize app and connect signals"""
        # Import here to avoid circular imports
        from .signals import create_initial_data
        post_migrate.connect(create_initial_data, sender=self)