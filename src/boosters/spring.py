from typing import Tuple
from pygame_utility import load_frames
from .base import Booster
from constants import HEIGHT
from config import GRAPHICS


class Spring(Booster):
    def __init__(self, midbottom_position: Tuple[int, int]):
        frame_duration = 200
        frames = load_frames(GRAPHICS / "spring")
        super().__init__(
            midbottom_position, frames, frame_duration, repeat_animation=False
        )

    def update(self, *args, **kwargs):
        if self.animate() and not self.is_repeatable():
            self.kill()
        if self.rect.top >= HEIGHT:
            self.kill()
