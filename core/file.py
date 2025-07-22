class File:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.content: list[str] = []

    def load(self) -> None:
        with open(self.name, "r") as file:
            for line in file.readlines():
                self.content.append(line.replace("\n", ""))

    def save(self) -> None:
        with open(self.name, "w") as file:
            for line in self.content:
                file.write(line + "\n")

    def write(self, content: list[str]) -> None:
        self.content = content
        self.save()

    def read(self) -> list[str]:
        self.load()
        return self.content
