# states/optionpage.py
import pygame, os
from decoModule import load_image, get_base_path
from button import Button  # ใช้ class Button ตัวใหม่ที่มี handle_event

RATIO_720p = 1.5
BASE_PATH   = get_base_path()

class OptionPage:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display       = display
        self.gsm           = gameStateManager
        self.sw, self.sh   = screen_w, screen_h
        self.sound_manager = sound_manager

        # พื้นหลัง
        self.background = load_image("background", "option_background.png", (self.sw, self.sh))

        # ปุ่ม Random Mode
        img = load_image("button", "random-mode_button.png")
        self.random_button = Button(43,  60, img, 1 / RATIO_720p)

        # ปุ่ม Normal Mode
        img = load_image("button", "normal-mode_button.png")
        self.normal_button = Button(667, 32, img, 1 / RATIO_720p)

        # ปุ่ม Back
        img = load_image("button", "back_button2.png")
        self.back_button   = Button(10, 618, img, 1 / RATIO_720p)

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
        # คลิกปุ่ม Random Mode
        if self.random_button.handle_event(event):
            if self.sound_manager:
                self.sound_manager.play("start_click")
            self.gsm.set_mode('random')
            from cake import Cake
            self.gsm.set_cake(Cake())
            self.gsm.set_state('random_cake')
            return

        # คลิกปุ่ม Normal Mode
        if self.normal_button.handle_event(event):
            if self.sound_manager:
                self.sound_manager.play("start_click")
            self.gsm.set_mode('normal')
            self.gsm.set_state('baking')
            return

        # คลิกปุ่ม Back
        if self.back_button.handle_event(event):
            self.gsm.set_state('start')
            return
