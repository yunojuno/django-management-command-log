from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.timezone import now


class ManagementCommandLog(models.Model):

    """Records the running of a management command."""

    # when did the event occur
    app_name = models.CharField(
        help_text="The app containing the management command", max_length=100
    )
    command_name = models.CharField(
        help_text="The management command that was executed", max_length=100
    )
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    result = JSONField(
        default=dict,
        help_text="The return value of the command (must be JSON serializable)",
    )

    def __str__(self):
        return f"{self.management_command} run at {self.started_at}"

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.pk} command="{self.management_command}">'

    @property
    def management_command(self):
        return f"{self.app_name}.{self.command_name}"

    @property
    def duration(self):
        try:
            return self.finished_at - self.started_at
        except TypeError:
            return None

    @property
    def exit_code(self):
        """Return 1 if the command raised an error, else 0."""
        return 1 if "error" in self.result else 0

    def start(self):
        """
        Mark the beginning of a management command execution.

        This method does not save object.

        """
        self.started_at = now()

    def finish(self, result):
        """
        Mark the end of a management command execution.

        This method does not save the object.

        """
        self.finished_at = now()
        self.result = result
