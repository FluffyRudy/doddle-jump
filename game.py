import pygame
from typing import Optional
from pygame import Color
from enum import Enum, auto
from constants import HEIGHT, WIDTH, FPS, ROWS, COLS, GRID_SIZE, GREY, LIGHTGREY
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
        self.main_menu = Mainmenu({"start": lambda: self.go_ingame()})

    def draw_grid(self):
        for i in range(ROWS):
            for j in range(COLS):
                pygame.draw.rect(
                    self.screen,
                    LIGHTGREY,
                    (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                    1,
                    1,
                )

    def go_ingame(self):
        self.main_state = GameState.INGAME

    def restart(self):
        self.level = Level()
        self.main_state = GameState.INGAME
        self.ingame_state = InGameState.NOTSTARTED

    def handle_events(self):
        self.event = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ingame_state = InGameState.STARTED
            self.event = event

    def manage_state(self):
        if self.main_state == GameState.MAINMENU:
            self.main_menu.update(self.event)
            self.main_menu.draw()
        elif self.main_state == GameState.INGAME:
            self.draw_grid()
            if self.ingame_state == InGameState.STARTED:
                self.level.update()
                self.level.draw()
            else:
                self.level.draw()
                self.level.display_message("PRESS SPACE TO START")
        elif self.main_state == GameState.PAUSED:
            pass
        elif self.main_state == GameState.GAMEOVER:
            self.restart()

        if self.level.is_player_dead():
            self.main_state = GameState.GAMEOVER

    def run(self):
        while self.running:
            self.screen.fill(GREY)

            delta_time = self.clock.tick(FPS)

            self.handle_events()
            self.manage_state()

            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
