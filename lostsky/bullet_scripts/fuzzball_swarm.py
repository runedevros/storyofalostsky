from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
from random import randint
import os
import pygame


class FuzzballEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 20
        max_emissions = 10

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'fuzzball.png')).convert_alpha()


    def generate_position(self):
        return (50+randint(0,50), randint(50, 450))

    def emit(self):
        self.bullets.add(Bullet(self.generate_position(),
                                 self.bullet_img,
                                 15,
                                 0))
        self.bullets.add(Bullet(self.generate_position(),
                                 self.bullet_img,
                                 15,
                                 0))

class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [FuzzballEmitter(self.bullet_group, (0, 0), 0),
                         ]
        self.sfx_timings = [(counter*10, 'shoot1') for counter in xrange(0,10)]
