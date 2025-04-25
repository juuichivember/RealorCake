# states/gallerypage.py

import os
import pygame
from datetime import datetime
from decoModule import load_image, get_base_path
from button import Button

def blur_surface(surface: pygame.Surface, factor: int = 1) -> pygame.Surface:
    w, h = surface.get_size()
    if factor <= 1:
        return surface.copy()
    small = pygame.transform.smoothscale(surface, (w // factor, h // factor))
    return pygame.transform.smoothscale(small, (w, h))

BASE_PATH       = get_base_path()
WHITE           = (255, 255, 255)
BLACK           = (0,   0,   0)
RATIO_720p      = 1.5

# layout constants
COLS, ROWS          = 3, 2
PADDING             = 30
TOP_OFFSET          = 80
GRID_LEFT_OFFSET    = 20
THUMB_SIZE          = (370, 207)
TEXT_HEIGHT         = 30
PER_PAGE            = COLS * ROWS

class GalleryPage:
    def __init__(self, display, gsm, sw, sh, sound_manager=None):
        self.display       = display
        self.gsm           = gsm
        self.sw, self.sh   = sw, sh
        self.sound         = sound_manager

        # โหลด background และปุ่ม
        self.background = load_image("background", "gallery_background.png", (self.sw, self.sh))
        self.btn_back  = Button(15, self.sh - 100,
                                load_image("button","back_button2.png"), 1/RATIO_720p)
        self.btn_left  = Button(self.sw//2 - 80, self.sh - 80,
                                load_image("button","backward-button.png"), 1/RATIO_720p)
        self.btn_right = Button(self.sw//2 + 20, self.sh - 80,
                                load_image("button","forward-button.png"), 1/RATIO_720p)

        self.date_font = pygame.font.Font(None, 18)

        # เตรียม container
        self.full_images = []
        self.thumbs      = []
        self.dates       = []
        self.thumb_rects = []
        self.page        = 0
        self.max_page    = 0
        self.full_index  = None

        # โหลดครั้งแรก
        self.reload_gallery()

    def reload_gallery(self):
        """ โหลดไฟล์ใหม่จากโฟลเดอร์ Downloads/RealorCakeGallery ทุกครั้ง """
        folder = os.path.join(os.path.expanduser("~"), "Downloads", "RealorCakeGallery")
        os.makedirs(folder, exist_ok=True)
        files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]
        files.sort(reverse=True)

        self.full_images.clear()
        self.thumbs.clear()
        self.dates.clear()

        for fn in files:
            path = os.path.join(folder, fn)
            full = pygame.image.load(path).convert_alpha()
            self.full_images.append(full)
            thumb = pygame.transform.smoothscale(full, THUMB_SIZE)
            self.thumbs.append(thumb)
            dt = datetime.fromtimestamp(os.path.getmtime(path))
            self.dates.append(dt.strftime("%Y-%m-%d %H:%M"))

        self.page     = 0
        self.max_page = max(0, (len(self.thumbs) - 1) // PER_PAGE)
        self.full_index = None

    def enter(self):
        # ทุกครั้งที่เข้ามาหน้านี้ ให้ reload รูปและเล่นเพลง
        self.reload_gallery()
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(BASE_PATH, "assets", "Sound", "PhotoPageBackground.mp3"))
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

    def run(self):
        if self.full_index is not None:
            # full-view
            blurred = blur_surface(self.background, factor=5)
            self.display.blit(blurred, (0,0))

            img = self.full_images[self.full_index]
            w, h = img.get_size()
            maxW, maxH = int(self.sw*0.8), int(self.sh*0.8)
            scale = min(maxW/w, maxH/h)
            img_s = pygame.transform.smoothscale(img, (int(w*scale), int(h*scale)))
            r = img_s.get_rect(center=(self.sw//2, self.sh//2))

            glow = pygame.Surface((r.width+20, r.height+20), pygame.SRCALPHA)
            pygame.draw.rect(glow, (255,255,255,100), glow.get_rect())
            self.display.blit(glow, (r.x-10, r.y-10))

            pygame.draw.rect(self.display, WHITE, (r.x, r.y, r.width, r.height), width=4)
            self.display.blit(img_s, r)
            return

        # grid mode
        self.display.blit(self.background, (0,0))
        mx, my = pygame.mouse.get_pos()
        self.thumb_rects.clear()

        start = self.page * PER_PAGE
        for idx in range(PER_PAGE):
            gi = start + idx
            if gi >= len(self.thumbs):
                break

            row, col = divmod(idx, COLS)
            x = GRID_LEFT_OFFSET + PADDING + col * (THUMB_SIZE[0] + PADDING)
            y = TOP_OFFSET + row * (THUMB_SIZE[1] + TEXT_HEIGHT + PADDING)

            glow = pygame.Surface((THUMB_SIZE[0]+12, THUMB_SIZE[1]+12), pygame.SRCALPHA)
            pygame.draw.rect(glow, (255,255,255,100), glow.get_rect())
            self.display.blit(glow, (x-6, y-6))

            rect = pygame.Rect(x, y, *THUMB_SIZE)
            if rect.collidepoint(mx, my):
                hover = pygame.Surface((THUMB_SIZE[0]+16, THUMB_SIZE[1]+16), pygame.SRCALPHA)
                pygame.draw.rect(hover, (255,255,255,150), hover.get_rect())
                self.display.blit(hover, (x-8, y-8))

            self.display.blit(self.thumbs[gi], (x, y))

            date_s = self.date_font.render(self.dates[gi], True, BLACK)
            dx = x + (THUMB_SIZE[0] - date_s.get_width())//2
            dy = y + THUMB_SIZE[1] + 10
            self.display.blit(date_s, (dx, dy))

            self.thumb_rects.append((gi, pygame.Rect(x, y, THUMB_SIZE[0], THUMB_SIZE[1] + TEXT_HEIGHT)))

        for btn in (self.btn_back, self.btn_left, self.btn_right):
            btn.draw(self.display)

    def handle_events(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        if self.full_index is not None:
            self.full_index = None
            return

        if self.btn_back.handle_event(event):
            self.gsm.set_state('start')
            return

        if self.btn_left.handle_event(event) and self.page > 0:
            self.page -= 1
            if self.sound:
                self.sound.play("normal_click")
            return

        if self.btn_right.handle_event(event) and self.page < self.max_page:
            self.page += 1
            if self.sound:
                self.sound.play("normal_click")
            return

        for gi, rect in self.thumb_rects:
            if rect.collidepoint(event.pos):
                self.full_index = gi
                return

    def exit(self):
        pass
