# -*- coding: utf-8 -*-
from typing import Tuple, List, Optional, Union, Callable
from pygame import Surface, SRCALPHA, Rect, Color, draw
from pygame import MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION
from pygame.event import Event
from pygame.display import get_surface as main_surface
from .dtype import DtypeDrawable


MouseEvent = Union[MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]


class Drawable(DtypeDrawable):
    def __init__(
        self,
        size: Tuple[int, int],
        position: Tuple[int, int],
        parent: Union["Drawable", Surface],
        image: Optional[Surface] = None,
    ):
        is_parent_surf = isinstance(parent, Surface)
        if is_parent_surf and parent is not main_surface():
            raise ValueError(
                "Surface must be a reference of pygame.display.get_surface() or Drawable"
            )

        self.image = Surface(size, SRCALPHA)
        if isinstance(image, Surface):
            self.image = image
        elif image is not None:
            warnmsg = f"Warning: Expected image as instance of Surface or NoneType got {type(image).__name__}"
            print(warnmsg)

        self.global_x = position[0] if is_parent_surf else parent.global_x + position[0]
        self.global_y = position[1] if is_parent_surf else parent.global_y + position[1]
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.global_rect = Rect(self.global_x, self.global_y, *size)
        self.parent = parent
        self.display_surf = parent if is_parent_surf else self.parent.image

        self.children: List["Drawable"] = []

    def add_widget(self, widget: "Drawable", index: Optional[int] = None):
        if index is not None:
            self.children.insert(index, widget)
        else:
            self.children.append(widget)

    def set_color(self, color: Union[Color, str, tuple]):
        self.image.fill(color)

    def set_opacity(self, opacity: int):
        self.image.set_alpha(opacity)

    def update_global_rect(self):
        if isinstance(self.parent, Drawable):
            self.global_x = self.parent.global_x + self.rect.x
            self.global_y = self.parent.global_y + self.rect.y
        else:
            self.global_x = self.rect.x
            self.global_y = self.rect.y
        self.global_rect = Rect(
            self.global_x, self.global_y, self.rect.width, self.rect.height
        )

    def set_center(self):
        parent_size = self.display_surf.get_size()
        center_x = int(parent_size[0] // 2)
        center_y = int(parent_size[1] // 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.update_global_rect()

    def draw(self):
        for child in self.children:
            child.draw()
        self.display_surf.blit(self.image, self.rect.topleft)

    def update(self, event: Optional[Event]):
        pass
