import pygame
import button
from decoModule import load_image, load_cake_part
from screen import change_ratio_1080_to_720 as change
from timer import Timer
from elementStateManager import ElementStateManager
from colorPalette import ColorPalette
from cake import Cake
from cakeDecorator import CakeDecorator
from letterTextBox import LetterTextBox
from saveImgButton import SaveImgButton
from alert import Alert

# กำหนดสี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RATIO_720p = 1.5 # หาร 1080p ด้วย 1.5

# Concrete State
# ทุก State class ต้องมี function อันเดียวกันทั้งหมด
# concern: ตอนนี้ state ยังไม่จำข้อมูล คือถ้าย้อนกลับจะรีเซ็ทหน้าใหม่ ต้องเพิ่มวิธีเก็บข้อมูลโดยเฉพาะในหน้า decoration
class Start:
    # Constructor
    def __init__(self, display, gameStateManager, screen_w, screen_h):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.background = pygame.image.load("Elements/background/homepage_bg.png")
        self.background = pygame.transform.smoothscale(self.background, (self.screen_w, self.screen_h))

        self.logo = pygame.image.load("Elements/other/logo.png")
        logo_w, logo_h = self.logo.get_size()
        self.logo = pygame.transform.smoothscale(self.logo, (logo_w / RATIO_720p, logo_h / RATIO_720p))

        self.play_button = pygame.image.load("Elements/button/play_button.png").convert_alpha()
        self.play_button = button.Button(165, 311, self.play_button, 1 / RATIO_720p)
        self.exit_button = pygame.image.load("Elements/button/exit_button.png").convert_alpha()
        self.exit_button = button.Button(165, 423, self.exit_button, 1 / RATIO_720p)

        self.font = pygame.font.Font(None, 20)
        self.open_message = False
        self.alert = Alert("Exit the game?", self.font, self.screen_w / 2 - 200, self.screen_h / 2 - 100, 400, 200)
        self.alert_active = False
            
    def run(self):
        # RUN
        self.display.blit(self.background, (0,0))
        self.display.blit(self.logo, (22,35))
        self.play_button.draw(self.display)
        self.exit_button.draw(self.display)

        self.cake = self.gameStateManager.get_cake()
        if self.cake:
            self.gameStateManager.reset()

        if self.play_button.is_mouse_over():
            self.gameStateManager.set_state('decoration') ########
        if self.exit_button.is_mouse_over():
            self.alert_active = True

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if self.alert_active:
                if self.alert.handle_event(event, mouse_pos):
                    self.alert_active = False # alert is done
        if self.alert_active:
            self.alert.draw(self.display)
        else:
            if self.alert.result is not None:
                if self.alert.result:
                    pygame.quit()
                    pass #print("OK was clicked. Image Saved")
                else:
                    pass #print("Cancel was clicked. Image Cancel")
            else:
                pass #print("No button clicked")

    def enter(self):
        pass

# added
class RandomCake:
    # Constructor
    def __init__(self, display, gameStateManager, screen_w, screen_h):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h

        # โหลดภาพพื้นหลัง
        self.background = pygame.image.load("Elements/background/randomCake_bg.png")
        self.background = pygame.transform.smoothscale(self.background, (self.screen_w, self.screen_h))

        self.board = pygame.image.load("Elements/other/board.png")
        self.board = pygame.transform.smoothscale(self.board, (change(self.board.get_width()), change(self.board.get_height())))  # ปรับขนาดชั้นวาง
        self.board_pos = (338, 108)
        self.timer = Timer(self.display)
        self.timer.start()

    def run(self):
        self.display.blit(self.background, (0,0))
        self.display.blit(self.board, self.board_pos)
        self.timer.render()

        current_image = self.timer.get_current_image()
        image_pos = self.timer.get_pos()
        if current_image:
            self.display.blit(current_image, image_pos)

        if self.timer.is_finished():
            print("Timer finished!")
            self.timer.reset()
            self.gameStateManager.set_state('decoration')

    def enter(self):
        self.timer.start()

class Decoration:
    # Constructor
    def __init__(self, display, gameStateManager, screen_w, screen_h):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h

        # โหลดภาพพื้นหลัง
        self.background = pygame.image.load("Elements/background/shop_background.png")
        self.background = pygame.transform.smoothscale(self.background, (self.screen_w, self.screen_h))

        # โหลดภาพชั้นวางเค้ก
        self.shelve = pygame.image.load("Elements/other/shelve.png")
        self.shelve = pygame.transform.smoothscale(self.shelve, (change(self.shelve.get_width()), change(self.shelve.get_height())))  # ปรับขนาดชั้นวาง
        self.shelve_pos = (725, 112)

        # โหลดภาพแถบสี
        self.color_palette = ColorPalette()

        # โหลดปุ่มรีเซ็ต ปุ่มเสร็จสิ้น ปุ่มกลับ
        reset_button_img = pygame.image.load("Elements/button/reset_button.png")
        self.reset_button = button.Button(929, 638, reset_button_img, 1 / RATIO_720p)

        finish_button_img = pygame.image.load("Elements/button/finish_button.png")
        self.finish_button = button.Button(1096, 638, finish_button_img, 1 / RATIO_720p)

        back_button_img = pygame.image.load("Elements/button/back_button1.png")
        self.back_button = button.Button(21, 15, back_button_img, 1 / RATIO_720p)

        # โหลดไอคอนปุ่มด้านบนสำหรับเปลี่ยน sub-state
        self.base_button = pygame.image.load("Elements/decoration_elements/deco_button/base_button.png").convert_alpha()
        self.base_button = button.Button(720, 24, self.base_button, 1 / RATIO_720p, smooth=False)

        self.behindcream_button = pygame.image.load("Elements/decoration_elements/deco_button/behindcream_button.png").convert_alpha()
        self.behindcream_button = button.Button(805, 24, self.behindcream_button, 1 / RATIO_720p, smooth=False)

        self.lowercream_button = pygame.image.load("Elements/decoration_elements/deco_button/lowercream_button.png").convert_alpha()
        self.lowercream_button = button.Button(890, 24, self.lowercream_button, 1 / RATIO_720p, smooth=False)

        self.middlecream_button = pygame.image.load("Elements/decoration_elements/deco_button/middlecream_button.png").convert_alpha()
        self.middlecream_button = button.Button(975, 24, self.middlecream_button, 1 / RATIO_720p, smooth=False)

        self.topcream_button = pygame.image.load("Elements/decoration_elements/deco_button/topcream_button.png").convert_alpha()
        self.topcream_button = button.Button(1060, 24, self.topcream_button, 1 / RATIO_720p, smooth=False)

        self.topping_button = pygame.image.load("Elements/decoration_elements/deco_button/topping_button.png").convert_alpha()
        self.topping_button = button.Button(1145, 24, self.topping_button, 1 / RATIO_720p, smooth=False)

        self.element_manager = ElementStateManager()

        self.cake = Cake()  # Create an empty cake object
        self.decorator = CakeDecorator(self.cake, self.display)

        # ตัวแปรอื่น ๆ
        self.selected_color_global = "grape"

    def run(self):
        self.handle_events()
        self.draw_scene()

    # ฟังก์ชันวาดฉากd
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


    # ฟังก์ชันจัดการเหตุการณ์
    def handle_events(self):
        self.gameStateManager.set_cake(self.cake)

        if self.reset_button.is_mouse_over():
            self.cake.reset()  # Reset cake design
            self.selected_color_global = None
            self.decorator.decorations.clear()
            print("Reset selection")

        if self.finish_button.is_mouse_over():
            self.gameStateManager.set_state('end')

        if self.back_button.is_mouse_over():
            self.cake.reset()
            self.gameStateManager.set_state('start')

        # Check for element state selection
        for button, state_name in [
            (self.base_button, "base"),
            (self.behindcream_button, "behindcream"),
            (self.lowercream_button, "lowercream"),
            (self.middlecream_button, "middlecream"),
            (self.topcream_button, "topcream"),
            (self.topping_button, "topping"),
        ]:
            if button.is_mouse_over():
                self.element_manager.set_state(state_name)

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

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]  # Left click

        selected_color = self.color_palette.get_color()
        if selected_color:
            self.selected_color_global = selected_color  # Save the current color
            if self.element_manager.current_state in self.cake.parts:
                part_type = self.cake.parts[self.element_manager.current_state][0]
                self.decorator.add_decoration(self.element_manager.current_state, part_type, self.selected_color_global)

        current_state_name = self.element_manager.current_state  # base, lowercream, etc.
        shelf_items = state_options[current_state_name]

        for i, item_type in enumerate(shelf_items):
            x, y = shelf_positions[i]
            if x <= mouse_x <= x + 167 and y <= mouse_y <= y + 167 and mouse_clicked:
                if self.selected_color_global is None:
                    self.cake.reset()
                else:
                    print(f"Placing {item_type} in {current_state_name} with color {self.selected_color_global}")
                    self.decorator.add_decoration(current_state_name, item_type, self.selected_color_global)

    def enter(self):
        pass

# added
class Score:
    # Constructor
    def __init__(self, display, gameStateManager, screen_w, screen_h):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h

    def run(self):
        self.display.fill('green')  
        font = pygame.font.Font(None, 50)
        text = font.render("Score Page! press e to go to the next page", True, BLACK)
        self.display.blit(text, (self.screen_w // 2 - text.get_width() // 2, self.screen_h // 2 - text.get_height() // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('end')

    def enter(self):
        pass

class End:
    # Constructor
    def __init__(self, display, gameStateManager, screen_w, screen_h):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.background = pygame.image.load("Elements/background/endpage_bg.png")
        self.background = pygame.transform.smoothscale(self.background, (self.screen_w, self.screen_h))

        self.back_button = pygame.image.load("Elements/button/back_button2.png").convert_alpha()
        self.back_button = button.Button(10, 618, self.back_button, 1 / RATIO_720p)

        self.create_wish_btn = pygame.image.load("Elements/button/wish_button.png").convert_alpha()
        self.create_wish_btn = button.Button(922, 612, self.create_wish_btn, 1 / RATIO_720p)

        self.save_button = pygame.image.load("Elements/button/save_button.png").convert_alpha()
        self.save_button = SaveImgButton(1095, 638, self.save_button, 1 / RATIO_720p)

        self.font = pygame.font.Font(None, 20)
        self.open_message = False
        self.alert = Alert("Save the cake image?", self.font, self.screen_w / 2 - 200, self.screen_h / 2 - 100, 400, 200)
        self.alert_active = False

    def run(self):
        self.display.blit(self.background, (0,0))

        self.back_button.draw(self.display)
        self.create_wish_btn.draw(self.display)
        self.save_button.draw(self.display)

                
        self.cake = self.gameStateManager.get_cake()
        self.decorator = CakeDecorator(self.cake, self.display)
        self.decorator.decorate(424, 186, (457, 457))

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if self.alert_active:
                if self.alert.handle_event(event, mouse_pos):
                    self.alert_active = False # alert is done
        if self.alert_active:
            self.alert.draw(self.display)
        else:
            if self.alert.result is not None:
                if self.alert.result:
                    self.save_button.save_cake_img(self.display, 395, 186, 514, 417)
                    self.alert.result = False
                    pass #print("OK was clicked. Image Saved")
                else:
                    pass #print("Cancel was clicked. Image Cancel")
            else:
                pass #print("No button clicked")

        if self.back_button.is_mouse_over():
            self.gameStateManager.set_state('decoration')
        if self.create_wish_btn.is_mouse_over():
            self.gameStateManager.set_state('end_message')
        if self.save_button.is_mouse_over():
            self.alert_active = True
        if pygame.key.get_pressed()[pygame.K_e]:
            self.gameStateManager.reset()
            self.gameStateManager.set_state('start')

    def enter(self):
        pass


class Message:
    # Constructor
    def __init__(self, display, gameStateManager, screen_w, screen_h):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.background = pygame.image.load("Elements/background/end_message_bg.png")
        self.background = pygame.transform.smoothscale(self.background, (self.screen_w, self.screen_h))

        self.back_button = pygame.image.load("Elements/button/back_button2.png").convert_alpha()
        self.back_button = button.Button(10, 618, self.back_button, 1 / RATIO_720p)

        self.save_button = pygame.image.load("Elements/button/save_button.png").convert_alpha()
        self.save_button = SaveImgButton(1095, 638, self.save_button, 1 / RATIO_720p)
        
        self.remove_button = pygame.image.load("Elements/button/remove_button.png").convert_alpha()
        self.remove_button = button.Button(922, 612, self.remove_button, 1 / RATIO_720p)

        self.text_box = LetterTextBox(706, 181, 300, 270)

        self.font = pygame.font.Font(None, 20)
        self.open_message = False
        self.alert = Alert("Save the cake image?", self.font, self.screen_w / 2 - 200, self.screen_h / 2 - 100, 400, 200)

    def run(self):
        self.display.blit(self.background, (0,0))

        self.back_button.draw(self.display)
        self.save_button.draw(self.display)
        self.remove_button.draw(self.display)
        self.text_box.draw(self.display)

        self.gameStateManager.set_event(self.text_box)
        self.text_box.update()

        self.cake = self.gameStateManager.get_cake()
        self.decorator = CakeDecorator(self.cake, self.display)
        if self.decorator.decorate(371, 181, (457, 457)):
            print("pass")

        self.gameStateManager.set_alert(self.alert)
        if self.gameStateManager.get_alert_active():
            self.alert.draw(self.display)
        else:
            if self.alert.result is not None:
                if self.alert.result:
                    self.save_button.save_cake_img(self.display, 185, 100, 900, 494)
                    self.alert.result = False
                else:
                    pass #print("Cancel was clicked. Image Cancel")
            else:
                pass #print("No button clicked")

        if self.back_button.is_mouse_over():
            self.gameStateManager.set_state('decoration')
        if self.remove_button.is_mouse_over():
            self.gameStateManager.set_state('end')
        if self.save_button.is_mouse_over():
            self.gameStateManager.set_alert_active(True)
        if pygame.key.get_pressed()[pygame.K_e]:
            self.gameStateManager.reset()
            self.gameStateManager.set_state('start')

    def enter(self):
        pass