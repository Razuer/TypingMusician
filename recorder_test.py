import pygame

# Inicjalizacja modułu Pygame
pygame.init()

# Ustawienia okna
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pojawianie i znikanie kwadratu")
clock = pygame.time.Clock()
# Kolor kwadratu
square_color = (255, 0, 0)  # Czerwony

# Pobieranie czasów wciśnięcia klawiszy z pliku
times = []
with open("czasy_wcisniecia.txt", "r") as file:
    for line in file:
        time_str = line.strip()
        time = float(time_str)
        times.append(time)

pygame.mixer.music.load("sounds\dream-land.mp3")
pygame.mixer.music.play()

# Pętla główna programu
running = True
current_index = 0  # Aktualny indeks czasu wciśnięcia klawisza
while running:
    # Sprawdzanie zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pobieranie aktualnego czasu
    current_time = pygame.time.get_ticks()
    screen.fill((0, 0, 0))
    # Wyświetlanie kwadratu, jeśli jest czas do jego pojawienia się
    if current_index < len(times) and current_time >= times[current_index]:
        screen.fill((0, 0, 0))  # Czyszczenie ekranu
        pygame.draw.rect(screen, square_color, pygame.Rect(100, 100, 100, 100))  # Rysowanie kwadratu
        current_index += 1
    
    clock.tick(60)
    pygame.display.update()

# Wyłączanie modułu Pygame
pygame.quit()
