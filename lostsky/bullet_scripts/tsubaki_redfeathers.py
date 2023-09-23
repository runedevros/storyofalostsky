from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
from random import randint
import os
import pygame

class BirdEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 20
        max_emissions = 10

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'tsubaki_birds.png')).convert_alpha()


    def emit(self):

        for i in xrange(0, 5):
            self.bullets.add(Bullet((randint(0, 50), randint(50, 450)), self.bullet_img, 15, randint(-10, 10)))

class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [BirdEmitter(self.bullet_group, (220, 250), 0),
                         ]
        self.sfx_timings = [(counter*20, 'shoot1') for counter in xrange(0,10)]

