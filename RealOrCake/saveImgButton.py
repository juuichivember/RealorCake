from button import Button
from decoModule import get_base_path
import pygame, os, re

# ref: https://stackoverflow.com/questions/68804453/save-created-image-to-file-system-python-and-pygame/68805404

# ปุ่มบันทึกภาพใน End State


class SaveImgButton(Button):
    def __init_subclass__(cls):
        return super().__init_subclass__()

    def save_cake_img(self, screen, x, y, width, height):
        # เซฟรูปโดยการแคปหน้าจอเกมไปที่โฟลเดอร์ Downloads
        downloads_path = self.get_downloads_path()
        os.makedirs(downloads_path, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี

        number = self.get_last_highest_screenshot_number(downloads_path)
        if number:
            id = int(number) + 1
        else:
            id = 1
        rect_area = pygame.Rect(x, y, width, height)
        area_surf = screen.subsurface(rect_area).copy()
        save_path = os.path.join(downloads_path, f"shots{id}.png")
        pygame.image.save(area_surf, save_path)
        print(f"Screenshot saved to {save_path}")

    def get_last_highest_screenshot_number(self, directory):
        # ตรวจชื่อไฟล์ใน Directory Screenshots แล้ว return เลขสูงสุดของไฟล์ใน Directory เพื่อนำไปตั้งชื่อไฟล์
        # หากไม่มี Directory Screenshots ก็จะสร้างขึ้นมา
        try:
            filenames = os.listdir(directory)
        except FileNotFoundError:
            return None  # Return None if directory not found

        numbers = []
        pattern = re.compile(r"shots(\d+)\.png")

        for filename in filenames:
            match = pattern.match(filename)
            if match:
                numbers.append(int(match.group(1)))

        if numbers:  # Check if the list is not empty
            return max(numbers)  # Return the highest number
        else:
            return None
        
    def get_downloads_path(self):
        """ คืนค่า path ของโฟลเดอร์ Downloads ของผู้ใช้ """
        return os.path.join(os.path.expanduser("~"), "Downloads")