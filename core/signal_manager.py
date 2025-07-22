from typing import Callable

class SignalManager:
    listeners: dict[str, list[Callable]] = {}

    @classmethod
    def listen(cls, signal: str, callback: Callable) -> None:
        if signal not in cls.listeners:
            cls.listeners[signal] = []
        cls.listeners[signal].append(callback)

    @classmethod
    def emit(cls, signal: str, data: dict) -> None:
        if signal in cls.listeners:
            for callback in cls.listeners[signal]:
                callback(data)