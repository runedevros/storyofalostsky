
from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
from lostsky.core.linalg import Vector2
import os
import pygame
from random import randint

class SeekingDaggerEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 20
        max_emissions = 8

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'dagger_red.png')).convert_alpha()


    def emit(self):

        self.bullets.add(SeekingDaggerBullet(self.position,
                                 self.bullet_img,
                                 10,
                                 randint(-20, 20)))

class SeekingDaggerBullet(Bullet):

    def __init__(self, initial_position, image, speed, angle):

        Bullet.__init__(self, initial_position, image, speed, angle)
        self.target = Vector2(650, 250)


    def update_velocity(self, delta_t):
        """
        function: update_velocity
        purpose: Bullet that accelerates towards target and then stops at a fixed distance
        """
        displacement_vector = self.target - self.float_position
        distance = displacement_vector.get_magnitude()
        FREEZE_DISTANCE = 100
        if distance < FREEZE_DISTANCE or self.float_position.x > self.target.x:
            self.velocity = Vector2(0, 0)
        else:
            ACCEL_CONSTANT = 0.8
            self.velocity += ACCEL_CONSTANT*displacement_vector.get_normalized()





class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 180
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [SeekingDaggerEmitter(self.bullet_group, (220, 250), 0),
                         ]

        self.sfx_timings = [(time*20, 'shoot2') for time in xrange(0, 8)]