import pygame
import numpy as np
import math

JUMP_SPEED = 400
G = 1000
JUMP_TIME = 2 * JUMP_SPEED / G

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

rng = np.random.default_rng()

class Player:

    def __init__(self, agent=None):
        self.image = pygame.image.load('assets/dino.png')
        self.image = pygame.transform.scale_by(self.image, 0.2)
        self.rect = self.image.get_rect()
        self.rect.left = 20
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.originRect = self.rect
        self.y = 0
        self.vy = 0
        self.jumpTime = 0
        self.rotation = 0
        self.vr = 1
        self.vrDir = 1
        self.dead = False

        self.agent = agent

    def update(self, dt, cacti, speed):

        if self.agent != None:
            closest = SCREEN_WIDTH
            for cactus in cacti:
                if cactus.x < closest:
                    closest = cactus.x
            output = self.agent.runPolicy([closest, speed])
            if output[0]:
                self.jump()

        self.y += self.vy * dt
        if self.y > 0:
            self.vy -= G * dt
            self.jumpTime += dt
            self.rotation = -360 * self.jumpTime / JUMP_TIME
        else:
            self.vy = 0
            self.y = 0

            if self.rotation < 10 and self.rotation > -10:
                self.rotation += self.vr * self.vrDir

            if (self.rotation > 5 or self.rotation < -5):
                self.vrDir = -1
            if (self.rotation < -5):
                self.vrDir = 1

        if (self.rotation > 180):
            self.rotation -= 180
        if (self.rotation < -180):
            self.rotation += 180

        self.rect = self.originRect.move(0, -self.y)

        for cactus in cacti:
            if pygame.Rect.colliderect(self.rect, cactus.rect):
                self.dead = True

    def draw(self, screen):
        screen.blit(pygame.transform.rotate(self.image, self.rotation), self.rect)

    def jump(self):
        if self.y == 0:
            self.vy = JUMP_SPEED
            self.jumpTime = 0

class Cactus:

    def __init__(self, startX):
        self.image = pygame.image.load('assets/cactus.png')
        self.image = pygame.transform.scale_by(self.image, 1.0)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.originRect = self.rect
        self.x = startX

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt, speed):
        self.x -= speed * dt
        self.rect = self.originRect.move(self.x, 0)

class Game:

    def __init__(self, display=True):
        if (display):
            pygame.init()
            pygame.font.init()
            self.font = pygame.font.SysFont('Comic Sans MS', 30)

            self.running = True
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

            self.reset()

    def reset(self):
        self.clock = pygame.time.Clock()
        
        self.speed = 300
        self.score = 0

        self.ground = pygame.Rect(0, self.screen.get_height() - 10, self.screen.get_width(), 10)

        self.players = []
        # self.player = Player()
        # self.players.append(self.player)
        self.player = None

        self.cacti = []

    def addAgent(self, agent):
        self.players.append(Player(agent))

    def run(self):
        # while self.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

        self.running = False
        for player in self.players:
            if not player.dead:
                self.running = True

        if self.player != None:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                if not self.player.dead:
                    self.player.jump()
                else:
                    self.reset()

        if self.player == None or not self.player.dead:
            self.screen.fill("white")
            dt = self.clock.tick(60) / 1000

            self.speed = 300 + (self.score / 10) * 100
            for player in self.players:
                player.vr = math.floor(self.score / 10) + 1

            closestCacti = 0
            for cactus in self.cacti:
                cactus.update(dt, self.speed)
                cactus.draw(self.screen)
                if (cactus.x < -20):
                    self.cacti.remove(cactus)
                    self.score += 1
                if (cactus.x > closestCacti):
                    closestCacti = cactus.x

            for player in self.players:
                player.update(dt, self.cacti, self.speed)

            closestCacti = SCREEN_WIDTH - closestCacti + 100
            if (closestCacti > 500 and rng.random() > 5.0 / self.speed):
                self.cacti.append(Cactus(SCREEN_WIDTH + 100))

            pygame.draw.rect(self.screen, "grey", self.ground)
            for player in self.players:
                player.draw(self.screen)

            scoreText = self.font.render(str(self.score), False, (0, 0, 0))
            self.screen.blit(scoreText, (20, 20))

            pygame.display.flip()

        # pygame.quit()