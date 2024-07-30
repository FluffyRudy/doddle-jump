from typing import Tuple, List
from pygame import Surface
from pygame.sprite import Sprite


class Booster(Sprite):
    def __init__(
        self,
        midbottom_position: Tuple[int, int],
        animation_frames: List[Surface],
        last_duration: int,
        is_active: bool = False,
        repeat_animation: bool = False,
    ):
        super().__init__()
        self.__frames = animation_frames
        self.__frame_index = 0
        self.__animation_speed = (last_duration / 1000.0) / len(self.__frames)

        self.__is_active = is_active
        self.__repeat_animation = repeat_animation

        self.image = self.__frames[0]
        self.rect = self.image.get_rect(midbottom=midbottom_position)
        self.rect.inflate_ip(0, -10)

    def activate(self):
        self.__is_active = True

    def is_active(self) -> bool:
        return self.__is_active

    def is_repeatable(self) -> bool:
        return self.__repeat_animation

    def scroll(self, distance: int):
        self.rect.y += distance

    def animate(self) -> bool:
        if not self.is_active():
            return
        reach_last_frame = False
        self.__frame_index += self.__animation_speed
        if self.__frame_index >= len(self.__frames):
            self.__frame_index = 0
            reach_last_frame = True
        self.image = self.__frames[int(self.__frame_index)]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        return reach_last_frame
