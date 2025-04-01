import pygame, os
from screen import change_ratio_1080_to_720 as change
from decoModule import load_image, get_base_path

DURATION = 10

# ตัวจับเวลาใน Random Cake state นับจาก 10 - 1

class Timer():
    def __init__(self, display):
        # เตรียม variables ต่างๆ

        self.display = display
        self.duration = DURATION * 1000  # convert seconds to milliseconds
        self.start_time = None
        self.active = False
        self.images = {}
        base_path = get_base_path()

        self.clock_img = load_image(folder="timer", filename="clock.png")
        self.clock_img = pygame.transform.smoothscale(self.clock_img, (change(self.clock_img.get_width()), change(self.clock_img.get_height())))
        self.clock_rect = self.clock_img.get_rect()
        self.clock_rect.topleft = (800, 74)

        # load ทุกรูปเตรียมไว้ เวลาเรียก จะใช้เลข index
        for i in range(1, DURATION + 1):
            index = i
            filename = f't_{index}.png'
            self.images[index] = load_image(folder="timer", filename=filename)
            self.images[index] = pygame.transform.smoothscale(self.images[index], (change(self.images[index].get_width()), change(self.images[index].get_height())))

    def get_time_left(self):
        # ดูเวลาที่เหลืออยู่ โดยจะมีการจับเวลาโดยใช้ get_ticks ลบกับเวลาเริ่มต้นหรือ start time และได้รู้ว่าในขณะนั้น
        # คือ elapsed_time เท่าไหร่ จากนั้นเอามาลบกับ 10 วิ และจะได้ว่าเหลือเวลาเท่าไหร่
        # ตัวนี้คือตัวที่จะรู้ว่าจะ display เลขอะไรในวินาทีนั้น

        if not self.active or self.start_time is None:
            return DURATION
        # round ให้เป็นเลขหลัก 1000
        elapsed_time = round(pygame.time.get_ticks() - self.start_time, -3)
        time_left = max(0, self.duration - elapsed_time)
        return time_left // 1000
    
    def is_finished(self):
        # check if จับเวลาเสร็จหรือยัง

        if not self.active:
            return False
        return self.get_time_left() <= 0
    
    def get_current_image(self):
        # เรียกรูปตามเวลาที่เหลืออยู่ โดยดูจาก index

        time_left = self.get_time_left()
        return self.images.get(time_left)
    
    def start(self):
        # เมื่อเริ่ม Random State จะเรียก start เพื่อเก็บ ticks ของเวลาเริ่มต้น

        self.start_time = pygame.time.get_ticks()
        self.active = True

    def reset(self):
        # รีเซ็ทเวลา

        self.start_time = None
        self.active = False

    def render(self):
        # display รูปนาฬิกา

        self.active = True
        self.display.blit(self.clock_img , (self.clock_rect.x, self.clock_rect.y))

    def get_pos(self):
        # set x, y ที่ควร display นาฬิกา

        offset_x = 36
        offset_y = 30
        digit_x = self.clock_rect.centerx - offset_x
        digit_y = self.clock_rect.centery - offset_y
        return (digit_x, digit_y)