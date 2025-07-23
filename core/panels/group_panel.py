import pygame
from . import Panel
from ..signal_manager import SignalManager


class GroupPanel(Panel):
    def __init__(self, panels: list[Panel], ratios: list[int], direction: str) -> None:
        self.panels: list[Panel] = panels
        self.ratios: list[int] = ratios
        self.direction: str = direction.lower()
        if self.direction not in ["h", "v"]:
            raise ValueError("Direction must be either 'h' or 'v'")

        total: int = sum(self.ratios)
        self.scales: list[float] = [ratio / total for ratio in self.ratios]
        self.layouts: list[tuple[pygame.Rect, Panel]] = []

        self.active_panel: int = 0

    def get_layouts(
        self, width: int, height: int, pos: tuple[int, int]
    ) -> list[tuple[pygame.Rect, Panel]]:
        layouts = []
        offset = 0
        total = sum(self.scales)
        x: int = pos[0]
        y: int = pos[1]

        for scale, panel in zip(self.scales, self.panels):
            norm_scale = scale / total
            if self.direction == "v":
                h = int(height * norm_scale)
                rect = pygame.Rect(x, y + offset, width, h)
                offset += h
            else:
                w = int(width * norm_scale)
                rect = pygame.Rect(x + offset, y, w, height)
                offset += w
            layouts.append((rect, panel))

        return layouts

    def update(
        self,
        events: list[pygame.event.Event],
        pos: tuple[int, int],
        width: int,
        height: int,
        active: bool = False,
    ) -> list[pygame.event.Event]:
        self.layouts = self.get_layouts(width, height, pos)
        handled: list[pygame.event.Event] = []
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, (rect, panel) in enumerate(self.layouts):
                    if rect.collidepoint(event.pos):
                        self.active_panel = i
                        panel.on_active()
                        handled.append(event)
                        break

        for i, (rect, panel) in enumerate(self.layouts):
            events = panel.update(
                events,
                rect.topleft,
                rect.width,
                rect.height,
                active=(i == self.active_panel and active),
            )

        for event in handled:
            if event in events:
                events.remove(event)

        return events

    def draw(
        self, pos: tuple[int, int], width: int, height: int, active: bool = False
    ) -> pygame.Surface:
        surface = pygame.Surface((width, height))
        for i, (rect, panel) in enumerate(self.layouts):
            panel_surface = panel.draw(
                rect.topleft,
                rect.width,
                rect.height,
                active=(i == self.active_panel and active),
            )
            surface.blit(panel_surface, (rect.left - pos[0], rect.top - pos[1]))
        return surface
