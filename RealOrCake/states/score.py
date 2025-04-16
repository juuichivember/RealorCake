# states/score.py
import pygame, os
from decoModule import load_image, get_base_path
from randomGameScoreboard import RandomGameScoreboard
from cakeDecorator import CakeDecorator

RATIO_720p = 1.5
BASE_PATH = get_base_path()

class Score:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.sound_manager = sound_manager

        self.background_win = load_image("background", "score_win_bg.png", (self.screen_w, self.screen_h))
        self.background_lose = load_image("background", "score_lose_bg.png", (self.screen_w, self.screen_h))

        self.board = load_image("other", "scoreboard.png", (562, 548))
        self.board = pygame.transform.smoothscale(self.board, (562, 548))
        self.board_pos = (171, 17)

        next_button_img = load_image("button", "next_button.png")
        self.next_button = pygame.transform.scale(next_button_img, (int(next_button_img.get_width()/RATIO_720p), int(next_button_img.get_height()/RATIO_720p)))
        # Assuming button.Button is used as before:
        from button import Button
        self.next_button = Button(1097, 624, next_button_img, 1 / RATIO_720p)

        self.font = pygame.font.Font(os.path.join(BASE_PATH, "assets", "font", "nura-jeni-thin.ttf"), 50)
        self.music_loaded = False

    def run(self):
        self.player_cake = self.gameStateManager.get_cake()
        self.random_cake = self.gameStateManager.get_randomcake()
        self.scoreboard = RandomGameScoreboard(self.player_cake.get_parts(), self.random_cake.get_parts())
        self.scoreboard.calculate_score()
        star = self.scoreboard.score_5star()

        if not self.music_loaded:
            pygame.mixer.music.stop()
            if star > 2:
                pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", "ShowScorePage[Win].mp3"))
                pygame.mixer.music.set_volume(1)
            else:
                pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", "ShowScorePage[Lose].mp3"))
                pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            self.music_loaded = True

        if star > 2:
            self.display.blit(self.background_win, (0,0))
        else:
            self.display.blit(self.background_lose, (0,0))
        self.display.blit(self.board, self.board_pos)
        self.next_button.draw(self.display)

        self.star_text = self.font.render(str(star), True, (0, 0, 0))

        self.player_decorator = CakeDecorator(self.player_cake, self.display)
        self.random_decorator = CakeDecorator(self.random_cake, self.display)

        self.player_decorator.decorate(617, 369, (310, 310))
        self.random_decorator.decorate(357, 357, (170, 170))

        self.display.blit(self.star_text, (428, 50))

        self.scoreboard.render(self.display)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('end')
        if self.next_button.is_mouse_over():
            self.gameStateManager.set_state('end')

    def handle_events(self, event):
        pass

    def enter(self):
        self.music_loaded = False
