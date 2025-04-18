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
        # Core references
        self.screen = screen
        self.gsm    = gsm
        self.sw, self.sh = sw, sh
        self.sound = sound_manager
        self.filling_selected = None  # กำหนดตัวแปรเก็บค่า filling ที่ผู้เล่นเลือก

        # State flags
        self.step           = STEP_INGREDIENTS
        self.ingredients    = ['egg','sugar','vanilla_extract','baking_flour',
                               'baking_powder','milk','butter','salt']
        self.completed      = set()
        self.persistent     = {}
        self.no_persist     = {'salt'}
        self.mix_ready      = False
        self.mix_done       = False
        self.cut_done       = False
        self.frost_done     = False
        self.dragging       = None
        self.drag_offset    = (0, 0)
        self.current_flavor = None

        # Ingredient animation mapping
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
        mix_base = os.path.join(BASE_PATH, 'assets', 'baking_elements', 'stage1_mixing', '01_start')
        self.bg        = load_image(mix_base, 'mixing_backgroud.png', (self.sw, self.sh))
        self.bar       = load_image(mix_base, 'ingredients_bar.png', (self.sw, self.sh))
        self.bowl      = load_image(mix_base, 'bowl.png', (self.sw, self.sh))
        self.bowl_rect = pygame.Rect(490, 474, 275, 170)
        back_img       = load_image(mix_base, 'back_button.png', (self.sw, self.sh))
        next_img       = load_image(mix_base, 'next_button.png', (self.sw, self.sh))
        self.btn_back  = Button(0, 0, back_img, 1)
        self.btn_next  = Button(0, 0, next_img, 1)

        # Ingredient icons
        self.icon_buttons = {}
        self.icon_masks   = {}
        for ing in self.ingredients:
            img_path = os.path.join(mix_base, f"{ing}.png")
            surf = pygame.image.load(img_path).convert_alpha()
            surf = pygame.transform.smoothscale(surf, (self.sw, self.sh))
            btn  = Button(0, 0, surf, 1)
            self.icon_buttons[ing] = btn
            self.icon_masks[ing]   = btn.mask

        # Ingredient animations
        self.anim_frames = {}
        for ing, folder in self.anim_map.items():
            anim_dir = os.path.join(BASE_PATH, 'assets', 'baking_elements', 'stage1_mixing', folder)
            frames   = []
            if os.path.isdir(anim_dir):
                for fn in sorted(os.listdir(anim_dir)):
                    if fn.endswith('.png'):
                        frames.append(load_image(anim_dir, fn, (self.sw, self.sh)))
            self.anim_frames[ing] = frames

        # Mix-it UI
        mix_dir = os.path.join(BASE_PATH, 'assets', 'baking_elements', 'stage1_mixing', '10_mix_it')
        self.mix_it_bar    = load_image(mix_dir, 'mix_it_bar.png', (self.sw, self.sh))
        blender_img        = load_image(mix_dir, 'mix_it_blender.png', (self.sw, self.sh))
        self.blender_btn   = Button(0, 0, blender_img, 1)
        self.mix_it_frames = []
        if os.path.isdir(mix_dir):
            for fn in sorted(os.listdir(mix_dir)):
                if fn.startswith('mix_it_') and fn.endswith('.png') and fn not in ('mix_it_bar.png','mix_it_blender.png'):
                    self.mix_it_frames.append(load_image(mix_dir, fn, (self.sw, self.sh)))

        # Cutting UI
        cut_dir = os.path.join(BASE_PATH, 'assets', 'baking_elements', 'stage2_cutting')
        self.cake_rect   = pygame.Rect(450, 420, 355, 225)
        self.cutting_1   = load_image(cut_dir, 'cutting_1.png', (self.sw, self.sh))
        self.cutting_8   = load_image(cut_dir, 'cutting_8.png', (self.sw, self.sh))
        knife_img        = load_image(cut_dir, 'knife.png', (self.sw, self.sh))
        self.knife_btn   = Button(0, 0, knife_img, 1)
        self.cut_frames  = [load_image(cut_dir, f'cutting_{i}.png', (self.sw, self.sh)) for i in range(2,7)]
        self.cut_final   = [load_image(cut_dir, fn, (self.sw, self.sh)) for fn in ('cutting_7.png','cutting_8.png')]

        # Frosting UI
        frost_base         = os.path.join(BASE_PATH, 'assets', 'baking_elements', 'stage3_creaming')
        self.piping_bar     = load_image(frost_base, 'piping_bar.png', (self.sw, self.sh))
        self.reset_img      = load_image(frost_base, 'reset_flavour_button.png', (self.sw, self.sh))
        self.reset_btn      = Button(0, 0, self.reset_img, 1)
        self.piping_flavors = ['blueberry','chocolate','orange','strawberry','vanilla']
        self.piping_buttons = {}
        self.piping_masks   = {}
        for flavor in self.piping_flavors:
            img = load_image(frost_base, f'{flavor}_piping.png', (self.sw, self.sh))
            btn = Button(0, 0, img, 1)
            self.piping_buttons[flavor] = btn
            self.piping_masks[flavor]   = btn.mask
        self.frost_frames = {}
        for flavor in self.piping_flavors:
            suf = 'bluberry' if flavor=='blueberry' else flavor
            frames = []
            for subdir, fn_template in [('step_2_smooth_cream', f'smooth_cream_{suf}.png'),
                                       ('step1_spread_cream', f'spread_cream_{suf}.png'),
                                       ('step3_assemble_cake', f'assemble_cake_{suf}.png')]:
                frames.append(load_image(os.path.join(frost_base, subdir), fn_template, (self.sw, self.sh)))
            self.frost_frames[flavor] = frames

    def enter(self):
        self.step           = STEP_INGREDIENTS
        self.completed.clear()
        self.persistent.clear()
        self.mix_ready      = self.mix_done = self.cut_done = self.frost_done = False
        self.dragging       = None
        self.current_flavor = None
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", "baking_background.mp3"))
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

    def run(self):
        if self.step == STEP_INGREDIENTS:
            self.draw_mixing()
        elif self.step == STEP_MIX_IT:
            self.draw_mix_it()
        elif self.step == STEP_CUTTING:
            self.draw_cutting()
        elif self.step == STEP_FROSTING:
            self.draw_frosting()
        pygame.display.flip()

    def draw_mixing(self):
        self.screen.blit(self.bg, (0,0))
        self.screen.blit(self.bar, (0,0))
        self.screen.blit(self.bowl,(0,0))
        for surf in self.persistent.values():
            self.screen.blit(surf,(0,0))
        mx,my = pygame.mouse.get_pos()
        for ing,btn in self.icon_buttons.items():
            mask = self.icon_masks[ing]
            if ing in self.completed:
                glow = mask.to_surface(setcolor=(255,255,0,180), unsetcolor=(0,0,0,0))
                self.screen.blit(glow,(0,0))
                self.screen.blit(btn.image,(0,0))
            else:
                btn.draw(self.screen)
                if mask.get_at((mx,my)):
                    glow = mask.to_surface(setcolor=(255,255,0,100), unsetcolor=(0,0,0,0))
                    self.screen.blit(glow,(0,0))
        self.btn_back.draw(self.screen)
        if self.mix_ready:
            self.btn_next.draw(self.screen)
        if self.dragging:
            img = self.icon_buttons[self.dragging].image
            ox,oy = self.drag_offset
            self.screen.blit(img,(mx-ox,my-oy))

    def draw_mix_it(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.mix_it_bar, (0, 0))
        if self.mix_it_frames:
            frame = self.mix_it_frames[-1] if self.mix_done else self.mix_it_frames[0]
            self.screen.blit(frame, (0, 0))
        self.blender_btn.draw(self.screen)
        
        # เพิ่มการแสดงแสง (glow) สำหรับ blender
        mx, my = pygame.mouse.get_pos()
        if self.blender_btn.mask.get_at((mx, my)):
            glow = self.blender_btn.mask.to_surface(setcolor=(255, 255, 0, 100), unsetcolor=(0, 0, 0, 0))
            self.screen.blit(glow, (0, 0))
        
        if self.mix_done:
            self.btn_next.draw(self.screen)

    def draw_cutting(self):
        self.screen.blit(self.bg, (0, 0))
        if not self.cut_done and self.dragging is None:
            self.screen.blit(self.cutting_1, (0, 0))
            self.knife_btn.draw(self.screen)
            
            # เพิ่มการแสดงแสง (glow) สำหรับ knife
            mx, my = pygame.mouse.get_pos()
            if self.knife_btn.mask.get_at((mx, my)):
                glow = self.knife_btn.mask.to_surface(setcolor=(255, 255, 0, 100), unsetcolor=(0, 0, 0, 0))
                self.screen.blit(glow, (0, 0))
        elif self.dragging == 'knife':
            mx, my = pygame.mouse.get_pos()
            ox, oy = self.drag_offset
            self.screen.blit(self.cutting_1, (0, 0))
            self.screen.blit(self.knife_btn.image, (mx - ox, my - oy))
        else:
            for img in self.cut_final:
                self.screen.blit(img, (0, 0))
            self.btn_next.draw(self.screen)


    def draw_frosting(self):
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.cutting_8,(0,0))
        self.reset_btn.draw(self.screen)
        mx,my = pygame.mouse.get_pos()
        if self.frost_done and self.current_flavor:
            assemble = self.frost_frames[self.current_flavor][2]
            self.screen.blit(assemble,(0,0))
            self.btn_next.draw(self.screen)
        else:
            self.screen.blit(self.piping_bar,(0,0))
            for flavor,btn in self.piping_buttons.items():
                mask = self.piping_masks[flavor]
                btn.draw(self.screen)
                if mask.get_at((mx,my)):
                    glow = mask.to_surface(setcolor=(255,255,0,100),unsetcolor=(0,0,0,0))
                    self.screen.blit(glow,(0,0))
            if self.dragging in self.piping_flavors:
                mx,my = pygame.mouse.get_pos()
                ox,oy = self.drag_offset
                self.screen.blit(self.piping_buttons[self.dragging].image,(mx-ox,my-oy))

    def handle_events(self, e):
        if self.step == STEP_INGREDIENTS:
            self._handle_ing(e)
        elif self.step == STEP_MIX_IT:
            self._handle_mix_it(e)
        elif self.step == STEP_CUTTING:
            self._handle_cutting(e)
        elif self.step == STEP_FROSTING:
            self._handle_frosting(e)

    def _handle_ing(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.btn_back.mask.get_at(e.pos):
                self.gsm.set_state('option_page')
                return
            if self.mix_ready and self.btn_next.mask.get_at(e.pos):
                self.step = STEP_MIX_IT
                return
            mx,my = e.pos
            for ing,mask in self.icon_masks.items():
                if ing not in self.completed and mask.get_at((mx,my)):
                    self.dragging,self.drag_offset = ing,(mx,my)
                    break
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and self.dragging:
            x,y = e.pos
            ing = self.dragging
            self.dragging = None
            if self.bowl_rect.collidepoint(x,y):
                self.completed.add(ing)
                self.play_animation(ing)
                if set(self.ingredients) == self.completed:
                    self.mix_ready = True

    def _handle_mix_it(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.mix_done and self.btn_next.mask.get_at(e.pos):
                self.step = STEP_CUTTING
                return
            if self.blender_btn.mask.get_at(e.pos) and not self.mix_done:
                self.sound.play("cake_mixer")
                self.play_mix_it_animation()
                self.sound.stop("cake_mixer")
                self.mix_done = True

    def _handle_cutting(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.cut_done and self.btn_next.mask.get_at(e.pos):
                self.step = STEP_FROSTING
                return
            if self.knife_btn.mask.get_at(e.pos) and not self.cut_done:
                self.dragging, self.drag_offset = 'knife', e.pos
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and self.dragging == 'knife':
            x, y = e.pos
            self.dragging = None
            if self.cake_rect.collidepoint(x, y):
                self.sound.play("cut_cake")
                self.play_cut_animation()
                self.sound.stop("cut_cake")
                self.cut_done = True

    def _handle_frosting(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            # Next to decoration if frosting done
            if self.frost_done and self.btn_next.mask.get_at(e.pos):
                # ส่งค่า filling (flavor) ไปยัง GameStateManager
                self.gsm.set_flavor(self.current_flavor)  # ส่งค่าสีไส้ที่เลือก
                self.gsm.set_state('decoration')
                return
            # Reset frosting to choose again
            if self.reset_btn.mask.get_at(e.pos):
                self.frost_done = False
                self.current_flavor = None
                return
            # Start dragging piping bag
            if not self.frost_done:
                for flavor, mask in self.piping_masks.items():
                    if mask.get_at(e.pos):
                        self.dragging, self.drag_offset = flavor, e.pos
                        break
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and self.dragging in self.piping_flavors:
            x, y = e.pos
            flavor = self.dragging
            self.dragging = None
            # Apply frosting only when dropped in cake area
            if self.cake_rect.collidepoint(x, y):
                self.sound.play("yam")
                for frame in self.frost_frames[flavor]:
                    self.screen.blit(self.bg, (0,0))
                    self.screen.blit(self.cutting_8, (0,0))
                    self.screen.blit(frame, (0,0))
                    pygame.display.flip()
                    pygame.time.delay(300)
                self.sound.stop("yam")
                self.current_flavor = flavor
                print(f"[Debug] ผู้เล่นเลือกไส้เค้กเป็น: {flavor}")
                self.frost_done = True
                
    def play_animation(self,name):
         # เล่นเสียงตามชื่อของวัตถุดิบที่เลือก
        if name == 'egg':
            self.sound.play("crack_egg")
        elif name == 'sugar' or name == 'baking_flour' or name == 'baking_powder' or name == 'salt' or name == 'butter':
            self.sound.play("dried_food")
        elif name == 'vanilla_extract' or name == 'milk':
            self.sound.play("liquid")

        frames = self.anim_frames[name]
        base   = self._make_snapshot()
        for f in frames:
            self.screen.blit(base,(0,0))
            self.screen.blit(f,(0,0))
            pygame.display.flip()
            pygame.time.delay(300)
        if name not in self.no_persist and frames:
            self.persistent[name] = frames[-1]

        if name in ['egg', 'sugar', 'vanilla_extract', 'milk', 'baking_flour', 'baking_powder', 'butter', 'salt']:
            self.sound.stop(name)

    def play_mix_it_animation(self):
        for f in self.mix_it_frames:
            self.screen.blit(self.bg,(0,0))
            self.screen.blit(self.mix_it_bar,(0,0))
            self.screen.blit(f,(0,0))
            pygame.display.flip()
            pygame.time.delay(300)

    def play_cut_animation(self):
        for f in self.cut_frames:
            self.screen.blit(self.bg,(0,0))
            self.screen.blit(f,(0,0))
            pygame.display.flip()
            pygame.time.delay(300)

    def _make_snapshot(self):
        base = pygame.Surface((self.sw,self.sh),pygame.SRCALPHA)
        base.blit(self.bg,(0,0))
        base.blit(self.bar,(0,0))
        base.blit(self.bowl,(0,0))
        for surf in self.persistent.values(): base.blit(surf,(0,0))
        for ing,btn in self.icon_buttons.items():
            if ing in self.completed:
                glow = self.icon_masks[ing].to_surface(setcolor=(255,255,0,180),unsetcolor=(0,0,0,0))
                base.blit(glow,(0,0))
            base.blit(btn.image,(0,0))
        self.btn_back.draw(base)
        return base

    def exit(self):
        pass
