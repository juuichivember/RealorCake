import pygame

class Button():
    def __init__(self, x, y, image, scale, smooth=True):
        width = image.get_width()
        height = image.get_height()
        if smooth:
            self.image = pygame.transform.smoothscale(
                image, (int(width * scale), int(height * scale)))
        else:
            self.image = pygame.transform.scale(
                image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        return self

    def is_mouse_over(self):
        """เดิม: ใช้ตรวจสอบและจัดการ click-once"""
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action

    def handle_event(self, event):
        """
        เพิ่มเพื่อรองรับโค้ดที่เรียก handle_event(event):
        คืน True เมื่อมี MOUSEBUTTONDOWN ภายในปุ่ม
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


# สำหรับ BakingPage: pixel‐perfect hit testing
class MaskButton:
    def __init__(self, x, y, image, scale=1.0, smooth=True):
        w, h = image.get_size()
        if smooth:
            self.image = pygame.transform.smoothscale(
                image, (int(w * scale), int(h * scale)))
        else:
            self.image = pygame.transform.scale(
                image, (int(w * scale), int(h * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.clicked = False

    def draw(self, surf):
        surf.blit(self.image, self.rect.topleft)

    def is_mouse_over(self):
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx, my):
            rx, ry = mx - self.rect.x, my - self.rect.y
            if self.mask.get_at((rx, ry)):
                if pygame.mouse.get_pressed()[0] and not self.clicked:
                    self.clicked = True
                    return True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return False

    def handle_event(self, event):
        """Pixel-perfect click handling"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self.rect.collidepoint(mx, my):
                rx, ry = mx - self.rect.x, my - self.rect.y
                if self.mask.get_at((rx, ry)):
                    return True
        return False
