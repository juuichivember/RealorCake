import pygame

# ข้อความแจ้งเตือน (alert box)

class AlertButton:
    # ปุ่มที่สร้างบน alert box เช่น yes, no
    def __init__(self, x, y, width, height, text, font, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

class Alert:
    # คลาสหลักของ alert  
    def __init__(self, message, font, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.message = message
        self.font = font
        self.ok_button = AlertButton(x + width // 4 - 50, y + height - 60, 100, 40, "Yes", font, (100, 200, 100), (120, 220, 120))
        self.cancel_button = AlertButton(x + 3 * width // 4 - 50, y + height - 60, 100, 40, "No", font, (200, 100, 100), (220, 120, 120))
        self.result = None  # True == OK, False == Cancel

    def draw(self, screen):
        # สำหรับใส่ใน state
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        text_surface = self.font.render(self.message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        self.ok_button.draw(screen)
        self.cancel_button.draw(screen)

    def handle_event(self, event, mouse_pos):
        # สำหรับ run
        if event.type == pygame.MOUSEMOTION:
            self.ok_button.hovered = self.ok_button.is_over(mouse_pos)
            self.cancel_button.hovered = self.cancel_button.is_over(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.ok_button.is_over(mouse_pos):
                self.result = True
                return True # Indicate alert completion
            elif self.cancel_button.is_over(mouse_pos):
                self.result = False
                return True # Indicate alert completion
        return False # Alert is still active