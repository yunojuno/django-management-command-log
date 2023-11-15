import argparse
import contextlib
import datetime
from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command
from django.db.models.signals import post_save

from command_log.management.commands.base import isodate
from command_log.models import ManagementCommandLog
from command_log.utils.signals import MODEL_SIGNALS

from .management.commands import test_command

TEST_MODULE = "command_log.management.commands.base"


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
class TestDisableModelSignalsOption:
    @pytest.mark.parametrize("model_signals_disabled", (True, False))
    @patch("tests.management.commands.test_command.Command.do_command")
    def test_disables_model_signals_during_do_command(
        self,
        do_command: Mock,
        model_signals_disabled: bool,
    ) -> None:
        disabled_currently = ()
        disabled_during_command = ()

        def fake_do_command(*args, **kwargs):
            nonlocal disabled_during_command, disabled_currently
            disabled_during_command = disabled_currently

        do_command.side_effect = fake_do_command

        @contextlib.contextmanager
        def fake_disable_signals(signals):
            nonlocal disabled_currently
            disabled_currently = signals
            yield
            disabled_currently = ()

        command_args = ("--disable-model-signals",) if model_signals_disabled else ()

        # Patch here so we don't need to mock __enter__ etc.
        with patch(f"{TEST_MODULE}.disable_signals", fake_disable_signals):
            call_command("test_command", *command_args)

        assert disabled_currently == ()
        assert disabled_during_command == (
            MODEL_SIGNALS if model_signals_disabled else ()
        )

    def test_does_not_disable_management_command_log_signals(self):
        received = {}

        def receiver(sender, *args, **kwargs):
            received["sender"] = sender
            received["args"] = args

        post_save.connect(receiver)
        call_command("test_command", "--disable-model-signals")
        assert received == {
            "sender": ManagementCommandLog,
            "args": (),
        }


@pytest.mark.django_db
def test_transaction_command__get_logs():
    call_command("test_command")
    assert ManagementCommandLog.objects.get() == test_command.Command().get_logs().get()


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
