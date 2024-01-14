import pygame
import json
import sys
from scripts.utils import render_text, load_image, ASSETS_BASE_PATH
from scripts.entities import Player


class Game:
    def __init__(self):
        self.state = 'main-menu'
        self.screen = pygame.display.set_mode((960, 544))
        self.display = pygame.surface.Surface((480, 272))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(ASSETS_BASE_PATH + 'font.ttf', 64)
        self.assets = {
            'background': load_image('Background/Yellow.png'),
            'terrain': load_image('terrain.png'),
            'player': {
                'idle': load_image('Main Characters/Ninja Frog/Idle (32x32).png'),
                'run': load_image('Main Characters/Ninja Frog/Run (32x32).png'),
                'jump': load_image('Main Characters/Ninja Frog/Jump (32x32).png'),
                'fall': load_image('Main Characters/Ninja Frog/Fall (32x32).png'),
                'double_jump': load_image('Main Characters/Ninja Frog/Double Jump (32x32).png'),
                'wall_jump': load_image('Main Characters/Ninja Frog/Wall Jump (32x32).png'),
                'hit': load_image('Main Characters/Ninja Frog/Hit (32x32).png')
            }
        }
        self.offset = [0, -64]
        self.level = 0
        self.player = Player(self, [32, 128], 32)
        self.tile_size = 16

        maps_file = open('maps.json'.format(self.level), 'r')
        self.maps = json.load(maps_file)['maps']

        pygame.display.set_caption('Platformer')

    def render (self):
        pygame.display.update()

        if self.state == 'main-menu':
            WHITE = (255, 255, 255)
            title = render_text('Platformer', ASSETS_BASE_PATH + 'font.ttf', WHITE, 32)
            play_btn = render_text('Play', ASSETS_BASE_PATH + 'font.ttf', WHITE, 16)

            self.display.blit(title, (self.display.get_width() / 2 - title.get_width() / 2, title.get_height()))
            self.display.blit(play_btn, (self.display.get_width() / 2 - play_btn.get_width() / 2, self.display.get_height() / 2))
        elif self.state == 'game':
            for y in range(9):
                for x in range(10):
                    self.display.blit(self.assets['background'], (self.offset[0] + x * self.assets['background'].get_width(), self.offset[1] + y * self.assets['background'].get_height()))

            for block in self.maps[self.level]:
                block_img = self.assets[block['asset']].subsurface(block['rect'])
                self.display.blit(block_img, (block['pos'][0] * block['size'], block['pos'][1] * block['size']))

            self.player.render()

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            
    def update (self):
        if self.state == 'game':
            # Update background position
            if self.offset[1] < 0:
                self.offset[1] += 0.5
            else:
                self.offset[1] = -64

            self.player.update()


    def events (self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.state == 'main-menu':
                    self.state = 'game'

    
    def run (self):
        while True:
            self.render()
            self.update()
            self.events()
            self.clock.tick(60)
