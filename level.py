import pygame
from pygame.sprite import Group
from random import randint
from src.characters.player.doodle import Doodle
from src.platform.base import Platform
from constants import (
    SCREEN_CENTER,
    WIDTH,
    HEIGHT,
    MAX_PLATFORMS,
    MIN_SPACING_Y,
    MAX_SPACING_Y,
    SCROLLING_TOP,
    JUMP_SPEED,
    SCROLLING_RECT,
)


class Level:
    def __init__(self):
        self.main_surface = pygame.display.get_surface()
        self.player = Doodle(position=(SCREEN_CENTER[0], HEIGHT // 2))

        self.visible_group = Group()
        self.platform_group = Group()
        self.visible_group.add(self.player)

        self.scrolling_rect = pygame.Rect(SCROLLING_RECT)

        self.create_platforms()

    def create_platforms(self):
        platforms_len = len(self.platform_group.sprites())
        if platforms_len >= MAX_PLATFORMS:
            return
        for platform_index in range(MAX_PLATFORMS):
            pos_x = randint(int(0), int(WIDTH))
            pos_y = platform_index * randint(MIN_SPACING_Y, MAX_SPACING_Y)
            platform = Platform((pos_x, pos_y))
            self.visible_group.add(platform)
            self.platform_group.add(platform)

    def handle_platform_collision(self):
        for platform in self.platform_group.sprites():
            if (
                self.player.hitbox.colliderect(platform.rect)
                and self.player.velocity_y > 0
            ):
                if self.player.hitbox.bottom <= platform.rect.top + JUMP_SPEED:
                    self.player.jump()

    def scroll(self):
        if self.player.rect.top <= SCROLLING_TOP:
            for platform in self.platform_group.sprites():
                platform.scroll(abs(JUMP_SPEED))

    def draw(self):
        self.visible_group.update()
        self.visible_group.draw(self.main_surface)

    def update(self):
        self.create_platforms()
        self.handle_platform_collision()
        self.scroll()
        pygame.draw.rect(self.main_surface, "red", self.scrolling_rect)

    def run(self):
        self.update()
        self.draw()
