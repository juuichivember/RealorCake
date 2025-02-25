import os
import pygame

def load_cake_image(cake_type):
    path = f"Elements/layer7_base_1/{cake_type}.png"
    if os.path.exists(path):
        return pygame.image.load(path)
    return None