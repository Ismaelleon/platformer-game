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
        self.fullscreen = False
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
        self.option = 0
        self.options_quantity = 2
        self.options = {
            'fullscreen': False
        }

        maps_file = open('maps.json'.format(self.level), 'r')
        self.maps = json.load(maps_file)['maps']

        pygame.display.set_caption('Platformer')

    def toggle_fullscreen (self):
        self.options['fullscreen'] = not self.options['fullscreen']

        if self.options['fullscreen'] == True:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((960, 544))

    def set_state(self, state):
        if state == 'main-menu':
            self.state = 'main-menu'
            self.options_quantity = 2
        elif state == 'game':
            self.state = 'game'
            self.options_quantity = 0
        elif state == 'options':
            self.state = 'options'
            self.options_quantity = 1

        self.option = 0
            

    def render (self):
        pygame.display.update()

        WHITE = (255, 255, 255)
        GRAY = (150, 150, 150)
        BLACK = (0, 0, 0)
        font = ASSETS_BASE_PATH + 'font.ttf'

        if self.state == 'main-menu':
            self.display.fill(BLACK)

            title = render_text('Platformer', font, WHITE, 32)
            play_btn = render_text('Play', font, WHITE if self.option == 0 else GRAY, 16)
            options_btn = render_text('Options', font, WHITE if self.option == 1 else GRAY, 16)
            quit_btn = render_text('Quit', font, WHITE if self.option == 2 else GRAY, 16)

            self.display.blit(title, (self.display.get_width() / 2 - title.get_width() / 2, title.get_height()))
            self.display.blit(play_btn, (self.display.get_width() / 2 - play_btn.get_width() / 2, self.display.get_height() / 2))
            self.display.blit(options_btn, (self.display.get_width() / 2 - options_btn.get_width() / 2, self.display.get_height() / 2 + 25))
            self.display.blit(quit_btn, (self.display.get_width() / 2 - quit_btn.get_width() / 2, self.display.get_height() / 2 + 50))
        elif self.state == 'options':
            self.display.fill(BLACK)

            title = render_text('Options', font, WHITE, 32)
            fullscreen_option = render_text('Fullscreen', font, WHITE if self.option == 0 else GRAY, 16)
            fullscreen_state = render_text('On' if self.options['fullscreen'] == True else 'Off', font, WHITE if self.option == 0 else GRAY, 16)

            back_btn = render_text('Back', font, WHITE if self.option == 1 else GRAY, 16)

            self.display.blit(title, (self.display.get_width() / 2 - title.get_width() / 2, title.get_height()))
            self.display.blit(fullscreen_option, (25, title.get_height() + 50))
            self.display.blit(fullscreen_state, (self.display.get_width() - fullscreen_state.get_width() - 25, title.get_height() + 50))
            self.display.blit(back_btn, (25, self.display.get_height() - back_btn.get_height() - 25))

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
                if event.key == pygame.K_s:
                    if self.state == 'main-menu' or self.state == 'options':
                        if self.option < self.options_quantity:
                            self.option += 1
                        else:
                            self.option = 0
                
                if event.key == pygame.K_w:
                    if self.state == 'main-menu' or self.state == 'options':
                        if self.option > 0:
                            self.option -= 1
                        else:
                            self.option = self.options_quantity

                if event.key == pygame.K_RETURN:
                    if self.state == 'main-menu':
                        if self.option == 0:
                            self.set_state('game')
                        elif self.option == 1:
                            self.set_state('options')
                        else:
                            pygame.quit()
                            sys.exit()

                    elif self.state == 'options':
                        if self.option == 0:
                            self.toggle_fullscreen()

                        if self.option == self.options_quantity:
                            self.set_state('main-menu')

                    self.option = 0

    def run (self):
        while True:
            self.render()
            self.update()
            self.events()
            self.clock.tick(60)
