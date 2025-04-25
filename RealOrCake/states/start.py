import pygame, os, sys
import button
from decoModule import load_image, get_base_path
from screen import change_ratio_1080_to_720 as change
from alert import Alert

# ค่าคงที่
RATIO_720p = 1.5
BASE_PATH   = get_base_path()

class Start:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display       = display
        self.gsm           = gameStateManager
        self.sw, self.sh   = screen_w, screen_h
        self.sound_manager = sound_manager

        # โหลดพื้นหลัง + โลโก้
        self.background = load_image("background", "homepage_bg.png", (self.sw, self.sh))
        logo = load_image("other", "logo.png")
        lw, lh = logo.get_size()
        self.logo = pygame.transform.smoothscale(logo, (lw / RATIO_720p, lh / RATIO_720p))

        # ปุ่มต่างๆ
        self.play_button    = button.Button(165, 316, load_image("button","play_button.png"),    1/RATIO_720p)
        self.gallery_button = button.Button(165, 430, load_image("button","gallery_button.png"), 1/RATIO_720p)
        self.exit_button    = button.Button(165, 541, load_image("button","exit_button.png"),   1/RATIO_720p)

        # Alert ออกจากเกม
        self.font         = pygame.font.Font(None, 20)
        self.alert        = Alert("Exit the game?", self.font,
                                  self.sw//2 - 200, self.sh//2 - 100, 400, 200)
        self.alert_active = False

    def enter(self):
        # เริ่มเล่นเพลง Intro ตั้งแต่เข้าหน้า Start
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", "IntroPage.mp3"))
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

        # รีเซ็ตเค้กและ Alert ทุกครั้งที่เข้ามา
        if self.gsm.get_cake():
            self.gsm.reset()
        if self.gsm.get_randomcake():
            self.gsm.reset_randomcake()
        self.alert.result = None
        self.alert_active = False

    def run(self):
        # วาดพื้นหลัง / โลโก้ / ปุ่ม
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.logo,       (22, 35))
        self.play_button.draw(self.display)
        self.gallery_button.draw(self.display)
        self.exit_button.draw(self.display)

        # ถ้า Alert เปิดอยู่ ก็วาดทับไว้
        if self.alert_active:
            self.alert.draw(self.display)

    def handle_events(self, event):
        # 1) ถ้าเป็นคลิกเมาส์ซ้าย
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # ปุ่ม Play
            if self.play_button.handle_event(event):
                self.sound_manager.play("start_click")
                self.gsm.set_state('option_page')
                return

            # ปุ่ม Gallery
            if self.gallery_button.handle_event(event):
                self.sound_manager.play("start_click")
                self.gsm.set_state('gallery_page')
                return

            # ปุ่ม Exit
            if self.exit_button.handle_event(event):
                self.alert_active = True
                return

        # 2) ถ้า Alert กำลังเปิด ให้จัดการก่อน
        if self.alert_active:
            mouse_pos = pygame.mouse.get_pos()
            if self.alert.handle_event(event, mouse_pos):
                self.alert_active = False
                # ถ้าผลลัพธ์ Alert เป็น True => exit
                if self.alert.result:
                    pygame.quit()
                    sys.exit()
                else:
                    self.alert.result = None
