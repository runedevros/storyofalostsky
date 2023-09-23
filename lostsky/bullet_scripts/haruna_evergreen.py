from lostsky.battle.bullet_sys import MultiPartScript, MovingEmitter, PreRenderedScript, Bullet, BulletScript
import os
import pygame


class UpwardEmitter(MovingEmitter):

    def __init__(self, bullet_group, initial_position):
        delay = 10
        max_emissions = 10
        start_delay = 0
        speed = 4
        angle = -90

        self.bullet_img = pygame.image.load(os.path.join('images', 'bullets', 'crystal_teal.png')).convert_alpha()

        MovingEmitter.__init__(self, bullet_group, initial_position,
                               delay, max_emissions, start_delay, speed, angle)

    def emit(self):
        self.bullets.add(Bullet(self.position, self.bullet_img, 7, 50))
        self.bullets.add(Bullet(self.position, self.bullet_img, 6, 50))
        self.bullets.add(Bullet(self.position, self.bullet_img, 5, 50))
        self.bullets.add(Bullet(self.position, self.bullet_img, 7, -230))
        self.bullets.add(Bullet(self.position, self.bullet_img, 6, -230))
        self.bullets.add(Bullet(self.position, self.bullet_img, 5, -230))

class AnimScript(PreRenderedScript):

    def __init__(self, target_surface, background):

        image = pygame.image.load(os.path.join('images', 'anim', 'prerendered_spells', '192x192_water.png')).convert_alpha()

        # Size of each animation frame
        frame_size = (192, 192)

        # Coordinates to display animation
        coords = (610, 250)

        # Hold each animation for this amount of frames
        delay = 2

        PreRenderedScript.__init__(self, target_surface, background, image, frame_size, delay, coords)

        self.sfx_timings = [(0, 'support1')]

class BranchScript(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 150
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [UpwardEmitter(self.bullet_group, (610, 250)),
                         ]

        self.sfx_timings = [(15, 'shimmer')]


class Script(MultiPartScript):

    def __init__(self, target_surface, background):


        MultiPartScript.__init__(self, [BranchScript(target_surface, background),
                                        AnimScript(target_surface, background),
                                                                                ])