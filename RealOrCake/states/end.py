# states/end.py
import pygame, os
from decoModule import load_image, get_base_path
from saveImgButton import SaveImgButton
from button import Button
from alert import Alert

RATIO_720p = 1.5
BASE_PATH   = get_base_path()

class End:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display        = display
        self.gsm            = gameStateManager
        self.sw, self.sh    = screen_w, screen_h
        self.sound          = sound_manager

        # Surface สำหรับ background + cake (ที่จะเซฟ)
        self.content_surface = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)

        # Background
        self.background = load_image("background", "endpage_bg.png", (self.sw, self.sh))

        # สร้างปุ่ม UI ทุกปุ่ม
        self.back_button     = Button(10,   618, load_image("button","back_button2.png"), 1/RATIO_720p)
        self.create_wish_btn = Button(922,  612, load_image("button","wish_button.png"),    1/RATIO_720p)
        self.save_button     = SaveImgButton(1095,638, load_image("button","save_button.png"),1/RATIO_720p)
        self.home_button     = Button(1091, 0,   load_image("button","home_button.png"),   1/RATIO_720p)

        # Alert
        self.font         = pygame.font.Font(None, 20)
        self.alert        = Alert("Save the cake image?", self.font,
                                  self.sw//2 - 200, self.sh//2 - 100, 400, 200)
        self.alert_active = False

    def enter(self):
        # เล่นเพลงหน้า End
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(BASE_PATH,"assets","Sound","EndPage.mp3"))
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

        # รีเซ็ต Alert
        self.alert.result = None
        self.alert_active = False

    def run(self):
        # 1) เตรียม content_surface (background + cake)
        self.content_surface.fill((0,0,0,0))
        self.content_surface.blit(self.background, (0,0))

        from cakeDecorator import CakeDecorator
        cake      = self.gsm.get_cake()
        decorator = CakeDecorator(cake, self.content_surface)
        decorator.decorate(424, 186, (457, 457))

        # 2) แสดง content_surface
        self.display.blit(self.content_surface, (0,0))

        # 3) วาดปุ่ม UI
        if self.gsm.get_mode() == 'random':
            # Back จะวาดเฉพาะใน random mode
            self.back_button.draw(self.display)

        # ปุ่มอื่นวาดเสมอ
        self.create_wish_btn.draw(self.display)
        self.save_button.draw(self.display)
        self.home_button.draw(self.display)

        # 4) วาด Alert (ถ้ามี)
        if self.alert_active:
            self.alert.draw(self.display)
        elif self.alert.result is not None:
            if self.alert.result:
                # ถ้ากด Save → เซฟภาพจาก content_surface
                self.save_button.save_cake_img(self.content_surface)
                self.alert.result = False
            else:
                self.alert.result = None

    def handle_events(self, event):
        # --- 1) ให้ Alert จัดการก่อน ---
        if self.alert_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.alert.handle_event(event, pygame.mouse.get_pos()):
                    self.alert_active = False
                    return

        # --- 2) ปุ่ม Back (เฉพาะ random mode) ---
        if self.gsm.get_mode() == 'random' and self.back_button.handle_event(event):
            self.gsm.set_state('score_page')
            return

        # --- 3) ปุ่มสร้างคำอวยพร ---
        if self.create_wish_btn.handle_event(event):
            self.gsm.set_state('end_message')
            return

        # --- 4) ปุ่ม Save (เปิด Alert) ---
        if self.save_button.handle_event(event):
            self.alert_active = True
            return

        # --- 5) ปุ่ม Home (กลับหน้า Start) ---
        if self.home_button.handle_event(event):
            self.gsm.reset()
            self.gsm.reset_randomcake()
            self.gsm.set_state('start')
            self.gsm.get_cake().reset()
            return
