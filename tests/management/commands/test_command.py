from command_log.bases import LoggedCommand


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
            raise Exception("Forced error")
        return {"updated": 1}
