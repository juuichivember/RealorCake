import pygame
import button
from decoModule import load_image, load_cake_part
from screen import change_ratio_1080_to_720 as change

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
            
    def run(self):
        # RUN
        self.display.blit(self.background, (0,0))
        self.display.blit(self.logo, (22,35))
        self.play_button.draw(self.display)
        self.exit_button.draw(self.display)
        if self.play_button.is_mouse_over():
            self.gameStateManager.set_state('random_cake')
        if self.exit_button.is_mouse_over():
            pygame.quit()

# added
class RandomCake:
    # Constructor
    def __init__(self, display, gameStateManager, screen_w, screen_h):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h

    def run(self):
        self.display.fill('green')  
        font = pygame.font.Font(None, 50)
        text = font.render("Random Cake Page! press e to go to the next page", True, BLACK)
        self.display.blit(text, (self.screen_w // 2 - text.get_width() // 2, self.screen_h // 2 - text.get_height() // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('decoration')

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
        self.palette_bg = load_image("Elements/decoration_elements/Color/painttray.png")
        self.palette_bg = pygame.transform.smoothscale(self.palette_bg, (change(self.palette_bg.get_width()), change(self.palette_bg.get_height()))) 
        self.palette_pos = (613, 114) 

        # โหลดปุ่มรีเซ็ต ปุ่มเสร็จสิ้น ปุ่มกลับ
        reset_button_img = pygame.image.load("Elements/button/reset_button.png")
        self.reset_button = button.Button(929, 638, reset_button_img, 1 / RATIO_720p)

        finish_button_img = pygame.image.load("Elements/button/finish_button.png")
        self.finish_button = button.Button(1096, 638, finish_button_img, 1 / RATIO_720p)

        back_button_img = pygame.image.load("Elements/button/back_button1.png")
        self.back_button = button.Button(21, 15, back_button_img, 1 / RATIO_720p)

        self.font = pygame.font.Font(None, 50)

        # จัดการ "สี" (color) และตำแหน่งไอคอนในพาเลตต์ โดยปรับ x เพิ่ม 100px
        #self.color_names = [
            #"none", "grape", "bluberry", "mint", "vanilla", "milk",
            #"carrot", "redvelvet", "strawberry", "charcole", "chocolate", "coffee"
        #]

        self.color_names = [
            "mint", "carrot", "charcole", "grape", "bluberry", "coffee",
            "vanilla", "milk", "strawberry", "chocolate", "redvelvet", "none"
        ]

        self.color_icons = {}
        for color in self.color_names:
            img = load_image(f"Elements/decoration_elements/Color/{color}.png", (44, 42), smooth=False)
            if img:
                self.color_icons[color] = img
        
        self.color_positions = []
        for i, _ in enumerate(self.color_names):
            col = i % 2
            row = i // 2
            # เริ่มต้น x ใช้ palette_pos[0] ที่ปรับแล้ว
            x_pos = self.palette_pos[0] + 12 + (col * 50)
            y_pos = self.palette_pos[1] + 12 + (row * 48)
            self.color_positions.append((x_pos, y_pos))

        self.states = ["base", "behindcream", "lowercream", "middlecream", "topcream", "topping"]

        self.state_options = {
            "base":        ["layered", "plain"],
            "behindcream": ["feather", "wave"],
            "lowercream":  ["feather", "wave"],
            "middlecream": ["ribbon",  "ruffle"],
            "topcream":    ["feather", "wave"],
            "topping":     ["bow", "crown", "floweredge", "flowertop", "pearl", "strawberry_3", "strawberry_4"]
        }

        self.selected_type = {s: None for s in self.states}
        self.selected_color = {s: None for s in self.states}
        self.current_mode = "base"

        # โหลดไอคอนปุ่มด้านบนสำหรับเปลี่ยน sub-state พร้อมปรับตำแหน่ง x (+100)
        self.mode_icons = {}
        self.icon_positions = {}
        start_x = 720
        gap_x = 85
        for i, st in enumerate(self.states):
            icon_path = f"Elements/decoration_elements/deco_button/{st}_button.png"
            icon_img = load_image(icon_path, (88, 85), smooth=False)
            self.mode_icons[st] = icon_img
            self.icon_positions[st] = (start_x + i * gap_x, 24)

        # ตำแหน่งของชั้นวาง (shelf) สำหรับวางภาพตัวเลือก type (แก้ x +100)
        self.shelf_positions = [
            (749, 135), (892, 135), (1038, 135),
            (749, 285), (892, 285), (1038, 285),
            (749, 435), (892, 435), (1038, 435)
        ]

        # ตัวแปรและฟอนต์อื่น ๆ
        self.selected_color_global = None
        self.show_cakes = True
        self.font = pygame.font.Font(None, 50)

    def run(self):
        self.handle_events()
        self.draw_scene()

    # ฟังก์ชันวาดฉากd
    def draw_scene(self):
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.palette_bg, self.palette_pos)

        if self.shelve:
            self.display.blit(self.shelve, self.shelve_pos)

        if self.back_button:
            self.back_button.draw(self.display)

        if self.reset_button:
            self.reset_button.draw(self.display)

        if self.finish_button:
            self.finish_button.draw(self.display)

        for st in self.states:
            icon_img = self.mode_icons[st]
            if icon_img:
                self.display.blit(icon_img, self.icon_positions[st])

        for i, color in enumerate(self.color_names):
            if color in self.color_icons:
                self.display.blit(self.color_icons[color], self.color_positions[i])

        if self.show_cakes:
            types_for_this_state = self.state_options[self.current_mode]
            for i, cake_type in enumerate(types_for_this_state):
                if i < len(self.shelf_positions):
                    thumb_path = f"Elements/decoration_elements/thumbnail/{self.current_mode}_{cake_type}.png"
                    thumb_img = load_image(thumb_path, (167, 167))
                    if thumb_img:
                        self.display.blit(thumb_img, self.shelf_positions[i])

        cake_draw_order = ["base", "topcream", "lowercream", "middlecream", "behindcream", "topping"]
        # ปรับตำแหน่งของเค้กให้ x +100 (จาก 60 เป็น 160)
        final_cake_x, final_cake_y = 62, 209

        for st in cake_draw_order:
            t = self.selected_type[st]
            c = self.selected_color[st]
            part_img = load_cake_part(st, t, c)
            if part_img:
                part_img = pygame.transform.smoothscale(part_img, (511, 511)) #509
                self.display.blit(part_img, (final_cake_x, final_cake_y))

    # ฟังก์ชันจัดการเหตุการณ์
    def handle_events(self):
        if self.reset_button.is_mouse_over():
            for st in self.states:
                self.selected_type[st] = None
                self.selected_color[st] = None
            selected_color_global = None
            print("Reset selection")

        if self.finish_button.is_mouse_over():
            self.show_cakes = not self.show_cakes
            self.gameStateManager.set_state('score_page')

        if self.back_button.is_mouse_over():
            self.gameStateManager.set_state('start')

        x, y = pygame.mouse.get_pos()

        for st in self.states:
            icon_img = self.mode_icons[st]
            if icon_img:
                icon_rect = pygame.Rect(self.icon_positions[st][0],
                                        self.icon_positions[st][1],
                                        icon_img.get_width(),
                                        icon_img.get_height())
                if icon_rect.collidepoint(x, y) and pygame.mouse.get_pressed()[0] == 1:
                    self.current_mode = st
                    print(f"Switched to sub-state: {self.current_mode}")
                    break

        for i, pos in enumerate(self.color_positions):
            color_rect = pygame.Rect(pos[0], pos[1], 30, 30)
            if color_rect.collidepoint(x, y) and pygame.mouse.get_pressed()[0] == 1:
                selected_color_global = self.color_names[i]
                self.selected_color[self.current_mode] = selected_color_global
                print(f"Selected color for [{self.current_mode}]: {selected_color_global}")

        if self.show_cakes:
            types_for_this_state = self.state_options[self.current_mode]
            for i, cake_type in enumerate(types_for_this_state):
                if i < len(self.shelf_positions):
                    rect = pygame.Rect(self.shelf_positions[i], (156, 156))
                    if rect.collidepoint(x, y) and pygame.mouse.get_pressed()[0] == 1:
                        self.selected_type[self.current_mode] = cake_type
                        print(f"Selected type for [{self.current_mode}]: {cake_type}")

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
        self.save_button = button.Button(1095, 638, self.save_button, 1 / RATIO_720p)

    def run(self):
        self.display.blit(self.background, (0,0))

        self.back_button.draw(self.display)
        self.create_wish_btn.draw(self.display)
        self.save_button.draw(self.display)
        if self.back_button.is_mouse_over():
            self.gameStateManager.set_state('decoration')
        if self.create_wish_btn.is_mouse_over():
            self.gameStateManager.set_state('end_message')
        if self.save_button.is_mouse_over():
            self.gameStateManager.set_state('start')


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
        self.save_button = button.Button(1095, 638, self.save_button, 1 / RATIO_720p)
        
        self.remove_button = pygame.image.load("Elements/button/remove_button.png").convert_alpha()
        self.remove_button = button.Button(922, 612, self.remove_button, 1 / RATIO_720p)

        self.open_message = False

    def run(self):
        self.display.blit(self.background, (0,0))

        self.back_button.draw(self.display)
        self.save_button.draw(self.display)
        self.remove_button.draw(self.display)
        if self.back_button.is_mouse_over():
            self.gameStateManager.set_state('decoration')
        if self.remove_button.is_mouse_over():
            self.gameStateManager.set_state('end')
        if self.save_button.is_mouse_over():
            self.gameStateManager.set_state('start')