import pygame
import os
from decoModule import load_image, get_base_path
from button import MaskButton as Button
from stateManager import GameStateManager

# Constants for stages
STEP_INGREDIENTS = 0
STEP_MIX_IT      = 1
STEP_CUTTING     = 2
STEP_FROSTING    = 3

BASE_PATH = get_base_path()

class BakingPage:
    def __init__(self, screen, gsm: GameStateManager, sw, sh, sound_manager=None):
        self.screen = screen
        self.gsm    = gsm
        self.sw, self.sh = sw, sh
        self.sound = sound_manager

        # Stage state
        self.step        = STEP_INGREDIENTS
        self.ingredients = [
            'egg','sugar','vanilla_extract','baking_flour',
            'baking_powder','milk','butter','salt'
        ]
        self.completed   = set()
        self.persistent  = {}
        self.no_persist  = {'salt'}  # salt marked complete but not persisted

        # Ingredient animation folders
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

        # Load mixing UI
        base = os.path.join(BASE_PATH, 'assets', 'baking_elements', 'stage1_mixing', '01_start')
        self.bg         = load_image(base, 'mixing_backgroud.png', (self.sw, self.sh))
        self.bar        = load_image(base, 'ingredients_bar.png', (self.sw, self.sh))
        self.bowl       = load_image(base, 'bowl.png',         (self.sw, self.sh))
        self.bowl_rect  = pygame.Rect(490, 474, 275, 170)

        # Navigation buttons
        back_img = load_image(base, 'back_button.png', (self.sw, self.sh))
        next_img = load_image(base, 'next_button.png', (self.sw, self.sh))
        self.btn_back = Button(0, 0, back_img, 1)
        self.btn_next = Button(0, 0, next_img, 1)

        # Load ingredient icons and animations
        self.icon_buttons = {}
        self.icon_masks   = {}
        self.anim_frames  = {}
        for ing in self.ingredients:
            path = os.path.join(base, f"{ing}.png")
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (self.sw, self.sh))
            btn = Button(0, 0, img, 1)
            self.icon_buttons[ing] = btn
            self.icon_masks[ing]   = btn.mask
            anim_dir = os.path.join(BASE_PATH, 'assets', 'baking_elements', 'stage1_mixing', self.anim_map[ing])
            frames = []
            if os.path.isdir(anim_dir):
                for fn in sorted(os.listdir(anim_dir)):
                    if fn.endswith('.png'):
                        frames.append(load_image(os.path.join('baking_elements','stage1_mixing',self.anim_map[ing]), fn, (self.sw, self.sh)))
            self.anim_frames[ing] = frames

        # Load mix-it UI
        mix_dir = os.path.join(BASE_PATH, 'assets', 'baking_elements', 'stage1_mixing', '10_mix_it')
        self.mix_it_bar    = load_image(mix_dir, 'mix_it_bar.png', (self.sw, self.sh))
        blender_img         = load_image(mix_dir, 'mix_it_blender.png', (self.sw, self.sh))
        self.blender_btn   = Button(0, 0, blender_img, 1)
        self.mix_it_frames = []
        if os.path.isdir(mix_dir):
            for fn in sorted(os.listdir(mix_dir)):
                if fn.startswith('mix_it_') and fn.endswith('.png') and fn not in ('mix_it_bar.png','mix_it_blender.png'):
                    self.mix_it_frames.append(load_image(mix_dir, fn, (self.sw, self.sh)))

        # State flags
        self.mix_ready = False  # all ingredients added
        self.mix_done  = False  # mix-it animation played
        self.dragging  = None
        self.drag_offset = (0,0)

    def enter(self):
        self.step       = STEP_INGREDIENTS
        self.completed.clear()
        self.persistent.clear()
        self.mix_ready = False
        self.mix_done  = False
        self.dragging  = None

    def run(self):
        if self.step == STEP_INGREDIENTS:
            self.draw_mixing()
        elif self.step == STEP_MIX_IT:
            self.draw_mix_it()
        elif self.step == STEP_CUTTING:
            pass  # future
        pygame.display.flip()

    def draw_mixing(self):
        # Base mixing UI
        self.screen.blit(self.bg,   (0,0))
        self.screen.blit(self.bar,  (0,0))
        self.screen.blit(self.bowl, (0,0))
        for surf in self.persistent.values():
            self.screen.blit(surf, (0,0))
        # Ingredient icons
        mx,my = pygame.mouse.get_pos()
        for ing, btn in self.icon_buttons.items():
            mask = self.icon_masks[ing]
            if ing in self.completed:
                glow = mask.to_surface(setcolor=(255,255,0,180), unsetcolor=(0,0,0,0))
                self.screen.blit(glow,(0,0))
                self.screen.blit(btn.image,(0,0))
            else:
                btn.draw(self.screen)
                if mask.get_at((mx,my)):
                    glow=mask.to_surface(setcolor=(255,255,0,100),unsetcolor=(0,0,0,0))
                    self.screen.blit(glow,(0,0))
        # Navigation
        self.btn_back.draw(self.screen)
        # Show Next only when ready
        if self.mix_ready:
            self.btn_next.draw(self.screen)
        # Drag overlay
        if self.dragging:
            surf=self.icon_buttons[self.dragging].image; ox,oy=self.drag_offset
            self.screen.blit(surf,(mx-ox,my-oy))

    def draw_mix_it(self):
        # Base mix-it UI
        self.screen.blit(self.bg,         (0,0))
        self.screen.blit(self.mix_it_bar, (0,0))
        # Mix frame first or last
        if self.mix_it_frames:
            frame = self.mix_it_frames[-1] if self.mix_done else self.mix_it_frames[0]
            self.screen.blit(frame,(0,0))
        # Blender icon
        self.blender_btn.draw(self.screen)
        # Show Next only when mixed
        if self.mix_done:
            self.btn_next.draw(self.screen)

    def handle_events(self, e):
        if self.step == STEP_INGREDIENTS:
            self._handle_ing(e)
        elif self.step == STEP_MIX_IT:
            self._handle_mix_it(e)

    def _handle_ing(self, e):
        if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
            # Back always allowed
            if self.btn_back.is_mouse_over():
                self.gsm.set_state('option_page'); return
            # Next only if ready
            if self.btn_next.is_mouse_over() and self.mix_ready:
                self.step = STEP_MIX_IT; return
            # Start drag
            mx,my=e.pos
            for ing,mask in self.icon_masks.items():
                if ing not in self.completed and mask.get_at((mx,my)):
                    self.dragging,self.drag_offset=ing,(mx,my); break
        elif e.type==pygame.MOUSEBUTTONUP and e.button==1 and self.dragging:
            x,y=e.pos; ing=self.dragging; self.dragging=None
            if self.bowl_rect.collidepoint(x,y):
                self.completed.add(ing)
                self.play_animation(ing)
                if set(self.ingredients)==self.completed:
                    self.mix_ready=True

    def _handle_mix_it(self, e):
        if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
            # Next only if mixed
            if self.btn_next.is_mouse_over() and self.mix_done:
                self.step = STEP_CUTTING; return
            # Blend action
            if self.blender_btn.is_mouse_over() and not self.mix_done:
                self.play_mix_it_animation(); self.mix_done=True

    def play_animation(self, name):
        frames=self.anim_frames[name]; delay=500
        base=self._make_snapshot()
        for f in frames:
            self.screen.blit(base,(0,0)); self.screen.blit(f,(0,0))
            pygame.display.flip(); pygame.time.delay(delay)
        if name not in self.no_persist and frames:
            self.persistent[name]=frames[-1]

    def play_mix_it_animation(self):
        delay = 500
        for frame in self.mix_it_frames:
            self.screen.blit(self.bg,         (0,0))
            self.screen.blit(self.mix_it_bar, (0,0))
            self.screen.blit(frame,           (0,0))
            pygame.display.flip()
            pygame.time.delay(delay)

    def _make_snapshot(self):
        base = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        base.blit(self.bg,   (0,0))
        base.blit(self.bar,  (0,0))
        base.blit(self.bowl, (0,0))
        for surf in self.persistent.values():
            base.blit(surf, (0,0))
        for ing, btn in self.icon_buttons.items():
            if ing in self.completed:
                glow = self.icon_masks[ing].to_surface(setcolor=(255,255,0,180), unsetcolor=(0,0,0,0))
                base.blit(glow, (0,0))
            base.blit(btn.image, (0,0))
        self.btn_back.draw(base)
        # Next button intentionally omitted from snapshot
        return base

    def exit(self):
        pass
