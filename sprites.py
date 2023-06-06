import pygame
import random
from settings import *

class Aim(pygame.sprite.Sprite):
    AIM_IMGS = []
    for i in range(1,4):
        aim_img = pygame.image.load(f"graphics/Aim/aim{i}.png").convert_alpha()
        scale = 0.45
        if i == 2: scale = 0.46
        elif i == 3: scale = 0.43 
        aim_img = pygame.transform.scale_by(aim_img, scale)
        aim_img.set_alpha(200)
        AIM_IMGS.append(aim_img)

    def __init__(self, keys) -> None:
        super().__init__()
        self.rect = Aim.AIM_IMGS[0].get_rect(center=(220, 305))
        self.image = Aim.AIM_IMGS[0]
        self.cooldown = 0
        self.keys_group = keys

    def animation(self):
        if pygame.sprite.spritecollide(self, self.keys_group, False) and self.cooldown == 0:
            self.image = Aim.AIM_IMGS[1]
            self.rect = Aim.AIM_IMGS[1].get_rect(center=(220, 305))
        elif self.cooldown > 0:
            self.image = Aim.AIM_IMGS[2]
            self.rect = Aim.AIM_IMGS[2].get_rect(center=(220, 305))
            self.cooldown = max(self.cooldown-0.2, 0)
        else: 
            self.image = Aim.AIM_IMGS[0]
            self.rect = Aim.AIM_IMGS[0].get_rect(center=(220, 305))

    def update(self, pressed):
        if pressed:
            self.cooldown = 1
        self.animation()

class Text(pygame.sprite.Sprite):
    def __init__(self, text, font_size, color, x, y, duration):
        super().__init__()
        self.text = text
        self.font_size = font_size
        self.color = color
        self.duration = duration
        self.start_time = pygame.time.get_ticks()

        self.font = pygame.font.Font(FONT, self.font_size)
        self.image = self.font.render(self.text, False, self.color)

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (round(self.x),round(self.y))

        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-1, 1)

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if elapsed_time >= self.duration:
            self.kill()  # Usuwanie sprite'a po zakończeniu czasu trwania

        # Przesunięcie tekstu na ekranie
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.center = (round(self.x),round(self.y))

        alpha = int(max(0, 255 - (elapsed_time / self.duration) * 255))
        self.image.set_alpha(alpha)

class Key(pygame.sprite.Sprite):
    
    LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
               'W', 'X', 'Y', 'Z']
    KEY_IMGS = []
    for i in range(1, 8):
        key_image = pygame.image.load(f"graphics/Key/key{i}.png").convert_alpha()
        key_image = pygame.transform.scale_by(key_image, 0.45)
        if i == 1:
            color = (200, 152, 230)
        elif i == 2:
            color = (196, 242, 148)
        elif i == 3:
            color = (120, 248, 252)
        elif i == 4:
            color = (254, 171, 239)
        elif i == 5:
            color = (244, 251, 161)
        elif i == 6:
            color = (94, 242, 124)
        else :
            color = (255, 150, 156)
        KEY_IMGS.append((key_image, color))

    font = pygame.font.Font(FONT, 32)

    def __init__(self, screen, speed) -> None:
        super().__init__()
        self.screen = screen
        self.key = random.choice(Key.LETTERS)
        self.touchedAim = False
        self.speed = speed

        self.image, self.color = random.choice(Key.KEY_IMGS)
        self.rect = self.image.get_rect(center=(WIDTH + 20, HEIGHT // 2 + 10))

        self.text_shadow = Key.font.render(self.key, False, BLACK)
        self.text = Key.font.render(self.key, False, WHITE)

    def update(self):
        self.rect.move_ip(-self.speed, 0)

        self.drawLetter()
        self.destroy()

    def drawLetter(self):
        offset = 2
        text_rects = [
            self.text_shadow.get_rect(center=(self.rect.centerx + 9 + offset, self.rect.centery - 2 + offset)),
            self.text_shadow.get_rect(center=(self.rect.centerx + 9 + offset, self.rect.centery - 2 - offset)),
            self.text_shadow.get_rect(center=(self.rect.centerx + 9 - offset, self.rect.centery - 2 + offset)),
            self.text_shadow.get_rect(center=(self.rect.centerx + 9 - offset, self.rect.centery - 2 - offset)),
            self.text.get_rect(center=(self.rect.centerx + 9, self.rect.centery - 2))
        ]

        self.screen.blit(self.text_shadow, text_rects[2])
        self.screen.blit(self.text_shadow, text_rects[0])
        self.screen.blit(self.text_shadow, text_rects[1])
        self.screen.blit(self.text_shadow, text_rects[3])
        self.screen.blit(self.text, text_rects[4])

    def destroy(self):
        if self.rect.right <= 0:
            self.kill()

class Button(pygame.sprite.Sprite):
    HOVER_SOUND = f"sounds/click.mp3"
    def __init__(self, screen, text, x, y, width, height, color, hover_color, border_color, deactivated_color = (70,70,70), active = True, sound = True):
        super().__init__()

        self.screen = screen
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

        self.text = text
        self.font = pygame.font.Font(FONT, int(self.rect.height//1.5))
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.deact_color = deactivated_color
        self.active = active
        self.sound = sound
        self.delay = 0

        self.isHovered = False
    def update(self):
        mouse = pygame.mouse.get_pos()

        if self.delay > 0: self.delay -= 0.01

        if self.active:
            if self.rect.collidepoint(mouse):
                if not self.isHovered:
                    pygame.mixer.Sound(Button.HOVER_SOUND).play().set_volume(0.5)

                self.image.fill(self.hover_color)
                self.isHovered = True
            else:
                self.image.fill(self.color)
                self.isHovered = False
        else: self.image.fill(self.deact_color)
        pygame.draw.rect(self.image, self.border_color, self.image.get_rect(), 3)  # Dodajemy czarne obramowanie

        text_surface = self.font.render(self.text, False, BLACK)
        text_rect = text_surface.get_rect(center = (self.rect.centerx, self.rect.centery-2))
        self.screen.blit(text_surface, text_rect)

    def checkForInput(self):
        if self.active:
            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse) and self.delay <= 0:
                self.delay = 1
                return True
        else: return False

class Spark(pygame.sprite.Sprite):
    def __init__(self, x, y, color, screen_width, screen_height):
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

        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def update(self):
        self.x += self.speed_x
        self.y += (self.speed_y + self.gravity)
        self.rect.center = (round(self.x),round(self.y))
        self.radius -= 0.03
        self.gravity += 0.1
        if self.radius <= 0 or self.rect.centerx < 0 or self.rect.centerx > self.screen_width or self.rect.centery > self.screen_height:
            self.kill()

        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
class Sparks(pygame.sprite.Group):
    def __init__(self, screen_width, screen_height, sound=True):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sound = sound

    def create_sparks(self, x, y, size=50, color=None):
        if self.sound:
            pop = f"sounds/pop{random.randint(1, 5)}.mp3"
            pygame.mixer.Sound(pop).play().set_volume(0.5)
        for _ in range(size):
            if not color:
                color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            spark = Spark(x, y, color, self.screen_width, self.screen_height)
            self.add(spark)

class ErrorX(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_copy = pygame.image.load("graphics/Stats/X-mark.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image_copy, 0.5)
        self.image_copy = pygame.transform.scale_by(self.image_copy, 0.5)
        self.rect = self.image.get_rect(center = (WIDTH//2, 460))
        self.start_time = pygame.time.get_ticks()
        self.duration = 300  # Czas trwania efektu w milisekundach

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        # Powiększanie obrazka
        scale_factor = elapsed_time / self.duration
        if scale_factor < 0.4:
            scaled_image = pygame.transform.scale_by(self.image_copy, scale_factor)
            scaled_rect = scaled_image.get_rect(center=self.rect.center)
            self.image = scaled_image
            self.rect = scaled_rect

        # Zanikanie obrazka
        fade_duration = 400  # Czas trwania zanikania w milisekundach
        fade_alpha = int(max(255 - (elapsed_time - self.duration) / fade_duration * 255, 0))
        self.image.set_alpha(fade_alpha)

        if elapsed_time >= self.duration + fade_duration:
            self.kill()

class ErrorCircle(pygame.sprite.Sprite):
    def __init__(self, x, y, duration = 200, fade_duration = 300, red = True):
        super().__init__()
        if red:
            self.image_copy = pygame.image.load("graphics/Stats/errorCircle.png").convert_alpha()
        else:
            self.image_copy = pygame.image.load("graphics/Stats/goodCircle.png").convert_alpha()
        self.image_copy = pygame.transform.scale_by(self.image_copy, 0.5)
        self.image = self.image_copy
        self.rect = self.image.get_rect(center = (x,y))
        self.start_time = pygame.time.get_ticks()
        self.duration = duration  # Czas trwania efektu w milisekundach
        self.fade_duration = fade_duration

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        # Powiększanie obrazka
        scale_factor = elapsed_time / self.duration + 0.45
        scaled_image = pygame.transform.scale_by(self.image_copy, scale_factor)
        scaled_rect = scaled_image.get_rect(center=self.rect.center)
        self.image = scaled_image
        self.rect = scaled_rect

        # Zanikanie obrazka
        fade_alpha = int(max(255 - (elapsed_time - self.duration) / self.fade_duration * 255, 0))
        self.image.set_alpha(fade_alpha)

        if elapsed_time >= self.duration + self.fade_duration:
            self.kill()
