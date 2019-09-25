import datetime
import json
from decimal import Decimal

from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.utils.safestring import mark_safe

from .models import ManagementCommandLog


def format_json_for_admin(result):
    """Pretty-print formatted result JSON.

    Take entity result JSON, indent it, order the keys and then
    present it as a <code> block. That's about as good as we can get
    until someone builds a custom syntax function.

    """

    def _clean(val):
        """Convert unserializable values into serializable versions."""
        if type(val) is Decimal:
            return float(val)
        if type(val) is datetime.date:
            return val.isoformat()
        if type(val) is datetime.datetime:
            return val.isoformat()
        raise TypeError("Unserializable JSON value: %s" % val)

    pretty = json.dumps(
        result, sort_keys=True, indent=4, separators=(",", ": "), default=_clean
    )
    # https://docs.djangoproject.com/en/1.11/ref/utils/#django.utils.html.format_html
    # this is a fudge to get around the fact that we cannot put a <pre> inside a <p>,
    # but we want the <p> formatting (.align CSS). We can either use a <pre> and an
    # inline style to mimic the CSS, or forego the <pre> and put the spaces
    # and linebreaks in as HTML.
    pretty = pretty.replace(" ", "&nbsp;").replace("\n", "<br/>")
    return format_html("<code>{}</code>", mark_safe(pretty))


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
        "result_",
    )
    exclude = ("app_name", "command_name", "result")

    def result_(self, obj):
        return format_json_for_admin(obj.result)

    result_.short_description = "Result"


admin.site.register(ManagementCommandLog, ManagementCommandLogAdmin)
