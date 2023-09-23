import pygame
import os
# Manages game's sound effects
class SfxSystem(object):

    def __init__(self):
        """
        Creates a sound effects system
        """
        self.sound_catalog = {}

        self.load_effects()

    def load_effects(self):
        """
        load_effects: Loads all the sound effects from /soundeffects/ into sound_catalog
        """

        for sound_file in os.listdir('soundeffects'):
            if sound_file.endswith('.wav') or sound_file.endswith('.ogg'):
                sound_data = pygame.mixer.Sound(os.path.join('soundeffects', sound_file))
                self.sound_catalog[sound_file[:-4]] = sound_data


    def update_volume(self, volume_setting):

        for sound in self.sound_catalog.values():

            # Calculated exponential decay from 1
            sound.set_volume((0, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125, 0.25,  0.5, 1.0)[volume_setting])