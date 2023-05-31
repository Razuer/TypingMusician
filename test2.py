import pygame
import numpy as np

# Inicjalizacja biblioteki Pygame
pygame.init()

# Ustalenie rozmiaru okna
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Kwadrat w rytm muzyki")

# Inicjalizacja dźwięku
pygame.mixer.init()

# Załadowanie pliku dźwiękowego
sound_file = "songs\sexy-fashion-beats-simulate-11176.wav"
sound = pygame.mixer.Sound(sound_file)

# Pobranie informacji o częstotliwości próbkowania pliku dźwiękowego
sample_rate = pygame.mixer.get_init()[0]

# Odtwarzanie dźwięku w pętli
sound.play(-1)

# Główna pętla programu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pobranie próbek dźwięku
    samples = pygame.sndarray.array(sound.get_buffer())

    # Obliczenie średniej wartości amplitudy dźwięku
    amplitude = np.mean(np.abs(samples))

    # Obliczenie rozmiaru kwadratu w zależności od amplitudy
    square_size = int(amplitude * 200)

    # Wyczyszczenie ekranu
    window.fill((0, 0, 0))

    # Wyświetlenie kwadratu na środku ekranu
    square_x = (window_width - square_size) // 2
    square_y = (window_height - square_size) // 2
    pygame.draw.rect(window, (255, 255, 255), (square_x, square_y, square_size, square_size))

    # Zaktualizowanie ekranu
    pygame.display.flip()

# Zakończenie programu
pygame.quit()
