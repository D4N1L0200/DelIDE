import os
from .folder import Folder
from .. import SignalManager


class Data:
    def __init__(self, path: str) -> None:
        self.path: str = path.replace("\\", "/")
        self.path_list: list[str] = self.path.split("/")
        self.folder: Folder = Folder(self.path)

        SignalManager.emit("get_folder", {"folder": self.folder})
        SignalManager.listen("update_text", self.on_update_text)

    def on_update_text(self, data: dict) -> None:
        for file in self.folder.files:
            if file.name == data["file_name"]:
                file.write(data["lines"])
                break
