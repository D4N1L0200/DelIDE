import pygame
from . import Panel
from ..data import File
from typing import Optional
from ..signal_manager import SignalManager


class CodePanel(Panel):
    def __init__(self) -> None:
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/undefined-medium.ttf", 20
        )
        self.file: Optional[File] = None
        self.lines: list[str] = [""]
        self.file_path: str = ""

        SignalManager.register("p.code.update_file", self.to_get_file)
        SignalManager.listen("p.explorer.open_file", self.on_open_file)

    def to_get_file(self) -> None:
        if not self.file_path:
            return

        SignalManager.emit(
            "p.code.update_file",
            {"file": self.file},
        )

    def on_open_file(self, data: dict) -> None:
        self.file = data["file"]
        self.file_path = data["file"].path

        if self.file:
            if not self.file.byte_file:
                self.lines = data["file"].read()
            else:
                self.lines = ["Byte file"]

        SignalManager.emit(
            "p.code.update_file",
            {"file": self.file},
        )

    def on_active(self) -> None:
        self.to_get_file()

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
                if not self.file or self.file.byte_file:
                    events.remove(event)

                    continue

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.lines.append("")
                    elif event.key == pygame.K_BACKSPACE:
                        if self.lines[-1]:
                            self.lines[-1] = self.lines[-1][:-1]
                        else:
                            self.lines.pop()
                    else:
                        self.lines[-1] += event.unicode

                    self.file.write(self.lines)

                    SignalManager.emit(
                        "p.code.update_file",
                        {"file": self.file},
                    )
                    events.remove(event)

        return events

    def draw(
        self, pos: tuple[int, int], width: int, height: int, active: bool = False
    ) -> pygame.Surface:
        surface: pygame.Surface = super().draw(pos, width, height, active)

        line_height: int = self.font.get_height()
        for i, line in enumerate(self.lines):
            try:
                surface.blit(
                    self.font.render(line, False, (255, 255, 255)),
                    (10, line_height * i),
                )
            except ValueError:
                print(f"Error rendering line {i}: {line}")
                assert self.file
                self.file.byte_file = True
                self.lines = ["Byte file"]

        pygame.draw.rect(
            surface,
            (130, 50, 150) if active else (255, 255, 255),
            (0, 0, width, height),
            2 if active else 1,
        )

        return surface
