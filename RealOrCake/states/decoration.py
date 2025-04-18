# states/decoration.py
import pygame, os
from decoModule import load_image, get_base_path
from screen import change_ratio_1080_to_720 as change
from elementStateManager import ElementStateManager
from colorPalette import ColorPalette
from cake import Cake
from cakeDecorator import CakeDecorator
from button import Button
from alert import Alert
pygame.mixer.init()

RATIO_720p = 1.5
BASE_PATH = get_base_path()

class Decoration:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.sound_manager = sound_manager

        self.background = load_image("background", "shop_background.png", (self.screen_w, self.screen_h))
        self.shelve = load_image("other", "shelve.png")
        self.shelve = pygame.transform.smoothscale(self.shelve, (change(self.shelve.get_width()), change(self.shelve.get_height())))
        self.shelve_pos = (725, 112)

        reset_button_img = load_image("button", "reset_button.png")
        self.reset_button = Button(929, 638, reset_button_img, 1 / RATIO_720p)
        finish_button_img = load_image("button", "finish_button.png")
        self.finish_button = Button(1096, 638, finish_button_img, 1 / RATIO_720p)
        back_button_img = load_image("button", "back_button1.png")
        self.back_button = Button(21, 15, back_button_img, 1 / RATIO_720p)

        self.base_button = pygame.image.load(os.path.join(BASE_PATH, "assets", "decoration_elements", "deco_button", "base_button.png")).convert_alpha()
        self.base_button = Button(720, 24, self.base_button, 1 / RATIO_720p, smooth=False)
        self.behindcream_button = pygame.image.load(os.path.join(BASE_PATH, "assets", "decoration_elements", "deco_button", "behindcream_button.png")).convert_alpha()
        self.behindcream_button = Button(805, 24, self.behindcream_button, 1 / RATIO_720p, smooth=False)
        self.lowercream_button = pygame.image.load(os.path.join(BASE_PATH, "assets", "decoration_elements", "deco_button", "lowercream_button.png")).convert_alpha()
        self.lowercream_button = Button(890, 24, self.lowercream_button, 1 / RATIO_720p, smooth=False)
        self.middlecream_button = pygame.image.load(os.path.join(BASE_PATH, "assets", "decoration_elements", "deco_button", "middlecream_button.png")).convert_alpha()
        self.middlecream_button = Button(975, 24, self.middlecream_button, 1 / RATIO_720p, smooth=False)
        self.topcream_button = pygame.image.load(os.path.join(BASE_PATH, "assets", "decoration_elements", "deco_button", "topcream_button.png")).convert_alpha()
        self.topcream_button = Button(1060, 24, self.topcream_button, 1 / RATIO_720p, smooth=False)
        self.topping_button = pygame.image.load(os.path.join(BASE_PATH, "assets", "decoration_elements", "deco_button", "topping_button.png")).convert_alpha()
        self.topping_button = Button(1145, 24, self.topping_button, 1 / RATIO_720p, smooth=False)

        self.element_manager = ElementStateManager()
        self.cake = Cake()
        self.decorator = CakeDecorator(self.cake, self.display)
        self.color_palette = ColorPalette(self.element_manager, self.cake)

        self.font = pygame.font.Font(None, 20)
        self.alert = Alert("Finish the decoration?", self.font, self.screen_w // 2 - 200, self.screen_h // 2 - 100, 400, 200)
        self.alert_active = False
        self.alert_b = Alert("Go back to Home page?", self.font, self.screen_w // 2 - 200, self.screen_h // 2 - 100, 400, 200)
        self.alert_b_active = False

        self.selected_color_global = "milk"

    def run(self):
        self.draw_scene()

    def draw_scene(self):
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.shelve, self.shelve_pos)
        self.back_button.draw(self.display)
        self.reset_button.draw(self.display)
        self.finish_button.draw(self.display)
        self.base_button.draw(self.display)
        self.behindcream_button.draw(self.display)
        self.lowercream_button.draw(self.display)
        self.middlecream_button.draw(self.display)
        self.topcream_button.draw(self.display)
        self.topping_button.draw(self.display)
        self.element_manager.draw(self.display)
        self.color_palette.draw(self.display)
        self.decorator.decorate(62, 209, (511, 511))

    def handle_events(self, event):
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
        self.gameStateManager.set_cake(self.cake)

        if self.reset_button.is_mouse_over():
            self.cake.reset()  # Reset cake design
            if self.sound_manager:
                self.sound_manager.play("reset_cake")
        elif self.finish_button.is_mouse_over():
            self.sound.play("serve")
            if self.gameStateManager.get_mode() == 'normal':
                self.gameStateManager.set_state('end')
            else:
                self.gameStateManager.set_state('score_page')
        elif self.back_button.is_mouse_over():
            # หากโหมดเป็น normal ให้กลับไปที่ optionPage โดยไม่รีเซ็ตเค้กเพิ่มเติม
            if self.gameStateManager.get_mode() == 'normal':
                self.gameStateManager.set_state('option_page')
            else:
                # ในโหมด random ก็ให้รีเซ็ตและกลับไปที่ optionPageตามเดิม
                self.cake.reset()
                self.random_cake = self.gameStateManager.get_randomcake()
                self.gameStateManager.reset_randomcake()
                self.gameStateManager.set_state('option_page')
        # ... ส่วนที่เกี่ยวกับการเปลี่ยน sub-state และตรวจจับการเลือกองค์ประกอบ
        for button_item, state_name in [
            (self.base_button, "base"),
            (self.behindcream_button, "behindcream"),
            (self.lowercream_button, "lowercream"),
            (self.middlecream_button, "middlecream"),
            (self.topcream_button, "topcream"),
            (self.topping_button, "topping"),
        ]:
            if button_item.is_mouse_over():
                self.element_manager.set_state(state_name)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            
            # เช็คการเลือกสี
            selected_color = self.color_palette.get_color()
            if selected_color:
                self.selected_color_global = selected_color
                if self.element_manager.current_state in self.cake.parts:
                    part_type = self.cake.parts[self.element_manager.current_state][0]
                    self.decorator.add_decoration(self.element_manager.current_state, part_type, self.selected_color_global)
                    selected_color = self.color_palette.get_color()
            
            # เช็คการเลือกองค์ประกอบจากชั้นวาง
            current_state_name = self.element_manager.current_state
            if current_state_name in state_options:
                shelf_items = state_options[current_state_name]
                for i, item_type in enumerate(shelf_items):
                    x, y = shelf_positions[i]
                    if x <= mouse_x <= x + 167 and y <= mouse_y <= y + 167:
                        print(f"Placing {item_type} in {current_state_name} with color {self.selected_color_global}")
                        self.decorator.add_decoration(current_state_name, item_type, self.selected_color_global)
                        if self.sound_manager:
                            self.sound_manager.play("apply_frosting")


    def enter(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", "InGamePage.mp3"))
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)
        self.element_manager.set_state('base')