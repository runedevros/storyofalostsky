from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame
from random import randint



class SpearEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        delay = 5
        max_emissions = 15
        start_delay = 16

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'spear_yellow.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)


    def emit(self):

        position = (randint(120, 320), randint(150, 350))

        self.bullets.add(Bullet(position, self.image, 10, 0))


class LeafEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        delay = 2
        max_emissions = 30
        start_delay = 5

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'crystal_green.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)


    def emit(self):

        position = (1, randint(50, 450))

        self.bullets.add(Bullet(position, self.image, 10, 0))



class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [SpearEmitter(self.bullet_group, (220, 250)),
                         LeafEmitter(self.bullet_group, (220, 250)),
                         ]

        self.sfx_timings = [(15, 'shoot6')]