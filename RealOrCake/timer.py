import pygame
from screen import change_ratio_1080_to_720 as change

DURATION = 10

class Timer():
    def __init__(self, display):
        self.display = display
        self.duration = DURATION * 1000  # convert seconds to milliseconds
        self.start_time = None
        self.active = False
        self.images = {}

        self.clock_img = pygame.image.load("Elements/timer/clock.png")
        self.clock_img = pygame.transform.smoothscale(self.clock_img, (change(self.clock_img.get_width()), change(self.clock_img.get_height())))
        self.clock_rect = self.clock_img.get_rect()
        self.clock_rect.topleft = (800, 74)

        for i in range(1, DURATION + 1):
            index = i
            filename = f'Elements/timer/t_{index}.png'
            self.images[index] = pygame.image.load(filename).convert_alpha()
            self.images[index] = pygame.transform.smoothscale(self.images[index], (change(self.images[index].get_width()), change(self.images[index].get_height())))

    def get_time_left(self):
        if not self.active or self.start_time is None:
            return DURATION
        elapsed_time = round(pygame.time.get_ticks() - self.start_time, -3)
        time_left = max(0, self.duration - elapsed_time)
        return time_left // 1000
    
    def is_finished(self):
        if not self.active:
            return False
        return self.get_time_left() <= 0
    
    def get_current_image(self):
        time_left = self.get_time_left()
        return self.images.get(time_left)
    
    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.active = True

    def reset(self):
        self.start_time = None
        self.active = False

    def render(self):
        self.active = True
        self.display.blit(self.clock_img , (self.clock_rect.x, self.clock_rect.y))

    def get_pos(self):
        offset_x = 36
        offset_y = 30
        digit_x = self.clock_rect.centerx - offset_x
        digit_y = self.clock_rect.centery - offset_y
        return (digit_x, digit_y)