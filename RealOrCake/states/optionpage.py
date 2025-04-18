# states/optionpage.py
import pygame, os
import button
from decoModule import load_image, get_base_path

RATIO_720p = 1.5
BASE_PATH = get_base_path()

class OptionPage:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.sound_manager = sound_manager

        self.background = load_image("background", "option_background.png", (self.screen_w, self.screen_h))
        random_button_img = load_image("button", "random-mode_button.png")
        self.random_button = button.Button(43, 60, random_button_img, 1 / RATIO_720p)
        normal_button_img = load_image("button", "normal-mode_button.png")
        self.normal_button = button.Button(667, 32, normal_button_img, 1 / RATIO_720p)
        self.back_button = load_image("button", "back_button2.png")
        self.back_button = button.Button(10, 618, self.back_button, 1 / RATIO_720p)

    def enter(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", "SelectModePageBackground.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def run(self):
        self.display.blit(self.background, (0, 0))
        self.random_button.draw(self.display)
        self.normal_button.draw(self.display)
        self.back_button.draw(self.display)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # ตรวจสอบว่าปุ่ม Random ถูกคลิกจริงหรือไม่
            if self.random_button.is_mouse_over():
                if self.sound_manager:
                    self.sound_manager.play("start_click")
                self.gameStateManager.set_mode('random')
                self.gameStateManager.set_state('random_cake')
            elif self.normal_button.is_mouse_over():
                if self.sound_manager:
                    self.sound_manager.play("start_click")
                self.gameStateManager.set_mode('normal')
                self.gameStateManager.set_state('baking')
            elif self.back_button.is_mouse_over():
                self.gameStateManager.set_state('start')

