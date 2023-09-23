import os
import pygame
from lostsky.battle.bullet_sys import PreRenderedScript

class Script(PreRenderedScript):

    def __init__(self, target_surface, background):

        image = pygame.image.load(os.path.join('images', 'anim', 'prerendered_spells', '192x192_lightspell.png')).convert_alpha()

        # Size of each animation frame
        frame_size = (192, 192)

        # Coordinates to display animation
        coords = (610, 250)

        # Hold each animation for this amount of frames
        delay = 3

        PreRenderedScript.__init__(self, target_surface, background, image, frame_size, delay, coords)

        self.sfx_timings = [(0, 'support2')]