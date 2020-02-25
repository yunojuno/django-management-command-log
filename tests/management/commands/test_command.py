from command_log.commands import LoggedCommand, isodate

# declared here so they can be referred to in tests
EXCEPTION_MSG = "Forced error"
DEFAULT_RETURN_VALUE = {"updated": 1}


class Command(LoggedCommand):
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
            "--error",
            action="store_true",
            dest="error",
            default=False,
            help="Use this option to force the command to raise an exception",
        )
        parser.add_argument(
            "--start-date",
            action="store",
            dest="start_date",
            type=isodate,
            help="Parse as a date",
        )

    def do_command(self, *args, **options):
        error = options["error"]
        return_null = options["return_null"]
        start_date = options.get("start_date")
        self.stdout.write(
            f"Running test command, "
            f"--error={error}, "
            f"--null={return_null}, "
            f"--start_date={start_date}"
        )
        if error:
            raise Exception(EXCEPTION_MSG)
        if return_null:
            return None
        if start_date:
            return {"start_date": start_date}
        return DEFAULT_RETURN_VALUE
