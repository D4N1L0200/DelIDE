import os
from . import File, Folder
from typing import Optional
from .. import SignalManager


class Data:
    def __init__(self) -> None:
        self.path: str = ""
        self.path_list: list[str] = []
        self.folder: Folder

    def save(self, file: File) -> None:
        file.save()

    def load(self, path: str) -> None:
        self.path = path.replace("\\", "/")
        self.path_list = self.path.split("/")
        self.folder = Folder(self.path)
        self.folder.load()

        SignalManager.emit("d.get_folder", {"folder": self.folder})
