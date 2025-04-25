# cakeDecorator.py
import pygame
from decoModule import load_cake_part

class CakeDecorator:
    def __init__(self, cake, display):
        """
        cake: ออบเจกต์ Cake() ที่เก็บ parts
        display: surface ที่จะใช้ blit รูป
        """
        self.cake = cake
        self.display = display
        # cache เก็บภาพที่สเกลแล้วตาม part เพื่อไม่ต้องสเกลซ้ำ
        self.cache = {}

    def add_decoration(self, part, type, color, scale):
        """
        - part: ชื่อ layer (เช่น "base", "topping" ฯลฯ)
        - type: subtype ของ layer (เช่น "feather", "wave")
        - color: สี (เช่น "vanilla", "milk")
        - scale: tuple (w,h) ขนาดที่ต้องการสเกลรูป
        """
        # บันทึก part ลงใน cake.parts
        self.cake.parts[part] = (type, color)
        # โหลดรูปดิบ
        img = load_cake_part(part, type, color)
        if not img:
            return
        # สเกลแล้วเก็บลง cache
        surf = pygame.transform.smoothscale(img, scale)
        self.cache[part] = surf

    def decorate(self, x, y, scale):
        """
        วาดทุก layer ตามลำดับเสมอ (รวม base ถ้ายังไม่ cache)
        - x,y: พิกัดมุมซ้ายบนในการ blit
        - scale: (w,h) ขนาดในการสเกลแต่ละภาพ
        """
        draw_order = ["base", "topcream", "lowercream",
                      "middlecream", "behindcream", "topping"]
        for part in draw_order:
            # ถ้า part ถูกกำหนดใน cake.parts
            if part in self.cake.parts:
                # มีใน cache หรือยัง
                surf = self.cache.get(part)
                if surf is None:
                    ptype, color = self.cake.parts[part]
                    img = load_cake_part(part, ptype, color)
                    if not img:
                        continue
                    surf = pygame.transform.smoothscale(img, scale)
                    # เก็บใน cache เพื่อรอบหน้า
                    self.cache[part] = surf
                # วาด
                self.display.blit(surf, (x, y))
