import pygame
import random

from sparks import Sparks 

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Musician")

menu_image = pygame.image.load("graphics/city.jpg").convert()
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))

background_image = pygame.image.load("graphics/city2.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

stripe_image = pygame.image.load("graphics/stripe1.png").convert_alpha()
stripe_image = pygame.transform.scale(stripe_image, (WIDTH, HEIGHT))
stripe_image.set_alpha(200)

aim_image = pygame.image.load("graphics/aim2.png").convert_alpha()
aim_image = pygame.transform.scale(aim_image, (WIDTH, HEIGHT))
aim_image.set_alpha(200)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']

key1_image = pygame.image.load("graphics/key1.png").convert_alpha()
key1_image = pygame.transform.scale(key1_image, (WIDTH // 15, WIDTH // 15))
key2_image = pygame.image.load("graphics/key2.png").convert_alpha()
key2_image = pygame.transform.scale(key2_image, (WIDTH // 15, WIDTH // 15))
key3_image = pygame.image.load("graphics/key3.png").convert_alpha()
key3_image = pygame.transform.scale(key3_image, (WIDTH // 15, WIDTH // 15))
key4_image = pygame.image.load("graphics/key4.png").convert_alpha()
key4_image = pygame.transform.scale(key4_image, (WIDTH // 15, WIDTH // 15))
key5_image = pygame.image.load("graphics/key5.png").convert_alpha()
key5_image = pygame.transform.scale(key5_image, (WIDTH // 15, WIDTH // 15))
key6_image = pygame.image.load("graphics/key6.png").convert_alpha()
key6_image = pygame.transform.scale(key6_image, (WIDTH // 15, WIDTH // 15))
key7_image = pygame.image.load("graphics/key7.png").convert_alpha()
key7_image = pygame.transform.scale(key7_image, (WIDTH // 15, WIDTH // 15))

key_images = [key1_image, key2_image, key3_image, key4_image, key5_image, key6_image, key7_image]

class Key:
    def __init__(self, key, revival, speed) -> None:
        self.key = key
        self.revival = revival
        self.time_alive = 0
        self.speed = speed
        self.key_image = random.choice(key_images)
        self.x = WIDTH
        self.y = HEIGHT // 2 + 10

    def update(self, current_time):
        self.x -= self.speed
        self.time_alive = (current_time - self.revival)

    def draw(self):
        font = pygame.font.Font('fonts/font.ttf', 32)

        text = font.render(self.key, False, (255, 255, 255))
        text1 = font.render(self.key, False, (0, 0, 0))

        text_rect = text.get_rect(center=(self.x + 2, self.y - 2))

        text1_rect = text1.get_rect(center=(self.x + 2 + 2, self.y - 2 + 2))
        text2_rect = text1.get_rect(center=(self.x + 2 + 2, self.y - 2 - 2))
        text3_rect = text1.get_rect(center=(self.x + 2 - 2, self.y - 2 + 2))
        text4_rect = text1.get_rect(center=(self.x + 2 - 2, self.y - 2 - 2))

        button_rect = self.key_image.get_rect(center=(self.x, self.y))
        screen.blit(self.key_image, button_rect)
        screen.blit(text1, text1_rect)
        screen.blit(text1, text2_rect)
        screen.blit(text1, text3_rect)
        screen.blit(text1, text4_rect)
        screen.blit(text, text_rect)

    def __str__(self) -> str:
        return f"Key - {self.key} - {self.revival} - {self.time_alive} - (x,y): ({self.x},{self.y})"

key_list: list[Key] = []
alive_keys: list[Key] = []
KEYS_SIZE = 40

# Funkcja rysująca tekst
def draw_text(text, size, color, x, y):
    font = pygame.font.Font('fonts/font.ttf', size)
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# Funkcja rysująca przycisk
def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, width, height)
    button_rect.center = (x, y)

    dark_rect = pygame.Rect(x, y, width+6, height+6)
    dark_rect.center = (x, y)


    pygame.draw.rect(screen, BLACK, dark_rect)
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, button_rect)
        if click[0] == 1 and action is not None:
            action()
            return True
    else:
        pygame.draw.rect(screen, color, button_rect)
        # pygame.draw.rect(screen, color, button_rect, border_radius=5)

    draw_text(text, int(height//1.5), BLACK, button_rect.centerx, button_rect.centery-2)
    return False

def create_keys():
    rev = 0
    while len(key_list) < KEYS_SIZE:
        rev += random.uniform(0.1, 1)
        key = Key(random.choice(LETTERS), rev, 7)
        key_list.append(key)

def display_keys(running_time):
    copy = key_list[:]
    for item in copy:
        if item.revival <= running_time:
            alive_keys.append(item)
            key_list.remove(item)
    copy = alive_keys[:]
    for item in copy:
        item.update(running_time)
        if item.x < 0:
            alive_keys.remove(item)
        else: item.draw()


def get_key():
    if len(alive_keys) > 0:
        return alive_keys[0]
    else:
         return None


def display_score(score, reaction_time, average_reaction):
    font = pygame.font.Font('fonts/font.ttf', 20)

    text = font.render(str(score), False, (255, 255, 255))
    text_rect = text.get_rect(topright=(WIDTH - 10, 10))

    reaction_text = font.render("Reaction time: {:.3f} s".format(reaction_time), False, (255, 255, 255))
    reaction_text_rect = reaction_text.get_rect(topleft=(10, 10))

    average_text = font.render("Average reaction time: {:.3f} s".format(average_reaction), False, (255, 255, 255))
    average_text_rect = reaction_text.get_rect(topleft=(10, 56))

    screen.blit(average_text, average_text_rect)
    screen.blit(reaction_text, reaction_text_rect)
    screen.blit(text, text_rect)


def start_game():
    running = True
    clock = pygame.time.Clock()
    pygame.mixer.stop()
    score = 0
    reaction_time = 0
    reaction_time_sum = 0
    run_num = 0
    average_reaction = 0
    app_start_time = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()
    sparks = Sparks(screen=screen)

    create_keys()
    # key = get_key().key
    
    while running:
        clock.tick(60)
        screen.fill((22, 22, 22))
        screen.blit(background_image, (0, 0))
        screen.blit(stripe_image, (0,13))
        
        display_score(score, reaction_time, average_reaction)
        display_keys((pygame.time.get_ticks() - app_start_time) / 1000)

        screen.blit(aim_image, (0,13))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and event.unicode.upper() == key:
                    run_num += 1
                    score += 10

                    sparks.create_sparks(WIDTH / 2, HEIGHT / 2, 20, (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))

                    reaction_time = (pygame.time.get_ticks() - start_time) / 1000
                    reaction_time_sum += reaction_time
                    average_reaction = reaction_time_sum / run_num
                    print("Poprawny klawisz! Czas reakcji: {:.3f} s".format(reaction_time))
                    
                    start_time = pygame.time.get_ticks()
                    # key = get_key().key

                else:
                    print("Niepoprawny klawisz.")

        sparks.update_sparks()
        pygame.display.update()
        

# Główna pętla gry
def main_menu():
    running = True
    clock = pygame.time.Clock()

    sparks = Sparks(screen=screen)
    # Ustawienie losowych interwałów dla tworzenia iskier
    SPARKS_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500))

    pygame.mixer.Sound('songs/mp3/dream-land.mp3').play(-1)

    while running:
        clock.tick(60)
        screen.blit(menu_image, (0, 0))
        
        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPARKS_EVENT:
                sparks.create_sparks(random.randint(0, WIDTH), random.randint(0, HEIGHT - 50), 50, (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
                pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500)) # Wywoływanie co losową liczbę milisekund
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                explosion_size = 50
                explosion_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                explosion_x, explosion_y = pygame.mouse.get_pos()
                sparks.create_sparks(explosion_x, explosion_y, explosion_size, explosion_color)

        sparks.update_sparks()

        # Rysowanie elementów menu
        draw_text("Type Musician", 60, (228, 108, 235), WIDTH // 2, HEIGHT // 4)
        draw_button("Start", WIDTH // 2 , HEIGHT // 1.7, 200, 50, GRAY, WHITE, start_game)
        
        # Odświeżenie ekranu
        pygame.display.update()

    # Wyjście z gry
    pygame.quit()



# Uruchomienie gry
if __name__ == "__main__":
    main_menu()
