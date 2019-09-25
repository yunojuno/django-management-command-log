from django.contrib import admin

from .models import ManagementCommandLog


class ManagementCommandLogAdmin(admin.ModelAdmin):
    list_display = ("management_command", "started_at", "duration", "exit_code")
    list_filter = ("started_at", "app_name", "command_name")
    search_fields = ("command_name",)
    readonly_fields = (
        "management_command",
        "started_at",
        "finished_at",
        "duration",
        "exit_code",
        "output",
    )
    exclude = ("app_name", "command_name", "output")


admin.site.register(ManagementCommandLog, ManagementCommandLogAdmin)
