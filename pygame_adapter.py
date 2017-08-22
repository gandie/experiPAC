from engine import Player
from engine import Enemy
from engine import Grid
from engine import PowerUp
import pygame
import time
import random
import json
import sys


class FieldHandler(object):

    def __init__(self, resolution=(800, 800)):

        self.resoltuion = resolution
        self.grid_size = 30
        self.field_size = resolution[0] / self.grid_size


        self.grid = Grid(size_x=self.field_size, size_y=self.field_size)
        self.load_map()

        player_field = random.choice(self.grid.fields)
        while player_field.blocked is True:
            print 'PLAYER FIELD'
            player_field = random.choice(self.grid.fields)
        self.player = Player(grid=self.grid, field=player_field)

        enemy_field = random.choice(self.grid.fields)
        while enemy_field.blocked is True:
            print 'ENEMY FIELD'
            enemy_field = random.choice(self.grid.fields)
        self.enemy = Enemy(grid=self.grid, field=enemy_field)

        powerup_field = random.choice(self.grid.fields)
        while powerup_field.blocked is True:
            print 'POWERUP FIELD'
            powerup_field = random.choice(self.grid.fields)
        self.powerup = PowerUp(grid=self.grid, field=powerup_field)
        # self.create_walls()

    def load_map(self):
        with open('pac_map.json', 'r') as save_map:
            pac_map_raw = save_map.read()
            pac_map = json.loads(pac_map_raw)
        for raw_field in pac_map:
            if raw_field['blocked'] is True:
                field = self.grid.get_field_c(
                    cx=raw_field['pos_x'],
                    cy=raw_field['pos_y']
                )
                field.blocked = True

    def create_walls(self):
        for field in self.grid.fields:
            rvalue = random.random()
            if rvalue > 0.6:
                field.blocked = True

    def click(self, pos):
        x = pos[0] / self.field_size
        y = pos[1] / self.field_size
        for field in self.grid.fields:
            if not field.x == x:
                continue
            if not field.y == y:
                continue
            field.food += 10000

    def right_click(self, pos):
        x = pos[0] / self.field_size
        y = pos[1] / self.field_size
        for field in self.grid.fields:
            if not field.x == x:
                continue
            if not field.y == y:
                continue
            if not field.blocked:
                field.blocked = True
            else:
                field.blocked = False

    def draw_fields(self, display):
        # time.sleep(0.5)
        collision = self.player.field == self.enemy.field
        if collision and self.player.powerupped is False:
            print 'GAME OVER'
            sys.exit(0)
        elif collision and self.player.powerupped is True:
            print 'WIN!'
            sys.exit(0)

        collision_powerup = self.player.field == self.powerup.field
        if collision_powerup is True:
            print 'POWERUP COLLECTED!'
            self.player.powerupped = True
            self.powerup.field = None
        for field in self.grid.fields:
            red = 0
            green = 0
            blue = 0

            field_surface = pygame.Surface(
                (self.field_size, self.field_size)
            )

            if field.home:
                green = 255

            if field.food > 0:
                red = 255

            if field.blocked:
                red = 255
                blue = 255
                green = 255

            if field == self.player.field:
                blue = 255

            if field == self.enemy.field:
                red = 255
                green = 255

            if field == self.powerup.field:
                green = 255

            pygame.draw.rect(
                field_surface,
                (red, green, blue),
                (0, 0, self.field_size, self.field_size)
            )
            field_surface = field_surface.convert()

            pos = (
                field.x * self.field_size,
                field.y * self.field_size
            )
            display.blit(field_surface, pos)

        return display


class PygameLabel(object):

    def __init__(self, text, colour, position, fontsize, fontstring):

        self.text = text
        self.colour = (colour[0],colour[1],colour[2])
        self.position = (position[0],position[1])
        if fontsize == 0:
            fontsize = 1
        self.fontsize = fontsize
        self.fontstring = fontstring

        self.draw(0)

    def draw(self, angle):

        self.font = pygame.font.Font(pygame.font.match_font(self.fontstring),
                                     self.fontsize)
        self.surface = self.font.render(self.text,True,(self.colour[0],
                                                        self.colour[1],
                                                        self.colour[2]))
        self.surface = pygame.transform.rotozoom(self.surface,
                                                 angle, 1.0)
