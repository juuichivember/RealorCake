import os
import pygame

def load_image(path, scale=None, smooth=True):
    if os.path.exists(path):
        try:
            image = pygame.image.load(path).convert_alpha()
            if scale:
                if smooth:
                    image = pygame.transform.smoothscale(image, scale)
                image = pygame.transform.scale(image, scale)
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
    else:
        print(f"File not found: {path}")
    return pygame.Surface((1, 1), pygame.SRCALPHA)

def load_cake_part(state_name, cake_type, color):
    if not cake_type:
        return None
    if not color:
        color = "grape"
    path = f"Elements/decoration_elements/{state_name}_{cake_type}/{state_name}_{cake_type}_{color}.png"
    if os.path.exists(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"Error loading cake part {path}: {e}")
    else:
        pass
        #print(f"File not found: {path}")
    return None