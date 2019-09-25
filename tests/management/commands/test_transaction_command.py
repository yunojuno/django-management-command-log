from command_log.commands import TransactionLoggedCommand


class Command(TransactionLoggedCommand):
    def do_command(self, *args, **options):
        commit = options["commit"]
        self.stdout.write(f"Running test transaction command, --commit={commit}")
