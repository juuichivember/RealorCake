import pygame 
import os
import datetime
from button import Button
from decoModule import get_base_path

BASE_PATH = get_base_path()

class SaveImgButton(Button):
    def save_cake_img(self, content_surface):
        # ตั้งค่าโฟลเดอร์เก็บภาพเป็น Downloads/RealorCakeGallery
        downloads_path = self.get_downloads_path()
        os.makedirs(downloads_path, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี

        # สร้างชื่อไฟล์ด้วยวันที่และเวลาปัจจุบัน
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cake_{timestamp}.png"
        save_path = os.path.join(downloads_path, filename)

        # เซฟ content_surface ทั้งหมดโดยตรง
        pygame.image.save(content_surface, save_path)
        print(f"Screenshot saved to {save_path}")

    def get_downloads_path(self):
        """คืนค่า path ของโฟลเดอร์ Downloads/RealorCakeGallery ของผู้ใช้"""
        return os.path.join(os.path.expanduser("~"), "Downloads", "RealorCakeGallery")
