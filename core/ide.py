import pygame
from .panels import *
from .file import File
from .signal_manager import SignalManager


class IDE:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()

        # Pygame
        self.width: int = 1280
        self.height: int = 720
        self.surface: pygame.Surface = pygame.display.set_mode(
            (self.width, self.height)
        )
        self.fps: int = 60
        self.running: bool = True
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.events: list[pygame.event.Event] = []
        pygame.display.set_caption("Del IDE")

        # UI
        self.panel: Panel = GroupPanel(
            [
                BlankPanel(),
                GroupPanel(
                    [
                        BlankPanel(),
                        BlankPanel(),
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
        self.file: File = File("test.txt")
        SignalManager.emit("ide.get_file.post", {"file": self.file.read()})
        SignalManager.listen("code_panel.update_text", self.on_update_text)
        
    def on_update_text(self, data: dict) -> None:
        self.file.write(data["lines"])

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.events.append(event)
                elif event.type == pygame.KEYDOWN:
                    self.events.append(event)

            self.surface.fill((0, 0, 0))

            unhandled_events: list[pygame.event.Event] = self.panel.update(
                self.events, self.width, self.height, active=True
            )
            if len(unhandled_events) > 0:
                print(f"\nUnhandled events: {unhandled_events}")

            panel_surface: pygame.Surface = self.panel.draw(
                self.width, self.height, active=True
            )
            self.surface.blit(panel_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
