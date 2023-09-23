# Lost Sky Project Main Program

enable_pygamesdl2 = False

if enable_pygamesdl2:

    try:
        import pygame_sdl2
        pygame_sdl2.import_as_pygame()

        pygame_sdl2mode = True

    except:
        pygame_sdl2mode = False
        print "Pygame SDL2 not found, attempting to load Pygame"

else:

    pygame_sdl2mode = False


import pygame
import os
import sys
import time
from lostsky.missions import mission_catalog
from lostsky.worldmap.worldmap import Worldmap
from lostsky.core.engine import Engine
from lostsky.core import xmlreader

try:
    from xdg import BaseDirectory
    use_xdg = True
except ImportError:
    use_xdg = False

def get_file_path(filename=None):
    if use_xdg:
        if filename == 'options.dat':
            directory = BaseDirectory.save_config_path('lostsky')
        else:
            directory = BaseDirectory.save_data_path('lostsky')
    else:
        directory = 'data'
    if filename:
        return os.path.join(directory, filename)
    return directory


def bootstrap():
    # Diagonstic print to text file mode
    if len(sys.argv) > 1:
        if sys.argv[1] == "-p":
            print "Enabled Diagnostic Printing to output.txt!"
            output_file = file(get_file_path('output.txt'), 'w')
            sys.stdout = output_file
            sys.stderr = output_file
            print "Started a run on %s" % (time.asctime())
        else:
            print "Invalid Debug Flag"
            print "   -p : Enable printing to a text file"

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    if pygame_sdl2mode:
        pygame.mixer.pre_init(frequency=44100, buffersize=32768)
    pygame.init()
    tilesize = 35
    size_x = 24
    size_y = 18
    size_window = (size_x, size_y)
    screen_size = (tilesize * size_x, tilesize * size_y)
    screen = pygame.display.set_mode(screen_size, 0, 32)
    pygame.display.set_icon(pygame.image.load(os.path.join('images', 'portrait', '02-youmu-av.png')).convert_alpha())

    # Engine Intialization
    #   Initialize player units catalog
    #   Initialize trait catalog
    #   Initialize the spell catalog
    #   Initialize unit animations catalog
    engine = Engine(screen, tilesize, size_window)
#    engine.player_units_catalog = xmlreader.get_player_unit_catalog()
#    engine.trait_catalog = xmlreader.get_trait_catalog()
#    engine.trait_learning_catalog = xmlreader.get_trait_learning_catalog()
#    for unit in
#    engine.spell_catalog = xmlreader.SpellCatalog()
#    engine.unit_anim_catalog = xmlreader.UnitAnimCatalog()
#    engine.enemynpc_units_catalog = xmlreader.EnemyNPCTemplatesCatalog()
#    engine.terrain_types, engine.terrain_data_by_symbol = xmlreader.get_terrain_data()
#    engine.layer_2_terrain_data = xmlreader.get_layer_2_data()
#    # Assigns character battle animations
#    for unit in engine.player_units_catalog.values():
#        if unit.animation_enable:
#            unit.anim_frames = engine.unit_anim_catalog[unit.anim_id_string]

    ####################################################
    # Initialization of the world map
    ####################################################
    region_list, region_paths_list, engine.region_backgrounds, engine.active_location_images, engine.inactive_location_images, engine.hidden_location_images = xmlreader.get_world_map(engine)
    wm = Worldmap(engine, region_list, region_paths_list)


    ##################################
    # Unit starting units initialization
    ##################################
    xmlreader.initialize_units(engine, 'initialize.xml')

    ##################################
    # Get Important Engine data
    ##################################
    mission_list = mission_catalog.get_catalog()
    engine.add_event_master(mission_list)
    engine.landmark_catalog = xmlreader.get_landmark_data()
    engine.hint_list = xmlreader.get_hint_list()
    engine.profile_list = xmlreader.get_profiles_list()
    engine.news_reports_list = xmlreader.get_news_reports()
    engine.treasure_catalog = xmlreader.TreasureCatalog()
    engine.music_catalog = xmlreader.get_music()
    engine.trading_catalog = xmlreader.TradingCatalog()
    engine.spell_recipes_catalog = xmlreader.get_spell_recipes()
    engine.portrait_catalog = xmlreader.get_portrait_catalog()
    engine.emotion_bubbles, engine.effect_animations = xmlreader.get_effects_catalog()

    ##################################
    # OTHER CUSTOM SETTINGS GO HERE
    ##################################

    engine.game_version = "1.1.1"

    # Debug Flags
    engine.enable_prologue = True
    engine.single_turn_win = False
    engine.enable_splash = True
    engine.enable_wm_tutorial = False
    engine.disable_ai = False
    engine.unlock_wm = False
    engine.unlock_shops = False
    engine.demo_mode = False

    ############################
    # Main Program
    ###########################
    pygame.display.set_caption("Story of a Lost Sky v%s" % engine.game_version)
    engine.title_screen()
    wm.navigate_loop()

def demo_mode(mission_name):


    # Diagonstic print to text file mode
    if len(sys.argv) > 1:
        if sys.argv[1] == "-p":
            print "Enabled Diagnostic Printing to output.txt!"
            output_file = file('output.txt', 'w')
            sys.stdout = output_file
            sys.stderr = output_file
            print "Started a run on %s" % (time.asctime())
        else:
            print "Invalid Debug Flag"
            print "   -p : Enable printing to a text file"

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    tilesize = 35
    size_x = 24
    size_y = 18
    size_window = (size_x, size_y)
    screen_size = (tilesize * size_x, tilesize * size_y)
    screen = pygame.display.set_mode(screen_size, 0, 32)

    engine = Engine(screen, tilesize, size_window)
    ####################################################
    # Initialization of the world map
    ####################################################
    region_list, region_paths_list, engine.region_backgrounds, engine.active_location_images, engine.inactive_location_images, engine.hidden_location_images = xmlreader.get_world_map(engine)
    wm = Worldmap(engine, region_list, region_paths_list)

    ##################################
    # Get Important Engine data
    ##################################
    mission_list = mission_catalog.get_catalog()
    engine.add_event_master(mission_list)

    engine.landmark_catalog = xmlreader.get_landmark_data()
    engine.hint_list = xmlreader.get_hint_list()
    engine.news_reports_list = xmlreader.get_news_reports()
    engine.treasure_catalog = xmlreader.TreasureCatalog()
    engine.music_catalog =xmlreader.get_music()
    engine.trading_catalog = xmlreader.TradingCatalog()
    engine.spell_recipes_catalog = xmlreader.get_spell_recipes()
    engine.portrait_catalog = xmlreader.get_portrait_catalog()
    engine.emotion_bubbles, engine.effect_animations = xmlreader.get_effects_catalog()


    ##################################
    # OTHER CUSTOM SETTINGS GO HERE
    ##################################

    engine.game_version = "1.1.1"

    # Debug Flags
    engine.enable_prologue = False
    engine.single_turn_win = False
    engine.disable_ai = False
    engine.enable_splash = False
    engine.enable_wm_tutorial = False
    engine.unlock_wm = False
    engine.unlock_shops = False
    engine.demo_mode = True
    ############################
    # Main Program - Configure your Mission here
    ###########################

    # Make sure your mission is loaded in the mission_catalog.py file.
    print "Launching Mission: %s"%mission_name

    # Add all characters. If the character is added during
    # a certain mission as part of the story, do not place them here.
    characters = {
                  'Youmu':{'level':15,
                        'spells':['Dagger Throw','Ageless Obsession'],
                        'traits':[] },

                  'Ran':{'level':15,
                            'spells':['Fireball','Princess Tenko','Mystic Wall','Mystic Barrier','Fried Tofu'],
                            'traits':[] },

                  'Chen':{'level':15,
                            'spells':['Leaf Crystal','Pentagram Flight', 'Rice Cake'],
                             'traits':[]},
                 'Marisa':{'level':15,
                             'spells':['Fireball','Master Spark','Rice Cake', 'Exorcism Tag'],
                             'traits':[]},
                 'Mokou':{'level':15,
                            'spells':['Dagger Throw','Flying Phoenix','Rice Cake'],
                              'traits':[] },

                 'Alice':{'level':15,
                            'spells':['Fireball','Artful Sacrifice','Rice Cake'],
                             'traits':[] },
                 #
                  }



    for unit_name,unit_info in characters.items():
        # Adds new units to catalog
        unit = engine.player_units_catalog[unit_name]

        engine.player_units.append(unit)
        engine.player_units_by_name[unit_name] = unit


        engine.player.add_unit_data(unit)

        unit.level = 1

        # sets unit to appropriate level
        while unit.level < unit_info['level']:
            unit.level_up()
            unit.level += 1
        unit.HP = unit.maxHP

        # Adds unit spells and traits
        [unit.add_spell(engine.spell_catalog[spell].construct_spell()) for spell in unit_info['spells']]

        unit.update_trait_learning_data()


    pygame.display.set_caption("Story of a Lost Sky v%s"%(engine.game_version))
    engine.worldmap.unit_associate()

    # Enables all Missions
    for event in engine.all_events_master.values():
        event.location = engine.worldmap.all_locations_by_name[event.location_name]

    engine.all_events_master[mission_name].map_init()
    if engine.all_events_master[mission_name].type == 'Conversation':
        engine.all_events_master[mission_name].map.nobattle = True

    print mission_name
    engine.title_screen(disable_load = True, demo_mission_name = mission_name)
