from django.apps import AppConfig


class ManagementCommandLogConfig(AppConfig):
    name = "command_log"
    verbose_name = "Management command audit log"
    default_auto_field = "django.db.models.AutoField"
