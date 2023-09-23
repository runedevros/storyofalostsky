'''
Created on Feb 6, 2011

@author: Fawkes
'''
from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame
from random import randint, choice

class RadialEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        self.num_bullets = 18
        delay = 0
        max_emissions = 1

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'smallorb_orange.png')).convert_alpha()

    def emit(self):
        [self.bullets.add(Bullet(self.position, self.bullet_img, 8, counter*360.0/self.num_bullets+15*(self.emissions%2)))
         for counter in xrange(0, self.num_bullets)]


class EruptionEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 5
        max_emissions = 6

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        image_base_names = ['smallorb_orange.png', 'smallorb_red.png', 'medorb_orange.png', 'medorb_red.png',
                            ]
        self.bullet_images = [pygame.image.load(os.path.join('images', 'bullets', name)).convert_alpha() for
                                name in image_base_names]


    def emit(self):
        """
        function: emit
        purpose: Emits a star of a random bouncing color
        """
        for i in xrange(0, 4):
            self.bullets.add(EruptionBullet(self.position, choice(self.bullet_images), randint(7, 9), -90+randint(-20, 20)))

class EruptionBullet(Bullet):

    def __init__(self, initial_position, image, speed, angle):
        Bullet.__init__(self, initial_position, image, speed, angle)

    def update_velocity(self, delta_t):
        """
        function: update_velocity
        purpose: "bounces" the star up and down
        """
        self.velocity.y += 0.1

class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [EruptionEmitter(self.bullet_group, (420, 470), 20),
                         RadialEmitter(self.bullet_group, (420, 470), 0),
                         ]

        self.sfx_timings = [(0, 'explode'),
                            (60, 'fire2'),

        ]
