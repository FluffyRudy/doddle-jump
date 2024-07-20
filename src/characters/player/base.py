from pygame.sprite import Sprite
from enum import Enum
from .state import Status


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.status = Status()
