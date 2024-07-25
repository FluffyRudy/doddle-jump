import pygame
from random import randint
from pygame.sprite import Group, GroupSingle
from src.characters.player.doodle import Doodle
from src.platform.base import Platform
from constants import (
    SCREEN_CENTER,
    WIDTH,
    HEIGHT,
    RANGE_PLATFORM,
    MIN_SPACING_Y,
    MAX_SPACING_Y,
    SCROLLING_TOP,
    JUMP_SPEED,
    SCROLLING_RECT,
    DEFAULT_PLATFORM_SIZE,
)


class Level:
    def __init__(self):
        self.setup()

    def setup(self):
        self.main_surface = pygame.display.get_surface()
        self.player = Doodle(
            position=(SCREEN_CENTER[0], HEIGHT - DEFAULT_PLATFORM_SIZE[1])
        )
        self.player_group = GroupSingle(self.player)

        self.visible_group = Group()
        self.platform_group = Group()
        self.scrolling_rect = pygame.Rect(SCROLLING_RECT)

        self.create_platforms()

        self.player.hitbox.midbottom = self.platform_group.sprites()[0].rect.topleft

    def create_platforms(self):
        platforms_len = len(self.platform_group.sprites())
        if platforms_len < RANGE_PLATFORM:
            for platform_index in range(
                -RANGE_PLATFORM + platforms_len, RANGE_PLATFORM - platforms_len
            ):
                pos_x = randint(0, WIDTH)
                pos_y = platform_index * randint(MIN_SPACING_Y, MAX_SPACING_Y)
                platform = Platform((pos_x, pos_y))
                self.visible_group.add(platform)
                self.platform_group.add(platform)

            for platform in self.platform_group.sprites():
                for other_platform in self.platform_group.sprites():
                    if platform is not other_platform and platform.rect.colliderect(
                        other_platform
                    ):
                        platform.kill()
                        break

    def handle_platform_collision(self):
        for platform in self.platform_group.sprites():
            if self.player.hitbox.colliderect(platform.rect):
                if self.player.hitbox.bottom <= platform.rect.top + JUMP_SPEED:
                    self.player.jump()

    def scroll(self):
        if self.player.hitbox.top <= SCROLLING_TOP:
            scroll_amount = SCROLLING_TOP - self.player.hitbox.top
            self.player.hitbox.y += scroll_amount
            for platform in self.platform_group.sprites():
                platform.scroll(scroll_amount)

    def draw(self):
        self.visible_group.draw(self.main_surface)
        self.player_group.draw(self.main_surface)

    def update(self):
        self.handle_platform_collision()
        self.visible_group.update()
        self.player_group.update()
        self.create_platforms()
        self.scroll()
        # pygame.draw.rect(self.main_surface, "red", self.scrolling_rect)

    def run(self):
        self.update()
        self.draw()
