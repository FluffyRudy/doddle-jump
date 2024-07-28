import pygame
from typing import Optional
from pygame import Color
from enum import Enum, auto
from constants import HEIGHT, WIDTH, FPS
from level import Level
from src.menus.mainmenu import Mainmenu


class GameState(Enum):
    MAINMENU = auto()
    PAUSED = auto()
    INGAME = auto()
    GAMEOVER = auto()


class InGameState(Enum):
    STARTED = auto()
    NOTSTARTED = auto()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("DOODLE JUMP")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True
        self.main_state = GameState.MAINMENU
        self.ingame_state = InGameState.NOTSTARTED

        self.level = Level()

        self.event: Optional[pygame.event.Event] = None
        menu_size = int(WIDTH * 0.5), int(HEIGHT * 0.5)
        self.main_menu = Mainmenu(menu_size, (10, 0), self.screen)

    def restart(self):
        self.level = Level()

    def handle_events(self):
        self.event = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                pass
            self.event = event

    def manage_state(self):
        if self.main_state == GameState.MAINMENU:
            self.main_menu.update(self.event)
            self.main_menu.draw()
        elif self.main_state == GameState.INGAME:
            if self.ingame_state == InGameState.STARTED:
                self.level.update()
            else:
                self.level.display_message("PRESS SPACE TO START")
            self.level.draw()
        elif self.main_state == GameState.PAUSED:
            pass

    def run(self):
        while self.running:
            self.screen.fill(Color("#658da0"))
            delta_time = self.clock.tick(FPS)

            self.handle_events()
            self.manage_state()

            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
