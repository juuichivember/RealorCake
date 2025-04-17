import pygame

# สร้าง Object ปุ่มกด

class Button():
    def __init__(self, x, y, image, scale, smooth=True):
        # constructor
        width = image.get_width()
        height = image.get_height()
        if smooth:
            self.image = pygame.transform.smoothscale(image, (int(width * scale), int(height * scale)))
        else:
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False # unclick state

    def draw(self, surface):
        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y)) # surface == screen

        return self
    
    def is_mouse_over(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # if left clicked
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0: # if right clicked
            self.clicked = False

        return action

#สำหรับ bakingPage ที่ asset เต็มจอ ต้องการ pixel‑perfect hit    
class MaskButton:
    def __init__(self, x, y, image, scale=1.0, smooth=True):
        # สร้าง surface ขนาดตาม scale
        w, h = image.get_size()
        if smooth:
            self.image = pygame.transform.smoothscale(image, (int(w*scale), int(h*scale)))
        else:
            self.image = pygame.transform.scale(image, (int(w*scale), int(h*scale)))
        # rect สำหรับการวาด
        self.rect = self.image.get_rect(topleft=(x, y))
        # mask สร้างจาก surface
        self.mask = pygame.mask.from_surface(self.image)
        # สถานะกดค้าง
        self.clicked = False

    def draw(self, surf):
        surf.blit(self.image, self.rect)
    
    def is_mouse_over(self):
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx, my):
            # แปลงเป็นพิกัดภายในภาพ
            rx, ry = mx - self.rect.x, my - self.rect.y
            # ถ้า pixel ตรงนี้ทึบ (alpha>0)
            if self.mask.get_at((rx, ry)):
                if pygame.mouse.get_pressed()[0] and not self.clicked:
                    self.clicked = True
                    return True
        # reset เมื่อปล่อย
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return False