from typing import Tuple
from pygame_utility import load_frames
from .booster import Booster
from config import GRAPHICS


class Spring(Booster):
    def __init__(self, midbottom_position: Tuple[int, int]):
        last_duration = 1000
        frames = load_frames(GRAPHICS / "spring")
        super().__init__(midbottom_position, frames, last_duration)

    def update(self, *args, **kwargs):
        if self.is_lastframe():
            self.kill()
        self.animate()
