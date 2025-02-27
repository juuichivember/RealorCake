import pygame
import sys
from state import Start, RandomCake, Decoration, Score, End, Message
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
        self.random_cake = RandomCake(self.screen, self.gameStateManager, self.screen_w, self.screen_h)
        self.decoration = Decoration(self.screen, self.gameStateManager, self.screen_w, self.screen_h)
        self.score_page = Score(self.screen, self.gameStateManager, self.screen_w, self.screen_h)
        self.end = End(self.screen, self.gameStateManager, self.screen_w, self.screen_h)
        self.message = Message(self.screen, self.gameStateManager, self.screen_w, self.screen_h)

        self.states = {'start': self.start, 
                       'random_cake': self.random_cake,
                       'decoration': self.decoration,
                       'score_page': self.score_page,
                       'end': self.end,
                       'end_message': self.message
                       }


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.states[self.gameStateManager.get_state()].run()
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()