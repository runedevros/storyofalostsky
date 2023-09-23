__author__ = 'Fawkes'

import pygame
import os
from pygame.locals import *
from sys import exit

def main():

    pygame.init()


    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    tilesize = 35
    size_x = 5
    size_y = 5
    size_window = (size_x,size_y)
    screen_size = (tilesize*size_x,tilesize*size_y)
    screen =  pygame.display.set_mode(screen_size,0, 32)
    clock = pygame.time.Clock()

    terrain_tiles = pygame.image.load(os.path.join('images', 'terraintilesv4.png')).convert_alpha()
    house = pygame.image.load(os.path.join('images', 'landmarks.png')).convert_alpha().subsurface((70, 35, 35, 35))

    font = pygame.font.Font('VeraSeBd.ttf', 16)

    grass_tiles = terrain_tiles.subsurface((0, 70, 35, 35))

    fog_tile = pygame.Surface((35*5, 35*2), SRCALPHA)
    fog_tile.fill((60, 60, 60))

    caption = font.render('BLEND_ADD', True, (0, 0, 0))

    while True:

        for event in pygame.event.get():

            if event.type == QUIT:
                exit()

        for x in xrange(0, size_x):
            for y in xrange(0, size_y):

                screen.blit(grass_tiles, (35*x, 35*y))

        screen.blit(house, (30, 30))
        screen.blit(house, (30, 70))
        screen.blit(fog_tile, (0, 0), special_flags = BLEND_ADD)
        screen.blit(caption, (10, 140))

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()