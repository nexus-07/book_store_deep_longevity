from django.apps import AppConfig as AppBaseConfig


class AppConfig(AppBaseConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
