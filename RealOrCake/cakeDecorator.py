import pygame
from decoModule import load_cake_part

# ตัวเพิ่มครีมกับท็อปปิ้งบน object Cake()

class CakeDecorator:
    def __init__(self, cake, display):
        self.cake = cake
        self.display = display
        self.decorations = {}  # Stores decoration images to display

    def add_decoration(self, part, type, color):
        # Apply a decoration to the cake and load the corresponding image.
        # เพิ่ม layer แต่ละครั้งที่ผู้เล่นกดครีมหรือท็อปปิ้งอะไร

        if part in self.cake.parts:
            # If the part already exists, update its color
            self.cake.parts[part] = (type, color)
            img = load_cake_part(part, type, color)
            if img:
                self.decorations[part] = img
            else:
                pass
                #print(f"Failed to load decoration: {part} {type} in {color}")
        else:
            # If the part doesn't exist, add it
            self.cake.add_part(part, type, color)
            img = load_cake_part(part, type, color)

            if img:
                self.decorations[part] = img
            else:
                pass
                #print(f"Failed to load decoration: {part} {type} in {color}")

    def decorate(self, x, y, scale):
        # เพิ่มใน run เพื่อโชว์ภาพแต่ละเลเยอร์

        for part, (part_type, part_color) in self.cake.parts.items():
            img = load_cake_part(part, part_type, part_color)
            if img:
                img = pygame.transform.smoothscale(img, scale)
                self.display.blit(img, (x, y))
            else:
                pass
                #print(f"Failed to load image for {part} ({part_type}, {part_color})")

