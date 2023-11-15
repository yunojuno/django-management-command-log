import datetime
from typing import Any, Dict

from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils.timezone import now as tz_now
from django.utils.translation import gettext_lazy as _lazy

from command_log.management.commands.base import TransactionLoggedCommand
from command_log.models import ManagementCommandLog


def logs_to_truncate() -> QuerySet:
    """Fetch the base queryset of objects to remove."""
    return ManagementCommandLog.objects.filter(truncate_at__lte=tz_now())


def breakdown_by_name(queryset: QuerySet) -> Dict[str, int]:
    """Convert logs queryset into {name: count} dictionary."""
    return {
        x[0]: x[1]
        for x in queryset.values_list("command_name")
        .annotate(count=Count("id"))
        .order_by("command_name")
    }


class Command(TransactionLoggedCommand):
    help = _lazy(  # noqa: A003
        "Truncate all log records that have passed their truncate_at timestamp."
    )

    truncate_interval = datetime.timedelta(days=7)

    def do_command(self, *args: Any, **options: Any) -> Dict[str, Any]:
        logs = logs_to_truncate()
        breakdown = breakdown_by_name(logs)
        self.stdout.write("Deleting expired management command logs.")
        count, _ = logs.delete()
        self.stdout.write(f"Management command logs deleted: {count}")
        return {
            "count": count,
            "breakdown": breakdown,
        }
