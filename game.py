import os
import sys
import pygame
import random
import csv
from pygame_textinput import TextInputManager, TextInputVisualizer
from custom_song_loader import load_to_custom

from settings import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

menu_image = pygame.image.load(MENU_BG).convert()
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))

background_image = pygame.image.load(GAME_BG).convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
city1_image = pygame.image.load(OPT_BG).convert()
city1_image = pygame.transform.scale(city1_image, (WIDTH, HEIGHT))
city3_image = pygame.image.load(CITY3_BG).convert()
city3_image = pygame.transform.scale(city3_image, (WIDTH, HEIGHT))
city4_image = pygame.image.load(CITY4_BG).convert()
city4_image = pygame.transform.scale(city4_image, (WIDTH, HEIGHT))
pirate_image = pygame.image.load(PIRATE_BG).convert()
pirate_image = pygame.transform.scale(pirate_image, (WIDTH, HEIGHT))


savescore_image = pygame.image.load('graphics/Background/savescore.png').convert_alpha()
savescore_image = pygame.transform.scale_by(savescore_image, 1.4)
savescore_image.set_alpha(200)

stripe_image = pygame.image.load(STRIPE).convert_alpha()
stripe_image = pygame.transform.scale(stripe_image, (WIDTH, HEIGHT))
stripe_image.set_alpha(200)

CUSTOM = ""

from sprites import Key, Button, Aim, Text, Sparks, ErrorX, ErrorCircle

def draw_text(text, font, color, x, y, angle = 0, shadow = False, shadow_offset = 2, shadow_color = BLACK, center = True):
    text_surface = font.render(text, False, color)
    text_surface = pygame.transform.rotate(text_surface, angle)
    if(center):
        text_rect = text_surface.get_rect(center = (x, y))
    else: 
        text_rect = text_surface.get_rect(top = (x,y))

    if shadow:
        text_shadow = font.render(text, False, shadow_color)
        text_shadow = pygame.transform.rotate(text_shadow, angle)
        text_rects = [
            text_shadow.get_rect(center=(text_rect.centerx + shadow_offset, text_rect.centery + shadow_offset)),
            text_shadow.get_rect(center=(text_rect.centerx + shadow_offset, text_rect.centery - shadow_offset)),
            text_shadow.get_rect(center=(text_rect.centerx - shadow_offset, text_rect.centery + shadow_offset)),
            text_shadow.get_rect(center=(text_rect.centerx - shadow_offset, text_rect.centery - shadow_offset)),
        ]

        screen.blit(text_shadow, text_rects[0])
        screen.blit(text_shadow, text_rects[2])
        screen.blit(text_shadow, text_rects[1])
        screen.blit(text_shadow, text_rects[3])
    
    screen.blit(text_surface, text_rect)    

def leaderboard():
    sparks = Sparks(WIDTH, HEIGHT, True)
    SPARKS_EVENT = pygame.USEREVENT + 5
    pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500))
    
    button_group = pygame.sprite.Group()
    but1 = Button(screen, "Return", WIDTH // 2 , HEIGHT - 70, 300, 50, GRAY, WHITE, BLACK)
    button_group.add(but1)

    with open(SCORES_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            sorted_rows = sorted(reader, reverse=True, key=lambda row: (int(row[1]), (row[2]), row[0]))
        
    with open(SCORES_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sorted_rows) 

    # Funkcja wczytująca dane z pliku CSV
    def load_scores_from_csv(filename):
        scores = {}
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                player_name, score, song = row
                if song not in scores:
                    scores[song] = []
                scores[song].append((player_name, int(score)))
        return scores

    # Funkcja wyświetlająca dane
    def get_scores(scores, title):
        scores_list = []
        if title in scores:
            top_scores = scores[title]
            for i in range(10):
                if i < len(top_scores):
                    player_name, score = top_scores[i]
                    text = f"{i+1}. {player_name} - {score}"
                else:
                    text = f"{i+1}. {'_'*10}"
                scores_list.append(text)
        else:
            scores_list.append(text)
        return scores_list

    def draw_scores(scores, title, x, y):
        draw_text(title, FONT30, WHITE, x, y-30)
        for i, score in enumerate(scores):
            draw_text(score, FONT20, WHITE, x, y + (i+1)*30)

    scores = load_scores_from_csv('leaderboard.csv')
    scores1 = get_scores(scores, "PERFECT")
    scores2 = get_scores(scores, "DREAMLAND")
    scores3 = get_scores(scores, "PIRATE")

    while True:
        clock.tick(FPS)
        screen.blit(menu_image, (0, 0))

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(DREAMLAND)
            pygame.mixer.music.play()

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
        
        
        draw_text("Leaderboard", FONT40, WHITE, WIDTH//2, 60)

        # Wywołaj funkcję draw_scores dla każdej piosenki
        draw_scores(scores1, "PERFECT", WIDTH//2 - 300, 150)
        draw_scores(scores2, "DREAMLAND", WIDTH//2, 150)
        draw_scores(scores3, "PIRATE", WIDTH//2 + 300, 150)

        pygame.draw.line(screen, WHITE, (350, 130), (350, 430), 2)
        pygame.draw.line(screen, WHITE, (650, 130), (650, 430), 2)
        
        pygame.display.update()

def start_game(song_path = None):
    key_timings = None
    if song_path:
        with open(f"{os.path.splitext(song_path)[0]}.txt", "r") as file:
            key_timings = [int(line.strip()) for line in file.readlines()]
            pygame.mixer.fadeout(1000)
            zen = False
    else:
        song_path = ZEN_SONG
        key_timer = pygame.USEREVENT + 4
        pygame.time.set_timer(key_timer, 500)
        zen = True

    pygame.mixer.music.load(song_path)
    pygame.mixer.music.set_volume(1)
    end_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(end_timer, 0)

    if song_path == PERFECT:
        gameplay_bg = city4_image
    elif song_path == DREAMLAND:
        gameplay_bg = city3_image
    elif song_path == PIRATE:
        gameplay_bg = pirate_image
    elif zen:
        gameplay_bg = city1_image
    else:
        gameplay_bg = background_image
    
    sparks = Sparks(WIDTH, HEIGHT, False)
    sparks2 = Sparks(WIDTH, HEIGHT, False)
    delayed_sparks = []
    keys_group = pygame.sprite.Group()
    texts_group = pygame.sprite.Group()
    aim = Aim(keys_group)
    aim_group = pygame.sprite.GroupSingle(aim)
    errorX_group = pygame.sprite.GroupSingle()
    multiCircle_group = pygame.sprite.Group()

    score = 0
    play_music = False
    timerSet = False
    start_time = pygame.time.get_ticks()
    combo = 0
    multiplier = 1

    def display_score(score, combo, multiplier):
        text = FONT40.render(str(score), False, WHITE)

        combo1_text = FONT30.render(f"COMBO", False, WHITE)
        combo2_text = FONT30.render(str(combo), False, WHITE)
        multi_text = FONT45.render(f"x{multiplier}", False, WHITE)

        pygame.draw.circle(screen, WHITE, (WIDTH-100, 80), 50, 5) # draw circle around multi_text
        screen.blit(multi_text, multi_text.get_rect(center=(WIDTH-100, 75))) # center multi_text in the circle

        combo_line_width = 150 # set the width of the line
        combo_line_height = 5 # set the height of the line
        combo_line_rect_top = combo1_text.get_rect(center=(100, 30)) # get the rect of combo1_text and move it up by 15 pixels
        combo_line_rect_bottom = combo1_text.get_rect(center=(100, 130)) # get the rect of combo1_text and move it down by 15 pixels
        
        pygame.draw.rect(screen, WHITE, (combo_line_rect_top.centerx - combo_line_width//2, combo_line_rect_top.centery - combo_line_height//2, combo_line_width, combo_line_height)) # draw line above combo1_text
        pygame.draw.rect(screen, WHITE, (combo_line_rect_bottom.centerx - combo_line_width//2, combo_line_rect_bottom.centery - combo_line_height//2, combo_line_width, combo_line_height)) # draw line below combo1_text

        screen.blit(combo1_text, combo1_text.get_rect(center=(100, 60)))
        screen.blit(combo2_text, combo2_text.get_rect(center=(100, 100)))
        screen.blit(text, text.get_rect(midtop=(WIDTH//2, 10))) # display score at the top-center of the screen

    while True:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks() - start_time

        if not play_music and current_time >= DELAY:
            if zen: pygame.mixer.music.play(-1)
            else: pygame.mixer.music.play()
            play_music = True

        colided = pygame.sprite.spritecollide(aim, keys_group, False)

        if colided:
            colided_dist = aim.rect.centerx - colided[0].rect.centerx
            if colided_dist > 62:
                combo = 0
                if multiplier > 1:
                    multiCircle_group.add(ErrorCircle(WIDTH-100, 80, 100))
                    multiplier = 1
                pygame.mixer.Sound(ERROR_SOUND).play()
                errorX_group.add(ErrorX())
                
                texts_group.add(Text(random.choice(["Ouch...", "Bye...", "Oh no!", "Nooo...", "Ahhh...", "Uh-oh...", "Yikes!", "Ah well...", "D'oh!d"]), 20, RED,  random.randint(40, 160), random.randint(HEIGHT//2 - 50, HEIGHT//2 + 60), 1200))

        pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            elif event.type == end_timer and timerSet:
                save_score(score, song_path, True, zen)
                
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    save_score(score, song_path, False, zen)
                
                elif event.unicode.isalpha():
                    pressed = True
                    if colided:
                        dist = aim.rect.centerx - colided[0].rect.centerx
                        if event.unicode.upper() == colided[0].key:                    
                            sparks2.create_sparks(aim.rect.centerx, aim.rect.centery, 70, colided[0].color)
                            combo +=1
                            
                            if abs(dist) < 14:
                                texts_group.add(Text("PERFECT!", 40, CYAN, 500, 150, 1000))
                                points = 10 * multiplier
                                texts_group.add(Text(f"+{points}", 30, CYAN, random.randint(190, 250), random.randint(270, 330), 700))
                                score += points
                            else: 
                                texts_group.add(Text("GOOD!", 35, WHITE, 500, 150, 1000))
                                points = 5 * multiplier
                                texts_group.add(Text(f"+{points}", 30, WHITE, random.randint(190, 250), random.randint(270, 330), 700))
                                score += points
                            if combo == 15:
                                multiplier = 2
                                multiCircle_group.add(ErrorCircle(WIDTH-100, 80, 100, red=False))
                            elif combo == 30:
                                multiplier = 3
                                multiCircle_group.add(ErrorCircle(WIDTH-100, 80, 100, red=False))
                            elif combo == 45:
                                multiplier = 4
                                multiCircle_group.add(ErrorCircle(WIDTH-100, 80, 100, red=False))
                            colided[0].kill()
        
            elif zen and event.type == key_timer:
                delayed_sparks.append(current_time+DELAY)
                keys_group.add(Key(screen, KEY_SPEED))
                pygame.time.set_timer(key_timer, random.randint(200, 800))

        if key_timings and key_timings[0] <= current_time:
            delayed_sparks.append(current_time+DELAY)
            keys_group.add(Key(screen, KEY_SPEED))
            key_timings.pop(0)

        if delayed_sparks and delayed_sparks[0] <= current_time:
            sparks.create_sparks(random.randint(50, WIDTH-50), random.randint(20, HEIGHT - 50))
            delayed_sparks.pop(0)

        screen.blit(gameplay_bg, (0, 0))

        sparks.draw(screen)
        sparks.update()
    
        screen.blit(stripe_image, (0,13))
        
        display_score(score, combo, multiplier)

        keys_group.draw(screen)
        keys_group.update()

        sparks2.draw(screen)
        sparks2.update()

        aim_group.draw(screen)
        aim_group.update(pressed)

        texts_group.draw(screen)
        texts_group.update()

        errorX_group.update()
        errorX_group.draw(screen)

        multiCircle_group.update()
        multiCircle_group.draw(screen)

        pygame.display.update()

        if not pygame.mixer.music.get_busy() and play_music and not timerSet and current_time >= DELAY:
            pygame.time.set_timer(end_timer, 1000)
            timerSet = True
        
def save_score(score, song_path, finished, zen):
    buttons_group = pygame.sprite.Group()
    but1 = Button(screen, "Save score", 500, 400, 300, 50, CYAN, WHITE, BLACK)
    but2 = Button(screen, "Exit", 500, 460, 300, 50, CYAN, WHITE, BLACK)
    buttons_group.add(but1, but2)

    pygame.mixer.music.load(song_path)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    manager = TextInputManager(validator = lambda input: len(input) <= 15)
    textinput = TextInputVisualizer(manager=manager, font_object=FONT40, font_color=BLACK)

    input_surface = pygame.Surface((500, 60))
    input_surface.fill((255, 255, 255))  # Biały kolor prostokąta
    input_rect = input_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    
    def save_it(player_name):
        song = ''
        if song_path == PERFECT:
            song = "PERFECT"
        elif song_path == DREAMLAND:
            song = 'DREAMLAND'
        elif song_path == PIRATE:
            song = 'PIRATE'
        
        with open(SCORES_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([player_name, score, song])   

    
    if score < 1000 or not finished:
        congrats = random.choice(['MEH...', 'IMPRESSIVE... NOT', 'STELLAR EFFORT.', 'KEEP PRACTICING!', "PRETTY... BAD"])
    else:
        congrats = random.choice(['GREAT!', 'AMAZING!', 'AWESOME!', 'WHAT A PRO!'])
    
    pygame.key.set_repeat(200, 25)
    
    global CUSTOM
    if song_path == CUSTOM:
        isCustom = True
    else: 
        isCustom = False
    saved = False

    while True:
        clock.tick(FPS)
        screen.blit(background_image, (0, 0))
        screen.blit(savescore_image, savescore_image.get_rect(center=(500, 300)))
        
        draw_text(congrats, FONT45, WHITE, 500, 150)
        draw_text(f"Your score: {score}", FONT30, WHITE, 500, 200)
        if isCustom or zen:
            draw_text("You can't save custom game!", FONT30, WHITE, input_rect.midtop[0], input_rect.midtop[1]-15)
        elif finished:
            draw_text("Enter your nick:", FONT20, WHITE, input_rect.midtop[0], input_rect.midtop[1]-15)
        else:
            draw_text("To save your score you must finish the game!", FONT20, WHITE, input_rect.midtop[0], input_rect.midtop[1]-15)
        buttons_group.draw(screen)
        buttons_group.update()

        events = pygame.event.get()
        if finished and not isCustom:
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
                    saved = True
                    save_it(textinput.value)
                if but2.checkForInput():
                    pygame.mixer.music.fadeout(1000)
                    level_select()
        pygame.display.update()

def level_select():
    sparks = Sparks(WIDTH, HEIGHT, True)
    SPARKS_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500))
    
    but1 = Button(screen, "He's a Pirate!", WIDTH // 2 , HEIGHT // 2 - 200, 440, 50, RED, WHITE, BLACK)
    but2 = Button(screen, "Dream Land", WIDTH // 2 , HEIGHT // 2 - 120, 440, 50, YELLOW, WHITE, BLACK)
    but3 = Button(screen, "Perfect", WIDTH // 2 , HEIGHT // 2 + - 40, 440, 50, LIGHTERBLUE, WHITE, BLACK)
    but4 = Button(screen, "Zen Mode", WIDTH // 2 , HEIGHT // 2 + 40, 440, 50, LIGHTGREEN, WHITE, BLACK)
    but5 = Button(screen, "Custom Song", WIDTH // 2 - 60, HEIGHT // 2 + 120, 320, 50, PURPLE, WHITE, BLACK)
    but6 = Button(screen, "Load", but5.rect.midright[0] + 65, HEIGHT // 2 + 120, 110, 50, PURPLE, WHITE, BLACK)
    but7 = Button(screen, "Return", WIDTH // 2 , HEIGHT - 50, 420, 50, GRAY, WHITE, BLACK)
    button_group = pygame.sprite.Group(but1, but2, but3, but4, but5, but6, but7)

    text_group = pygame.sprite.GroupSingle()

    global CUSTOM

    while True:
        clock.tick(60)
        screen.blit(menu_image, (0, 0))

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(DREAMLAND)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()

        if CUSTOM == "":
            but5.active = False
        else: 
            but5.active = True

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == SPARKS_EVENT:
                if len(sparks) < 250:
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
                    start_game(CUSTOM)
                if but6.checkForInput():
                    CUSTOM = load_to_custom()
                    if CUSTOM == "":
                        text_group.add(Text("ERROR", 40, WHITE, but6.rect.centerx, but6.rect.centery, 8000))

                if but7.checkForInput():
                    main_menu()

        sparks.draw(screen)
        sparks.update()

        button_group.draw(screen)
        button_group.update()

        text_group.draw(screen)
        text_group.update()

        draw_text("HARD", FONT20, WHITE, but1.rect.topright[0]-10, but1.rect.topright[1]+10, -45, True)
        draw_text("MEDIUM", FONT20, WHITE, but2.rect.topright[0]-10, but2.rect.topright[1]+10, -45, True)
        draw_text("EASY", FONT20, WHITE, but3.rect.topright[0]-10, but3.rect.topright[1]+10, -45, True)
        
        pygame.display.update()

def main_menu():
    # Ustawienie losowych interwałów dla tworzenia iskier
    SPARKS_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500))

    sparks = Sparks(WIDTH, HEIGHT, True)
    button_group = pygame.sprite.Group()
    text_group = pygame.sprite.Group()

    but1 = Button(screen, "Start", WIDTH // 2 , HEIGHT // 2, 300, 50, PINK, WHITE, BLACK)
    but2 = Button(screen, "Leaderboard", WIDTH // 2 , HEIGHT // 2 + 80, 300, 50, CYAN, WHITE, BLACK)
    but3 = Button(screen, "Exit", WIDTH // 2 , HEIGHT // 2 + 160, 300, 50, GRAY, RED, BLACK)
    button_group.add(but1)
    button_group.add(but2)
    button_group.add(but3)

    while True:
        clock.tick(FPS)
        screen.blit(menu_image, (0, 0))

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(DREAMLAND)
            pygame.mixer.music.play()

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
        text_group.update()
        
        draw_text(TITLE, FONT60, PINK, WIDTH // 2, HEIGHT // 4, shadow=True, shadow_color=WHITE)
        
        pygame.display.update()

    # Wyjście z gry
    pygame.quit()

if __name__ == "__main__":
    main_menu()
    
