import pygame
from . import Panel


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

    def get_layouts(self, width: int, height: int) -> list[tuple[pygame.Rect, Panel]]:
        layouts = []
        offset = 0
        for scale, panel in zip(self.scales, self.panels):
            if self.direction == "v":
                h = int(height * scale)
                rect = pygame.Rect(0, offset, width, h)
                offset += h
            else:
                w = int(width * scale)
                rect = pygame.Rect(offset, 0, w, height)
                offset += w
            layouts.append((rect, panel))
        return layouts

    def update(
        self,
        events: list[pygame.event.Event],
        width: int,
        height: int,
        active: bool = False,
    ) -> list[pygame.event.Event]:
        self.layouts = self.get_layouts(width, height)
        handled: list[pygame.event.Event] = []
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, (rect, panel) in enumerate(self.layouts):
                    if rect.collidepoint(event.pos):
                        self.active_panel = i
                        handled.append(event)
                        break

        for i, panel in enumerate(self.panels):
            events = panel.update(events, width, height, active=(i == self.active_panel and active))

        for event in handled:
            if event in events:
                events.remove(event)

        return events

    def draw(self, width: int, height: int, active: bool = False) -> pygame.Surface:
        surface = pygame.Surface((width, height))
        for i, (rect, panel) in enumerate(self.layouts):
            panel_surface = panel.draw(
                rect.width, rect.height, active=(i == self.active_panel and active)
            )
            surface.blit(panel_surface, rect.topleft)
        return surface
