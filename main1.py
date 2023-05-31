import pygame
import random

from sparks import Sparks 

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Musician")

menu_image = pygame.image.load("graphics/city.jpg")
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))

background_image = pygame.image.load("graphics/city2.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

stripe_image = pygame.image.load("graphics/stripe1.png").convert_alpha()
stripe_image = pygame.transform.scale(stripe_image, (WIDTH, HEIGHT))
stripe_image.set_alpha(200)

aim_image = pygame.image.load("graphics/aim2.png").convert_alpha()
aim_image = pygame.transform.scale(aim_image, (WIDTH, HEIGHT))
aim_image.set_alpha(280)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']
key_list: list[str] = []
KEYS_SIZE = 5

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

class Key:
    def __init__(self, key, revival, time_alive, key_image) -> None:
        self.key = key
        self.revival = revival
        self.time_alive = time_alive
        self.key_image = key_image
        self.x = WIDTH
        self.y = HEIGHT // 2 + 10

    def move(self):
        self.x -= 1

    def draw(self):
        font = pygame.font.Font('fonts/font.ttf', 32)

        text = font.render(self.key, True, (255, 255, 255))
        text1 = font.render(self.key, True, (0, 0, 0))

        text_rect = text.get_rect(center=(self.x, self.y - 2))

        text1_rect = text1.get_rect(center=(self.x + 2, self.y - 2 + 2))
        text2_rect = text1.get_rect(center=(self.x + 2, self.y - 2 - 2))
        text3_rect = text1.get_rect(center=(self.x - 2, self.y - 2 + 2))
        text4_rect = text1.get_rect(center=(self.x - 2, self.y - 2 - 2))

        button_rect = key5_image.get_rect(center=(self.x, self.y))
        screen.blit(key5_image, button_rect)
        screen.blit(text1, text1_rect)
        screen.blit(text1, text2_rect)
        screen.blit(text1, text3_rect)
        screen.blit(text1, text4_rect)
        screen.blit(text, text_rect)

# Funkcja rysująca tekst
def draw_text(text, size, color, x, y):
    font = pygame.font.Font('fonts/font.ttf', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# Funkcja rysująca przycisk
def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, width, height)
    button_rect.center = (x, y)

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

def display_keys():
    while len(key_list) < KEYS_SIZE:
        key_list.append(random.choice(LETTERS))

    font = pygame.font.Font('fonts/font.ttf', 32)

    for i, item in enumerate(key_list):
        text = font.render(item, True, (255, 255, 255))
        text1 = font.render(item, True, (0, 0, 0))

        text_rect = text.get_rect(center=(WIDTH / 2 + i * 70 + 2, HEIGHT / 2 + 8))

        text1_rect = text1.get_rect(center=(WIDTH / 2 + i * 70 + 2 + 2, HEIGHT / 2 + 8 + 2))
        text2_rect = text1.get_rect(center=(WIDTH / 2 + i * 70 + 2 + 2, HEIGHT / 2 + 8 - 2))
        text3_rect = text1.get_rect(center=(WIDTH / 2 + i * 70 + 2 - 2, HEIGHT / 2 + 8 + 2))
        text4_rect = text1.get_rect(center=(WIDTH / 2 + i * 70 + 2 - 2, HEIGHT / 2 + 8 - 2))

        button_rect = key5_image.get_rect(center=(WIDTH / 2 + i * 70, HEIGHT / 2 + 10))
        screen.blit(key5_image, button_rect)
        screen.blit(text1, text1_rect)
        screen.blit(text1, text2_rect)
        screen.blit(text1, text3_rect)
        screen.blit(text1, text4_rect)
        screen.blit(text, text_rect)

def get_key():
    while len(key_list) < KEYS_SIZE:
        key_list.append(random.choice(LETTERS))
    
    return key_list[0]


def display_score(score, reaction_time, average_reaction):
    font = pygame.font.Font('fonts/font.ttf', 20)

    text = font.render(str(score), True, (255, 255, 255))
    text_rect = text.get_rect(topright=(WIDTH - 10, 10))

    reaction_text = font.render("Reaction time: {:.3f} s".format(reaction_time), True, (255, 255, 255))
    reaction_text_rect = reaction_text.get_rect(topleft=(10, 10))

    average_text = font.render("Average reaction time: {:.3f} s".format(average_reaction), True, (255, 255, 255))
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

    start_time = pygame.time.get_ticks()
    sparks = Sparks(screen=screen)

    key = get_key()
    
    while running:
        clock.tick(60)
        screen.fill((22, 22, 22))
        screen.blit(background_image, (0, 0))
        screen.blit(stripe_image, (0,13))
        screen.blit(aim_image, (0,13))

        display_score(score, reaction_time, average_reaction)
        display_keys()
                
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
                    key_list.pop(0)
                    key = get_key()

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

    pygame.mixer.Sound('sounds/dream-land.mp3').play(-1)

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
