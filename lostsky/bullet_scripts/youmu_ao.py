from lostsky.battle.bullet_sys import Emitter, MovingEmitter, Bullet, BulletScript
import os
import pygame

class ForceEmitter(MovingEmitter):

    def __init__(self, bullet_group, initial_position, color):
        """
        Downward moving curtain of force bullets (color input refers to bullet color)
        """

        delay = 5
        max_emissions = 10
        start_delay = 0
        speed = 6
        angle = 60

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'force_%s.png'%(color))).convert_alpha()

        MovingEmitter.__init__(self, bullet_group, initial_position,
                               delay, max_emissions, start_delay, speed, angle)

    def emit(self):
        starting_angle = -0
        self.bullets.add(Bullet(self.position, self.bullet_img, 5, starting_angle+2*self.emissions))

class WhiteOrbEmitter(Emitter):
    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 0
        max_emissions = 1

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'medorb_white.png')).convert_alpha()

    def emit(self):
        self.bullets.add(Bullet(self.position, self.bullet_img, 6, 60))


class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [ForceEmitter(self.bullet_group, (305, 120), 'blue'),
                         ForceEmitter(self.bullet_group, (285, 125), 'white'),
                         ForceEmitter(self.bullet_group, (265, 130), 'blue'),
                         WhiteOrbEmitter(self.bullet_group, (245, 130), 0),
                         ]

        self.sfx_timings = [(0, 'shoot4')]
