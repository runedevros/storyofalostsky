from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame

class TreeEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, color, start_delay, angle):
        delay = 20
        max_emissions = 60

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'crystal_%s.png'%color)).convert_alpha()

        self.angle = angle

    def emit(self):
        self.bullets.add(Bullet(self.position,
                                 self.bullet_img,
                                 4,
                                 self.angle))


class RadialEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, color, start_delay):

        self.num_bullets = 18
        delay = 2
        max_emissions = 2

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.red_bullet = pygame.image.load(os.path.join('images', 'bullets', 'force_%s.png'%color)).convert_alpha()

    def emit(self):
        [self.bullets.add(Bullet(self.position, self.red_bullet, 6, counter*360.0/self.num_bullets+15*(self.emissions%2)))
          for counter in xrange(0, self.num_bullets)]

class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 300
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [
                            TreeEmitter(self.bullet_group,(410, 475), 'orange', 0, -90),
                            TreeEmitter(self.bullet_group,(420, 475), 'orange', 0, -90),
                            TreeEmitter(self.bullet_group,(430, 475), 'orange', 0, -90),
                            TreeEmitter(self.bullet_group,(435, 250), 'green', 60, -50),
                            TreeEmitter(self.bullet_group,(405, 250), 'green', 60, -130),

                            TreeEmitter(self.bullet_group,(500, 200), 'green', 120, 20),
                            TreeEmitter(self.bullet_group,(360, 200), 'green', 120, 160),
                            TreeEmitter(self.bullet_group,(520, 180), 'green', 130, 10),
                            TreeEmitter(self.bullet_group,(320, 180), 'green', 130, 170),

                            TreeEmitter(self.bullet_group,(620, 250), 'green', 140, 35),
                            TreeEmitter(self.bullet_group,(650, 190), 'green', 140, -5),

                            TreeEmitter(self.bullet_group,(220, 250), 'green', 140, 145),
                            TreeEmitter(self.bullet_group,(190, 190), 'green', 140, -175),


                            RadialEmitter(self.bullet_group, (420, 120), 'green', 90),

                            RadialEmitter(self.bullet_group, (500, 150), 'green', 120),
                            RadialEmitter(self.bullet_group, (360, 150), 'green', 120),

                            RadialEmitter(self.bullet_group, (650, 175), 'green', 150),
                            RadialEmitter(self.bullet_group, (220, 175), 'green', 150),


                         ]
        self.sfx_timings = [(counter*20, 'shoot1') for counter in xrange(0,10)]
        self.sfx_timings.append((90, 'shoot4'))
        self.sfx_timings.append((120, 'shoot4'))
        self.sfx_timings.append((150, 'shoot4'))
        self.sfx_timings.sort()

