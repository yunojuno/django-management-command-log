import argparse
import datetime

import pytest
from django.core.management import call_command

from command_log.commands import isodate
from command_log.models import ManagementCommandLog

from .management.commands import test_command


@pytest.mark.django_db
def test_command__exit_code_0():
    call_command("test_command")
    # implicit assert that there is only one object
    log = ManagementCommandLog.objects.get()
    assert log.exit_code == 0
    assert log.output == str(test_command.DEFAULT_RETURN_VALUE)
    assert log.error == ""


@pytest.mark.django_db
def test_command__exit_code__date():
    call_command("test_command", start_date="2020-01-01")
    log = ManagementCommandLog.objects.get()
    assert log.exit_code == ManagementCommandLog.EXIT_CODE_SUCCESS
    assert log.output == str({"start_date": "2020-01-01"})
    assert log.error == ""


@pytest.mark.django_db
def test_command__exit_code_1():
    call_command("test_command", exit_code=ManagementCommandLog.EXIT_CODE_FAILURE)
    # implicit assert that there is only one object
    log = ManagementCommandLog.objects.get()
    assert log.exit_code == ManagementCommandLog.EXIT_CODE_FAILURE
    assert log.error == test_command.EXCEPTION_MSG
    assert log.output == ""


@pytest.mark.django_db
def test_command__exit_code_2():
    call_command("test_command", exit_code=ManagementCommandLog.EXIT_CODE_PARTIAL)
    # implicit assert that there is only one object
    log = ManagementCommandLog.objects.get()
    assert log.exit_code == ManagementCommandLog.EXIT_CODE_PARTIAL
    assert log.output == str(test_command.DEFAULT_RETURN_VALUE)
    assert log.error == test_command.EXCEPTION_MSG


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


def test_isodate():
    assert isodate("2020-01-01") == datetime.date(2020, 1, 1)


def test_isodate__error():
    with pytest.raises(argparse.ArgumentTypeError):
        isodate("01-01-2020")
