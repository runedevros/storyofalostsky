from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame

class AmuletEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 5
        max_emissions = 6

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'amulet_red.png')).convert_alpha()


    def emit(self):
        self.bullets.add(Bullet(self.position,
                                 self.bullet_img,
                                 8,
                                 -self.emissions*3+6))

class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 120
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [AmuletEmitter(self.bullet_group, (280, 250), 0),
                         ]
        self.sfx_timings = [(time*10, 'shoot3') for time in xrange(0, 6)]
