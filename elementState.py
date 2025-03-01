from decoModule import load_image

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
    def __init__(self):
        self.name = "none"

    def enter(self):
        pass

    def update(self):
        pass

    def draw(self, screen):  
        self.display = screen
        types_for_this_state = state_options[self.name]
        for i, type in enumerate(types_for_this_state):
            if i < len(shelf_positions):
                thumb_path = f"Elements/decoration_elements/thumbnail/{self.name}_{type}.png"
                thumb_img = load_image(thumb_path, (167, 167))
                if thumb_img:
                    self.display.blit(thumb_img, shelf_positions[i])

class BaseState(State):
    def __init__(self):
        self.name = "base"

    def draw(self, screen):
        return super().draw(screen)

class BCreamState(State):
    def __init__(self):
        self.name = "behindcream"

    def draw(self, screen):
        return super().draw(screen)

class LCreamState(State):
    def __init__(self):
        self.name = "lowercream"

    def draw(self, screen):
        return super().draw(screen)

class MCreamState(State):
    def __init__(self):
        self.name = "middlecream"

    def draw(self, screen):
        return super().draw(screen)

class TCreamState(State):
    def __init__(self):
        self.name = "topcream"        

    def draw(self, screen):
        return super().draw(screen)

class ToppingState(State):
    def __init__(self):
        self.name = "topping"    

    def draw(self, screen):
        return super().draw(screen)
