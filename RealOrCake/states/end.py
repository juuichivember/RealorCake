# ภายใน RealorCake\states\end.py
import pygame, os
from decoModule import load_image, get_base_path
from saveImgButton import SaveImgButton
from button import Button
from alert import Alert

RATIO_720p = 1.5
BASE_PATH = get_base_path()

class End:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.sound_manager = sound_manager

        self.background = load_image("background", "endpage_bg.png", (self.screen_w, self.screen_h))
        
        self.back_button = load_image("button", "back_button2.png")
        self.back_button = Button(10, 618, self.back_button, 1 / RATIO_720p)
        
        self.create_wish_btn = load_image("button", "wish_button.png")
        self.create_wish_btn = Button(922, 612, self.create_wish_btn, 1 / RATIO_720p)
        
        self.save_button = load_image("button", "save_button.png")
        self.save_button = SaveImgButton(1095, 638, self.save_button, 1 / RATIO_720p)
        
        self.home_button = load_image("button", "home_button.png")
        self.home_button = Button(1091, 0, self.home_button, 1 / RATIO_720p)
        
        self.font = pygame.font.Font(None, 20)
        self.alert = Alert("Save the cake image?", self.font, self.screen_w // 2 - 200, self.screen_h // 2 - 100, 400, 200)
        self.alert_active = False

        # สร้าง surface สำหรับเนื้อหาที่ต้องการเซฟ (content layer)
        self.content_surface = pygame.Surface((self.screen_w, self.screen_h))

    def run(self):
        # วาดพื้นหลังลงใน content_surface และใส่เค้กตกแต่งลงไป
        self.content_surface.blit(self.background, (0, 0))
        
        # สมมุติว่าเนื้อหาหลักของคุณคือการแสดงเค้ก (คุณอาจจะมี CakeDecorator หรือ sprite อื่น ๆ)
        # ตัวอย่าง: วาดเค้กลงบน content_surface
        from cakeDecorator import CakeDecorator
        cake = self.gameStateManager.get_cake()  # ได้เค้กจาก gameStateManager
        decorator = CakeDecorator(cake, self.content_surface)
        decorator.decorate(424, 186, (457, 457))

        # จากนั้น แสดง content_surface ลงบน display
        self.display.blit(self.content_surface, (0, 0))
        
        # วาด UI บน display (บนนอก content_surface) เช่นปุ่มต่าง ๆ:
        self.back_button.draw(self.display)
        self.create_wish_btn.draw(self.display)
        self.save_button.draw(self.display)
        self.home_button.draw(self.display)
        
        # จัดการ alert (ถ้ามี)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if self.alert_active:
                if self.alert.handle_event(event, mouse_pos):
                    self.alert_active = False
        if self.alert_active:
            self.alert.draw(self.display)
        else:
            if self.alert.result is not None:
                if self.alert.result:
                    # เรียกใช้ save_cake_img แต่ให้ใช้ content_surface
                    # ปรับค่า x,y,width,height ตามที่ต้องการ (ตัวอย่างนี้ใช้ค่าตรงที่เค้กอยู่)
                    self.save_button.save_cake_img(self.content_surface)
                    self.alert.result = False

        # ตรวจสอบปุ่ม UI
        if self.back_button.is_mouse_over():
            self.gameStateManager.set_state('score_page')
        if self.create_wish_btn.is_mouse_over():
            self.gameStateManager.set_state('end_message')
        if self.save_button.is_mouse_over():
            self.alert_active = True
        if self.home_button.is_mouse_over():
            self.gameStateManager.reset()
            self.gameStateManager.set_state('start')

    def handle_events(self, event):
        # สามารถจัดการ event ในส่วน UI ตามปกติ
        pass

    def enter(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", "EndPage.mp3"))
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)
