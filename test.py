import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Ustalenie wymiarów ekranu
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animacja Iskier")

# background_image = pygame.image.load("background.png")
# background_image = pygame.transform.scale(background_image, (width, height))

# Kolor tła
background_color = (0, 0, 0)

# Klasa reprezentująca iskrę
class Spark:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.randint(2, 5)
        self.speed_x = random.uniform(-4, 4)
        self.speed_y = random.uniform(-4, 4)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.radius -= 0.1

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

# Lista przechowująca iskry
sparks = []

# Metoda do tworzenia iskier
def create_sparks(x, y, size, color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))):
    for _ in range(size):
        spark = Spark(x, y, color)
        sparks.append(spark)

# Metoda do znikania iskier
def update_sparks():
    alive_sparks = []
    for spark in sparks:
        spark.update()
        if spark.radius > 0:
            alive_sparks.append(spark)
            spark.draw()
    sparks[:] = alive_sparks


# Główna pętla programu
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(background_color)
    # screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Tworzenie eksplozji iskier po wciśnięciu przycisku SPACJA
                explosion_size = 20
                explosion_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                explosion_x = random.randint(100, width - 100)
                explosion_y = random.randint(100, height - 100)
                create_sparks(explosion_x, explosion_y, explosion_size, explosion_color)

    # Aktualizowanie i rysowanie iskier
    update_sparks()

    pygame.display.flip()
    clock.tick(60)

# Zakończenie Pygame
pygame.quit()
