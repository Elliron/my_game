import pygame
from config import *

class Barrier(pygame.sprite.Sprite):
        def __init__(self, game, x, y):
            self.game = game
            self._layer = BARRIER_LAYER
            self.groups = self.game.all_sprites, self.game.barrier, self.game.player_barrier
            pygame.sprite.Sprite.__init__(self, self.groups)

            self.x = x * TILESIZE
            self.y = y * TILESIZE
            self.width = TILESIZE
            self.height = TILESIZE

            self.image = self.game.barrier_spritesheet.get_sprite(16, 160, self.width/2, self.height/2)
            self.image = pygame.transform.scale(self.image, (32,32))

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y