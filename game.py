import pygame
from pygame import Color
from constants import HEIGHT, WIDTH, FPS, BLACK


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True
        self.start = False
        self.paused = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FPS)
            self.screen.fill(Color(BLACK))

            self.handle_events()

            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
