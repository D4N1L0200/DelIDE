import pygame
from .panels import *
from .data import Data, File
from . import SignalManager
from typing import Optional

import tkinter as tk
from tkinter import filedialog


def open_folder_dialog() -> str | None:
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title="Select Folder")
    root.destroy()
    return folder_path if folder_path else None


class IDE:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()

        # Pygame
        self.surface: pygame.Surface = pygame.display.set_mode((0, 0))
        self.width: int = self.surface.get_width()
        self.height: int = self.surface.get_height()
        self.fps: int = 60
        self.running: bool = True
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.events: list[pygame.event.Event] = []
        pygame.display.set_caption("Del IDE")

        # UI
        self.panel: Panel = GroupPanel(
            [
                GroupPanel(
                    [
                        ButtonPanel("New", ""),
                        ButtonPanel("Open", "o.open"),
                        ButtonPanel("Save", "o.save"),
                        ButtonPanel("Exit", "o.exit"),
                    ],
                    0.08,
                    direction="h",
                ),
                GroupPanel(
                    [
                        GroupPanel(
                            [
                                ButtonPanel("E", ""),
                                ButtonPanel("S", ""),
                                ButtonPanel("G", ""),
                                ButtonPanel("R", ""),
                            ],
                            0.1,
                            direction="v",
                        ),
                        ExplorerPanel(),
                        GroupPanel(
                            [CodePanel(), BlankPanel()],
                            [7, 3],
                            direction="v",
                        ),
                    ],
                    [1, 4, 15],
                    direction="h",
                ),
                StatusPanel(),
            ],
            [1, 18, 1],
            direction="v",
        )

        # Data
        self.data: Data = Data()
        self.last_file: Optional[File] = None

        SignalManager.listen("p.code.update_file", self.on_update_file)
        SignalManager.listen("o.open", self.on_open)
        SignalManager.listen("o.save", self.on_save)
        SignalManager.listen("o.exit", self.on_exit)

    def on_update_file(self, data: dict) -> None:
        file: File = data["file"]
        pygame.display.set_caption(f"Del IDE - {file.path.split("/")[-1]}")
        self.last_file = file

    def on_open(self, data: dict) -> None:
        selected = open_folder_dialog()
        if selected:
            self.data.load(selected)

    def on_save(self, data: dict) -> None:
        if self.last_file is None:
            return

        self.data.save(self.last_file)

    def on_exit(self, data: dict) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.events.append(event)
                elif event.type == pygame.KEYDOWN:
                    event.mod &= ~(pygame.KMOD_NUM | pygame.KMOD_CAPS)

                    if event.mod & pygame.KMOD_CTRL:
                        if event.key == pygame.K_o:
                            SignalManager.emit("o.open", {})
                        elif event.key == pygame.K_s:
                            SignalManager.emit("o.save", {})
                    else:
                        if event.key == pygame.K_F5:
                            self.data.load(
                                "C:\\Users\\danil\\Documents\\Dev\\DelIDE\\demo"
                            )
                        elif event.unicode:
                            self.events.append(event)
                        else:
                            print(f"Unhandled key: {event.key}")

            self.surface.fill((0, 0, 0))

            unhandled_events: list[pygame.event.Event] = self.panel.update(
                self.events, (0, 0), self.width, self.height, active=True
            )
            if len(unhandled_events) > 0:
                print(f"\nUnhandled events: {unhandled_events}")

            panel_surface: pygame.Surface = self.panel.draw(
                (0, 0), self.width, self.height, active=True
            )
            self.surface.blit(panel_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
