import datetime

import pytest

from command_log.models import ManagementCommandLog


def test_start():
    log = ManagementCommandLog()
    assert log.started_at is None
    assert log.finished_at is None
    assert log.duration is None
    log.start()
    assert log.started_at is not None
    assert log.finished_at is None
    assert log.duration is None


def test_start__twice_fails():
    # cannot restart a log that has been started
    log = ManagementCommandLog()
    log.start()
    with pytest.raises(ValueError):
        log.start()


def test_finish():
    log = ManagementCommandLog()
    log.start()
    log.finish({})
    assert log.result == {}
    assert log.duration is not None
    assert log.exit_code == 0


def test_finish__before_start_fails():
    # cannot call finish before the timer has started
    log = ManagementCommandLog()
    with pytest.raises(ValueError):
        log.finish({})


def test_finish__twice_fails():
    # cannot call finish a second time.
    log = ManagementCommandLog()
    log.start()
    log.finish({})
    with pytest.raises(ValueError):
        log.finish({})


def test_exit_code__0():
    log = ManagementCommandLog()
    log.start()
    log.finish({})
    assert log.exit_code == 0


def test_exit_code__1():
    log = ManagementCommandLog()
    log.start()
    log.finish({"error": True})
    assert log.exit_code == 1


def test_duration():
    log = ManagementCommandLog()
    log.started_at = datetime.datetime.now()
    assert log.duration is None
    log.finished_at = log.started_at + datetime.timedelta(seconds=1)
    assert log.duration == log.finished_at - log.started_at
