import pygame
import sys, os
from state import Start, RandomCake, Decoration, Score, End, Message
from stateManager import *
from screen import set_screen
from decoModule import get_base_path

# 1) import SoundManager
from soundManager import SoundManager

#SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

# Default setup

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # เริ่มต้นระบบเสียง

        # 2) สร้างออบเจ็กต์ SoundManager
        self.sound_manager = SoundManager()

        screen_size = pygame.display.get_desktop_sizes()
        self.screen_w, self.screen_h = set_screen(screen_size[0])

                # โหลดโลโก้
        base_path = get_base_path() # หา path ของไฟล์
        icon_path = os.path.join(base_path, "assets", "other", "logo64.png")  # path ของโลโก้, ทำมาใหม่ให้เป็น 64x64
        icon = pygame.image.load(icon_path)  # โหลดรูปภาพ

        pygame.display.set_caption("Namkhing's Cake")
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.clock = pygame.time.Clock()

        # Call Context's and Concrete State's Constructor
        self.gameStateManager = GameStateManager('start')

        # 3) ส่ง sound_manager เข้าไปใน State แต่ละตัว
        self.start = Start(self.screen, self.gameStateManager, self.screen_w, self.screen_h, self.sound_manager)
        self.random_cake = RandomCake(self.screen, self.gameStateManager, self.screen_w, self.screen_h, self.sound_manager)
        self.decoration = Decoration(self.screen, self.gameStateManager, self.screen_w, self.screen_h, self.sound_manager)
        self.score_page = Score(self.screen, self.gameStateManager, self.screen_w, self.screen_h, self.sound_manager)
        self.end = End(self.screen, self.gameStateManager, self.screen_w, self.screen_h, self.sound_manager)
        self.message = Message(self.screen, self.gameStateManager, self.screen_w, self.screen_h, self.sound_manager)

        self.states = {
            'start': self.start, 
            'random_cake': self.random_cake,
            'decoration': self.decoration,
            'score_page': self.score_page,
            'end': self.end,
            'end_message': self.message
        }
        self.start.enter()
        # เพิ่ม flag สำหรับตรวจสอบการกด mouse click
        self.click_sound_played = False

    def run(self):
        current_state = self.gameStateManager.get_state()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # ตรวจสอบการกดปุ่ม mouse
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # ถ้าไม่ได้กดในพื้นที่ของปุ่ม start (หรือปุ่มใดๆ ที่มีเสียงเฉพาะ) ให้เล่น normal_click
                    # ตัวอย่าง: สมมติว่าคุณตรวจสอบตำแหน่งของ play_button (หรือสามารถให้แต่ละปุ่มจัดการเอง)
                    if not self.start.play_button.rect.collidepoint(event.pos):
                        if not self.click_sound_played:
                            self.sound_manager.play("normal_click")
                            self.click_sound_played = True
                        
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # รีเซ็ต flag เมื่อปล่อยปุ่ม
                    self.click_sound_played = False

                if current_state == "end_message":
                    self.gameStateManager.get_event().handle_event(event)

                if self.gameStateManager.get_alert_active():
                    if self.gameStateManager.alert.handle_event(event, mouse_pos):
                        self.gameStateManager.set_alert_active(False)  # alert is done
                
                self.states[current_state].handle_events(event)

            new_state = self.gameStateManager.get_state()

            if new_state != current_state:
                self.states[new_state].enter()
                current_state = new_state
            
            self.states[new_state].run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
