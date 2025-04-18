import pygame, os
from decoModule import load_image, get_base_path
from letterTextBox import LetterTextBox
from saveImgButton import SaveImgButton
from button import Button
from alert import Alert

RATIO_720p = 1.5
BASE_PATH = get_base_path()

class Message:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display = display
        self.gsm     = gameStateManager
        self.sw, self.sh = screen_w, screen_h
        self.sound  = sound_manager

        # Surface ลูกสำหรับวาด background + cake + text_box (ที่จะเซฟ)
        self.content_surface = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)

        # Background
        self.background = load_image("background", "end_message_bg.png", (self.sw, self.sh))

        # UI buttons (ไม่เซฟ)
        self.back_button   = Button(10,   618, load_image("button","back_button2.png"), 1/RATIO_720p)
        self.save_button   = SaveImgButton(1095,638, load_image("button","save_button.png"), 1/RATIO_720p)
        self.remove_button = Button(922,  612, load_image("button","remove_button.png"), 1/RATIO_720p)
        self.home_button   = Button(1091, 0,   load_image("button","home_button.png"), 1/RATIO_720p)

        # Text box (เซฟด้วย)
        self.text_box = LetterTextBox(706, 181, 300, 270)

        # Alert
        self.font  = pygame.font.Font(None, 20)
        self.alert = Alert(
            "Save the cake image?",
            self.font,
            self.sw//2 - 200,
            self.sh//2 - 100,
            400, 200
        )

    def enter(self):
        # รีเซ็ต Alert
        self.alert.result = None
        self.gsm.set_alert_active(False)

    def run(self):
        # 1) วาดลง content_surface: background → cake → text box
        self.content_surface.fill((0,0,0,0))
        self.content_surface.blit(self.background, (0,0))

        from cakeDecorator import CakeDecorator
        cake = self.gsm.get_cake()
        decorator = CakeDecorator(cake, self.content_surface)
        decorator.decorate(371, 181, (457, 457))

        # วาด TextBox ลงบน content_surface
        self.text_box.draw(self.content_surface)

        # 2) Blit content_surface ขึ้น display
        self.display.blit(self.content_surface, (0,0))

        # 3) วาด UI buttons บน display
        for btn in (self.back_button, self.save_button, self.remove_button, self.home_button):
            btn.draw(self.display)

        # 4) อัปเดต TextBox
        self.gsm.set_event(self.text_box)
        self.text_box.update()

        # 5) วาด Alert (แต่ไม่ดัก event ที่นี่)
        self.gsm.set_alert(self.alert)
        if self.gsm.get_alert_active():
            self.alert.draw(self.display)
        elif self.alert.result is not None:
            if self.alert.result:
                # เซฟภาพจาก content_surface ทั้งใบ
                self.save_button.save_cake_img(self.content_surface)
                self.alert.result = False
            else:
                self.alert.result = None

    def handle_events(self, event):
        # 1) ส่งให้ TextBox รับ event
        self.text_box.handle_event(event)

        # 2) ส่งให้ Alert รับ event
        if self.gsm.get_alert_active():
            if self.alert.handle_event(event, pygame.mouse.get_pos()):
                self.gsm.set_alert_active(False)

        # 3) UI button click ต่างๆ
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.is_mouse_over():
                self.gsm.set_state('score_page')
            elif self.remove_button.is_mouse_over():
                self.gsm.set_state('end')
            elif self.save_button.is_mouse_over():
                self.gsm.set_alert_active(True)
            elif self.home_button.is_mouse_over():
                self.gsm.reset()
                self.gsm.set_state('start')
