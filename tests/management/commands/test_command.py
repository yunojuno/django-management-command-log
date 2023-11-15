import datetime

from command_log.commands import LoggedCommand, PartialCompletionError, isodate
from command_log.models import ManagementCommandLog

# declared here so they can be referred to in tests
EXCEPTION_MSG = "Forced error"
DEFAULT_RETURN_VALUE = {"updated": 1}


class Command(LoggedCommand):
    truncate_interval = datetime.timedelta(seconds=10)

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--null",
            action="store_true",
            dest="return_null",
            default=False,
            help="Return None rather than the default dict return value",
        )
        parser.add_argument(
            "--start-date",
            action="store",
            dest="start_date",
            type=isodate,
            help="Parse as a date",
        )
        parser.add_argument(
            "--exit-code",
            action="store",
            dest="exit_code",
            type=int,
            default=ManagementCommandLog.EXIT_CODE_SUCCESS,
            choices=ManagementCommandLog.EXIT_CODE_CHOICES,
            help="Use this option to force a specific exit code.",
        )

    def do_command(self, *args, **options):
        exit_code = options["exit_code"]
        return_null = options["return_null"]
        start_date = options.get("start_date")
        self.stdout.write(
            f"Running test command, "
            f"--exit-code={exit_code}, "
            f"--null={return_null}, "
            f"--start_date={start_date}"
        )
        if exit_code == ManagementCommandLog.EXIT_CODE_FAILURE:
            raise Exception(EXCEPTION_MSG)
        if exit_code == ManagementCommandLog.EXIT_CODE_PARTIAL:
            raise PartialCompletionError(EXCEPTION_MSG, output=DEFAULT_RETURN_VALUE)
        if return_null:
            return None
        if start_date:
            return {"start_date": start_date}
        return DEFAULT_RETURN_VALUE
