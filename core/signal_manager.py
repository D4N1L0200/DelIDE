from typing import Callable


class SignalManager:
    listeners: dict[str, list[Callable]] = {}

    @classmethod
    def register_signals(cls) -> None:
        cls.emmiters = {
            "p.code.update_file": [],
        }
        cls.listeners = {
            "p.code.update_file": [],
            "d.get_folder": [],
            "p.explorer.open_file": [],
            "o.open": [],
            "o.save": [],
            "o.exit": [],
        }

    @classmethod
    def register(cls, signal: str, callback: Callable) -> None:
        if signal not in cls.emmiters:
            raise ValueError(f"Signal {signal} not found to register")

        cls.emmiters[signal].append(callback)

    @classmethod
    def listen(cls, signal: str, callback: Callable) -> None:
        if signal not in cls.listeners:
            raise ValueError(f"Signal {signal} not found to listen")

        cls.listeners[signal].append(callback)

    @classmethod
    def request(cls, signal: str) -> None:
        if signal not in cls.emmiters:
            raise ValueError(f"Signal {signal} not found to request")

        for callback in cls.emmiters[signal]:
            callback()

    @classmethod
    def emit(cls, signal: str, data: dict) -> None:
        if signal not in cls.listeners:
            raise ValueError(f"Signal {signal} not found to emit")

        for callback in cls.listeners[signal]:
            callback(data)
