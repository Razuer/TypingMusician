import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Musician")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']
key_list: list[str] = []
KEYS_SIZE = 5

button_width, button_height = 200, 50
button_x, button_y = WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2

button_image = pygame.image.load("img.png").convert_alpha()
button_image = pygame.transform.scale(button_image, (button_image.get_width() // 15, button_image.get_height() // 15))

# Funkcja rysująca tekst
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# Funkcja rysująca przycisk
def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    draw_text(text, 30, BLACK, x + width / 2, y + height / 2)


def display_key():
    while len(key_list) < KEYS_SIZE:
        key_list.append(random.choice(LETTERS))

    def key_render(k):
        return font.render(k, True, (255, 255, 255))

    font = pygame.font.Font(None, 36)

    for i, item in enumerate(key_list):
        text = key_render(item)
        text_rect = text.get_rect(center=(WIDTH / 2 + i * 50, HEIGHT / 2))
        screen.blit(button_image, text_rect)
        screen.blit(text, text_rect)

    return key_list.pop(0)


def display_score(score, reaction_time, average_reaction):
    font = pygame.font.Font(None, 36)

    text = font.render(str(score), True, (255, 255, 255))
    text_rect = text.get_rect(topright=(WIDTH - 10, 10))

    reaction_text = font.render("Czas reakcji: {:.3f} s".format(reaction_time), True, (255, 255, 255))
    reaction_text_rect = reaction_text.get_rect(topleft=(10, 10))

    average_text = font.render("Średni czas reakcji: {:.3f} s".format(average_reaction), True, (255, 255, 255))
    average_text_rect = reaction_text.get_rect(topleft=(10, 56))

    screen.blit(average_text, average_text_rect)
    screen.blit(reaction_text, reaction_text_rect)
    screen.blit(text, text_rect)


def start_game():
    running = True
    clock = pygame.time.Clock()
    score = 0
    reaction_time = 0
    reaction_time_sum = 0
    run_num = 0
    average_reaction = 0

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0))
        key = display_key()
        display_score(score, reaction_time, average_reaction)
        pygame.display.update()

        run_num += 1
        waiting_for_key = True
        start_time = pygame.time.get_ticks()
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_key = False
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha() and event.unicode.upper() == key:
                        reaction_time = (pygame.time.get_ticks() - start_time) / 1000
                        reaction_time_sum += reaction_time
                        average_reaction = reaction_time_sum / run_num
                        print("Poprawny klawisz! Czas reakcji: {:.3f} s".format(reaction_time))
                        score += 10
                        waiting_for_key = False
                    else:
                        print("Niepoprawny klawisz.")
            pygame.display.update()


# Główna pętla gry
def main_menu():
    running = True
    while running:
        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Czyszczenie ekranu
        screen.fill(WHITE)

        # Rysowanie elementów menu
        draw_text("Type Musician", 60, BLACK, WIDTH // 2, HEIGHT // 4)
        draw_button("Start", button_x, button_y, button_width, button_height, GRAY, BLACK, start_game)

        # Odświeżenie ekranu
        pygame.display.flip()

    # Wyjście z gry
    pygame.quit()


# Uruchomienie gry
if __name__ == "__main__":
    main_menu()
