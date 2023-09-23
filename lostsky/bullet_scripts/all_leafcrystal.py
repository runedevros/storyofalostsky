from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
from math import pi, cos, sin
import os
import pygame

class RingEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay, bullet_speed, bullet_angle):
        self.num_bullets = 10
        delay = 20
        max_emissions = 1
        self.bullet_speed = bullet_speed
        self.bullet_angle = bullet_angle

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'crystal_green.png')).convert_alpha()


    def emit(self):
        r = 60
        for i in xrange(0, self.num_bullets):
            angle_offset = i*2*pi/self.num_bullets
            position_vector = (self.position[0]+r*cos(angle_offset),
                               self.position[1]+r*sin(angle_offset))

            self.bullets.add(Bullet(position_vector, self.bullet_img, self.bullet_speed, self.bullet_angle))

class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 120
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [RingEmitter(self.bullet_group, (150, 200), 0, 8, 10),
                         RingEmitter(self.bullet_group, (150, 350), 0, 8, -10)
                         ]
        self.sfx_timings = [(0, 'shoot1')]