from decoModule import get_base_path
import pygame, os

# เก็บ State การเปลี่ยนหน้าครีมและท็อปปิง โดย State เหล่านี้จะอยู่ใน Decoration State อีกที

shelf_positions = [
    (749, 135), (892, 135), (1038, 135),
    (749, 285), (892, 285), (1038, 285),
    (749, 435), (892, 435), (1038, 435)
]

state_options = {
    "base":        ["layered", "plain"],
    "behindcream": ["feather", "wave"],
    "lowercream":  ["feather", "wave"],
    "middlecream": ["ribbon",  "ruffle"],
    "topcream":    ["feather", "wave"],
    "topping":     ["bow", "crown", "floweredge", "flowertop", "pearl", "strawberry_3", "strawberry_4"]
}

RATIO_720p = 1.5

class State:
    # Super class ของ Elements State

    def __init__(self):
        self.name = "none"

    def enter(self):
        pass

    def update(self):
        pass

    def draw(self, screen):  
        # ใส่ใน run, ไว้แสดงรูปแต่ละ element state

        self.display = screen
        types_for_this_state = state_options[self.name]
        base_path =  get_base_path()
        for i, type in enumerate(types_for_this_state):
            if i < len(shelf_positions):
                thumb_img = pygame.image.load(os.path.join(base_path, "assets", "decoration_elements", "thumbnail", f"{self.name}_{type}.png"))
                thumb_img = pygame.transform.smoothscale(thumb_img, (167, 167)).convert_alpha()
                if thumb_img:
                    self.display.blit(thumb_img, shelf_positions[i])

class BaseState(State):
    # Subclass, สำหรับ Base Cake state

    def __init__(self):
        self.name = "base"

    def draw(self, screen):
        # เรียก function ตาม superclass

        return super().draw(screen)

class BCreamState(State):
    # Subclass, สำหรับ Behind cream state

    def __init__(self):
        self.name = "behindcream"

    def draw(self, screen):
        # เรียก function ตาม superclass

        return super().draw(screen)

class LCreamState(State):
    # Subclass, สำหรับ Lower cream state

    def __init__(self):
        self.name = "lowercream"

    def draw(self, screen):
        return super().draw(screen)

class MCreamState(State):
    # Subclass, สำหรับ Middle cream state

    def __init__(self):
        self.name = "middlecream"

    def draw(self, screen):
        return super().draw(screen)

class TCreamState(State):
    # Subclass, สำหรับ Top cream state

    def __init__(self):
        self.name = "topcream"        

    def draw(self, screen):
        return super().draw(screen)

class ToppingState(State):
    # Subclass, สำหรับ Topping state

    def __init__(self):
        self.name = "topping"    

    def draw(self, screen):
        return super().draw(screen)
