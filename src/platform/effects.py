from typing import Tuple, Dict, Union
from enum import Enum
from pygame import Surface
from pygame.transform import rotate
from pygame_utility import load_image
from constants import DEFAULT_PLATFORM_SIZE, DEFAULT_PLATFORM_SPEED, HEIGHT
from config import GRAPHICS


class EffectTypes(Enum):
    BROKEN = 0


class BrokenPlatformEffect:
    def __init__(
        self,
        platform_center: Tuple[int, int],
        size: Tuple[int, int],
    ):
        self.left_piece = rotate(
            load_image(GRAPHICS / "broken_platform_piece0.png", scale_size=size), -45
        )
        self.right_piece = rotate(
            load_image(GRAPHICS / "broken_platform_piece1.png", scale_size=size), 45
        )
        self.left_piece_rect = self.left_piece.get_rect(topright=platform_center)
        self.right_piece_rect = self.right_piece.get_rect(topleft=platform_center)

    @property
    def left_rect(self):
        return self.left_piece_rect

    def update(self, scroll_speeed):
        self.left_piece_rect.y += scroll_speeed
        self.right_piece_rect.y += scroll_speeed

    def draw(self, display_surface: Surface):
        display_surface.blit(self.left_piece, self.left_piece_rect.topleft)
        display_surface.blit(self.right_piece, self.right_piece_rect.topleft)

    def isoffview(self):
        return self.left_piece_rect.top >= HEIGHT


effect_map: Dict[EffectTypes, Union[BrokenPlatformEffect]] = {
    EffectTypes.BROKEN: BrokenPlatformEffect
}
