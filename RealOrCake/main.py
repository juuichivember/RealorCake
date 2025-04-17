import pygame
import sys, os
from states import (
    Start, OptionPage, RandomCake, Decoration,
    Score, End, Message, GalleryPage, BakingPage,
)
from stateManager import GameStateManager
from screen import set_screen
from decoModule import get_base_path

from soundManager import SoundManager

FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.sound_manager = SoundManager()

        # ตั้งขนาดหน้าจอ
        screen_size = pygame.display.get_desktop_sizes()[0]
        self.screen_w, self.screen_h = set_screen(screen_size)

        # ตั้งไอคอน
        base = get_base_path()
        icon = pygame.image.load(os.path.join(base, "assets","other","logo64.png"))
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Namkhing's Cake")

        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.clock  = pygame.time.Clock()

        # สร้าง GameStateManager
        self.gsm = GameStateManager('start')

        # สร้าง state ต่าง ๆ
        self.start        = Start(self.screen, self.gsm, self.screen_w, self.screen_h, self.sound_manager)
        self.option_page  = OptionPage(self.screen, self.gsm, self.screen_w, self.screen_h, self.sound_manager)
        self.random_cake  = RandomCake(self.screen, self.gsm, self.screen_w, self.screen_h, self.sound_manager)
        self.baking = BakingPage(self.screen, self.gsm, self.screen_w, self.screen_h, self.sound_manager)
        self.decoration   = Decoration(self.screen, self.gsm, self.screen_w, self.screen_h, self.sound_manager)
        self.score_page   = Score(self.screen, self.gsm, self.screen_w, self.screen_h, self.sound_manager)
        self.end          = End(self.screen, self.gsm, self.screen_w, self.screen_h, self.sound_manager)
        self.message      = Message(self.screen, self.gsm, self.screen_w, self.screen_h, self.sound_manager)
        self.gallery_page = GalleryPage(self.screen, self.gsm, self.screen_w, self.screen_h, self.sound_manager)

        # แมปชื่อ state ไปยังออบเจ็กต์
        self.states = {
            'start':        self.start,
            'option_page':  self.option_page,
            'random_cake':  self.random_cake,
            'baking':       self.baking,
            'decoration':   self.decoration,
            'score_page':   self.score_page,
            'end':          self.end,
            'end_message':  self.message,
            'gallery_page': self.gallery_page,
        }

        # เริ่มต้นที่หน้า start
        self.start.enter()
        self.click_sound_played = False

    def run(self):
        current = self.gsm.get_state()

        while True:
            # 1) ดัก event ครั้งเดียว
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # เสียงคลิกทั่วไป (ถ้าต้องการ)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # ถ้าไม่ได้คลิกบนปุ่มที่มีเสียงเฉพาะ
                    if not self.start.play_button.rect.collidepoint(event.pos):
                        if not self.click_sound_played:
                            self.sound_manager.play("normal_click")
                            self.click_sound_played = True

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.click_sound_played = False

                # 2) ส่งต่อให้ state ปัจจุบันจัดการ
                self.states[current].handle_events(event)

            # 3) เช็คเปลี่ยน state
            nxt = self.gsm.get_state()
            if nxt != current:
                self.states[nxt].enter()
                current = nxt

            # 4) วาดหน้าจอ
            self.states[current].run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    Game().run()
