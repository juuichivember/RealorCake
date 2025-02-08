import pygame
import button
from loadImage import load_cake_image
from screen import change_ratio_1080_to_720 as change

# กำหนดสี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

        self.background = pygame.image.load("Elements/Homepage_bg.png")
        self.background = pygame.transform.smoothscale(self.background, (self.screen_w, self.screen_h))

        self.button_img = pygame.image.load("Elements/button.png").convert_alpha()
        self.play_button = button.Button(200, 200, self.button_img, 0.2)
        self.exit_button = button.Button(200, 300, self.button_img, 0.2)
    
    def run(self):
        # RUN
        self.display.blit(self.background, (0,0))
        self.play_button.draw(self.display)
        self.exit_button.draw(self.display)
        if self.play_button.is_mouse_over():
            self.gameStateManager.set_state('decoration')
        if self.exit_button.is_mouse_over():
            pygame.quit()

class Decoration:
    # Constructor
    def __init__(self, display, gameStateManager, screen_w, screen_h):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h

        pygame.display.set_caption("Namkhing's Cake - Select Your Cake Base")

        # โหลดภาพพื้นหลัง
        self.background = pygame.image.load("Elements/shop_background.png")
        self.background = pygame.transform.smoothscale(self.background, (self.screen_w, self.screen_h))

        # โหลดภาพชั้นวางเค้ก
        self.shelve = pygame.image.load("Elements/shelve.png")
        self.shelve = pygame.transform.smoothscale(self.shelve, (508, 534))  # ปรับขนาดชั้นวาง

        # โหลดภาพโต๊ะ
        self.table = pygame.image.load("Elements/table.png")
        self.table = pygame.transform.smoothscale(self.table, (868, 542))  # ปรับขนาดโต๊ะ

        # โหลดปุ่มรีเซ็ตและปุ่มเสร็จสิ้น
        reset_button_img = pygame.image.load("Elements/reset_button.png")
        self.reset_button = button.Button(826, 633, reset_button_img, 0.511)

        finish_button_img = pygame.image.load("Elements/finish_button.png")
        self.finish_button = button.Button(1026, 633, finish_button_img, 0.511)

        self.font = pygame.font.Font(None, 50)

        cake_types = ["vanilla", "chocolate", "strawberry",
                      "charcole", "blueberry", "grape",
                      "carrot", "milk", "mint"]
        
        self.cake_options = {cake: load_cake_image(cake) for cake in cake_types}

        self.final_positions = {
            "vanilla": (770, 139), "chocolate": (918, 139), "strawberry": (1063, 139),
            "charcole": (770, 293), "blueberry": (918, 293), "grape": (1063, 293),
            "carrot": (770, 444), "milk": (918, 444), "mint": (1063, 444)
        }
        
        for key in self.cake_options:
            if self.cake_options[key]:  # ตรวจสอบว่ารูปโหลดสำเร็จ
                self.cake_options[key] = pygame.transform.smoothscale(self.cake_options[key], (173, 173)).convert_alpha()

        self.selected_cake = None
        self.show_cakes = False
    
    def run(self):
        shelve_x, shelve_y = (747, -194) # เริ่มต้นอยู่นอกจอด้านบน
        shelve_target_y = 72  # จุดที่ชั้นวางต้องหยุด
        shelve_speed = 15  # ความเร็วในการเลื่อนลงมา
        table_x, table_y = (-355, 530)

        # -------- RUN ---------
        self.display.blit(self.background, (0, 0))  # วาดพื้นหลัง

        # เคลื่อนชั้นวางและโต๊ะเข้ามาพร้อมกัน
        move = True
        while move:
            if shelve_y < shelve_target_y:
                shelve_y += shelve_speed
            if table_x < -88:
                table_x += shelve_speed  # ใช้ความเร็วเดียวกับชั้นวาง
            else:
                move = False
                self.show_cakes = True  # เมื่อชั้นวางถึงจุดสุดท้าย ให้แสดงเค้ก

        self.display.blit(self.shelve, (shelve_x, shelve_y))
        self.display.blit(self.table, (table_x, table_y))
        
        # แสดงข้อความ
        text = self.font.render("Select Your Cake Base", True, BLACK)
        self.display.blit(text, (self.screen_w // 2 - text.get_width() // 2, change(100)))

        # แสดงฐานเค้กหลังจากชั้นวางถึงตำแหน่งสุดท้าย
        if self.show_cakes:
            for key, pos in self.final_positions.items():
                if self.cake_options[key]:
                    self.display.blit(self.cake_options[key], pos)
            self.reset_button.draw(self.display)
            self.finish_button.draw(self.display)

        for key, pos in self.final_positions.items():
            if self.cake_options[key]:
                self.display.blit(self.cake_options[key], pos)
        
        if pygame.mouse.get_pressed()[0] == 1 and self.show_cakes:
            x, y = pygame.mouse.get_pos()
            for key, pos in self.final_positions.items():
                cake_rect = pygame.Rect(pos[0], pos[1], 173, 173)
                if cake_rect.collidepoint(x, y):
                    self.selected_cake = key

        # แสดงฐานเค้กที่ถูกเลือก
        if self.selected_cake:
            selected_cake_img = load_cake_image(self.selected_cake)
            if selected_cake_img:
                selected_cake_img = pygame.transform.smoothscale(selected_cake_img, (564, 564))
                cake_x = 66
                cake_y = 165
                self.display.blit(selected_cake_img, (cake_x, cake_y))

        if self.finish_button.is_mouse_over():
            self.gameStateManager.set_state('end')
        if self.reset_button.is_mouse_over():
            self.selected_cake = None

class End:
    # Constructor
    def __init__(self, display, gameStateManager, screen_w, screen_h):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h

    def run(self):
        self.display.fill('green')  
        font = pygame.font.Font(None, 80)
        text = font.render("End page!", True, BLACK)
        self.display.blit(text, (self.screen_w // 2 - text.get_width() // 2, self.screen_h // 2 - text.get_height() // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('start')