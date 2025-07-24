import os
from .file import File


class Folder:
    def __init__(self, path: str) -> None:
        self.path: str = path.replace("\\", "/")
        self.path_list: list[str] = self.path.split("/")
        self.folders: list[Folder] = []
        self.files: list[File] = []

        self.load()

    def load(self) -> None:
        for file_name in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, file_name)):
                file: File = File(self.path, file_name)
                file.load()
                self.files.append(file)
            else:
                folder: Folder = Folder(os.path.join(self.path, file_name))
                folder.load()
                self.folders.append(folder)

    def search(self, path: str, depth: int = 0) -> File | None:
        path_list: list[str] = path.split("/")

        if path_list[depth] != self.path_list[depth]:
            return None

        if depth + 2 == len(path_list):
            for file in self.files:
                if file.path == path:
                    return file
            return None

        for folder in self.folders:
            if file := folder.search(path, depth + 1):
                return file

        return None
