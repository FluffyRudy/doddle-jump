import pygame
from typing import Callable, Optional
from pygame_utility.image_util import load_image
from constants import WIDTH, HEIGHT, BLACK
from config import GRAPHICS


class Mainmenu:
    BORDER_WIDTH = 5
    BORDER_RADIUS = 5
    MENUCOLOR = (104, 104, 104)
    BUTTON_OFFSET = 25

    def __init__(self, callback_dict: dict[str, Callable]):
        self.display_surface = pygame.display.get_surface()
        self.width = int(WIDTH * 0.6)
        self.height = int(HEIGHT * 0.6)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.surface_border_rect = self.surface_rect.inflate(
            Mainmenu.BORDER_WIDTH, Mainmenu.BORDER_WIDTH
        )
        self.surface.fill(self.MENUCOLOR)

        # buttons
        self.start_button_normal = load_image(GRAPHICS / "play.png")
        self.start_button_hover = load_image(GRAPHICS / "play-on.png")
        self.current_start_button = self.start_button_normal
        self.start_button_rect = self.start_button_normal.get_rect(
            midtop=(self.surface_rect.centerx, self.surface_rect.centery)
        )
        self.callback_dict = callback_dict

    def update(self, event: Optional[pygame.event.Event]):
        self.on_button_hover()
        if event and event.type == pygame.MOUSEBUTTONUP:
            if self.start_button_rect.collidepoint(event.pos):
                self.callback_dict["start"]()

    def on_button_hover(self):
        if self.start_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.current_start_button = self.start_button_hover
        elif self.current_start_button != self.start_button_normal:
            self.current_start_button = self.start_button_normal

    def draw(self):
        pygame.draw.rect(
            self.display_surface,
            self.MENUCOLOR,
            self.surface_border_rect,
            Mainmenu.BORDER_WIDTH,
            Mainmenu.BORDER_RADIUS,
        )
        self.display_surface.blit(self.surface, self.surface_rect.topleft)
        self.display_surface.blit(
            self.current_start_button, self.start_button_rect.topleft
        )
