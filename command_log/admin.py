from __future__ import annotations

import ast
import json

from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from command_log.models import ManagementCommandLog


def pretty_print(data: dict | None) -> str:
    """Convert dict into formatted HTML."""
    if data is None:
        return ""
    pretty = json.dumps(data, sort_keys=True, indent=4, separators=(",", ": "))
    html = pretty.replace(" ", "&nbsp;").replace("\n", "<br>")
    return mark_safe("<pre><code>%s</code></pre>" % html)  # noqa: S308, S703


class StatusListFilter(admin.SimpleListFilter):
    title = "status"
    parameter_name = "status"

    def lookups(
        self,
        request: HttpRequest,
        model_admin: ManagementCommandLogAdmin,
    ) -> tuple[tuple[str, str], ...]:
        return (
            ("0", "In progress"),
            ("1", "Complete"),
        )

    def queryset(
        self,
        request: HttpRequest,
        queryset: models.QuerySet[ManagementCommandLog],
    ) -> models.QuerySet[ManagementCommandLog]:
        if self.value() == "0":
            return queryset.filter(started_at__isnull=False, finished_at__isnull=True)
        if self.value() == "1":
            return queryset.filter(started_at__isnull=False, finished_at__isnull=False)
        return queryset


class ManagementCommandLogAdmin(admin.ModelAdmin):
    list_display = ("management_command", "started_at", "duration", "exit_code_display")
    list_filter = (
        "started_at",
        StatusListFilter,
        "exit_code",
        "app_name",
        "command_name",
    )
    search_fields = ("command_name",)
    readonly_fields = (
        "management_command",
        "started_at",
        "finished_at",
        "duration",
        "exit_code",
        "_output",
        "error",
        "truncate_at",
    )
    exclude = ("app_name", "command_name", "output")

    def _output(self, obj: ManagementCommandLog) -> str:
        """Format output as JSON if applicable."""
        try:
            data = ast.literal_eval(obj.output)
            return pretty_print(data)
        except Exception:  # noqa: B902
            return mark_safe(  # noqa: S308, S703
                f"<pre><code>{obj.output}</code></pre>"
            )

    _output.short_description = "Output (formatted)"  # type: ignore

    def exit_code_display(self, obj: ManagementCommandLog) -> bool | None:
        """Display NullBoolean icons for exit code."""
        if obj.exit_code == ManagementCommandLog.EXIT_CODE_PARTIAL:
            return None
        return obj.exit_code == ManagementCommandLog.EXIT_CODE_SUCCESS

    exit_code_display.boolean = True  # type: ignore
    exit_code_display.short_description = "Exit code"  # type: ignore


admin.site.register(ManagementCommandLog, ManagementCommandLogAdmin)
