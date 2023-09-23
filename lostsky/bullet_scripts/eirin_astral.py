from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript, MultiPartScript
from math import sin, cos
import os
import pygame

class FirstBurst(Emitter):

    def __init__(self, bullet_group, initial_position):
        self.num_bullets = 6
        delay = 15
        max_emissions = 1
        start_delay = 0

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'medorb_white.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        # Shoots bullets in a series of rings
        [self.bullets.add(Bullet(self.position, self.image, 8, counter*360.0/self.num_bullets+30))
                          for counter in xrange(0, self.num_bullets)]

class Sources(Emitter):

    def __init__(self, bullet_group, initial_position):
        self.num_bullets = 6
        delay = 10
        max_emissions = 1
        start_delay = 0

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'medorb_white.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):

        origin = (610, 250)

        for i in xrange(0,6):

            theta = 60*i + 30
            radius = 120.0

            coord = calculate_circle_position(origin, radius, theta)
            self.bullets.add(Bullet(coord, self.image, 0, 0))

class SecondBurst(Emitter):

    def __init__(self, bullet_group, initial_position):
        delay = 15
        max_emissions = 18
        start_delay = 0

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'oval_darkblue.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):

        origin = (610, 250)

        for i in xrange(0,6):

            theta = 60*i + 30
            radius = 120.0

            coord = calculate_circle_position(origin, radius, theta)
            self.bullets.add(Bullet(coord, self.image, 8, 20*self.emissions))

def calculate_circle_position(origin, r, theta):
        """
        calculates the X,Y coordinates given an origin, radius, and theta
        """

        x = int(origin[0]+r*cos(theta*3.14/180))
        y = int(origin[1]+r*sin(theta*3.14/180))

        return (x,y)

class Script(MultiPartScript):


    def __init__(self, target_surface, background):


        MultiPartScript.__init__(self, [FirstScript(target_surface, background),
                                        SecondScript(target_surface, background),
                                                                                ])

class FirstScript(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 90
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [FirstBurst(self.bullet_group, (210, 250)),

                         ]

        self.sfx_timings = [(0, 'shoot1')]


class SecondScript(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [Sources(self.bullet_group, (210, 250)),
                         SecondBurst(self.bullet_group, (210, 250))
                         ]

        self.sfx_timings = [(15*index, 'shoot2') for index in xrange(0, 18)]