# states/message.py
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
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.sound_manager = sound_manager

        # Background สำหรับ Message State
        self.background = load_image("background", "end_message_bg.png", (self.screen_w, self.screen_h))
        
        # สร้าง content_surface สำหรับวาดเนื้อหาที่ต้องการเซฟ (รวม background, เค้กตกแต่ง, และ text box)
        self.content_surface = pygame.Surface((self.screen_w, self.screen_h))
        # (หาก LetterTextBox มี method เพื่อทำให้พื้นหลังโปร่งใส ให้เรียกใช้ที่นี่)
        # เช่น: self.text_box.set_background_transparent()  (ขึ้นอยู่กับการออกแบบของ LetterTextBox)

        # ปุ่ม UI ที่ไม่ต้องการให้เซฟ
        self.back_button = load_image("button", "back_button2.png")
        self.back_button = Button(10, 618, self.back_button, 1 / RATIO_720p)

        self.save_button = load_image("button", "save_button.png")
        self.save_button = SaveImgButton(1095, 638, self.save_button, 1 / RATIO_720p)
        
        self.remove_button = load_image("button", "remove_button.png")
        self.remove_button = Button(922, 612, self.remove_button, 1 / RATIO_720p)

        self.home_button = load_image("button", "home_button.png")
        self.home_button = Button(1091, 0, self.home_button, 1 / RATIO_720p)

        # สร้าง text box ซึ่งต้องการให้แสดงและรวมอยู่ใน content_surface
        self.text_box = LetterTextBox(706, 181, 300, 150)
        # ถ้า LetterTextBox มีตัวเลือกตั้งพื้นหลังให้โปร่งใส สามารถทำได้เช่น:
        # self.text_box.background_color = (0, 0, 0, 0)  หรือเรียก method ที่เกี่ยวข้อง

        self.font = pygame.font.Font(None, 20)
        self.alert = Alert("Save the cake image?", self.font, self.screen_w // 2 - 200, self.screen_h // 2 - 100, 400, 200)
        self.alert_active = False

    def run(self):
        # 1. วาดพื้นหลังลงใน content_surface
        self.content_surface.blit(self.background, (0, 0))
        
        # 2. วาดเค้กตกแต่งลงใน content_surface
        self.cake = self.gameStateManager.get_cake()
        from cakeDecorator import CakeDecorator
        self.decorator = CakeDecorator(self.cake, self.content_surface)
        self.decorator.decorate(371, 181, (457, 457))
        
        # 3. วาด text box ลงใน content_surface (โดยที่ text box ควรวาดเฉพาะข้อความ ไม่มีพื้นหลังทึบ)
        self.text_box.draw(self.content_surface)
        
        # 4. วาง content_surface ลงบน display (รูปที่ต้องเซฟจะเป็น content_surface นี้)
        self.display.blit(self.content_surface, (0, 0))
        
        # 5. วาด UI ปุ่ม (back, save, remove, home) บน display ซึ่งจะไม่ถูกรวมใน content_surface
        self.back_button.draw(self.display)
        self.save_button.draw(self.display)
        self.remove_button.draw(self.display)
        self.home_button.draw(self.display)
        
        # อัปเดต text box (รับอินพุต)
        self.gameStateManager.set_event(self.text_box)
        self.text_box.update()
        
        # แสดง Alert หาก active
        self.gameStateManager.set_alert(self.alert)
        if self.gameStateManager.get_alert_active():
            self.alert.draw(self.display)
        else:
            if self.alert.result is not None:
                if self.alert.result:
                    # เมื่อกด Save ให้เซฟ content_surface (ซึ่งรวมทุกอย่างที่ต้องการ)
                    self.save_button.save_cake_img(self.content_surface)
                    self.alert.result = False
                else:
                    self.alert.result = None

    def handle_events(self, event):
        # ควรจัดการ event ของ text_box, alert และปุ่ม UI
        # ตัวอย่าง:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.is_mouse_over():
                self.gameStateManager.set_state('score_page')
            elif self.remove_button.is_mouse_over():
                self.gameStateManager.set_state('end')
            elif self.save_button.is_mouse_over():
                self.gameStateManager.set_alert_active(True)
            elif self.home_button.is_mouse_over():
                self.gameStateManager.reset()
                self.gameStateManager.set_state('start')
        # เพิ่มการจัดการอื่น ๆ ตามที่ต้องการ (รวมถึงส่ง event ไปให้ text_box)
        self.text_box.handle_event(event)

    def enter(self):
        # หากมีการตั้งค่าเริ่มต้นสำหรับ Message state ให้ทำที่นี่
        pass
