from typing import Tuple
from pygame.sprite import Sprite
from pygame_utility.image_util import load_image
from constants import WIDTH, HEIGHT, DEFAULT_PLATFORM_SIZE
from config import GRAPHICS


class Platform(Sprite):
    def __init__(
        self, position: Tuple[int, int], size: Tuple[int, int] = DEFAULT_PLATFORM_SIZE
    ):
        super().__init__()
        self.image = load_image(GRAPHICS / "platform.png", scale_size=size)
        self.rect = self.image.get_rect(topleft=position)

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

    def scroll(self, distance: int):
        self.rect.y += distance

    def update(self, *args, **kwargs):
        if self.rect.top > HEIGHT:
            self.kill()
