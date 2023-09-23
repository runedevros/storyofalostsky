from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame

class SpiralEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):

        self.delta_angle = 40
        delay = 20
        max_emissions = 9

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.red_amulet = pygame.image.load(os.path.join('images', 'bullets', 'amulet_red.png')).convert_alpha()
        self.white_amulet = pygame.image.load(os.path.join('images', 'bullets', 'amulet_white.png')).convert_alpha()

    def emit(self):

        self.bullets.add(Bullet(self.position, self.red_amulet, 6, self.delta_angle*(self.emissions)))
        self.bullets.add(Bullet(self.position, self.white_amulet, 6, 15+self.delta_angle*(self.emissions)))

        self.bullets.add(Bullet(self.position, self.red_amulet, 6, 180+self.delta_angle*(self.emissions)))

        self.bullets.add(Bullet(self.position, self.white_amulet, 6, 195+self.delta_angle*(self.emissions)))

class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [SpiralEmitter(self.bullet_group, (220, 250), 0),
                         ]
        self.sfx_timings = [(time*20, 'shoot1') for time in xrange(0, 9)]