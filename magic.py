import pygame, math
from config import *

class Magic(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.magic, self.game.player_barrier
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.image = self.game.magic_spritesheet.get_sprite(0, 8, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.fire()
        self.collide()
        
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()

    def fire(self):
        direction = self.game.player.facing
        if -10 < self.rect.x < 710:
            if direction == "right":
                self.image = self.game.magic_spritesheet.get_sprite(8, 264, self.width * 2, self.height * 2)
                self.rect.move_ip(12, 0)
            if direction == "left":
                self.image = self.game.magic_spritesheet.get_sprite(0, 0, self.width * 2, self.height * 2)
                self.rect.move_ip(-12, 0)
            if direction == "up":
                self.image = self.game.magic_spritesheet.get_sprite(8, 104, self.width * 2, self.height * 2)
                self.rect.move_ip(0, -12)
            if direction == "down":
                self.image = self.game.magic_spritesheet.get_sprite(8, 384, self.width * 2, self.height * 2)
                self.rect.move_ip(0, 12)
        else:
            self.kill()




        # for sprite in self.game.all_sprites:
        #     sprite.rect.x += MAGIC_SPEED
        #     sprite.rect.y += MAGIC_SPEED