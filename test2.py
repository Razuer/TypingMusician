import pygame
pygame.init()

# Ustawienie rozmiaru okna:
size = (700, 500)
screen = pygame.display.set_mode(size)

# Ustawienie tytułu okna:
pygame.display.set_caption("Poruszający się napis")

# Ustawienia kolorów:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ustawienia czcionki i tekstu:
font = pygame.font.Font(None, 36)
text = font.render("Hello, World!", True, WHITE)

# Początkowe położenie tekstu:
text_x = size[0]

# Główna pętla programu:
done = False

while not done:
    # Wydarzenia (event) aplikacji:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Wyczyszczenie ekranu:
    screen.fill(BLACK)

    # Przemieszczenie tekstu o jeden piksel w lewo:
    text_x -= 0.1
    
    # Sprawdzenie, czy tekst w całości zniknął z ekranu:
    if text_x < -200:
        text_x = size[0]

    # Wyświetlenie tekstu na ekranie:
    screen.blit(text, [text_x, 250])

    # Odświeżenie ekranu:
    pygame.display.flip()

# Po zakończeniu pętli:
pygame.quit()
