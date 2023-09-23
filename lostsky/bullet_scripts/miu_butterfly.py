from lostsky.battle.bullet_sys import MovingEmitter, Emitter, Bullet, BulletScript
from random import randint
import os
import pygame

class DustEmitter(MovingEmitter):

    def __init__(self, bullet_group, initial_position):
        delay = 15
        max_emissions = 10
        start_delay = 0
        speed = 4
        angle = 0

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'smallorb_yellow.png')).convert_alpha()

        MovingEmitter.__init__(self, bullet_group, initial_position,
                               delay, max_emissions, start_delay, speed, angle)

    def emit(self):
        self.bullets.add(Bullet(self.position, self.bullet_img, 3+randint(0,2), 95+randint(0,15)))

class ButterflyEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, color):
        delay = 15
        max_emissions = 1
        start_delay = 5

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'butterfly_'+color+'.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        self.bullets.add(Bullet(self.position, self.image, 4, 0))


class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 260
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [ButterflyEmitter(self.bullet_group, (200, 220), 'blue'),
                         DustEmitter(self.bullet_group, (200, 200)),
                         ButterflyEmitter(self.bullet_group, (240, 180), 'orange'),
                         DustEmitter(self.bullet_group, (240, 180)),
                         ButterflyEmitter(self.bullet_group, (280, 140), 'magenta'),
                         DustEmitter(self.bullet_group, (280, 160)),

                         ]

        self.sfx_timings = [(5+30*i, 'shoot1') for i in xrange(0,10)]