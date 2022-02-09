from __future__ import annotations

import pytest
from django.dispatch import Signal

from command_log.utils.signals import disable_signals


class TestDisableSignals:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.messages = []

    def receive(self, signal: Signal, sender, message: str):
        self.messages.append(message)

    @pytest.fixture()
    def signal(self) -> Signal:
        sig = Signal()
        sig.connect(self.receive)
        return sig

    def test_signals_disabled_during(self, signal: Signal) -> None:
        assert len(self.messages) == 0
        with disable_signals([signal]):
            signal.send(sender=None, message="disabled")
        assert len(self.messages) == 0

    def test_signals_reenabled_after(self, signal: Signal) -> None:
        assert len(self.messages) == 0
        with disable_signals([signal]):
            pass
        signal.send(sender=None, message="re-enabled")
        assert self.messages == ["re-enabled"]

    def test_signals_reenabled_on_exception(self, signal: Signal) -> None:
        try:
            with disable_signals([signal]):
                raise ValueError("test")
        except ValueError:
            pass
        signal.send(sender=None, message="re-enabled")
        assert self.messages == ["re-enabled"]

    def test_other_signals_always_enabled(self, signal: Signal) -> None:
        self.other_message = None

        def listener(signal: Signal, sender, message: str) -> None:
            self.other_message = message

        other_signal = Signal()
        other_signal.connect(listener)

        with disable_signals([signal]):
            other_signal.send(sender=None, message="always_enabled")

        assert len(self.messages) == 0
        assert self.other_message == "always_enabled"
