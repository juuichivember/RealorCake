# states/start.py
import pygame, os, sys
import button
from decoModule import load_image, get_base_path
from screen import change_ratio_1080_to_720 as change
from alert import Alert

# กำหนด constant ที่ใช้ร่วมกัน
RATIO_720p = 1.5  # หาร 1080p ด้วย 1.5
BASE_PATH = get_base_path()

class Start:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.sound_manager = sound_manager

        # โหลดภาพพื้นหลังหน้า Start
        self.background = load_image("background", "homepage_bg.png", (self.screen_w, self.screen_h))

        # โหลดโลโก้
        self.logo = load_image("other", "logo.png")
        logo_w, logo_h = self.logo.get_size()
        self.logo = pygame.transform.smoothscale(self.logo, (logo_w / RATIO_720p, logo_h / RATIO_720p))

        # ปุ่ม Play
        self.play_button = load_image("button", "play_button.png")
        self.play_button = button.Button(165, 316, self.play_button, 1 / RATIO_720p)

        # ปุ่ม Gallery (เพิ่มใหม่)
        self.gallery_button = load_image("button", "gallery_button.png")  
        # แก้ตำแหน่งตามดีไซน์ เช่น x=165, y=367 ถัดจาก Play
        self.gallery_button = button.Button(165, 430, self.gallery_button, 1 / RATIO_720p)

        # ปุ่ม Exit
        self.exit_button = load_image("button", "exit_button.png")
        self.exit_button = button.Button(165, 541, self.exit_button, 1 / RATIO_720p)

        # Alert สำหรับออกเกม
        self.font = pygame.font.Font(None, 20)
        self.alert = Alert("Exit the game?", self.font, self.screen_w // 2 - 200, self.screen_h // 2 - 100, 400, 200)
        self.alert_active = False

        self.click_sound_played = False
            
    def enter(self):
        # เล่นเพลง background หน้า start
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", "IntroPage.mp3"))
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

        # รีเซ็ตเค้กและ random cake เมื่อเข้าสู่หน้า Start
        self.cake = self.gameStateManager.get_cake()
        if self.cake:
            self.gameStateManager.reset()

        self.random_cake = self.gameStateManager.get_randomcake()
        if self.random_cake:
            self.gameStateManager.reset_randomcake()
        
        self.alert.result = None
        self.alert_active = False

    def run(self):
        # วาดพื้นหลัง โลโก้ และปุ่มต่าง ๆ ลงบนหน้าจอ
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.logo, (22, 35))

        self.play_button.draw(self.display)
        self.gallery_button.draw(self.display)  # ปุ่ม Gallery
        self.exit_button.draw(self.display)

        # หาก alert ถูกเปิดอยู่ ให้วาด alert
        if self.alert_active:
            self.alert.draw(self.display)

    def handle_events(self, event):
        # ตรวจจับการคลิกเมาส์ซ้าย
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # ปุ่ม Play
            if self.play_button.is_mouse_over():
                self.sound_manager.play("start_click")
                self.gameStateManager.set_state('option_page')

            # ปุ่ม Gallery (เพิ่มส่วนนี้)
            elif self.gallery_button.is_mouse_over():
                self.sound_manager.play("start_click")
                self.gameStateManager.set_state('gallery_page')

            # ปุ่ม Exit
            elif self.exit_button.is_mouse_over():
                self.alert_active = True

        # หาก alert เปิดอยู่ ให้จัดการ event ของ alert
        if self.alert_active:
            mouse_pos = pygame.mouse.get_pos()
            if self.alert.handle_event(event, mouse_pos):
                self.alert_active = False
            if self.alert.result is not None:
                if self.alert.result:
                    pygame.quit()
                    sys.exit()
                else:
                    self.alert.result = None