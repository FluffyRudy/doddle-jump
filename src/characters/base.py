from typing import Tuple
from pygame.sprite import Sprite
from enum import Enum
from .status import Status


class Player(Sprite):
    def __init__(self, position: Tuple[int, int]):
        super().__init__()
        self.status = Status()
