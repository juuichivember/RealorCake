import pygame

class LetterTextBox():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font('font/nura-wat-thin.ttf', 36) #http://nurarada.lnwshop.com/product/329/ฟอนต์นูร่าหวัด-โหลดฟรีที่รายละเอียดสินค้า
        self.text = "To: "
        self.lines = [self.text]
        self.text_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.border_color = (255, 255, 255)
        self.border_width = 1
        self.active = False
        self.max_width = width - 10
        self.delete_pressed = False
        self.delete_timer = 0
        self.delete_delay = 200
        self.delete_repeat_delay = 50
        self.max_height = height - 10 


    def handle_event(self, event):
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos):
            if mouse[0]:
                self.active = True
                cursor = pygame.cursors.compile(pygame.cursors.textmarker_strings)
                pygame.mouse.set_cursor((8, 16), (0, 0), *cursor)
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.rect.collidepoint(mouse_pos):
            self.active = False
            pygame.mouse.set_cursor(pygame.cursors.arrow)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.lines.append('')
                    total_height = sum(self.font.size(line)[1] + 25 for line in self.lines)
                    if total_height + self.font.size(' ')[1] + 25 <= self.max_height:
                        self.lines.append('')
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.delete_pressed = True
                    self.delete_timer = pygame.time.get_ticks() + self.delete_delay
                    self.delete_text()
                else:
                    self.lines[-1] += event.unicode
                    if self.font.size(self.lines[-1])[0] > self.max_width:
                        last_space = self.lines[-1].rfind(' ')
                        if last_space != -1:
                            self.lines.append(self.lines[-1][last_space + 1:])
                            self.lines[-1] = self.lines[-1][:last_space]
                        else:
                            self.lines.append(self.lines[-1][-1])
                            self.lines[-1] = self.lines[-1][:-1]
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                self.delete_pressed = False

    def delete_text(self):
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            if self.lines[-1]:
                self.lines[-1] = self.lines[-1][:-1]
            elif len(self.lines) > 1:
                self.lines.pop()
        elif pygame.key.get_pressed()[pygame.K_DELETE]:
            if self.lines[-1]:
                self.lines[-1] = self.lines[-1][1:]
            elif len(self.lines) > 1:
                self.lines.pop()

    def update(self):
        if self.delete_pressed and pygame.time.get_ticks() >= self.delete_timer:
            self.delete_text()
            self.delete_timer = pygame.time.get_ticks() + self.delete_repeat_delay

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)

        y_offset = 5
        line_spacing = 25
        for line in self.lines:
            text_surface = self.font.render(line, True, self.text_color)
            if self.rect.y + y_offset + text_surface.get_height() > self.rect.y + self.max_height:
                break
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + y_offset))
            y_offset += line_spacing

        # คำนวณความสูงทั้งหมด
        total_height = sum(self.font.size(line)[1] + 25 for line in self.lines)