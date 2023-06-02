import pygame
import random

pygame.mixer.init()

class Spark(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = color
        self.radius = random.randint(2, 5)
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (round(self.x),round(self.y))
        self.speed_x = random.uniform(-4, 4)
        self.speed_y = random.uniform(-4, 4)
        self.gravity = 0
    
    def update(self):
        self.x += self.speed_x
        self.y += (self.speed_y + self.gravity)
        self.rect.center = (round(self.x),round(self.y))
        self.radius -= 0.03
        self.gravity += 0.1
        if self.radius <= 0 or self.rect.centerx < 0 or self.rect.centery > 600:
            self.kill()

        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)


class Sparks(pygame.sprite.Group):
    def __init__(self, sound=True):
        super().__init__()
        self.sound = sound

    def create_sparks(self, x, y, size=50, color=None):
        if self.sound:
            pop = f"sounds/pop{random.randint(1, 5)}.mp3"
            pygame.mixer.Sound(pop).play().set_volume(0.5)
        for _ in range(size):
            if not color:
                color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            spark = Spark(x, y, color)
            self.add(spark)
