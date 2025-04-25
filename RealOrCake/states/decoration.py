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
        self.display          = display
        self.gameStateManager = gameStateManager
        self.screen_w         = screen_w
        self.screen_h         = screen_h
        self.sound_manager    = sound_manager

        # ขนาดสเกลที่จะใช้กับทุกการตกแต่ง
        self.dec_scale = (511, 511)

        # --- โหลด assets ---
        self.background = load_image(
            "background", "shop_background.png",
            (self.screen_w, self.screen_h)
        )
        self.shelve = load_image("other", "shelve.png")
        self.shelve = pygame.transform.smoothscale(
            self.shelve,
            (change(self.shelve.get_width()), change(self.shelve.get_height()))
        )
        self.shelve_pos = (725, 112)

        self.reset_button  = Button(
            929, 638,
            load_image("button","reset_button.png"),
            1/RATIO_720p
        )
        self.finish_button = Button(
            1096, 638,
            load_image("button","finish_button.png"),
            1/RATIO_720p
        )
        self.back_button   = Button(
            21, 15,
            load_image("button","back_button1.png"),
            1/RATIO_720p
        )

        # sub-state tabs
        def make_bt(fname, x):
            img = pygame.image.load(os.path.join(
                BASE_PATH, "assets", "decoration_elements",
                "deco_button", fname
            )).convert_alpha()
            return Button(x, 24, img, 1/RATIO_720p, smooth=False)

        self.base_button        = make_bt("base_button.png", 720)
        self.behindcream_button = make_bt("behindcream_button.png", 805)
        self.lowercream_button  = make_bt("lowercream_button.png", 890)
        self.middlecream_button = make_bt("middlecream_button.png", 975)
        self.topcream_button    = make_bt("topcream_button.png", 1060)
        self.topping_button     = make_bt("topping_button.png", 1145)

        # core objects
        self.element_manager = ElementStateManager()
        self.cake            = Cake()
        self.decorator       = CakeDecorator(self.cake, self.display)
        self.color_palette   = ColorPalette(self.element_manager, self.cake)

        # alerts
        self.font           = pygame.font.Font(None, 20)
        self.alert          = Alert(
            "Finish the decoration?",
            self.font,
            self.screen_w//2 - 200,
            self.screen_h//2 - 100,
            400, 200
        )
        self.alert_active   = False
        self.alert_b        = Alert(
            "Go back to Home page?",
            self.font,
            self.screen_w//2 - 200,
            self.screen_h//2 - 100,
            400, 200
        )
        self.alert_b_active = False

        self.selected_color_global = "milk"

    def run(self):
        # วาด scene
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.shelve, self.shelve_pos)
        self.back_button.draw(self.display)
        self.reset_button.draw(self.display)
        self.finish_button.draw(self.display)
        for btn in (
            self.base_button, self.behindcream_button,
            self.lowercream_button, self.middlecream_button,
            self.topcream_button, self.topping_button
        ):
            btn.draw(self.display)

        self.element_manager.draw(self.display)
        self.color_palette.draw(self.display)

        # ใช้ cache จาก CakeDecorator พร้อมสเกลที่กำหนดไว้
        self.decorator.decorate(62, 209, self.dec_scale)

    def handle_events(self, event):
        # รับแค่ MOUSEBUTTONDOWN เพื่อให้ตอบสนองเร็ว
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        # 1) Reset cake
        if self.reset_button.handle_event(event):
            self.cake.reset()
            self.decorator.cache.clear()
            self.gameStateManager.set_cake(self.cake)
            if self.sound_manager:
                self.sound_manager.play("reset_cake")
            return

        # 2) Finish → end/score
        if self.finish_button.handle_event(event):
            if self.sound_manager:
                self.sound_manager.play("start_click")
                self.sound_manager.play("serve")
            if self.gameStateManager.get_mode() == 'normal':
                self.gameStateManager.set_state('end')
            else:
                self.gameStateManager.set_state('score_page')
            return

        # 3) Back
        if self.back_button.handle_event(event):
            if self.gameStateManager.get_mode() == 'normal':
                self.gameStateManager.set_state('option_page')
            else:
                self.cake.reset()
                self.decorator.cache.clear()
                self.gameStateManager.set_cake(self.cake)
                rnd = self.gameStateManager.get_randomcake()
                if rnd:
                    self.gameStateManager.reset_randomcake()
                self.gameStateManager.set_state('option_page')
            return

        # 4) Sub-state tabs
        tabs = [
            (self.base_button,        "base"),
            (self.behindcream_button, "behindcream"),
            (self.lowercream_button,  "lowercream"),
            (self.middlecream_button, "middlecream"),
            (self.topcream_button,    "topcream"),
            (self.topping_button,     "topping"),
        ]
        for btn, state_name in tabs:
            if btn.handle_event(event):
                self.element_manager.set_state(state_name)
                return

        # 5) เลือกสีจาก palette → add_decoration + cache
        sel = self.color_palette.get_color()
        if sel:
            self.selected_color_global = sel
            cur = self.element_manager.current_state
            if cur in self.cake.parts:
                part_type = self.cake.parts[cur][0]
                # เพิ่ม scale เข้าไปตาม signature ใหม่
                self.decorator.add_decoration(
                    cur,
                    part_type,
                    self.selected_color_global,
                    self.dec_scale
                )
                self.gameStateManager.set_cake(self.cake)
            return

        # 6) วาง decoration จาก shelf
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
            "topping":     ["bow","crown","floweredge","flowertop","pearl","strawberry_3","strawberry_4"]
        }
        cur = self.element_manager.current_state
        if cur in state_options:
            for idx, item in enumerate(state_options[cur]):
                x, y = shelf_positions[idx]
                if x <= event.pos[0] <= x + 167 and y <= event.pos[1] <= y + 167:
                    # เพิ่ม scale เข้าไปด้วย
                    self.decorator.add_decoration(
                        cur,
                        item,
                        self.selected_color_global,
                        self.dec_scale
                    )
                    self.gameStateManager.set_cake(self.cake)
                    if self.sound_manager:
                        self.sound_manager.play("apply_frosting")
                    return

    def enter(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(
            BASE_PATH, "assets", "Sound", "InGamePage.mp3"
        ))
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

        # เริ่ม sub-state ที่ base และเค้กเปล่า
        self.element_manager.set_state('base')
        self.cake.reset()
        self.decorator.cache.clear()
        self.gameStateManager.set_cake(self.cake)
