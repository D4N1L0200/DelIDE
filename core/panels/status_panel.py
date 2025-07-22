import pygame
from . import Panel
from ..signal_manager import SignalManager


class StatusPanel(Panel):
    def __init__(self) -> None:
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/undefined-medium.ttf", 20
        )
        self.text: str = "Lines: NaN | Chars: NaN"

        SignalManager.listen("code_panel.update_text", self.update_text)

    def update_text(self, data: dict) -> None:
        print(data)
        self.text = f"Lines: {len(data["lines"])} | Chars: {sum(len(line) for line in data["lines"])}"

    def update(
        self,
        events: list[pygame.event.Event],
        width: int,
        height: int,
        active: bool = False,
    ) -> list[pygame.event.Event]:
        return events

    def draw(self, width: int, height: int, active: bool = False) -> pygame.Surface:
        surface: pygame.Surface = super().draw(width, height, active)

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
