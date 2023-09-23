from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame

class OrbEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        self.num_bullets = 20
        delay = 15
        max_emissions = 2

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'yyorb_red.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        # Shoots bullets in a series of rings
        [self.bullets.add(Bullet(self.position, self.image, 6, counter*360.0/self.num_bullets+7.5*(self.emissions%2)))
                          for counter in xrange(0, self.num_bullets)]

class AmuletEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 20
        max_emissions = 2

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'amulet_white.png')).convert_alpha()


    def emit(self):
        [self.bullets.add(Bullet(self.position,
                                 self.bullet_img,
                                 6,
                                 i*3)) for i in xrange(-3, 4)]

class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 200
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [OrbEmitter(self.bullet_group, (220, 250), 0),
                         AmuletEmitter(self.bullet_group, (220, 250), 10)
                         ]

        self.sfx_timings = [(0, 'shoot1'), (20, 'shoot1')]