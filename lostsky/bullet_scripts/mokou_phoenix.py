from lostsky.battle.bullet_sys import Emitter, MovingEmitter, Bullet, BulletScript
import os
import pygame

class PhoenixEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 0
        max_emissions = 1

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', '07-redorb.png')).convert_alpha()

    def emit(self):

        # Draws the Phoenix

        # Body
        self.bullets.add(Bullet((self.position[0]+25, self.position[1]+15),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]+25, self.position[1]-15),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]+50, self.position[1]),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet(self.position, self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]-25, self.position[1]),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]-50, self.position[1]),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]-75, self.position[1]),
                                self.bullet_img, 7, 0))

        self.bullets.add(Bullet((self.position[0]-100, self.position[1]+25),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]-100, self.position[1]-25),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]-125, self.position[1]+30),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]-125, self.position[1]-30),
                                self.bullet_img, 7, 0))

        # Draws Upper Wing
        self.bullets.add(Bullet((self.position[0]-10, self.position[1]+25),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0], self.position[1]+50),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]-15, self.position[1]+75),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]-40, self.position[1]+100),
                                self.bullet_img, 7, 0))

        # Draw Lower Wing
        self.bullets.add(Bullet((self.position[0]-10, self.position[1]-25),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0], self.position[1]-50),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]-15, self.position[1]-75),
                                self.bullet_img, 7, 0))
        self.bullets.add(Bullet((self.position[0]-40, self.position[1]-100),
                                self.bullet_img, 7, 0))


class FlameTail(MovingEmitter):

    def __init__(self, bullet_group, initial_position):
        delay = 15
        max_emissions = 10
        start_delay = 0
        speed = 7
        angle = 0

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', '02-orangeorb.png')).convert_alpha()

        MovingEmitter.__init__(self, bullet_group, initial_position,
                               delay, max_emissions, start_delay, speed, angle)

    def emit(self):
        self.bullets.add(Bullet(self.position, self.bullet_img, 7, 190))
        self.bullets.add(Bullet(self.position, self.bullet_img, 7, 180))
        self.bullets.add(Bullet(self.position, self.bullet_img, 7, 170))



class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [PhoenixEmitter(self.bullet_group, (300, 250), 0),
                         FlameTail(self.bullet_group, (275, 250)),
                         FlameTail(self.bullet_group, (295, 180)),
                         FlameTail(self.bullet_group, (295, 320)),
                         ]
        self.sfx_timings = [(0, 'fire2'), (30, 'fire')]