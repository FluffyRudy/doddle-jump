from typing import Tuple
from pygame_utility.image_util import load_image
from pygame import Rect
from pygame.sprite import Sprite
from pygame.transform import flip
from pygame import K_LEFT, K_RIGHT
from pygame.key import get_pressed
from pygame import Surface
from ..status import Direction, State
from ..base import Character
from config import GRAPHICS
from constants import DOODLE_SPEED, WIDTH, HEIGHT, GRAVITY, JUMP_SPEED, SCROLLING_TOP


class Doodle(Character):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)
        self.image = load_image(GRAPHICS / "doodler-right.png", (0.7, 0.7))
        self.rect = self.image.get_rect(midbottom=position)
        self.hitbox = self.rect.inflate(-20, 0)
        self.velocity_y = 0
        self.jump_speed = JUMP_SPEED
        self.speed = DOODLE_SPEED
        self.speed_increment = 0

        self.is_dead = False

    def movement(self):
        keys = get_pressed()
        dx, dy = 0, 0

        if keys[K_LEFT]:
            if self.status.get_status()[0] != Direction.LEFT:
                self.status.set_direction(Direction.LEFT)
                self.image = flip(self.image, True, False)
            dx -= self.speed + self.speed_increment
        if keys[K_RIGHT]:
            if self.status.get_status()[0] != Direction.RIGHT:
                self.status.set_direction(Direction.RIGHT)
                self.image = flip(self.image, True, False)
            dx = self.speed + self.speed_increment

        self.velocity_y += GRAVITY
        dy += self.velocity_y

        self.hitbox.x += dx
        self.hitbox.y += dy
        self.rect.center = self.hitbox.center

        if self.hitbox.left > WIDTH:
            self.hitbox.right = 0
        elif self.hitbox.right < 0:
            self.hitbox.left = WIDTH

    def jump(self, amplification: int = 1):
        self.velocity_y = -(self.jump_speed + self.speed_increment) * amplification

    def is_on_platform(self, platform_rect: Rect):
        threshold = abs(self.velocity_y * 1.5)
        if self.hitbox.colliderect(platform_rect):
            if self.hitbox.bottom <= platform_rect.top + int(threshold):
                return True
        return False

    def update(self, *args, **kwargs):
        if not self.is_dead:
            self.movement()
