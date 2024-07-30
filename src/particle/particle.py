from typing import Tuple, List
from pygame import Surface
from pygame_utility.image_util import load_frames
from config import GRAPHICS


class Animation:
    def __init__(self, frames: List[Surface], animation_speed: float):
        self.__frames = frames
        self.__frame_index = 0
        self.__animation_speed = animation_speed

    def animate(self):
        reach_last_frame = False
        self.__frame_index += self.__animation_speed
        if self.__frame_index >= len(self.__frames):
            self.__frame_index = 0
            reach_last_frame = True
        self.image = self.__frames[int(self.__frame_index)]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        return reach_last_frame


class Stunned(Animation):
    def __init__(self, midtop_position: Tuple[int, int]):
        frames = load_frames(GRAPHICS / "stunned")
        animation_speed = 0.2
        super().__init__(frames, animation_speed)

        self.image = frames[0]
        self.rect = self.image.get_rect(midtop=midtop_position)

    def draw(self, surface: Surface, position: Tuple[int, int]):
        surface.blit(self.image, position)
