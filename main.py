import pygame
import random

#from sparks import Sparks 
from sparks_sprite import Sparks

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Musician")

menu_image = pygame.image.load("graphics/Background/city.jpg").convert()
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))

background_image = pygame.image.load("graphics/Background/city2.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

stripe_image = pygame.image.load("graphics/stripe1.png").convert_alpha()
stripe_image = pygame.transform.scale(stripe_image, (WIDTH, HEIGHT))
stripe_image.set_alpha(200)

aim_image = pygame.image.load("graphics/Aim/aim1.png").convert_alpha()
aim_image = pygame.transform.scale_by(aim_image, 0.45)
aim_image.set_alpha(200)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']

# Key images
key1_image = pygame.image.load("graphics/Key/key1.png").convert_alpha()
key2_image = pygame.image.load("graphics/Key/key2.png").convert_alpha()
key3_image = pygame.image.load("graphics/Key/key3.png").convert_alpha()
key4_image = pygame.image.load("graphics/Key/key4.png").convert_alpha()
key5_image = pygame.image.load("graphics/Key/key5.png").convert_alpha()
key6_image = pygame.image.load("graphics/Key/key6.png").convert_alpha()
key7_image = pygame.image.load("graphics/Key/key7.png").convert_alpha()
key_images = [key1_image, key2_image, key3_image, key4_image, key5_image, key6_image, key7_image]
key_images = [pygame.transform.scale_by(key, 0.45) for key in key_images]

class Aim(pygame.sprite.Sprite):
    def __init__(self, keys) -> None:
        super().__init__()
        aim_img1 = pygame.image.load("graphics/Aim/aim1.png").convert_alpha()
        aim_img1 = pygame.transform.scale_by(aim_img1, 0.45)
        aim_img1.set_alpha(200)
        aim_img2 = pygame.image.load("graphics/Aim/aim1.png").convert_alpha()
        aim_img2 = pygame.transform.scale_by(aim_img2, 0.5)
        aim_img2.set_alpha(200)
        aim_img3 = pygame.image.load("graphics/Aim/aim3.png").convert_alpha()
        aim_img3 = pygame.transform.scale_by(aim_img3, 0.4)
        aim_img3.set_alpha(200)
        self.aim = [aim_img1, aim_img2, aim_img3]

        self.keys = keys

        self.image = self.aim[0]
        self.rect = self.image.get_rect(center = (220, 250))

    def animation(self):
        if pygame.sprite.spritecollide(self, self.keys):
            self.image = self.aim[1]
        elif pygame.key.get_pressed():
            self.image = self.aim[2]
        else: 
            self.image = self.aim[0]

    def update(self):
        self.animation()

class Key(pygame.sprite.Sprite):
    def __init__(self, revival, speed) -> None:
        super().__init__()

        self.key = random.choice(LETTERS)
        self.revival = revival
        self.time_alive = 0
        self.speed = speed

        self.image = random.choice(key_images)
        self.rect = self.image.get_rect(center = (WIDTH, HEIGHT // 2 + 10))

    def update(self, current_time):
        self.rect.x -= self.speed
        self.time_alive = (current_time - self.revival)

        self.drawLetter()
        self.destroy()

    def drawLetter(self):
        font = pygame.font.Font('fonts/font.ttf', 32)

        text = font.render(self.key, False, (255, 255, 255))
        text1 = font.render(self.key, False, (0, 0, 0))

        text_rect = text.get_rect(center=(self.rect.centerx + 10, self.rect.centery - 2))

        text1_rect = text1.get_rect(center=(self.rect.centerx + 10 + 2, self.rect.centery - 2 + 2))
        text2_rect = text1.get_rect(center=(self.rect.centerx + 10 + 2, self.rect.centery - 2 - 2))
        text3_rect = text1.get_rect(center=(self.rect.centerx + 10 - 2, self.rect.centery - 2 + 2))
        text4_rect = text1.get_rect(center=(self.rect.centerx + 10 - 2, self.rect.centery - 2 - 2))

        screen.blit(text1, text1_rect)
        screen.blit(text1, text2_rect)
        screen.blit(text1, text3_rect)
        screen.blit(text1, text4_rect)
        screen.blit(text, text_rect)

    def destroy(self):
        if self.rect.x <= -100: 
            print(f"boom! {self}")
            self.kill()

    def __str__(self) -> str:
        return f"Key - {self.key} - {self.revival} - {self.time_alive} - (x,y): ({self.rect.x},{self.rect.y})"


keys_group = pygame.sprite.Group()

KEYS_SIZE = 40

# Funkcja rysująca tekst
def draw_text(text, size, color, x, y):
    font = pygame.font.Font('fonts/font.ttf', size)
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


class Button(pygame.sprite.Sprite):

    def __init__(self, text, x, y, width, height, color, hover_color, border_color, action=None):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.action = action

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse):
            self.image.fill(self.hover_color)
            
            if click[0] == 1 and self.action is not None:
                self.action()
        else:
            self.image.fill(self.color)
        pygame.draw.rect(self.image, self.border_color, self.image.get_rect(), 3)  # Dodajemy czarne obramowanie

        draw_text(self.text, int(self.rect.height//1.5), BLACK, self.rect.centerx, self.rect.centery-2)



rev = 0
def create_key():
    global rev 

    rev += random.uniform(0.1, 1)
    key = Key(rev, 7)
    keys_group.add(key)


def get_key():
    if len(keys_group) > 0:

        return keys_group[0]
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

key_timer = pygame.USEREVENT + 2
pygame.time.set_timer(key_timer, random.randint(500, 1800))

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
    sparks = Sparks(True)

    # key = get_key().key
    
    while running:
        clock.tick(60)
        screen.fill((22, 22, 22))
        screen.blit(background_image, (0, 0))
        screen.blit(stripe_image, (0,13))
        
        display_score(score, reaction_time, average_reaction)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            
            if event.type == pygame.KEYDOWN:
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

            if event.type == key_timer:
                create_key()
                pygame.time.set_timer(key_timer, random.randint(500, 1800))

        keys_group.draw(screen)
        keys_group.update((pygame.time.get_ticks() - app_start_time) / 1000)
        screen.blit(aim_image, (220,245))
        sparks.draw(screen)
        sparks.update()
        pygame.display.update()
        

# Główna pętla gry
def main_menu():
    running = True
    clock = pygame.time.Clock()

    sparks = Sparks(True)

    # Ustawienie losowych interwałów dla tworzenia iskier
    SPARKS_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPARKS_EVENT, random.randint(500, 1500))

    pygame.mixer.Sound('songs/mp3/dream-land.mp3').play(-1)
    
    button_group = pygame.sprite.Group()
    button_group.add(Button("Start", WIDTH // 2 , HEIGHT // 1.7, 200, 50, GRAY, WHITE, BLACK, start_game))

    while running:
        clock.tick(60)
        screen.blit(menu_image, (0, 0))
        
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

        sparks.draw(screen)
        sparks.update()

        button_group.draw(screen)
        button_group.update()

        # Rysowanie elementów menu
        draw_text("Type Musician", 60, (228, 108, 235), WIDTH // 2, HEIGHT // 4)
        
        # Odświeżenie ekranu
        pygame.display.update()

    # Wyjście z gry
    pygame.quit()



# Uruchomienie gry
if __name__ == "__main__":
    main_menu()
