import pygame
import os
from sys import exit
from pygame.locals import *
try: from cmath import floor, sin, pi, cos, ceil
except: from math import floor, sin, pi, cos, ceil, log10

from lostsky.core.persistentobjects import Options, PlayerData, EventData, get_file_path
from lostsky.worldmap.mission_manager import MissionManager
from lostsky.worldmap.trading import TradingSystem
from lostsky.worldmap.spell_synthesis import SpellSynthesisSystem
from lostsky.battle import status_effects
from lostsky.battle import trait_skills
from lostsky.battle.battle_event import BattleEventSystem
from lostsky.core.utils import split_lines, padlib_rounded_rect, draw_aligned_text, get_ui_panel
from lostsky.core.sound_effects import SfxSystem
from lostsky.core.colors import selected_color, panel_color, border_color, scroll_bar_color, disabled_color
from lostsky.core import xmlreader

try: import cPickle as pickle
except: import pickle

class Engine(object):

    """
    # Central Game Engine
    """

    def __init__(self, surface, tilesize, size):
        """
        # Function Name: __init__
        # Purpose: Intializes the game engine, and loads some game engine level graphics
        # Inputs: surface = the surface to render the images on
        #         tilesize = the size of the tiles
        #         size = the size of the screen in terms of number of tiles
        """


        self.clock = pygame.time.Clock()

        # Splash images
        self.splash_fmp = pygame.image.load(os.path.join('images', 'splash_fmp.jpg'))

        # Cursor image
        self.cursor_img = pygame.image.load(os.path.join('images', 'cursor.png')).convert_alpha()

        # Music Library
        self.music_catalog = {}

        # Small Font, Big Font, Combat display font
        self.sfont = pygame.font.Font(os.path.join('fonts','ABeeZee-Regular.ttf'), 16)
        self.speaker_font = pygame.font.Font(os.path.join('fonts',"BPreplayBold.otf"), 22)
        self.small_speaker_font = pygame.font.Font(os.path.join('fonts',"BPreplayBold.otf"), 20)
        self.message_font = pygame.font.Font(os.path.join('fonts', 'ABeeZee-Regular.ttf'), 20)
        self.bfont = pygame.font.Font(os.path.join('fonts',"VeraSeBd.ttf"), 14)
        self.cfont = pygame.font.Font(os.path.join('fonts',"VeraSeBd.ttf"), 24)
        self.battle_effect_font = pygame.font.Font(os.path.join('fonts',"HammersmithOne.ttf"), 56)
        self.title_font = pygame.font.Font(os.path.join('fonts',"HammersmithOne.ttf"), 36)
        self.section_font = pygame.font.Font(os.path.join('fonts',"HammersmithOne.ttf"), 24)
        self.newspaper_top_font = pygame.font.Font(os.path.join('fonts','proclamate_light.ttf'), 72)

        self.newspaper_title_font = pygame.font.Font(os.path.join('fonts','Habibi.ttf'), 56)
        self.newspaper_mission_title_font = pygame.font.Font(os.path.join('fonts','Habibi.ttf'), 36)
        self.newspaper_subtitle_font = pygame.font.Font(os.path.join('fonts','Habibi.ttf'), 28)
        self.newspaper_body_font = pygame.font.Font(os.path.join('fonts', 'Habibi.ttf'), 20)

        self.data_font = pygame.font.Font(os.path.join('fonts',"SourceSansPro-Regular.otf"), 24)

        # The size of the window
        self.size_x = size[0]
        self.size_y = size[1]
        self.surface = surface

        # The size of each tile
        self.tilesize = tilesize

        # Colored Tiles
        self.move_tile = pygame.image.load(os.path.join('images', 'green_tile.png')).convert_alpha()
        self.attack_tile = pygame.image.load(os.path.join('images', 'red_tile.png')).convert_alpha()
        self.heal_tile = pygame.image.load(os.path.join('images', 'blue_tile.png')).convert_alpha()
        self.fog_panel = pygame.image.load(os.path.join('images', 'foglayer.png')).convert_alpha()
        self.fog_panel_x = self.fog_panel.get_width()/35
        self.fog_panel_y = self.fog_panel.get_height()/35
        self.deploy_tile = pygame.image.load(os.path.join('images', 'deploy_tile.png')).convert_alpha()
        self.team_panels = pygame.image.load(os.path.join('images', 'team_panels.png')).convert_alpha()

        # Various menu panels
        self.menu_board = pygame.image.load(os.path.join('images', 'menuboard.png')).convert_alpha()
        self.vertical_panel = pygame.image.load(os.path.join('images', 'menu_panel.png')).convert_alpha()
        self.spell_select_panel = pygame.image.load(os.path.join('images', 'spell_select_panel.png')).convert()
        self.move_arrow = pygame.image.load(os.path.join('images', 'move_arrow.png')).convert_alpha()
        self.battle_panel = pygame.image.load(os.path.join('images', 'battlepanel2.png')).convert_alpha()
        self.battle_bg = pygame.image.load(os.path.join('images', 'battlebg.jpg'))
        self.stats_bg = pygame.image.load(os.path.join('images', 'statsbg.jpg'))
        self.battle_board = pygame.image.load(os.path.join('images', 'battleboard.png')).convert()
        self.battle_top = pygame.image.load(os.path.join('images', 'battletop.png')).convert_alpha()
        self.results_panel = pygame.image.load(os.path.join('images', 'results_panel.png')).convert()
        self.text_board = pygame.image.load(os.path.join('images', 'textboard.png')).convert()
        self.map_spell_board = pygame.image.load(os.path.join('images', 'map_spell_panel.png')).convert_alpha()
        self.small_text_board = pygame.image.load(os.path.join('images', 'small_text_panel.png')).convert()
        self.tiny_text_board = pygame.image.load(os.path.join('images', 'tiny_text_panel.png')).convert()
        self.shop_bg = pygame.image.load(os.path.join('images', 'shopbg.jpg'))
        self.chapter_title = pygame.image.load(os.path.join('images', 'chapter_titles.png')).convert_alpha()
        self.health_meter = pygame.image.load(os.path.join('images', 'health_meter.png')).convert_alpha()

        battle_meters = pygame.image.load(os.path.join('images', 'meters.png')).convert_alpha()
        self.meter_outline = battle_meters.subsurface((0, 0, 300, 25))
        self.big_hp_meter = battle_meters.subsurface((0, 25, 296, 21))
        self.big_sc_meter = battle_meters.subsurface((0, 50, 296, 21))
        self.big_exp_meter = battle_meters.subsurface((0, 75, 296, 21))

        self.stats_icons = pygame.image.load(os.path.join('images', 'icons', 'stat_icons.png')).convert_alpha()
        self.movement_range_icon = self.stats_icons.subsurface((0,100,50,50))
        self.spell_type_icons_big = {
                                     'Spiritual':self.stats_icons.subsurface(50,100,50,50),
                                     'Natural':self.stats_icons.subsurface(100,100,50,50),
                                     'Force':self.stats_icons.subsurface(50,150,50,50),
                                     'Elemental':self.stats_icons.subsurface(100,150,50,50),
                                     }

        # Item Categories
        self.item_category_cursor = pygame.image.load(os.path.join('images', 'item_category_cursor.png')).convert_alpha()
        self.item_category_header = pygame.image.load(os.path.join('images', 'item_category_header.png')).convert_alpha()
        self.treasure_header = pygame.image.load(os.path.join('images', 'treasure_header.png')).convert_alpha()


        # Team move images
        self.p1turn = pygame.image.load(os.path.join('images', 'player1turn.png')).convert_alpha()
        self.p2turn = pygame.image.load(os.path.join('images', 'player2turn.png')).convert_alpha()

        # Status images
        self.status_effect_icons = pygame.image.load(os.path.join('images', 'status_effect_icons.png')).convert_alpha()
        self.status_spirit = pygame.image.load(os.path.join('images', 'status-spirit.png')).convert_alpha()

        # Image for displaying hit/miss percent
        self.arrows = pygame.image.load(os.path.join('images', 'hit_arrows.png')).convert_alpha()
        self.combatstats = pygame.image.load(os.path.join('images', 'combatstats.png')).convert_alpha()


        # Load terrain tile file
        self.terrain_img = pygame.image.load(os.path.join('images', 'terraintilesv4.png')).convert_alpha()
        self.terrain_icon = pygame.image.load(os.path.join('images', 'terrainicons.png')).convert()
        self.layer_2_img = pygame.image.load(os.path.join('images', 'layer_2_tiles.png')).convert_alpha()

        # Spell icons
        spell_icons = pygame.image.load(os.path.join('images', 'icons', 'spell_type_icons.png')).convert_alpha()
        self.spell_type_icons = {'Spiritual':spell_icons.subsurface((0, 0, 35, 35)),
                                 'Natural':spell_icons.subsurface((35, 0, 35, 35)),
                                 'Force':spell_icons.subsurface((70, 0, 35, 35)),
                                 'Elemental':spell_icons.subsurface((105, 0, 35, 35)),
                                 'Item':spell_icons.subsurface((0, 35, 35, 35)),
                                 'Healing':spell_icons.subsurface((35, 35, 35, 35)),
                                 }

        self.trait_type_icons = {'Support':spell_icons.subsurface((70, 35, 35, 35)),
                                'Proximity':spell_icons.subsurface((105, 35, 35, 35)),
                                'Trait Skill':spell_icons.subsurface((140, 35, 35, 35)),


                                }

        self.spell_icons = pygame.image.load(os.path.join('images', 'spell_icons.png')).convert()
        self.spell_icons_big = pygame.image.load(os.path.join('images', 'spell_icons_big.png')).convert()
        self.spell_rel_diag = pygame.image.load(os.path.join('images', 'spell_type_diagram.png')).convert_alpha()
        self.level_stars = pygame.image.load(os.path.join('images', 'level_stars.png')).convert_alpha()
        relation_arrows = pygame.image.load(os.path.join('images', 'icons', 'advantage_icons.png')).convert_alpha()
        self.relation_arrows = {'up': relation_arrows.subsurface(0, 0, 20, 20),
                                'down': relation_arrows.subsurface(20, 0, 20, 20),
                                'neutral': relation_arrows.subsurface(40, 0, 20, 20)
                                }


        self.heal_bullet = pygame.image.load(os.path.join('images', 'bullets', 'smallorb_magenta.png')).convert_alpha()

        # Giant Fuzzy for CH2ST5 event
        self.giant_fuzzy = pygame.image.load(os.path.join('images', 'bullets', 'giant_fuzzy.png')).convert_alpha()

        # World Map objects
        self.wm_bg = pygame.image.load(os.path.join('images', 'map_background', 'top_level_bg.jpg')).convert()
        self.region_bg = pygame.image.load(os.path.join('images', 'worldmap_empty.jpg'))
        self.map_cursor = pygame.image.load(os.path.join('images', 'map_cursor.png')).convert_alpha()
        self.player_img = pygame.image.load(os.path.join('images', 'map_sprites', '02-youmu-d.png')).convert_alpha()
        self.location_circle = pygame.image.load(os.path.join('images', 'location_tile.png')).convert_alpha()
        self.event_icon = pygame.image.load(os.path.join('images', 'event_icon.png')).convert_alpha()
        direction_arrows = pygame.image.load(os.path.join('images', 'direction_arrows.png')).convert_alpha()
        self.direction_arrows = {'up':direction_arrows.subsurface(0, 0, 35, 35),
                                 'down':direction_arrows.subsurface(35, 0, 35, 35),
                                 'left':direction_arrows.subsurface(70, 0, 35, 35),
                                 'right':direction_arrows.subsurface(105, 0, 35, 35),

                                 }

        worldmap_icon_images = pygame.image.load(os.path.join('images', 'icons', 'wm_menu_icons.png')).convert_alpha()

        self.wm_icons = { 'Mission':worldmap_icon_images.subsurface((0, 0, 35, 35)),
                          'Conversation':worldmap_icon_images.subsurface((0, 35, 35, 35)),
                          'Party':worldmap_icon_images.subsurface(35, 0, 35, 35),
                          'Options':worldmap_icon_images.subsurface(70, 0, 35, 35),
                          'Missions':worldmap_icon_images.subsurface(35, 35, 35, 35),
                          'Data':worldmap_icon_images.subsurface(70, 35, 35, 35),
                          'Disabled Trading':worldmap_icon_images.subsurface(0, 70, 35, 35),
                          'Treasures':worldmap_icon_images.subsurface(35, 70, 35, 35),
                          'Trading':worldmap_icon_images.subsurface(70, 70, 35, 35),
                          'Disabled Synthesis':worldmap_icon_images.subsurface(0, 105, 35, 35),
                          'Synthesis':worldmap_icon_images.subsurface(35, 105, 35, 35),
                          'Exit':worldmap_icon_images.subsurface(70, 105, 35, 35),
                          'Cancel':worldmap_icon_images.subsurface(0, 140, 35, 35),
                            }

        # Party Management Menu Images
        self.party_bg = pygame.image.load(os.path.join('images', 'partybg.jpg'))
        self.unit_tile = pygame.image.load(os.path.join('images', 'unit_tile.png')).convert_alpha()

        # Loads the game options
        # Attempts to get the game options from saved data

        self.options = Options()
        try:

            loaded_options = Options.load()
            self.options.apply_saved_config(loaded_options)
            self.options.save()

        # If it fails, creates a new options object and saves it
        except IOError:
            self.options = Options()
            self.options.save()

        # Save/Load text images
        self.text_save = self.bfont.render("Saving.", True, (255, 255, 255))
        self.text_load = self.bfont.render("Loading...", True, (255, 255, 255))

        # Title Screen Objects
        self.title = pygame.image.load(os.path.join('images', 'title.jpg'))
        self.title_cursor = pygame.image.load(os.path.join('images', 'title_cursor.png')).convert_alpha()

        # Mission Manager
        self.mission_manager = MissionManager(self)
        self.mission_bg = pygame.image.load(os.path.join('images', 'missionbg.jpg'))

        # Landmark images
        self.landmark_img = pygame.image.load(os.path.join('images', 'landmarks.png')).convert_alpha()
        self.highlight_tile = pygame.image.load(os.path.join('images', 'highlight_tile.png')).convert_alpha()

        # Victory/Defeat banners
        self.mission_victory = pygame.image.load(os.path.join('images', 'mission_victory.png')).convert_alpha()
        self.mission_failure = pygame.image.load(os.path.join('images', 'mission_failure.png')).convert_alpha()

        # Generates empty player data object
        self.player_units = []
        self.player_units_by_name = {}
        self.player = PlayerData()
        self.all_events_master = {}

        # Sound Effects System
        self.sfx_system = SfxSystem()
        self.sfx_system.update_volume(self.options.sfx_volume)

        # Battle Event system
        self.battle_event_system = BattleEventSystem(self)


        # Trading / Synth system stuff
        self.trading_system = TradingSystem(self)

        # Spell synthesis system
        self.spell_synthesis_system = SpellSynthesisSystem(self)

        #Debugging Shortcut Flags
        self.enable_prologue = True
        self.single_turn_win = False
        self.enable_splash = True
        self.enable_wm_tutorial = True
        self.unlock_wm = True
        self.unlock_shops = False

        # Music - Currently playing song
        self.current_music = None

        # Map BG overlay images
        self.night_overlay = pygame.Surface((self.size_x*35, self.size_y*35))
        self.night_overlay.fill((0, 0, 50))
        self.night_overlay.set_alpha(150)
        self.sunset_overlay = pygame.Surface((self.size_x*35, self.size_y*35))
        self.sunset_overlay.fill((150, 0, 0))
        self.sunset_overlay.set_alpha(70)

        # Status Effects
        self.status_effect_icons = pygame.image.load(os.path.join('images', 'status_effect_icons.png')).convert_alpha()
        self.status_effects_catalog = status_effects.get_effects_catalog()
        for status in self.status_effects_catalog.values():
            status.icon = self.status_effect_icons.subsurface((status.icon_location[0]*24, status.icon_location[1]*24, 24, 24))

        # Emotion Bubble Images

        self.treasure_icons = pygame.image.load(os.path.join('images', 'icons', 'treasureicons.png')).convert_alpha()
        self.card_icons = pygame.image.load(os.path.join('images', 'icons', 'cards.png')).convert_alpha()

        self.icons = {
                      # Spell Card Icons
                      'red card': self.card_icons.subsurface((0, 0, 12, 14)),
                      'orange card': self.card_icons.subsurface((12, 0, 12, 14)),
                      'yellow card': self.card_icons.subsurface((24, 0, 12, 14)),
                      'green card': self.card_icons.subsurface((36, 0, 12, 14)),
                      'teal card': self.card_icons.subsurface((48, 0, 12, 14)),
                      'blue card': self.card_icons.subsurface((60, 0, 12, 14)),
                      'purple card': self.card_icons.subsurface((72, 0, 12, 14)),
                      'gray card': self.card_icons.subsurface((84, 0, 12, 14)),

                      # Crystal Icons
                      'silver crystal': self.treasure_icons.subsurface((0, 0, 24, 24)),
                      'red crystal': self.treasure_icons.subsurface((24, 0, 24, 24)),
                      'orange crystal': self.treasure_icons.subsurface((48, 0, 24, 24)),
                      'yellow crystal': self.treasure_icons.subsurface((72, 0, 24, 24)),
                      'green crystal': self.treasure_icons.subsurface((96, 0, 24, 24)),
                      'teal crystal': self.treasure_icons.subsurface((120, 0, 24, 24)),
                      'lightblue crystal': self.treasure_icons.subsurface((144, 0, 24, 24)),
                      'darkblue crystal': self.treasure_icons.subsurface((168, 0, 24, 24)),
                      'purple crystal': self.treasure_icons.subsurface((192, 0, 24, 24)),
                      'brown crystal': self.treasure_icons.subsurface((216, 0, 24, 24)),
                      'jade crystal': self.treasure_icons.subsurface((240, 0, 24, 24)),
                      'ruby crystal': self.treasure_icons.subsurface((264, 0, 24, 24)),
                      'white crystal': self.treasure_icons.subsurface((288, 0, 24, 24)),
                      'gray crystal': self.treasure_icons.subsurface((312, 0, 24, 24)),
                      'black crystal': self.treasure_icons.subsurface((336, 0, 24, 24)),
                      'rainbow crystal': self.treasure_icons.subsurface((360, 0, 24, 24)),
                      'package': self.treasure_icons.subsurface((384, 0, 24, 24)),
                      'treasure box': self.treasure_icons.subsurface((408, 0, 24, 24))


                      }

        self.load_game_data()

    def load_game_data(self):

        """
        load_game_data: Loads the game data from XML files
        """

        self.player_units_catalog = xmlreader.get_player_unit_catalog()
        self.trait_catalog = xmlreader.get_trait_catalog()
        self.trait_learning_catalog = xmlreader.get_trait_learning_catalog()

        # Loads trait learning data from engine catalog into individual units
        for unit_name in self.trait_learning_catalog.keys():

            # Create branches
            for branch_number in xrange(0, 2):

                new_branch = []
                for level, trait_name in self.trait_learning_catalog[unit_name][branch_number][1]:
                    new_branch.append((level, self.trait_catalog[trait_name]))
                self.trait_learning_catalog[unit_name][branch_number][1] = new_branch

            # Loads data into units
            self.player_units_catalog[unit_name].trait_learning_catalog = self.trait_learning_catalog[unit_name]

            # Updates traits
            self.player_units_catalog[unit_name].update_trait_learning_data()

        self.spell_catalog = xmlreader.SpellCatalog()
        self.unit_anim_catalog = xmlreader.UnitAnimCatalog()

        # Assigns character battle animations
        for unit in self.player_units_catalog.values():
            if unit.animation_enable:
                unit.anim_frames = self.unit_anim_catalog[unit.anim_id_string]


        self.enemynpc_units_catalog = xmlreader.EnemyNPCTemplatesCatalog()
        self.terrain_types, self.terrain_data_by_symbol = xmlreader.get_terrain_data()
        self.layer_2_terrain_data = xmlreader.get_layer_2_data()
        # Assigns character battle animations
        for unit in self.player_units_catalog.values():
            if unit.animation_enable:
                self.anim_frames = self.unit_anim_catalog[unit.anim_id_string]

        self.trait_actions_catalog = trait_skills.get_catalog()

    ############################################
    # Misc. utility methods
    ############################################

    def play_music(self, song_name):
        """
        # Function Name: Play Music
        # Purpose: Plays a certain song
        # Inputs: song_name = name of the song
        """

        self.current_music = song_name



        if self.options.music_volume:

            # Precomputed exponential scaling for volume
            pygame.mixer.music.set_volume((0, 0.0078125, 0.015625, 0.03125, 0.0625, 0.125, 0.25,  0.5, 1.0)[self.options.music_volume])
            pygame.mixer.music.load(os.path.join('music', self.music_catalog[song_name][0]))
            pygame.mixer.music.play(-1)

    def fade_to(self, color, time=0.25):
        """
        # Function Name: fade_to
        # Purpose: Fades the screen to a color
        # Inputs:   color - either the strings 'black', 'white'
        #                   or a RGB tuple e.g.(0, 0, 255)
        #           time = time (in seconds) to fade. Default is 0.25 s
        """

        if color == 'black':
            color = (0, 0, 0)
        elif color == 'white':
            color = (255, 255, 255)
        # Determines the max time (in # frames)
        max_time = int(time*60)

        # Gets a copy of what's currently on the screen
        screen_copy = self.surface.copy()
        overlay = pygame.Surface((self.size_x*35, self.size_y*35))
        overlay.fill(color)
        for t in xrange(0, max_time):
            pygame.event.get()
            # Uses a sin(x) function to get from 0 to 255
            overlay.set_alpha(int(255*sin(pi*t/(2*max_time))))
            self.surface.blit(screen_copy, (0, 0))
            self.surface.blit(overlay, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

    def fade_from(self, color, time=0.25):
        """
        # Function Name: fade_from
        # Purpose: Fades the screen from a color
        # Inputs:   color - either the strings 'black', 'white'
        #                   or a RGB tuple e.g.(0, 0, 255)
        #           time = time (in seconds) to fade. Default is 0.5 s
        """

        if color == 'black':
            color = (0, 0, 0)
        elif color == 'white':
            color = (255, 255, 255)
        max_time = int(time*60)

        screen_copy = self.surface.copy()
        overlay = pygame.Surface((self.size_x*35, self.size_y*35))
        overlay.fill(color)
        for t in xrange(0, max_time):
            pygame.event.get()
            # Uses a cos(x) function to get from 0 to 255
            overlay.set_alpha(int(255*cos(pi*t/(2*max_time))))
            self.surface.blit(screen_copy, (0, 0))
            self.surface.blit(overlay, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

        # Restores the screen (in case the alpha transparency locks in at 1 b/c rounding)
        self.surface.blit(screen_copy, (0, 0))
        pygame.display.flip()
        self.clock.tick(60)


    def pause(self, time):
        """
        # Function Name: pause
        # Purpose: pauses the game for a specified amount of seconds
        # Inputs: time = time to pause, in seconds. May be either an integer or float
        """

        framecount = int(60*time)
        for i in xrange(0, framecount):

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()

            pygame.display.flip()
            self.clock.tick(60)

    def render_outlined_text(self, line, font, text_color, outline_color, thickness = 2):
        """
        # Function Name: render_outlined_text
        # Purpose: Create a image of a set of text that has a 1 pixel padded outlined color
        # Inputs:    line - line of text to render
        #            font - font to render with
        #            text_color - (R, G, B)
        #            outline_color - (R, G, B)
        # Outputs: text_surface - image of outlined text
        """
        inner_text = font.render(line, True, text_color)
        outer_text = font.render(line, True, outline_color)

        # Following algorithm for outlined text is modified from Ptext.py by cosmologicon
        # Released under CC/0
        # https://github.com/cosmologicon/pygame-text

        w0, h0 = inner_text.get_size()
        opx = ceil(thickness * h0 / 24)

        text_surface = pygame.Surface((w0 + 2 * opx, h0 + 2 * opx)).convert_alpha()
        text_surface.fill((0, 0, 0, 0))

        def circlepoints(r):
            r = int(round(r))
            x, y, e = r, 0, 1 - r
            points = []
            while x >= y:
                points.append((x, y))
                y += 1
                if e < 0:
                    e += 2 * y - 1
                else:
                    x -= 1
                    e += 2 * (y - x) - 1
            points += [(y, x) for x, y in points if x > y]
            points += [(-x, y) for x, y in points if x]
            points += [(x, -y) for x, y in points if y]
            points.sort()
            return points


        for dx, dy in circlepoints(opx):
            text_surface.blit(outer_text, (dx + opx, dy + opx))
            text_surface.blit(inner_text, (opx, opx))

        return text_surface


    ############################################
    # Data Manipulation Methods
    ############################################

    def check_event_completion(self, event_list):
        """
        # Function Name: check_event_completion
        # Purpose: Checks if a list of events has been completed
        # Inputs: event_list - the list of events to check
        # Outputs: True if the events have been completed
        #          False if the events have not been completed
        """
        events_done = 0
        for event_id in event_list:
            # Case: The mission is not in the game
            if event_id not in self.all_events_master.keys():
                break

            if self.all_events_master[event_id].done:
                events_done += 1

        if events_done == len(event_list):
            return True
        else:
            return False

    def add_event_master(self, event_list):
        """
        # Function Name: add_event_master
        # Purpose: Adds event to the master list of events
        # Inputs: event_list - the list of event to be added
        """

        for event in event_list:
            # Assigns the event a unique ID
            self.all_events_master[event.event_id] = event
            # Adds the event to the player event data
            self.player.all_event_data[event.event_id] = EventData(event)

        self.all_events_available = []
        self.all_events_completed = []
        self.all_events_sign_up = []

        # Updates all events on the map
        self.worldmap.update_all_events()

    def save_menu(self, title_mode=False):

        """
        # Function Name: Save/Load Menu
        # Purpose: Manages saving and loading
        # Inputs: title_mode = Load from title screen. Sets method into Load only mode.
        """

        # Grabs the latest update to the save data
        self.update_player_data()
        data_report, filenames = self.data_summary()

        def update_data_text(data_report):
            """
            # Function Name: update data text
            # Purpose: Turns a data report dictionary and returns the rendered text objects
            # Inputs: data_report - a data report list
            """
            text_data_report = []
            for save_data in data_report:
                if save_data == 'No Data':

                    text_data_report.append([
                                            self.data_font.render("N/A", True, (0, 0, 0)),
                                            self.data_font.render("N/A", True, (0, 0, 0)),
                                            self.message_font.render("No Data", True, (0, 0, 0)),
                                            False
                                           ])
                else:
                    text_data_report.append([
                                            self.data_font.render(save_data[0], True, (0, 0, 0)),
                                            self.data_font.render(save_data[1], True, (0, 0, 0)),
                                            self.message_font.render(save_data[2], True, (0, 0, 0)),
                                            True
                                           ])
            return text_data_report

        text_data_report = update_data_text(data_report)
        text_data_headers = self.get_save_data_headers(text_data_report)

        max_slots = 4

        scroll_bar_total = max_slots*100 + (max_slots-1)*10
        scroll_bar_height = scroll_bar_total*max_slots/len(text_data_headers)
        if len(filenames) > max_slots:
            scroll_delta = scroll_bar_total / (len(filenames) - max_slots)
        else:
            scroll_delta = 0

        menu_flag = True
        menu_pos = 0
        update = True

        # If loading from title, set menu position to load
        if title_mode:
            menu_pos = 1

        while menu_flag:

             # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    update = True
                    if (event.key == K_z or event.key == K_RETURN) and menu_pos in (0, 1):

                        # Selects Save (locked out of loading from the main screen)
                        if menu_pos == 0 and title_mode == False:

                            self.slot_select_loop(text_data_report, filenames, 's', title_mode)
                            # Refreshes data reports
                            data_report, filenames = self.data_summary()
                            text_data_report = update_data_text(data_report)
                            text_data_headers = self.get_save_data_headers(text_data_report)

                            # Updates the scroll bar height
                            scroll_bar_height = scroll_bar_total*max_slots/len(text_data_headers)
                            if len(filenames) > max_slots:
                                scroll_delta = scroll_bar_total / (len(filenames) - max_slots)
                            else:
                                scroll_delta = 0

                        # Selects Load
                        if menu_pos == 1:

                            confirm = self.slot_select_loop(text_data_report, filenames, 'l', title_mode)
                            # Refreshes data reports
                            data_report, filenames = self.data_summary()
                            text_data_report = update_data_text(data_report)
                            text_data_headers = self.get_save_data_headers(text_data_report)


                            # Exits save menu after loading
                            if confirm:
                                return True

                    if event.key == K_UP or event.key == K_LEFT:
                        if menu_pos > 0:
                            menu_pos -= 1
                        else:
                            menu_pos = 2
                    if event.key == K_DOWN or event.key == K_RIGHT:
                        if menu_pos < 2:
                            menu_pos += 1
                        else:
                            menu_pos = 0
                    if ((event.key == K_z or event.key == K_RETURN) and menu_pos == 2) or event.key == K_x:
                        return False



            if menu_flag:

                if update:
                    update = False
                    self.draw_save_menu_background(title_mode)

                    # Draws the cursor
                    if menu_pos == 0:
                        cursor_pos = 210 - 150/2 - 2
                    elif menu_pos == 1:
                        cursor_pos = 420 - 150/2 - 2
                    else:
                        cursor_pos = 630 - 150/2 - 2

                    padlib_rounded_rect(self.surface, selected_color, (cursor_pos,
                                                                     48, 150 + 4, 60 + 4), 6, 5)

                    # Renders Saved Data
                    self.draw_save_data(text_data_headers, text_data_report, 0)

                    if len(filenames) > max_slots:
                        self.draw_save_menu_scrollbar(len(filenames), 0)

                    pygame.display.flip()
                self.clock.tick(60)

    def slot_select_loop(self, text_data_report, filenames, mode, title_mode):
        """
        # Function Name: slot select loop
        # Purpose: Allows player to select a save slot to save/load into
        # Inputs: text data report: current summary of saved data
        #         filenames: a listing of filenames associated with each save file.
        #         mode - 's' for save, 'l' for load
        #         title_mode - True for load only title mode
        # Outputs:  True if save/load done
        #           False if save/load cancelled
        """

        menu_flag = True
        menu_pos = 0
        offset = 0

        if not title_mode:
            text_save = self.title_font.render("Save", True, (0, 0, 0))
        else:
            text_save = self.title_font.render("Save", True, (100, 100, 100))
        text_load = self.title_font.render("Load", True, (0, 0, 0))
        text_cancel = self.title_font.render("Cancel", True, (0, 0, 0))

        text_data_headers = self.get_save_data_headers(text_data_report)


        #If save-mode, add "New File" to the top of the list
        if mode == 's':
            empty_file = [ self.data_font.render("N/A", True, (0, 0, 0)),
                          self.data_font.render("N/A", True, (0, 0, 0)),
                          self.data_font.render("Create a new save file", True, (0, 0, 0)),
                        False]

            empty_file_header = self.section_font.render("New File", True, (0, 0, 0))

            # determine next filename by looking at how many files are loaded
            next_save_filename = 'savedata%s.dat' % str(len(filenames)-1).zfill(4)

            text_data_report.insert(0, empty_file)
            text_data_headers.insert(0, empty_file_header)
            filenames.insert(0, next_save_filename)
#
            # Remove the auto save entries from the list
            del(text_data_report[1])
            del(text_data_report[1])
            del(filenames[1])
            del(filenames[1])
            del(text_data_headers[1])
            del(text_data_headers[1])

        max_slots = 4
        frame_num = 0

        go_up = False
        go_down = False

        update = True

        while menu_flag:

             # looks for event type data to select interaction
            keys_pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if event.key == K_z or event.key == K_RETURN:

                        if (mode == 's' and 'savedata' in filenames[menu_pos]) or (mode == 'l' and text_data_report[menu_pos][3]):

                            # If saving to an new file, save without prompting
                            if mode == 's' and menu_pos == 0:
                                self.player.save(filenames[menu_pos])
                                return True
                            # If overwriting an existing file, confirm the overwrite
                            elif mode == 's' and menu_pos != 0:

                                confirm_overwrite = self.data_confirm_loop(text_data_report, text_data_headers, filenames, menu_pos, offset)
                                if confirm_overwrite:
                                    self.player.save(filenames[menu_pos])
                                    return True
                                else:
                                    update = True
                            # If loading, load without prompting
                            else:
                                self.load_player(filenames[menu_pos])
                                return True

                    if event.key == K_UP or event.key == K_LEFT:
                        go_up = True
                        frame_num = 0

                    if event.key == K_DOWN  or event.key == K_RIGHT:
                        go_down = True
                        frame_num = 0

                    if event.key == K_x:
                        # Returns a False flag to inidicate that no selection has been made
                        return False

            # Enables holding down the arrow keys to allow you to scroll through the menu
            if frame_num == 9 and (keys_pressed[K_UP] or keys_pressed[K_LEFT]):
                go_up = True
                frame_num = 0

            elif frame_num == 9 and (keys_pressed[K_DOWN] or keys_pressed[K_RIGHT]):
                go_down = True
                frame_num = 0

            # Any time movement is triggered, update the screen
            if go_up or go_down:
                update = True

            if go_up:
                # Top of the list, jump to the bottom
                if menu_pos == 0:
                    menu_pos = len(filenames) - 1
                    offset = max(0, len(filenames) - max_slots)

                # Top of the itnerval, shift offset up
                elif menu_pos == offset:
                    menu_pos -= 1
                    offset -= 1

                # within interval, move cursor without changing shift
                elif menu_pos > 0:
                    menu_pos -= 1
                go_up = False

            elif go_down:
                # Bottom of the list of slots: Jumps to the top
                if menu_pos == len(filenames) - 1:
                    menu_pos = 0
                    offset = 0

                # Bottom of the interval, advance the offset by 1
                elif menu_pos == offset + max_slots - 1:
                    offset += 1
                    menu_pos += 1

                # intermediate interval: move the cursor only down by 1
                elif menu_pos < len(filenames) - 1:
                    menu_pos += 1

                go_down = False

            if menu_flag:

                if frame_num == 10:
                    frame_num = 0
                frame_num += 1

                if update:
                    update = False

                    self.draw_save_menu_background(title_mode)

                    # Draws the cursor for the mode
                    if mode == 's':
                        mode_cursor_pos = 210 - 150/2 - 2
                    else:
                        mode_cursor_pos = 420 - 150/2 - 2
                    padlib_rounded_rect(self.surface, selected_color, (mode_cursor_pos,
                                                                     48, 154, 64), 6, 5)

                    # Draws the save slots and the cursor for currently selected slot
                    self.draw_save_data(text_data_headers, text_data_report, offset)
                    padlib_rounded_rect(self.surface, selected_color, (68, 118 + (menu_pos-offset)*(110),
                                                                      705, 104), 6, 5)

                    if len(filenames) > max_slots:
                        self.draw_save_menu_scrollbar(len(filenames), offset)

                    pygame.display.flip()
                self.clock.tick(60)

    def get_save_data_headers(self, text_data_report):

        """
        Generates the "Current Data", "Autosave", "Save Slot X" text objects

        """

        text_data_headers = []

        # 1st set: Autosaves
        text_data_headers.append(self.section_font.render("Auto Save #1", True, (0, 0, 0)))
        text_data_headers.append(self.section_font.render("Auto Save #2", True, (0, 0, 0)))

        # All manual saves come afterwards: "Save slots"
        for i in xrange(0, len(text_data_report)-2):
            text_data_headers.append(self.section_font.render("Slot #%d"%(i+1), True, (0, 0, 0)))

        return text_data_headers


    def draw_save_menu_background(self, title_mode):

        """
        Draws the background objects for the save menu

        input: title mode - True if the save option is to be drawn disabled.
        """

        # title mode disables saving data, so draw
        if not title_mode:
            text_save = self.title_font.render("Save", True, (0, 0, 0))
        else:
            text_save = self.title_font.render("Save", True, (100, 100, 100))

        text_load = self.title_font.render("Load", True, (0, 0, 0))
        text_cancel = self.title_font.render("Cancel", True, (0, 0, 0))

        option_panel = get_ui_panel((150, 60), border_color, panel_color)
        save_slot_panel = get_ui_panel((700, 100), border_color, panel_color)
        data_panel = get_ui_panel((200, 35), border_color, panel_color)
        comment_panel = get_ui_panel((680, 40), border_color, panel_color)

        # Background image
        self.surface.blit(self.stats_bg, (0, 0))
        # Renders the options

        menu_y = 50
        # Draws the Save, Load, Cancel options
        self.surface.blit(option_panel, (210 - option_panel.get_width()/2, menu_y))
        self.surface.blit(text_save, (210 - text_save.get_width()/2,
                                        menu_y + option_panel.get_height()/2 - text_save.get_height()/2))
        self.surface.blit(option_panel, (420 - option_panel.get_width()/2, menu_y))
        self.surface.blit(text_load, (420 - text_load.get_width()/2,
                                        menu_y + option_panel.get_height()/2 - text_load.get_height()/2))
        self.surface.blit(option_panel, (630 - option_panel.get_width()/2, menu_y))
        self.surface.blit(text_cancel, (630 - text_cancel.get_width()/2,
                                        menu_y + option_panel.get_height()/2 - text_cancel.get_height()/2))

        max_slots = 4

        # Draws four slots below
        for index in xrange(0, max_slots):
            self.surface.blit(save_slot_panel, (420 - save_slot_panel.get_width()/2,
                              120 + index*(save_slot_panel.get_height()+10)))

            # Slot Name Panel
            self.surface.blit(data_panel, (430 - save_slot_panel.get_width()/2,
                              130 + index*(save_slot_panel.get_height()+10)))

            # Number of Missions Completed Panel
            self.surface.blit(data_panel, (420 - data_panel.get_width()/2,
                              130 + index*(save_slot_panel.get_height()+10)))

            # Average Level panel
            self.surface.blit(data_panel, (760 - data_panel.get_width(),
                              130 + index*(save_slot_panel.get_height()+10)))

            # A big box below for the save data's comment
            self.surface.blit(comment_panel, (430 - save_slot_panel.get_width()/2,
                              170 + index*(save_slot_panel.get_height()+10)))


    def draw_save_menu_scrollbar(self, filename_list_length, offset):

        """

        function name: draw_save_menu_scrollbar

        Draws a scrollbar to the right of the save slots

        Inputs:     filename_list_length - how many save slots are being viewed?
                    offset - position of scrollbar

        """

        max_slots = 4

        # Do not draw scrollbar if number of items is less than max length
        if filename_list_length <= max_slots:
            return

        scroll_bar_total = 110*max_slots - 10

        scroll_bar = get_ui_panel((20, scroll_bar_total), border_color, panel_color)

        # Calculates the length of the scroll bar section and how far the spacing is
        scroll_length = scroll_bar_total*max_slots/filename_list_length
        scroll_delta = (scroll_bar_total - scroll_length) / (filename_list_length - max_slots)

        scroll_bar_section = get_ui_panel((20, scroll_length), border_color, scroll_bar_color)

        self.surface.blit(scroll_bar, (780, 120))

        # Special case to clamp the scroll bar at the bottom of the screen to correct for round off
        if offset == filename_list_length - max_slots:
            self.surface.blit(scroll_bar_section, (780, 120 + scroll_bar_total - scroll_bar_section.get_height()))
        else:
            self.surface.blit(scroll_bar_section, (780, 120 + scroll_delta * offset))

    def draw_save_data(self, text_data_headers, text_data_report, offset):
        """
        # Function Name: render_save_slots
        # Purpose: Draws the data for all the manual and auto-save slots
        # Inputs:    text_data_headers - text represenations of each slot's title
        #            text_data_report - text representations of the information about the
        #                save data to display to the player
        """

        # Renders Saved Data
        slot_max = 4
        start = offset
        end = min(len(text_data_report), start + slot_max)

        SPACING = 110
        START_POSITION_Y = 130 + 35/2

        text_missions_completed = self.section_font.render("Missions:", True, (0, 0, 0))
        text_level = self.section_font.render("Av. Level:", True, (0, 0, 0))

        for index in xrange(start, end):

            self.surface.blit(text_data_headers[index], (180 - text_data_headers[index].get_width()/2,
                                                           START_POSITION_Y + 2 - text_data_headers[index].get_height()/2 +SPACING*(index-offset)))

            self.surface.blit(text_missions_completed, (350,
                                                           START_POSITION_Y + 2 - text_missions_completed.get_height()/2 +SPACING*(index-offset)))

            self.surface.blit(text_data_report[index][0], (490 - text_data_report[index][0].get_width(),
                                                           START_POSITION_Y - text_data_report[index][0].get_height()/2 +SPACING*(index-offset)))

            self.surface.blit(text_level, (590, START_POSITION_Y + 2 - text_level.get_height()/2 +SPACING*(index-offset)))

            self.surface.blit(text_data_report[index][1], (730 - text_data_report[index][1].get_width(),
                                                           START_POSITION_Y - text_data_report[index][1].get_height()/2 +SPACING*(index-offset)))

            self.surface.blit(text_data_report[index][2], (420 - text_data_report[index][2].get_width()/2,
                                                           START_POSITION_Y + 43 - text_data_report[index][2].get_height()/2 +SPACING*(index-offset)))


    def data_confirm_loop(self, text_data_report, text_data_headers, filenames, slot, offset):
        """
        # Function Name: data confirm loop
        # Purpose: Allows player to confirm saving/loading
        # Inputs:   text data report - current summary of saved data
        #           text_data_headers - set of headers to display for each save slot
        #           filenames - list of filenames
        #           slot - slot selected to save into
        #           offset - current offset of save menu window
        """

        menu_flag = True
        menu_pos = True

        text_directions = self.title_font.render("Overwrite Data?", True, (0, 0, 0))
        text_yes = self.title_font.render("Yes", True, (0, 0, 0))
        text_no = self.title_font.render("No", True, (0, 0, 0))

        top_panel =get_ui_panel((800, 80), border_color, panel_color)
        option_panel = get_ui_panel((150, 60), border_color, panel_color)

        update = True

        while menu_flag:

             # looks for event type data to select interaction
            for event in pygame.event.get():
                update = True
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if (event.key == K_z or event.key == K_RETURN):
                        if menu_pos == True:
                            return True
                        else:
                            return False

                    # If there is an arrow key press, toggle yes/no
                    if event.key in (K_UP, K_DOWN, K_RIGHT, K_LEFT):
                        menu_pos = not(menu_pos)

                    if event.key == K_x:
                        menu_flag = False
                        return False

            if menu_flag:
                if update:
                    update = False

                    self.draw_save_menu_background(False)
                    self.draw_save_data(text_data_headers, text_data_report, offset)
                    self.surface.blit(top_panel, (420 - top_panel.get_width()/2, 30))
                    self.surface.blit(text_directions, (60, 30 + top_panel.get_height()/2 - text_directions.get_height()/2))
                    self.surface.blit(option_panel, (500, 40))
                    self.surface.blit(text_yes, (500 + option_panel.get_width()/2 - text_yes.get_width()/2,
                                                 40 + option_panel.get_height()/2 - text_yes.get_height()/2))
                    self.surface.blit(option_panel, (660, 40))
                    self.surface.blit(text_no, (660 + option_panel.get_width()/2 - text_no.get_width()/2,
                                                40 + option_panel.get_height()/2 - text_no.get_height()/2))

                    padlib_rounded_rect(self.surface, selected_color, (68, 118 + (slot-offset)*(110),
                                                                      705, 104), 6, 5)

                    if menu_pos:
                        padlib_rounded_rect(self.surface, selected_color, (498, 38, 155, 64), 6, 5)
                    else:
                        padlib_rounded_rect(self.surface, selected_color, (658, 38, 155, 64), 6, 5)


                    self.draw_save_menu_scrollbar(len(filenames), offset)

                pygame.display.flip()
                self.clock.tick(60)

    def options_menu(self):
        """
        # Function Name: Options Menu
        # Purpose: Manages system options
        # Inputs: None
        """

        menu_flag = True
        menu_pos = 0
        text_yes = self.data_font.render("On", True, (0, 0, 0))
        text_no = self.data_font.render("Off", True, (0, 0, 0))


        text_options = [    self.section_font.render("Battle animations", True, (0, 0, 0)),
                            self.section_font.render("Auto-end turn", True, (0, 0, 0)),
                            self.section_font.render("Grid", True, (0, 0, 0)),
                            self.section_font.render("Music Volume", True, (0, 0, 0)),
                            self.section_font.render("SFX Volume", True, (0, 0, 0)),
                            self.section_font.render("Enemy movements", True, (0, 0, 0)),
                            self.section_font.render("Auto-save", True, (0, 0, 0)),
                            self.section_font.render("Return", True, (0, 0, 0))]

        text_desc = self.speaker_font.render("Description", True, (0, 0, 0))

        text_option_desc = ["Shows spell action battle animations if enabled.",
                            "Automatically ends player turn when all units have completed their actions.",
                            "Draws a grid on the map.",
                            "Sets the volume of music in the game.",
                            "Sets the volume of sound effects in the game.",
                            "Display the movement of enemies during their turn.",
                            "Automatically saves at the beginning and end of each mission.",
                            "Return and save settings.",]

        option_panel = get_ui_panel((300, 45), border_color, panel_color)
        enabled_panel = get_ui_panel((100, 40), border_color, panel_color)
        music_vol_panel = get_ui_panel((40, 40), border_color, panel_color)
        desc_panel = get_ui_panel((300, 140), border_color, panel_color)

        update = True

        while menu_flag:

             # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if (event.key == K_z or event.key == K_RETURN) and menu_pos <= 6:
                        update = True
                        if menu_pos == 0:
                            # Toggles true/false the battle animations setting
                            self.options.battle_anim = not(self.options.battle_anim)
                        elif menu_pos == 1:
                            # Toggles true/false the turn end setting
                            self.options.turn_end = not(self.options.turn_end)
                        elif menu_pos == 2:
                            # Toggles the grid setting
                            self.options.grid = not(self.options.grid)
                        elif menu_pos == 3:
                            # Increments the music volume every time you press z
                            self.options.music_volume += 1
                            if self.options.music_volume > 8:
                                self.options.music_volume = 0

                            if not self.options.music_volume:
                                pygame.mixer.music.stop()
                            else:
                                if self.current_music:
                                    self.play_music(self.current_music)


                        elif menu_pos == 4:

                            self.options.sfx_volume += 1
                            if self.options.sfx_volume > 8:
                                self.options.sfx_volume = 0

                            # Plays a sample SFX
                            self.sfx_system.update_volume(self.options.sfx_volume)
                            if self.options.sfx_volume:
                                self.sfx_system.sound_catalog['crit'].play()

                        elif menu_pos == 5:
                            # Toggles the show enemy movements setting.
                            self.options.show_enemy_moves = not self.options.show_enemy_moves

                        elif menu_pos == 6:
                            # Toggles the show enemy movements setting.
                            self.options.auto_save = not self.options.auto_save

                    if event.key == K_UP:
                        update = True
                        # top of first column, go to bottom of first column
                        if menu_pos == 0:
                            menu_pos = 4
                        # top of second column, go to bottom of second column
                        elif menu_pos == 5:
                            menu_pos = 7
                        else:
                            menu_pos -= 1


                    if event.key == K_DOWN:
                        update = True
                        # bottom of first column, go to top of first column
                        if menu_pos == 4:
                            menu_pos = 0
                        # bottom of second column, go to top of second column
                        elif menu_pos == 7:
                            menu_pos = 5
                        else:
                            menu_pos += 1

                    # Shifts the cursor from one side of the screen to the other
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        update = True
                        if menu_pos < 3:
                            menu_pos += 5
                            if menu_pos > len(text_options) - 1:
                                menu_pos = len(text_options) - 1

                        elif menu_pos == 3:

                            if event.key == K_LEFT:
                                self.options.music_volume -= 1
                                if self.options.music_volume < 0:
                                    self.options.music_volume = 8
                            else:
                                self.options.music_volume += 1
                                if self.options.music_volume > 8:
                                    self.options.music_volume = 0

                            if not self.options.music_volume:
                                pygame.mixer.music.stop()
                            else:
                                if self.current_music:
                                    self.play_music(self.current_music)

                        elif menu_pos == 4:

                            if event.key == K_LEFT:
                                self.options.sfx_volume -= 1
                                if self.options.sfx_volume < 0:
                                    self.options.sfx_volume = 8
                            else:
                                self.options.sfx_volume += 1
                                if self.options.sfx_volume > 8:
                                    self.options.sfx_volume = 0

                            # Plays a sample SFX
                            self.sfx_system.update_volume(self.options.sfx_volume)
                            if self.options.sfx_volume:
                                self.sfx_system.sound_catalog['crit'].play()




                        else:
                            menu_pos -= 5

                    if ((event.key == K_z or event.key == K_RETURN) and menu_pos == 7) or event.key == K_x:
                        menu_flag = False
                        self.options.save()
                        return

            if menu_flag:

                if update:
                    update = False
                    # Background image
                    self.surface.blit(self.stats_bg, (0, 0))

                    # Draws the possible settings
                    for index, option in enumerate(text_options):

                        if index < 5:
                            menu_x = 210
                            menu_y = 45 + 105*index
                        else:
                            menu_x = 630
                            menu_y = 45 + 105*(index-5)


                        self.surface.blit(option_panel, (menu_x - option_panel.get_width()/2, menu_y))
                        self.surface.blit(option, (menu_x - option.get_width()/2,
                                                   menu_y + 2 + option_panel.get_height()/2 - option.get_height()/2))

                    # Draws the cursor
                    if menu_pos < 5:
                        cursor_x = 210 - option_panel.get_width()/2 - 2
                        cursor_y = 43 + 105*menu_pos
                    else:
                        cursor_x = 630 - option_panel.get_width()/2 - 2
                        cursor_y = 43 + 105*(menu_pos - 5)
                    padlib_rounded_rect(self.surface, selected_color,
                                                (cursor_x  , cursor_y,
                                                 option_panel.get_width() + 4,
                                                 option_panel.get_height() + 4), 6, 5)

                    # Draws the status indicators for the settings
                    flag_list = (self.options.battle_anim, self.options.turn_end, self.options.grid, "Skip","Skip", self.options.show_enemy_moves, self.options.auto_save)
                    for index, flag in enumerate(flag_list):

                        # Suppresses drawing of volume controls which is not a binary option
                        if flag != "Skip":
                            if index < 4:
                                indicator_x = 210
                                indicator_y = 100 + 105*index
                            else:
                                indicator_x = 630
                                indicator_y = 100 + 105*(index-5)

                            self.surface.blit(enabled_panel, (indicator_x - enabled_panel.get_width() - 20, indicator_y))
                            self.surface.blit(text_yes, (indicator_x - enabled_panel.get_width()/2 - text_yes.get_height()/2 - 20,
                                                         indicator_y + enabled_panel.get_height()/2 - text_yes.get_height()/2))
                            self.surface.blit(enabled_panel, (indicator_x + 20, indicator_y))
                            self.surface.blit(text_no, (indicator_x + enabled_panel.get_width()/2 - text_no.get_height()/2 + 20,
                                                         indicator_y + enabled_panel.get_height()/2 - text_no.get_height()/2))

                            if flag:
                                padlib_rounded_rect(self.surface, selected_color,
                                                    (indicator_x - enabled_panel.get_width() - 22,
                                                     indicator_y - 2,
                                                     enabled_panel.get_width() + 4,
                                                     enabled_panel.get_height() + 4), 6, 5)
                            else:
                                padlib_rounded_rect(self.surface, selected_color,
                                                    (indicator_x + 18,
                                                     indicator_y - 2,
                                                     enabled_panel.get_width() + 4,
                                                     enabled_panel.get_height() + 4), 6, 5)

                    # Draws Music Volume setting
                    indicator_x = 210
                    indicator_y = 100 + 105*3

                    self.surface.blit(enabled_panel, (indicator_x - enabled_panel.get_width()/2, indicator_y))

                    self.surface.blit(music_vol_panel, (indicator_x - enabled_panel.get_width()/2 - music_vol_panel.get_width() - 10, indicator_y))
                    self.surface.blit(self.relation_arrows['down'], (indicator_x - enabled_panel.get_width()/2 - music_vol_panel.get_width()/2 - 10 - self.relation_arrows['down'].get_width()/2,
                                                                   indicator_y + music_vol_panel.get_height()/2 - self.relation_arrows['down'].get_height()/2))

                    self.surface.blit(music_vol_panel, (indicator_x + enabled_panel.get_width()/2 + 10, indicator_y))
                    self.surface.blit(self.relation_arrows['up'], (indicator_x + enabled_panel.get_width()/2 + music_vol_panel.get_width()/2 + 10 - self.relation_arrows['up'].get_width()/2,
                                                                   indicator_y + music_vol_panel.get_height()/2 - self.relation_arrows['up'].get_height()/2))


                    music_vol_text = self.data_font.render(str(self.options.music_volume), True, (0,0,0))
                    self.surface.blit(music_vol_text, (indicator_x  - music_vol_text.get_width()/2,
                                                         indicator_y + enabled_panel.get_height()/2 - music_vol_text.get_height()/2))

                    # Draws Music Volume setting
                    indicator_x = 210
                    indicator_y = 100 + 105*4

                    self.surface.blit(enabled_panel, (indicator_x - enabled_panel.get_width()/2, indicator_y))

                    self.surface.blit(music_vol_panel, (indicator_x - enabled_panel.get_width()/2 - music_vol_panel.get_width() - 10, indicator_y))
                    self.surface.blit(self.relation_arrows['down'], (indicator_x - enabled_panel.get_width()/2 - music_vol_panel.get_width()/2 - 10 - self.relation_arrows['down'].get_width()/2,
                                                                   indicator_y + music_vol_panel.get_height()/2 - self.relation_arrows['down'].get_height()/2))

                    self.surface.blit(music_vol_panel, (indicator_x + enabled_panel.get_width()/2 + 10, indicator_y))
                    self.surface.blit(self.relation_arrows['up'], (indicator_x + enabled_panel.get_width()/2 + music_vol_panel.get_width()/2 + 10 - self.relation_arrows['up'].get_width()/2,
                                                                   indicator_y + music_vol_panel.get_height()/2 - self.relation_arrows['up'].get_height()/2))


                    sfx_vol_text = self.data_font.render(str(self.options.sfx_volume), True, (0,0,0))
                    self.surface.blit(sfx_vol_text, (indicator_x  - music_vol_text.get_width()/2,
                                                         indicator_y + enabled_panel.get_height()/2 - music_vol_text.get_height()/2))





                    # Draws a description of the currently selected option
                    self.surface.blit(desc_panel, (630 - desc_panel.get_width()/2, 360))
                    self.surface.blit(text_desc, (630 - text_desc.get_width()/2, 370))
                    draw_aligned_text(self.surface, text_option_desc[menu_pos], self.message_font, (0, 0, 0),
                                      (640 - desc_panel.get_width()/2, 400), desc_panel.get_width() - 20)

                    pygame.display.flip()

                self.clock.tick(60)


    def treasure_menu(self):
        """
        # Function Name: treasure menu
        # Purpose: Allows player to view available treasures
        """

        small_icon_panel = get_ui_panel((41, 41), border_color, panel_color)
        header_panel = get_ui_panel((200, 60), border_color, panel_color)
        item_panel = get_ui_panel((260, 41), border_color, panel_color)
        desc_panel = get_ui_panel((320, 180), border_color, panel_color)

        text_header_ingredients = self.title_font.render("Synth", True, (0, 0, 0))
        text_header_artifacts = self.title_font.render("Artifacts", True, (0, 0, 0))
        text_header_key_items = self.title_font.render("Key Items", True, (0, 0, 0))

        text_synth_items = []
        text_artifacts = []
        text_key_items = []

        # Generates treasure objects
        for treasure_key in self.player.treasures.keys():
            text_single_treasure_data = []
            # Format (Text objects)
                # [name(string), small_name, quantity, type, description]
            text_single_treasure_data.append(self.treasure_catalog[treasure_key].name)
            text_single_treasure_data.append(self.section_font.render(self.treasure_catalog[treasure_key].name, True, (0, 0, 0)))
            text_single_treasure_data.append(self.data_font.render(str(self.player.treasures[treasure_key]), True, (0, 0, 0)))
            text_single_treasure_data.append(self.treasure_catalog[treasure_key].icon)
            text_single_treasure_data.append(self.treasure_catalog[treasure_key].desc)

            if self.treasure_catalog[treasure_key].type == "Spell Synthesis Item":
                text_synth_items.append(text_single_treasure_data)
            elif self.treasure_catalog[treasure_key].type == "Generic":
                text_artifacts.append(text_single_treasure_data)
            else:
                text_key_items.append(text_single_treasure_data)

        text_synth_items.sort()
        text_artifacts.sort()
        text_key_items.sort()
        text_item_descriptions = [text_synth_items, text_artifacts, text_key_items]

        # Sets up the scroll bar
        max_slots = 8
        scroll_bar_total = 60*8 - 20
        if len(text_synth_items) > max_slots:
            scroll_length_synth = scroll_bar_total*max_slots/len(text_synth_items)
            scroll_delta_synth = scroll_bar_total / (len(text_synth_items) - max_slots)

            scroll_bar_synth = get_ui_panel((20, scroll_length_synth), border_color, scroll_bar_color)
        else:
            scroll_bar_synth = None
            scroll_delta_synth = 0

        if len(text_artifacts) > max_slots:
            scroll_length_artifacts = scroll_bar_total*max_slots/len(text_artifacts)
            scroll_delta_artifacts = (scroll_bar_total - scroll_length_artifacts)/ (len(text_artifacts) - max_slots)

            scroll_bar_artifacts = get_ui_panel((20, scroll_length_artifacts), border_color, scroll_bar_color)
        else:
            scroll_bar_artifacts = None
            scroll_delta_artifacts = 0

        if len(text_key_items) > max_slots:

            scroll_length_key = scroll_bar_total*max_slots/len(text_artifacts)
            scroll_delta_key = scroll_bar_total / (len(text_artifacts) - max_slots)

            scroll_bar_key = get_ui_panel((20, scroll_length_key), border_color, scroll_bar_color)
        else:
            scroll_bar_key = None
            scroll_delta_key = 0

        scroll_bar = get_ui_panel((20, scroll_bar_total), border_color, panel_color)
        # Item list: 0 - Synth items, 1 - Artifacts, 2 - Key Items
        item_list_pos = 0
        menu_pos = 0
        offset = 0

        update = True
        menu_flag = True

        while menu_flag:

            menu_pos_before = menu_pos

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        update = True

                        # Top of the list, jump to the bottom
                        if menu_pos == 0:
                            menu_pos = len(text_item_descriptions[item_list_pos]) - 1
                            offset = max(0, len(text_item_descriptions[item_list_pos]) - max_slots)

                        # Top of the itnerval, shift offset up
                        elif menu_pos == offset:
                            menu_pos -= 1
                            offset -= 1

                        # within interval, move cursor without changing shift
                        elif menu_pos > 0:
                            menu_pos -= 1

                    if event.key == K_DOWN:
                        update = True

                        # Bottom of the list of slots: Jumps to the top
                        if menu_pos == len(text_item_descriptions[item_list_pos]) - 1:
                            menu_pos = 0
                            offset = 0

                        # Bottom of the interval, advance the offset by 1
                        elif menu_pos == offset + max_slots - 1:
                            offset += 1
                            menu_pos += 1

                        # intermediate interval: move the cursor only down by 1
                        elif menu_pos < len(text_item_descriptions[item_list_pos]) - 1:
                            menu_pos += 1


                    if event.key == K_RIGHT:
                        if item_list_pos < 2:
                            item_list_pos += 1
                        elif item_list_pos == 2:
                            item_list_pos = 0
                        menu_pos = 0
                        offset = 0
                        update = True
                    if event.key == K_LEFT:
                        if item_list_pos > 0:
                            item_list_pos -= 1
                        elif item_list_pos == 0:
                            item_list_pos = 2
                        menu_pos = 0
                        offset = 0
                        update = True

                    if event.key == K_x:
                        # Cancel
                        menu_flag = False

            if menu_flag:


                if update:

                    update = False

                    self.surface.blit(self.stats_bg, (0, 0))

                    # Draws the options at the top
                    self.surface.blit(header_panel, (90, 20))
                    self.surface.blit(text_header_ingredients, (90 + header_panel.get_width()/2 - text_header_ingredients.get_width()/2,
                                                         22 + header_panel.get_height()/2 - text_header_ingredients.get_height()/2))
                    self.surface.blit(header_panel, (320, 20))
                    self.surface.blit(text_header_artifacts, (320 + header_panel.get_width()/2 - text_header_artifacts.get_width()/2,
                                                         22 + header_panel.get_height()/2 - text_header_artifacts.get_height()/2))
                    self.surface.blit(header_panel, (550, 20))
                    self.surface.blit(text_header_key_items, (550 + header_panel.get_width()/2 - text_header_key_items.get_width()/2,
                                                         22 + header_panel.get_height()/2 - text_header_key_items.get_height()/2))

                    padlib_rounded_rect(self.surface, selected_color, (88 + 230*item_list_pos,
                                                                         18, header_panel.get_width() + 4, header_panel.get_height() + 4), 6, 5)

                    for index, text_item_description in enumerate(text_item_descriptions[item_list_pos][offset:offset+max_slots]):

                        # Draws the item name
                        self.surface.blit(item_panel, (50, 100 + 60*index))
                        self.surface.blit(text_item_description[1], (50 + item_panel.get_width()/2 - text_item_description[1].get_width()/2,
                                                                     102 + item_panel.get_height()/2 - text_item_description[1].get_height()/2 + 60*index))
                        # Draws the item quantity
                        self.surface.blit(small_icon_panel, (330, 100 + 60*index))
                        self.surface.blit(text_item_description[2], (331 + small_icon_panel.get_width()/2 - text_item_description[2].get_width()/2,
                                                                     100 + small_icon_panel.get_height()/2 - text_item_description[2].get_height()/2 + 60*index))

                    if text_item_descriptions[item_list_pos]:

                        # Draws the item select cursor
                        padlib_rounded_rect(self.surface, selected_color, (48,
                                                                         98 + 60*(menu_pos - offset), item_panel.get_width() + 4, item_panel.get_height() + 4), 6, 5)

                        # Draw the data of the selected item
                        text_selected_item = text_item_descriptions[item_list_pos][menu_pos]

                        self.surface.blit(small_icon_panel, (470, 100))
                        self.surface.blit(self.icons[text_selected_item[3]], (470 + small_icon_panel.get_width()/2 - self.icons[text_selected_item[3]].get_width()/2,
                                                                           100 + small_icon_panel.get_height()/2 - self.icons[text_selected_item[3]].get_height()/2))

                        self.surface.blit(item_panel, (530, 100))
                        self.surface.blit(text_selected_item[1], (530 + item_panel.get_width()/2 - text_selected_item[1].get_width()/2,
                                                                     102 + item_panel.get_height()/2 - text_selected_item[1].get_height()/2))

                        self.surface.blit(desc_panel, (470, 150))
                        draw_aligned_text(self.surface, text_selected_item[4], self.message_font, (0, 0, 0), (480, 160), 300 )

                    # Draws the scroll bar
                    if len(text_item_descriptions[item_list_pos]) > max_slots:
                        self.surface.blit(scroll_bar, (410, 100))

                        if item_list_pos == 0:
                            scroll_bar_section = scroll_bar_synth
                            scroll_delta = scroll_delta_synth
                        elif item_list_pos == 1:
                            scroll_bar_section = scroll_bar_artifacts
                            scroll_delta = scroll_delta_artifacts
                        else:
                            scroll_bar_section = scroll_bar_key
                            scroll_delta = scroll_delta_key

                        if offset == len(text_item_descriptions[item_list_pos]) - max_slots:
                            self.surface.blit(scroll_bar_section, (410, 100 + scroll_bar_total - scroll_bar_section.get_height()))
                        else:
                            self.surface.blit(scroll_bar_section, (410, 100 + scroll_delta * offset))

                pygame.display.flip()
                self.clock.tick(60)

    def spell_swap_inventory(self, unit):
        """
        # Function name: spell_swap_inventory
        # Purpose: Selects spell to swap into the unit from the inventory
        # Inputs: None
        # Outputs: False - if no selection has been made
        #          selected spell, inventory_list - spell and inventory if a selection has been made
        """

        menu_flag = True
    
        offset = 0
        menu_pos = [0, 0]

        update = True
        max_slots = 6

        while menu_flag:
            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        # Top of the list, jump to the bottom
                        if menu_pos[1] == 0:
                            menu_pos[1] = len(self.player.items[menu_pos[0]])-1
                            offset = max(0, len(self.player.items[menu_pos[0]]) - max_slots)

                        # Top of the itnerval, shift offset up
                        elif menu_pos[1] == offset:
                            menu_pos[1] -= 1
                            offset -= 1

                        # within interval, move cursor without changing shift
                        elif menu_pos[1]  > 0:
                            menu_pos[1]  -= 1

                        update = True
                    if event.key == K_DOWN:

                        # Bottom of the list of slots: Jumps to the top
                        if menu_pos[1] == len(self.player.items[menu_pos[0]]) - 1:
                            menu_pos[1]  = 0
                            offset = 0

                        # Bottom of the interval, advance the offset by 1
                        elif menu_pos[1] ==  offset + max_slots - 1:
                            offset += 1
                            menu_pos[1] += 1

                        # intermediate interval: move the cursor only down by 1
                        elif menu_pos[1] < len(self.player.items[menu_pos[0]]) - 1:
                            menu_pos[1] += 1

                        update = True

                    if event.key == K_LEFT:
                        if menu_pos[0] > 0:
                            menu_pos[0] -= 1
                        elif menu_pos[0] == 0:
                            menu_pos[0] = 3
                        # Resets the vertical position of the cursor when inventory slots are swapped
                        menu_pos[1] = 0
                        offset = 0
                        update = True

                    if event.key == K_RIGHT:
                        if menu_pos[0] < 3:
                            menu_pos[0] += 1
                        elif menu_pos[0] == 3:
                            menu_pos[0] = 0
                        # Resets the vertical position of the cursor when inventory slots are swapped
                        menu_pos[1] = 0
                        offset = 0

                        update = True

                    if (event.key == K_z or event.key == K_RETURN) and self.player.items[menu_pos[0]]:
                        if self.player.items[menu_pos[0]][menu_pos[1]]:

                            # Runs the verification
                            can_equip = self.player.items[menu_pos[0]][menu_pos[1]].check_restrictions(unit)

                            if can_equip:
                                # Pull the spell from the inventory
                                selected_spell = self.player.items[menu_pos[0]].pop(menu_pos[1])
                                return selected_spell, menu_pos[0]

                    if event.key == K_x:
                        # Cancel
                        menu_flag = False
                        return False

            if update:
                update = False
                # Draws the inventory list
                self.surface.blit(self.stats_bg, (0, 0))
                self.draw_inventory_categories(menu_pos[0])
                self.draw_spell_inventory_list(unit, self.player.items[menu_pos[0]], offset, menu_pos[1])
                self.draw_spell_inventory_scrollbar(len(self.player.items[menu_pos[0]]), offset)

                # Draws the currently selected spell's data and who can equip it
                if self.player.items[menu_pos[0]]:
                    self.draw_spell_action_data(self.player.items[menu_pos[0]][menu_pos[1]])
                    self.draw_equippable(self.player.items[menu_pos[0]][menu_pos[1]])

                pygame.display.flip()

            self.clock.tick(60)

    def draw_inventory_categories(self, menu_pos):
        """
        Function name: draw_inventory_categories

        Draws the indicators for the three inventory categories at the top, and the cursor

        Inputs; menu_pos: currently viewed inventory:
                    0: Attack
                    1: Support
                    2: Spell Cards
                    3: Items
        """


        category_panel = get_ui_panel((140, 35), border_color, panel_color)

        category_list = ["Attack","Support","Spell Card","Item"]
        text_categories = [self.section_font.render(category, True, (0, 0, 0)) for category in category_list]

        # Draws the four categories at the top
        for index, text_category in enumerate(text_categories):
            self.surface.blit(category_panel, (125+150*index, 10))
            self.surface.blit(text_category, (125 + category_panel.get_width()/2 - text_category.get_width()/2 + 150*index,
                                              12 + category_panel.get_height()/2 - text_category.get_height()/2))

        # Draws the cursor for the selected one
        padlib_rounded_rect(self.surface, selected_color, (123 + 150*menu_pos, 8, category_panel.get_width()+4, category_panel.get_height()+4), 6, 5)

    def draw_spell_inventory_scrollbar(self, spell_list_length, offset):
        """
        Function Name: draw_spell_inventory_scrollbar

        Purpose: draws the scroll bar for the currently viewed spell inventory

        Inputs: spell_list_length - how many items are in that list
                offset - How far the current view window is in the list
        """


        max_slots = 6

        # Do not draw scrollbar if number of items is less than max length
        if spell_list_length <= max_slots:
            return

        scroll_bar_total = max_slots*60 - 19

        scroll_bar = get_ui_panel((20, scroll_bar_total), border_color, panel_color)

        # Calculates the length of the scroll bar section and how far the spacing is
        scroll_length = scroll_bar_total*max_slots/spell_list_length
        scroll_delta = (scroll_bar_total - scroll_length) / (spell_list_length - max_slots)

        scroll_bar_section = get_ui_panel((20, scroll_length), border_color, scroll_bar_color)

        self.surface.blit(scroll_bar, (410, 60))

        # Special case to clamp the scroll bar at the bottom of the screen to correct for round off
        if offset == spell_list_length - max_slots:
            self.surface.blit(scroll_bar_section, (410, 60 + scroll_bar_total - scroll_bar_section.get_height()))
        else:
            self.surface.blit(scroll_bar_section, (410, 60 + scroll_delta * offset))

    def draw_spell_inventory_list(self, unit, spell_list, offset, menu_pos):
        """
        function name: draw_spell_inventory_list

        Purpose: Draws a list of max 6 spells in the currently viewed list

        Inputs: Unit - Unit attempting to equip a spell from this list.
                spell_list - A list of spell objects to display
                offset - Current index position of the list view window
                menu_pos - Current position of the inventory cursor

        """

        max_slots = 6

        small_icon_panel = get_ui_panel((41, 41), border_color, panel_color)
        spell_panel = get_ui_panel((230, 41), border_color, panel_color)
        disabled_panel = get_ui_panel((230, 41), border_color, disabled_color)

        for index, spell in enumerate(spell_list[offset:min(offset+max_slots, len(spell_list))]):
            text_spell = self.message_font.render(spell.namesuffix, True, (0, 0, 0))
            text_uses = self.data_font.render("%d"%spell.livesleft, True, (0, 0, 0))

            # Draw icon for spell
            self.surface.blit(small_icon_panel, (45, 60 + 60*index))
            spell_icon_position = (45 + small_icon_panel.get_width()/2 - self.spell_type_icons['Item'].get_width()/2,
                                   60 + small_icon_panel.get_height()/2 - self.spell_type_icons['Item'].get_height()/2 + 60*index)
            if spell.type in ('healing', 'support'):
                self.surface.blit(self.spell_type_icons['Healing'], spell_icon_position)
            elif spell.type == "healingitem":
                self.surface.blit(self.spell_type_icons['Item'], spell_icon_position)
            else:
                self.surface.blit(self.spell_type_icons[spell.affinity], spell_icon_position)

            # Use a disabled panel if spell cannot be used
            if spell.check_restrictions(unit):
                self.surface.blit(spell_panel, (95, 60 + 60*index))
            else:
                self.surface.blit(disabled_panel, (95, 60 + 60*index))

            # Draw spell name
            self.surface.blit(text_spell, (95 + spell_panel.get_width()/2 - text_spell.get_width()/2,
                                           60 + spell_panel.get_height()/2 - text_spell.get_height()/2 + 60*index))

            # Draw number of uses remaining
            self.surface.blit(small_icon_panel, (335, 60 + 60*index))
            self.surface.blit(text_uses, (335 + small_icon_panel.get_width()/2 - text_uses.get_width()/2,
                                           60 + small_icon_panel.get_height()/2 - text_uses.get_height()/2 + 60*index))

        # Only draw the cursor if there are actually items in the spell list
        if spell_list:
            padlib_rounded_rect(self.surface, selected_color, (93, 58 + 60*(menu_pos - offset), spell_panel.get_width()+4, spell_panel.get_height()+4), 6, 5)


    def draw_equippable(self, spell):
        """
        Function name: draw_equippable

        Purpose: Draw all the characters in the party and show if they can use this spell

        Inputs: spell - Spell action to check against
        """

        equippable_panel = get_ui_panel((330, 160), border_color, panel_color)

        self.surface.blit(equippable_panel, (210 - equippable_panel.get_width()/2, 420))

        for index, unit in enumerate(self.player_units):
            # Determine unit position
            unit_x = 70+50*(index%6)
            unit_y = 435+50*(index/6)

            # Draw shadow for unit
            self.surface.blit(self.unit_tile, (unit_x, unit_y+2))

            # Use regular image if unit can use it and a darkened image if unit cannot equip it.
            if spell.check_restrictions(unit):
                self.surface.blit(unit.image, (unit_x, unit_y), (0, 0, 35, 35))
            else:
                self.surface.blit(unit.image, (unit_x, unit_y), (105, 0, 35, 35))


    def data_summary(self):

        """
        # Function Name: data_summary
        # Purpose: Returns a summary of all player data (including saved Data)
        #               -Average Level
        #               -Mission Complete Count
        # Outputs: data_report - report containing above information
        #                        [Current Data, Save 1-4, Autosave]
        """

        def player_report(player):

            """
            # Function Name: player_report
            # Purpose: Returns a summary of player data
            #               -Average Level
            #               -Mission Complete Count
            # Inputs: Player Data
            """

            total_unit_level = 0
            missions_completed = 0
            # Sums up total unit level

            for unit_data in player.all_unit_data.values():
                total_unit_level += unit_data.level
            # Sums up amount of missions completed
            for event_data in player.all_event_data.values():
                if event_data.done:
                    missions_completed += 1

            # Subtract 1 from final mission complete count since prologue doesn't count
            if self.all_events_master['Prologue'].done:
                missions_completed -= 1

            # computes the average unit level
            level_avg = str(int(total_unit_level / len(player.all_unit_data.values())))

            # Comment about the save data
            comment = player.comment

            return (str(missions_completed), level_avg,  comment)

        data_report = []
        #data_report.append(player_report(self.player))


        # Attempts to load the Autosave Slot 1
        try:
            data_file = open(get_file_path('autosave01.dat'), 'rb')
            # Temporarily loads the player data
            temp_player = pickle.load(data_file)
            data_report.append(player_report(temp_player))
        except IOError:
            data_report.append("No Data")


        # Attempts to load the Autosave Slot 2
        try:
            data_file = open(get_file_path('autosave02.dat'), 'rb')
            # Temporarily loads the player data
            temp_player = pickle.load(data_file)
            data_report.append(player_report(temp_player))
        except IOError:
            data_report.append("No Data")

        # Iterates over all four save slots
        save_data = ['autosave01.dat', 'autosave02.dat']

        manual_saves = [filename for filename in os.listdir(get_file_path()) if 'savedata' in filename and '.dat' in filename]

        if manual_saves:
            manual_saves.reverse()
            save_data += manual_saves

        for index, data_filename in enumerate(save_data[2:]):
            # Attempts to load the data
            try:
                data_file = open(get_file_path(data_filename), 'rb')
                # Temporarily loads the player data
                temp_player = pickle.load(data_file)
                data_report.append(player_report(temp_player))
            except IOError:
                data_report.append("No Data")


        return data_report, save_data

    def load_player(self, filename):

        """
        # Function Name: load_player
        # Purpose: loads player data from file
        # Inputs: slot - save slot to load from
        """
        print filename

        # Attempts to load game save data
        try:
            self.player = self.player.load(filename)

        # If it fails, aborts load
        except IOError:
            print "No Player Data Available"
            return

        # Flushes the state of all player units before loading
        [unit.reset_state() for unit in self.player_units_catalog.values()]

        # Drops all party members from current game
        self.player_units = []
        self.player_units_by_name = {}

        # Brings back all party members in save data
        for unit_name in self.player.party_members:
            print unit_name+" being added to party"
            added_unit = self.player_units_catalog[unit_name]
            if added_unit.map == None:
                added_unit.map = self.worldmap
            self.player_units.append(added_unit)
            self.player_units_by_name[added_unit.name] = added_unit



        # Update to units
        for unit in self.player_units:
            self.player.all_unit_data[unit.name].update_to_unit(unit)
            unit.HP = unit.maxHP

            # Loads most recent version of spell
            for index, spell in enumerate(unit.spell_actions):
                if spell:
                    uses = spell.livesleft
                    new_spell = self.spell_catalog[spell.namesuffix].construct_spell()
                    new_spell.livesleft = uses

                    # Saves spell back into character
                    new_spell.get_attack_range(unit)
                    unit.spell_actions[index] = new_spell

        # Loads in updated data for player spells.
        for type_index, spell_list in enumerate(self.player.items):

            if spell_list:
                for spell_index, spell in enumerate(spell_list):

                    if spell:
                        uses = spell.livesleft
                        new_spell = self.spell_catalog[spell.namesuffix].construct_spell()

                        new_spell.livesleft = uses

                        self.player.items[type_index][spell_index] = new_spell




        # Adds in any new missions
        for event_id in self.all_events_master.keys():
            if event_id not in self.player.all_event_data.keys():
                print "New Mission detected! "+event_id
                # Adds the event to the player event data
                self.player.all_event_data[event_id] = EventData(self.all_events_master[event_id])


        # Update to events
        for id in self.player.all_event_data.keys():

            if id in self.all_events_master.keys():
                #Updates completion data for events
                self.player.all_event_data[id].update_to_event(self.all_events_master[id])
            else:
                # If an event no longer exists, delete it from the data
                del self.player.all_event_data[id]

        # Calls for a world map refresh
        self.worldmap.update_all_events()

    def update_player_data(self):

        """
        # Function Name: update player data
        # Purpose: updates the stored unit data
        """

        # Update from units
        for unit in self.player_units:
            self.player.all_unit_data[unit.name].update_from_unit(unit)

        # Update from events
        for event in self.all_events_master.values():
            self.player.all_event_data[event.event_id].update_from_event(event)

        self.worldmap.update_all_events()

    ############################################
    # Inventory Management Functions
    ############################################

    def get_inventory_list(self, list_num):
        """
        # Function Name: get_inventory_list
        # Purpose: Generates the text objects of the currently selected inventory list
        # Inputs: list - 0 for Offensive Spells
        #                1 for Healing Spells
        #                2 for Spell Cards
        #                3 for Items
        #                4 for Misc
        """

        text_inventory_list = []
        for item in self.player.items[list_num]:
            if not item:
                text_inventory_list.append((None, self.sfont.render('Empty', True, (100, 100, 100))))
            else:
                text_inventory_list.append((item.name, self.sfont.render(item.name, True, (0, 0, 0)), self.sfont.render(str(item.livesleft)+"/"+str(item.lives), True, (0, 0, 0))))
        return text_inventory_list

    def draw_uncreated_spell(self, spell_action_key):
        """
        # Function name: draw_spell_data
        # Purpose: draws information about a single spell that has not already been created
        # Inputs: Spell action key - name of spell action
        """
        # Generates data about the spell from a temporary spell action
        temp_spell = self.spell_catalog[spell_action_key].construct_spell()
        self.draw_spell_action_data(temp_spell)

    def draw_spell_action_data(self, spell_action):
        """
        # Function name: draw_spell_data
        # Purpose: draws information about a single spell on the right panel
        # Inputs: spell_action - spell action to draw
        #         text_spell_data - rendered text generated with self.get_selected_spell_data
        """

        # Preliminary text items

        small_icon_panel = get_ui_panel((41, 41), border_color, panel_color)
        short_panel = get_ui_panel((100, 35), border_color, panel_color)
        spell_type_panel = get_ui_panel((200, 35), border_color, panel_color)
        full_width_panel = get_ui_panel((310, 40), border_color, panel_color)
        description_panel = get_ui_panel((310, 120), border_color, panel_color)

        # Name and type
        text_name = self.title_font.render(spell_action.namesuffix, True, (0,0,0))
        if not spell_action.consumable:
            spell_type = "Spell Card"
        elif spell_action.type == 'attack':
            spell_type = "Attack Spell"
        elif spell_action.type == 'healing':
            spell_type = "Healing Spell"
        elif spell_action.type == 'support':
            spell_type = "Support Spell"
        elif spell_action.type == 'healingitem':
            spell_type = "Item"
        else:
            spell_type = "Other"
        text_type = self.data_font.render(spell_type, True, (0,0,0))

        self.surface.blit(text_name, (840*3/4 - text_name.get_width()/2, 70-text_name.get_height()/2))

        self.surface.blit(spell_type_panel, (840*3/4 - spell_type_panel.get_width()/2, 100))
        self.surface.blit(text_type, (840*3/4 - text_type.get_width()/2, 100 + spell_type_panel.get_height()/2 - text_type.get_height()/2))


        # Spell type icon
        self.surface.blit(small_icon_panel, (475, 97))
        if spell_action.type == 'attack':
            spell_icon = self.spell_type_icons[spell_action.affinity]
        elif spell_action.type == 'healingitem':
            spell_icon = self.spell_type_icons['Item']
        else:
            spell_icon = self.spell_type_icons['Healing']

        self.surface.blit(spell_icon, (475 + small_icon_panel.get_width()/2 - spell_icon.get_width()/2,
                                       97 + small_icon_panel.get_height()/2 - spell_icon.get_height()/2))

        # Uses remaining
        if spell_action.livesleft == 0:
            number_color = (200, 20, 20)
        else:
            number_color = (0, 0, 0)

        self.surface.blit(small_icon_panel, (840 - 55 - small_icon_panel.get_width(), 97))
        text_uses_remaining = self.section_font.render(str(spell_action.livesleft), True, number_color)
        self.surface.blit(text_uses_remaining, (840 - 55 - small_icon_panel.get_width()/2 - text_uses_remaining.get_width()/2,
                                                99 + small_icon_panel.get_height()/2 - text_uses_remaining.get_height()/2))

        self.surface.blit(description_panel, (475, 145))

        draw_aligned_text(self.surface, spell_action.desc, self.sfont, (0, 0, 0), (486, 155), description_panel.get_width() - 20)

        # Draws the user type, target effect type, and whether this can counterattack
        row_position = 335
        # Shows the source type for this spell
        # If this spell uses magic, show symbol for magic.
        # If this spell uses strength, show symbol for strength.
        self.surface.blit(short_panel, (475, row_position))
        text_source = self.data_font.render('User', True, (0,0,0))
        self.surface.blit(text_source, (475 + short_panel.get_width()/2 - text_source.get_width()/2,
                                        row_position + short_panel.get_height()/2 - text_source.get_height()/2))
        if spell_action.type in ('attack', 'healing'):
            if spell_action.attacktype == 'physical':
                source_icon = self.stats_icons.subsurface(0, 0, 50, 50)
            else:
                source_icon = self.stats_icons.subsurface(50, 0, 50, 50)
        # Support spell and items have no source type since they don't have unit dependent stats
        else:
            source_icon = self.stats_icons.subsurface(0, 150, 50, 50)

        # Shows the target damage type for this spell
        # If this spell does physical damage, the symbol for physical defense is shown
        # If this spell does magic damage, the symbol for magic defense is shown
        self.surface.blit(source_icon, (475 + short_panel.get_width()/2 - source_icon.get_width()/2, row_position - 60))
        self.surface.blit(short_panel, (840*3/4 - short_panel.get_width()/2, row_position))
        if spell_action.type == 'attack':
            if spell_action.damagetype == 'physical':
                effect_icon = self.stats_icons.subsurface(0, 50, 50, 50)
            else:
                effect_icon = self.stats_icons.subsurface(50, 50, 50, 50)
        else:
            effect_icon = self.stats_icons.subsurface(0, 150, 50, 50)
        self.surface.blit(effect_icon, (840*3/4-source_icon.get_width()/2, row_position - 60))
        text_effect = self.data_font.render('Target', True, (0, 0, 0))
        self.surface.blit(text_effect, (840*3/4 - text_effect.get_width()/2,
                                        row_position + short_panel.get_height()/2 - text_effect.get_height()/2))

        # Shows whether counterattack is possible (N/A for healing and items)
        # An okay sign if yes, a prohibited sign is displayed if counterattack is not enabled
        if spell_action.type == 'attack':
            if spell_action.counterattack:
                counter_icon = self.stats_icons.subsurface(50, 200, 50, 50)
            else:
                counter_icon = self.stats_icons.subsurface(0, 200, 50, 50)
        else:
            counter_icon = self.stats_icons.subsurface(0, 150, 50, 50)

        self.surface.blit(counter_icon, (840 - 55 - short_panel.get_width()/2 - counter_icon.get_width()/2, row_position - 60))
        self.surface.blit(short_panel, (840 - 55 - short_panel.get_width(), row_position))
        text_counter = self.data_font.render('Counter', True, (0, 0, 0))
        self.surface.blit(text_counter, (840 - 55 - short_panel.get_width()/2 - text_counter.get_width()/2,
                                        row_position + short_panel.get_height()/2 - text_counter.get_height()/2))

        # Display for the spell action's spirit charge minimum and unlock
        row_position += 40
        text_sc_min = self.section_font.render('SC Min.', True, (0, 0, 0))
        if spell_action.unlock:
            text_sc_min_value = self.data_font.render('%d'%spell_action.unlock, True, (0, 0, 0))
        else:
            text_sc_min_value = self.data_font.render('N/A', True, (0, 0, 0))

        text_sc_cost = self.section_font.render('Cost', True, (0, 0, 0))
        if spell_action.sc_cost:
            text_cost_value = self.data_font.render('%d'%spell_action.sc_cost, True, (0, 0, 0))
        else:
            text_cost_value = self.data_font.render('N/A', True, (0, 0, 0))
        self.surface.blit(full_width_panel, (475, row_position))
        self.surface.blit(text_sc_min, (495, row_position+full_width_panel.get_height()/2-text_sc_min.get_height()/2+3))
        self.surface.blit(text_sc_min_value, (495+text_sc_min.get_width()+10, row_position+full_width_panel.get_height()/2-text_sc_min.get_height()/2))
        self.surface.blit(text_sc_cost, (840-55-text_cost_value.get_width()-text_sc_cost.get_width()-30, row_position+full_width_panel.get_height()/2-text_sc_min.get_height()/2+3))
        self.surface.blit(text_cost_value, (840-55-text_cost_value.get_width()-20, row_position+full_width_panel.get_height()/2-text_sc_min.get_height()/2))

        # Display for the spell action's spirit use range
        row_position += 45
        self.surface.blit(full_width_panel, (475, row_position))
        text_range = self.section_font.render("Range", True, (0, 0, 0))
        text_range_value = self.data_font.render("%d - %d"%(spell_action.minrange, spell_action.spellrange), True, (0, 0, 0))
        range_width = (10 + text_range.get_width() + text_range_value.get_width())
        self.surface.blit(text_range, (840*3/4 - range_width/2, row_position+full_width_panel.get_height()/2-text_range.get_height()/2))
        self.surface.blit(text_range_value, (840*3/4 + range_width/2 - text_range_value.get_width(), row_position+full_width_panel.get_height()/2-text_range_value.get_height()/2 - 2))

        if spell_action.type == 'attack' or spell_action.type == 'healing':
            row_position += 45
            self.surface.blit(full_width_panel, (475, row_position))
            text_power = self.section_font.render("Power", True, (0, 0, 0))
            text_power_value = self.data_font.render("%2.1f"%spell_action.effect, True, (0, 0, 0))
            power_width = (10 + text_power.get_width() + text_power_value.get_width())
            self.surface.blit(text_power, (840*3/4 - power_width/2, row_position+full_width_panel.get_height()/2-text_power.get_height()/2))
            self.surface.blit(text_power_value, (840*3/4 + power_width/2 - text_power_value.get_width(), row_position+full_width_panel.get_height()/2-text_power_value.get_height()/2 - 2))

        # Draws the status effects this spell causes or cures
        if spell_action.status_effects:
            row_position += 45
            if spell_action.type in ('attack', 'support'):
                se_text = "Status Effects"
            elif spell_action.type in ('healing', 'healingitem'):
                se_text = "Cures"
            text_se_header = self.section_font.render(se_text, True, (0,0,0))
            self.surface.blit(spell_type_panel, (840*3/4 - spell_type_panel.get_width()/2, row_position))
            self.surface.blit(text_se_header, (840*3/4 - text_se_header.get_width()/2, row_position + spell_type_panel.get_height()/2 - text_se_header.get_height()/2+3))

            # Healing, support, and items have 100% success rate
            if spell_action.type in ('healing', 'healingitem', 'support'):
                probability = "100%"
                text_prob = self.data_font.render(probability, True, (0, 0, 0))
                status_list = spell_action.status_effects
                probability_list = [text_prob]*len(spell_action.status_effects)
            else:
                status_list = []
                probability_list = []
                for status, probability in spell_action.status_effects.items():
                    status_list.append(status)
                    probability_list.append(self.data_font.render(str(int(probability))+"%", True, (0,0,0)))

            # Draws each status effect, and the probability of it working
            row_counter = 0
            row_position += 40
            for index, status in enumerate(status_list):
                if row_counter == 0:
                    column_position = 475
                elif row_counter == 1:
                    column_position = 840*3/4 - short_panel.get_width()/2
                elif row_counter == 2:
                    column_position = 840 - 55 - short_panel.get_width()

                self.surface.blit(short_panel, (column_position, row_position))
                status_icon = self.status_effects_catalog[status].icon
                # Render the status effect
                self.surface.blit(status_icon, (column_position+7, row_position + short_panel.get_height()/2 - status_icon.get_height()/2))
                self.surface.blit(probability_list[index], (column_position-7+short_panel.get_width()-probability_list[index].get_width(), row_position + short_panel.get_height()/2 - probability_list[index].get_height()/2))

                row_counter += 1
                if row_counter > 2:
                    row_counter = 0
                    row_position += 40

    def draw_trait_data(self, trait):

        """
        # Function name: draw_trait_data
        # Purpose: Draws the trait information on the RHS stats screen
        # Inputs: text_selected_trait - text representation of trait properties
        """

        text_name = self.title_font.render(trait.name, True, (0,0,0))
        if trait.variation == 'Support':
            text_type = self.section_font.render('Support Type', True, (0,0,0))
        elif trait.variation == 'Proximity':
            text_type = self.section_font.render('Proximity Type', True, (0,0,0))
        else:
            text_type = self.section_font.render('Trait Skill', True, (0,0,0))

        # Preliminary text items
        small_icon_panel = get_ui_panel((41, 41), border_color, panel_color)
        trait_type_panel = get_ui_panel((260, 35), border_color, panel_color)
        full_width_panel = get_ui_panel((310, 40), border_color, panel_color)
        description_panel = get_ui_panel((310, 120), border_color, panel_color)

        self.surface.blit(text_name, (840*3/4 - text_name.get_width()/2, 67-text_name.get_height()/2))

        self.surface.blit(small_icon_panel, (475, 100))
        trait_icon = self.trait_type_icons[trait.variation]
        self.surface.blit(trait_icon, (475+small_icon_panel.get_width()/2-trait_icon.get_width()/2,
                                       100+small_icon_panel.get_height()/2-trait_icon.get_height()/2))




        self.surface.blit(trait_type_panel, (840 - 55 - trait_type_panel.get_width(), 102))
        self.surface.blit(text_type, (840 - 55 - trait_type_panel.get_width()/2 - text_type.get_width()/2,
                                      105 + trait_type_panel.get_height()/2 - text_type.get_height()/2))

        self.surface.blit(description_panel, (475, 145))
        draw_aligned_text(self.surface, trait.desc, self.sfont, (0, 0, 0), (486, 155), description_panel.get_width() - 20)

        row_position = 275

        # If it is a skill, show the required SC to execute
        if trait.variation == 'Trait Skill':
            skill = self.trait_actions_catalog[trait.name]
            text_sc_min = self.section_font.render('SC Min.', True, (0, 0, 0))
            text_sc_min_value = self.data_font.render('%d'%skill.sc_minimum, True, (0, 0, 0))

            text_sc_cost = self.section_font.render('Cost', True, (0, 0, 0))
            text_cost_value = self.data_font.render('%d'%skill.sc_cost, True, (0, 0, 0))
            self.surface.blit(full_width_panel, (475, row_position))
            self.surface.blit(text_sc_min, (495, row_position+full_width_panel.get_height()/2-text_sc_min.get_height()/2+3))
            self.surface.blit(text_sc_min_value, (495+text_sc_min.get_width()+10, row_position+full_width_panel.get_height()/2-text_sc_min.get_height()/2))
            self.surface.blit(text_sc_cost, (840-55-text_cost_value.get_width()-text_sc_cost.get_width()-30, row_position+full_width_panel.get_height()/2-text_sc_min.get_height()/2+3))
            self.surface.blit(text_cost_value, (840-55-text_cost_value.get_width()-20, row_position+full_width_panel.get_height()/2-text_sc_min.get_height()/2))

            row_position += 50

        # For proximity traits (and if applicable for skills), display range of effect
        if trait.variation == 'Proximity' or (trait.variation == "Trait Skill" and skill.show_range):

            self.surface.blit(full_width_panel, (475, row_position))
            text_range = self.section_font.render("Range", True, (0, 0, 0))
            if trait.variation == 'Proximity':
                text_range_value = self.data_font.render("%d"%(trait.range), True, (0, 0, 0))
            elif trait.variation == "Trait Skill":

                if skill.maxrange == skill.minrange:
                    text_range_value = self.data_font.render("%d"%(skill.maxrange), True, (0, 0, 0))
                else:
                    text_range_value = self.data_font.render("%d - %d"%(skill.minrange, skill.maxrange), True, (0, 0, 0))

            range_width = (10 + text_range.get_width() + text_range_value.get_width())
            self.surface.blit(text_range, (840*3/4 - range_width/2, row_position+full_width_panel.get_height()/2-text_range.get_height()/2))
            self.surface.blit(text_range_value, (840*3/4 + range_width/2 - text_range_value.get_width(), row_position+full_width_panel.get_height()/2-text_range_value.get_height()/2 - 2))

    def draw_treasure_data(self, treasure_key):

        """
        # Function name: draw_treasure_data
        # Purpose: draws information about a single treasure
        # Inputs: treasure_key - treasure id string
        """

        text_treasure = self.bfont.render("Treasure", True, (0, 0, 0))
        text_desc = self.bfont.render("Description", True, (0, 0, 0))
        text_single_treasure_data = self.get_single_treasure_data(treasure_key)
        # Renders currently selected treasure data
        self.surface.blit(text_single_treasure_data[0], (470, 50))
        self.surface.blit(text_treasure, (470, 70))
        self.surface.blit(text_desc, (480, 110))
        self.surface.blit(text_single_treasure_data[1], (490, 130))

    def draw_conversation_message(self, line, speaker = None, portrait = None):
        """
        draw_conversation_message

        Purpose: Draws a conversation message (and the name of the speaker and a portrait if specified)

        Inputs: line - the line of text to display
        Speaker: the person saying the line
        Portrait: the portrait of the speaker

        """

        name_panel = get_ui_panel((200, 35), border_color, panel_color)

        if speaker:
            text_speaker = self.speaker_font.render(speaker, True, (0, 0, 0))
        else:
            text_speaker = None


        self.surface.blit(self.text_board, (0, 490))

        # If the portrait is drawn, shift text over to the side, otherwise make use of the full length of the window
        if portrait:
            self.surface.blit(self.portrait_catalog[portrait], (10, 500))

            self.surface.blit(name_panel, (140, 505))
            self.surface.blit(text_speaker, (140 + name_panel.get_width()/2 - text_speaker.get_width()/2,
                                                    505 + name_panel.get_height()/2 - text_speaker.get_height()/2))
            draw_aligned_text(self.surface, line, self.message_font, (0, 0, 0), (140, 545), 680)

        else:
            if speaker:
                self.surface.blit(name_panel, (70, 505))
                self.surface.blit(text_speaker, (70 + name_panel.get_width()/2 - text_speaker.get_width()/2,
                                                        505 + name_panel.get_height()/2 - text_speaker.get_height()/2))
                draw_aligned_text(self.surface, line, self.message_font, (0, 0, 0), (20, 545), 800)
            else:
                draw_aligned_text(self.surface, line, self.message_font, (0, 0, 0), (20, 525), 800)

    def draw_choice_prompt(self, query, responses):

        """
        draw_choice_prompt

        Purpose: Draws a question and answers for the player to select
        Inputs: query - the question to ask the player
                responses - a set of (max 2) responses to ask the player
        Output: response - the selected response among the questions asked

        """

        text_query = self.speaker_font.render(query, True, (0, 0, 0))

        query_panel = get_ui_panel((830, 35), border_color, panel_color)
        option_panel = get_ui_panel((550, 35), border_color, panel_color)

        text_responses = []

        # Draws the background panel
        self.surface.blit(self.text_board, (0, 490))

        # Draws the question first
        self.surface.blit(query_panel, (5, 495))
        self.surface.blit(text_query, (420 - text_query.get_width()/2,
                                                  495 + query_panel.get_height()/2 - text_query.get_height()/2))

        # Then the responses
        for response in responses:
            text_responses.append(self.message_font.render(response, True, (0, 0, 0)))

            for index, response in enumerate(text_responses):
                self.surface.blit(option_panel, (140, 535 + 45*index))
                self.surface.blit(response, (420 - response.get_width()/2,
                                535 + option_panel.get_height()/2 - response.get_height()/2 + 45*index))



    def get_text_selected_trait(self, trait):

        """
        # Function name: get_text_selected_trait
        # Purpose: From a single trait, returns a list of text objects with the data
        # Inputs: trait - trait to be processed
        # Outputs: text_selected_trait - a list containing the text objects for the trait
        """

        if trait:
            text_selected_trait = [trait.name, self.sfont.render(trait.name, True, (0, 0, 0))]

            text_selected_trait.append(self.bfont.render(trait.name, True, (0, 0, 0)))
            text_selected_trait.append(self.sfont.render(trait.variation, True, (0, 0, 0)))
            text_selected_trait.append([])
            [text_selected_trait[4].append(self.sfont.render(line, True, (0, 0, 0))) for line in split_lines(trait.desc, 50)]

            text_selected_trait.append(self.sfont.render("STR: "+str(trait.statmods[0]*100)+"%", True, (0, 0, 0)))
            text_selected_trait.append(self.sfont.render("DEF: "+str(trait.statmods[1]*100)+"%", True, (0, 0, 0)))
            text_selected_trait.append(self.sfont.render("MAG: "+str(trait.statmods[2]*100)+"%", True, (0, 0, 0)))
            text_selected_trait.append(self.sfont.render("MDEF: "+str(trait.statmods[3]*100)+"%", True, (0, 0, 0)))
            text_selected_trait.append(self.sfont.render("ACC: "+str(trait.statmods[4]*100)+"%", True, (0, 0, 0)))
            text_selected_trait.append(self.sfont.render("AGL: "+str(trait.statmods[5]*100)+"%", True, (0, 0, 0)))
            text_selected_trait.append(self.sfont.render("MOVE: "+str(trait.movemod_add), True, (0, 0, 0)))
            text_selected_trait.append(self.sfont.render("EXP: "+str(trait.expmod*100)+"%", True, (0, 0, 0)))
            text_selected_trait.append(self.sfont.render("SC: "+str(trait.spiritmod*100)+"%", True, (0, 0, 0)))
            text_selected_trait.append([])


            # Displays the properties
            if trait.properties != []:
                for property in sorted(trait.properties):
                    text_selected_trait[14].append(self.sfont.render(property, True, (0, 0, 0)))

        # Case for empty trait slot
        else:
            text_selected_trait = [None, self.sfont.render("Empty", True, (100, 100, 100))]

        return text_selected_trait

    def splash_screen(self):
        """
        # Function Name: splash screen
        # Purpose: displays the splash screen(s)
        """

        self.surface.fill((255, 255, 255))
        pygame.display.flip()
        self.clock.tick(60)
        self.surface.blit(self.splash_fmp, (0, 0))
        self.fade_from('white', 0.5)
        self.pause(2.5)
        self.fade_to('white', 0.5)

    def title_screen(self, disable_load = False, demo_mission_name = None):
        """
        # Function Name: title screen
        # Purpose: Title screen menu
        # Inputs:
        #     - Disable Load: Flag to disable loading the game
        #     - demo_mission_name: If in demo mode, what mission to load instead of prologue
        """

        self.play_music('title')

        if self.enable_splash:
            self.splash_screen()

        menu_flag = True
        menu_pos = 0
        fade_flag = False

        print demo_mission_name

        while menu_flag:
            # looks for event type data to select interaction
            for event in pygame.event.get():

                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if ( event.key == K_UP or event.key == K_LEFT ):
                        if menu_pos > 0:
                            menu_pos -= 1
                        elif menu_pos == 0:
                            menu_pos = 3
                    if ( event.key == K_DOWN or event.key == K_RIGHT ):
                        if menu_pos < 3:
                            menu_pos += 1
                        elif menu_pos == 3:
                            menu_pos = 0

                    # Selection
                    if event.key == K_z or event.key == K_RETURN:
                        if menu_pos == 0:


                            if self.demo_mode == False:

                                self.worldmap.update_all_events()

                                self.fade_to('black')
                                if self.enable_prologue:
                                    #self.all_events_master['Prologue'].location = self.worldmap.all_locations_by_name[self.all_events_master['Prologue'].location_name]
                                    self.all_events_master['Prologue'].execute()

                                self.all_events_master['Prologue'].done = True
                                self.worldmap.update_all_events()

                                self.fade_to('black')
                                self.launch_wm()

                            else:

                                background = pygame.image.load(os.path.join('images', 'credits_bg.jpg'))
                                self.worldmap.update_all_events()
                                self.fade_to('black')

                                self.all_events_master[demo_mission_name].map.turn_loop()

                                pygame.mixer.music.stop()
                                self.show_the_end(background)



                        elif menu_pos == 1 and not disable_load:

                            self.all_events_master['Prologue'].done = True
                            self.worldmap.update_all_events()

                            self.fade_to('black')
                            confirm_load = self.save_menu(True)
                            if confirm_load == True:
                                self.launch_wm(True)
                            fade_flag = False

                        elif menu_pos == 2:
                            self.fade_to('black')
                            self.options_menu()
                            fade_flag = False

                        elif menu_pos == 3:
                            exit()

            self.surface.blit(self.title, (0, 0))
            self.surface.blit(self.title_cursor, (770, 110+60*menu_pos))

            if fade_flag == False:
                self.fade_from('white')
                fade_flag = True

            pygame.display.update(Rect(770, 110, 23, 203))
            self.clock.tick(60)

    def launch_wm(self, load_player=False):
        """
        # Function Name: launch world map
        # Purpose: start the world map
        # Inputs: load_player - False if new game, True if load from save game
        """

        # If new game, invokes navigate loop fresh start
        if not load_player:
            self.worldmap.navigate_loop()
        # Game has been loaded and new map is called up with saved player position
        while not self.check_event_completion(['CH5ST2']):
            self.worldmap.navigate_loop(True)

        if self.check_event_completion(['CH5ST2']):
            self.play_ending()

    def play_ending(self):

        if self.options.enable_music:
            pygame.mixer.music.load(os.path.join('music', self.music_catalog['credits'][0]))
            pygame.mixer.music.play(0)

        credits = xmlreader.get_credits_catalog()

        background = pygame.image.load(os.path.join('images', 'credits_bg.jpg'))

        for event_key in self.all_events_master.keys():
            if "Credits" in event_key:
                self.all_events_master[event_key].location = self.worldmap.all_locations_by_name['Western Village Path']


        self.show_credits(background, 'Level Design', credits['Level Design'])
        self.all_events_master['Credits1'].execute()
        self.show_credits(background, 'Programming', credits['Programming'])
        self.all_events_master['Credits2'].execute()
        self.show_credits(background, 'Art', credits['Art'])
        self.all_events_master['Credits3'].execute()
        self.show_credits(background, 'Music', credits['Music'])
        self.all_events_master['Credits4'].execute()
        self.show_credits(background, 'Design Advisors', credits['Design Advisors'])
        self.show_credits(background, 'Testing', credits['Testing'])
        self.all_events_master['Credits5'].execute()
        self.show_credits(background, 'Web Administrator', credits['Web Administrator'])
        self.show_credits(background, 'Image Resources', credits['Image Resources'])
        self.show_credits(background, 'SFX Resources', credits['SFX Resources'])
        self.all_events_master['Credits6'].execute()
        self.show_credits(background, 'Libraries', credits['Libraries'])
        self.all_events_master['Credits7'].execute()
        self.show_credits(background, 'Special Thanks', credits['Special Thanks'])
        self.show_credits(background, 'Original Work', credits['Original Work'])
        self.show_credits(background, 'Project Leader', credits['Project Leader'])
        self.show_credits(background, 'Copyright', credits['Copyright'])
        self.show_credits(background, 'Finally...', credits['Finally...'])
        self.all_events_master['Credits8'].execute()

        self.show_the_end(background)

    def show_credits(self, background, title, line_list):
        """
        Display a sequence of credits

        """

        # Makes font smaller to allow text to fit
        if len(title) > 9:
            title_text = self.newspaper_mission_title_font.render(title, True, (255, 255, 255))
        else:
            title_text = self.newspaper_title_font.render(title, True, (255, 255, 255))

        if len(line_list) > 5:
            name_list_text = [self.newspaper_body_font.render(line, True, (255, 255, 255)) for line in line_list]
        else:
            name_list_text = [self.newspaper_mission_title_font.render(line, True, (255, 255, 255)) for line in line_list]


        self.surface.blit(background, (0, 0))
        self.surface.blit(title_text, (420-title_text.get_width()/2, 50))
        for index, name_text in enumerate(name_list_text):

            self.surface.blit(name_text, (420-name_text.get_width()/2,150+(name_text.get_height()+5)*index))

        self.fade_from('black', 2.0)

        self.pause(max(2.0, 0.3*len(line_list)))

        self.fade_to('black', 2.0)

    def show_the_end(self, background):
        """

        """

        self.surface.blit(background, (0, 0))

        title_text = self.newspaper_title_font.render("The End", True, (255, 255, 255))
        exit_font = self.newspaper_body_font.render('Press any key to exit.', True, (255, 255, 255))
        self.surface.blit(title_text, (420-title_text.get_width()/2, 315-title_text.get_height()/2))
        self.surface.blit(exit_font, (10, 630 - exit_font.get_height()-2))

        pygame.display.flip()

        self.fade_from('black', 1.0)



        while True:
            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN):
                        exit()

            if not pygame.mixer.music.get_busy():
                self.play_music('title')


            self.clock.tick(60)

        def show_demo_ending_screen(self,background):

            """
            Ending screen for demo mode

            """

            self.play_music('title')

            self.surface.blit(background, (0, 0))

            title_text = self.newspaper_mission_title_font.render("Thank you everyone!", True, (255, 255, 255))
            self.surface.blit(title_text, (420-title_text.get_width()/2, 315-title_text.get_height()/2))

            pygame.display.flip()

            self.fade_from('black', 1.0)

            while True:
                # looks for event type data to select interaction
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                            exit()

                self.clock.tick(60)