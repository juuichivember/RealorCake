import pygame, os
from decoModule import load_image, get_base_path
from screen import change_ratio_1080_to_720 as change
from timer import Timer
from cakeDecorator import CakeDecorator
from randomizeCake import RandomizeCake

RATIO_720p = 1.5
BASE_PATH = get_base_path()

class RandomCake:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display = display
        self.gameStateManager = gameStateManager
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.sound_manager = sound_manager

        self.background = load_image("background", "randomCake_bg.png", (self.screen_w, self.screen_h))
        self.board = load_image("other", "board.png")
        self.board = pygame.transform.smoothscale(self.board, (change(self.board.get_width()), change(self.board.get_height())))
        self.board_pos = (338, 108)

        # ส่ง self.gameStateManager ให้กับ RandomizeCake เพื่อเชื่อมโยงกับ GameStateManager
        self.rand_cake = RandomizeCake(self.gameStateManager)  # ส่ง gsm ให้ RandomizeCake
        self.decorator = CakeDecorator(self.rand_cake, self.display)
        self.timer = Timer(self.display)

        self.font = pygame.font.Font(os.path.join(BASE_PATH, "assets", "font", "nura-jeni-thin.ttf"), 30)

    def enter(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", "RandomPage.mp3"))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        if self.gameStateManager.get_mode() == 'random':
            self.rand_cake.random_parts()  # สุ่มส่วนประกอบต่างๆ
            self.timer.start()

    def run(self):
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.board, self.board_pos)
        # ดึงรสชาติที่สุ่มมา (เก็บไว้ใน RandomizeCake.parts['filling'][1])
        flavor = self.rand_cake.get_parts().get('filling', ('none', 'none'))[1]
        flavor_text = f"Cake Flavor: {flavor.capitalize()}"
        # ตำแหน่งปรับได้ตามดีไซน์
        text_surf = self.font.render(flavor_text, True, (0, 0, 0))
        self.display.blit(text_surf, (self.board_pos[0] + 30, self.board_pos[1] + 20))
        if self.gameStateManager.get_mode() == 'random':
            self.timer.render()
            for part, (part_type, part_color) in self.rand_cake.parts.items():
                self.decorator.add_decoration(part, part_type, part_color)
            self.decorator.decorate(407, 117, (410, 410))
            self.gameStateManager.set_randomcake(self.rand_cake)
            
            current_image = self.timer.get_current_image()
            image_pos = self.timer.get_pos()
            if current_image:
                self.display.blit(current_image, image_pos)
            if self.timer.is_finished():
                print("Timer finished!")
                self.timer.reset()
                self.gameStateManager.set_state('baking')
        else:
            self.decorator.decorate(407, 117, (410, 410))

    def handle_events(self, event):
        if self.gameStateManager.get_mode() == 'normal':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.gameStateManager.set_state('baking')
