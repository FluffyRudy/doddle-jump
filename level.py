import pygame
from typing import Tuple
from functools import reduce
from random import randint, choice
from pygame.sprite import Group, GroupSingle
from src.characters.player.doodle import Doodle
from src.platform.effects import EffectTypes, effect_map
from src.platform.platform import (
    Platform,
    StaticPlatform,
    KineticPlatform,
    BrokenPlatform,
    create_platform,
)
from constants import (
    SCREEN_CENTER,
    WIDTH,
    HEIGHT,
    INITIAL_PLATFORM_COUNT,
    DEFAULT_MIN_SPACING_X,
    DEFAULT_MAX_SPACING_X,
    DEFAULT_MIN_SPACING_Y,
    DEFAULT_MAX_SPACING_Y,
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
        self.game_over = False

    def setup(self):
        Platform.reset_position()
        self.main_surface = pygame.display.get_surface()
        self.player = Doodle(
            position=(SCREEN_CENTER[0], HEIGHT - DEFAULT_PLATFORM_SIZE[1])
        )

        self.player_group = GroupSingle(self.player)
        self.visible_group = Group()
        self.platform_group = Group()
        self.effects_group = []

        self.create_platforms()
        bottom_platform_rect = self.bottomost_platform().rect
        self.player.hitbox.midbottom = (
            bottom_platform_rect.centerx,
            bottom_platform_rect.top - 5,
        )
        self.player_group.update()

        self.total_scroll = 0
        self.score = 0
        self.font = pygame.font.Font(None, 50)
        self.score_surface = pygame.Surface(SCORE_CONTAINER_SIZE, pygame.SRCALPHA)
        self.score_surface.fill(pygame.Color(SCORE_CONTAINERE_BG))
        self.score_surface.set_alpha(100)

    def create_platforms(self):
        _, last_y = Platform.get_last_pos()
        while len(self.platform_group.sprites()) < INITIAL_PLATFORM_COUNT:
            pos_x = randint(DEFAULT_MIN_SPACING_X, DEFAULT_MAX_SPACING_X)
            pos_y = last_y - randint(DEFAULT_MIN_SPACING_Y, DEFAULT_MAX_SPACING_Y)
            last_y = pos_y
            platform = create_platform((pos_x, pos_y))
            self.visible_group.add(platform)
            self.platform_group.add(platform)
            Platform.update_position((pos_x, last_y))

    def manage_platforms_scrolling(self):
        if self.player.hitbox.top <= SCROLLING_TOP:
            scroll_amount = SCROLLING_TOP - self.player.hitbox.top
            self.player.hitbox.y += scroll_amount
            for platform in self.platform_group.sprites():
                platform.scroll(scroll_amount)
                if platform.isoffview():
                    last_x, last_y = Platform.get_last_pos()
                    last_y = self.topmost_platform().rect.y - randint(
                        DEFAULT_MIN_SPACING_Y, DEFAULT_MAX_SPACING_Y
                    )
                    Platform.update_position((last_x, last_y))
                    platform.kill()
            self.total_scroll += scroll_amount

    def handle_platform_collision(self):
        if self.player.velocity_y <= 0:
            return
        for platform in self.platform_group.sprites():
            if self.player.is_on_platform(platform.rect):
                self.player.hitbox.bottom = platform.rect.top
                self.player.rect.center = self.player.hitbox.center
                self.player.jump()
                if isinstance(platform, BrokenPlatform):
                    self.add_effect(
                        EffectTypes.BROKEN, platform.rect.center, platform.rect.size
                    )
                    platform.kill()
                break

    def topmost_platform(self) -> Platform:
        return min(self.platform_group.sprites(), key=lambda platform: platform.rect.y)

    def bottomost_platform(self) -> Platform:
        return max(self.platform_group.sprites(), key=lambda platform: platform.rect.y)

    def add_effect(
        self, effect_type: EffectTypes, position: Tuple[int, int], size: Tuple[int, int]
    ):
        effect = effect_map[effect_type]
        self.effects_group.append(effect(position, size))

    def manage_effect(self):
        for effect in self.effects_group[:]:
            scroll_amount = effect.left_rect.top - self.player.rect.bottom
            effect.update(scroll_amount // 10)
            effect.draw(self.main_surface)
            if effect.isoffview():
                self.effects_group.remove(effect)

    def update_score(self):
        self.score = int(self.total_scroll // 10)

    def display_score(self):
        score_ui = self.font.render(f"{self.score}", True, pygame.Color(BLACK))
        score_x = (self.score_surface.get_width() - score_ui.get_width()) // 2
        score_y = (self.score_surface.get_height() - score_ui.get_height()) // 2
        self.score_surface.blit(score_ui, (score_x, score_y))
        self.main_surface.blit(self.score_surface, (0, 0))
        self.score_surface.fill(SCORE_CONTAINERE_BG)

    def display_start_message(self):
        message = "PRESS ENTER TO CONTINUE"
        start_message = self.font.render(message, True, BLACK)
        start_rect = start_message.get_rect(center=SCREEN_CENTER)
        self.main_surface.blit(start_message, start_rect.topleft)

    def is_player_dead(self):
        if self.player.hitbox.bottom >= HEIGHT:
            return True
        return False

    def update(self):
        self.handle_platform_collision()
        self.visible_group.update()
        self.player_group.update()
        self.create_platforms()
        self.manage_platforms_scrolling()
        self.manage_effect()
        self.update_score()

    def draw(self):
        self.visible_group.draw(self.main_surface)
        self.player_group.draw(self.main_surface)
        self.display_score()
