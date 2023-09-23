from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame



class SpearEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        delay = 15
        max_emissions = 1
        start_delay = 5

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'spear_red.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        [self.bullets.add(Bullet(self.position,
                                 self.image,
                                 8,
                                 i*6)) for i in xrange(-5, 6)]

class OrbEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        delay = 10
        max_emissions = 2
        start_delay = 5

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'medorb_orange.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)


    def emit(self):
        [self.bullets.add(Bullet(self.position,
                                 self.image,
                                 8,
                                 (i*6+3))) for i in xrange(-5, 6)]



class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 150
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [SpearEmitter(self.bullet_group, (220, 250)),
                         OrbEmitter(self.bullet_group, (220, 250)),
                         ]

        self.sfx_timings = [(15, 'shoot4')]