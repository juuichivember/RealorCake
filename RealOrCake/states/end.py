import pygame, os
from decoModule import load_image, get_base_path
from saveImgButton import SaveImgButton
from button import Button
from alert import Alert

RATIO_720p = 1.5
BASE_PATH = get_base_path()

class End:
    def __init__(self, display, gameStateManager, screen_w, screen_h, sound_manager=None):
        self.display = display
        self.gsm     = gameStateManager
        self.sw, self.sh = screen_w, screen_h
        self.sound  = sound_manager

        # Surface สำหรับ background + cake (ที่จะเซฟ)
        self.content_surface = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)

        # Background
        self.background = load_image("background", "endpage_bg.png", (self.sw, self.sh))

        # UI buttons
        self.back_button     = Button(10,   618, load_image("button","back_button2.png"), 1/RATIO_720p)
        self.create_wish_btn = Button(922,  612, load_image("button","wish_button.png"),    1/RATIO_720p)
        self.save_button     = SaveImgButton(1095,638, load_image("button","save_button.png"),1/RATIO_720p)
        self.home_button     = Button(1091, 0,   load_image("button","home_button.png"),   1/RATIO_720p)

        # Alert
        self.font  = pygame.font.Font(None, 20)
        self.alert = Alert(
            "Save the cake image?",
            self.font,
            self.sw//2 - 200,
            self.sh//2 - 100,
            400, 200
        )
        self.alert_active = False

    def enter(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(BASE_PATH,"assets","Sound","EndPage.mp3"))
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

        # รีเซ็ต Alert
        self.alert.result = None
        self.alert_active = False

    def run(self):
        # 1) วาด background + cake ลง content_surface
        self.content_surface.fill((0,0,0,0))
        self.content_surface.blit(self.background, (0,0))

        from cakeDecorator import CakeDecorator
        cake = self.gsm.get_cake()
        decorator = CakeDecorator(cake, self.content_surface)
        decorator.decorate(424, 186, (457, 457))

        # 2) Blit content_surface ขึ้น display
        self.display.blit(self.content_surface, (0,0))

        # 3) วาด UI buttons บน display
        for btn in (self.back_button, self.create_wish_btn, self.save_button, self.home_button):
            btn.draw(self.display)

        # 4) Alert
        if self.alert_active:
            self.alert.draw(self.display)
        elif self.alert.result is not None:
            if self.alert.result:
                # เซฟภาพจาก content_surface
                self.save_button.save_cake_img(self.content_surface)
                self.alert.result = False
            else:
                self.alert.result = None

    def handle_events(self, event):
        # 1) Alert event
        if self.alert_active and event.type == pygame.MOUSEBUTTONDOWN:
            if self.alert.handle_event(event, pygame.mouse.get_pos()):
                self.alert_active = False

        # 2) Buttons
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.is_mouse_over():
                self.gsm.set_state('score_page')
            elif self.create_wish_btn.is_mouse_over():
                self.gsm.set_state('end_message')
            elif self.save_button.is_mouse_over():
                self.alert_active = True
            elif self.home_button.is_mouse_over():
                self.gsm.reset()
                self.gsm.set_state('start')
