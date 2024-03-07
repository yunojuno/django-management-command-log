from __future__ import annotations

from contextlib import contextmanager
from typing import Iterable, Iterator

import django.db.models.signals
from django.dispatch import Signal

MODEL_SIGNALS = (
    django.db.models.signals.pre_init,
    django.db.models.signals.post_init,
    django.db.models.signals.pre_save,
    django.db.models.signals.post_save,
    django.db.models.signals.pre_delete,
    django.db.models.signals.post_delete,
    django.db.models.signals.pre_migrate,
    django.db.models.signals.post_migrate,
    django.db.models.signals.m2m_changed,
)


@contextmanager
def disable_signals(signals: Iterable[Signal]) -> Iterator[None]:
    """
    Temporariliy disable signals.

    Examples:

        with disable_signals([signals.pre_save, signals.post_save]):
            user.save()

        with disable_signals(MODEL_SIGNALS):
            do_things()

    """
    stashed_receivers: dict[Signal, list] = {}

    # Disconnect each signal by temporarily emptying the receivers list.
    for signal in signals:
        stashed_receivers[signal] = signal.receivers
        signal.receivers = ()

    try:
        yield
    finally:
        # Reconnect all disconnected signals with their receivers.
        for signal, receivers in stashed_receivers.items():
            signal.receivers = receivers
