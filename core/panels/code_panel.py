import pygame
from . import Panel
from ..signal_manager import SignalManager


class CodePanel(Panel):
    def __init__(self) -> None:
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/undefined-medium.ttf", 20
        )
        self.lines: list[str] = [""]
        self.file_path: str = ""

        SignalManager.listen("update_text.get", self.to_get_file)
        SignalManager.listen("get_file.post", self.on_get_file)
        SignalManager.listen("open_file.post", self.on_open_file)

    def to_get_file(self, data: dict) -> None:
        SignalManager.emit(
            "update_text.post",
            {"file_name": self.file_path, "lines": self.lines},
        )

    def on_get_file(self, data: dict) -> None:
        if data["file"].path == self.file_path:
            self.lines = data["file"].read()

    def on_open_file(self, data: dict) -> None:
        self.file_path = data["file"].path
        self.lines = data["file"].read()

        SignalManager.emit(
            "update_text.post",
            {"file_name": self.file_path, "lines": self.lines},
        )

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
                        "update_text.post",
                        {"file_name": self.file_path, "lines": self.lines},
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
