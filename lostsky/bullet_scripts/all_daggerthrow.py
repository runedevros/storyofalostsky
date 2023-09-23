from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame

class DaggerEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 20
        max_emissions = 1

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'dagger_blue.png')).convert_alpha()


    def emit(self):
        [self.bullets.add(Bullet(self.position,
                                 self.bullet_img,
                                 10,
                                 i*3)) for i in xrange(-3, 4)]

class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 80
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [DaggerEmitter(self.bullet_group, (220, 250), 0),
                         ]
        self.sfx_timings = [(0, 'shoot4')]

