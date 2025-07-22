import pygame


class Panel:
    def __init__(self) -> None:
        pass

    def update(
        self,
        events: list[pygame.event.Event],
        width: int,
        height: int,
        active: bool = False,
    ) -> list[pygame.event.Event]:
        return events

    def draw(self, width: int, height: int, active: bool = False) -> pygame.Surface:
        surface: pygame.Surface = pygame.Surface((width, height))
        surface.fill((0, 0, 0))

        return surface
