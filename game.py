import pygame
from typing import List
from pygame.event import Event
from pygame import Color
from constants import HEIGHT, WIDTH, FPS, BLACK, SCREEN_CENTER
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("DOODLE JUMP")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True
        self.start = False
        self.paused = False
        self.on_menu = False

        self.level = Level()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                and not self.start
            ):
                self.start = True

    def run(self):
        while self.running:
            self.screen.fill(Color("#658da0"))
            delta_time = self.clock.tick(FPS)

            self.handle_events()

            self.level.draw()
            if self.start and not self.paused and not self.on_menu:
                self.level.update()

            if not self.on_menu and not self.start:
                self.level.display_start_message()

            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
