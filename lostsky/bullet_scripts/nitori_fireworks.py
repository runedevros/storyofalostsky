from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript, PreRenderedScript, MultiPartScript
import os
import pygame

class FireworksLauncher(Emitter):

    def __init__(self, bullet_group, initial_position):
        self.num_bullets = 20
        delay = 15
        max_emissions = 1
        start_delay = 0

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'smallorb_orange.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        # Shoots bullets in a series of rings

        self.bullets.add(Bullet(self.position, self.image, 8, -9))


class Script(MultiPartScript):

    def __init__(self, target_surface, background):


        MultiPartScript.__init__(self, [RocketScript(target_surface, background),
                                        ExplosionScript(target_surface, background),
                                                                                ])

class ExplosionScript(PreRenderedScript):

    def __init__(self, target_surface, background):

        image = pygame.image.load(os.path.join('images', 'anim', 'prerendered_spells', '192x192_fireworks.png')).convert_alpha()

        # Size of each animation frame
        frame_size = (192, 192)

        # Coordinates to display animation
        coords = (610, 195)

        # Hold each animation for this amount of frames
        delay = 2

        PreRenderedScript.__init__(self, target_surface, background, image, frame_size, delay, coords)

        self.sfx_timings = [(0, 'fireworks')]

class RocketScript(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 55
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [FireworksLauncher(self.bullet_group, (210, 230)),

                         ]
        self.sfx_timings = [(0, 'shoot6')]
