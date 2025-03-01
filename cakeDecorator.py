import pygame
from decoModule import load_image, load_cake_part

class CakeDecorator:
    def __init__(self, cake, display):
        self.cake = cake
        self.display = display
        self.decorations = {}  # Stores decoration images to display

    def add_decoration(self, part, type, color):
        """Apply a decoration to the cake and load the corresponding image."""
        if part in self.cake.parts:
            # If the part already exists, update its color
            self.cake.parts[part] = (type, color)
            img = load_cake_part(part, type, color)
            if img:
                self.decorations[part] = img
            else:
                print(f"Failed to load decoration: {part} {type} in {color}")
        else:
            # If the part doesn't exist, add it
            self.cake.add_part(part, type, color)
            img = load_cake_part(part, type, color)

            if img:
                self.decorations[part] = img
            else:
                print(f"Failed to load decoration: {part} {type} in {color}")

    def decorate(self, x, y, scale):
        for part, (part_type, part_color) in self.cake.parts.items():
            img = load_cake_part(part, part_type, part_color)
            if img:
                img = pygame.transform.smoothscale(img, scale)
                self.display.blit(img, (x, y))
            else:
                print(f"Failed to load image for {part} ({part_type}, {part_color})")

