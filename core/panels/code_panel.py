import pygame
from . import Panel
from ..signal_manager import SignalManager


class CodePanel(Panel):
    def __init__(self, file_name: str) -> None:
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/undefined-medium.ttf", 20
        )
        self.lines: list[str] = [""]
        self.file_name: str = file_name

        SignalManager.listen("code_panel.update_text.get", self.to_get_file)
        SignalManager.listen("ide.get_file.post", self.on_get_file)

    def to_get_file(self, data: dict) -> None:
        SignalManager.emit(
            "code_panel.update_text.post",
            {"file_name": self.file_name, "lines": self.lines},
        )

    def on_get_file(self, data: dict) -> None:
        if data["file"].name == self.file_name:
            self.lines = data["file"].read()

    def on_active(self) -> None:
        self.to_get_file({})

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.lines.append("")
                    else:
                        self.lines[-1] += event.unicode

                    SignalManager.emit(
                        "code_panel.update_text.post",
                        {"file_name": self.file_name, "lines": self.lines},
                    )
                    events.remove(event)

        return events

    def draw(
        self, pos: tuple[int, int], width: int, height: int, active: bool = False
    ) -> pygame.Surface:
        surface: pygame.Surface = super().draw(pos, width, height, active)

        line_height: int = self.font.get_height()
        for i, line in enumerate(self.lines):
            surface.blit(
                self.font.render(line, False, (255, 255, 255)),
                (10, line_height * i),
            )

        pygame.draw.rect(
            surface,
            (130, 50, 150) if active else (255, 255, 255),
            (0, 0, width, height),
            2 if active else 1,
        )

        return surface
