class File:
    def __init__(self, path: str, name: str) -> None:
        self.folder: str = path
        self.name: str = name
        self.path: str = f"{self.folder}/{self.name}"
        self.content: list[str] = []
        self.saved: bool = False
        self.byte_file: bool = False

    def load(self) -> None:
        self.content = []
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                for line in file.readlines():
                    self.content.append(line.replace("\n", ""))
        except UnicodeDecodeError:
            self.byte_file = True
        self.saved = True

    def save(self) -> None:
        if self.byte_file:
            return

        with open(self.path, "w", encoding="utf-8") as file:
            for line in self.content:
                file.write(line + "\n")
        self.saved = True

    def write(self, content: list[str]) -> None:
        self.content = content
        self.saved = False

    def read(self) -> list[str]:
        return self.content
