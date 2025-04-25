# RealorCake/states/randomcake.py

import pygame
import os
from decoModule import load_image, get_base_path
from screen import change_ratio_1080_to_720 as change
from timer import Timer
from cakeDecorator import CakeDecorator
from randomizeCake import RandomizeCake

RATIO_720p = 1.5
BASE_PATH = get_base_path()

class RandomCake:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display          = display
        self.gameStateManager = gameStateManager
        self.screen_w         = screen_w
        self.screen_h         = screen_h
        self.sound_manager    = sound_manager

        # พื้นหลังและบอร์ด
        self.background = load_image(
            "background", "randomCake_bg.png",
            (self.screen_w, self.screen_h)
        )
        self.board = load_image("other", "board.png")
        self.board = pygame.transform.smoothscale(
            self.board,
            (
                change(self.board.get_width()),
                change(self.board.get_height())
            )
        )
        self.board_pos = (338, 108)

        # ตัวสุ่มเค้ก
        self.rand_cake = RandomizeCake(self.gameStateManager)
        self.decorator = CakeDecorator(self.rand_cake, self.display)
        self.timer     = Timer(self.display)

        # ฟอนต์แสดงรสชาติ
        font_path = os.path.join(BASE_PATH, "assets", "font", "nura-jeni-thin.ttf")
        self.font = pygame.font.Font(font_path, 30)

    def enter(self):
        # เริ่มเพลงหน้า Random
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(
            BASE_PATH, "assets", "Sound", "RandomPage.mp3"
        ))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        if self.gameStateManager.get_mode() == 'random':
            # สุ่มส่วนประกอบ และเริ่มจับเวลา
            self.rand_cake.random_parts()
            self.timer.start()

    def run(self):
        # วาดพื้นหลังและบอร์ด
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.board, self.board_pos)

        # แสดงรสชาติที่สุ่มได้
        flavor = self.rand_cake.get_parts().get('filling', ('none', 'none'))[1]
        flavor_text = f"Cake Flavor: {flavor.capitalize()}"
        text_surf = self.font.render(flavor_text, True, (0, 0, 0))
        self.display.blit(
            text_surf,
            (self.board_pos[0] + 30, self.board_pos[1] + 20)
        )

        if self.gameStateManager.get_mode() == 'random':
            # วาดตัวจับเวลา
            self.timer.render()

            # เติมส่วนตกแต่งพร้อมสเกล (410×410)
            for part, (part_type, part_color) in self.rand_cake.parts.items():
                self.decorator.add_decoration(
                    part,
                    part_type,
                    part_color,
                    (410, 410)
                )

            # วาดเค้กพร้อมสเกล
            self.decorator.decorate(407, 117, (410, 410))

            # บันทึก state ของเค้กสุ่ม
            self.gameStateManager.set_randomcake(self.rand_cake)

            # วาดภาพ timer frame
            current_image = self.timer.get_current_image()
            image_pos     = self.timer.get_pos()
            if current_image:
                self.display.blit(current_image, image_pos)

            # เมื่อหมดเวลา -> ไปหน้า Baking
            if self.timer.is_finished():
                print("Timer finished!")
                self.timer.reset()
                self.gameStateManager.set_state('baking')

        else:
            # โหมด normal ใช้ decorate กับสเกลเดียวกัน
            self.decorator.decorate(407, 117, (410, 410))

    def handle_events(self, event):
        # ในโหมด normal คลิกใดก็ไปหน้า Baking
        if (self.gameStateManager.get_mode() == 'normal' and
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            self.gameStateManager.set_state('baking')
