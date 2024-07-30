from typing import Tuple, List
from pygame import Surface
from pygame.sprite import Sprite


class Booster(Sprite):
    def __init__(
        self,
        midbottom_position: Tuple[int, int],
        animation_frames: List[Surface],
        last_duration: int,
    ):
        super().__init__()
        self.__frames = animation_frames
        self.__frame_index = 0
        self.__animation_speed = (last_duration / 1000.0) / len(self.__frames)

        self.image = self.__frames[0]
        self.rect = self.image.get_rect(midbottom=midbottom_position)

    def animate(self):
        self.__frame_index += self.__animation_speed
        if self.is_last_frame():
            self.__frame_index = 0
        self.image = self.__frames[int(self.__frame_index)]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def is_last_frame(self) -> bool:
        return self.__frame_index >= len(self.__frames)
