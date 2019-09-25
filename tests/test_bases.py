import pytest
from django.core.management import call_command

from command_log.models import ManagementCommandLog

from .management.commands import test_command


@pytest.mark.django_db
def test_command__exit_code_0():
    call_command("test_command")
    # implicit assert that there is only one object
    log = ManagementCommandLog.objects.get()
    assert log.exit_code == 0
    assert log.result == test_command.DEFAULT_RETURN_VALUE


@pytest.mark.django_db
def test_command__exit_code_1():
    call_command("test_command", "--error")
    # implicit assert that there is only one object
    log = ManagementCommandLog.objects.get()
    assert log.exit_code == 1
    assert log.result == {"error": True, "message": test_command.EXCEPTION_MSG}
