import pygame
import random

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

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.radius -= 0.1

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), int(self.radius))

class Sparks:
    def __init__(self, screen):
        self.sparks: list[Spark] = []
        self.screen: pygame.display = screen
        
    # Metoda do tworzenia iskier
    def create_sparks(self, x, y, size=20, color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))):
        for _ in range(size):
            spark = Spark(self.screen, x, y, color)
            self.sparks.append(spark)

    # Metoda do znikania iskier
    def update_sparks(self):
        alive_sparks = []
        for spark in self.sparks:
            spark.update()
            if spark.radius > 0:
                alive_sparks.append(spark)
                spark.draw()
        self.sparks[:] = alive_sparks

