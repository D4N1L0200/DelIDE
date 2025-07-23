import os
from .file import File


class Folder:
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.files: list[File] = []

        self.load()

    def load(self) -> None:
        for file in os.listdir(self.path):
            if file.endswith(".txt"):
                self.files.append(File(f"{self.path}/{file}"))
