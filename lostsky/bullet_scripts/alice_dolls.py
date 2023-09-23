from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript, PreRenderedScript, MultiPartScript
import os
import pygame

class DollThrowingEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        self.num_bullets = 20
        delay = 15
        max_emissions = 1
        start_delay = 0

        self.image = pygame.image.load(os.path.join('images', 'bullets', 'doll.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        # Shoots bullets in a series of rings

        self.bullets.add(DollBullet(self.position, self.image, 6, -45))


class DollBullet(Bullet):

    def __init__(self, initial_position, image, speed, angle):
        Bullet.__init__(self, initial_position, image, speed, angle)

    def update_velocity(self, delta_t):
        """
        function: update_velocity
        purpose: "bounces" the star up and down
        """
        self.velocity.y += 0.1
        if self.float_position.y > 320:
            self.float_position.y = 319
            self.velocity.y = -0.70*self.velocity.y

class Script(MultiPartScript):

    def __init__(self, target_surface, background):

        MultiPartScript.__init__(self, [DollThrowingScript(target_surface, background),
                                        ExplosionScript(target_surface, background),
                                                                                ])

class ExplosionScript(PreRenderedScript):

    def __init__(self, target_surface, background):

        image = pygame.image.load(os.path.join('images', 'anim', 'prerendered_spells', '192x192_explosion.png')).convert_alpha()

        # Size of each animation frame
        frame_size = (192, 192)

        # Coordinates to display animation
        coords = (610, 240)

        # Hold each animation for this amount of frames
        delay = 2

        PreRenderedScript.__init__(self, target_surface, background, image, frame_size, delay, coords)

        self.sfx_timings = [(0, 'explode')]

# Doll Throwing Portion of Script
class DollThrowingScript(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 100
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [DollThrowingEmitter(self.bullet_group, (210, 230)),

                         ]
        self.sfx_timings = [(0, 'shoot6')]
