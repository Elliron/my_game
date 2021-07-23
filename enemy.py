import pygame
import random
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.movement_loop = 0
        self.maximum_travel = random.randint(20, 60)

        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width/2, self.height/2)
        self.image = pygame.transform.scale(self.image, (32,32))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.current_health = ENEMY_CURRENT_HEALTH
        self.max_health = ENEMY_MAX_HEALTH

    def update(self):
        self.movement()
        self.basic_health()

        self.rect.x += self.x_change
        self.collide_barrier('x')
        self.collide_player('x')
        # self.collide_attacks('x')
        self.rect.y += self.y_change
        self.collide_barrier('y')
        self.collide_player('y')
        # self.collide_attacks('y')
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.maximum_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.maximum_travel:
                self.facing = 'left'

    # def collide_attacks(self, direction):
    #     if direction == "x":
    #         hits = pygame.sprite.spritecollide(self, self.game.attacks, False)
    #         if hits:
    #             if self.x_change > 0:
    #                 for sprite in self.game.enemies:
    #                     sprite.rect.x += ENEMY_SPEED
    #                 self.rect.x = hits[0].rect.left - self.rect.width
    #             if self.x_change < 0:
    #                 for sprite in self.game.enemies:
    #                     sprite.rect.x -= ENEMY_SPEED
    #                 self.rect.x = hits[0].rect.right

    #     if direction == 'y':
    #         hits = pygame.sprite.spritecollide(self, self.game.attacks, False)
    #         if hits:
    #             if self.y_change > 0:
    #                 for sprite in self.game.enemies:
    #                     sprite.rect.y += ENEMY_SPEED
    #                 self.rect.y = hits[0].rect.top - self.rect.height
    #             if self.y_change < 0:
    #                 for sprite in self.game.enemies:
    #                     sprite.rect.y -= ENEMY_SPEED
    #                 self.rect.y = hits[0].rect.bottom

    def collide_player(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.players, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.enemies:
                        sprite.rect.x += ENEMY_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.enemies:
                        sprite.rect.x -= ENEMY_SPEED
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.players, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.enemies:
                        sprite.rect.y += ENEMY_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.enemies:
                        sprite.rect.y -= ENEMY_SPEED
                    self.rect.y = hits[0].rect.bottom
    
    def collide_barrier(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.barrier, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.enemies:
                        sprite.rect.x += ENEMY_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.enemies:
                        sprite.rect.x -= ENEMY_SPEED
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.barrier, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.enemies:
                        sprite.rect.y += ENEMY_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.enemies:
                        sprite.rect.y -= ENEMY_SPEED
                    self.rect.y = hits[0].rect.bottom

    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
            self.kill()
            self.game.playing = False

    def get_health(self, amount):
        if self.current_health < self.max_health:
            self.current_health += amount
        if self.current_health >= self.max_health:
            self.current_health = self.max_health

    def basic_health(self):
        pygame.draw.line(self.image, GREEN, (0,30),(0, 30) , self.current_health)
        if self.current_health < self.max_health / 2:
            pygame.draw.line(self.image, YELLOW, (0,30),(0, 30) , self.current_health)

        if self.current_health < self.max_health / 4:
            pygame.draw.line(self.image, RED, (0,30),(0, 30) , self.current_health)