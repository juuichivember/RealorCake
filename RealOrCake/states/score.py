import pygame, os
from decoModule import load_image, get_base_path
from randomGameScoreboard import RandomGameScoreboard
from cakeDecorator import CakeDecorator

RATIO_720p = 1.5
BASE_PATH = get_base_path()

class Score:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display = display
        self.gsm = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.sound_manager = sound_manager

        # Load backgrounds for win/lose
        self.bg_win = load_image("background", "score_win_bg.png", (self.screen_w, self.screen_h))
        self.bg_lose = load_image("background", "score_lose_bg.png", (self.screen_w, self.screen_h))

        # Scoreboard board image
        self.board = load_image("other", "scoreboard.png", (562, 548))
        self.board_pos = (171, 17)

        # Next button
        next_img = load_image("button", "next_button.png")
        self.next_button = pygame.transform.scale(
            next_img,
            (
                int(next_img.get_width() / RATIO_720p),
                int(next_img.get_height() / RATIO_720p)
            )
        )
        from button import Button
        self.next_button = Button(1097, 624, next_img, 1 / RATIO_720p)

        # Large font for stars and flavor
        font_path = os.path.join(BASE_PATH, "assets", "font", "nura-jeni-thin.ttf")
        self.font = pygame.font.Font(font_path, 50)
        self.small_font = pygame.font.Font(font_path, 30)
        self.music_loaded = False

    def enter(self):
        # Reset music flag
        self.music_loaded = False

    def run(self):
        # Retrieve cakes
        player_cake = self.gsm.get_cake()
        random_cake = self.gsm.get_randomcake()

        # Score calculation
        scoreboard = RandomGameScoreboard(player_cake.get_parts(), random_cake.get_parts(), self.gsm)
        total_score = scoreboard.calculate_score()
        star = scoreboard.score_5star()

        # Play sound once
        if not self.music_loaded:
            pygame.mixer.music.stop()  # หยุดเสียงก่อน
            sound_file = "ShowScorePage[Win].mp3" if star > 2 else "ShowScorePage[Lose].mp3"
            pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", sound_file))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            self.music_loaded = True

        # Background depending on win/lose
        bg = self.bg_win if star > 2 else self.bg_lose
        self.display.blit(bg, (0, 0))

        # Draw scoreboard
        self.display.blit(self.board, self.board_pos)
        scoreboard.render(self.display)

        # Draw star count
        star_text = self.font.render(str(star), True, (0, 0, 0))
        self.display.blit(star_text, (428, 50))

        # Draw player vs random cake
        player_deco = CakeDecorator(player_cake, self.display)
        random_deco = CakeDecorator(random_cake, self.display)
        player_deco.decorate(617, 369, (310, 310))
        random_deco.decorate(357, 357, (170, 170))

        # Next button
        self.next_button.draw(self.display)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_button.is_mouse_over():
                self.gsm.set_state('end')
