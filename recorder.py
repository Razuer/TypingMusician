import os
import random
from tkinter import filedialog
import tkinter
import pygame
import time
from sparks import Sparks

def main(song_path):
    # Inicjalizacja modułu Pygame
    pygame.init()

    WIDTH, HEIGHT = 400, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Recorder")

    clock = pygame.time.Clock()
    sparks = Sparks(screen, False)

    # Odtwarzanie muzyki
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    # Tworzenie pustej listy, do której będziemy dodawać czasy wciśnięcia klawiszy
    times = []

    # Pętla główna programu
    running = True
    while running:
        clock.tick(60)
        screen.fill((22, 22, 22))
        # Pobieranie aktualnego czasu
        current_time = pygame.time.get_ticks()

        # Sprawdzanie wciśnięcia klawiszy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            elif event.type == pygame.KEYDOWN:
                # Dodawanie aktualnego czasu do listy
                times.append(current_time)
                # print(current_time)
                explosion_size = 40
                explosion_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                explosion_x = random.randint(100, WIDTH - 100)
                explosion_y = random.randint(100, HEIGHT - 100)
                sparks.create_sparks(explosion_x, explosion_y, explosion_size, explosion_color)

        sparks.update_sparks()
        pygame.display.update()

        # Warunek zakończenia programu - np. po wciśnięciu klawisza ESC
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    # Zapisywanie czasów wciśnięcia klawiszy do pliku
    with open(f"songs/txt/{os.path.basename(song_path).split('.')[0]}.txt", "w") as file:
        for t in times:
            file.write(str(t) + "\n")

    # Zatrzymywanie odtwarzania muzyki
    pygame.mixer.music.stop()

    # Wyłączanie modułu Pygame
    pygame.quit()

if __name__ == "__main__":

    # Create the main Tkinter window
    root = tkinter.Tk()

    # Hide the main window since we don't need it
    root.withdraw()
    # Get the current working directory
    current_directory = os.getcwd()

    # Display a file dialog for selecting MIDI files in the current directory
    song_path = filedialog.askopenfilename(initialdir="songs/mp3", filetypes=[("MP3 files", "*.mp3")])

    main(song_path)
