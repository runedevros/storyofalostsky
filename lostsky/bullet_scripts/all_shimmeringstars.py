'''
Created on Feb 6, 2011

@author: Fawkes
'''
from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame
from random import randint

class MeteorEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 10
        max_emissions = 15

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        star_colors = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'magenta']
        self.stars = [pygame.image.load(os.path.join('images', 'bullets', ('star_%s.png')%color)).convert_alpha()
                      for color in star_colors]

    def emit(self):
        """
        function: emit
        purpose: Emits a star of a random bouncing color
        """
        star_num = randint(0, 6)
        self.bullets.add(MeteorBullet(self.position, self.stars[star_num], 8, randint(-15, 15)))

class MeteorBullet(Bullet):

    def __init__(self, initial_position, image, speed, angle):
        Bullet.__init__(self, initial_position, image, speed, angle)

    def update_velocity(self, delta_t):
        """
        function: update_velocity
        purpose: "bounces" the star up and down
        """
        self.velocity.y += 0.1
        if self.float_position.y > 320:
            self.float_position.y = 319
            self.velocity.y = -0.70*self.velocity.y

class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [MeteorEmitter(self.bullet_group, (200, 150), 0),
                         ]

        self.sfx_timings = [(0, 'shimmer2')]
