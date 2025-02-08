import pygame
import button

def main():
    pygame.init()

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    pygame.display.set_caption("Namkhing's Cake")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
    clock = pygame.time.Clock()

    homepage = pygame.image.load("Elements/Homepage_bg.png")
    homepage = pygame.transform.smoothscale(homepage, (SCREEN_WIDTH, SCREEN_HEIGHT))

    button_img = pygame.image.load("Elements/button.png").convert_alpha()
    play_button = button.Button(200, 200, button_img, 0.2)
    photo_button = button.Button(200, 300, button_img, 0.2)

    current_page = "homepage"
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if current_page == "homepage":
            screen.blit(homepage, (0, 0))
            play_button.draw(screen)
            photo_button.draw(screen)
            if play_button.IsMouseOver():
                print("Play")
                current_page = "decopage"
            if photo_button.IsMouseOver():
                print("Photo")
        else:
            screen.fill((255,255,255))
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__': main()