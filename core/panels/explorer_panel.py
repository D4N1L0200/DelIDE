import pygame
from . import Panel
from .. import File, Folder, SignalManager


class ExplorerPanel(Panel):
    def __init__(self) -> None:
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/undefined-medium.ttf", 20
        )
        self.folder: Folder
        self.folders: list[Folder] = []
        self.files: list[File] = []
        self.lines: list[str] = []

        SignalManager.listen("get_folder", self.on_get_folder)

    def on_get_folder(self, data: dict) -> None:
        def get_content(folder: Folder) -> None:
            if folder.path_list[-1] == "__pycache__":
                return

            self.folders.extend(folder.folders)
            self.files.extend(folder.files)

            self.lines.append(f"{folder.path_list[-1]}/")
            for nested_folder in folder.folders:
                get_content(nested_folder)
            self.lines.extend([file.name for file in folder.files])
            self.lines.append("")

        self.folder = data["folder"]

        self.folders = []
        self.files = []

        get_content(self.folder)

    def update(
        self,
        events: list[pygame.event.Event],
        pos: tuple[int, int],
        width: int,
        height: int,
        active: bool = False,
    ) -> list[pygame.event.Event]:
        line_height: int = self.font.get_height()
        lines: list[str] = [line for line in self.lines if line]

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, line in enumerate(lines):
                    if "/" in line:
                        continue

                    rect: pygame.Rect = pygame.Rect(
                        pos[0], pos[1] + line_height * i, width, line_height
                    )
                    if rect.collidepoint(event.pos):
                        print(f"Opening file {lines[i]} at {self.folder.path_list[-1]}")
                        for file in self.files:
                            if file.name == lines[i]:
                                SignalManager.emit("open_file", {"file": file})
                                break

        return events

    def draw(
        self, pos: tuple[int, int], width: int, height: int, active: bool = False
    ) -> pygame.Surface:
        surface: pygame.Surface = super().draw(pos, width, height, active)

        line_height: int = self.font.get_height()
        tab: int = 0
        i: int = 0
        for line in self.lines:
            if not line:
                tab -= 1
                continue

            line = "| " * tab + line
            surface.blit(
                self.font.render(line, False, (255, 255, 255)),
                (10, line_height * i),
            )
            if "/" in line:
                tab += 1
            i += 1

        pygame.draw.rect(
            surface,
            (130, 50, 150) if active else (255, 255, 255),
            (0, 0, width, height),
            2 if active else 1,
        )

        return surface
