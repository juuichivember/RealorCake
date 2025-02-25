import pygame
import sys
from state import Start, Decoration, End
from stateManager import *
from screen import set_screen

#SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

# Default setup

class Game():
    def __init__(self):
        pygame.init()
        screen_size = pygame.display.get_desktop_sizes()
        self.screen_w, self.screen_h = set_screen(screen_size[0])

        pygame.display.set_caption("Namkhing's Cake")
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.clock = pygame.time.Clock()

        # Call Context's and Concrete State's Constructor
        self.gameStateManager = GameStateManager('start')
        self.start = Start(self.screen, self.gameStateManager, self.screen_w, self.screen_h)
        self.decoration = Decoration(self.screen, self.gameStateManager, self.screen_w, self.screen_h)
        self.end = End(self.screen, self.gameStateManager, self.screen_w, self.screen_h)

        self.states = {'start': self.start, 'decoration': self.decoration, 'end': self.end}


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.states[self.gameStateManager.get_state()].run()
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()