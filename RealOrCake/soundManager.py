# soundManager.py
import pygame, os
from decoModule import get_base_path

class SoundManager:
    def __init__(self):
        # โหลดเสียงทั้งหมดที่ต้องการใช้
        base_path = get_base_path()
        self.sounds = {
            "apply_frosting": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "ApplyFrosting.mp3")),
            "end_page": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "EndPage.mp3")),
            "in_game": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "InGamePage.mp3")),
            "intro": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "IntroPage.mp3")),
            "normal_click": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "NormalClick.mp3")),
            "random_page": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "RandomPage.mp3")),
            "reset_cake": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "ResetCake.mp3")),
            "score_lose": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "ShowScorePage[Lose].mp3")),
            "score_win": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "ShowScorePage[Win].mp3")),
            "start_click": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "StartClick.mp3")),
            "cake_mixer": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "CakeMixer.mp3")),
            "crack_egg": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "CrackEgg.mp3")),
            "cream_cake": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "CreamCake.mp3")),
            "cut_cake": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "CutCake.mp3")),
            "dried_food": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "DriedFood.mp3")),
            "liquid": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "Liquid.mp3")),
            "photo_page_background": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "PhotoPageBackground.mp3")),
            "select_mode_page_background": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "SelectModePageBackground.mp3")),
            "serve": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "Serve .mp3")),
            "yam": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "Yam.mp3")),
            "bakingPage_backgound": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "baking_background.mp3")),
        }

    def play(self, key):
        """เล่นเสียงเอฟเฟกต์ตาม key ที่กำหนด"""
        if key in self.sounds:
            self.sounds[key].play()

    def stop(self, key):
        """หยุดเสียงที่กำหนด"""
        if key in self.sounds:
            self.sounds[key].stop()
