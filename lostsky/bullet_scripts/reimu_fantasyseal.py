from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame

class WhiteEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        self.num_bullets = 20
        delay = 15
        max_emissions = 5
        start_delay = 0

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'medorb_white.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        # Shoots bullets in a series of rings
        [self.bullets.add(Bullet(self.position, self.image, 5, counter*360.0/self.num_bullets+7.5*(self.emissions%2)))
                          for counter in xrange(0, self.num_bullets)]

class PacketEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):

        delay = 30
        max_emissions = 4
        start_delay = 7

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'amulet_red.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):

        self.bullets.add(Bullet(self.position,
                                self.bullet_img, 5, 0))
        self.bullets.add(Bullet(self.position,
                                self.bullet_img, 5, 5))
        self.bullets.add(Bullet(self.position,
                                self.bullet_img, 5, -5))
class UpperPacketEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):

        delay = 30
        max_emissions = 4
        start_delay = 7

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'amulet_red.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):

        self.bullets.add(Bullet(self.position,
                                self.bullet_img, 5, -10))
        self.bullets.add(Bullet(self.position,
                                self.bullet_img, 5, -5))
        self.bullets.add(Bullet(self.position,
                                self.bullet_img, 5, 0))

class LowerPacketEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):

        delay = 30
        max_emissions = 4
        start_delay = 7

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'amulet_red.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):

        self.bullets.add(Bullet(self.position,
                                self.bullet_img, 5, 10))
        self.bullets.add(Bullet(self.position,
                                self.bullet_img, 5, 5))
        self.bullets.add(Bullet(self.position,
                                self.bullet_img, 5, 0))
class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [WhiteEmitter(self.bullet_group, (210, 250)),
                         UpperPacketEmitter(self.bullet_group, (250, 200)),
                         PacketEmitter(self.bullet_group, (210, 250)),
                         LowerPacketEmitter(self.bullet_group, (250, 300))

                         ]

        self.sfx_timings = [(15*index, 'shoot6') for index in xrange(0, 6)]