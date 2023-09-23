from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
from random import randint
import os
import pygame


class OrbEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 20
        max_emissions = 1

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'yyorb_red.png')).convert_alpha()


    def emit(self):
        # Emits three orbs
        [self.bullets.add(Bullet(self.position,
                                 self.bullet_img,
                                 8,
                                 i*5)) for i in xrange(-1, 2)]

class AmuletEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 2
        max_emissions = 20
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)
        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'amulet_red.png')).convert_alpha()

    def emit(self):
        # Amulets scattered in an 80 degree cone upon impact of orbs
        self.bullets.add(Bullet(((self.position[0]+randint(-5, 5)), self.position[1]+randint(-20, 20)),
                                 self.bullet_img,
                                 8,
                                 randint(-40, 40)))


class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 120
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [OrbEmitter(self.bullet_group, (220, 250), 0),
                         AmuletEmitter(self.bullet_group, (600, 250), 45)
                         ]
        self.sfx_timings = [(0, 'shoot1'), (40, 'shoot4')]
