import os
import sys
import pygame
import random
import csv
from pygame_textinput import TextInputManager, TextInputVisualizer

from settings import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

menu_image = pygame.image.load(MENU_BG).convert()
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))

background_image = pygame.image.load(GAME_BG).convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

savescore_image = pygame.image.load('graphics/Background/savescore.png').convert_alpha()
savescore_image = pygame.transform.scale_by(savescore_image, 1.4)
savescore_image.set_alpha(200)

stripe_image = pygame.image.load(STRIPE).convert_alpha()
stripe_image = pygame.transform.scale(stripe_image, (WIDTH, HEIGHT))
stripe_image.set_alpha(200)

from sprites import Key, Button, Aim, Text, Sparks

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(FONT, size)
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect(center = (x, y))
    screen.blit(text_surface, text_rect)

def display_score(score, fps):
    font = pygame.font.Font(FONT, 20)

    text = font.render(str(score), False, (255, 255, 255))
    text_rect = text.get_rect(topright=(WIDTH - 10, 10))

    reaction_text = font.render("FPS: {:.3f}".format(fps), False, (255, 255, 255))
    reaction_text_rect = reaction_text.get_rect(topleft=(10, 10))

    screen.blit(reaction_text, reaction_text_rect)
    screen.blit(text, text_rect)

def leaderboard():
    running = True
    clock = pygame.time.Clock()
    sparks = Sparks(WIDTH, HEIGHT, True)
    SPARKS_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500))
    
    button_group = pygame.sprite.Group()
    but1 = Button(screen, "Return", WIDTH // 2 , HEIGHT // 2 + 180, 300, 50, GRAY, WHITE, BLACK)
    button_group.add(but1)

    while running:
        clock.tick(60)
        screen.blit(menu_image, (0, 0))
        current_time = pygame.time.get_ticks()

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('songs/mp3/dream-land.mp3')
            pygame.mixer.music.play()

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == SPARKS_EVENT:
                sparks.create_sparks(random.randint(0, WIDTH), random.randint(0, HEIGHT - 50))
                pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500)) # Wywoływanie co losową liczbę milisekund
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                explosion_x, explosion_y = pygame.mouse.get_pos()
                sparks.create_sparks(explosion_x, explosion_y)

                if but1.checkForInput():
                    main_menu()

        sparks.draw(screen)
        sparks.update()

        button_group.draw(screen)
        button_group.update()

        draw_text("Leaderboard", 40, WHITE, WIDTH//2, 60)
        draw_text("EASY", 30, WHITE, WIDTH//2 - 300, 150)
        draw_text("MEDIUM", 30, WHITE, WIDTH//2, 150)
        draw_text("HARD", 30, WHITE, WIDTH//2 + 300, 150)

        pygame.draw.line(screen, WHITE, (350, 130), (350, 430), 2)
        pygame.draw.line(screen, WHITE, (650, 130), (650, 430), 2)
        
        pygame.display.update()

def start_game(song_path = None):
    key_timings = None
    if song_path:
        with open(f"{os.path.splitext(song_path)[0]}.txt", "r") as file:
            # Odczytanie linii z pliku i usunięcie znaków nowej linii
            key_timings = [int(line.strip()) for line in file.readlines()]
            pygame.mixer.fadeout(1000)

            pygame.mixer.music.load(song_path)
            zen = False
    else:
        pygame.mixer.music.load("songs/wav/hes-pirate.wav")
        key_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(key_timer, random.randint(500, 1800))
        zen = True

    end_timer = pygame.USEREVENT + 3
    savescore_timer = pygame.USEREVENT + 4
    pygame.time.set_timer(savescore_timer, 1000)

    clock = pygame.time.Clock()
    sparks = Sparks(WIDTH, HEIGHT, False)
    delayed_sparks = []
    destroy_sparks = Sparks(WIDTH, HEIGHT, False)
    keys_group = pygame.sprite.Group()
    aim_group = pygame.sprite.GroupSingle()
    texts_group = pygame.sprite.Group()
    aim = Aim(keys_group)
    aim_group.add(aim)

    score = 0
    play_music = False
    
    start_time = pygame.time.get_ticks()
    timerSet = False
    running = True
    while running:
        current_time = pygame.time.get_ticks() - start_time

        if not play_music and current_time >= DELAY:
            if zen: pygame.mixer.music.play(-1)
            else: pygame.mixer.music.play()

            play_music = True

        colided: Key = pygame.sprite.spritecollide(aim, keys_group, False)
        pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            elif event.type == end_timer:
                save_score(score, song_path)
            elif event.type == pygame.KEYDOWN :
                pressed = True
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                elif event.unicode.isalpha() and colided and event.unicode.upper() == colided[0].key:                    
                    destroy_sparks.create_sparks(aim.rect.centerx, aim.rect.centery, 90)
        
                    dist = abs(aim.rect.centerx - colided[0].rect.centerx)
                    if dist < 12:
                        texts_group.add(Text("PERFECT!", 40, CYAN, 500, 150, 1000, current_time))
                        texts_group.add(Text("+10", 20, CYAN, random.randint(190, 250), random.randint(270, 330), 700, current_time))
                        score += 10
                    else : 
                        texts_group.add(Text("GOOD!", 35, WHITE, 500, 150, 1000, current_time))
                        texts_group.add(Text("+5", 20, WHITE, random.randint(190, 250), random.randint(270, 330), 700, current_time))
                        score += 5
                    
                    colided[0].is_alive = False
        
            elif zen and event.type == key_timer:
                delayed_sparks.append(current_time+DELAY)
                keys_group.add(Key(screen, current_time, KEY_SPEED))
                pygame.time.set_timer(key_timer, random.randint(300, 1000))

        if key_timings and key_timings[0] <= current_time:
            delayed_sparks.append(current_time+DELAY)
            keys_group.add(Key(screen, current_time, KEY_SPEED))
            key_timings.pop(0)

        if delayed_sparks and delayed_sparks[0] <= current_time:
            sparks.create_sparks(random.randint(0, WIDTH), random.randint(0, HEIGHT - 50))
            delayed_sparks.pop(0)

        screen.blit(background_image, (0, 0))

        sparks.draw(screen)
        sparks.update()
    
        screen.blit(stripe_image, (0,13))
        
        display_score(score, clock.get_fps())

        keys_group.draw(screen)
        keys_group.update((current_time) / 1000)

        destroy_sparks.draw(screen)
        destroy_sparks.update()

        aim_group.draw(screen)
        aim_group.update(pressed)

        texts_group.draw(screen)
        texts_group.update(current_time)

        pygame.display.update()
        clock.tick(FPS)

        if not pygame.mixer.music.get_busy() and play_music and not timerSet:
            pygame.time.set_timer(end_timer, 1800)
            timerSet = True

    pygame.mixer.music.fadeout(1500)
        
def save_score(score, song_path):
    clock = pygame.time.Clock()
    buttons_group = pygame.sprite.Group()
    but1 = Button(screen, "Save score", 500, 400, 300, 50, CYAN, WHITE, BLACK)
    but2 = Button(screen, "Exit", 500, 460, 300, 50, CYAN, WHITE, BLACK)
    buttons_group.add(but1, but2)

    pygame.mixer.music.load(song_path)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    font = pygame.font.Font(FONT, 40)
    manager = TextInputManager(validator = lambda input: len(input) <= 15)
    textinput = TextInputVisualizer(manager=manager, font_object=font, font_color=BLACK)

    input_surface = pygame.Surface((500, 60))
    input_surface.fill((255, 255, 255))  # Biały kolor prostokąta
    input_rect = input_surface.get_rect(center=(WIDTH/2, HEIGHT/2))

    
    def save_it(player_name):
        song = ''
        if song_path == PERFECT:
            song = "PERFECT"
        elif song_path == DREAMLAND:
            song = 'DREAMLAND'
        
        # Dodaj wynik do pliku CSV
        with open(SCORES_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([player_name, score, song])
        
        # Posortuj zawartość pliku CSV i zapisz ją z powrotem
        with open(SCORES_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            sorted_rows = sorted(reader, key=lambda row: (row[2], int(row[1]), row[0]))
        
        with open(SCORES_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(sorted_rows)    

    saved = False
    if score < 100:
        congrats = random.choice(['MEH...', 'IMPRESSIVE... NOT', 'STELLAR EFFORT.', 'KEEP PRACTICING!'])
    else:
        congrats = random.choice(['GREAT!', 'AMAZING!', 'AWESOME!', 'WHAT A PRO!'])
    pygame.key.set_repeat(200, 25)
    while True:
                screen.blit(background_image, (0, 0))
                screen.blit(savescore_image, savescore_image.get_rect(center=(500, 300)))
                
                draw_text(congrats, 45, WHITE, 500, 150)
                draw_text(f"Your score: {score}", 30, WHITE, 500, 200)
                draw_text("Enter your nick:", 20, WHITE, input_rect.midtop[0], input_rect.midtop[1]-15)
                buttons_group.draw(screen)
                buttons_group.update()

                events = pygame.event.get()
                
                screen.blit(input_surface, input_rect)

                textinput.update(events)
                screen.blit(textinput.surface, (input_rect.x+15, input_rect.y+5))

                if(len(textinput.value) > 0) and not saved : but1.active = True
                else: but1.active = False

                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if but1.checkForInput() and not saved:
                            print('but1')
                            saved = True
                            save_it(textinput.value)
                        if but2.checkForInput():
                            pygame.mixer.music.fadeout(1000)
                            level_select()
                pygame.display.update()
                clock.tick(FPS)

def level_select():
    running = True
    clock = pygame.time.Clock()
    sparks = Sparks(WIDTH, HEIGHT, True)
    SPARKS_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500))
    
    but1 = Button(screen, "He's a Pirate! - HARD", WIDTH // 2 , HEIGHT // 2 - 200, 440, 50, GRAY, WHITE, BLACK)
    but2 = Button(screen, "MEDIUM", WIDTH // 2 , HEIGHT // 2 - 120, 440, 50, GRAY, WHITE, BLACK)
    but3 = Button(screen, "Perfect - EASY", WIDTH // 2 , HEIGHT // 2 + - 40, 440, 50, GRAY, WHITE, BLACK)
    but4 = Button(screen, "Zen Mode", WIDTH // 2 , HEIGHT // 2 + 40, 440, 50, GRAY, WHITE, BLACK)
    but6 = Button(screen, "Custom Song", WIDTH // 2 - 60, HEIGHT // 2 + 120, 320, 50, GRAY, WHITE, BLACK)
    but7 = Button(screen, "Load", but6.rect.midright[0] + 65, HEIGHT // 2 + 120, 110, 50, GRAY, WHITE, BLACK)
    but5 = Button(screen, "Return", WIDTH // 2 , HEIGHT - 50, 420, 50, GRAY, WHITE, BLACK)
    button_group = pygame.sprite.Group(but1, but2, but3, but4, but5, but6, but7)

    pygame.mixer.music.set_volume(1)

    while running:
        clock.tick(60)
        screen.blit(menu_image, (0, 0))
        current_time = pygame.time.get_ticks()

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('songs/mp3/dream-land.mp3')
            pygame.mixer.music.play()

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == SPARKS_EVENT:
                sparks.create_sparks(random.randint(0, WIDTH), random.randint(0, HEIGHT - 50))
                pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500)) # Wywoływanie co losową liczbę milisekund
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                explosion_x, explosion_y = pygame.mouse.get_pos()
                sparks.create_sparks(explosion_x, explosion_y)

                if but1.checkForInput():
                    start_game(PIRATE)
                if but2.checkForInput():
                    start_game(DREAMLAND)
                if but3.checkForInput():
                    start_game(PERFECT)
                if but4.checkForInput():
                    start_game()
                if but5.checkForInput():
                    running = False
                    main_menu()

        sparks.draw(screen)
        sparks.update()

        button_group.draw(screen)
        button_group.update()
        
        pygame.display.update()

def main_menu():
    running = True
    clock = pygame.time.Clock()

    sparks = Sparks(WIDTH, HEIGHT, True)

    # Ustawienie losowych interwałów dla tworzenia iskier
    SPARKS_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500))
    
    button_group = pygame.sprite.Group()
    text_group = pygame.sprite.Group()

    def add_text(text):
        text_group.add(Text(text, 60, WHITE, 500, 400, 2000, pygame.time.get_ticks()))

    but1 = Button(screen, "Start", WIDTH // 2 , HEIGHT // 2, 300, 50, GRAY, WHITE, BLACK)
    but2 = Button(screen, "Leaderboard", WIDTH // 2 , HEIGHT // 2 + 80, 300, 50, GRAY, WHITE, BLACK)
    but3 = Button(screen, "Exit", WIDTH // 2 , HEIGHT // 2 + 160, 300, 50, GRAY, WHITE, BLACK)
    button_group.add(but1)
    button_group.add(but2)
    button_group.add(but3)

    while running:
        clock.tick(60)
        screen.blit(menu_image, (0, 0))
        current_time = pygame.time.get_ticks()

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('songs/mp3/dream-land.mp3')
            pygame.mixer.music.play()

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPARKS_EVENT:
                sparks.create_sparks(random.randint(0, WIDTH), random.randint(0, HEIGHT - 50))
                pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500)) # Wywoływanie co losową liczbę milisekund
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                explosion_x, explosion_y = pygame.mouse.get_pos()
                sparks.create_sparks(explosion_x, explosion_y)

                if but1.checkForInput():
                    level_select()
                if but2.checkForInput():
                    leaderboard()
                if but3.checkForInput():
                    pygame.quit()
                    sys.exit()
                
        sparks.draw(screen)
        sparks.update()

        button_group.draw(screen)
        button_group.update()

        text_group.draw(screen)
        text_group.update(current_time)

        draw_text(TITLE, 60, PINK, WIDTH // 2, HEIGHT // 4)
        
        pygame.display.update()

    # Wyjście z gry
    pygame.quit()

if __name__ == "__main__":
    main_menu()
