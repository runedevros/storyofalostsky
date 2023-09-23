from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame

class RadialEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, start_delay):
        delay = 20
        max_emissions = 1

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        star_colors = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'magenta']
        self.stars = [pygame.image.load(os.path.join('images', 'bullets', ('star_%s.png')%color)).convert_alpha()
                      for color in star_colors]

    def emit(self):
        [self.bullets.add(Bullet(self.position, star_img, 6, index*360.0/len(self.stars)+15*(self.emissions%2)))
          for index, star_img in enumerate(self.stars)]


class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 240
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [RadialEmitter(self.bullet_group, (750, 250), 0),
                         RadialEmitter(self.bullet_group, (650, 300), 15),
                         RadialEmitter(self.bullet_group, (700, 200), 45),
                         RadialEmitter(self.bullet_group, (600, 450), 30),
                         RadialEmitter(self.bullet_group, (575, 200), 60),
                         ]

        self.sfx_timings = [(0, 'shoot6'), (15, 'shoot6'), (30, 'shoot6'), (45, 'shoot6'), (60, 'shoot6')]