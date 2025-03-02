import pygame

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