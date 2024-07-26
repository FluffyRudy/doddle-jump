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
    SCORE_CONTAINER_SIZE,
    SCORE_CONTAINERE_BG,
    BLACK,
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

        self.total_scroll = 0
        self.score = 0
        self.font = pygame.font.Font(None, 50)
        self.score_surface = pygame.Surface(SCORE_CONTAINER_SIZE, pygame.SRCALPHA)
        self.score_surface.fill(pygame.Color(SCORE_CONTAINERE_BG))
        self.score_surface.set_alpha(100)

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
        if self.player.velocity_y > 0:
            for platform in self.platform_group.sprites():
                if self.player.hitbox.colliderect(platform.rect):
                    if self.player.hitbox.bottom <= platform.rect.top + JUMP_SPEED:
                        self.player.hitbox.bottom = platform.rect.top
                        self.player.rect.center = self.player.hitbox.center
                        self.player.jump()
                        break

    def scroll(self):
        if self.player.hitbox.top <= SCROLLING_TOP:
            scroll_amount = SCROLLING_TOP - self.player.hitbox.top
            self.player.hitbox.y += scroll_amount
            for platform in self.platform_group.sprites():
                platform.scroll(scroll_amount)
            self.total_scroll += scroll_amount

    def update_score(self):
        self.score = int(self.total_scroll // 10)

    def display_score(self):
        score_ui = self.font.render(f"{self.score}", True, pygame.Color(BLACK))
        score_x = (self.score_surface.get_width() - score_ui.get_width()) // 2
        score_y = (self.score_surface.get_height() - score_ui.get_height()) // 2
        self.score_surface.blit(score_ui, (score_x, score_y))
        self.main_surface.blit(self.score_surface, (0, 0))
        self.score_surface.fill(SCORE_CONTAINERE_BG)

    def update(self):
        self.handle_platform_collision()
        self.visible_group.update()
        self.player_group.update()
        self.create_platforms()
        self.scroll()
        self.update_score()

    def draw(self):
        self.visible_group.draw(self.main_surface)
        self.player_group.draw(self.main_surface)
        self.display_score()

    def run(self):
        self.update()
        self.draw()
