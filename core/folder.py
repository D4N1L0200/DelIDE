import os
from .file import File
from .signal_manager import SignalManager


class Folder:
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.files: list[File] = []

        self.load()

        SignalManager.listen("update_text.post", self.on_update_text)
        
    def on_update_text(self, data: dict) -> None:
        for file in self.files:
            if file.path == data["file_name"]:
                file.write(data["lines"])
                break
        else:
            raise ValueError(f"File {data['file_name']} not found")

    def load(self) -> None:
        for file in os.listdir(self.path):
            if file.endswith(".txt"):
                self.files.append(File(self.path, file))
