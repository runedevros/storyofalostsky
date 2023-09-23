# Lost Sky Project Single Mission Launcher
# Use this program to launch a single mission without needing the rest of the game

try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except:
    print "Pygame SDL2 not found, attempting to load Pygame"

import pygame
from pygame.locals import *
import sys
from lostsky.missions import mission_catalog
from lostsky.battle.mapobj import *
from lostsky.battle.spells import *
from lostsky.battle.animations import *
from lostsky.worldmap.worldmap import *
from lostsky.core.engine import Engine
from lostsky.core import xmlreader
import time

# Diagonstic print to text file mode
if len(sys.argv) > 1:
    if sys.argv[1] == "-p":
        print "Enabled Diagnostic Printing to output.txt!"
        output_file = file('output.txt','w')
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
size_window = (size_x,size_y)
screen_size = (tilesize*size_x,tilesize*size_y)
screen =  pygame.display.set_mode(screen_size,0, 32)

# Engine Intialization
#   Initialize player units catalog
#   Initialize trait catalog
#   Initialize the spell catalog
#   Initialize unit animations catalog
engine = Engine(screen,tilesize,size_window)

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

engine.game_version = ". Mission Tester"

# Debug Flags
engine.enable_prologue = False
engine.single_turn_win = False
engine.disable_ai = False
engine.enable_splash = False
engine.enable_wm_tutorial = False
engine.unlock_wm = False
engine.unlock_shops = False

############################
# Main Program - Configure your Mission here
###########################

# Make sure your mission is loaded in the mission_catalog.py file.
mission_name = 'CH3SQ1'
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
                        'spells':['Leaf Crystal','Pentagram Flight'],
                         'traits':[]},
             'Marisa':{'level':15,
                         'spells':['Fireball','Master Spark','Rice Cake', 'Exorcism Tag'],
                         'traits':[]},

             'Reimu':{'level':15,
                         'spells':['Holy Amulet','Fantasy Seal','Barrier Buster','Weakening Amulet'],
                         'traits':[] },
             'Keine':{'level':15,
                         'spells':['Healing Drop','Medicinal Drop','Sunbeam Mirror','Encourage'],
                         'traits':[] },

             'Mokou':{'level':15,
                        'spells':['Dagger Throw','Flying Phoenix','Rice Cake'],
                          'traits':[] },
             'Aya':{'level':15,
                        'spells':['Holy Amulet','Tengu Wind Path', 'Rice Cake'],
                        'traits':[] },
             # 'Reisen':{'level':28,
             #            'spells':['Dagger Throw','Invisible Full Moon'],
             #             'traits':[] },
             # 'Eirin':{'level':28,
             #            'spells':['Healing Drop', 'Medicinal Drop', 'Astral Entombing'],
             #             'traits':[] },
             # 'Kaguya':{'level':28,
             #            'spells':['Holy Amulet','Mysterium'],
             #             'traits':[] },

             'Alice':{'level':15,
                        'spells':['Fireball','Artful Sacrifice','Rice Cake'],
                         'traits':[] },
             #
             # #
             # 'Yukari':{'level':28,
             #            'spells':['Holy Amulet', 'Barrier Buster', 'Weakening Amulet', 'Ran and Chen'],
             #             'traits':[] },
             #
             #
             # 'Yuyuko':{'level':28,
             # 'spells':['Fireball', 'Resurrection Butterfly'],
             #   'traits':[] },

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


engine.all_events_master[mission_name].map.turn_loop()
