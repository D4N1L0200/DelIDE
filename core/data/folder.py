import os
from .file import File
from typing import Optional


class Folder:
    def __init__(self, path: str) -> None:
        self.path: str = path.replace("\\", "/")
        self.path_list: list[str] = self.path.split("/")
        self.folders: list[Folder] = []
        self.files: list[File] = []
        self.loaded: bool = False

    def load(self) -> None:
        for file_name in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, file_name)):
                file: File = File(self.path, file_name)
                file.load()
                self.files.append(file)
            else:
                folder: Folder = Folder(os.path.join(self.path, file_name))
                self.folders.append(folder)

        self.loaded = True

    def search_file(self, path: str, depth: int = 0) -> Optional[File]:
        path_list: list[str] = path.split("/")

        if path_list[depth] != self.path_list[depth]:
            return None

        if depth + 2 == len(path_list):
            for file in self.files:
                if file.path == path:
                    return file
            return None

        for folder in self.folders:
            if file := folder.search_file(path, depth + 1):
                return file

        return None

    def search_folder(
        self, path: str, root_size: int, depth: int = 0
    ) -> Optional["Folder"]:
        path_list: list[str] = path.split("/")

        if path_list[depth] != self.path_list[depth]:
            return None

        if depth + 1 == len(path_list) - root_size:
            for folder in self.folders:
                if folder.path == path:
                    return folder
            return None

        for folder in self.folders:
            if folder := folder.search_folder(path, root_size, depth + 1):
                return folder

        return None
