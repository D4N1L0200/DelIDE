import pygame
from . import Panel
from ..data import File
from ..signal_manager import SignalManager


class StatusPanel(Panel):
    def __init__(self) -> None:
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/undefined-medium.ttf", 20
        )
        self.text: str = "Lines: NaN | Chars: NaN"

        SignalManager.request("p.code.update_file")
        SignalManager.listen("p.code.update_file", self.update_file)

    def update_file(self, data: dict) -> None:
        file: File = data["file"]
        self.text = f"Lines: {len(file.content)} | Chars: {sum(len(line) for line in file.content)}"

    def update(
        self,
        events: list[pygame.event.Event],
        pos: tuple[int, int],
        width: int,
        height: int,
        active: bool = False,
    ) -> list[pygame.event.Event]:
        return events

    def draw(
        self, pos: tuple[int, int], width: int, height: int, active: bool = False
    ) -> pygame.Surface:
        surface: pygame.Surface = super().draw(pos, width, height, active)

        surface.blit(
            self.font.render(self.text, False, (255, 255, 255)),
            (10, 0),
        )

        pygame.draw.rect(
            surface,
            (130, 50, 150) if active else (255, 255, 255),
            (0, 0, width, height),
            2 if active else 1,
        )

        return surface
