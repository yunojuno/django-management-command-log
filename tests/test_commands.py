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
    assert log.result == {"error": test_command.EXCEPTION_MSG}


@pytest.mark.django_db
def test_command__disable_logging():
    # explicitly disable logging
    call_command("test_command", "--disable-logging")
    assert not ManagementCommandLog.objects.exists()


@pytest.mark.django_db
def test_transaction_command__commit():
    # without the --commit option no record is stored
    call_command("test_transaction_command", "--commit")
    assert ManagementCommandLog.objects.exists()


@pytest.mark.django_db
def test_transaction_command__rollback():
    # without the --commit option no record is stored
    call_command("test_transaction_command")
    assert not ManagementCommandLog.objects.exists()
