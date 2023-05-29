import pygame
from pygame.locals import *

pygame.init()

# Inicjalizacja ekranu
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Kolor przycisku
button_color = (255, 0, 0)

# Rozmiary i położenie przycisku
button_width, button_height = 200, 100
button_x, button_y = (width - button_width) // 2, (height - button_height) // 2

# Prędkość znikania
fade_speed = 5

# Główna pętla programu
running = True
fade = False
alpha = 255

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                fade = True

    screen.fill((255, 255, 255))

    # Rysowanie przycisku
    button_surface = pygame.Surface((button_width, button_height))
    button_surface.set_alpha(alpha)
    button_surface.fill(button_color)
    screen.blit(button_surface, (button_x, button_y))

    if fade:
        alpha -= fade_speed
        if alpha <= 0:
            fade = False
            alpha = 255

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
