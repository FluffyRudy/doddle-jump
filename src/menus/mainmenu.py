import pygame
from typing import Tuple, Optional
from pygame import Surface
from src.menus.button import Button
from src.menus.drawable import Drawable


class Mainmenu(Drawable):
    def __init__(
        self, size: Tuple[int, int], position: tuple[int, int], parent: Surface
    ):
        super().__init__(size, position, parent, image=None)
        self.set_color((100, 255, 200, 100))

        self.set_center()

        game_start = Button("Start", (0, 0), self, (100, 50), None)
        self.add_widget(game_start)

    def update(self, event: Optional[pygame.event.Event]):
        for child in self.children:
            child.update(event)
        pygame.draw.rect(self.display_surf, "red", self.global_rect, 5)
