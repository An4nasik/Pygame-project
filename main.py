import pygame
from pygame import *
import os
import sys
import random

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    pygame.display.flip()
    running = True


    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image
fps = 60
MYEVENTTYPE = pygame.USEREVENT + 1
Enemy_generation_event = pygame.USEREVENT + 2
pygame.time.set_timer(Enemy_generation_event, 2000)
pygame.time.set_timer(MYEVENTTYPE, fps)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
attackers = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
font.init()
path = font.match_font("arial")
Font = font.Font(path, 25)
GRAVITY = 5
screen_rect = (0, 0, width, height)

class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [transform.scale(load_image("zap.webp"), (7, 7))]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

class Live(pygame.sprite.Sprite):
    image = transform.scale(load_image("heart.png"), (30, 30))

    def __init__(self, i):
        super().__init__(all_sprites)
        self.image = Live.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 60 - i * 30, 0


class Hero(pygame.sprite.Sprite):
    image = transform.scale(load_image("hero.png"), (50, 50))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect((0, 0), (50, 50))
        self.rect.x = width // 2 - 35
        self.rect.y = height // 2 - 35


class Enemy(sprite.Sprite):
    lives = 5
    image = transform.scale(load_image("fireball.png"), (20, 20))
    score = 0

    def __init__(self):
        super().__init__(attackers)
        self.image = Enemy.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        z = True
        self.lives = 5
        self.ticks = fps - 10
        self.go = False
        i = 0
        if len(attackers) >= 2:
            while z:
                marks = [True]
                self.rect.x = random.randrange(width)
                self.rect.y = random.randrange(height)
                if self.rect.x in range(sprite.rect.x - 100, sprite.rect.x + 100) and self.rect.y in range(
                        sprite.rect.y - 100, sprite.rect.y + 100):
                    marks.append(False)
                if all(marks):
                    z = False

    def attack(self):
        if self.go:
            y = self.rect.y
            x = self.rect.x
            new_x, new_y = sprite.rect.x + 10, sprite.rect.y + 10
            horizontal_move = True
            v_speed = (new_y - y) // 10
            h_speed = (new_x - x) // 10
            if horizontal_move and y - 10 >= new_y and v_speed < 0:
                y = y - 10
            if horizontal_move and y + 10 <= new_y and v_speed > 0:
                y = y + 10
            else:
                if x - 10 >= new_x and h_speed < 0:
                    x = x - 10
                if x + 10 <= new_x and h_speed > 0:
                    x = x + 10
            self.rect.x, self.rect.y = x, y
            if x in range(new_x - 10, new_x + 10) and y in range(new_y - 10, new_y + 10):
                self.kill()
                if len(all_sprites) == 0:
                    pygame.quit()
                for x in all_sprites:
                    x.kill()
                    break

    def click(self):
        self.lives -= 1
        if self.lives <= 0:
            Enemy.score = Enemy.score + 10
            create_particles((self.rect.x, self.rect.y))
            self.kill()

    def tick(self):
        self.ticks -= 1
        if self.ticks <= 0:
            self.go = True

    def hide(self):
        self.image.fill((255, 255, 255))

def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

for i in range(3):
    all_sprites.add(Live(i))
sprite = Hero()
hero_group.add(sprite)
all_sprites.draw(screen)
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MYEVENTTYPE:
            screen.fill((255, 255, 255))
            all_sprites.draw(screen)
            all_sprites.update()
            attackers.draw(screen)
            hero_group.draw(screen)
            text = f'Счет: {Enemy.score}'
            a = Font.render(text, 1, (100, 100, 100))
            screen.blit(a, (350, 0))
            first = True
            for x in attackers:
                if not first:
                    x.tick()
                    x.attack()
                else:
                    first = False
            pygame.display.flip()
        if event.type == MOUSEBUTTONDOWN:
            for x in attackers:
                cor_x = event.pos[0]
                cor_y = event.pos[1]
                if cor_x in range(x.rect.x, x.rect.x + 20) and cor_y in range(x.rect.y, x.rect.y + 20):
                    x.click()
        if event.type == Enemy_generation_event:
            attackers.add(Enemy())
        all_sprites.draw(screen)
        pygame.display.flip()

pygame.quit()
