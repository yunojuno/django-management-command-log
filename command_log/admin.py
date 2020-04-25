from django.contrib import admin

from .models import ManagementCommandLog


class ManagementCommandLogAdmin(admin.ModelAdmin):
    list_display = ("management_command", "started_at", "duration", "exit_code_display")
    list_filter = ("started_at", "app_name", "command_name", "exit_code")
    search_fields = ("command_name",)
    readonly_fields = (
        "management_command",
        "started_at",
        "finished_at",
        "duration",
        "exit_code",
        "output",
        "error"
    )
    exclude = ("app_name", "command_name")

    def exit_code_display(self, obj):
        """Display NullBoolean icons for exit code."""
        if obj.exit_code == ManagementCommandLog.EXIT_CODE_PARTIAL:
            return None
        return obj.exit_code == ManagementCommandLog.EXIT_CODE_SUCCESS
    exit_code_display.boolean = True
    exit_code_display.short_description = "Exit code"

admin.site.register(ManagementCommandLog, ManagementCommandLogAdmin)
