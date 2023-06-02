import pygame
import random
from sparks_sprite import Sparks

# Inicjalizacja Pygame
pygame.init()

# Ustalenie wymiarów ekranu
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animacja Iskier")

background_image = pygame.image.load("graphics/city2.jpg")
background_image = pygame.transform.scale(background_image, (width, height))

# Kolor tła
background_color = (0, 0, 0)

# Główna pętla programu
running = True
clock = pygame.time.Clock()

sparks = Sparks(True)

while running:
    screen.fill(background_color)
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Tworzenie eksplozji iskier po wciśnięciu przycisku SPACJA
                explosion_size = 50
                explosion_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                explosion_x = random.randint(100, width - 100)
                explosion_y = random.randint(100, height - 100)
                sparks.create_sparks(explosion_x, explosion_y, explosion_size, explosion_color)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            explosion_size = 50
            explosion_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            explosion_x, explosion_y = pygame.mouse.get_pos()
            sparks.create_sparks(explosion_x, explosion_y, explosion_size, explosion_color)

    # Aktualizowanie i rysowanie iskier
    sparks.update()
    sparks.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# Zakończenie Pygame
pygame.quit()
