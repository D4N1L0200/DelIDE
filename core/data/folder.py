import os
from .file import File
from .. import SignalManager


class Folder:
    def __init__(self, path: str) -> None:
        self.path: str = path.replace("\\", "/")
        self.path_list: list[str] = self.path.split("/")
        self.folders: list[Folder] = []
        self.files: list[File] = []

        self.load()

        SignalManager.listen("update_text", self.on_update_text)

    def on_update_text(self, data: dict) -> None:
        for file in self.files:
            if file.path == data["file_name"]:
                file.write(data["lines"])
                break

    def load(self) -> None:
        for file in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, file)):
                self.files.append(File(self.path, file))
            else:
                self.folders.append(Folder(os.path.join(self.path, file)))

    def search(self, name: str) -> File | None:
        for file in self.files:
            if file.name == name:
                return file

        for folder in self.folders:
            if file := folder.search(name):
                return file

        return None