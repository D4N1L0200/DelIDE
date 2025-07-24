import os
from . import File, Folder
from typing import Optional
from .. import SignalManager


class Data:
    def __init__(self, path: str) -> None:
        self.path: str = path.replace("\\", "/")
        self.path_list: list[str] = self.path.split("/")
        self.folder: Folder = Folder(self.path)
        self.folder.load()

        SignalManager.emit("d.get_folder", {"folder": self.folder})

    def save(self, file: File) -> None:
        file.save()
