import pygame
import os
from decoModule import load_image, get_base_path
from button import MaskButton as Button
from alert import Alert
from stateManager import GameStateManager

# Constants for stages
STEP_INGREDIENTS = 0
STEP_CUTTING     = 1
STEP_FROSTING    = 2

BASE_PATH = get_base_path()

class BakingPage:
    def __init__(self, screen, gsm: GameStateManager, sw, sh, sound_manager=None):
        self.screen = screen
        self.gsm    = gsm
        self.sw, self.sh = sw, sh
        self.sound = sound_manager

        # Stage 1 state
        self.step        = STEP_INGREDIENTS
        self.ingredients = [
            'egg', 'sugar', 'vanilla_extract', 'baking_flour',
            'baking_powder', 'milk', 'butter', 'salt'
        ]
        self.no_persist  = {'salt'}  # salt ไม่ต้องเก็บภาพ แต่ต้องบันทึกว่าใส่แล้ว
        self.completed   = set()
        self.persistent  = {}

        # Map each ingredient to its animation directory
        self.anim_map = {
            'egg': '02_add_eggs',
            'sugar': '03_add_sugar',
            'vanilla_extract': '04_add_vanillla',
            'baking_flour': '05_add_flour',
            'baking_powder': '06_add_baking_soda',
            'milk': '07_add_milk',
            'butter': '08_add_butter',
            'salt': '09_add_salt',
        }

        # Base asset path
        base = os.path.join(BASE_PATH, 'assets', 'baking_elements', 'stage1_mixing', '01_start')

        # Fullscreen UI layers
        self.bg    = load_image(base, 'mixing_backgroud.png',   (self.sw, self.sh))
        self.bar   = load_image(base, 'ingredients_bar.png',    (self.sw, self.sh))
        self.bowl  = load_image(base, 'bowl.png',               (self.sw, self.sh))
        # Define rectangular bowl area for drop detection
        self.bowl_rect = pygame.Rect(490, 474, 275, 170)

        # Navigation buttons
        back_img     = load_image(base, 'back_button.png', (self.sw, self.sh))
        next_img     = load_image(base, 'next_button.png', (self.sw, self.sh))
        self.btn_back = Button(0, 0, back_img, 1)
        self.btn_next = Button(0, 0, next_img, 1)

        # Ingredient icons + masks + animations
        self.icon_buttons = {}
        self.icon_masks   = {}
        self.anim_frames  = {}
        for ing in self.ingredients:
            path = os.path.join(base, f'{ing}.png')
            surf = pygame.image.load(path).convert_alpha()
            surf = pygame.transform.smoothscale(surf, (self.sw, self.sh))
            btn = Button(0, 0, surf, 1)
            self.icon_buttons[ing] = btn
            self.icon_masks[ing]   = btn.mask

            anim_dir = os.path.join(BASE_PATH, 'assets', 'baking_elements', 'stage1_mixing', self.anim_map[ing])
            frames = []
            if os.path.isdir(anim_dir):
                for fn in sorted(os.listdir(anim_dir)):
                    if fn.endswith('.png'):
                        frame = load_image(
                            os.path.join('baking_elements', 'stage1_mixing', self.anim_map[ing]),
                            fn, (self.sw, self.sh)
                        )
                        frames.append(frame)
            self.anim_frames[ing] = frames

        # Drag & animation state
        self.dragging    = None
        self.drag_offset = (0, 0)
        self.animating   = False

        # Alert for incomplete ingredients
        self.font         = pygame.font.Font(None, 24)
        self.alert        = Alert('Please add all ingredients!', self.font,
                                   self.sw // 2 - 200, self.sh // 2 - 100, 400, 200)
        self.alert_active = False

    def enter(self):
        self.step         = STEP_INGREDIENTS
        self.completed.clear()
        self.persistent.clear()
        self.dragging     = None
        self.animating    = False
        self.alert_active = False

    def run(self):
        if self.step == STEP_INGREDIENTS:
            self.draw_mixing()
        elif self.step == STEP_CUTTING:
            pass
        else:
            pass
        pygame.display.flip()

    def draw_mixing(self):
        # Base UI
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.bar, (0, 0))
        self.screen.blit(self.bowl, (0, 0))
        # persistent layers
        for surf in self.persistent.values():
            self.screen.blit(surf, (0, 0))

        mx, my = pygame.mouse.get_pos()
        # Draw icons and hover
        for ing, btn in self.icon_buttons.items():
            mask = self.icon_masks[ing]
            if ing in self.completed:
                glow = mask.to_surface(setcolor=(255, 255, 0, 180), unsetcolor=(0, 0, 0, 0))
                self.screen.blit(glow, (0, 0))
                self.screen.blit(btn.image, (0, 0))
            else:
                btn.draw(self.screen)
                if not self.animating and mask.get_at((mx, my)):
                    glow = mask.to_surface(setcolor=(255, 255, 0, 100), unsetcolor=(0, 0, 0, 0))
                    self.screen.blit(glow, (0, 0))

        # Draw dragging icon if any
        if self.dragging and not self.animating:
            surf = self.icon_buttons[self.dragging].image
            ox, oy = self.drag_offset
            self.screen.blit(surf, (mx - ox, my - oy))

        # Navigation
        self.btn_back.draw(self.screen)
        self.btn_next.draw(self.screen)
        if self.alert_active:
            self.alert.draw(self.screen)

    def handle_events(self, e):
        if self.step != STEP_INGREDIENTS:
            return
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx, my = e.pos
            for ing, mask in self.icon_masks.items():
                if ing not in self.completed and mask.get_at((mx, my)):
                    self.dragging     = ing
                    self.drag_offset = (mx, my)
                    break
            if self.btn_back.is_mouse_over():
                self.gsm.set_state('option_page')
            if self.btn_next.is_mouse_over():
                needed = set(self.ingredients) - self.no_persist
                if needed.issubset(self.completed):
                    self.step = STEP_CUTTING
                else:
                    self.alert_active = True

        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            if self.dragging and not self.animating:
                x, y = e.pos
                # ตรวจขอบเขตชามด้วยสี่เหลี่ยมกำหนดเอง
                if self.bowl_rect.collidepoint(x, y):
                    self.completed.add(self.dragging)
                    to_animate = self.dragging
                    self.dragging = None
                    self.play_animation(to_animate)
                else:
                    self.dragging = None

        if self.alert_active and self.alert.handle_event(e, pygame.mouse.get_pos()):
            self.alert_active = False

    def play_animation(self, name):
        frames = self.anim_frames.get(name, [])
        delay  = 800  # ms per frame
        base_surface = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        # วาด background, bar, bowl, persistent
        base_surface.blit(self.bg,   (0, 0))
        base_surface.blit(self.bar,  (0, 0))
        base_surface.blit(self.bowl, (0, 0))
        for surf in self.persistent.values():
            base_surface.blit(surf, (0, 0))
        # วาด icons ตามสถานะ completed
        for ing, btn in self.icon_buttons.items():
            mask = self.icon_masks[ing]
            if ing in self.completed:
                glow = mask.to_surface(setcolor=(255, 255, 0, 180), unsetcolor=(0, 0, 0, 0))
                base_surface.blit(glow, (0, 0))
            base_surface.blit(btn.image, (0, 0))
        # วาดปุ่ม navigation
        self.btn_back.draw(base_surface)
        self.btn_next.draw(base_surface)

        # เล่นแอนิเมชัน
        for frame in frames:
            self.screen.blit(base_surface, (0, 0))
            self.screen.blit(frame, (0, 0))
            pygame.display.flip()
            pygame.time.delay(delay)

        # หลังจบ animation เก็บเฟรมสุดท้ายถ้าจำเป็น
        if name not in self.no_persist and frames:
            self.persistent[name] = frames[-1]

    def exit(self):
        pass
