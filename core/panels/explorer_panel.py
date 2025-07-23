import pygame
from . import Panel
from ..file import File
from ..signal_manager import SignalManager


class ExplorerPanel(Panel):
    def __init__(self) -> None:
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/undefined-medium.ttf", 20
        )
        self.folder: str = ""
        self.files: list[File] = []
        self.lines: list[str] = []

        SignalManager.listen("get_folder.post", self.on_get_folder)

    def on_get_folder(self, data: dict) -> None:
        self.folder = data["folder"].path
        self.files = data["folder"].files

        self.lines = [f"{self.folder}/"]
        self.lines.extend([file.name for file in self.files])

    def update(
        self,
        events: list[pygame.event.Event],
        pos: tuple[int, int],
        width: int,
        height: int,
        active: bool = False,
    ) -> list[pygame.event.Event]:
        line_height: int = self.font.get_height()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, line in enumerate(self.lines):
                    if "/" in line:
                        continue

                    rect: pygame.Rect = pygame.Rect(
                        pos[0], pos[1] + line_height * i, width, line_height
                    )
                    if rect.collidepoint(event.pos):
                        print(f"Opening file {self.lines[i]} at {self.folder}")
                        for file in self.files:
                            if file.name == self.lines[i]:
                                SignalManager.emit("open_file.post", {"file": file})
                                break

        return events

    def draw(
        self, pos: tuple[int, int], width: int, height: int, active: bool = False
    ) -> pygame.Surface:
        surface: pygame.Surface = super().draw(pos, width, height, active)

        line_height: int = self.font.get_height()
        tab: int = 0
        for i, line in enumerate(self.lines):
            line = " " * tab + line
            surface.blit(
                self.font.render(line, False, (255, 255, 255)),
                (10, line_height * i),
            )
            if "/" in line:
                tab += 1

        pygame.draw.rect(
            surface,
            (130, 50, 150) if active else (255, 255, 255),
            (0, 0, width, height),
            2 if active else 1,
        )

        return surface
