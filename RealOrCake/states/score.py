# states/score.py

import pygame, os
from decoModule import load_image, get_base_path
from randomGameScoreboard import RandomGameScoreboard
from cakeDecorator import CakeDecorator
from button import Button

RATIO_720p = 1.5
BASE_PATH  = get_base_path()

class Score:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display       = display
        self.gsm           = gameStateManager
        self.screen_w      = screen_w
        self.screen_h      = screen_h
        self.sound_manager = sound_manager

        # Backgrounds
        self.bg_win  = load_image("background", "score_win_bg.png", (self.screen_w, self.screen_h))
        self.bg_lose = load_image("background", "score_lose_bg.png", (self.screen_w, self.screen_h))

        # Scoreboard frame
        self.board     = load_image("other", "scoreboard.png", (562, 548))
        self.board_pos = (171, 17)

        # Next button (scale ahead)
        next_img = load_image("button", "next_button.png")
        sw, sh = int(next_img.get_width()/RATIO_720p), int(next_img.get_height()/RATIO_720p)
        self.next_surf       = pygame.transform.scale(next_img, (sw, sh))
        self.next_button     = Button(1097, 624, self.next_surf, 1)
        self.next_button_rect = pygame.Rect(1097, 624, sw, sh)

        # Font for star
        font_path = os.path.join(BASE_PATH, "assets", "font", "nura-jeni-thin.ttf")
        self.font = pygame.font.Font(font_path, 50)

        # We'll store these in enter()
        self.scoreboard     = None
        self.player_cake    = None
        self.random_cake    = None
        self.star_text      = None
        self.music_loaded   = False

    def enter(self):
        # 1) Prepare data & scoring
        self.player_cake = self.gsm.get_cake()
        self.random_cake = self.gsm.get_randomcake()

        sb = RandomGameScoreboard(
            self.player_cake.get_parts(),
            self.random_cake.get_parts(),
            self.gsm
        )
        sb.calculate_score()                 # populate per-line and final
        star = sb.score_5star()              # number of filled stars
        self.scoreboard = sb

        # 2) Prepare the star text
        self.star_text = self.font.render(str(star), True, (0,0,0))

        # 3) Play music once
        if not self.music_loaded:
            pygame.mixer.music.stop()
            fname = "ShowScorePage[Win].mp3" if star>2 else "ShowScorePage[Lose].mp3"
            pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", fname))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            self.music_loaded = True

    def run(self):
        # 1) background
        bg = self.bg_win if self.scoreboard.score_5star()>2 else self.bg_lose
        self.display.blit(bg, (0,0))

        # 2) board frame
        self.display.blit(self.board, self.board_pos)

        # 3) draw decorated cakes on top of the board
        #    left: random cake
        rnd = CakeDecorator(self.random_cake, self.display)
        for part,(ptype,color) in self.random_cake.get_parts().items():
            rnd.add_decoration(part, ptype, color, (170,170))
        rnd.decorate(357, 357, (170,170))

        #    right: player cake
        ply = CakeDecorator(self.player_cake, self.display)
        for part,(ptype,color) in self.player_cake.get_parts().items():
            ply.add_decoration(part, ptype, color, (310,310))
        ply.decorate(617, 369, (310,310))

        # 4) star count (over the center star)
        self.display.blit(self.star_text, (428, 50))

        # 5) draw the scoreboard table (per‐line / final)
        self.scoreboard.render(self.display)  # will draw text at the right positions over the board

        # 6) Next button
        self.next_button.draw(self.display)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_button_rect.collidepoint(event.pos):
                self.gsm.set_state('end')
