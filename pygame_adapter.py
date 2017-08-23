from engine import Player
from engine import Enemy
from engine import Grid
from engine import PowerUp
import pygame
import time
import random
import json
import sys

ENEMY_COUNT = 5


class FieldHandler(object):

    def __init__(self, resolution=(800, 800)):

        self.resoltuion = resolution
        self.grid_size = 30
        self.field_size = resolution[0] / self.grid_size
        self.cur_time = 0
        self.powerup_time = None
        self.game_running = False
        self.window_running = False

        self.grid = Grid(size_x=self.field_size, size_y=self.field_size)
        self.load_map()

        self.player = Player(
            grid=self.grid,
            field=self.get_unblocked_field()
        )

        self.powerup = PowerUp(
            grid=self.grid,
            field=self.get_unblocked_field()
        )

        self.enemies = []
        for i in xrange(ENEMY_COUNT):
            enemy = self.create_ghost()
            self.enemies.append(enemy)

    def get_unblocked_field(self):
        '''
        get a field which is not blocked
        '''
        field = random.choice(self.grid.fields)
        while field.blocked is True:
            print 'POWERUP FIELD'
            field = random.choice(self.grid.fields)
        return field

    def create_ghost(self):
        enemy = Enemy(
            grid=self.grid,
            field=self.get_unblocked_field()
        )
        return enemy

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

    def check_collision(self):
        # time.sleep(0.5)
        #collision = self.player.field in enemy_fields
        dead_enemies = []
        for enemy in self.enemies:
            collision = self.player.field == enemy.field

            if collision and self.player.powerupped is False:
                print 'GAME OVER!'
                self.game_running = False
                game_over_label = PygameLabel('GAME OVER', (255,0,0), (300, 400), 100, 'Arial')
                # pygame_main.END_LABEL = game_over_label
                # sys.exit(0)
            elif collision and self.player.powerupped is True:
                self.player.kills += 1
                self.player.powerupped = False
                dead_enemies.append(enemy)

        for enemy in dead_enemies:
            self.enemies.remove(enemy)

        if self.player.kills == ENEMY_COUNT:
            with open('highscore.json', 'a') as highscore_file:
                highscore_file.write(str(self.cur_time) + '\n')
            print 'WIN!'
            sys.exit(0)

        collision_powerup = self.player.field == self.powerup.field
        if collision_powerup is True:
            print 'POWERUP COLLECTED!'
            self.player.powerupped = True
            self.powerup_time = time.time()
            self.powerup.field = self.get_unblocked_field()

    def draw_fields(self, display):
        enemy_fields = [enemy.field for enemy in self.enemies]

        for field in self.grid.fields:
            red = 0
            green = 0
            blue = 0

            field_surface = pygame.Surface(
                (self.field_size, self.field_size)
            )

            if field.blocked:
                red = 255
                blue = 255
                green = 255

            if field == self.player.field:
                if self.player.powerupped:
                    if self.ticks % 2 == 0:
                        red = 255
                    else:
                        blue = 255
                else:
                    blue = 255

            if field in enemy_fields:
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
