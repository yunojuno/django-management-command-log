from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.timezone import now


class ManagementCommandLog(models.Model):

    """Records the running of a management command."""

    app_name = models.CharField(
        help_text="The app containing the management command", max_length=100
    )
    command_name = models.CharField(
        help_text="The management command that was executed", max_length=100
    )
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    exit_code = models.IntegerField(
        default=0, help_text="0 if the command ran without error."
    )
    result = JSONField(
        default=dict,
        help_text="The return value of the command (must be JSON serializable)",
        null=True,
        blank=True,
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

    def start(self):
        """
        Mark the beginning of a management command execution.

        This method does not save object.

        """
        if self.started_at:
            raise ValueError("Cannot call start twice on the same log.")
        self.started_at = now()
        self.finished_at = None

    def stop(self, result=None):
        """
        Mark the end of a management command execution.

        This method does not save the object.

        """
        if not self.started_at:
            raise ValueError("Cannot call finish before start.")
        if self.finished_at:
            raise ValueError("Cannot call finish twice on the same log.")
        self.finished_at = now()
        self.result = result
