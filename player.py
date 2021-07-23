import pygame, math, random
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE / 2
        self.height = TILESIZE / 2



        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1
        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (32,32))
        self.image.set_colorkey(WHITE)

        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.current_health = PLAYER_CURRENT_HEALTH
        self.max_health = PLAYER_MAX_HEALTH

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

    def update(self):
        self.movement()
        self.animate()
        # self.advanced_health()
        self.basic_health()

        self.rect.x += self.x_change
        self.collide_barrier('x')
        self.collide_enemy('x')
        self.rect.y += self.y_change
        self.collide_barrier('y')
        self.collide_enemy('y')
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_barrier(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.barrier, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.barrier, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom

    def collide_enemy(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.get_damage(ENEMY_DAMAGE)

    def animate(self):
        # load in all of the animations
        down_animations = [self.game.character_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(16, 32, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 32, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(0, 16, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(16, 16, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(32, 16, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(16, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(16, 0, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height)]

        # if we hit the down arrow key
        if self.facing == "down":
            # if standing still
            if self.y_change == 0:
            # load the image that is facing down from the character spritesheet
                self.image = self.game.character_spritesheet.get_sprite(0, 32, self.width, self.height)
                self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
                self.image.set_colorkey(WHITE)
            else:
                # if moving, load image from the down animations list
                self.image = down_animations[math.floor(self.animation_loop)]
                self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
                self.image.set_colorkey(WHITE)
                # starts with the first image in the list and loops through adding .1 every frame, completes 1, 2, or 3 every 10 frames going through a new image.
                self.animation_loop += 0.1
                # resets image list to the first image if we reach the last image
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 16, self.width, self.height)
                self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
                self.image.set_colorkey(WHITE)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
                self.image.set_colorkey(WHITE)
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
                self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
                self.image.set_colorkey(WHITE)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
                self.image.set_colorkey(WHITE)
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
                self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
                self.image = pygame.transform.flip(self.image, True, False)
                self.image.set_colorkey(WHITE)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
                self.image = pygame.transform.flip(self.image, True, False)
                self.image.set_colorkey(WHITE)
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1  