import pygame
from pygame.locals import *

pygame.init()

window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Glass Button")

# Wczytaj obraz przycisku
button_image = pygame.image.load("button.png").convert_alpha()

# Zmniejsz rozmiar przycisku o połowę
button_image = pygame.transform.scale(button_image, (button_image.get_width() // 2, button_image.get_height() // 2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    window.fill((255, 255, 255))

    # Ustaw pozycję i narysuj obraz przycisku na ekranie
    button_rect = button_image.get_rect()
    button_rect.center = (window_width // 2, window_height // 2)
    window.blit(button_image, button_rect)

    pygame.display.flip()

pygame.quit()
