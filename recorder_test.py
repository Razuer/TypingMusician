import pygame
import random
import os
import sounddevice as sd
import soundfile as sf

def play_wav(file_path):
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)

def run_test(file_path):
    # Inicjalizacja modułu Pygame
    pygame.init()

    # Ustawienia okna
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Rhythm test")
    clock = pygame.time.Clock()

    # Pobieranie czasów rytmów z pliku
    times = []
    with open(f"{os.path.splitext(file_path)[0]}.txt", "r") as file:
        for line in file:
            time_str = line.strip()
            time = float(time_str)
            times.append(time)
    
    play_wav(file_path)

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
            screen.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))  # Czyszczenie ekranu
            current_index += 1
        
        clock.tick(60)
        pygame.display.update()

    # Wyłączanie modułu Pygame
    pygame.quit()

file_path = 'songs/wav/fashion_beats.wav'
run_test(file_path)