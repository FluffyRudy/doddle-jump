from typing import Tuple
from pygame_utility.image_util import load_frames
from random import choice
from ..base import Character
from constants import WIDTH, HEIGHT, WASP_SPEED
from config import GRAPHICS


class Wasp(Character):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)

        self.__frames = load_frames(GRAPHICS / "wasp")
        self.__frame_index = 0
        self.__animation_speed = 0.2

        self.image = self.__frames[self.__frame_index]
        self.rect = self.image.get_rect(topleft=position)

        self.__speed = choice([1, -1]) * WASP_SPEED

    def update(self, *args, **kwargs):
        self.animate()
        self.movement()
        if self.rect.top > HEIGHT:
            self.kill()

    def movement(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.__speed *= -1
        elif self.rect.left < 0:
            self.rect.left = 0
            self.__speed *= -1
        self.rect.x += self.__speed

    def animate(self):
        reach_last_frame = False
        self.__frame_index += self.__animation_speed
        if self.__frame_index >= len(self.__frames):
            self.__frame_index = 0
            reach_last_frame = True
        self.image = self.__frames[int(self.__frame_index)]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        return reach_last_frame

    def scroll(self, distance: int):
        self.rect.y += distance
