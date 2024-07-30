from typing import Tuple
from pygame_utility.image_util import load_image
from pygame import Rect
from pygame.sprite import Sprite
from pygame.transform import flip
from pygame.display import get_surface
from pygame import K_LEFT, K_RIGHT
from pygame.key import get_pressed
from pygame import Surface
from src.particle.particle import Stunned
from ..status import Direction, State
from ..base import Character
from config import GRAPHICS
from constants import DOODLE_SPEED, WIDTH, HEIGHT, GRAVITY, JUMP_SPEED, SCROLLING_TOP


class Doodle(Character):
    def __init__(self, position: Tuple[int, int]):
        self.main_surface = get_surface()
        super().__init__(position)
        self.image = load_image(GRAPHICS / "doodler-right.png", (0.7, 0.7))
        self.rect = self.image.get_rect(midbottom=position)
        self.hitbox = self.rect.inflate(-20, 0)
        self.velocity_y = 0
        self.jump_speed = JUMP_SPEED
        self.jump_speed_increment = 0
        self.jump_speed_inc_factor = 0.5
        self.speed = DOODLE_SPEED
        self.speed_increment = 0
        self.speed_inc_factor = 0.2

        self.is_dead = False
        self.stunned_effect = Stunned(self.rect.midtop)

    def movement(self):
        keys = get_pressed()
        dx, dy = 0, 0

        if keys[K_LEFT]:
            if self.status.get_status()[0] != Direction.LEFT:
                self.status.set_direction(Direction.LEFT)
                self.image = flip(self.image, True, False)
            dx -= self.speed
        elif keys[K_RIGHT]:
            if self.status.get_status()[0] != Direction.RIGHT:
                self.status.set_direction(Direction.RIGHT)
                self.image = flip(self.image, True, False)
            dx = self.speed

        self.velocity_y += GRAVITY
        dy += self.velocity_y

        self.hitbox.x += dx
        self.hitbox.y += dy
        self.rect.center = self.hitbox.center

        if self.hitbox.left > WIDTH:
            self.hitbox.right = 0
        elif self.hitbox.right < 0:
            self.hitbox.left = WIDTH

    def increase_speed(self):
        self.speed_increment += self.speed_inc_factor
        self.speed += int(self.speed_increment)

    def increase_jump_speed(self):
        self.jump_speed_increment += self.jump_speed_inc_factor
        self.jump_speed += int(self.jump_speed_increment)

    def jump(self, amplification: int = 1):
        self.velocity_y = -self.jump_speed * amplification

    def is_on_platform(self, platform_rect: Rect):
        threshold = abs(self.velocity_y * 1.5)
        if self.hitbox.colliderect(platform_rect):
            if self.hitbox.bottom <= platform_rect.top + int(threshold):
                return True
        return False

    def dead(self):
        self.is_dead = True

    def update(self, *args, **kwargs):
        self.movement()
        if self.is_dead:
            x = self.rect.centerx - self.stunned_effect.image.get_width() // 2
            y = self.rect.top - 50
            self.stunned_effect.draw(self.main_surface, (x, y))
            self.stunned_effect.animate()
