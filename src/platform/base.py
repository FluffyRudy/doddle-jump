from typing import Tuple
from pygame.sprite import Sprite
from pygame_utility.image_util import load_image
from constants import WIDTH, HEIGHT
from config import GRAPHICS


class Platform(Sprite):
    def __init__(self, position: Tuple[int, int]):
        super().__init__()
        self.image = load_image(GRAPHICS / "platform.png", (0.7, 0.7))
        self.rect = self.image.get_rect(topleft=position)

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

    def scroll(self, distance: int):
        self.rect.y += distance

    def update(self, *args, **kwargs):
        if self.rect.bottom > int(HEIGHT * 1.2):
            self.kill()
