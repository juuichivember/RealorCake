from decoModule import load_image, get_base_path
import pygame, os
from screen import change_ratio_1080_to_720 as change
import button

RATIO_720p = 1.5

# แถบสี

class ColorPalette():
    def __init__(self):
        self.base_path = get_base_path()
        self.palette_bg = pygame.image.load(os.path.join(self.base_path, "assets", "decoration_elements", "Color", "painttray.png"))
        self.palette_bg = pygame.transform.smoothscale(self.palette_bg, (change(self.palette_bg.get_width()), change(self.palette_bg.get_height()))).convert_alpha()
        self.palette_pos = (613, 114) 

        self.color_names = [
            "mint", "carrot", "charcole", "grape", "bluberry", "coffee",
            "vanilla", "milk", "strawberry", "chocolate", "redvelvet", "none"
        ]

        self.color_positions = []
        for i, _ in enumerate(self.color_names):
            col = i % 2
            row = i // 2
            # เริ่มต้น x ใช้ palette_pos[0] ที่ปรับแล้ว
            x_pos = self.palette_pos[0] + 12 + (col * 50)
            y_pos = self.palette_pos[1] + 12 + (row * 48)
            self.color_positions.append((x_pos, y_pos))

        self.color_icons = {}
        for i, color in enumerate(self.color_names):
            img = pygame.image.load(os.path.join(self.base_path, "assets", "decoration_elements", "Color", f"{color}.png"))
            img = pygame.transform.scale(img, (44, 42)).convert_alpha()
            color_button = button.Button(self.color_positions[i][0], self.color_positions[i][1], img, 1)
            if color_button: 
                self.color_icons[color] = color_button

    def draw(self, screen):
        # ใส่ใน run, แสดงรูปถาดและสี
        self.display = screen

        self.display.blit(self.palette_bg, self.palette_pos)
        for color in self.color_names:
            self.color_icons[color].draw(self.display)

    def get_color(self):
        #  ใส่ใน run
        for color in self.color_names:
            if self.color_icons[color].is_mouse_over():
                return color
        if self.color_icons["none"].is_mouse_over():
            return None