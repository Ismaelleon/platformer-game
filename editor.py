import pygame
import os
import sys
import math
import json
from scripts.utils import load_image

class Editor:
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.surface.Surface((320, 240))
        self.crop_pos = [0, 0]
        self.level = 0
        self.assets = {
            'background': load_image('Background/Yellow.png'),
            'terrain': load_image('terrain.png')
        }
        self.tile_size = 16
        map_file = open('maps.json', 'r')
        self.maps = json.load(map_file)['maps']
        self.pressed = [False, False]
        
    def render(self):
        self.display.fill((0, 0, 0))
        pygame.display.update()

        for block in self.maps[self.level]:
            block_img = self.assets[block['asset']].subsurface(block['rect'])
            self.display.blit(block_img, (block['pos'][0] * block['size'], block['pos'][1] * block['size']))

        actual_asset = self.assets['terrain'].subsurface(self.crop_pos[0], self.crop_pos[1], self.tile_size, self.tile_size)
        self.display.blit(actual_asset, (0, 0))

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

    def events (self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and self.crop_pos[0] < self.assets['terrain'].get_width() - self.tile_size:
                    self.crop_pos[0] += self.tile_size
                if event.key == pygame.K_a and self.crop_pos[0] > 0:
                    self.crop_pos[0] -= self.tile_size

                if event.key == pygame.K_s and self.crop_pos[1] < self.assets['terrain'].get_height() - self.tile_size:
                    self.crop_pos[1] += self.tile_size
                if event.key == pygame.K_w and self.crop_pos[1] > 0:
                    self.crop_pos[1] -= self.tile_size

                if event.key == pygame.K_PLUS:
                    if len(self.maps) - 1 < self.level + 1:
                        self.maps.append([]) 

                    self.level += 1
                if event.key == pygame.K_MINUS:
                    if self.level > 0:
                        self.level -= 1

                if event.key == pygame.K_RETURN:
                    maps_dict = {'maps': self.maps}
                    maps_json = json.dumps(maps_dict)

                    f = open('maps.json', 'w')
                    f.write(maps_json)
                    f.close()

                    pygame.quit()
                    sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.pressed[0] = True
                if event.button == 3:
                    self.pressed[1] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.pressed[0] = False 
                if event.button == 3:
                    self.pressed[1] = False 

    def update (self):
        pos = list(pygame.mouse.get_pos())
        pos[0] = math.floor(pos[0] / 32)
        pos[1] = math.floor(pos[1] / 32)

        if self.pressed[0]:
            repeated = False 
            for index, block in enumerate(self.maps[self.level]):
                if block['pos'][0] == pos[0] and block['pos'][1] == pos[1]:
                    repeated = True 

            if not repeated:
                self.maps[self.level].append({
                    'pos': pos,
                    'asset': 'terrain',
                    'rect': (self.crop_pos[0], self.crop_pos[1], self.tile_size, self.tile_size),
                    'size': self.tile_size 
                })
        elif self.pressed[1]:
            for index, block in enumerate(self.maps[self.level]):
                if block['pos'][0] == pos[0] and block['pos'][1] == pos[1]:
                    self.maps[self.level].pop(index)

    def run (self):
        while True:
            self.render()
            self.update()
            self.events()

Editor().run()
