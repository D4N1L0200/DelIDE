import pygame
from . import Panel
from .. import SignalManager
from ..data import Folder
from typing import Optional


class ExItem:
    def __init__(
        self,
        name: str,
        path: str,
        size: int = 1,
        folder_ref: "ExFolder | None" = None,
        is_dedent: bool = False,
    ) -> None:
        self.name: str = name
        self.path: str = path
        self.size: int = size
        self.folder_ref: "ExFolder | None" = folder_ref
        self.is_dedent: bool = is_dedent


class ExFolder(Folder):
    def __init__(self, folder: Folder) -> None:
        super().__init__(folder.path)

        self.ex_folders: list[ExFolder] = []
        self.open: bool = True
        self.hover: bool = False

    def get_items(self) -> list[ExItem]:
        items: list[ExItem] = [
            ExItem(
                f"{self.path_list[-1]}/",
                "",
                len(self.folders) + len(self.files),
                folder_ref=self,
            )
        ]

        for folder in self.ex_folders:
            items.extend(folder.get_items())

        items.extend([ExItem(file.name, file.path) for file in self.files])
        items.append(ExItem("", "", is_dedent=True))

        return items


class ExplorerPanel(Panel):
    def __init__(self) -> None:
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/undefined-medium.ttf", 18
        )
        self.folder: Optional[ExFolder] = None
        self.items: list[ExItem] = []
        self.hovered_files: set[str] = set()

        SignalManager.listen("d.get_folder", self.on_get_folder)

    def on_get_folder(self, data: dict) -> None:
        def get_content(folder: ExFolder) -> ExFolder:
            if folder.path_list[-1] == "__pycache__":
                return folder

            for nested_folder in folder.folders:
                ex_nested_folder: ExFolder = get_content(ExFolder(nested_folder))
                folder.ex_folders.append(ex_nested_folder)

            return folder

        self.folder = ExFolder(data["folder"])
        self.folder = get_content(self.folder)

    def update(
        self,
        events: list[pygame.event.Event],
        pos: tuple[int, int],
        width: int,
        height: int,
        active: bool = False,
    ) -> list[pygame.event.Event]:
        text_height = self.font.get_height()
        mouse_event = None
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_event = event
                break

        draw_idx = 0

        def handle_folder(folder: ExFolder, tab: int) -> None:
            nonlocal draw_idx, mouse_event

            folder_rect = pygame.Rect(
                pos[0], pos[1] + text_height * draw_idx, width, text_height
            )

            folder.hover = folder_rect.collidepoint(mouse_pos)

            if mouse_event and folder_rect.collidepoint(mouse_event.pos):
                folder.open = not folder.open
                events.remove(mouse_event)
                mouse_event = None

            draw_idx += 1

            if not folder.open:
                return

            for sub in folder.ex_folders:
                handle_folder(sub, tab + 1)

            for file in folder.files:
                file_rect = pygame.Rect(
                    pos[0], pos[1] + text_height * draw_idx, width, text_height
                )

                if file_rect.collidepoint(mouse_pos):
                    self.hovered_files.add(file.path)
                else:
                    self.hovered_files.discard(file.path)

                if mouse_event and file_rect.collidepoint(mouse_event.pos):
                    events.remove(mouse_event)
                    mouse_event = None
                    SignalManager.emit("p.explorer.open_file", {"file": file})

                draw_idx += 1

        if self.folder is None:
            return events

        handle_folder(self.folder, 0)
        return events

    def draw(
        self, pos: tuple[int, int], width: int, height: int, active: bool = False
    ) -> pygame.Surface:
        surface: pygame.Surface = super().draw(pos, width, height, active)

        text_height: int = self.font.get_height()
        draw_idx: int = 0

        def draw_folder(folder: ExFolder, tab: int) -> None:
            nonlocal draw_idx

            if folder.hover:
                surface.fill(
                    (80, 60, 120), (0, text_height * draw_idx, width, text_height)
                )

            text = f"{"| " * tab}{"v" if folder.open else ">"} {folder.path_list[-1]}/"
            surface.blit(
                self.font.render(text, False, (255, 255, 255)),
                (10, text_height * draw_idx),
            )
            draw_idx += 1

            if not folder.open:
                return

            for sub in folder.ex_folders:
                draw_folder(sub, tab + 1)

            for file in folder.files:
                if file.path in self.hovered_files:
                    surface.fill(
                        (80, 60, 120), (0, text_height * draw_idx, width, text_height)
                    )

                text = f"{"| " * (tab + 1)}{file.name}{"" if file.saved else "*"}"
                surface.blit(
                    self.font.render(text, False, (255, 255, 255)),
                    (10, text_height * draw_idx),
                )
                draw_idx += 1

        if self.folder is not None:
            draw_folder(self.folder, 0)

        pygame.draw.rect(
            surface,
            (130, 50, 150) if active else (255, 255, 255),
            (0, 0, width, height),
            2 if active else 1,
        )

        return surface
