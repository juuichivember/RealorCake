# states/gallerypage.py

import pygame, os
from decoModule import load_image, get_base_path
from button import Button

RATIO_720p = 1.5
BASE_PATH = get_base_path()

class GalleryPage:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.sound_manager = sound_manager

        # โหลดพื้นหลัง
        self.background = load_image("background", "gallery_background.png", (self.screen_w, self.screen_h))

        # โหลดปุ่ม
        # ปุ่ม Back (ย้อนกลับไปหน้า start หรือหน้าอื่น ๆ)
        back_img = load_image("button", "back_button2.png")  
        self.back_button = Button(15, 625, back_img, 1 / RATIO_720p)

        # ปุ่มเลื่อนซ้าย (backward)
        backward_img = load_image("button", "backward-button.png")
        self.backward_button = Button(515, 630, backward_img, 1 / RATIO_720p)

        # ปุ่มเลื่อนขวา (forward)
        forward_img = load_image("button", "forward-button.png")
        self.forward_button = Button(650, 630, forward_img, 1 / RATIO_720p)

        # โหลดกรอบรูป
        self.blank_frame = load_image("other", "blank_frame.png")
        # ถ้าต้องการปรับขนาดให้เท่าพื้นที่รูป  (สมมติให้เป็น 400x300)
        # self.blank_frame = pygame.transform.smoothscale(self.blank_frame, (400, 300))
        self.frame_pos = (440, 200)  # ตำแหน่งที่จะวางกรอบภาพ (ปรับได้ตามดีไซน์)

        # โหลดภาพทั้งหมดในโฟลเดอร์เก็บภาพ
        self.image_files = self.load_images()
        self.current_index = 0  # แสดงภาพที่ index 0

    def enter(self):
        """ เรียกใช้เมื่อเข้าสู่หน้า GalleryPage (ถ้าต้อง refresh ข้อมูลก็ทำในนี้ได้) """
        pass

    def load_images(self):
        """
        ตัวอย่าง: โหลดไฟล์ .png ในโฟลเดอร์เฉพาะ (สมมติ Downloads/RealorCakeGallery) 
        หรือปรับตามตำแหน่งที่คุณเก็บไฟล์
        """
        folder = os.path.join(os.path.expanduser("~"), "Downloads", "RealorCakeGallery")
        if not os.path.exists(folder):
            return []
        all_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".png")]
        all_files.sort(reverse=True)  # เรียงจากใหม่ไปเก่า (หรือตามต้องการ)
        return all_files

    def run(self):
        # 1) วาดพื้นหลัง
        self.display.blit(self.background, (0,0))

        # 2) วาดปุ่ม UI
        self.back_button.draw(self.display)
        self.backward_button.draw(self.display)
        self.forward_button.draw(self.display)

        # 3) วาดกรอบ (blank_frame)
        self.display.blit(self.blank_frame, self.frame_pos)

        # 4) แสดงรูปปัจจุบัน (ถ้ามีไฟล์รูป)
        if self.image_files:
            current_image_path = self.image_files[self.current_index]
            try:
                # โหลดรูป
                image = pygame.image.load(current_image_path).convert_alpha()
                # ปรับขนาดรูปให้เล็กลงให้พอดีกรอบ (หากกรอบเป็น 400x300)
                # สมมติกรอบของเรามีขนาด 400x300
                # หรือใช้ self.blank_frame.get_width(), self.blank_frame.get_height() มาเป็นขนาดก็ได้
                image = pygame.transform.smoothscale(image, (400, 300))

                # คำนวณตำแหน่งวางภาพให้อยู่ตรงกลางกรอบ
                frame_rect = self.blank_frame.get_rect(topleft=self.frame_pos)
                image_rect = image.get_rect(center=frame_rect.center)

                # วาดรูปลงบน display
                self.display.blit(image, image_rect)
            except Exception as e:
                print(f"Error loading image {current_image_path}: {e}")

    def handle_events(self, event):
        """ จัดการ event สำหรับปุ่มเลื่อนซ้าย/ขวา และปุ่ม Back """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.is_mouse_over():
                # ย้อนกลับไปหน้า start หรือหน้าอื่น
                # ตัวอย่าง:
                self.gameStateManager.set_state('start')

            elif self.backward_button.is_mouse_over():
                # เลื่อนภาพไปทางซ้าย (ลด index)
                if self.current_index > 0:
                    self.current_index -= 1
                    if self.sound_manager:
                        self.sound_manager.play("normal_click")

            elif self.forward_button.is_mouse_over():
                # เลื่อนภาพไปทางขวา (เพิ่ม index)
                if self.current_index < len(self.image_files) - 1:
                    self.current_index += 1
                    if self.sound_manager:
                        self.sound_manager.play("normal_click")

    def get_state_name(self):
        """ ออปชันเสริม ถ้าต้องการคืนชื่อ state (ไม่บังคับ) """
        return "gallery_page"