from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript, MultiPartScript
import os
import pygame
from math import sin, cos, radians, atan2, degrees
from lostsky.core.linalg import Vector2

class DaggerEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 20
        max_emissions = 8

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'dagger_blue.png')).convert_alpha()


    def emit(self):
        for angle in xrange(0, 360, 20):
            radius = 150
            offset_x = radius * cos(radians(angle))
            offset_y = radius * sin(radians(angle))

            bullet_position = self.position + Vector2(offset_x, offset_y)

            target_position = Vector2(620, 230)

            delta_position = target_position - bullet_position
            norm_direction = delta_position.get_normalized()
            angle_rad = atan2(norm_direction.y, norm_direction.x)

            self.bullets.add(Bullet(bullet_position,
                                             self.bullet_img,
                                             8,
                                             degrees(angle_rad)))


class Spinning_Bullet(Bullet):
    def __init__(self, initial_position, image, speed, angle):

        Bullet.__init__(self, initial_position, image, speed, angle)

        self.delta_theta = 1.0
        self.angle = 0

    def update_rotation(self):

        if self.angle != 0:
            self.lhs_image = pygame.transform.rotate(self.unrotated_image, self.angle)
        else:
            self.lhs_image = self.unrotated_image


    def update(self, delta_t, rhs_source ):

        self.angle += delta_t*self.delta_theta

        self.update_velocity(delta_t)
        self.update_rotation()

        # Espected 16.7 ms/frame
        self.float_position += (delta_t / 16.7) * self.velocity

        # If the RHS unit is using the spell, invert across the center of the screen.
        if not rhs_source:
            self.image = self.lhs_image
            self.rect = self.image.get_rect()
            self.rect.center = (int(self.float_position.x), int(self.float_position.y))
        else:
            self.image = self.rhs_image
            self.rect = pygame.Rect(0,0,100,100)
            self.rect.center = (int(840 - self.float_position.x), int(self.float_position.y))

        # check bounds
        if ((self.rect.topleft[0] > 840 or self.rect.topleft[0] < 0) or
                (self.rect.bottomleft[1] > 490 or self.rect.topleft[1] < 100)):
            self.kill()


class Rotating_Emitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 20
        max_emissions = 1
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'dagger_blue.png')).convert_alpha()

    def emit(self):
        for angle in xrange(0, 360, 20):
            radius = 150
            offset_x = radius*cos(radians(angle))
            offset_y = radius*sin(radians(angle))

            self.bullets.add(Spinning_Bullet(self.position+Vector2(offset_x, offset_y),
                                    self.bullet_img,
                                    0,
                                    angle))




class Stream(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 250
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [DaggerEmitter(self.bullet_group, (220, 280), 0),
                         Rotating_Emitter(self.bullet_group, (220, 280), 0)
                         ]
        self.sfx_timings = [(0, 'shoot4')]

class Rotating_Bullets(BulletScript):
    def __init__(self, target_surface, background):
        self.max_frames = 60
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [Rotating_Emitter(self.bullet_group, (220, 280), 0),
                         ]
        self.sfx_timings = []


    def update(self, t0, rhs_source):
        """
        Function: update
        Purpose: updates all bullets and emitters
                t0 - time of last frame
                rhs_source - (T/F) if RHS unit using this spell.
        """

        delta_t = pygame.time.get_ticks()-t0
        [emitter.update(delta_t) for emitter in self.emitters]
        self.bullet_group.update(delta_t, rhs_source)
        return self.bullet_group.draw(self.target_surface)


class Script(MultiPartScript):
    def __init__(self, target_surface, background):
        MultiPartScript.__init__(self, [Rotating_Bullets(target_surface, background),
                                        Stream(target_surface, background)
                                        ])