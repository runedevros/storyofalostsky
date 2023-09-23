from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
from math import sin, cos, pi
import os
import pygame

class RadialEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):

        self.num_bullets = 18
        delay = 2
        max_emissions = 2

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.red_bullet = pygame.image.load(os.path.join('images', 'bullets', 'force_red.png')).convert_alpha()

    def emit(self):
        [self.bullets.add(Bullet(self.position, self.red_bullet, 6, counter*360.0/self.num_bullets+15*(self.emissions%2)))
          for counter in xrange(0, self.num_bullets)]


class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)

        unordered_positions = self.calculate_pentagram_positions()

        # Order definition
        # 1. Top
        # 2. Lower left
        # 3. Upper Right
        # 4. Upper Left
        # 5. Lower Right
        pentagram_positions = [unordered_positions[0],
                               unordered_positions[2],
                               unordered_positions[4],
                               unordered_positions[1],
                               unordered_positions[3],
                               unordered_positions[0],
                               ]

        self.emitters = [RadialEmitter(self.bullet_group, position, 30*index)
                         for index, position in enumerate(pentagram_positions)
                         ]

        self.sfx_timings = [(30*index, 'shoot4') for index, _ in enumerate(self.emitters)]

    def calculate_pentagram_positions(self):
        """
        # Calculate position of pentagram emitters
        """
        center = (420, 300)
        radius = 120
        offset = -90

        position_list = []
        for index in xrange(0, 5):
            # Calculates each angle of the pentagram and convert to radians
            angle = (index*-72+offset)*pi/180
            rel_position = (radius*cos(angle), radius*sin(angle))
            abs_position = (center[0]+rel_position[0], center[1]+rel_position[1])
            position_list.append(abs_position)

        return position_list