import os
from . import File, Folder
from .. import SignalManager


class Data:
    def __init__(self) -> None:
        self.path: str = ""
        self.path_list: list[str] = []
        self.folder: Folder

        SignalManager.listen("d.load_folder", self.on_load_folder)

    def on_load_folder(self, data: dict) -> None:
        path = data["path"]

        if path == self.folder.path:
            self.folder.load()
            SignalManager.emit("d.get_folder", {"folder": self.folder})
            return

        folder = self.folder.search_folder(path, len(self.path_list))
        if folder:
            folder.load()
            SignalManager.emit("d.get_folder", {"folder": self.folder})
        else:
            print(f"[ERROR] Folder '{path}' not found in root '{self.folder.path}'")

    def save(self, file: File) -> None:
        file.save()

    def load(self, path: str) -> None:
        self.path = path.replace("\\", "/")
        self.path_list = self.path.split("/")
        self.folder = Folder(self.path)

        SignalManager.emit("d.get_folder", {"folder": self.folder})
