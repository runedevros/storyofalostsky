from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame

class BlueEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        self.num_bullets = 20
        delay = 15
        max_emissions = 5
        start_delay = 0

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'crystal_blue.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        # Shoots bullets in a series of rings
        [self.bullets.add(Bullet(self.position, self.image, 5, counter*360.0/self.num_bullets+7.5*(self.emissions%2)))
                          for counter in xrange(0, self.num_bullets)]


class TealEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        self.num_bullets = 20
        delay = 15
        max_emissions = 5
        start_delay = 5

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'crystal_teal.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        # Shoots bullets in a series of rings
        [self.bullets.add(Bullet(self.position, self.image, 5, (counter+0.33)*360.0/self.num_bullets+7.5*(self.emissions%2)))
                          for counter in xrange(0, self.num_bullets)]


class GreenEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        self.num_bullets = 20
        delay = 15
        max_emissions = 5
        start_delay = 5

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'crystal_green.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        # Shoots bullets in a series of rings
        [self.bullets.add(Bullet(self.position, self.image, 5, (counter+0.66)*360.0/self.num_bullets+7.5*(self.emissions%2)))
                          for counter in xrange(0, self.num_bullets)]


class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [BlueEmitter(self.bullet_group, (210, 250)),
                         TealEmitter(self.bullet_group, (240, 200)),
                         GreenEmitter(self.bullet_group, (270, 250)),

                         ]

        self.sfx_timings = [(15*index, 'shoot5') for index in xrange(0, 6)]