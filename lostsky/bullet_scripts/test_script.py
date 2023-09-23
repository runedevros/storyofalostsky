from lostsky.battle.bullet_sys import Emitter, MovingEmitter, Bullet, BulletScript
import os
import pygame

class BasicEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        delay = 20
        max_emissions = 2

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', '06-star.png')).convert_alpha()

    def emit(self):
        [self.bullets.add(Bullet(self.position, self.bullet_img, 10, i*5)) for i in xrange(-5, 5)]

class DelayedEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        delay = 5
        max_emissions = 5

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', '01-dagger.png')).convert_alpha()

    def emit(self):
        self.bullets.add(Bullet(self.position, self.bullet_img, 10, 5-self.emissions*5))

class SpiralEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        delay = 2
        max_emissions = 15

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions)

        self.bullet_img2 = pygame.image.load(os.path.join('images', 'bullets', '06-star.png')).convert_alpha()
        self.bullet_img1 = pygame.image.load(os.path.join('images', 'bullets', '02-orangeorb.png')).convert_alpha()

    def emit(self):
        rotation = 10
        speed = 8
        self.bullets.add(Bullet(self.position, self.bullet_img1, speed, 0+self.emissions*rotation))
        self.bullets.add(Bullet(self.position, self.bullet_img2, speed, 45+self.emissions*rotation))
        self.bullets.add(Bullet(self.position, self.bullet_img1, speed, 90+self.emissions*rotation))
        self.bullets.add(Bullet(self.position, self.bullet_img2, speed, 135+self.emissions*rotation))
        self.bullets.add(Bullet(self.position, self.bullet_img1, speed, 180+self.emissions*rotation))
        self.bullets.add(Bullet(self.position, self.bullet_img2, speed, 225+self.emissions*rotation))
        self.bullets.add(Bullet(self.position, self.bullet_img1, speed, 270+self.emissions*rotation))
        self.bullets.add(Bullet(self.position, self.bullet_img2, speed, 315+self.emissions*rotation))



class TopEmitter(MovingEmitter):

    def __init__(self, bullet_group, initial_position, speed, angle):
        delay = 40
        max_emissions = 5
        MovingEmitter.__init__(self, bullet_group, initial_position, delay, max_emissions, speed, angle)

        self.emit_start = True

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', '02-orangeorb.png')).convert_alpha()

    def emit(self):
        [self.bullets.add(Bullet(self.position, self.bullet_img, 10, i*15+90)) for i in xrange(-4, 5)]

class BottomEmitter(MovingEmitter):

    def __init__(self, bullet_group, initial_position, speed, angle):
        delay = 40
        max_emissions = 5
        MovingEmitter.__init__(self, bullet_group, initial_position, delay, max_emissions, speed, angle)

        self.emit_start = True

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', '02-orangeorb.png')).convert_alpha()

    def emit(self):
        [self.bullets.add(Bullet(self.position, self.bullet_img, 10, i*15-90)) for i in xrange(-4, 5)]

class TestScript(BulletScript):

    def __init__(self, target_surface, background):
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [#SpiralEmitter(self.bullet_group, (420, 300))
                         #BottomEmitter(self.bullet_group, (0, 450), 6, 0),
                         #TopEmitter(self.bullet_group, (0, 110), 6, 0),
                         #DiagEmitter(self.bullet_group, (300, 250), 6, 45)
                         #BasicEmitter(self.bullet_group, (300, 250))
                         DelayedEmitter(self.bullet_group, (300, 250))
                         ]
