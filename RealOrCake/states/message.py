# states/message.py
import pygame, os
from decoModule import load_image, get_base_path
from letterTextBox import LetterTextBox
from saveImgButton import SaveImgButton
from button import Button
from alert import Alert

RATIO_720p = 1.5
BASE_PATH   = get_base_path()

class Message:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display       = display
        self.gsm           = gameStateManager
        self.sw, self.sh   = screen_w, screen_h
        self.sound_manager = sound_manager

        # Surface สำหรับ background + cake + textbox (ที่จะเซฟ)
        self.content_surface = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)

        # Background
        self.background = load_image("background", "end_message_bg.png", (self.sw, self.sh))

        # UI buttons (ไม่รวมในภาพที่จะเซฟ)
        self.back_button   = Button(10,   618, load_image("button","back_button2.png"), 1/RATIO_720p)
        self.remove_button = Button(922,  612, load_image("button","remove_button.png"), 1/RATIO_720p)
        self.save_button   = SaveImgButton(1095,638, load_image("button","save_button.png"), 1/RATIO_720p)
        self.home_button   = Button(1091,   0, load_image("button","home_button.png"), 1/RATIO_720p)

        # Text box (รวมในภาพที่จะเซฟ)
        self.text_box = LetterTextBox(706, 181, 300, 270)

        # Alert สำหรับ Save
        self.font  = pygame.font.Font(None, 20)
        self.alert = Alert(
            "Save the cake image?",
            self.font,
            self.sw//2 - 200,
            self.sh//2 - 100,
            400, 200
        )
        self.alert_active = False

    def enter(self):
        # รีเซ็ต Alert state
        self.alert.result     = None
        self.alert_active     = False
        self.gsm.set_alert_active(False)

    def run(self):
        # 1) วาดลง content_surface: background → cake → text box
        self.content_surface.fill((0,0,0,0))
        self.content_surface.blit(self.background, (0,0))

        from cakeDecorator import CakeDecorator
        cake      = self.gsm.get_cake()
        decorator = CakeDecorator(cake, self.content_surface)
        decorator.decorate(371, 181, (457, 457))

        # วาด text box ลง content_surface
        self.text_box.draw(self.content_surface)

        # 2) Blit content_surface ขึ้น display
        self.display.blit(self.content_surface, (0,0))

        # 3) วาด UI buttons บน display
        # ปุ่ม back วาดเฉพาะ random mode เท่านั้น
        if self.gsm.get_mode() == 'random':
            self.back_button.draw(self.display)

        self.remove_button.draw(self.display)
        self.save_button.draw(self.display)
        self.home_button.draw(self.display)

        # 4) อัปเดต text_box (cursor blink, delete repeat ฯลฯ)
        self.gsm.set_event(self.text_box)
        self.text_box.update()

        # 5) วาด Alert (ถ้ามี)
        if self.alert_active:
            self.alert.draw(self.display)
        elif self.alert.result is not None:
            if self.alert.result:
                # เมื่อกด OK ให้ save ภาพจาก content_surface
                self.save_button.save_cake_img(self.content_surface)
                self.alert.result = False
            else:
                # กด Cancel
                self.alert.result = None

    def handle_events(self, event):
        # 1) ให้ text_box รับ event เสมอ (สำหรับพิมพ์ข้อความ)
        self.text_box.handle_event(event)

        # 2) หากกำลังแสดง Alert ให้จัดการก่อน
        if self.alert_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.alert.handle_event(event, pygame.mouse.get_pos()):
                    self.alert_active = False
            return  # รอปิด alert ก่อน จึงตรวจปุ่มอื่น

        # 3) ปุ่ม Back → random mode only
        if self.gsm.get_mode() == 'random':
            if self.back_button.handle_event(event):
                self.gsm.set_state('score_page')
                return

        # 4) ปุ่ม Remove → กลับไปหน้า End
        if self.remove_button.handle_event(event):
            self.gsm.set_state('end')
            return

        # 5) ปุ่ม Save → เปิด alert
        if self.save_button.handle_event(event):
            self.alert_active = True
            return

        # 6) ปุ่ม Home → รีเซ็ตข้อความใน textbox แล้วกลับหน้าเริ่ม
        if self.home_button.handle_event(event):
            # สร้าง text_box ใหม่ เพื่อเคลียร์ข้อความกลับไปค่าเริ่มต้น ("To:")
            self.text_box = LetterTextBox(706, 181, 300, 270)
            # รีเซ็ตสถานะเกม
            self.gsm.reset()
            self.gsm.reset_randomcake()
            self.gsm.set_state('start')
            self.gsm.get_cake().reset()
            return
