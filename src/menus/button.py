# -*- coding: utf-8 -*-
from typing import Tuple, Union, Optional, Callable
from pygame import Surface, SRCALPHA, Color
from pygame import MOUSEBUTTONUP
from pygame.event import Event
from pygame.font import SysFont
from constants import DEFAULT_BUTTON_SIZE
from .drawable import Drawable
import pygame


class Button(Drawable):
    DEFAULT_COLOR = "#4682b4"

    def __init__(
        self,
        text: str,
        position: Tuple[int, int],
        parent: Union[Drawable, Surface],
        size: Tuple[int, int] = DEFAULT_BUTTON_SIZE,
        image: Optional[Surface] = None,
        font_size: Optional[int] = None,
        font_color: Optional[Union[str, tuple, Color]] = "#ffffff",
        action: Optional[Callable] = None,
    ):
        super().__init__(size, position, parent, image)
        self.set_color(Button.DEFAULT_COLOR)

        font_inflation = -10
        min_dim = min(size) // 2 + font_inflation
        font_size = min(font_size, min_dim) if font_size else min_dim
        self.font = SysFont("monospace", font_size)
        self.text_surf = self.font.render(text, True, Color(font_color))
        self.text_surf_rect = self.text_surf.get_rect(
            center=(size[0] // 2, size[1] // 2)
        )

        self.action = lambda: print("<Empty>") if action is None else action

        self.set_center()

    def draw(self):
        self.image.fill(Button.DEFAULT_COLOR)
        self.image.blit(self.text_surf, self.text_surf_rect)
        super().draw()

    def on_hover(self):
        self.set_opacity(200)

    def mouse_event(self):
        pass

    def update(self, event: Optional[Event]):
        if event is None:
            return
        if event.type == MOUSEBUTTONUP:
            if self.global_rect.collidepoint(event.pos):
                self.action()
