import pygame
from pygame_adapter import FieldHandler
from pygame_adapter import PygameLabel
import json
import time
import sys
import random

FPS = 100

LEFT=1 # left mouse button
MIDDLE=2
RIGHT=3 # ...
WHEELUP=4
WHEELDOWN=5

GAME_TIME = 60
enemy_movement = 5
UP_TIME = 5

END_LABEL = None

def main():

    pygame.init()

    resolution = (800, 800)

    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("experiPAC - BETA")
    pygame.mouse.set_visible(1)
    pygame.font.init()

    fontlist = pygame.font.get_fonts()
    font = random.choice(fontlist)


    # frame limiter
    clock = pygame.time.Clock()

    fieldhandler = FieldHandler(
        resolution=resolution
    )

    fieldhandler.ticks = 0

    label = PygameLabel('Time:', (255, 255, 255), (700, 0), 20, font)

    fieldhandler.game_running = True
    fieldhandler.window_running = True
    start_time = time.time()

    while fieldhandler.window_running is True:

        if fieldhandler.game_running is True:

            fieldhandler.cur_time = (start_time - time.time()) * (-1)
            #print round(fieldhandler.cur_time, 2)
            if fieldhandler.cur_time > GAME_TIME:
                label.text = 'GAME OVER!'
            else:
                label.text = str(round(fieldhandler.cur_time, 2))

            fieldhandler.ticks += 1
            clock.tick(FPS)
            background = pygame.Surface(resolution)
            background.fill((0,0,0))
            background = background.convert()

            # temporary surface to draw things to
            display = pygame.Surface(resolution)
            display.fill((0,0,0))
            display = display.convert()

            display.blit(background, (0,0))

            # put display to draw method
            fieldhandler.check_collision()
            display = fieldhandler.draw_fields(display)
            #label.text = str(round(cur_time, 2))
            label.draw(0)
            display.blit(label.surface, (label.position[0], label.position[1]))

            #if END_LABEL is not None:
            #    display.blit(END_LABEL.surface, (END_LABEL.position[0], END_LABEL.position[1]))

            screen.blit(display, (0,0))

            #    fieldhandler.enemy.move()
            if fieldhandler.ticks % enemy_movement == 0:
                for enemy in fieldhandler.enemies:
                    enemy.move()

            if fieldhandler.powerup_time is not None:
                if time.time() - fieldhandler.powerup_time > UP_TIME:
                    fieldhandler.player.powerupped = False
                    fieldhandler.powerup_time = None

        # look for events
        for event in pygame.event.get():

            # quit game
            if event.type == pygame.QUIT:
                pac_map = []
                for field in fieldhandler.grid.fields:
                    field_d = {
                        'pos_x': field.x,
                        'pos_y': field.y,
                        'blocked': field.blocked
                    }
                    pac_map.append(field_d)
                pac_map_json = json.dumps(pac_map)
                with open('pac_map.json', 'w') as save_map:
                    save_map.write(pac_map_json)

                fieldhandler.window_running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                fieldhandler.right_click(event.pos)
                print('right mouse button')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    fieldhandler.player.move(x_dir=0, y_dir=-1)
                if event.key == pygame.K_DOWN:
                    fieldhandler.player.move(x_dir=0, y_dir=1)
                if event.key == pygame.K_LEFT:
                    fieldhandler.player.move(x_dir=-1, y_dir=0)
                if event.key == pygame.K_RIGHT:
                    fieldhandler.player.move(x_dir=1, y_dir=0)

        pygame.display.flip()
        time.sleep(0.1)

if __name__ == '__main__':
    # run main programm
    main()
