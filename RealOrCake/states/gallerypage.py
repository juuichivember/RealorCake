# states/gallerypage.py

import os, pygame
from datetime import datetime
from decoModule import load_image, get_base_path
from button import Button

def blur_surface(surface: pygame.Surface, factor: int = 1) -> pygame.Surface:
    """
    ทำ surface ให้เบลอด้วยการย่อ–ขยาย
    factor ยิ่งมาก ย่อมาก → เบลอมาก
    """
    w, h = surface.get_size()
    # ย่อภาพลง
    small = pygame.transform.smoothscale(surface, (w // factor, h // factor))
    # ขยายกลับขึ้นมา
    return pygame.transform.smoothscale(small, (w, h))

BASE_PATH   = get_base_path()
WHITE       = (255,255,255)
BLACK       = (0,0,0)
RATIO_720p  = 1.5

# layout
COLS, ROWS   = 3, 2
PADDING      = 30
TOP_OFFSET   = 80
ZOOM_FACTOR    = 0.6    # (เหมือนเดิม) สัดส่วนพื้นที่ที่จะ crop ก่อนย่อ
CROP_Y_FACTOR  = 0.7    # 0.5 = ตรงกลาง, 0.7 = เลื่อนลงมา 70% ของระยะว่าง
GRID_LEFT_OFFSET = 20   # เลื่อนขอบซ้ายกริดไปทางขวา 20px
THUMB_SIZE  = (370, 207)
TEXT_HEIGHT  = 30   # พื้นที่สำหรับวันที่ใต้ภาพ
PER_PAGE     = COLS * ROWS


class GalleryPage:
    def __init__(self, display, gsm, sw, sh, sound_manager=None):
        self.display = display
        self.gsm     = gsm
        self.sw, self.sh = sw, sh
        self.sound  = sound_manager

        # background
        self.background = load_image(
            "background","gallery_background.png",
            (self.sw, self.sh)
        )

        # navigation buttons
        self.btn_back  = Button(15, self.sh-100,
                                load_image("button","back_button2.png"),
                                1/RATIO_720p)
        self.btn_left  = Button(self.sw//2-80, self.sh-80,
                                load_image("button","backward-button.png"),
                                1/RATIO_720p)
        self.btn_right = Button(self.sw//2+20, self.sh-80,
                                load_image("button","forward-button.png"),
                                1/RATIO_720p)

        # font สำหรับวันที่
        self.date_font = pygame.font.Font(None, 18)

        # โหลดรูปทั้งหมด
        folder = os.path.join(
            os.path.expanduser("~"),
            "Downloads","RealorCakeGallery"
        )
        os.makedirs(folder, exist_ok=True)
        files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]
        files.sort(reverse=True)

        self.full_images = []
        self.thumbs      = []
        self.dates       = []

        thumb_ratio = THUMB_SIZE[0]/THUMB_SIZE[1]
        for fn in files:
            path = os.path.join(folder, fn)
            full = pygame.image.load(path).convert_alpha()
            fW, fH = full.get_size()

            # 1) center-crop ให้ได้อัตราส่วน THUMB_SIZE
            if fW/fH > thumb_ratio:
                newW, newH = int(fH * thumb_ratio), fH
            else:
                newW, newH = fW, int(fW / thumb_ratio)
            cx, cy = (fW-newW)//2, (fH-newH)//2
            cropped = full.subsurface((cx, cy, newW, newH)).copy()

            # 2) zoom-crop ตรงกลาง แต่เลื่อนลงมา
            w2, h2 = cropped.get_size()
            zw, zh = int(w2 * ZOOM_FACTOR), int(h2 * ZOOM_FACTOR)
            zx = (w2 - zw)//2
            # ใช้ CROP_Y_FACTOR แทน 0.5
            zy = int((h2 - zh) * CROP_Y_FACTOR)
            zoomed = cropped.subsurface((zx, zy, zw, zh)).copy()

            # 3) ย่อภาพ zoomed กลับมาเป็น THUMB_SIZE
            thumb = pygame.transform.smoothscale(zoomed, THUMB_SIZE)
            self.thumbs.append(thumb)
            self.full_images.append(full)

            # เก็บวันที่แก้ไขล่าสุด
            dt = datetime.fromtimestamp(os.path.getmtime(path))
            self.dates.append(dt.strftime("%Y-%m-%d %H:%M"))

        # pagination
        self.page     = 0
        self.max_page = max(0, (len(self.thumbs)-1)//PER_PAGE)

        # full-view state
        self.full_index = None

        # เก็บ rect ของแต่ละ thumbnail (รวมพื้นที่วัน) เพื่อเช็ค click
        self.thumb_rects = []

    def enter(self):
        pass

    def run(self):
        # — full-view mode —
        if self.full_index is not None:
            # 1) วาด background เบลอแทนพื้นดำ
            blurred_bg = blur_surface(self.background, factor=5)
            self.display.blit(blurred_bg, (0, 0))

            # 2) วาดรูปเต็มหน้าจอ
            img = self.full_images[self.full_index]
            w, h = img.get_size()
            maxW, maxH = int(self.sw * 0.8), int(self.sh * 0.8)
            scale = min(maxW / w, maxH / h)
            img_s = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
            r = img_s.get_rect(center=(self.sw // 2, self.sh // 2))

            # 3) วาด glow & border
            glow = pygame.Surface((r.width + 20, r.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow, (255, 255, 255, 100), glow.get_rect())
            self.display.blit(glow, (r.x - 10, r.y - 10))

            pygame.draw.rect(self.display, WHITE,
                             (r.x, r.y, r.width, r.height), width=4)
            # 4) วาดรูป
            self.display.blit(img_s, r)
            return

        # — normal grid mode —
        self.display.blit(self.background, (0,0))
        mx,my = pygame.mouse.get_pos()
        self.thumb_rects.clear()

        start = self.page * PER_PAGE
        for idx in range(PER_PAGE):
            gi = start + idx
            if gi >= len(self.thumbs): break

            row, col = divmod(idx, COLS)
            x = GRID_LEFT_OFFSET + PADDING + col * (THUMB_SIZE[0] + PADDING)
            y = TOP_OFFSET + row * (THUMB_SIZE[1]+TEXT_HEIGHT+PADDING)

            # glow เบื้องต้น (alpha=40)
            glow = pygame.Surface((THUMB_SIZE[0]+12,THUMB_SIZE[1]+12), pygame.SRCALPHA)
            pygame.draw.rect(glow, (255,255,255,100), glow.get_rect())
            self.display.blit(glow, (x-6,y-6))

            # glow เวลา hover (alpha=120)
            rect = pygame.Rect(x,y,*THUMB_SIZE)
            if rect.collidepoint(mx,my):
                hover = pygame.Surface((THUMB_SIZE[0]+16,THUMB_SIZE[1]+16), pygame.SRCALPHA)
                pygame.draw.rect(hover, (255,255,255,150), hover.get_rect())
                self.display.blit(hover, (x-8,y-8))

            # วาด thumbnail
            self.display.blit(self.thumbs[gi], (x,y))

            # วาดวันที่ใต้ภาพ
            date_s = self.date_font.render(self.dates[gi], True, BLACK)
            dx = x + (THUMB_SIZE[0]-date_s.get_width())//2
            dy = y + THUMB_SIZE[1] + 10
            self.display.blit(date_s, (dx, dy))

            # เก็บ rect (รวมวันที่) สำหรับ click detection
            self.thumb_rects.append((gi, pygame.Rect(x, y, THUMB_SIZE[0], THUMB_SIZE[1]+TEXT_HEIGHT)))

        # วาดปุ่ม navigation
        for btn in (self.btn_back, self.btn_left, self.btn_right):
            btn.draw(self.display)

    def handle_events(self, event):
        if event.type!=pygame.MOUSEBUTTONDOWN or event.button!=1:
            return

        mx,my = event.pos

        # ถ้าอยู่ full-view → ออกจาก full-view ทันที
        if self.full_index is not None:
            self.full_index = None
            return

        # ปุ่มเลื่อนไปหน้าเก่า
        if self.btn_left.rect.collidepoint(mx,my) and self.page>0:
            self.page -= 1
            if self.sound: self.sound.play("normal_click")
            return

        # ปุ่มเลื่อนไปหน้าถัดไป
        if self.btn_right.rect.collidepoint(mx,my) and self.page<self.max_page:
            self.page += 1
            if self.sound: self.sound.play("normal_click")
            return

        # ปุ่ม Back
        if self.btn_back.rect.collidepoint(mx,my):
            self.gsm.set_state('start')
            return

        # คลิกที่ thumbnail → full-view
        for gi, rect in self.thumb_rects:
            if rect.collidepoint(mx,my):
                self.full_index = gi
                return

    def exit(self):
        pass
