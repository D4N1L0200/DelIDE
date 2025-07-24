import pygame
from . import Panel
from .. import SignalManager


class ButtonPanel(Panel):
    def __init__(self, text: str, signal: str) -> None:
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/undefined-medium.ttf", 20
        )
        self.text: str = text
        self.signal: str = signal

    def update(
        self,
        events: list[pygame.event.Event],
        pos: tuple[int, int],
        width: int,
        height: int,
        active: bool = False,
    ) -> list[pygame.event.Event]:
        if active:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.signal:
                        SignalManager.emit(self.signal, {})
                    events.remove(event)
        return events

    def draw(
        self, pos: tuple[int, int], width: int, height: int, active: bool = False
    ) -> pygame.Surface:
        surface: pygame.Surface = super().draw(pos, width, height, active)

        text_surface: pygame.Surface = self.font.render(
            self.text, False, (255, 255, 255)
        )

        text_width, text_height = text_surface.get_size()
        surface.blit(
            text_surface,
            (int(width / 2 - text_width / 2), int((height - text_height) / 2)),
        )

        pygame.draw.rect(
            surface,
            (130, 50, 150) if active else (255, 255, 255),
            (0, 0, width, height),
            2 if active else 1,
        )

        return surface
