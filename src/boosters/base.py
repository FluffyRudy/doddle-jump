from typing import Tuple, List
from pygame import Surface
from pygame.sprite import Sprite


class Booster(Sprite):
    """
    A Pygame Sprite class for handling a booster with animation and activation.

    Attributes:
        image (Surface): The current image of the booster.
        rect (Rect): The rectangle area of the booster, used for positioning and collision.
    """

    def __init__(
        self,
        midbottom_position: Tuple[int, int],
        animation_frames: List[Surface],
        animation_duration: int,
        is_active: bool = False,
        repeat_animation: bool = False,
    ):
        """
        Initializes the Booster with animation frames and settings.

        Args:
            midbottom_position (Tuple[int, int]): The (x, y) coordinates for the midbottom position of the booster.
            animation_frames (List[Surface]): A list of Pygame surfaces representing the frames of the animation.
            animation_duration (int): The total duration in milliseconds for the entire animation cycle.
            is_active (bool, optional): Whether the booster is active. Defaults to False.
            repeat_animation (bool, optional): Whether the animation should repeat after completing. Defaults to False.
        """
        super().__init__()
        self.__frames = animation_frames
        self.__frame_index = 0
        self.__animation_speed = animation_duration / 1000.0

        self.__is_active = is_active
        self.__repeat_animation = repeat_animation

        self.image = self.__frames[0]
        self.rect = self.image.get_rect(midbottom=midbottom_position)
        self.rect.inflate_ip(0, -10)

    def activate(self):
        """
        Activates the booster.
        """
        self.__is_active = True

    def is_active(self) -> bool:
        """
        Checks if the booster is active.

        Returns:
            bool: True if the booster is active, False otherwise.
        """
        return self.__is_active

    def is_repeatable(self) -> bool:
        """
        Checks if the animation should repeat after completing.

        Returns:
            bool: True if the animation should repeat, False otherwise.
        """
        return self.__repeat_animation

    def scroll(self, distance: int):
        """
        Scrolls the booster vertically by the specified distance.

        Args:
            distance (int): The distance to scroll the booster.
        """
        self.rect.y += distance

    def animate(self) -> bool:
        """
        Updates the animation frame of the booster.

        Returns:
            bool: True if the last frame was reached and the animation should repeat, False otherwise.
        """
        if not self.is_active():
            return False

        reach_last_frame = False
        self.__frame_index += self.__animation_speed
        if self.__frame_index >= len(self.__frames):
            self.__frame_index = 0
            reach_last_frame = True

        self.image = self.__frames[int(self.__frame_index)]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        return reach_last_frame
