from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame

class RadialEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        self.num_bullets = 18
        delay = 20
        max_emissions = 2

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'smallorb_orange.png')).convert_alpha()

    def emit(self):
        [self.bullets.add(Bullet(self.position, self.bullet_img, 8, counter*360.0/self.num_bullets+15*(self.emissions%2)))
          for counter in xrange(0, self.num_bullets)]


class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 120
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [RadialEmitter(self.bullet_group, (220, 250), 0),
                         ]
        self.sfx_timings = [(0, 'fire'), (40, 'fire')]