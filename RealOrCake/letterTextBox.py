# letterTextBox.py
import pygame, os
from decoModule import get_base_path

BLINK_INTERVAL      = 500  # ms เคอร์เซอร์กะพริบ
BS_INITIAL_DELAY    = 400  # ms หน่วงก่อนเริ่มลบซ้ำ
BS_REPEAT_DELAY     = 50   # ms ระยะห่างระหว่างลบแต่ละครั้ง

class LetterTextBox:
    def __init__(self, x, y, width, height):
        # Rect และ Font
        self.rect = pygame.Rect(x, y, width, height)
        base = get_base_path()
        self.font = pygame.font.Font(
            os.path.join(base, "assets", "font", "nura-wat-thin.ttf"), 36
        )

        # เนื้อหาเริ่มต้น
        self.lines  = ["To: "]
        self.cursor = [0, len(self.lines[0])]  # [line_index, char_index]

        # สี ขอบ
        self.text_color   = (0, 0, 0)
        self.border_color = (255, 255, 255, 0)
        self.border_w     = 2

        # สถานะ focus
        self.active = False

        # Surface โปร่งใส สำหรับวาดทั้งหมด
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # สั่ง pygame ให้ส่ง TEXTINPUT events
        pygame.key.start_text_input()

        # เคอร์เซอร์กะพริบ
        self.last_blink     = pygame.time.get_ticks()
        self.cursor_visible = True

        # การลบซ้ำ
        self.bs_held      = False
        self.del_held     = False
        self.bs_next_time = 0
        self.del_next_time= 0

        # ขอบเขตข้อความ
        self.max_w = width  - 10
        self.max_h = height - 10

    def handle_event(self, event):
        mx, my = pygame.mouse.get_pos()

        # เปิด/ปิด focus ด้วยเม้าส์
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mx, my):
                self.active = True
                curs = pygame.cursors.compile(pygame.cursors.textmarker_strings)
                pygame.mouse.set_cursor((8,16),(0,0),*curs)
            else:
                self.active = False
                pygame.mouse.set_cursor(*pygame.cursors.arrow)

        if not self.active:
            return

        # KEYDOWN: ลูกศร, enter, initial backspace/delete
        if event.type == pygame.KEYDOWN:
            li, ci = self.cursor
            line = self.lines[li]

            if event.key == pygame.K_LEFT:
                if ci>0:
                    ci -= 1
                elif li>0:
                    li -= 1
                    ci = len(self.lines[li])

            elif event.key == pygame.K_RIGHT:
                if ci < len(line):
                    ci += 1
                elif li < len(self.lines)-1:
                    li += 1
                    ci = 0

            elif event.key == pygame.K_UP:
                if li>0:
                    li -= 1
                    ci = min(ci, len(self.lines[li]))

            elif event.key == pygame.K_DOWN:
                if li < len(self.lines)-1:
                    li += 1
                    ci = min(ci, len(self.lines[li]))

            elif event.key == pygame.K_RETURN:
                # แยกบรรทัด
                rest = line[ci:]
                self.lines[li] = line[:ci]
                self.lines.insert(li+1, rest)
                li += 1
                ci  = 0

            elif event.key == pygame.K_BACKSPACE:
                # initial delete
                if ci>0:
                    self.lines[li] = line[:ci-1] + line[ci:]
                    ci -= 1
                elif li>0:
                    prev = self.lines[li-1]
                    ci = len(prev)
                    self.lines[li-1] = prev + line
                    self.lines.pop(li)
                    li -= 1

                # ตั้ง flag ลบค้าง
                self.bs_held      = True
                self.bs_next_time = pygame.time.get_ticks() + BS_INITIAL_DELAY

            elif event.key == pygame.K_DELETE:
                # initial delete
                if ci < len(line):
                    self.lines[li] = line[:ci] + line[ci+1:]
                elif li < len(self.lines)-1:
                    self.lines[li] += self.lines[li+1]
                    self.lines.pop(li+1)

                # ตั้ง flag delete ค้าง
                self.del_held       = True
                self.del_next_time  = pygame.time.get_ticks() + BS_INITIAL_DELAY

            self.cursor = [li, ci]
            self.cursor_visible = True
            self.last_blink     = pygame.time.get_ticks()

        # KEYUP: หยุดลบซ้ำ
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.bs_held = False
            elif event.key == pygame.K_DELETE:
                self.del_held = False

        # TEXTINPUT: รับตัวอักษรจริง
        elif event.type == pygame.TEXTINPUT:
            ch = event.text
            if ch:
                li, ci = self.cursor
                line = self.lines[li]
                # แทรก ch
                self.lines[li] = line[:ci] + ch + line[ci:]
                ci += len(ch)

                # auto-wrap
                if self.font.size(self.lines[li])[0] > self.max_w:
                    sp = self.lines[li].rfind(' ')
                    if sp >= 0:
                        tail = self.lines[li][sp+1:]
                        self.lines[li] = self.lines[li][:sp]
                        self.lines.insert(li+1, tail)
                        li += 1
                        ci  = len(tail)
                    else:
                        tail = self.lines[li][-1]
                        self.lines[li] = self.lines[li][:-1]
                        self.lines.insert(li+1, tail)
                        li += 1
                        ci  = 1

                self.cursor = [li, ci]
                self.cursor_visible = True
                self.last_blink = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()

        # เคอร์เซอร์กะพริบ
        if now - self.last_blink >= BLINK_INTERVAL:
            self.cursor_visible = not self.cursor_visible
            self.last_blink     = now

        # ลบซ้ำถ้ากดค้าง Backspace
        if self.bs_held and now >= self.bs_next_time:
            li, ci = self.cursor
            line = self.lines[li]
            if ci>0:
                self.lines[li] = line[:ci-1] + line[ci:]
                ci -= 1
            elif li>0:
                prev = self.lines[li-1]
                ci = len(prev)
                self.lines[li-1] = prev + line
                self.lines.pop(li)
                li -= 1

            # รอบต่อไป
            self.bs_next_time = now + BS_REPEAT_DELAY
            self.cursor       = [li, ci]

        # ลบซ้ำถ้ากดค้าง Delete
        if self.del_held and now >= self.del_next_time:
            li, ci = self.cursor
            line = self.lines[li]
            if ci < len(line):
                self.lines[li] = line[:ci] + line[ci+1:]
            elif li < len(self.lines)-1:
                self.lines[li] += self.lines[li+1]
                self.lines.pop(li+1)

            self.del_next_time = now + BS_REPEAT_DELAY

    def draw(self, screen):
        # ล้าง surface
        self.surface.fill((0,0,0,0))

        # วาดขอบ
        pygame.draw.rect(
            self.surface,
            self.border_color,
            self.surface.get_rect(),
            width=self.border_w,
            border_radius=4
        )

        # วาดข้อความ
        y       = 5
        line_h  = self.font.get_height() + 5
        for line in self.lines:
            if y + self.font.get_height() > self.max_h:
                break
            ts = self.font.render(line, True, self.text_color)
            self.surface.blit(ts, (5, y))
            y += line_h

        # วาด cursor ถ้า focus และ visible
        if self.active and self.cursor_visible:
            li, ci = self.cursor
            pre = self.lines[li][:ci]
            cx = self.font.size(pre)[0] + 5
            cy = li * line_h + 5
            pygame.draw.line(
                self.surface, self.text_color,
                (cx, cy), (cx, cy + self.font.get_height()), 2
            )

        # Blit ขึ้นหน้าจอ
        screen.blit(self.surface, (self.rect.x, self.rect.y))
