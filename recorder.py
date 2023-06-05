import os
import random
from tkinter import filedialog
import tkinter
import pygame

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.Font('fonts/font.ttf', size)
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect(center = (x, y))
    screen.blit(text_surface, text_rect)

def main(song_path):
    # Inicjalizacja modułu Pygame
    pygame.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 400, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Recorder")

    from sprites import Sparks

    clock = pygame.time.Clock()
    sparks = Sparks(WIDTH, HEIGHT, False)

    # Odtwarzanie muzyki
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.set_endevent

    MUSIC_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(MUSIC_END)

    # Tworzenie pustej listy, do której będziemy dodawać czasy wciśnięcia klawiszy
    times = []

    delay = 3000
    play_music = False
    running = True
    start_time = pygame.time.get_ticks()
    
    while running:
        clock.tick(60)
        screen.fill((22, 22, 22))
        draw_text(screen, "Press ESC to save earlier", 10, (255,255,255), 200, 10)
        draw_text(screen, "Keep pressing keys in rhythm to save timing!", 10, (255,255,255), 200, 390)
        # Pobieranie aktualnego czasu
        current_time = pygame.time.get_ticks()

        if not play_music and current_time >= delay:
            pygame.mixer.music.play()
            play_music = True
        
        # Sprawdzanie wciśnięcia klawiszy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif play_music:
                    times.append(current_time-delay)
                    explosion_x = random.randint(100, WIDTH - 100)
                    explosion_y = random.randint(100, HEIGHT - 100)
                    sparks.create_sparks(explosion_x, explosion_y)
            elif event.type == MUSIC_END:
                pygame.mixer.music.stop()
                running = False

        sparks.draw(screen)
        sparks.update()

        pygame.display.update()           

    # Zapisywanie czasów wciśnięcia klawiszy do pliku
    output_file = f"{os.path.splitext(song_path)[0]}.txt"
    with open(output_file, "w") as file:
        for t in times:
            file.write(str(t) + "\n")

    print(f"Pomyślnie zapisano wyniki w {output_file}")

    pygame.quit()

if __name__ == "__main__":
    root = tkinter.Tk()

    root.withdraw()

    song_path = filedialog.askopenfilename(initialdir="songs", filetypes=[("MP3 and WAV files", "*.mp3;*.wav"),("MP3 files", "*.mp3"), ("WAV files", "*.wav")])

    if song_path:
        main(song_path)
    else:
        print("File was not selected")
    
