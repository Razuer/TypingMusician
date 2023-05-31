import pygame
import random


pygame.mixer.init()
# Klasa reprezentująca iskrę
class Spark:
    def __init__(self, screen, x, y, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.randint(2, 5)
        self.speed_x = random.uniform(-4, 4)
        self.speed_y = random.uniform(-4, 4)
        self.cycles = 0

    def update(self):
        self.x += self.speed_x
        self.y += (self.speed_y + self.cycles) 
        self.radius -= 0.03
        self.cycles += 0.1

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), int(self.radius))

class Sparks:
    def __init__(self, screen, sound = True):
        self.sparks: list[Spark] = []
        self.screen: pygame.display = screen
        self.sound = sound
        
    # Metoda do tworzenia iskier
    def create_sparks(self, x, y, size=50, color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))):
        if self.sound:
            pop = f"sounds/pop{random.randint(1, 5)}.mp3"
            pygame.mixer.Sound(pop).play().set_volume(0.5)
        for _ in range(size):
            spark = Spark(self.screen, x, y, color)
            self.sparks.append(spark)
        

    # Metoda do znikania iskier
    def update_sparks(self):
        alive_sparks = []
        for spark in self.sparks:
            spark.update()
            if spark.radius > 0 and not (spark.y > self.screen.get_height() or spark.x < 0 or spark.x > self.screen.get_width()):
                alive_sparks.append(spark)
                spark.draw()
        self.sparks[:] = alive_sparks