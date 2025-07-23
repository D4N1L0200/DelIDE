from typing import Callable


class SignalManager:
    listeners: dict[str, list[Callable]] = {}

    @classmethod
    def register_signals(cls) -> None:
        cls.listeners = {
            "update_text.get": [],
            "update_text.post": [],
            "get_file.post": [],
        }

    @classmethod
    def listen(cls, signal: str, callback: Callable) -> None:
        if signal not in cls.listeners:
            raise ValueError(f"Signal {signal} not found")
        cls.listeners[signal].append(callback)

    @classmethod
    def emit(cls, signal: str, data: dict) -> None:
        if signal not in cls.listeners:
            raise ValueError(f"Signal {signal} not found")

        for callback in cls.listeners[signal]:
            callback(data)
