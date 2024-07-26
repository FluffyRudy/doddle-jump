from typing import Tuple
from pygame.sprite import Sprite
from pygame_utility.image_util import load_image
from constants import WIDTH, HEIGHT, DEFAULT_PLATFORM_SIZE, SCREEN_CENTER
from config import GRAPHICS


class Platform(Sprite):
    last_x = (SCREEN_CENTER[0] - DEFAULT_PLATFORM_SIZE[0]) // 2
    last_y = HEIGHT - DEFAULT_PLATFORM_SIZE[1]

    def __init__(
        self, position: Tuple[int, int], size: Tuple[int, int] = DEFAULT_PLATFORM_SIZE
    ):
        super().__init__()
        self.image = load_image(GRAPHICS / "platform.png", scale_size=size)
        self.rect = self.image.get_rect(topleft=position)

    @classmethod
    def update_position(cls, position: Tuple[int, int]):
        cls.last_x = position[0]
        cls.last_y = position[1]

    @classmethod
    def get_last_pos(cls) -> Tuple[int, int]:
        return cls.last_x, cls.last_y

    def scroll(self, distance: int):
        self.rect.y += distance

    def isoffview(self):
        return self.rect.top > HEIGHT
