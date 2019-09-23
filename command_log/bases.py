import logging

from django.core.management.base import BaseCommand

from .models import ManagementCommandLog

logger = logging.getLogger("command_log")


class LoggedCommand(BaseCommand):

    @property
    def app_name(self):
        return self.__module__.split('.')[-4]

    @property
    def command_name(self):
        return self.__module__.split('.')[-1]

    def add_arguments(self, parser):
        parser.add_argument(
            "--disable-logging",
            action="store_true",
            dest="disable",
            default=False,
            help="Disable the logging of the command",
        )

    def do_command(self, *args, **options):
        raise NotImplementedError()

    def handle(self, *args, **options):
        """Run the do_command method and log the output."""
        disable = options["disable"]
        log = ManagementCommandLog(app_name=self.app_name, command_name=self.command_name)
        log.start()
        try:
            result = self.do_command(*args, **options)
        except Exception as ex:
            logger.exception("Error running management command: %s", log)
            result = {"error": True, "message": str(ex)}
        log.finish(result)
        if not disable:
            log.save()
