import pygame
from pygame import Color
from constants import HEIGHT, WIDTH, FPS, BLACK
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

        self.level = Level()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.screen.fill(Color("#658da0"))
            delta_time = self.clock.tick(FPS)

            self.handle_events()
            self.level.run()

            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
