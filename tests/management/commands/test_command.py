from command_log.commands import LoggedCommand

# declared here so they can be referred to in tests
EXCEPTION_MSG = "Forced error"
DEFAULT_RETURN_VALUE = {"updated": 1}


class Command(LoggedCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--error",
            action="store_true",
            dest="error",
            default=False,
            help="Use this option to force the command to raise an exception",
        )

    def do_command(self, *args, **options):
        error = options["error"]
        self.stdout.write(f"Running test command, --error={error}")
        if error:
            raise Exception(EXCEPTION_MSG)
        return DEFAULT_RETURN_VALUE
