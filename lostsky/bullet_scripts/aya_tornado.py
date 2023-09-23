import os
import pygame
from lostsky.battle.bullet_sys import BulletScript, MovingEmitter, Emitter, Bullet, MultiPartScript
from random import randint


class WhirlwindEmitter(MovingEmitter):

    def __init__(self, bullet_group, initial_position, speed, angle, start_delay):
        delay = 7
        max_emissions = 30
        self.speed = speed
        self.angle = angle

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'crystal_green.png')).convert_alpha()
        self.orb_image = pygame.image.load(os.path.join('images', 'bullets', 'medorb_teal.png')).convert_alpha()
        MovingEmitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay, speed, angle)


    def emit(self):

        position = self.position

        if self.emissions == 0:

            self.bullets.add(Bullet(position, self.orb_image, self.speed, self.angle))

        self.bullets.add(Bullet(position, self.image, 6, 10*self.emissions))
        self.bullets.add(Bullet(position, self.image, 6, 90+10*self.emissions))
        self.bullets.add(Bullet(position, self.image, 6, 180+10*self.emissions))
        self.bullets.add(Bullet(position, self.image, 6, 270+10*self.emissions))





class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 360
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [WhirlwindEmitter(self.bullet_group, (50, 200), 5, 20, 20),
                         WhirlwindEmitter(self.bullet_group, (50, 300), 5, 0, 0),
                         WhirlwindEmitter(self.bullet_group, (50, 400), 5, -20, 20),

                         ]

        self.sfx_timings = [(15, 'shoot6')]

