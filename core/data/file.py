class File:
    def __init__(self, path: str, name: str) -> None:
        self.folder: str = path
        self.name: str = name
        self.path: str = f"{self.folder}/{self.name}"
        self.content: list[str] = []
        self.saved: bool = False

    def load(self) -> None:
        self.content = []
        with open(self.path, "r") as file:
            for line in file.readlines():
                self.content.append(line.replace("\n", ""))
        self.saved = True

    def save(self) -> None:
        with open(self.path, "w") as file:
            for line in self.content:
                file.write(line + "\n")
        self.saved = True

    def write(self, content: list[str]) -> None:
        self.content = content
        self.saved = False

    def read(self) -> list[str]:
        return self.content
