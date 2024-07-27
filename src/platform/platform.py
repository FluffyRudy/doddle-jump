from typing import Tuple, List
from enum import Enum
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame_utility.image_util import load_image
from random import choice, choices
from constants import (
    WIDTH,
    HEIGHT,
    DEFAULT_PLATFORM_SIZE,
    SCREEN_CENTER,
    DEFAULT_PLATFORM_SPEED,
)
from config import GRAPHICS


class PlatformTypes(Enum):
    STATIC = "platform"
    BROKEN = "broken"
    KINETIC = "kinetic"


SURFACES = {
    PlatformTypes.STATIC: GRAPHICS / "platform.png",
    PlatformTypes.BROKEN: GRAPHICS / "platform-broken.png",
    PlatformTypes.KINETIC: GRAPHICS / "platform.png",
}


class Platform(Sprite):
    last_x = (SCREEN_CENTER[0] - DEFAULT_PLATFORM_SIZE[0]) // 2
    last_y = HEIGHT - DEFAULT_PLATFORM_SIZE[1]

    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int],
        platform_type: PlatformTypes,
    ):
        super().__init__()
        self.image = load_image(SURFACES[platform_type], scale_size=size)
        self.rect = self.image.get_rect(topleft=position)

    @staticmethod
    def update_position(position: Tuple[int, int]):
        Platform.last_x = position[0]
        Platform.last_y = position[1]

    @staticmethod
    def get_last_pos() -> Tuple[int, int]:
        return Platform.last_x, Platform.last_y

    @staticmethod
    def reset_position():
        Platform.last_x = (SCREEN_CENTER[0] - DEFAULT_PLATFORM_SIZE[0]) // 2
        Platform.last_y = HEIGHT - DEFAULT_PLATFORM_SIZE[1]

    def scroll(self, distance: int):
        self.rect.y += distance

    def isoffview(self):
        return self.rect.top > HEIGHT

    def collision_effect(self):
        pass


class StaticPlatform(Platform):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size, PlatformTypes.STATIC)


class BrokenPlatform(Platform):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size, PlatformTypes.BROKEN)
        self.destroyed = False

    def collision_effect(self):
        self.destroyed = True


class KineticPlatform(Platform):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size, PlatformTypes.KINETIC)
        self.speed = DEFAULT_PLATFORM_SPEED
        self.direction = Vector2(choice([-1, 1]), 0)

    def update(self):
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.direction.x *= -1
        self.rect.x += self.speed * self.direction.x


def create_platform(
    position: Tuple[int, int], size: Tuple[int, int] = DEFAULT_PLATFORM_SIZE
) -> Platform:
    platform_types: List[Platform] = [StaticPlatform, BrokenPlatform, KineticPlatform]
    weight = [0.92, 0.05, 0.03]
    platform_type: Platform = choices(platform_types, weights=weight)[0]
    return platform_type(position, DEFAULT_PLATFORM_SIZE)
