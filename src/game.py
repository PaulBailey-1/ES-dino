import pygame
import numpy as np

JUMP_SPEED = 400
G = 1000
JUMP_TIME = 2 * JUMP_SPEED / G

rng = np.random.default_rng()

class Player:

    def __init__(self):
        self.image = pygame.image.load('assets/dino.png')
        self.image = pygame.transform.scale_by(self.image, 0.2)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = -10
        self.y = 0
        self.vy = 0
        self.jumpTime = 0
        self.rotation = 0
        self.vr = 1
        self.vrDir = 1
        self.dead = False

    def draw(self, screen):
        screen.blit(pygame.transform.rotate(self.image, self.rotation), self.rect.move(20, screen.get_height() - self.y))

    def jump(self):
        if self.y == 0:
            self.vy = JUMP_SPEED
            self.jumpTime = 0

    def update(self, dt, cacti):
        self.y += self.vy * dt
        if self.y > 0:
            self.vy -= G * dt
            self.jumpTime += dt
            self.rotation = -360 * self.jumpTime / JUMP_TIME
        else:
            self.vy = 0
            self.y = 0

            self.rotation += self.vr * self.vrDir
            if (self.rotation > 180):
                self.rotation -= 180
            if (self.rotation < -180):
                self.rotation += 180
            if (self.rotation > 5 or self.rotation < -5):
                self.vrDir = -1
            if (self.rotation < -5):
                self.vrDir = 1

        for cactus in cacti:
            if self.rect.colliderect(cactus.rect):
                self.dead = True

class Cactus:

    def __init__(self, startX):
        self.image = pygame.image.load('assets/cactus.png')
        self.image = pygame.transform.scale_by(self.image, 1.0)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = -10
        self.x = startX

    def draw(self, screen):
        screen.blit(self.image, self.rect.move(self.x, screen.get_height()))

    def update(self, dt, speed):
        self.x -= speed * dt

class Game:

    def __init__(self, display=True):
        if (display):
            pygame.init()
            pygame.font.init()
            self.font = pygame.font.SysFont('Comic Sans MS', 30)

            self.running = True
            self.screen = pygame.display.set_mode((600, 400))

            self.reset()

    def reset(self):
        self.clock = pygame.time.Clock()
        
        self.speed = 300
        self.score = 0

        self.ground = pygame.Rect(0, self.screen.get_height() - 10, self.screen.get_width(), 10)
        self.player = Player()
        self.cacti = []

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if not self.player.dead:
                    self.player.jump()
                else:
                    self.reset()

            if not self.player.dead:
                self.screen.fill("white")
                dt = self.clock.tick(60) / 1000

                closestCacti = 0
                for cactus in self.cacti:
                    cactus.update(dt, self.speed)
                    cactus.draw(self.screen)
                    if (cactus.x < -20):
                        self.cacti.remove(cactus)
                        self.score += 1
                    if (cactus.x > closestCacti):
                        closestCacti = cactus.x

                closestCacti = self.screen.get_width() - closestCacti + 100
                if (closestCacti > 300 and rng.random() < 5.0 / self.speed):
                    self.cacti.append(Cactus(self.screen.get_width() + 100))

                self.player.update(dt, self.cacti)

                pygame.draw.rect(self.screen, "grey", self.ground)
                self.player.draw(self.screen)

                scoreText = self.font.render(str(self.score), False, (0, 0, 0))
                self.screen.blit(scoreText, (20, 20))

                pygame.display.flip()


        pygame.quit()