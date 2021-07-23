from pygame.sprite import Sprite
from enemy import Enemy
import pygame, sys
from player import *
from barrier import *
from config import *
from sprites import *
from ground import *
from button import *
from attacks import *


# main game class
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.font = pygame.font.Font('Tomatoes-O8L8.ttf', 64)
        self.clock = pygame.time.Clock()
        self.running = True

        # sprite sheets
        self.character_spritesheet = Spritesheet('img/hero.png')
        self.grass_spritesheet = Spritesheet('img/grass-tile.png')
        self.barrier_spritesheet = Spritesheet('img/tiles-map.png')
        self.enemy_spritesheet = Spritesheet('img/roguelikecreatures.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.intro_background = pygame.image.load('img/tiles-map.png')
        self.go_background = pygame.image.load('img/tiles-map.png')

    def create_tile_map(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Barrier(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    Player(self, j, i)

    def intro_screen(self):
        intro = True

        title = self.font.render('My Game', True, RED)
        title_rect = title.get_rect(x=200,y=10)
        play_button = Button(25,550,100,50, RED, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.intro_background = pygame.transform.scale(self.intro_background, (WIN_WIDTH, WIN_HEIGHT))
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.barrier = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        # self.players = pygame.sprite.LayeredUpdates()

        self.create_tile_map()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
    
    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(WIN_WIDTH/2, WIN_HEIGHT - 90, 120, 50, RED, BLUE, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            # self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()
while g.running is True:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()