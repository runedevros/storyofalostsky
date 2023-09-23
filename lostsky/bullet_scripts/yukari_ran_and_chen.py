__author__ = 'Fawkes'
from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript, PreRenderedScript, MultiPartScript
import os
import pygame
from random import choice, randint

class Script(MultiPartScript):

    def __init__(self, target_surface, background):

        summon_script_image = pygame.image.load(os.path.join('images', 'anim', 'prerendered_spells', '192x192_darkspell.png')).convert_alpha()


        MultiPartScript.__init__(self, [SummonScript(target_surface, background, summon_script_image, (320, 250)),
                                        ChenAttacks(target_surface, background),
                                        SummonScript(target_surface, background, summon_script_image, (320, 250)),
                                        RanAttacks(target_surface, background),
                                                                                ])

class SummonScript(PreRenderedScript):

    def __init__(self, target_surface, background, image, coords):

        # Size of each animation frame
        frame_size = (192, 192)

        # Hold each animation for this amount of frames
        delay = 2

        PreRenderedScript.__init__(self, target_surface, background, image, frame_size, delay, coords)

        self.sfx_timings = [(0, 'support1')]

class ChenAttacks(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 120
        BulletScript.__init__(self, target_surface, background)
        chen_position = (320, 250)
        bullet_emitter_position = (340, 250)
        self.emitters = [ChenEmitter(self.bullet_group, chen_position, 0),
                         ChenBulletsEmitter(self.bullet_group, bullet_emitter_position, 5)
                         ]
        self.sfx_timings = [(0, 'shoot6')]


class ChenEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 1
        max_emissions = 1

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'chen.png')).convert_alpha()


    def emit(self):
        angle_offset = 0
        self.bullets.add(Bullet(self.position, self.bullet_img, 0, angle_offset))

class ChenBulletsEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 1
        max_emissions = 1


        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_imgs = [pygame.image.load(os.path.join('images', 'bullets', 'force_'+color+'.png')).convert_alpha()
                            for color in ('blue', 'green', 'magenta', 'orange', 'red', 'teal')]


    def emit(self):

        for _ in xrange(0,15):
            angle_offset = randint(-25, 25)
            self.bullets.add(Bullet(self.position, choice(self.bullet_imgs), randint(6,8), angle_offset))


class RanAttacks(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 120
        BulletScript.__init__(self, target_surface, background)
        chen_position = (320, 250)
        bullet_emitter_position = (340, 250)
        self.emitters = [RanEmitter(self.bullet_group, chen_position, 0),
                         RanBulletsEmitter(self.bullet_group, bullet_emitter_position, 5)
                         ]
        self.sfx_timings = [(0, 'fire')]

class RanEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 1
        max_emissions = 1

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'ran.png')).convert_alpha()


    def emit(self):
        angle_offset = 0
        self.bullets.add(Bullet(self.position, self.bullet_img, 0, angle_offset))


class RanBulletsEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 1
        max_emissions = 1


        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        self.bullet_imgs = [pygame.image.load(os.path.join('images', 'bullets', 'medorb_'+color+'.png')).convert_alpha()
                            for color in ('blue', 'green', 'magenta', 'orange', 'red', 'teal')]+\
                           [pygame.image.load(os.path.join('images', 'bullets', 'smallorb_'+color+'.png')).convert_alpha()
                            for color in ('blue', 'green', 'magenta', 'orange', 'red', 'teal')]

    def emit(self):

        for _ in xrange(0,15):
            angle_offset = randint(-25, 25)
            self.bullets.add(Bullet(self.position, choice(self.bullet_imgs), randint(6,8), angle_offset))