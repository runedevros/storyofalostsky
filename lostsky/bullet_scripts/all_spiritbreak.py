
from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame
from random import randint, choice

class DrainEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 1
        max_emissions = 60

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)
        self.bullet_list = [pygame.image.load(os.path.join('images', 'bullets', 'amulet_red.png')).convert_alpha(),
                            pygame.image.load(os.path.join('images', 'bullets', 'amulet_white.png')).convert_alpha(),
                            pygame.image.load(os.path.join('images', 'bullets', 'yyorb_red.png')).convert_alpha()
                            ]

    def emit(self):
        """
        function: emit
        purpose: Randomly emits a white tag, red tag, or ying yang orb from target
        """
        self.bullets.add(Bullet(self.position, choice(self.bullet_list), 8, randint(0, 360)))


class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 120
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [DrainEmitter(self.bullet_group, (620, 250), 0),
                         ]


        self.sfx_timings = [(0, 'shoot5')]