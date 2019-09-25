import datetime
from unittest import mock

import pytest

from command_log.models import ManagementCommandLog


def mock_save(obj):
    """Mock out the model.save method as this drags in the database unnecessarily."""
    pass


@mock.patch.object(ManagementCommandLog, "save", mock_save)
def test_start():
    log = ManagementCommandLog()
    assert log.started_at is None
    assert log.finished_at is None
    assert log.duration is None
    log.start()
    assert log.started_at is not None
    assert log.finished_at is None
    assert log.duration is None


@mock.patch.object(ManagementCommandLog, "save", mock_save)
def test_start__twice_fails():
    # cannot restart a log that has been started
    log = ManagementCommandLog()
    log.start()
    with pytest.raises(ValueError):
        log.start()


@mock.patch.object(ManagementCommandLog, "save", mock_save)
def test_stop():
    log = ManagementCommandLog()
    log.start()
    log.stop(output=None, exit_code=0)
    assert log.output is None
    assert log.duration is not None
    assert log.exit_code == 0


@mock.patch.object(ManagementCommandLog, "save", mock_save)
def test_stop__before_start_fails():
    # cannot call stop before the timer has started
    log = ManagementCommandLog()
    with pytest.raises(ValueError):
        log.stop(output=None, exit_code=0)


@mock.patch.object(ManagementCommandLog, "save", mock_save)
def test_stop__twice_fails():
    # cannot call stop a second time.
    log = ManagementCommandLog()
    log.start()
    log.stop(output=None, exit_code=0)
    with pytest.raises(ValueError):
        log.stop(output=None, exit_code=0)


def test_duration():
    log = ManagementCommandLog()
    log.started_at = datetime.datetime.now()
    assert log.duration is None
    log.finished_at = log.started_at + datetime.timedelta(seconds=1)
    assert log.duration == log.finished_at - log.started_at
