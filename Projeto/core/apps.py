from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Desativa a restrição de versão mínima do MariaDB diretamente no backend do MySQL
        from django.db.backends.mysql.base import DatabaseWrapper
        DatabaseWrapper.check_database_version_supported = lambda self: None