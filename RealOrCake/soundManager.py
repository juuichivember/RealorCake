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
            "start_click": pygame.mixer.Sound(os.path.join(base_path, "assets", "Sound", "StartClick.mp3"))
        }

    def play(self, key):
        """เล่นเสียงเอฟเฟกต์ตาม key ที่กำหนด"""
        if key in self.sounds:
            self.sounds[key].play()
