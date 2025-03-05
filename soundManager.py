# soundManager.py
import pygame

class SoundManager:
    def __init__(self):
        # โหลดเสียงทั้งหมดที่ต้องการใช้
        self.sounds = {
            "apply_frosting": pygame.mixer.Sound("Elements/Sound/ApplyFrosting.mp3"),
            "end_page": pygame.mixer.Sound("Elements/Sound/EndPage.mp3"),
            "in_game": pygame.mixer.Sound("Elements/Sound/InGamePage.mp3"),
            "intro": pygame.mixer.Sound("Elements/Sound/IntroPage.mp3"),
            "normal_click": pygame.mixer.Sound("Elements/Sound/NormalClick.mp3"),
            "random_page": pygame.mixer.Sound("Elements/Sound/RandomPage.mp3"),
            "reset_cake": pygame.mixer.Sound("Elements/Sound/ResetCake.mp3"),
            "score_lose": pygame.mixer.Sound("Elements/Sound/ShowScorePage[Lose].mp3"),
            "score_win": pygame.mixer.Sound("Elements/Sound/ShowScorePage[Win].mp3"),
            "start_click": pygame.mixer.Sound("Elements/Sound/StartClick.mp3")
        }

    def play(self, key):
        """เล่นเสียงเอฟเฟกต์ตาม key ที่กำหนด"""
        if key in self.sounds:
            self.sounds[key].play()
