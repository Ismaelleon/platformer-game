import pygame
import math

class Entity:
    def __init__(self, game, pos, type, size):
        self.game = game
        self.pos = pos
        self.type = type
        self.assets = game.assets[type]
        self.flip = False
        self.frame = 0
        self.action = 'idle'
        self.size = size
        self.last_update = 0
        self.surrounding_positions = (
            (-1, -1), (0, -1), (1, -1), (2, -1),
            (-1, 0), (0, 0), (1, 0), (2, 0),
            (-1, 1), (0, 1), (1, 1), (2, 1),
            (-1, 2), (0, 2), (1, 2), (2, 2)
        )
        self.velocity = [0, 0]
        self.collisions = {
            'up': False,
            'down': False,
            'right': False,
            'left': False
        }
        self.jump = 0

    def render (self):
        frame = self.assets[self.action].subsurface(self.frame * self.size, 0, self.size, self.size)
        self.game.display.blit(pygame.transform.flip(frame, self.flip, False), self.pos)

    def animate (self):
        if self.frame * self.size < self.assets[self.action].get_width() - self.size:
            self.frame += 1
        else:
            self.frame = 0

    def surrounding_blocks (self):
        pos = [
            math.floor(self.pos[0] / self.game.tile_size),
            math.floor(self.pos[1] / self.game.tile_size),
        ]

        surrounding_blocks = []

        for block in self.game.maps[self.game.level]:
            for sur_block in self.surrounding_positions:
                if block['pos'][0] == pos[0] + sur_block[0] and block['pos'][1] == pos[1] + sur_block[1]:
                    surrounding_blocks.append(block)

        return surrounding_blocks
    
    def rect (self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

    def set_action (self, action):
        if action != self.action:
            self.frame = 0
            self.action = action

    def update (self):
        self.collisions = {
            'up': False,
            'down': False,
            'right': False,
            'left': False
        }

        if pygame.time.get_ticks() - self.last_update > 50:
            self.animate()
            self.last_update = pygame.time.get_ticks()

        self.pos[0] += self.velocity[0]
        entity_rect = self.rect()
        for block in self.surrounding_blocks():
            block_rect = pygame.Rect(block['pos'][0] * self.game.tile_size, block['pos'][1] * self.game.tile_size, block['size'], block['size'])
            if self.rect().colliderect(block_rect):
                if self.velocity[0] > 0:
                    entity_rect.right = block_rect.left
                    self.collisions['right'] = True
                if self.velocity[0] < 0:
                    entity_rect.left = block_rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += self.velocity[1]
        entity_rect = self.rect()
        for block in self.surrounding_blocks():
            block_rect = pygame.Rect(block['pos'][0] * self.game.tile_size, block['pos'][1] * self.game.tile_size, block['size'], block['size'])
            if entity_rect.colliderect(block_rect):
                if self.velocity[1] > 0:
                    entity_rect.bottom = block_rect.top
                    self.collisions['down'] = True
                    self.jump = 0
                if self.velocity[1] < 0:
                    entity_rect.top = block_rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(10, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

class Player (Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, 'player', size)
        self.keys = {
            'left': False,
            'right': False
        }

    def events (self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.keys['right'] = True
                elif event.key == pygame.K_a:
                    self.keys['left'] = True

                if event.key == pygame.K_w:
                    self.velocity[1] = -3
                    if self.jump == 0:
                        self.set_action('jump')
                    elif self.jump == 1:
                        self.set_action('double_jump')
                    self.jump += 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.keys['right'] = False 
                elif event.key == pygame.K_a:
                    self.keys['left'] = False 

    def update (self):
        super().update()
        self.events()

        if self.keys['right']:
            self.velocity[0] = 2
            self.flip = False 
            if round(self.velocity[1]) == 0:
                self.set_action('run')
            elif self.jump == 0:
                self.set_action('fall')
        elif self.keys['left']:
            self.velocity[0] = -2
            self.flip = True
            if round(self.velocity[1]) == 0:
                self.set_action('run')
            elif self.jump == 0:
                self.set_action('fall')
        else:
            self.velocity[0] = 0
            if round(self.velocity[1]) == 0:
                self.set_action('idle')
            elif self.velocity[1] < 0 and self.jump == 0:
                self.set_action('jump')
            elif self.velocity[1] > 0 and self.jump == 0:
                self.set_action('fall')

