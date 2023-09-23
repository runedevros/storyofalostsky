from char import Unit, Doll
from lostsky.battle.spells import AttackSpell, SupportSpell, HealingSpell, HealingItem
from lostsky.battle.trait import SupportTrait, TraitSkill, ProximityTrait
from lostsky.battle.terrain import Terrain
from lostsky.worldmap.treasure import Treasure
from lostsky.worldmap.worldmap import Region, Location, Path
from lostsky.worldmap.trading import Trade
from lostsky.worldmap.spell_synthesis import Recipe
from xml.etree import ElementTree
from linalg import Vector2

import os
import pygame


def str_2_num_list(string):
    """
    # Function Name: str_2_num_list
    # Purpose: Given a string of the format (X, Y, Z) returns the list with XYZ integers
    # Inputs: string - a string in the above format
    # Outputs: num_list - a list of integers converted from the string format
    """

    # Validation that string is enclosed in brackets
    if string[0]+string[-1] == "()":
        # Splits by commas
        string_list = string[1:-1].split(',')
        num_list = []
        for number in string_list:
            num_list.append(int(number))
        return num_list

def get_music():
    """
    # Function Name: get_music
    # Purpose: Constructs the music dictionary
    # Output: music_dict - a dictionary of game songs
    """
    music_dict = {}
    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'music.xml')))
    for song_node in xml_data.findall('song'):
        song_name = song_node.attrib.get('name')
        id_string = song_node.find('id_string').text
        filename = song_node.find('filename').text
        music_dict[id_string] = [filename, song_name]
    return music_dict

def get_world_map(engine):

    """
    # Function Name: get_world_map
    # Purpose: Constructs the world map
    # Output: region_list - a list of regions
    """

    region_list = []
    location_type_dict = {'Neutral': 0, 'Danger': 1, 'Safe': 2, 'Gate': 3}
    directions = ['up', 'down', 'left', 'right']

    region_backgrounds = {}
    active_location_images = {}
    inactive_location_images = {}
    hidden_location_images = {}

    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'worldmap.xml')))
    # Loads all the regions
    for region_node in xml_data.findall('region'):

        # If this flag is enabled, enable the use of advanced backgrounds, otherwise fall back on default look
        enable_adv_background = region_node.attrib.get('advanced_background') == 'True'

        region_name = region_node.attrib.get('name')
        region_coords = Vector2(str_2_num_list(region_node.find('coords').text))
        region_desc = region_node.find('desc').text

        # Loads connecting region paths
        region_paths_data = xml_data.find('region_paths')
        region_paths = get_connecting_paths(region_paths_data)

        # Load region's top level images
        active_location_images[region_name] = pygame.image.load(os.path.join('images', 'map_background', region_node.find('active_image').text)).convert_alpha()
        inactive_location_images[region_name] = pygame.image.load(os.path.join('images', 'map_background', region_node.find('inactive_image').text)).convert_alpha()
        hidden_location_images[region_name] = pygame.image.load(os.path.join('images', 'map_background', region_node.find('hidden_image').text)).convert_alpha()

        # Load region's prerequisit missions for unlocking
        region_prereq = [prereq.text for prereq in region_node.findall('prereq')]

        if enable_adv_background:
            background_filename = region_node.find('background_image').text
            region_backgrounds[region_name] = pygame.image.load(os.path.join('images', 'map_background', background_filename)).convert()

        region_img_pos = Vector2(str_2_num_list(region_node.find('image_pos').text))

        region = Region(engine, region_name, region_coords, region_prereq, region_img_pos, enable_adv_background)
        region.desc = region_desc
        region.entrances = {}

        entrance_nodes = region_node.findall('entrance')
        #Case: There is only one entrance
        if len(entrance_nodes) == 1:
            region.entrances['default'] = region_node.find('entrance').text
        else:
            for entrance_node in entrance_nodes:
                # Default entrance node
                if entrance_node.attrib.get('default') == 'True':
                    region.entrances['default'] = entrance_node.text
                # Assigns entrances based on incoming directions
                region.entrances[entrance_node.attrib.get('direction')] = entrance_node.text

        # Loads all the locations
        location_list = []
        for location_node in region_node.find('locations').findall('location'):

            location_name = location_node.attrib.get('name')
            try:
                location_desc = location_node.find('desc').text
            except IndexError:
                location_desc = None
                print location_name+" needs a description!"
            location_coords = Vector2(str_2_num_list(location_node.find('coords').text))

            location_type = location_type_dict[location_node.find('type').text]
            location_portrait = location_node.find('portrait').text

            if enable_adv_background:
                active_location_images[location_name] = pygame.image.load(os.path.join('images', 'map_background', location_node.find('active_image').text)).convert_alpha()
                inactive_location_images[location_name] = pygame.image.load(os.path.join('images', 'map_background', location_node.find('inactive_image').text)).convert_alpha()
                hidden_location_images[location_name] = pygame.image.load(os.path.join('images', 'map_background', location_node.find('hidden_image').text)).convert_alpha()

                location_img_pos = Vector2(str_2_num_list(location_node.find('image_pos').text))
            else:
                location_img_pos = None

            if location_node.findall('prereq'):
                prereq = [item.text for item in location_node.findall('prereq')]
            else:
                prereq = []

            location = Location(location_name, location_desc, location_coords, location_type, location_portrait, location_img_pos, prereq)
            location_list.append(location)

        location_paths_data = region_node.find('location_paths')
        location_paths = get_connecting_paths(location_paths_data)

        region.add_locations(location_list)
        region.initialize_paths(location_paths)
        region_list.append(region)

    return region_list, region_paths, region_backgrounds, active_location_images, inactive_location_images, hidden_location_images

def get_connecting_paths(path_data_node):

    """
    # Function Name: get_connecting_paths
    # Purpose: From a region/worldmap's XML representation of paths, construct the list of paths
    # Inputs: path data node - Either the <region_paths> node in the worldmap or the <location_paths> node in each region
    # Outputs: Path list - a list of paths generated
    """

    directions = ['up', 'down', 'left', 'right']
    path_list = []
    for path_node in path_data_node.findall('path'):

        # Gets the two connected locations
        path_locations = {}
        for direction in directions:
            if path_node.findall(direction):
                path_locations[direction] = path_node.find(direction).text

        # Gets any prereq missions that have to be fulfilled for the path to be open
        path_prereqs = []
        [path_prereqs.append(prereq_node.text) for prereq_node in path_node.findall('prereq')]
        path_list.append(Path(path_locations, path_prereqs))

    return path_list

def get_landmark_data():

    """
    # Function Name: get_landmark_data
    # Purpose: get the landmark template data
    # Inputs: None
    # Outputs: landmark_catalog
    """
    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'landmark.xml')))
    landmark_catalog = {}

    for landmark_template_node in xml_data.findall('landmark_template'):

        # Loads landmark template data
        template_data =  {  'size': tuple(str_2_num_list(landmark_template_node.find('size').text)),
                            'img_coords': tuple(str_2_num_list(landmark_template_node.find('coords').text)),
                            'passable': landmark_template_node.find('passable').text == 'True'
                          }
        id_string = landmark_template_node.find('id_string').text

        landmark_catalog[id_string] = template_data
    return landmark_catalog


def initialize_units(engine, xml_filename):

    """
    #  Function Name: initialize_units
    # Purpose: Reads in the player unit initialization XML data and processes it, assigning traits, spells, and adding the units to the party
    # Inputs: Engine - Game system engine
    """
    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', xml_filename)))
    starting_unit_list = xml_data.findall('starting_unit')

    # Sets up the player units
    for starting_unit_node in starting_unit_list:
        unit = engine.player_units_catalog[starting_unit_node.attrib.get('name')]
        # Reads in the spell actions and traits
        for spell_action_node in starting_unit_node.findall('spell_action'):
            unit.add_spell(engine.spell_catalog[spell_action_node.text].construct_spell())

        engine.player_units.append(unit)
        engine.player_units_by_name[unit.name] = unit
        engine.player.add_unit_data(unit)

def get_hint_list():
    """
    # Function: Get hint list
    # Purpose: Constructs the hint catalog
    # Output: hint_list
    """
    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'hints.xml')))
    hint_list = []
    for hint_node in xml_data.findall('hint'):
        hint_name = hint_node.attrib.get('name')
        hint_author = hint_node.find('author').text
        hint_location = hint_node.find('location').text
        hint_text = hint_node.find('hint_text').text
        hint_prereqs = [prereq_node.text for prereq_node in hint_node.findall('prereq')]

        hint = Hint(hint_name, hint_author, hint_location, hint_text, hint_prereqs)
        hint_list.append(hint)

    return hint_list

class Hint(object):

    def __init__(self, name, author, location,  text, prereqs):
        self.name = name
        self.author = author
        self.location = location
        self.text = text
        self.prereqs = prereqs

def get_profiles_list():
    """
    # function: get_profiles_list
    # Purpose: collects the data for character profiles
    # output: profile_list - a list of profile data
    """

    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'profiles.xml')))

    profile_list = []
    for profile_node in xml_data.findall('profile'):

        name = profile_node.find('name').text
        title = profile_node.find('title').text
        specialty = profile_node.find('specialty').text
        image = profile_node.find('portrait').text
        desc = profile_node.find('desc').text
        prereqs = profile_node.find('unlock').text

        profile_data = CharaProfile(name, title, specialty, image, desc, prereqs)


        profile_list.append(profile_data)

    return profile_list


class CharaProfile(object):

    def __init__(self, name, title, specialty, image, desc, prereqs):
        self.name = name
        self.title = title
        self.specialty = specialty
        self.image = image
        self.desc = desc
        self.prereqs = prereqs


def get_news_reports():
    """
    # Function: Get news reports
    # Purpose: Constructs the top story list
    # Output: news_report_list
    """

    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'news_reports.xml')))
    news_report_list = []
    for report_node in xml_data.findall('report'):
        news_report = {}
        news_report['name'] = report_node.attrib.get('name')

        news_report['mission'] = report_node.find('mission').text
        news_report['date'] = report_node.find('date').text
        news_report['subtitle'] = report_node.find('subtitle').text
        news_report['location'] = report_node.find('location').text
        news_report['text'] = report_node.find('text').text

        news_report_list.append(news_report)

    return news_report_list

def get_spell_recipes():

    """
    # Function: Get spell recipes
    # Purpose: Construncts the catalog of spell creation recipes
    # Output: spell_recipes - a dictionary containing all the recipes
    """

    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'spellrecipes.xml')))

    spell_recipes_by_ing = {}
    spell_recipes_by_name = {}
    for recipe_node in xml_data.findall('recipe'):
        spell_name = recipe_node.find('spell_action').text
        ingredients_list = {}

        for ingredient_node in recipe_node.findall('ingredient'):
            ingredients_list[ingredient_node.find('item_id').text] = int(ingredient_node.find('quantity').text)

        recipe = Recipe(spell_name, ingredients_list)
        spell_recipes_by_name[recipe.spell_action] = recipe

    return spell_recipes_by_name

def get_portrait_catalog():
    """
    # function name: get_portrait_catalog()
    # purpose: constructs a catalog of conversation portraits
    """

    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'portraits.xml')))
    portrait_catalog = {}
    for portrait_node in xml_data.findall('portrait'):
        id_string = portrait_node.find('id_string').text
        portrait_catalog[id_string] = pygame.image.load(os.path.join('images', 'portrait', portrait_node.find('img').text)).convert()
    return portrait_catalog

def get_effects_catalog():
    """
    # function name: get_effects_catalog()
    # purpose: constructs a catalog of map effects
    """

    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'map_effect_animations.xml')))
    emote_catalog = {}
    effects_catalog = {}
    for anim_type in ('emote', 'effect'):
        for anim_node in xml_data.findall(anim_type):
            id_string = anim_node.find('id_string').text
            image = pygame.image.load(os.path.join('images', 'anim', 'effects', anim_node.find('image').text)).convert_alpha()
            frame_width = int(anim_node.find('frame_width').text)
            frame_height = int(anim_node.find('frame_height').text)
            frames_x = image.get_width()/frame_width
            frames_y = image.get_width()/frame_height
            delay = float(anim_node.find('delay').text)
            if anim_type == 'emote':
                emote_catalog[id_string] = {'image': image,
                                            'frame_width': frame_width,
                                            'frame_height': frame_height,
                                            'delay': delay }
            elif anim_type == 'effect':
                effects_catalog[id_string] = {'image': image,
                                              'frame_width': frame_width,
                                              'frame_height': frame_height,
                                              'delay': delay }

    return emote_catalog, effects_catalog


################
# Trait Catalog
###############

def get_trait_catalog():
    """
    # Function Name: get_trait_catalog
    # Purpose: returns a dict containing the game's traits
    """

    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'traits.xml')))
    trait_catalog = {}

    for trait_node in xml_data.findall('trait'):
        trait_name = trait_node.attrib.get('name')

        # Locates and loads type and description
        trait_type = trait_node.find('type').text
        trait_desc = trait_node.find('desc').text

        if trait_type == 'Support':

            # Gets the stat modifiers
            stats_node = trait_node.find('stat_mods')
            stat_mods = []
            for stat in ['STR', 'DEF', 'MAG', 'MDEF', 'ACC', 'AGL']:
                stat_mods.append(float(stats_node.find(stat).text))

            hit_bonus = int(trait_node.find('hit_bonus').text)
            evade_bonus = int(trait_node.find('evade_bonus').text)


            # Movement modifier
            move_mod_node = trait_node.find('move_mod')
            if move_mod_node.attrib.get('type') =='add':
                move_mod_add = int(trait_node.find('move_mod').text)
                move_mod_mult = 0
            elif move_mod_node.attrib.get('type') =='multiply':
                move_mod_add = 0
                move_mod_mult = int(trait_node.find('move_mod').text)
            else:
                move_mod_add = 0
                move_mod_mult = 0

            # Exp / SC mods
            spirit_mod = float(trait_node.find('spirit_mod').text)
            exp_mod = float(trait_node.find('exp_mod').text)

            #Additional Properties
            trait_properties = []

            if trait_node.findall('trait_properties'):
                properties_node = trait_node.find('trait_properties')
                for single_property in properties_node.findall('property'):
                    trait_properties.append(single_property.text)

            trait_catalog[trait_name] = SupportTrait(trait_name, trait_desc, stat_mods, hit_bonus, evade_bonus,
                move_mod_add, move_mod_mult, exp_mod, spirit_mod, trait_properties)

        elif trait_type == "Trait Skill":
            trait_catalog[trait_name] = TraitSkill(trait_name, trait_desc)

        elif trait_type == "Proximity":
            team_affected = trait_node.find('team').text
            trait_range = int(trait_node.find('range').text)

            # Gets the stat modifiers for emit and receive
            emit_node = trait_node.find('emit_mods')
            emit_mods = []
            for stat in ['STR', 'DEF', 'MAG', 'MDEF', 'ACC', 'AGL']:
                emit_mods.append(float(emit_node.find(stat).text))
            emit_hit_bonus = int(emit_node.find('hit_bonus').text)
            emit_evade_bonus = int(emit_node.find('evade_bonus').text)

            receive_node = trait_node.find('receive_mods')
            receive_mods = []
            for stat in ['STR', 'DEF', 'MAG', 'MDEF', 'ACC', 'AGL']:
                receive_mods.append(float(receive_node.find(stat).text))
            receive_hit_bonus = int(receive_node.find('hit_bonus').text)
            receive_evade_bonus = int(receive_node.find('evade_bonus').text)


        # Gets the target lists
            emit_target_node = trait_node.find('emit_targets')
            if emit_target_node is not None:
                emit_targets = [target_node.text for target_node in emit_target_node.findall('target')]
            else:
                emit_targets = []

            receive_sources_node = trait_node.find('receive_sources')
            if receive_sources_node is not None:
                receive_sources = [source_node.text for source_node in receive_sources_node.findall('source')]
            else:
                receive_sources = []


            trait_catalog[trait_name] = ProximityTrait(trait_name, trait_desc, team_affected, trait_range,
                            emit_mods, emit_hit_bonus, emit_evade_bonus, emit_targets, receive_mods,
                            receive_hit_bonus, receive_evade_bonus, receive_sources)





    return trait_catalog


def get_trait_learning_catalog():

    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'traitbranches.xml')))
    unit_nodes = xml_data.findall('unit')

    trait_learning_catalog = {}

    for unit_node in unit_nodes:
        unit_name = unit_node.attrib.get('name')
        trait_branch_nodes = unit_node.findall('trait_branch')
        trait_branch_data = []
        for branch_node in trait_branch_nodes:
            branch_name = branch_node.attrib.get('name')
            trait_list = []
            for trait in branch_node.findall('trait'):
                level = int(trait.attrib.get('level'))
                trait = trait.text
                trait_list.append((level, trait))
            trait_branch_data.append([branch_name, trait_list])
        trait_learning_catalog[unit_name] = trait_branch_data
    return trait_learning_catalog

####################################
# Unit Catalog Class
####################################
def get_player_unit_catalog():

    """
    # Function Name: get_player_unit_catalog():
    # Purpose: gets the dict of player units
    """
    player_units = {}
    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'playerunits.xml')))

    for unit_node in xml_data.findall('unit'):

        unit_name = unit_node.attrib.get('name')
        player_units[unit_name] = get_unit(unit_node)

    return player_units


def get_terrain_data():
    """
    # Function Name: get_terrain_data
    # Purpose: loads terrain data from xml file
    """
    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'terrain.xml')))
    terrain_data = []
    terrain_data_by_symbol = {}
    for terrain_node in xml_data.findall('terrain'):


        terrain_name = terrain_node.attrib.get('name')
        # Identification
        terrain_ident = int(terrain_node.find('id').text)
        terrain_icon = int(terrain_node.find('icon').text)

        terrain_symbol = terrain_node.find('symbol').text
        terrain_color = tuple(str_2_num_list(terrain_node.find('color').text))

        # Stat mods
        terrain_dmg = int(terrain_node.find('DMG').text)
        terrain_eva = int(terrain_node.find('EVA').text)

        terrain_cost = int(terrain_node.find('cost').text)

        # Whether terrain can be walked on or flown across
        terrain_walk = terrain_node.find('walk').text == 'True'
        terrain_fly = terrain_node.find('fly').text == 'True'

        layer2_flag = terrain_node.find('layer2').text == 'True'

        terrain_object = Terrain(terrain_name, terrain_ident, terrain_icon, terrain_color,
                                 terrain_symbol, terrain_dmg, terrain_eva, terrain_cost, terrain_walk, terrain_fly, layer2_flag)

        terrain_data.append(terrain_object)
        terrain_data_by_symbol[terrain_symbol] = terrain_object

    return terrain_data, terrain_data_by_symbol

def get_layer_2_data():
    """
    # Function Name: get_cliff_layer_data
    # Purpose: loads cliff layer data: for each tile whether it is passable
    # Output: cliff_layer_data - Dictionary of {(x, y):T/F} if passable
    """
    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'layer_2_tiles.xml')))
    layer_2_data = {}

    for tile_node in xml_data.findall('tile'):
        coords = tuple(str_2_num_list(tile_node.find('coords').text))

        if len(tile_node.find('terrain')):
            print tile_node.find('coords').text

        if tile_node.find('terrain').text != '0':
            terrain_override = tile_node.find('terrain').text
        else:
            terrain_override = None

        layer_2_data[coords] = terrain_override

    return layer_2_data



def get_unit_template(unit_node):

    """
    # Function Name: get_unit_template
    # Purpose: from a unit node, gets the data needed to construct a unit and returns the unit's template
    # Inputs:     unit_node = single unit node from parsed XML
    # Outputs:    unit_template = list of data unpacked to create a unit
    """

    unit_name = unit_node.attrib.get('name')


    # Locates and loads character sprite image
    unit_sprite = unit_node.find('sprite').text

    # Locates and loads portrait image
    unit_portrait = unit_node.find('portrait').text

    # Locates and loads  moves
    unit_moves = int(unit_node.find('moves').text)

    unit_stats = []
    # Load all stats
    stats_node = unit_node.find('stats')
    for stat in ['HP', 'STR', 'DEF', 'MAG', 'MDEF', 'AGL', 'ACC']:
        unit_stats.append(int(stats_node.find(stat).text))

    # Load starting level
    unit_level = int(unit_node.find('level').text)

    # Load Unit's spell preference
    unit_spell_preference = unit_node.find('spell_preference').text

    unit_type = unit_node.find('unit_type').text
    unit_class = unit_node.find('class').text
    try:
        anim_id_string = unit_node.find('animation').text
        if anim_id_string != 'False':
            unit_animation = anim_id_string
        else:
            unit_animation = False
    except IndexError:
        print unit_name+" has no animation assigned."
        unit_animation = False

    # Constructs the unit images
    unit_sprite_img = pygame.image.load(os.path.join('images', 'map_sprites', unit_sprite)).convert_alpha()
    unit_portrait_img = pygame.image.load(os.path.join('images', 'portrait', unit_portrait)).convert()

    # Loads Death Quotes to display upon unit's defeat
    unit_deathquotes = []
    [unit_deathquotes.append({'line':dq_node.find('line').text, 'portrait':dq_node.find('portrait').text}) for dq_node in unit_node.findall('death_quote')]


    template = (unit_name, unit_sprite_img, unit_portrait_img, unit_moves, unit_stats,
                unit_level, unit_spell_preference, unit_type, unit_class, unit_animation,
                unit_deathquotes)

    return template


def get_unit(unit_node):

    """
    # Function Name: get_unit
    # Purpose: from a unit node, builds a single unit
    # Inputs:     unit_node = single unit node from parsed XML
    """
    # Gets unit data
    template = get_unit_template(unit_node)

    # Doll units are decided by name
    if ((template[0]=="Shanghai") | (template[0]=="Hourai")):
        return Doll(*template)

    # Else, instantiates regular unit class
    return Unit(*template)


def get_credits_catalog():

    credits = {}


    xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'credits.xml')))

    for segment_node in xml_data.findall('segment'):
        segment_name = segment_node.attrib.get('title')
        credits_list = [line_node.text for line_node in segment_node.findall('line')]

        credits[segment_name] = credits_list

    return credits


##############################
# Item trading catalog
##############################
class TradingCatalog(object):

    def __init__(self):

        """
        # function name: __init__
        # purpose: creates trading catalog
        """

        xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'trading.xml')))
		# Ordinary trades unlocked by story progression
        self.trading_list = {}
        self.rewards = []
        self.milestones = []

        # Special trades unlocked by trading points
        for trade_node in xml_data.find('trading_list').findall('trade'):
            trade_name = trade_node.attrib.get('name')

            trade_id = trade_node.find('id_string').text
            trade_desc = trade_node.find('desc').text

            # Is the trade repeatable
            trade_repeatable = (trade_node.find('repeatable').text == 'True')

            # Trade Prereqs
            trade_prereqs = []
            [trade_prereqs.append(prereq_node.text) for prereq_node in trade_node.findall('prereq')]

            # Items traded by the player and given to the player in exchange

            items_offered = []

            # Trade costs format {'id_string':Treasure Id String, 'quantity':# of treasures costs}
            items_wanted = [{'id_string':traded_node.find('item_id').text,
                             'quantity':int(traded_node.find('quantity').text)}
                              for traded_node in trade_node.findall('item_wanted')]

            # Trade rewards format {'item_id': Treasure ID string if treasure, spell title if spell, 'item_type': 'spell_action' or 'treasure', 'quantity': # of item received from trade}
            items_offered = [{'item_id':received_node.find('item_id').text,
                              'item_type':received_node.find('item_type').text,
                              'quantity':int(received_node.find('quantity').text)}
                              for received_node in trade_node.findall('item_offered')]

            trade = Trade(trade_name, trade_id, trade_desc, trade_repeatable, trade_prereqs, items_wanted, items_offered)
            self.trading_list[trade_id] = trade

        # Loads in the rewards given for finding certain amounts of treasures
        for reward_node in xml_data.find('rewards_list').findall('reward'):

            # Reads reward data
            self.rewards.append({'desc':reward_node.find('desc').text,

                      'items_given': [{'item_id': item_node.find('item_id').text,
                                       'item_type': item_node.find('item_type').text,
                                       'quantity': int(item_node.find('quantity').text)
                                      } for item_node in reward_node.findall('item_given')]
                      })

            # Sets up a list of milestones
            self.milestones.append(int(reward_node.find('treasures').text))

# Treasure item catalog
class TreasureCatalog(dict):

    def __init__(self):

        """
        # Function name: __init__
        # Purpose: creates the treasure catalog
        """
        xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'treasure.xml')))

        for treasure_node in xml_data.findall('item'):
            treasure_name = treasure_node.attrib.get('name')
            treasure_desc = treasure_node.find('desc').text
            treasure_idstring = treasure_node.find('id_string').text
            treasure_type = treasure_node.find('type').text
            treasure_icon = treasure_node.find('icon').text

            self[treasure_idstring] = Treasure(treasure_name, treasure_idstring, treasure_desc, treasure_icon, treasure_type)

################
# Unit animation catalog class
################
class UnitAnimCatalog(dict):

    def __init__(self):

        """
        # Function name: __init__
        # Purpose: creates the unit animation catalog
        """

        for animation_file in os.listdir(os.path.join('data', 'XML', 'Animations')):
            if animation_file[-4:] == ".xml":
                xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'Animations', animation_file)))
                self.construct_anim_set(xml_data)

    def construct_anim_set(self, xml_data):

        """
        # Function name: construct_anim_set
        # Purpose: builds an animation data set
        """
        id_string = xml_data.find('id_string').text

        # Animation set dictionary
        anim_dict = {'filename': os.path.join('images', 'anim', xml_data.find('animation_filename').text)}


        # reads in all animation sequences
        for animation_sequence_node in xml_data.findall('animation_sequence'):
            anim_sequence = {}
            sequence_type = animation_sequence_node.attrib.get('type')
            anim_sequence['repeat'] = animation_sequence_node.attrib.get('repeat') == "True"
            anim_sequence['frames'] = []
            anim_sequence['coords'] = []
            # Loads all frames
            for frame_node in animation_sequence_node.findall('frame'):
                anim_sequence['frames'].append(tuple(str_2_num_list(frame_node.find('frame_coord').text)))
                anim_sequence['coords'].append(tuple(str_2_num_list(frame_node.find('coords').text)))

            anim_dict[sequence_type] = anim_sequence

        self[id_string] = anim_dict


###############
# Spell Catalog Class
#  Inherits from built in dictionary class
###############
class SpellCatalog(dict):

    def __init__(self):
        """
        # Function: __init__
        # Purpose: Constructs the catalog of the game's spells
        """

        xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'spellcatalog.xml')))
        for spell_action_node in xml_data.findall('spell_action'):
            spell_type = spell_action_node.find('type').text
            if spell_type == 'spell' or spell_type == 'spellcard':
                self[spell_action_node.attrib.get('name_suffix')] = AttackSpellTemplate(spell_action_node)
            elif spell_type == 'healing spell' or spell_type == 'healing spellcard':
                self[spell_action_node.attrib.get('name_suffix')] = HealingSpellTemplate(spell_action_node)
            elif spell_type == 'support spell' or spell_type == 'support spellcard':
                self[spell_action_node.attrib.get('name_suffix')] = SupportSpellTemplate(spell_action_node)
            elif spell_type == 'healing item':
                self[spell_action_node.attrib.get('name_suffix')] = HealingItemTemplate(spell_action_node)
            else:
                print "Unrecognized spell type"

#################################
# Spell Template Class
#################################
class SpellTemplate(object):

    def __init__(self, spell_action_node):

        """
        # Function Name: __init__
        # Purpose: Constructs a spell template
        # Inputs: spell_action_node = xml data for an individual spell
        """

        # Name

        self.name_prefix = spell_action_node.attrib.get('name_prefix')
        self.name_suffix = spell_action_node.attrib.get('name_suffix')
        self.name = self.name_prefix+" - "+self.name_suffix

        # Description
        self.desc = spell_action_node.find('desc').text

        # Number of uses
        self.uses = int(spell_action_node.find('uses').text)

        restriction_node_list = spell_action_node.findall('restriction')

        self.restrictions = {'class': ['All'],
                             'character': ['All'],
                             'level': 0}

        for restriction_node in restriction_node_list:
            restriction_type = restriction_node.attrib.get('type')
            # Class Restrictions
            if restriction_type == 'class':
                self.restrictions['class'].pop() # Pops out the "All" Term
                for unit_class in restriction_node.findall('class'):
                    self.restrictions['class'].append(unit_class.text)

            # Character Restrictions
            elif restriction_type == 'character':
                self.restrictions['character'].pop() # Pops out the "All" Term
                for unit in restriction_node.findall('character'):
                    self.restrictions['character'].append(unit.text)

            # level restrictions
            elif restriction_type == 'level':
                self.restrictions['level'] = int(restriction_node.find('level').text)


    def construct_spell(self):

        """
        # Function Name: Construct spell
        # Purpose: Template method for getting spells
        """

        pass

class AttackSpellTemplate(SpellTemplate):

    def __init__(self, spell_action_node):
        """
        # Function Name: __init__
        # Purpose: Constructs a spell template for an attack spell
        # Inputs: spell_action_node = xml data for an individual spell
        """

        # Generic Spell Vs. Spellcard
        if spell_action_node.find('type').text == "spellcard":
            self.consumable = False
        else:
            self.consumable = True

        # Attack Type / Damage Type
        self.attack_type = spell_action_node.find('attack_type').text
        self.damage_type = spell_action_node.find('damage_type').text


        # Stat Mods
        self.stat_mods = []
        stats_node = spell_action_node.find('stat_mods')
        for stat in ['STR', 'DEF', 'MAG', 'MDEF', 'AGL', 'ACC', 'CRIT']:
            self.stat_mods.append(int(stats_node.find(stat).text))

        # Effect/Shield
        self.effect = float(spell_action_node.find('effect').text)
        self.shield = float(spell_action_node.find('shield').text)

        # Spell Range (max, min)
        self.max_range = int(spell_action_node.find('max_range').text)
        self.min_range = int(spell_action_node.find('min_range').text)

        # Spell affinity and spell rank
        self.spell_affinity = spell_action_node.find('spell_affinity').text
        self.spell_rank = int(spell_action_node.find('spell_rank').text)

        # Unlock
        self.unlock = int(spell_action_node.find('spirit_unlock').text)
        self.sc_cost = int(spell_action_node.find('spirit_cost').text)

        # Counterattack
        if spell_action_node.find('counterattack').text == 'True':
            self.counterattack = True
        else:
            self.counterattack = False

        self.animation = spell_action_node.find('animation').text

        # Status Effects
        self.status_effects = {}
        if spell_action_node.findall('give_status'):
            for status_effect_node in spell_action_node.findall('give_status'):
                self.status_effects[status_effect_node.find('type').text] = float(status_effect_node.find('chance').text)

        SpellTemplate.__init__(self, spell_action_node)

    def construct_spell(self):
        """
        # Function Name: Construct spell
        # Purpose: Creates a new spell item out of the spell template
        # Outputs: spell
        """
        spell_action = AttackSpell(self.name_prefix,
                                   self.name_suffix,
                                   self.attack_type,
                                   self.damage_type,
                                   self.uses,
                                   self.stat_mods,
                                   self.effect,
                                   self.shield,
                                   self.max_range,
                                   self.spell_affinity,
                                   self.spell_rank,
                                   self.counterattack,
                                   self.unlock,
                                   self.sc_cost,
                                   self.min_range,
                                   self.consumable,
                                   self.status_effects)
        spell_action.desc = self.desc
        spell_action.animation = self.animation
        spell_action.restrictions = self.restrictions
        return spell_action


class HealingSpellTemplate(SpellTemplate):


    def __init__(self, spell_action_node):

        """
        # Function Name: __init__
        # Purpose: Constructs a spell template for a healing spell
        # Inputs: spell_action_node = xml data for an individual spell
        """
        type = spell_action_node.find('type').text
        if type == 'healing spell':
            self.consumable = True
        elif type == 'healing spellcard':
            self.consumable = False

        # Attack Type / Damage Type
        self.attack_type = 'magical'
        self.damage_type = 'magical'

        # Stat Mods
        self.stat_mods = []
        stats_node = spell_action_node.find('stat_mods')
        for stat in ['STR', 'DEF', 'MAG', 'MDEF', 'AGL', 'ACC', 'CRIT']:
            self.stat_mods.append(int(stats_node.find(stat).text))

        # Effect/Shield
        self.effect = float(spell_action_node.find('effect').text)
        self.shield = float(spell_action_node.find('shield').text)

        # Spell Range (max, min)
        self.max_range = int(spell_action_node.find('max_range').text)
        self.min_range = int(spell_action_node.find('min_range').text)

        # Spell affinity and spell rank
        self.spell_affinity = spell_action_node.find('spell_affinity').text
        self.spell_rank = int(spell_action_node.find('spell_rank').text)

        # Unlock
        self.unlock = int(spell_action_node.find('spirit_unlock').text)
        self.sc_cost = int(spell_action_node.find('spirit_cost').text)

        # Full Restore
        self.fullres = spell_action_node.find('fullres').text=='True'

        # Status Effect Cure
        self.status_effects = []
        [self.status_effects.append(cure_node.text) for cure_node in spell_action_node.findall('cure_status')]

        ###########################
        # Section to be deprecated when the new animations go online
        ###########################

        # Animations
        self.animation = spell_action_node.find('animation').text

        SpellTemplate.__init__(self, spell_action_node)

    def construct_spell(self):
        """
        # Function Name: Construct spell
        # Purpose: Creates a new spell item out of the spell template
        # Outputs: spell
        """

        spell_action = HealingSpell(self.name_prefix,
                                    self.name_suffix,
                                    self.attack_type,
                                    self.damage_type,
                                    self.uses,
                                    self.stat_mods,
                                    self.effect,
                                    self.shield,
                                    self.max_range,
                                    self.spell_affinity,
                                    self.spell_rank,
                                    self.unlock,
                                    self.sc_cost,
                                    fullres = self.fullres,
                                    minrange=self.min_range,
                                    status_effects = self.status_effects,
                                    consumable = self.consumable)
        spell_action.desc = self.desc
        spell_action.animation = self.animation
        spell_action.restrictions = self.restrictions
        return spell_action

class SupportSpellTemplate(SpellTemplate):


    def __init__(self, spell_action_node):

        """
        # Function Name: __init__
        # Purpose: Constructs a spell template for a healing spell
        # Inputs: spell_action_node = xml data for an individual spell
        """
        type = spell_action_node.find('type').text
        if type == 'support spell':
            self.consumable = True
        elif type == 'support spellcard':
            self.consumable = False

        # Attack Type / Damage Type
        self.attack_type = 'magical'
        self.damage_type = 'magical'

        # Stat Mods
        self.stat_mods = []
        stats_node = spell_action_node.find('stat_mods')
        for stat in ['STR', 'DEF', 'MAG', 'MDEF', 'AGL', 'ACC', 'CRIT']:
            self.stat_mods.append(int(stats_node.find(stat).text))

        # Effect/Shield
        self.effect = 0
        self.shield = float(spell_action_node.find('shield').text)

        # Spell Range (max, min)
        self.max_range = int(spell_action_node.find('max_range').text)
        self.min_range = int(spell_action_node.find('min_range').text)

        # Spell affinity and spell rank
        self.spell_affinity = spell_action_node.find('spell_affinity').text
        self.spell_rank = int(spell_action_node.find('spell_rank').text)

        # Unlock
        self.unlock = int(spell_action_node.find('spirit_unlock').text)
        self.sc_cost = int(spell_action_node.find('spirit_cost').text)


        # Status Effect Cure
        self.status_effects = [status_node.text for status_node in spell_action_node.findall('give_status')]

        ###########################
        # Section to be deprecated when the new animations go online
        ###########################

        # Animations
        self.animation = spell_action_node.find('animation').text

        SpellTemplate.__init__(self, spell_action_node)

    def construct_spell(self):
        """
        # Function Name: Construct spell
        # Purpose: Creates a new spell item out of the spell template
        # Outputs: spell
        """

        spell_action = SupportSpell(self.name_prefix,
                                    self.name_suffix,
                                    self.attack_type,
                                    self.damage_type,
                                    self.uses,
                                    self.stat_mods,
                                    self.effect,
                                    self.shield,
                                    self.max_range,
                                    self.spell_affinity,
                                    self.spell_rank,
                                    self.unlock,
                                    self.sc_cost,
                                    minrange=self.min_range,
                                    status_effects = self.status_effects,
                                    consumable = self.consumable)
        spell_action.desc = self.desc
        spell_action.animation = self.animation
        spell_action.restrictions = self.restrictions
        return spell_action

class HealingItemTemplate(SpellTemplate):

    def __init__(self, spell_action_node):
        """
        # Function Name: __init__
        # Purpose: Constructs a spell template for a healing item
        # Inputs: spell_action_node = xml data for an individual spell
        """

        # Effect
        self.effect = float(spell_action_node.find('effect').text)

        # Effect Type (percent/constant)
        self.effect_type = spell_action_node.find('effect_type').text
        if self.effect_type == 'constant':
            self.effect = float(self.effect)

        # Spell Range (max, min)
        self.min_range = int(spell_action_node.find('min_range').text)
        self.max_range = int(spell_action_node.find('max_range').text)

        # Spell affinity and spell rank
        self.spell_affinity = spell_action_node.find('spell_affinity').text

        # Status Effect Cure
        self.status_effects = []
        [self.status_effects.append(cure_node.text) for cure_node in spell_action_node.findall('cure_status')]

        self.bullet_img = spell_action_node.find('animation').find('bullet_img').text

        SpellTemplate.__init__(self, spell_action_node)

    def construct_spell(self):
        """
        # Function Name: Construct spell
        # Purpose: Creates a new spell item out of the spell template
        # Outputs: spell
        """

        spell_action = HealingItem(self.name_suffix,
                                   self.uses,
                                   self.effect_type,
                                   self.effect,
                                   self.max_range,
                                   self.min_range,
                                   self.spell_affinity,
                                   self.status_effects)
        spell_action.desc = self.desc
        spell_action.restrictions = self.restrictions
        return spell_action

class EnemyNPCTemplatesCatalog(object):

    def __init__(self):
        """
        # Function Name: __init__
        # Purpose: sets up enemy / npc templates catalog
        """

        self.catalog = {}
        xml_data = ElementTree.parse(open(os.path.join('data', 'XML', 'npc_enemy_units.xml')))

        for unit_node in xml_data.findall('unit'):
            template = get_unit_template(unit_node)
            # Assigns unit name as key to template dict
            self.catalog[template[0]] = template


    def construct_unit(self, unit_attributes):
        """
        # Function Name: construct_unit
        # Purpose: from a unit attribute dict, construct the unit from the template
        #            attribute format { 'template_name':Template Unit name,
        #                               'unit_name': Name unit has in the mission
        #                               'level': unit's level }
        """

        unit = Unit(*self.catalog[unit_attributes['template_name']])
        unit.name = unit_attributes['unit_name']
        unit.level = unit_attributes['level']
        unit.update_stats()
        return unit
