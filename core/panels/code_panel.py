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
        self.file_path: str = ""
        self.lines: list[str] = [""]

        self.cursor_pos: tuple[int, int] = (0, 0)
        self.cursor_x_prev: int = 0

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
                if not self.lines:
                    self.lines = [""]
            else:
                self.lines = ["Byte file"]

        SignalManager.emit(
            "p.code.update_file",
            {"file": self.file},
        )

    def on_active(self) -> None:
        self.to_get_file()

    def insert_char(self, char: str, pos: tuple[int, int]) -> None:
        line: str = self.lines[pos[1]]
        self.lines[pos[1]] = line[: pos[0]] + char + line[pos[0] :]

    def insert_break(self) -> None:
        line: str = self.lines[self.cursor_pos[1]]
        self.lines.insert(self.cursor_pos[1] + 1, line[self.cursor_pos[0] :])
        self.lines[self.cursor_pos[1]] = line[: self.cursor_pos[0]]
        self.cursor_pos = (0, self.cursor_pos[1] + 1)

    def delete_char(self, pos: tuple[int, int]) -> None:
        line: str = self.lines[pos[1]]
        if pos[0] < len(line):
            self.lines[pos[1]] = line[: pos[0]] + line[pos[0] + 1 :]
        elif pos[1] < len(self.lines) - 1:
            self.lines[pos[1]] += self.lines.pop(pos[1] + 1)

    def backspace_char(self, pos: tuple[int, int]) -> None:
        line: str = self.lines[pos[1]]
        if pos[0] > 0:
            self.lines[pos[1]] = line[: pos[0] - 1] + line[pos[0] :]
            self.cursor_pos = (pos[0] - 1, pos[1])
        elif pos[1] > 0:
            self.lines[pos[1] - 1] += self.lines.pop(pos[1])
            self.cursor_pos = (len(self.lines[pos[1] - 1]) - len(line), pos[1] - 1)

    def move_cursor_left(self) -> None:
        next_left = self.cursor_pos[0] - 1
        if next_left < 0:
            next_up = self.cursor_pos[1] - 1
            if next_up >= 0:
                self.cursor_pos = (len(self.lines[next_up]), next_up)
        else:
            self.cursor_pos = (next_left, self.cursor_pos[1])

        self.cursor_x_prev = self.cursor_pos[0]

    def move_cursor_right(self) -> None:
        next_right = self.cursor_pos[0] + 1
        if next_right > len(self.lines[self.cursor_pos[1]]):
            next_down = self.cursor_pos[1] + 1
            if next_down < len(self.lines):
                self.cursor_pos = (0, next_down)
        else:
            self.cursor_pos = (next_right, self.cursor_pos[1])

        self.cursor_x_prev = self.cursor_pos[0]

    def move_cursor_up(self) -> None:
        next_up = self.cursor_pos[1] - 1
        if next_up < 0:
            if self.cursor_pos == (0, 0):
                self.cursor_x_prev = 0
            self.cursor_pos = (0, 0)
        elif self.cursor_x_prev > len(self.lines[next_up]):
            self.cursor_pos = (len(self.lines[next_up]), next_up)
        else:
            self.cursor_pos = (self.cursor_x_prev, next_up)

    def move_cursor_down(self) -> None:
        next_down = self.cursor_pos[1] + 1
        if next_down >= len(self.lines):
            if self.cursor_pos == (0, len(self.lines) - 1):
                self.cursor_x_prev = 0
            self.cursor_pos = (0, len(self.lines) - 1)
        else:
            if self.cursor_x_prev > len(self.lines[next_down]):
                self.cursor_pos = (len(self.lines[next_down]), next_down)
            else:
                self.cursor_pos = (self.cursor_x_prev, next_down)

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
                    if event.key == pygame.K_LEFT:
                        self.move_cursor_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_cursor_right()
                    elif event.key == pygame.K_UP:
                        self.move_cursor_up()
                    elif event.key == pygame.K_DOWN:
                        self.move_cursor_down()
                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        self.insert_break()
                    elif event.key == pygame.K_BACKSPACE:
                        self.backspace_char(self.cursor_pos)
                    elif event.key == pygame.K_DELETE:
                        self.delete_char(self.cursor_pos)
                    else:
                        self.insert_char(event.unicode, self.cursor_pos)
                        self.cursor_pos = (self.cursor_pos[0] + 1, self.cursor_pos[1])

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

        char_width, char_height = self.font.size(" ")

        for i, line in enumerate(self.lines):
            try:
                surface.blit(
                    self.font.render(line, False, (255, 255, 255)),
                    (10, char_height * i),
                )
            except ValueError:
                print(f"Error rendering line {i}: {line}")
                assert self.file
                self.file.byte_file = True
                self.lines = ["Byte file"]

        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (
                10 + char_width * self.cursor_pos[0],
                char_height * self.cursor_pos[1],
                1,
                char_height,
            ),
        )

        pygame.draw.rect(
            surface,
            (130, 50, 150) if active else (255, 255, 255),
            (0, 0, width, height),
            2 if active else 1,
        )

        return surface
