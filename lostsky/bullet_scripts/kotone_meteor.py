from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame




class OrbEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        delay = 30
        max_emissions = 4
        start_delay = 5

        self.image1 = pygame.image.load(os.path.join('images', 'bullets', 'smallorb_orange.png')).convert_alpha()
        self.image2 = pygame.image.load(os.path.join('images', 'bullets', 'medorb_orange.png')).convert_alpha()
        self.image3 = pygame.image.load(os.path.join('images', 'bullets', 'bigorb_orange.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)


    def emit(self):

        self.bullets.add(Bullet(self.position, self.image1, 6, 10+self.emissions*5))
        self.bullets.add(Bullet(self.position, self.image2, 8, 10+self.emissions*5))
        self.bullets.add(Bullet(self.position, self.image3, 10, 10+self.emissions*5))




class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 220
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [OrbEmitter(self.bullet_group, (220, 180)),
                         ]

        self.sfx_timings = [(5+30*i, 'fire') for i in xrange(0, 4)]