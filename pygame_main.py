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

    ticks = 0

    label = PygameLabel('Time:', (255, 255, 255), (700, 0), 20, font)

    running = True
    start_time = time.time()

    while running:

        cur_time = (start_time - time.time()) * (-1)
        print cur_time
        if cur_time > GAME_TIME:
            label.text = 'GAME OVER!'
            print 'foo'
        else:
            label.text = str(round(cur_time, 2))

        ticks += 1
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
        display = fieldhandler.draw_fields(display)
        #label.text = str(round(cur_time, 2))
        label.draw(0)
        display.blit(label.surface, (label.position[0], label.position[1]))

        screen.blit(display, (0,0))

        if ticks % 10 == 0:
            fieldhandler.enemy.move()

        if ticks % 100 == 0:
            print 'POWERUP'

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

                running = False

            '''
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                #click_x = event.pos[0]
                #click_y = event.pos[1]
                fieldhandler.click(event.pos)
                print('left mouse button')
            '''
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
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
