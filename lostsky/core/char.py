import pygame
import os
from pygame.locals import *
from linalg import Vector2
from math import floor, sin, cos, pi, ceil
from utils import set_transparency, draw_aligned_text, padlib_rounded_rect, get_ui_panel
from sys import exit
from lostsky.core.colors import selected_color, border_color, disabled_color, panel_color

class Unit(object):
    """
    # defines the basic class of characters
    """

    def __init__(self, name, image, avatar, moves, growthvector, level, spell_preference,
                 chartype, unitclass, animation, deathquote):

        """
        # Function Name: __init__
        # Purpose: Creates a character unit
        # Inputs: Name = Unit's name
        #         Image = Unit's Sprite Image
        #         Avatar = Unit's Portrait Image
        #         Moves = Unit's movement range
        #         Growthvector = A list of five numbers for the growth rates [HP, STR, DEF, MAG, MDEF, AGL, ACC]
        #         Level = Unit's Starting Level
        #         Preference = Preferred attack type
        #         Skill_rank = List of 4 numbers 0-5 representing a unit's skill in a certain magic school
        #              Input format:  [NAT, ELE, SPI, FOR]
        #         Chartype: Character type - PC, Enemy, Boss
        #         unitclass = Unit's class
        #         animation = animation ID string. None if none are available
        #         deathquotes = Sayings to display upon a unit being defeated
        """

        self.image = image                      # Unit's Sprite Image
        self.fadeout_images = self.generate_fadeout_images(image.subsurface((0, 0, 35, 35)))
        self.av = avatar                        # Unit's Portrait
        self.location_tile = Vector2(0, 0)      # Unit's Current Location in the Map Matrix
        self.location_pixel = Vector2(0, 0)     # Unit's Current Location on screen
        self.moves = moves                      # Unit's Range
        self.name = name                        # Unit's Name
        self.validmoves = {}                    # All the valid move vectors
        self.validmoves_path = {}
        self.validmoves[(0, 0)] = 1             # Sets the first entry to be a delta_r of (0, 0)
        self.spell_preference = spell_preference
        self.chartype = chartype                # Sets the character type: PC, Enemy, Boss
        self.ressurected = False                # Tracks whether a unit has ressurected in a map or not
        self.map = None                         # Unit's associated map
        self.in_battle = False                    # Unit is currently in a battle or not
        self.unitclass = unitclass              # Unit's class
        if animation:
            self.animation_enable = True        # Whether a Unit's animations are enabled
            self.anim_id_string = animation     # Key to the unit's animation set in the engine
        else:
            self.animation_enable = False
            self.anim_id_string = None

        self.spell_actions = [None, None, None, None, None]
        # Sets the default equipped spell position
        self.equipped = 0

        #Stats
        self.level = level
        self.starting_level = level
        self.growth = growthvector
        self.update_stats()
        self.HP = self.maxHP
        self.exp = 0
        self.alive = True
        self.team = 1 # Default to allies
        self.prohibited_tiles = []

        #self.spirit = 3.0                          # All units start with 3.0 levels of spirit charge
        self.spirit = 300

        self.spirit_stats = 'normal'               # High Spirits / Low Spirits Status

        #Turn Indicators. Default is that unit is dormant until activated by the map
        self.moved = True
        self.turnend = True

        #Sets up trait Slots
        # traits are stored in a list as follows: [[Action, Empty, Empty, Empty, Empty], [Support, Empty, Empty, Empty, Empty]]
        self.traits = [None, None, None, None, None]
        self.reserve_traits = [[None, None, None, None, None], [None, None, None, None, None]]
        self.trait_learning_catalog = [] #trait_learning_catalog
        self.trait_points = level*2

        # Flag for unit using the focus movement trait skill. If True, enhances accuracy and damage.
        self.focused = False

        # Status effects
        # Format - {'Status effect': # turns}
        self.status = {}
        self.draw_status = 0

        # Death Quotes
        self.deathquote = deathquote


        # Invincibility status (e.g. for Misaki)
        self.invincible = False

        self.sprite = UnitMapSprite(self)     # Unit map sprite
        self.circle = UnitCircleSprite(self)  # Unit team circle
        self.status_bubble = UnitStatusSprite(self)   # Unit Status Bubble sprite
        self.is_proxy_unit = False
        self.proxy_units = 0



    #############################
    # Computational Methods
    #############################

    def add_spell(self, spell):
        """
        # Function Name: add spell
        # Purpose: Gives a unit a spell at the first available position
        # Inputs: spell = The spell to be assigned
        # Output: assign = True if assigning was successful, 'inventoryerror' if all the slots are full

        """

        assign = False
        spell.get_attack_range(self)

        if None in self.spell_actions:
            self.spell_actions[self.spell_actions.index(None)] = spell
            assign = True

        return assign

    def add_trait(self, trait):

        """
        # Function Name: add trait
        # Purpose: Gives a unit a new trait
        # Inputs: trait = The trait to be assigned
        # Output: assign = True if assigning was successful, False if all the slots are full
        """

        assign = False

        # Assigns the trait to the first open slot
        if None in self.traits:
            self.traits[self.traits.index(None)] = trait
            assign = True

        for spell in self.spell_actions:
            if spell:
                spell.get_attack_range(self)

        if self.map and self.in_battle:
            self.get_moves_path()

        return assign

    def swap_trait(self, trait_pos):
        """
        # Function Name: swap_trait
        # Purpose: swaps a standby trait to an active trait
        # Inputs: trait_pos - position of desired standby trait
        """

        # Temporarily stores the targetted swap's contents
        branch0_trait = self.reserve_traits[0][trait_pos]
        branch1_trait = self.reserve_traits[1][trait_pos]

        # [branch#][trait_lists = 0][trait_position][trait_object = 1]
        if self.traits[trait_pos].name != branch0_trait.name:
            self.traits[trait_pos] = branch0_trait
        else:
            self.traits[trait_pos] = branch1_trait

        for spell in self.spell_actions:
            if spell:
                spell.get_attack_range(self)


    def reserve_trait(self, trait_pos):
        """
        # Function Name: reserve_trait
        # Purpose: unequips a trait and sends it to the reserve traits list
        # Inputs: trait_pos - position of desired standby trait
        """

        # Sends the trait to reserve
        self.reserve_traits[trait_pos[0]].append(self.traits[trait_pos[0]][trait_pos[1]])

        # Unequips the selected trait
        self.traits[trait_pos[0]][trait_pos[1]] = None

        # Resorts standby traits
        standby = []
        for trait in self.traits[trait_pos[0]][1:5]:
            if not trait:
                standby.append([1, None, None])
            else:
                standby.append([0, trait.name, trait])

        standby.sort()
        for i in (0, 1, 2, 3):
            self.traits[trait_pos[0]][i+1] = standby[i][2]

        for spell in self.spell_actions:
            if spell:
                spell.get_attack_range(self)

    def has_trait_property(self, trait_property):
        """
        # Function Name - has_trait_property
        # Purpose: Checks if a certain property is in either the unit's traits
        # Input:    property - property to check if equipped
        # Output:    True if the property is in one of the unit's equipped traits
        #            False if the property is not in either of the unit's equipped traits.
        """

        # Checks Action

        for trait in self.traits:
            if trait and trait_property in trait.properties:
                return True

        else:
            return False

    def get_prohibited(self):
        """
        # Function Name: get_prohibited
        # Purpose: From a unit's range, compute a list of positions the unit is allowed to pass through
        """

        if self.has_trait_property("Pass Through"):
            self.prohibited_tiles = []
        elif self.team == 1:
            self.prohibited_tiles = [tuple(unit.location_tile - self.location_tile) for unit in self.map.team2]
        elif self.team == 2:
            self.prohibited_tiles = [tuple(unit.location_tile - self.location_tile) for unit in self.map.team1]

    def calculate_max_moves(self):
        """
        calculate_max_moves
        Calculates total available movement distance
        """

        maxmoves = self.moves
        # Adds in trait effects to the movement range
        for trait in self.traits:
            if trait:
                maxmoves += trait.movemod_add

        # If unit has movement down, range is halved to a minimum of 1 movement
        if 'Movement Down' in self.status.keys():
            maxmoves /= 2
            if maxmoves <= 0:
                maxmoves = 1

        # If unit is immobilized, range is 0
        if 'Immobilize' in self.status.keys():
            maxmoves = 0

        return maxmoves

    def get_moves_path(self):

        """
        # Function Name: get moves path
        # Purpose: From a unit's range, compute a list of allowed delta-position vectors
        # Inputs: None
        # Outputs: None
        # Special Thanks to Jon Wyrick for help in the development of this algorithm
        # Modified by bbm29 to support non-unit cost tiles.
        """

        # Start position is your current location
        start = (0, 0)
        # How many moves can you make
        maxmoves = self.calculate_max_moves()

        # Check movement trait properties
        if self.has_trait_property('Flight'):
            flight = True
        else:
            flight = False

        if self.has_trait_property('Swimming'):
            swimming = True
        else:
            swimming = False

        self.validmoves = {start: (0, 0)}

        # Case for no valid moves or immobilized target
        if self.moves == 0 or 'Immobilize' in self.status.keys():

            self.validmoves_path = self.validmoves.copy()
            self.get_valid_spell_range()
            return


        wait_list = []      #The tiles on the wait list(Vector2, tuple, cost)
        wait_list_pos = []  #The tile(Vector2) which is on the wait list
        to_check = [start]
        current_moves = [start]

        # Define unit vectors
        up = Vector2(0, -1)
        down = Vector2(0, 1)
        left = Vector2(-1, 0)
        right = Vector2(1, 0)

        unit_vectors = [up, down, left, right]

        moves_left = maxmoves

        # Get the location of the prohibited tiles
        self.get_prohibited()

        # Initialization - Unless prohibited, a unit is allowed to move at least one step in each direction
        #   The very first move is treated as if the unit is flying so that you never get stuck
        #   in a tile if everything around you is too expensive to move into
        for unit_vector in unit_vectors:
            # processes each unit vector +/- x, +/- y
            new_pos = tuple(Vector2(start) + unit_vector)
            new_map_pos = tuple(new_pos + self.location_tile)
            # we only add the new position as a place of interest if
            #   1) It is not in all_moves, which means we have visited that spot in equal or fewer moves
            #   2) It is not in current_moves, which means we have visited that spot in the same move number
            #   3) It is not in the list of prohibited moves in units that you are now allowed to pass through
            #       Note: You ARE allowed to walk through allies.
            #   4) It is not a tile that you are not allowed to enter
            #   5) It is not a tile currently on the wait list
            #   6) Tile is on the map
            if (not self.validmoves.has_key(new_pos) and (new_pos not in current_moves)
                and (new_pos not in self.prohibited_tiles)
                and (new_map_pos not in self.map.map_walk_prohibited
                     or (flight == True
                         and new_map_pos not in self.map.map_fly_prohibited)
                     or (swimming == True
                         and self.map.terrainmap[new_map_pos][0].name == 'Deep Water')
                and wait_list_pos.count(new_pos) == 0)
                and self.map.terrainmap.has_key(new_map_pos)):
                self.validmoves[new_pos] = tuple(unit_vector)
                current_moves.append(new_pos)

        # Subtracts off the initial moves
        moves_left -= 1


        # Computes moves if there are more moves left to check
        while moves_left > 0:

            #Check if tiles in wait list are ready to be validated
            for tile in wait_list:
                tile[2] -= 1
                if tile[2] == 1:
                    self.validmoves[tile[0]] = tuple(tile[1])
            # Sets the current set of moves to be the ones to check in the next iteration
            to_check = current_moves
            current_moves = []

            for position in to_check:

                for unit_vector in unit_vectors:
                    # processes each unit vector +/- x, +/- y
                    new_pos = tuple(Vector2(position) + unit_vector)

                    new_map_pos = tuple(new_pos + self.location_tile)

                    # we only add the new position as a place of interest if
                    #   1) It is not in self.validmoves, which means we have visited that spot in equal or fewer moves
                    #   2) It is not in current_moves, which means we have visited that spot in the same move number
                    #   3) It is not in the list of prohibited moves in units that you are now allowed to pass through
                    #       Note: You ARE allowed to walk through allies.
                    #   4) It is not a tile that you are not allowed to enter
                    #   5) It is not a tile currently on the wait list
                    #   6) Tile is on the map
                    if (not self.validmoves.has_key(new_pos)
                        and (new_pos not in current_moves)
                        and (new_pos not in self.prohibited_tiles)
                        and self.map.terrainmap.has_key(new_map_pos)
                        and (new_map_pos not in self.map.map_walk_prohibited
                             or (flight == True
                                 and new_map_pos not in self.map.map_fly_prohibited)
                             or (swimming == True
                                 and self.map.terrainmap[new_map_pos][0].name == 'Deep Water')
                        and new_pos not in wait_list_pos)):
                        # Sets any non-1 movements to the side
                        if not flight:

                            # If unit has a swimming trait and the tile is water, treat it as a cost 1 tile
                            if (self.map.terrainmap[new_map_pos][0].cost == 1 or
                                (swimming and self.map.terrainmap[new_map_pos][0].name == 'Deep Water')):
                                self.validmoves[new_pos] = tuple(unit_vector)
                                current_moves.append(new_pos)
                            elif new_pos not in wait_list_pos:
                                wait_list.append([new_pos, tuple(unit_vector), self.map.terrainmap[new_map_pos][0].cost])
                                wait_list_pos.append(new_pos)
                        else:
                            self.validmoves[new_pos] = tuple(unit_vector)
                            current_moves.append(new_pos)

            #Add ready tiles to current_moves
            for tile in wait_list:
                if tile[2] == 1:
                    current_moves.append(tile[0])
            moves_left -= 1

        # Save a copy of valid moves before removing coordinates
        self.validmoves_path = self.validmoves.copy()
        # removes any coordinate someone else is standing on
        for other_unit in self.map.all_units_by_name.values():
            delta_pos = other_unit.location_tile - self.location_tile
            if self.validmoves.has_key(tuple(delta_pos)) and delta_pos != (0, 0): # for case of comparison with itself
                del self.validmoves[tuple(delta_pos)]

        # Updates the valid spell range display
        self.get_valid_spell_range()

    def get_valid_spell_range(self):

        """
        # Function Name: get valid spell range
        # Purpose: From a unit's spell range, compute a list of all allowed spell positions
        """

        # generates a valid attack range beyond movement range
        self.valid_spell_range = []

        # Checks if a spell is equipped
        if self.spell_actions[self.equipped]:

            # Define unit vectors
            up = Vector2(0, -1)
            down = Vector2(0, 1)
            left = Vector2(-1, 0)
            right = Vector2(1, 0)

            unit_vectors = [up, down, left, right]

            to_check = self.validmoves.keys()
            current_attacks = []
            attackrange = self.spell_actions[self.equipped].spellrange

            # Extend range effects do not affect items
            if self.spell_actions[self.equipped].type in ('healingitem', 'support', 'healing'):
                if self.has_trait_property('Extend Heal Max Range'):
                    attackrange += 1
                if self.has_trait_property('Reduce Heal Max Range'):
                    attackrange -= 1
                    if attackrange < 1:
                        attackrange = 1
            elif self.spell_actions[self.equipped].type == 'attack':

                if self.has_trait_property('Extend Atk Max Range'):
                    attackrange += 1
                if self.has_trait_property('Reduce Atk Max Range'):
                    attackrange -= 1
                    if attackrange < 1:
                        attackrange = 1

            else:
                pass

            while attackrange > 0:
                for position in to_check:
                    for unit_vector in unit_vectors:
                        # processes each unit vector +/- x, +/- y
                        new_pos = tuple(Vector2(position) + unit_vector)
                        # Conditions for adding a new position
                        # 1. New Position is not already in validmoves. We only care about the range beyond the valid
                        #   moves
                        # 2. New Position is not already in current moves. This means that position is already covered in this turn.
                        # 3. New position is not already in valid attacks. This means we already covered that position previously
                        #
                        if not self.validmoves.has_key(new_pos) and (new_pos not in current_attacks) and (new_pos not in self.valid_spell_range):
                            new_map_pos = tuple(new_pos + self.location_tile)

                            # Checks if the tile is even on the map (Important if the character is near an edge)
                            if self.map.terrainmap.has_key(new_map_pos):
                                self.valid_spell_range.append(new_pos)
                                current_attacks.append(new_pos)

                attackrange -= 1
                to_check = current_attacks

                # Clears out the current list of moves
                current_attacks = []


    def get_path(self, destination):
        """
        # Function name: Construct path
        # Purpose: generates a path from current position to any new position
        # Input: Destination - next location
        # Output: Returns a forward moving list of unit vector tuples that construct the path
        """


        #print self.validmoves_path
        path = [self.validmoves_path[destination]]
        # Gets the first step back
        next_pos = Vector2(destination) - Vector2(self.validmoves_path[destination])
        # Continues stepping until we reach the origin
        while next_pos != Vector2((0, 0)):
            path.append(self.validmoves_path[tuple(next_pos)])
            # Steps one more step back
            next_pos = Vector2(next_pos) - Vector2(self.validmoves_path[tuple(next_pos)])
        # Reverses the list to get forward moving
        path.reverse()
        return path


    def update_location(self, x, y):

        """
        # Function Name: update location
        # Purpose: Moves a unit to a location and updates both the unit's location
        #       on the tile grid as well as the pixel location
        # Inputs: x, y = location in terms of tile positions
        """

        self.location_tile = Vector2(x, y)
        self.location_pixel = self.location_tile*35


    def level_up(self):
        """
        # Function Name: level_up
        # Purpose: Levels a unit up
        """

        HP_before = self.maxHP
        self.update_stats()
        HP_gain = self.maxHP - HP_before
        self.HP += HP_gain

        self.trait_points += 2
        self.update_trait_learning_data()

    def update_stats(self):

        """
        # Function Name: update stats
        # Purpose: Using a unit's growthvector,
        # computes the stats of a unit for a certain level
        # Growth given as [HP, STR, DEF, MAG, MDEF, AGL, ACC]
        """

        # HP = 5*(HPgrow) + floor(HPgrow*.5*LV)
        self.maxHP = 5*self.growth[0]+int(floor(self.growth[0]*self.level/2))
        # STR = 2+(STRgrow)+floor((STR or MAGgrow)*LV/20)
        self.STR = 2+self.growth[1]+int(floor(self.growth[1]*self.level/20))
        # DEF = 2 +(DEFgrow) + floor((DEFgrow or MDEFgrow)*LV/25)
        self.DEF = 2+self.growth[2]+int(floor(self.growth[2]*self.level/25))
        # MAG = Int(5 * Growth Mod * Level /40);
        self.MAG = 2+self.growth[3]+int(floor(self.growth[3]*self.level/20))
        # MDEF = 2 +(DEFgrow or MDEFgrow) + floor((DEFgrow or MDEFgrow)*LV/25)
        self.MDEF = 2+self.growth[4]+int(floor(self.growth[4]*self.level/25))
        # AGL = 10 + floor(AGLgrow*LV*8/50)
        self.AGL = 10+int(floor(self.growth[5]*self.level*8/50))
        # ACC = 5+floor(ACCgrow*LV/10)
        self.ACC = 5 + int(floor(self.growth[6]*self.level/10))


    def refresh_traits(self):

        """
        # Function Name: refresh traits
        # Purpose: Called upon loading from player data. Loads the newest version of trait.
        #
        """
        for index, trait in enumerate(self.traits):
            if trait:
                self.traits[index] = self.map.engine.trait_catalog[trait.name]

        for index, trait in enumerate(self.reserve_traits[0]):
            if trait:
                self.reserve_traits[0][index] = self.map.engine.trait_catalog[trait.name]

        for index, trait in enumerate(self.reserve_traits[1]):
            if trait:
                self.reserve_traits[1][index] = self.map.engine.trait_catalog[trait.name]

    def refresh_spells(self):

        """
        # Function Name: refresh traits
        # Purpose: Called upon loading from player data. Loads the newest version of spell.
        #
        """

        for index, spell in enumerate(self.spell_actions):
            if spell:
                uses = spell.livesleft
                replacement_spell = self.map.engine.spell_catalog[spell.namesuffix].construct_spell()
                replacement_spell.get_attack_range(self)
                replacement_spell.livesleft = uses
                self.spell_actions[index] = replacement_spell


    def compute_trait_stats_bonus(self):
        """
        # Function Name: Compute trait
        # Purpose: Compute sum total of trait bonuses from support and active traits
        # Inputs: None
        # Output: trait_mods: Summed stat bonuses from both equipped traits
        """

        # Sums the trait bonuses for support and active
        trait_mods = [0, 0, 0, 0, 0, 0]
        for trait in self.traits:
            if trait and trait.variation == "Support":
                for index, modifier in enumerate(trait.statmods):

                    trait_mods[index] += modifier

            # Checks for received proximity mods if this proximity trait has them
            elif trait and trait.variation == "Proximity" and any([modifier != 0 for modifier in trait.receive_mods]):

                # Case: Receive a bonus if you are near ANY ally/enemy unit
                receive_check = False

                if not trait.receive_sources:

                    # Determines which team list to check
                    if (trait.team == "Ally" and self.team == 1) or (trait.team == "Enemy" and self.team == 2):
                        team_check = self.map.team1
                    elif (trait.team == "Enemy" and self.team == 1) or (trait.team == "Ally" and self.team == 2):
                        team_check = self.map.team2
                    else:
                        team_check = []

                    for unit in team_check:
                        # This unit does not count
                        if unit is not self and (unit.location_tile - self.location_tile).get_magnitude() <= trait.range:
                            receive_check = True

                # Case: Receive a bonus if any of a specific list of sources is nearby
                else:

                    for unit_name in trait.receive_sources:
                        # Check if unit is on the map
                        if unit_name in self.map.all_units_by_name.keys():
                            # Check if unit's distance is good
                            unit = self.map.all_units_by_name[unit_name]
                            if  (unit.location_tile - self.location_tile).get_magnitude() <= trait.range:
                                receive_check = True

                # If the conditions are fulfilled, add the bonus
                if receive_check:
                    for index, modifier in enumerate(trait.receive_mods):
                        trait_mods[index] += modifier

            # Trait Skills do not confer any bonuses
            else:
                pass

        # Checks for emitted proximity traits on other units
        for unit in self.map.all_units_by_name.values():
            # This unit does not count.
            if unit is not self:
                for trait in unit.traits:
                    # Conditions for proximity trait to be effective
                    #   Trait is variation "Proximity"
                    #   This unit is on the same team and the trait is "Ally" affecting type
                    #      OR
                    #   This unit is on the opposing team and the trait is "Enemy" affecting type
                    #   This unit's name is in the emit_target list if the list is non-empty
                    #   This unit is within the range of the proximity trait
                    if trait and trait.variation == "Proximity":

                        # Checks the right team is affected
                        if (trait.team == "Ally" and self.team == unit.team) or (trait.team == "Enemy" and self.team != unit.team):

                            # Either this affects everyone in general, or this unit needs to be on the target list
                            if not trait.emit_targets or self.name in trait.emit_targets:

                                # Checks for range
                                if (unit.location_tile-self.location_tile).get_magnitude() <= trait.range:

                                    # All conditions fulfilled, add in the trait modifiers
                                    for index, modifier in enumerate(trait.emit_mods):
                                        trait_mods[index] += modifier



        return trait_mods

    def compute_trait_hit_bonus(self):

        """
        # Function name: compute_trait_hit_bonus
        # Purpose: Sums up all the trait bonuses associated with hit and evade rates from equipped traits
            and from proximigy traits

        """
        hit_bonus = 0
        evade_bonus = 0

        for trait in self.traits:
            if trait and trait.variation == "Support":
                hit_bonus += trait.hit_bonus
                evade_bonus += trait.evade_bonus

            # Checks for received proximity mods if this proximity trait has them
            elif trait and trait.variation == "Proximity" and (trait.receive_hit_bonus != 0 or trait.receive_evade_bonus != 0):

                # Case: Receive a bonus if you are near ANY ally/enemy unit
                receive_check = False

                if not trait.receive_sources:

                    # Determines which team list to check
                    if (trait.team == "Ally" and self.team == 1) or (trait.team == "Enemy" and self.team == 2):
                        team_check = self.map.team1
                    elif (trait.team == "Enemy" and self.team == 1) or (trait.team == "Ally" and self.team == 2):
                        team_check = self.map.team2
                    else:
                        team_check = []

                    for unit in team_check:
                        # This unit does not count
                        if unit is not self and (unit.location_tile - self.location_tile).get_magnitude() <= trait.range:
                            receive_check = True

                # Case: Receive a bonus if any of a specific list of sources is nearby
                else:

                    for unit_name in trait.receive_sources:
                        # Check if unit is on the map
                        if unit_name in self.map.all_units_by_name.keys():
                            # Check if unit's distance is good
                            unit = self.map.all_units_by_name[unit_name]
                            if  (unit.location_tile - self.location_tile).get_magnitude() <= trait.range:
                                receive_check = True

                # If the conditions are fulfilled, add the bonus
                if receive_check:
                    hit_bonus += trait.receive_hit_bonus
                    evade_bonus += trait.receive_evade_bonus

            # Trait Skills do not confer any bonuses
            else:
                pass

        # Checks for emitted proximity traits on other units
        for unit in self.map.all_units_by_name.values():
            # This unit does not count.
            if unit is not self:
                for trait in unit.traits:
                    # Conditions for proximity trait to be effective
                    #   Trait is variation "Proximity"
                    #   This unit is on the same team and the trait is "Ally" affecting type
                    #      OR
                    #   This unit is on the opposing team and the trait is "Enemy" affecting type
                    #   This unit's name is in the emit_target list if the list is non-empty
                    #   This unit is within the range of the proximity trait
                    if trait and trait.variation == "Proximity":

                        # Checks the right team is affected
                        if (trait.team == "Ally" and self.team == unit.team) or (trait.team == "Enemy" and self.team != unit.team):

                            # Either this affects everyone in general, or this unit needs to be on the target list
                            if not trait.emit_targets or self.name in trait.emit_targets:

                                # Checks for range
                                if (unit.location_tile-self.location_tile).get_magnitude() <= trait.range:

                                    # All conditions fulfilled, add in the trait modifiers
                                    hit_bonus += trait.emit_hit_bonus
                                    evade_bonus += trait.emit_evade_bonus

        return hit_bonus, evade_bonus


    def compute_status_effect_bonus(self):
        """
        # Function Name: compute_status_effect_bonus
        # Purpose: Compute sum total of status effect bonuses from unit's status effects
        # Inputs: None
        # Output: se_mods - Status effect bonus total
        """

        se_mods = [0, 0, 0, 0, 0, 0]
        # Iterates over all status effects
        for se in self.status.keys():
            # Iterates over all stats changes caused by status effect
            for index, value in enumerate(self.map.engine.status_effects_catalog[se].statmods):
                se_mods[index] += value


        return se_mods

    def compute_total_stat_mods(self):
        """
        # Function Name: Compute total stat mods
        # Purpose: Compute the sum of the stat mods from the traits and status effects
        # Output: self_total_mods
        """
        self_trait_mods = self.compute_trait_stats_bonus()
        self_se_mods = self.compute_status_effect_bonus()
        self_total_mods = [sum(mod) for mod in zip(self_trait_mods, self_se_mods)]
        return self_total_mods

    def compute_hit_bonuses(self, target):
        """
        # Function Name: Compute hit bonuses
        # Purpose: Compute the total bonuses/penalties from traits and status effects to hit%
        # Output: hit_bonus - How much to add to unit's % hit
        """

        hit_bonus = 0

        ####
        # Effect from Traits
        ####

        trait_effect_self, _ = self.compute_trait_hit_bonus()
        _, trait_effect_target = target.compute_trait_hit_bonus()

        hit_bonus += trait_effect_self
        hit_bonus -= trait_effect_target

        ####
        # Effect from Status Effects
        ####
        hit_bonus += sum([self.map.engine.status_effects_catalog[se].hitmod for se in self.status.keys()])
        hit_bonus -= sum([self.map.engine.status_effects_catalog[se].evamod for se in target.status.keys()])


        # Spirits Bonus: +/- 10% to Evasion and +/- 5% to Accuracy:
        if self.spirit_stats == "high":
            hit_bonus += 10
        if target.spirit_stats == "high":
            hit_bonus -= 10
        if self.spirit_stats == "low":
            hit_bonus -= 10
        if target.spirit_stats == "low":
            hit_bonus += 10

        # Focused Movement Bonus (Grants +15% bonus to hit threshold)
        if self.focused:
            hit_bonus += 15

        # If spell type is same as this unit's spell preference, add a +5% chance to hit
        if self.spell_actions[self.equipped].affinity == self.spell_preference:
            hit_bonus += 5


        return hit_bonus

    def compute_crit_bonuses(self, target):
        """
        # Function Name: Compute crit bonuses
        # Purpose: Compute the total bonuses/penalties from traits and status effects to crit%
        # Output: hit_bonus - How much to add to unit's % crit
        """
        crit_bonus = 0

        if self.has_trait_property("Critical+ Lv.3"):
            crit_bonus += 20
        elif self.has_trait_property("Critical+ Lv.2"):
            crit_bonus += 15
        elif self.has_trait_property("Critical+ Lv.1"):
            crit_bonus += 10

        ####
        # Effect from Status Effects
        ####
        crit_bonus += sum([self.map.engine.status_effects_catalog[se].critmod for se in self.status.keys()])



        return crit_bonus


    def compute_spell_relation(self, target):
        """
        # Function Name: Compute spell relation
        # Purpose: Checks an attack type against a defense type and return advantage or disadvantage
        #          See: http://wiki.featheredmelody.com/Story_of_a_Lost_Sky/Spell_Type_Relationships
        # Inputs: User, target
        # Outputs: dmgmod = Float number to multiply damage by (Range: 0.75 -> 1.25)
        #          critmod = Number to add to the critical percent
        """

        strengths = {"Natural": "Elemental", "Elemental": "Spiritual", "Spiritual": "Force", "Force": "Natural"}
        weaknesses = {"Natural": "Force", "Elemental": "Natural", "Spiritual": "Elemental", "Force": "Spiritual"}

        # Checks to make sure target has something equipped
        if target.spell_actions[target.equipped]:

            # Against support, healing, and healing items, the relation is always neutral
            if target.spell_actions[target.equipped].type in ('healing', 'healingitem', 'support'):
                relation = 'Neutral'
                if self.spell_actions[self.equipped].affinity == self.spell_preference:
                    dmgmod = 1.10
                else:
                    dmgmod = 1.0
                critmod = 0


            # Case for the spell being strong against the target
            elif target.spell_actions[target.equipped].affinity == strengths[self.spell_actions[self.equipped].affinity]:
                relation = 'Strong'
                if self.spell_actions[self.equipped].affinity == self.spell_preference:
                    dmgmod = 1.35
                else:
                    dmgmod = 1.25

                critmod = 10

            # Case for the spell being weak against the target
            elif target.spell_actions[target.equipped].affinity == weaknesses[self.spell_actions[self.equipped].affinity]:
                relation = 'Weak'
                if self.spell_actions[self.equipped].affinity == self.spell_preference:
                    dmgmod = 0.85
                else:
                    dmgmod = 0.75
                critmod = -10

            # Case for the spell being neither weak nor strong against the target
            else:
                relation = 'Neutral'
                if self.spell_actions[self.equipped].affinity == self.spell_preference:
                    dmgmod = 1.10
                else:
                    dmgmod = 1.0
                critmod = 0

        # Case target does not have an equipped spell action
        else:
            relation = 'Strong'
            if self.spell_actions[self.equipped].affinity == self.spell_preference:
                dmgmod = 1.35
            else:
                dmgmod = 1.25
            critmod = 10

        return relation, dmgmod, critmod

    def compute_threshold(self, target):

        """
        # Function Name: Compute_base_threshold
        # Purpose: Returns hit threshold for an encounter
        # Inputs: Target
        # Output: Threshold = 100% - probability of hitting a target
        """


        if target.invincible:
            return 100

        # Trait / SE bonuses
        self_total_mods = self.compute_total_stat_mods()
        target_total_mods = target.compute_total_stat_mods()

        self_hit_bonus = self.compute_hit_bonuses(target)

        # THRESHOLD = defender's AGL*trait % Mod + defender's AGLmod + defender's terrain AGLmod - attacker's ACC - attacker's ACCmod - attacker's terrain AGLmod
        if target.spell_actions[target.equipped]:
            base_agl = target.AGL*(1.0+target_total_mods[5]) + target.spell_actions[target.equipped].aglmod

        else:
            base_agl = target.AGL*(1.0+target_total_mods[5])

        base_acc = self.ACC*(1.0+self_total_mods[4]) + self.spell_actions[self.equipped].accmod

        targetthreshold = int(base_agl - base_acc)
        targetthreshold -= self_hit_bonus
        targetthreshold += self.map.terrainmap[tuple(target.location_tile)][0].evade_mod

        # Fog Protection Penalty
        if self.map.enable_fog and not self.has_trait_property('Ignore Fog'):

            if tuple(target.location_tile) not in self.map.lit_tiles:

                # Fog veil makes targets unhittable when in fog
                if 'Fog Veil' in target.status.keys():
                    targetthreshold = 100

                # Otherwise, a hefty penalty to attack success is applied
                else:
                    targetthreshold += 33

        # Invisible targets cannot be hit.
        if "Invisible" in target.status.keys():
            targetthreshold = 100

        return targetthreshold

    def compute_hitpercent(self, target):

        """
        # Function Name: compute_hitpercent
        # Purpose: Determine the probability of hitting with an attack
        #           as well as the probability the enemy unit will counterattack
        # Inputs: enemy = the enemy unit
        # Outputs: percent1, percent2 = Probability of successful attack, counterattack respectively as strings
        #           if either unit is out of range, it will return the string "N/A"
        """

        # Computes the delta positions
        delta_pos_attack = target.location_tile - self.location_tile
        delta_pos_counter = self.location_tile - target.location_tile

        # checks if the enemy is in range
        if tuple(delta_pos_attack) in self.spell_actions[self.equipped].validattacks:


            # Gets the threshold of the target
            base_threshold_target = self.compute_threshold(target)
            # Note that the hit percent is not allowed to be greater than 100 or less than 0
            percent1 = str(max(min(100 - base_threshold_target, 100), 0))

        else:
            percent1 = 'N/A'

        # checks if you are in range of the enemy's counterattack if available
        if (target.spell_actions[target.equipped]
            and "Stun" not in target.status.keys()
            and target.spell_actions[target.equipped].counterattack == True
            and tuple(delta_pos_counter) in target.spell_actions[target.equipped].validattacks):

            # Gets the threshold of yourself
            base_threshold_self = target.compute_threshold(self)
            percent2 = str(max(min(100 - base_threshold_self, 100), 0))
        else:
            percent2 = 'N/A'

        return percent1, percent2


    def compute_crit_threshold(self, target):
        """
        # Function Name: Compute_crit_threshold
        # Purpose: Returns crit threshold for an encounter
        # Inputs: Target
        # Output: Threshold =  probability of critical against target
        """

        # Gets the relationship between the two spell types
        relationship, dmgmod, rel_critmod = self.compute_spell_relation(target)

        # Gets trait / se mods
        self_total_mods = self.compute_total_stat_mods()
        target_total_mods = target.compute_total_stat_mods()


        self_crit_bonus = self.compute_crit_bonuses(target)

        # CRIT THRESHOLD = self's ACC - average(target's DEF and MDEF) + self's SC Crit mod
        critthreshold = self.ACC*(1.0+self_total_mods[4]) - ((target.DEF*(1.0+target_total_mods[1]) + target.MDEF*(1.0+target_total_mods[3]))/2) + self.spell_actions[self.equipped].critmod

        # Adds in spell relation and equipped trait mods
        critthreshold += rel_critmod
        critthreshold += self_crit_bonus

        # Spirits Bonus: +/- 10% to Critical / Critical evasion
        if self.spirit_stats == "high":
            critthreshold += 10
        elif self.spirit_stats == "low":
            critthreshold -= 10
        if target.spirit_stats == "high":
            critthreshold -= 10
        elif target.spirit_stats == "low":
            critthreshold += 10

        # Crit threshold bounded by [0, 100]
        if critthreshold < 0:
            critthreshold = 0
        elif critthreshold > 100:
            critthreshold = 100
        else:
            critthreshold = int(critthreshold)

        return critthreshold


    def compute_critpercent(self, target):
        """
        # Function Name: compute_critpercent
        # Purpose: Determine the probability of scoring a critical hit with an attack,
        #           as well as the probability the enemy will score a critical hit
        # Inputs: enemy = the enemy unit
        # Outputs: crit1, crit2 = Probability of successful critical, counterattack critical respectively as strings
        #           if either unit is out of range, it will return the string "N/A"
        """

        # Computes the delta positions
        delta_pos_attack = target.location_tile - self.location_tile
        delta_pos_counter = self.location_tile - target.location_tile

        # checks if the enemy is in range
        if tuple(delta_pos_attack) in self.spell_actions[self.equipped].validattacks:
            crit1 = str(self.compute_crit_threshold(target))
        else:
            crit1 = 'N/A'

        # checks if you are in range of the target's counterattack if available
        if (target.spell_actions[target.equipped]
            and "Stun" not in target.status.keys()
            and target.spell_actions[target.equipped].counterattack == True
            and tuple(delta_pos_counter) in target.spell_actions[target.equipped].validattacks):
            crit2 = str(target.compute_crit_threshold(self))
        else:
            crit2 = 'N/A'

        return crit1, crit2



    def compute_damage(self, target):
        """
        # Function Name: compute_damage
        # Purpose: Computes the estimated damage of an attack
        # Inputs: target = the caster and the target
        # Outputs: damage = Estimated damage done by the spell
        """

        # Gets the relationship between the two spell types
        relationship, dmgmod, rel_critmod = self.compute_spell_relation(target)

        # Gets trait/se bonuses
        self_total_mods = self.compute_total_stat_mods()
        target_total_mods = target.compute_total_stat_mods()

        # Effect calculation for physical attack type spells
        # Damage = (Attacker's STR + Attacker's STRmod)*Attacker's Base Effect
        if self.spell_actions[self.equipped].attacktype == 'physical':
            effect = (self.STR*(1.0+self_total_mods[0]) + self.spell_actions[self.equipped].strmod)*self.spell_actions[self.equipped].effect

        # Effect calculation for magical attack type spells
        # Effect = (Attacker's MAG + Attacker's MAGmod)*Attacker's Base Effect
        elif self.spell_actions[self.equipped].attacktype == 'magical':
            effect = (self.MAG*(1.0+self_total_mods[2]) + self.spell_actions[self.equipped].magmod)*self.spell_actions[self.equipped].effect

        # If the defender has no equipped spell or is holding an item, the default shield effect is 1
        if target.spell_actions[target.equipped]:

            # Shield calculation for physical damage type spells
            # Shield = (Defender's DEF + Defender's DEFmod) * Defender's Base Shield
            if self.spell_actions[self.equipped].damagetype == 'physical':
                shield = (target.DEF*(1.0+target_total_mods[1]) + target.spell_actions[target.equipped].defmod)*target.spell_actions[target.equipped].shield

            # Shield calculation for magical damage type spells
            # Shield = (Defender's MDEF + Defender's MDEFmod) * Defender's Base Shield
            elif self.spell_actions[self.equipped].damagetype == 'magical':
                shield = (target.MDEF*(1.0+target_total_mods[3]) + target.spell_actions[target.equipped].mdefmod)*target.spell_actions[target.equipped].shield
        else:
            # Shield calculation for physical damage type spells
            # Shield = (Defender's DEF)
            if self.spell_actions[self.equipped].damagetype == 'physical':
                shield = (target.DEF*(1.0+target_total_mods[1]))

            # Shield calculation for magical damage type spells
            # Shield = (Defender's MDEF)
            elif self.spell_actions[self.equipped].damagetype == 'magical':
                shield = (target.MDEF*(1.0+target_total_mods[3]))

        # Final damage = Effect - Shield
        damage = effect - shield

        # Multiplies damage with the relationship effect
        damage *= dmgmod

        # Multiply damage by terrain defense modifier
        damage *= (1+self.map.terrainmap[tuple(target.location_tile)][0].damage_mod / 100.0)

        if self.spirit_stats == "high":
            damage = damage*1.1
        elif self.spirit_stats == "low":
            damage = damage*0.9
        else:
            damage = damage

        # Damage Modifying Status Effects
        DEFENSE_STATUS_UP_MOD = 0.9
        DEFENSE_STATUS_DOWN_MOD = 1.1
        MAGIC_FORTRESS_MOD = 0.75
        if "MDEF Up" in target.status.keys() and self.spell_actions[self.equipped].damagetype == 'magical':
            damage = damage*DEFENSE_STATUS_UP_MOD
        if "DEF Up" in target.status.keys() and self.spell_actions[self.equipped].damagetype == 'physical':
            damage = damage*DEFENSE_STATUS_UP_MOD
        if "MDEF Down" in target.status.keys() and self.spell_actions[self.equipped].damagetype == 'magical':
            damage = damage*DEFENSE_STATUS_DOWN_MOD
        if "DEF Down" in target.status.keys() and self.spell_actions[self.equipped].damagetype == 'physical':
            damage = damage*DEFENSE_STATUS_DOWN_MOD
        if "Magic Fortress" in target.status.keys():
            damage = damage*MAGIC_FORTRESS_MOD



        # Focused movement (20% increase in damage)
        FOCUSED_MOD = 1.2
        if self.focused:
            damage *= FOCUSED_MOD

        # Spirit Booster and Magic Saver effects
        # Spirit Saver causes spell actions using SC to be less effective
        # Spirit Booster causes spell actions using SC to be more effective
        SAVER_MOD = 0.8
        BOOSTER_MOD = 1.2
        if self.spell_actions[self.equipped].sc_cost > 0:
            if self.has_trait_property('Spirit Booster'):
                damage *= BOOSTER_MOD
            elif self.has_trait_property('Spirit Saver'):
                damage *= SAVER_MOD
            else:
                pass
        else:
            pass

        # Traits can confer resistances to certain affinity spell actions
        # If a unit has trait with property "Resist X" they take reduced damage
        RESIST_MOD = 0.85
        if target.has_trait_property("Resist %s"%self.spell_actions[self.equipped].affinity):
            damage *= RESIST_MOD

        # Level Bonus
        # If a unit has the trait "High Level Bonus", damage is increased against lower level enemies.
        HIGH_LEVEL_BONUS = 1.1
        if self.has_trait_property("High Level Bonus") and self.level > target.level:
            damage *= HIGH_LEVEL_BONUS

        # Cast to integer
        damage = int(damage)

        return damage



    def predict_damage(self, target):
        """
        # Function Name: predict_damage
        # Purpose: Determines an estimate of the amount of damage the attacker will do as well as counterattack damage
        # Inputs: enemy = the enemy unit
        # Outputs: damage1, damage2 = Damage (without critical factor), and counterattack damage respectively as strings
        #           if either unit is out of range, it will return the string "N/A"
        """

        # Computes the delta positions
        delta_pos_attack = target.location_tile - self.location_tile
        delta_pos_counter = self.location_tile - target.location_tile

        if self.spell_actions[self.equipped].type == 'attack':
            # checks if the enemy is in range
            if tuple(delta_pos_attack) in self.spell_actions[self.equipped].validattacks:
                damage1 = self.compute_damage(target)
                if damage1 < 1:
                    damage1 = 1

                damage1 = str(damage1)

            else:
                damage1 = 'N/A'

            # checks if you are in range of the enemy's counterattack
            if  (target.spell_actions[target.equipped] and "Stun" not in target.status.keys() and target.spell_actions[target.equipped].counterattack == True
                 and tuple(delta_pos_counter) in target.spell_actions[target.equipped].validattacks):
                damage2 = target.compute_damage(self)
                if damage2 < 0:
                    damage2 = 1
                damage2 = str(damage2)
            else:
                damage2 = 'N/A'


        elif self.spell_actions[self.equipped].type in ('healing', 'healingitem', 'support'):
            damage2 = 'N/A'
            damage1 = str(self.spell_actions[self.equipped].get_effect(self, target))

        return damage1, damage2




    def experience(self, enemy, damage):
        """
        # Function Name: experience
        # Purpose: Determines an estimate of the amount of damage the attacker will do as well as counterattack damage
        # Inputs: enemy = the enemy unit
        #         damage = damage done
        # Formulas:
        #    LDIF = Attacker's Level - Defender's Level
        #
        #    * Base EXP = 25 * 0.75 ^ LDIF
        #
        # NOTE: These values are rounded off to the nearest integer
        #    * Successful Story Boss Kill: 5 x Base EXP
        #    * Successful Boss Kill: 2 x Base EXP
        #    * Successful Kill: 1 x Base EXP
        #    * Successful Attack: 0.40 x Base EXP
        #    * Failed Attack: 0.10 x Base EXP
        """

        # Compute the base EXP
        LDIF = self.level - enemy.level
        # Check to see if the target is alive first
        if self.alive == True:
            base_exp = 25. * 0.75 ** LDIF
        else:
            base_exp = 0

        if damage == 'miss':
            exp = int(0.10 * base_exp)
        else:
            # Checks if the enemy is still alive after the turn action.
            if enemy.alive == True:
                exp = int(0.40 * base_exp)
            else:
                if enemy.chartype == 'enemy':
                    exp = int(base_exp)
                elif enemy.chartype == 'boss' or enemy.chartype == 'pc' or enemy.chartype == 'npc':
                    exp = int(2 * base_exp)
                elif enemy.chartype == 'storyboss':
                    exp = int(5 * base_exp)

        # Trait EXP bonus
        exp = int(exp*(1+sum([trait.expmod for trait in self.traits if trait])))

        # EXP Cap of 200 EXP
        if exp > 200:
            exp = 200

        self.exp += exp

        print self.name + " got EXP: " + str(exp)

        level_up = self.level_up_check()

        return exp, level_up


    def level_up_check(self):
        """
        function name: level_up_check
        Purpose: checks if this unit leveled up, and adjust EXP according

        Output: level_up - number of levels a unit gained

        """

        level_up = 0
        # Checks if there has been a successful level up:

        while self.exp >= 100:
            # Carries over extra EXP to the next level.
            self.exp = max(self.exp-100, 0)
            # Increase level by 1
            self.level += 1
            # Update stats
            print self.name + " level up."
            self.level_up()
            level_up += 1

        return level_up


    def battle_spirit(self, target, effect, critical):
        """
        # Function Name: battle_spirit
        # Purpose: determines the spirit effect of the last action
        # Inputs: target = the target unit
        #         damage = damage done
        #         critical = critical hit
        # FORMULAS
        #        * Successful Attack: SC + 15
        #        * Successful Defeated Enemy: SC + 100
        #        * Successful Critical: SC + 40
        #        * Failed Attack (Miss): SC - 10
        #        * Enemy Critical: SC - 40
        #        * Resurrect (Kaguya, Mokou, etc): SC resets to 0
        """

        self_spirit_before = self.spirit
        enemy_spirit_before = target.spirit

        # Checks if the player is alive
        spirit_self = 0
        spirit_enemy = 0
        if self.alive == True:
            if effect == 'miss':
                spirit_self -= 10
            else:
                spirit_self += 15

                # Both sides are on the same team, healing spell used
                if self.team == target.team:
                    healing_effect = 150
                    spirit_self += int(effect*healing_effect/target.maxHP)

                # Enemy Defeated
                if target.alive == False:
                    spirit_self += 100

        # Critical Hit
        if critical == True:
            spirit_self += 40
            spirit_enemy -= 40

        # Spirit Charge Modifying Traits
        spirit_self = int(spirit_self*(1+sum([trait.spiritmod for trait in self.traits if trait])))
        spirit_enemy = int(spirit_enemy*(1+sum([trait.spiritmod for trait in target.traits if trait])))

        self.spirit += spirit_self
        target.spirit += spirit_enemy

        self.check_spirit_range()
        target.check_spirit_range()

        # Accounts for maxed out spirit charge
        self_spirit_delta = self.spirit - self_spirit_before
        enemy_spirit_delta = target.spirit - enemy_spirit_before

        return self_spirit_delta, enemy_spirit_delta

    def sc_regen(self, message, sc_regen_value, sc_max):


        text_status_effect = self.map.engine.bfont.render(message, True, (0, 0, 0))
        sc_before = self.spirit
        self.spirit += sc_regen_value
        if self.spirit > sc_max:
            self.spirit = sc_max

        self.check_spirit_range()

        delta_sc = self.spirit - sc_before

        text_effect = self.map.engine.render_outlined_text(str(delta_sc), self.map.engine.cfont, (128, 255, 255), (0, 0, 0))

        # Renders SC change
        self.map.center_on(self)
        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
        self.map.engine.surface.blit(text_status_effect, (420-text_status_effect.get_width()/2, 25))
        self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
        self.plot_stats()
        self.map.engine.surface.blit(text_effect, ((self.location_pixel.x+18-text_effect.get_width()/2, self.location_pixel.y-25)-self.map.screen_shift*self.map.engine.tilesize))
        self.map.engine.pause(1)

        self.render_sc_change(sc_before, self.spirit)

    def check_spirit_range(self):

        """
        # Function Name: check_spirit_range
        # Purpose: checks to make sure the spirit charge values are in the appropriate range
        #    and checks if the spirit status conditions need to be updated
        """

        # Checks to ensure the spirit numbers remain within the range (0.00 -> 9.00
        if self.spirit > 900:
            self.spirit = 900
        if self.spirit < 0:
            self.spirit = 0

        # Checks spirit status conditions
        if self.spirit > 750:
            self.spirit_stats = 'high'
            if 'Low Spirit' in self.status.keys():
                self.remove_status('Low Spirit')
            if 'High Spirit' not in self.status.keys():
                self.give_status('High Spirit')

        elif self.spirit <= 750 and self.spirit >= 200:
            self.spirit_stats = 'normal'
            if 'High Spirit' in self.status.keys():
                self.remove_status('High Spirit')
            if 'Low Spirit' in self.status.keys():
                self.remove_status('Low Spirit')
        elif self.spirit < 200:
            self.spirit_stats = 'low'
            if 'High Spirit' in self.status.keys():
                self.remove_status('High Spirit')
            if 'Low Spirit' not in self.status.keys():
                self.give_status('Low Spirit')
        else:
            print "Spirit Range out of bounds"

    def check_spell_type_availability(self, type):
        """
        Function name: check_spell_type_availability
        Purpose; Checks if a unit has a certain type of spell. e.g. valid inputs would be "support" or "attack"
        Input:  type - spell action type
        Output: (T/F, index of spell)

        """


        for index, spell in enumerate(self.spell_actions):
            if spell and spell.type == type:
                return True, index
        return False, None

    def give_status(self, status_effect):
        """
        # Function: give_status
        # Purpose: Give unit a status effect
        # Inputs: status_effect = status effect to assign to unit
        """
        self.status[status_effect] = 0
        self.status_bubble.update_queue()

    def remove_status(self, status_effect):
        """
        # Function: remove_status
        # Purpose: Remove a status effect from unit
        # Inputs: status_effect = status effect to remove from unit
        """
        del self.status[status_effect]
        self.status_bubble.update_queue()

    def clear_status(self):
        """
        # Function: clear_status
        # Purpose: Remove all status effects from unit
        """
        self.status = {}
        self.status_bubble.update_queue()

    def reset_state(self):
        """
        # Function Name: reset_state
        # Purpose: clears out all spell actions, traits, exp, tp stuff
        """
        self.spell_actions = [None, None, None, None, None]
        self.traits = [None, None, None, None, None]
        self.reserve_traits = [[None, None, None, None, None], [None, None, None, None, None]]
        self.exp = 0
        self.level = self.starting_level
        self.update_stats()
        self.update_trait_learning_data()
        self.trait_points = self.starting_level*2
        self.proxy_units = 0;

    #############################
    # Graphical Methods
    #############################

    def generate_fadeout_images(self, surface):
        """
        fucntion name: generate_fadeout_images
        Generates a 15 frame duration sequence of increasing transparency versions of the main image
        """

        smoothstep = lambda v: (v*v*(3-2*v))

        start_pos = 255
        end_position = 1

        transparency_list = []

        frame_count = 6
        for t in xrange(0, frame_count+1):
            v = float(t)/float(frame_count)
            v = smoothstep(v*end_position)
            intermediate_step = int(v*255)

            current_pos = start_pos - intermediate_step
            transparency_list.append(current_pos)

        frame_list = [set_transparency(surface, alpha) for alpha in transparency_list]
        return frame_list


    def plot_valid_moves(self):

        """
        # Function Name: plot_valid_moves
        # Purpose: Plots the valid movement positions on the screen.
        """

        for tile in self.validmoves.keys():
            self.map.engine.surface.blit(self.map.engine.move_tile, (Vector2(tile)*35+self.location_pixel-self.map.screen_shift*self.map.engine.tilesize))

    def plot_moves_and_attacks(self):
        """
        # Function Name: plot_moves_and_attacks
        # Purpose: Plots the valid movement positions on the screen, as well as the possible valid attack locations.
        """

        self.plot_valid_moves()
        for tile in self.valid_spell_range:
            if self.spell_actions[self.equipped].type == 'attack':
                self.map.engine.surface.blit(self.map.engine.attack_tile, (Vector2(tile)*35+self.location_pixel-self.map.screen_shift*self.map.engine.tilesize))
            elif self.spell_actions[self.equipped].type in ('healing', 'healingitem', 'support'):
                self.map.engine.surface.blit(self.map.engine.heal_tile, (Vector2(tile)*35+self.location_pixel-self.map.screen_shift*self.map.engine.tilesize))

    def plot_attacks(self, delta=Vector2(0, 0)):

        """
        # Function Name: plot_attacks
        # Purpose: Plots the valid attack range for the equipped spell
        # Inputs: Delta: Vector corresponding to a shift in position, occurs if the plotting is to be done during the move confirmation screen.
        """

        for tile in self.spell_actions[self.equipped].validattacks:
            if self.spell_actions[self.equipped].type == 'attack':
                self.map.engine.surface.blit(self.map.engine.attack_tile, (Vector2(tile)*35+self.location_pixel+delta*35-self.map.screen_shift*self.map.engine.tilesize))
            elif self.spell_actions[self.equipped].type in ('healing', 'healingitem', 'support'):
                self.map.engine.surface.blit(self.map.engine.heal_tile, (Vector2(tile)*35+self.location_pixel+delta*35-self.map.screen_shift*self.map.engine.tilesize))


    def render(self):
        """
        # Function Name: render
        # Purpose: Plots the unit's sprite as well as a status condition bubble if applicable
        """

        x, y = self.location_pixel
        self.render_team_circle()


        # Draws the normal sprite if the turn is not over.
        if self.turnend == False or self.map.currentplayer != self.team :
            self.map.engine.surface.blit(self.image, ((x, y)-self.map.screen_shift*self.map.engine.tilesize), (0, 0, 35, 35))
        else:
            self.map.engine.surface.blit(self.image, ((x, y)-self.map.screen_shift*self.map.engine.tilesize), (105, 0, 35, 35))
        # Plots an icon if the unit has a status effect
        if self.status.keys():
            # Displays a different bubble every 2 seconds (lifetime of animation counter).
            if self.map.animation_counter in (1, 61):
                self.draw_status += 1
            # Checks if the tracking counter for status bubbles is bigger than number of status effects
            # Two cases:
            #       1. Unit is either in high / low spirits - We cap the drawing counter at #status effects and draw status effects at [1, ...]
            #       2. Unit is not in high/low spirits - We cap the drawing counter at #status effects and draw status effects at [0, ...]
            if (self.spirit_stats not in ('low', 'high') and self.draw_status > len(self.status.keys())-1) or (self.spirit_stats in ('low', 'high') and self.draw_status > len(self.status.keys())):
                self.draw_status = 0

            if self.spirit_stats in ('low', 'high'):
                # Draws Spirit Charge status
                if self.draw_status == 0:
                    if self.spirit_stats == "low":
                        self.map.engine.surface.blit(self.map.engine.status_spirit, (x+17, y)-self.map.screen_shift*self.map.engine.tilesize, (0, 0, 18, 18))
                    elif self.spirit_stats == "high":
                        self.map.engine.surface.blit(self.map.engine.status_spirit, (x+17, y)-self.map.screen_shift*self.map.engine.tilesize, (18, 0, 18, 18))
                # Draws status effects
                else:
                    self.map.engine.surface.blit(self.map.engine.status_effect_icons, (x+17, y)-self.map.screen_shift*self.map.engine.tilesize,
                        (self.map.engine.status_effects_catalog[self.status.keys()[self.draw_status-1]].icon_location*18, 0, 18, 18))
            else:
                # Draws status effects only
                self.map.engine.surface.blit(self.map.engine.status_effect_icons, (x+17, y)-self.map.screen_shift*self.map.engine.tilesize,
                    (self.map.engine.status_effects_catalog[self.status.keys()[self.draw_status]].icon_location*18, 0, 18, 18))

        else:
            if self.spirit_stats == "low":
                self.map.engine.surface.blit(self.map.engine.status_spirit, (x+17, y)-self.map.screen_shift*self.map.engine.tilesize, (0, 0, 18, 18))
            elif self.spirit_stats == "high":
                self.map.engine.surface.blit(self.map.engine.status_spirit, (x+17, y)-self.map.screen_shift*self.map.engine.tilesize, (18, 0, 18, 18))

    def render_proximity_range(self, trait):

        """
        # Function Name: render_proximity_range
        # Purpose: Plots the range of the proximity trait

        # input: trait - proximity trait to draw range for.
        """

        # show maximum range of proximity trait
        show_range = trait.range

        coords = []

        for diagonal_row_num in xrange(1, show_range + 1):
            for index in xrange(0, diagonal_row_num + 1):
                coords.append((diagonal_row_num-index, index))

        # generates the valid moveset for 2nd, 3rd, 4th quadrants
        for coord in list(coords):

            coords.append((-coord[0], coord[1]))
            coords.append((-coord[0], -coord[1]))
            coords.append((coord[0], -coord[1]))

        for coord in coords:
            base_vector = self.location_pixel-self.map.screen_shift*35+35*Vector2(coord)

            # Ensures drawing of proximity region remains on screen.
            if base_vector.y < 490:
                position1 = list(base_vector)+[35, 35]
                position2 = list(base_vector+Vector2(1, 1))+[33, 33]
                position3 = list(base_vector+Vector2(2, 2))+[31, 31]
                pygame.draw.rect(self.map.engine.surface, (50, 100, 200), position1, 1)
                pygame.draw.rect(self.map.engine.surface, (255, 255, 255), position2, 1)
                pygame.draw.rect(self.map.engine.surface, (50, 100, 200), position3, 1)




    def render_emote(self, emotion):
        """
        # Function name: render_emote
        # Purpose: Draws an emotion bubble
        # Input: Emotion- name of emotion type
        """
        emotion_image = self.map.engine.emotion_bubbles[emotion]['image']
        frame_width = self.map.engine.emotion_bubbles[emotion]['frame_width']
        frame_height = self.map.engine.emotion_bubbles[emotion]['frame_height']
        max_frames_x = emotion_image.get_width()/frame_width
        max_frames_y = emotion_image.get_height()/frame_height
        delay = self.map.engine.emotion_bubbles[emotion]['delay']

        for frame_num_y in xrange(0, max_frames_y):
            for frame_num_x in xrange(0, max_frames_x):

                self.map.render_background()
                self.map.render_all_units(bubbles = False)
                self.map.render_cursor()
                self.map.render_menu_panel()
                if self.map.enable_stats_panel:
                    self.plot_stats()


                # Draws emoticon frame
                self.map.engine.surface.blit(emotion_image, self.location_pixel+Vector2(15, -(frame_width-10))-35*self.map.screen_shift, (frame_width*frame_num_x, frame_height*frame_num_y, frame_width, frame_height))
                pygame.display.flip()
                self.map.engine.clock.tick(60)
                # Delay between frames
                if delay > 0:
                    self.map.engine.pause(delay)


    def render_team_circle(self):
        """
        # Function name: render_team_circle
        # Purpose: Draws the character's underneath circle
        """

        if self.chartype == 'boss':
            self.map.engine.surface.blit(self.map.engine.team_panels, ((self.location_pixel.x, self.location_pixel.y)-self.map.screen_shift*self.map.engine.tilesize), (70, 0, 35, 35))
        elif self.chartype == 'npc':
            self.map.engine.surface.blit(self.map.engine.team_panels, ((self.location_pixel.x, self.location_pixel.y)-self.map.screen_shift*self.map.engine.tilesize), (105, 0, 35, 35))
        elif self.team == 1:
            self.map.engine.surface.blit(self.map.engine.team_panels, ((self.location_pixel.x, self.location_pixel.y)-self.map.screen_shift*self.map.engine.tilesize), (0, 0, 35, 35))
        elif self.team == 2:
            self.map.engine.surface.blit(self.map.engine.team_panels, ((self.location_pixel.x, self.location_pixel.y)-self.map.screen_shift*self.map.engine.tilesize), (35, 0, 35, 35))

    def render_startle(self):
        """
        # Function name: render_startle
        # Purpose: Has a character jump up twice in a startled position
        """

        # Background render
        self.map.render_background()
        self.map.render_menu_panel()
        if self.map.enable_stats_panel:
            self.plot_stats()
        background_surface = self.map.engine.surface.copy()

        # First frame - Update entire screen
        self.map.sg_units.clear(self.map.engine.surface, background_surface)
        rects = self.map.render_all_units()
        self.map.render_cursor()
        pygame.display.flip()
        self.map.engine.clock.tick(60)

        starting_height = self.location_pixel.y
        # Freeze team color circle in place
        self.circle.hold = True

        # We want to have this unit drawn last so it is in the proper order when
        # the unit jumps to the next tile up.
        # Removes unit from map group and creates a separate group for it
        startle_group = pygame.sprite.RenderUpdates()

        self.map.sg_units.remove(self.sprite)
        startle_group.add(self.sprite)

        def y(a , v, t):
            """
            # function name: y
            # purpose:
            #     Simulates constant force towards bottom of screen for.
            #     (Positive = Down)
            #     Standard kinematics equation: y(t) = y0 + v*t + a*t^2
            #     Assume y0 = 0
            # Input: a - acceleration (pixel/frame^2)
            #        v - initial speed (pixel/frame)
            #        t - time (frame)
            """
            return int(a*t**2 + v*t)

        # Parameters for jumping
        v = -4.0
        # Number of frames in animation
        frames = 10
        # Require jump to reach max height midway through animation
        # e.g. velocity = 0 at max height
        # v(t) = v0 + a * t
        a = -v/frames/2

        for i in xrange(0, 2):
            for t in xrange(0, 2*frames-1):
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                        exit()

                self.location_pixel.y = starting_height+y(a, v, t)

                self.map.sg_units.clear(self.map.engine.surface, background_surface)
                startle_group.clear(self.map.engine.surface, background_surface)
                self.map.sg_unitcircles.clear(self.map.engine.surface, background_surface)


                # Draws all updated unit positions
                rects = self.map.render_all_units(bubbles = False)

                # Draw this unit last
                startle_group.update()
                rects += startle_group.draw(self.map.engine.surface)
                self.map.render_cursor()
                pygame.display.update(rects)
                self.map.engine.clock.tick(60)

        # Adds unit back to map group
        self.map.sg_units.add(self.sprite)

        # Reset current position
        self.circle.hold = False
        self.location_pixel.y = starting_height

        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.render_menu_panel()
        if self.map.enable_stats_panel:
            self.plot_stats()
        pygame.display.flip()
        self.map.engine.clock.tick(60)


    def render_walk(self, path):
        """
        # Function name: render_walk
        # Purpose: Plots the unit's sprite moving from A to B
        # Inputs:   Unit = Unit to make walk
        #           Path = A list of tuples containing the forward moving path (retrieved from self.get_path() )
        """

        new_path = [Vector2(path[0])]
        # converts the input path to a list of vectors
        for step in path[1:]:
            if Vector2(step) == Vector2(new_path[-1]).normalize():
                new_path[-1] += Vector2(step)
            else:
                new_path.append(step)


        # Smoothstep function
        # See: http://sol.gfxile.net/interpolation/
        smoothstep = lambda v: (v*v*(3-2*v))

        start_pos = self.location_pixel
        current_pos = start_pos.copy()

        # Background render
        self.map.render_background()
        self.map.render_cursor()
        self.map.render_menu_panel()
        if self.map.enable_stats_panel:
            self.plot_stats()
        background_surface = self.map.engine.surface.copy()

        # First frame - Update entire screen
        self.map.sg_units.clear(self.map.engine.surface, background_surface)
        rects = self.map.render_all_units()
        pygame.display.flip()
        self.map.engine.clock.tick(60)

        # Remove unit from map's main sprite groups
        self.map.sg_units.remove(self.sprite)
        self.map.sg_status.remove(self.status_bubble)

        # Add unit to map's moving unit sprite group
        self.map.sg_moving_unit.add((self.sprite, self.status_bubble))

        while new_path:
            next_step = Vector2(new_path.pop(0))
            # Sets frame count proportional to the square root of the magnitude of the step vector
            frame_count = int(10*next_step.get_magnitude()**(0.5))

            for t in xrange(0, int(frame_count)+1):

                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                        exit()

                v = float(t)/float(frame_count)
                v = smoothstep(v)
                scale_term = int(35*v)
                intermediate_step = scale_term*next_step
                current_pos = start_pos + intermediate_step

                # Gets updated current position
                self.location_pixel = Vector2(current_pos.x, current_pos.y)

                # Clears the background
                self.map.sg_unitcircles.clear(self.map.engine.surface, background_surface)
                self.map.sg_units.clear(self.map.engine.surface, background_surface)
                self.map.sg_status.clear(self.map.engine.surface, background_surface)
                self.map.sg_moving_unit.clear(self.map.engine.surface, background_surface)
                self.map.sg_moving_unit.update()

                # Draws all updated unit positions
                rects = self.map.render_all_units()

                # Draw this unit last so it will always be on top
                rects += self.map.sg_moving_unit.draw(self.map.engine.surface)

                pygame.display.update(rects)
                self.map.engine.clock.tick(60)

            start_pos = current_pos.copy()


        # Remove unit to map's moving unit sprite group
        self.map.sg_moving_unit.remove((self.sprite, self.circle, self.status_bubble))

        # Add unit back into map's main sprite groups
        self.map.sg_units.add(self.sprite)
        self.map.sg_status.add(self.status_bubble)


    def render_semitrans(self, delta):

        """
        # Function Name: render semitrans
        # Purpose: Renders a semitransparent copy of oneself at a position delta from the current location
        # Inputs: Delta (Vector2) relative to current position.
        """

        x, y = self.location_pixel
        x1, y1 = x+delta.x*self.map.engine.tilesize, y+delta.y*self.map.engine.tilesize

        # Draws a transparent copy of the sprite
        self.map.engine.surface.blit(self.image, ((x1, y1)-self.map.screen_shift*self.map.engine.tilesize), (140, 0, 35, 35))

    def render_fadeout(self):

        """
        # Function name: render_fadeout
        # Purse: draws the unit fading out from the screen
        """

        self.map.render_background()
        self.map.render_menu_panel()
        if self.map.enable_stats_panel:
            self.plot_stats()
        background_surface = self.map.engine.surface.copy()



        # We want to have this unit drawn last so it is in the proper order when
        # the unit jumps to the next tile up.
        # Removes unit from map group and creates a separate group for it
        fade_group = pygame.sprite.RenderUpdates()

        self.map.sg_units.remove(self.sprite)
        fade_group.add(self.sprite)

        # First frame - Update entire screen
        self.map.sg_units.clear(self.map.engine.surface, background_surface)
        self.map.sg_status.clear(self.map.engine.surface, background_surface)
        rects = self.map.render_all_units()
        self.map.render_cursor()
        pygame.display.flip()
        self.map.engine.clock.tick(60)


        for frame in self.fadeout_images:

            self.sprite.image = frame


            self.map.sg_units.clear(self.map.engine.surface, background_surface)
            self.map.sg_status.clear(self.map.engine.surface, background_surface)
            fade_group.clear(self.map.engine.surface, background_surface)

            # Draws all updated unit positions
            rects = self.map.render_all_units()
            rects += fade_group.draw(self.map.engine.surface)

            # Draw this unit last
            pygame.display.update(rects)

            for _ in xrange(0, 5):
                self.map.engine.clock.tick(60)

        if self.turnend:
            self.sprite.image = self.sprite.wait_image
        else:
            self.sprite.image = self.sprite.active_image

        self.map.sg_units.add(self.sprite)

    def render_hp_change(self, hp_before, hp_after):
        """
        # Function Name: render_hp_change
        # Purpose: Draws an HP meter and shows a change in HP
        # Inputs: hp_before, hp_after - the HP values before and after a change occurs
        """
        # Smoothstep function
        # See: http://sol.gfxile.net/interpolation/
        smoothstep = lambda v: (v*v*(3-2*v))
        meter_before = int(float(hp_before)*32/float(self.maxHP))
        meter_after = int(float(hp_after)*32/float(self.maxHP))
        delta_meter = meter_after - meter_before

        x, y = self.location_pixel

        frame_count = 30
        for t in xrange(0, frame_count):
            v = float(t)/float(frame_count)
            v = smoothstep(v)
            scale_term = int(delta_meter*v)

            current_percent = meter_before + scale_term

            # After the first action
            self.map.render_background()
            self.map.render_all_units()
            self.map.engine.surface.blit(self.map.engine.battle_board, (0, 490))

            # Draws background of health meter
            self.map.engine.surface.blit(self.map.engine.health_meter, ((x, y)-self.map.screen_shift*self.map.engine.tilesize), (35, 0, 35, 35))
            # Draws HP bar
            self.map.engine.surface.blit(self.map.engine.health_meter, ((x, y)-self.map.screen_shift*self.map.engine.tilesize), (2, 0, current_percent+1, 35))
            # Draws foreground of health meter
            self.map.engine.surface.blit(self.map.engine.health_meter, ((x, y)-self.map.screen_shift*self.map.engine.tilesize), (0, 35, 35, 35))

            pygame.display.flip()
            self.map.engine.clock.tick(60)
        self.map.engine.pause(0.5)


    def render_sc_change(self, sc_before, sc_after):
        """
        # Function Name: render_hp_change
        # Purpose: Draws an HP meter and shows a change in HP
        # Inputs: hp_before, hp_after - the HP values before and after a change occurs
        """
        # Smoothstep function
        # See: http://sol.gfxile.net/interpolation/
        smoothstep = lambda v: (v*v*(3-2*v))
        meter_before = int(float(sc_before)*32/900.0)
        meter_after = int(float(sc_after)*32/900.0)
        delta_meter = meter_after - meter_before


        x, y = self.location_pixel

        frame_count = 30
        for t in xrange(0, frame_count):
            v = float(t)/float(frame_count)
            v = smoothstep(v)
            scale_term = int(delta_meter*v)

            current_percent = meter_before + scale_term

            # After the first action
            self.map.render_background()
            self.map.render_all_units()
            self.map.engine.surface.blit(self.map.engine.battle_board, (0, 490))

            # Draws background of health meter
            self.map.engine.surface.blit(self.map.engine.health_meter, ((x, y)-self.map.screen_shift*self.map.engine.tilesize), (35, 0, 35, 35))
            # Draws HP bar
            self.map.engine.surface.blit(self.map.engine.health_meter, ((x, y)-self.map.screen_shift*self.map.engine.tilesize), (37, 35, current_percent+1, 35))
            # Draws foreground of health meter
            self.map.engine.surface.blit(self.map.engine.health_meter, ((x, y)-self.map.screen_shift*self.map.engine.tilesize), (0, 35, 35, 35))

            pygame.display.flip()
            self.map.engine.clock.tick(60)
        self.map.engine.pause(0.5)

    def plot_stats(self, rhs = False):

        """
        # Function Name: plot_stats
        # Purpose: Plots the unit's portrait, name, HP, four stats, active spell, and active spell's mods to the
        # left side of the display panel
        """

        # Initialization of all text surfaces


        small_icon_panel = get_ui_panel((41, 41), border_color, panel_color)
        name_panel = get_ui_panel((150, 35), border_color, panel_color)
        spell_panel = get_ui_panel((179, 35), border_color, panel_color)
        level_panel = get_ui_panel((70, 35), border_color, panel_color)
        stat_panel = get_ui_panel((110, 35), border_color, panel_color)


        text_name = self.map.engine.speaker_font.render(self.name, True, (0, 0, 0))

        if text_name.get_width() > name_panel.get_width() - 20:
            text_name =self.map.engine.small_speaker_font.render(self.name, True, (0, 0, 0))


        text_lv = self.map.engine.section_font.render('Lv.', True, (0, 0, 0))
        text_lv_value = self.map.engine.data_font.render('%d'%(self.level), True, (0, 0, 0))
        text_hp = self.map.engine.section_font.render('HP', True, (0, 0, 0))
        if self.maxHP < 100:
            text_hp_value = self.map.engine.data_font.render('%d/%d'%(self.HP, self.maxHP), True, (0, 0, 0))
        else:
            text_hp_value = self.map.engine.sfont.render('%d/%d'%(self.HP, self.maxHP), True, (0, 0, 0))


        text_SC = self.map.engine.section_font.render('SC', True, (0, 0, 0))
        text_SC_value = self.map.engine.data_font.render('%d'%self.spirit, True, (0, 0, 0))

        if self.spell_actions[self.equipped]:
            text_spell = self.map.engine.data_font.render(self.spell_actions[self.equipped].namesuffix, True, (0, 0, 0))
            if text_spell.get_width() > spell_panel.get_width() - 20:
                text_spell = self.map.engine.sfont.render(self.spell_actions[self.equipped].namesuffix, True, (0, 0, 0))


        else:
            text_spell = self.map.engine.message_font.render("Empty", True, (100, 100, 100))

        # If the RHS flag is enabled, draw the portrait on the far right of the screen and draw
        # the stats on the right side of the screen. Used in the target select interface
        if rhs:
            x_offset = 330
            self.map.engine.surface.blit(self.av, (710, 500))


        else:
            x_offset = 0
            self.map.engine.surface.blit(self.av, (10, 500))


        if self.status:

            # Draw status effect icons on the player avatar
            max_icons = 5

            status_effect_rows = ceil(len(self.status.keys())/float(max_icons))
            status_background = pygame.Surface((116, 26*status_effect_rows))
            status_background.set_alpha(128)
            status_background.fill((0,0,0))


            if rhs:
                self.map.engine.surface.blit(status_background, (712,502))
            else:
                self.map.engine.surface.blit(status_background, (12,502))

            for index, status_effect in enumerate(self.status.keys()):
                icon_x, icon_y = self.map.engine.status_effects_catalog[status_effect].icon_location
                status_effect_image = self.map.engine.status_effect_icons.subsurface(icon_x*24, icon_y*24, 24, 24)

                position_y = index/max_icons
                position_x = index%max_icons

                if rhs:
                    status_icon_offset0 = 715
                else:
                    status_icon_offset0 = 15


                self.map.engine.surface.blit(status_effect_image, (status_icon_offset0+22*position_x, 502 + 24*position_y) )



        # Row 1: Name and Level
        self.map.engine.surface.blit(name_panel, (x_offset + 140, 500))
        self.map.engine.surface.blit(text_name, (x_offset + 140 + name_panel.get_width()/2 - text_name.get_width()/2,
                                                 500 + name_panel.get_height()/2 - text_name.get_height()/2))

        self.map.engine.surface.blit(level_panel, (x_offset + 300, 500))
        self.map.engine.surface.blit(text_lv, (x_offset + 309,
                                                502 + level_panel.get_height()/2 - text_lv.get_height()/2))
        self.map.engine.surface.blit(text_lv_value, (x_offset + 300 + level_panel.get_width()*3/4 - text_lv_value.get_width()/2,
                                                500 + level_panel.get_height()/2 - text_lv_value.get_height()/2))

        # Row 2: HP and SC
        self.map.engine.surface.blit(stat_panel, (x_offset + 140, 540))
        self.map.engine.surface.blit(text_hp, (x_offset + 149,
                                               542 + stat_panel.get_height()/2 - text_hp.get_height()/2))
        if self.maxHP < 100:
            self.map.engine.surface.blit(text_hp_value, (x_offset + 130 + stat_panel.get_width() - text_hp_value.get_width(),
                                                   539 + stat_panel.get_height()/2 - text_hp_value.get_height()/2))
        else:
            self.map.engine.surface.blit(text_hp_value, (x_offset + 134 + stat_panel.get_width() - text_hp_value.get_width(),
                                                   540 + stat_panel.get_height()/2 - text_hp_value.get_height()/2))


        self.map.engine.surface.blit(stat_panel, (x_offset + 260, 540))
        self.map.engine.surface.blit(text_SC, (x_offset + 275,
                                                542 + stat_panel.get_height()/2 - text_SC.get_height()/2))
        self.map.engine.surface.blit(text_SC_value, (x_offset + 245 + stat_panel.get_width() - text_SC_value.get_width(),
                                                539 + stat_panel.get_height()/2 - text_SC_value.get_height()/2))


        # Row 3: Spell Action
        self.map.engine.surface.blit(small_icon_panel, (x_offset + 140, 580))
        if self.spell_actions[self.equipped]:
            spell_icon_position = (x_offset + 140+small_icon_panel.get_width()/2-self.map.engine.spell_type_icons['Healing'].get_width()/2,
                                580+small_icon_panel.get_height()/2-self.map.engine.spell_type_icons['Healing'].get_height()/2)

            if self.spell_actions[self.equipped].type in ('healing', 'support'):
                self.map.engine.surface.blit(self.map.engine.spell_type_icons['Healing'], spell_icon_position)
            elif self.spell_actions[self.equipped].type == "healingitem":
                self.map.engine.surface.blit(self.map.engine.spell_type_icons['Item'], spell_icon_position)
            else:
                self.map.engine.surface.blit(self.map.engine.spell_type_icons[self.spell_actions[self.equipped].affinity], spell_icon_position)

        self.map.engine.surface.blit(spell_panel, (x_offset + 191, 582))

        self.map.engine.surface.blit(text_spell, (x_offset + 192 + spell_panel.get_width()/2 - text_spell.get_width()/2,
                                                  582 + spell_panel.get_height()/2 - text_spell.get_height()/2))


    def plot_battle_lhs(self):
        """
        # Function Name: plot_battle_lhs
        # Purpose: Plots the unit's portrait, name, HP, four stats, active spell, and active spell's mods to the
        # left side of the display panel
        """

        text_name = self.map.engine.bfont.render(self.name, True, (0, 0, 0))
        text_line1 = self.map.engine.sfont.render("HP: %3.0f/%3.0f" % (self.HP, self.maxHP), True, (0, 0, 0))
        text_line2 = self.map.engine.sfont.render("LV: %2.0f    EXP: %3.0f/100" % (self.level, self.exp), True, (0, 0, 0))

        # Trait lines
        if self.traits[0][0]:
            text_line3_str = "Action Trait: "+ self.traits[0][0].name
        else:
            text_line3_str = "Action Trait: None"

        if self.traits[1][0]:
            text_line4_str = 'Support Trait: '+self.traits[1][0].name
        else:
            text_line4_str = 'Support Trait: None'

        text_line3 = self.map.engine.sfont.render(text_line3_str, True, (0, 0, 0))
        text_line4 = self.map.engine.sfont.render(text_line4_str, True, (0, 0, 0))

        text_line5 = self.map.engine.sfont.render("Spirit Charge: %3.0f" % (self.spirit), True, (0, 0, 0))

        if self.spell_actions[self.equipped]:
            # Attack type
            self.map.engine.surface.blit(self.map.engine.spell_icons_big, (150, 552), self.spell_actions[self.equipped].a_type_big)
            # Damage type
            self.map.engine.surface.blit(self.map.engine.spell_icons_big, (175, 552), self.spell_actions[self.equipped].d_type_big)
            # Spell Type
            self.map.engine.surface.blit(self.map.engine.spell_icons_big, (200, 552), self.spell_actions[self.equipped].al_type_big)
            # Counterattack
            self.map.engine.surface.blit(self.map.engine.spell_icons_big, (225, 552), self.spell_actions[self.equipped].c_type_big)

        self.map.engine.surface.blit(self.av, (10, 500))
        self.map.engine.surface.blit(text_name, (150, 500))
        self.map.engine.surface.blit(text_line1, (150, 520))
        self.map.engine.surface.blit(text_line2, (150, 535))
        self.map.engine.surface.blit(text_line3, (150, 575))
        self.map.engine.surface.blit(text_line4, (150, 590))
        self.map.engine.surface.blit(text_line5, (150, 605))


    def plot_battle_rhs(self):
        """
        # Function Name: plot_stats_rhs
        # Purpose: Plots the unit's portrait, name, HP, four stats, active spell, and active spell's mods to the right
        # side of the display panel
        """

        text_name = self.map.engine.bfont.render(self.name, True, (0, 0, 0))
        text_line1 = self.map.engine.sfont.render("HP: %3.0f/%3.0f" % (self.HP, self.maxHP), True, (0, 0, 0))
        text_line2 = self.map.engine.sfont.render("LV: %2.0f    EXP: %3.0f/100" % (self.level, self.exp), True, (0, 0, 0))

        # Trait lines
        if self.traits[0][0]:
            text_line3_str = "Action Trait: "+ self.traits[0][0].name
        else:
            text_line3_str = "Action Trait: None"

        if self.traits[1][0]:
            text_line4_str = 'Support Trait: '+self.traits[1][0].name
        else:
            text_line4_str = 'Support Trait: None'

        text_line3 = self.map.engine.sfont.render(text_line3_str, True, (0, 0, 0))
        text_line4 = self.map.engine.sfont.render(text_line4_str, True, (0, 0, 0))


        text_line5 = self.map.engine.sfont.render("Spirit Charge: %3.0f" % (self.spirit), True, (0, 0, 0))


        if self.spell_actions[self.equipped]:
            # Attack type
            self.map.engine.surface.blit(self.map.engine.spell_icons_big, (570, 552), self.spell_actions[self.equipped].a_type_big)
            # Damage type
            self.map.engine.surface.blit(self.map.engine.spell_icons_big, (595, 552), self.spell_actions[self.equipped].d_type_big)
            # Spell Type
            self.map.engine.surface.blit(self.map.engine.spell_icons_big, (620, 552), self.spell_actions[self.equipped].al_type_big)
            # Counterattack
            self.map.engine.surface.blit(self.map.engine.spell_icons_big, (645, 552), self.spell_actions[self.equipped].c_type_big)

        self.map.engine.surface.blit(self.av, (430, 500))
        self.map.engine.surface.blit(text_name, (570, 500))
        self.map.engine.surface.blit(text_line1, (570, 520))
        self.map.engine.surface.blit(text_line2, (570, 535))
        self.map.engine.surface.blit(text_line3, (570, 575))
        self.map.engine.surface.blit(text_line4, (570, 590))
        self.map.engine.surface.blit(text_line5, (570, 605))

    def plot_predictor(self, target):
        """
        # Function Name: plot_predictor
        # Purpose: Plots the combat stats for self attacking target
        #            Sprites
        #            HP/Level
        #            Spell Name, Rank, Relationships
        # Inputs: target - Target being attacked
        """
        # Asks for the strings for the battle stats
        if self.spell_actions[self.equipped].type == 'attack':
            hit_user, hit_target = self.compute_hitpercent(target)
            crit_user, crit_target = self.compute_critpercent(target)
            effect_user, effect_target = self.predict_damage(target)
            relation, dmgmod, critmod = self.compute_spell_relation(target)

            if hit_user != "N/A":
                hit_user += "%"
            if hit_target != "N/A":
                hit_target += "%"
            if crit_target != "N/A":
                crit_target += "%"
            if crit_user != "N/A":
                crit_user += "%"

            draw_target = True

        elif self.spell_actions[self.equipped].type in ('healing', 'healingitem', 'support'):

            hit_user, hit_target = "100%", "N/A"
            crit_user, crit_target = "N/A", "N/A"
            effect_user, effect_target = self.predict_damage(target)
            relation = 'Neutral'
            draw_target = False

        # Generates the text objects
        text_eff = self.map.engine.section_font.render("Effect", True, (0, 0, 0))
        text_hit = self.map.engine.section_font.render("Hit", True, (0, 0, 0))
        text_crit = self.map.engine.section_font.render("Crit", True, (0, 0, 0))


        text_hit_user = self.map.engine.data_font.render(hit_user, True, (0, 0, 0))
        text_hit_target = self.map.engine.data_font.render(hit_target, True, (0, 0, 0))
        text_crit_user = self.map.engine.data_font.render(crit_user, True, (0, 0, 0))
        text_crit_target = self.map.engine.data_font.render(crit_target, True, (0, 0, 0))
        text_effect_user = self.map.engine.data_font.render(effect_user, True, (0, 0, 0))
        text_effect_target = self.map.engine.data_font.render(effect_target, True, (0, 0, 0))

        small_icon_panel = get_ui_panel((41, 41), border_color, panel_color)
        name_panel = get_ui_panel((190, 35), border_color, panel_color)
        stat_panel = get_ui_panel((150, 35), border_color, panel_color)

        text_user_name = self.map.engine.speaker_font.render(self.name, True, (0, 0, 0))
        text_target_name = self.map.engine.speaker_font.render(target.name, True, (0, 0, 0))

        # If unit is on the one side of the screen currently, draw the menu on the opposite side.
        if self.location_pixel.x - self.map.screen_shift.x*35 > 420:
            menu_x = 35
        else:
            menu_x = 840 - self.map.engine.vertical_panel.get_width() - 35

        self.map.engine.surface.blit(self.map.engine.vertical_panel, (menu_x, 70))

        # Draws the user's name
        self.map.engine.surface.blit(name_panel, (menu_x + 10, 80))
        self.map.engine.surface.blit(text_user_name, (menu_x + 10 + name_panel.get_width()/2 - text_user_name.get_width()/2,
                                                      80 + name_panel.get_height()/2 - text_user_name.get_height()/2))

        # Draws effect value
        self.map.engine.surface.blit(stat_panel, (menu_x + 30, 120))
        self.map.engine.surface.blit(text_eff, (menu_x + 60,
                                                      122 + stat_panel.get_height()/2 - text_eff.get_height()/2))
        self.map.engine.surface.blit(text_effect_user, (menu_x + 20 + stat_panel.get_width() - text_effect_user.get_width(),
                                                      120 + stat_panel.get_height()/2 - text_effect_user.get_height()/2))

        # Draws the hit rate
        self.map.engine.surface.blit(stat_panel, (menu_x + 30, 160))
        self.map.engine.surface.blit(text_hit, (menu_x + 60,
                                                      162 + stat_panel.get_height()/2 - text_hit.get_height()/2))
        self.map.engine.surface.blit(text_hit_user, (menu_x + 20 + stat_panel.get_width() - text_hit_user.get_width(),
                                                      160 + stat_panel.get_height()/2 - text_hit_user.get_height()/2))

        # Draws the crit rate
        self.map.engine.surface.blit(stat_panel, (menu_x + 30, 200))
        self.map.engine.surface.blit(text_crit, (menu_x + 60,
                                                      202 + stat_panel.get_height()/2 - text_crit.get_height()/2))
        self.map.engine.surface.blit(text_crit_user, (menu_x + 20 + stat_panel.get_width() - text_crit_user.get_width(),
                                                      200 + stat_panel.get_height()/2 - text_crit_user.get_height()/2))


        # Draws the target's name
        self.map.engine.surface.blit(name_panel, (menu_x + 10, 245))
        if draw_target:
            self.map.engine.surface.blit(text_target_name, (menu_x + 10 + name_panel.get_width()/2 - text_target_name.get_width()/2,
                                                      245 + name_panel.get_height()/2 - text_target_name.get_height()/2))

        # Draws effect value
        self.map.engine.surface.blit(stat_panel, (menu_x + 30, 285))
        if draw_target:
            self.map.engine.surface.blit(text_eff, (menu_x + 60,
                                                          287 + stat_panel.get_height()/2 - text_eff.get_height()/2))
            self.map.engine.surface.blit(text_effect_target, (menu_x + 20 + stat_panel.get_width() - text_effect_target.get_width(),
                                                          285 + stat_panel.get_height()/2 - text_effect_target.get_height()/2))

        # Draws the hit rate
        self.map.engine.surface.blit(stat_panel, (menu_x + 30, 325))
        if draw_target:
            self.map.engine.surface.blit(text_hit, (menu_x + 60,
                                                          327 + stat_panel.get_height()/2 - text_hit.get_height()/2))
            self.map.engine.surface.blit(text_hit_target, (menu_x + 20 + stat_panel.get_width() - text_hit_target.get_width(),
                                                          325 + stat_panel.get_height()/2 - text_crit_user.get_height()/2))

        # Draws the crit rate
        self.map.engine.surface.blit(stat_panel, (menu_x + 30, 365))
        if draw_target:
            self.map.engine.surface.blit(text_crit, (menu_x + 60,
                                                          367 + stat_panel.get_height()/2 - text_crit.get_height()/2))
            self.map.engine.surface.blit(text_crit_target, (menu_x + 20 + stat_panel.get_width() - text_crit_target.get_width(),
                                                          365 + stat_panel.get_height()/2 - text_crit_target.get_height()/2))


        if relation == 'Neutral' or self.spell_actions[self.equipped].type in ('healing', 'healingitem', 'support'):
            self.map.engine.surface.blit(self.map.engine.relation_arrows['neutral'], (menu_x + 37, 127))
            self.map.engine.surface.blit(self.map.engine.relation_arrows['neutral'], (menu_x + 37, 207))
            if draw_target:
                self.map.engine.surface.blit(self.map.engine.relation_arrows['neutral'], (menu_x + 37, 292))
                self.map.engine.surface.blit(self.map.engine.relation_arrows['neutral'], (menu_x + 37, 372))

        elif relation == 'Strong':

            self.map.engine.surface.blit(self.map.engine.relation_arrows['up'], (menu_x + 37, 127))
            self.map.engine.surface.blit(self.map.engine.relation_arrows['up'], (menu_x + 37, 207))

            self.map.engine.surface.blit(self.map.engine.relation_arrows['up'], (170, 605))
            self.map.engine.surface.blit(self.map.engine.relation_arrows['down'], (500, 605))
            if effect_target != "N/A":
                self.map.engine.surface.blit(self.map.engine.relation_arrows['down'], (menu_x + 37, 292))
                self.map.engine.surface.blit(self.map.engine.relation_arrows['down'], (menu_x + 37, 372))

        elif relation == 'Weak':
            self.map.engine.surface.blit(self.map.engine.relation_arrows['down'], (170, 605))
            self.map.engine.surface.blit(self.map.engine.relation_arrows['down'], (menu_x + 37, 127))
            self.map.engine.surface.blit(self.map.engine.relation_arrows['down'], (menu_x + 37, 207))

            self.map.engine.surface.blit(self.map.engine.relation_arrows['up'], (500, 605))
            if effect_target != "N/A":
                self.map.engine.surface.blit(self.map.engine.relation_arrows['up'], (menu_x + 37, 292))
                self.map.engine.surface.blit(self.map.engine.relation_arrows['up'], (menu_x + 37, 372))

        # Draws a bonus to hit if spells are of the right user preference and an attack spell is being used
        if self.spell_actions[self.equipped].type == "attack" and self.spell_actions[self.equipped].affinity == self.spell_preference:
            self.map.engine.surface.blit(self.map.engine.relation_arrows['up'], (menu_x + 37, 167))
        else:
            self.map.engine.surface.blit(self.map.engine.relation_arrows['neutral'], (menu_x + 37, 167))


        if effect_target != "N/A" and target.spell_actions[target.equipped].affinity == target.spell_preference:
            self.map.engine.surface.blit(self.map.engine.relation_arrows['up'], (menu_x + 37, 332))
        else:
            if draw_target:
                self.map.engine.surface.blit(self.map.engine.relation_arrows['neutral'], (menu_x + 37, 332))


    def plot_results(self, target, self_exp_delta, self_level_up,
                     target_exp_delta, target_level_up, self_spirit_delta, target_spirit_delta,
                     sc_cost_user, sc_cost_target):

        """
        # Function Name: plot_results
        # Purpose: Displays the battle's results
        # Inputs:   target = The target of this battle event
        #           self_exp_delta, target_exp_delta = experience points gained
        #           self_level_up, target_level_up = number of levels increased
        #           self_spirit_delta, enemy_spirit_delta = spirit charge change
        #           sc_cost_user, sc_cost_target = spirit charge cost for spells
        """

        if target.is_proxy_unit:
            target = target.parentunit

        sc_color = (100, 250, 250)
        exp_color = (100, 100, 250)
        empty_color = (100, 100, 50)

        name_panel = get_ui_panel((175, 35), border_color, panel_color)
        level_panel = get_ui_panel((70, 35), border_color, panel_color)

        text_lv = self.map.engine.section_font.render('Lv.', True, (0, 0, 0))
        text_EXP = self.map.engine.speaker_font.render("EXP", True, (0, 0, 0))
        text_SC = self.map.engine.speaker_font.render("SC", True, (0, 0, 0))

        # Initial display levels are at pre-level up settings
        self_display_level = self.level - self_level_up
        target_display_level = target.level - target_level_up

        # Sets up rendered text objects for unit names
        text_name = self.map.engine.speaker_font.render(self.name, True, (0, 0, 0))
        text_lv_value = self.map.engine.data_font.render('%d'%self_display_level, True, (0, 0, 0))
        text_target_name = self.map.engine.speaker_font.render(target.name, True, (0, 0, 0))
        text_target_lv_value = self.map.engine.data_font.render('%d'%target_display_level, True, (0, 0, 0))


        # Sets up a blank meter to be used on the screen
        # Draws the meter outline which is 2 pixels thick
        meter_panel = get_ui_panel((60, 35), border_color, panel_color)

        meter_outline_surface = pygame.Surface((180, 25), pygame.SRCALPHA)
        meter_outline_surface.blit(self.map.engine.meter_outline, (0, 0), (0, 0, meter_outline_surface.get_width()-2, 25) )
        meter_outline_surface.blit(self.map.engine.meter_outline, (meter_outline_surface.get_width()-2, 0), (self.map.engine.meter_outline.get_width()-2, 0, 2, 25))
        # Fills it with a blank color
        pygame.draw.rect(meter_outline_surface, empty_color, (2, 2, meter_outline_surface.get_width() - 4, 21))

        meter_width = float(meter_outline_surface.get_width() - 4)

        # Generates text objects for the changes in SC and EXP to display beside the meters
        if self_spirit_delta - sc_cost_user >= 0:
            text_sc_delta_self = self.map.engine.data_font.render("+%d"%(self_spirit_delta - sc_cost_user), True, (0, 0, 0))
        else:
            text_sc_delta_self = self.map.engine.data_font.render("%d"%(self_spirit_delta - sc_cost_user), True, (0, 0, 0))

        text_exp_delta_self = self.map.engine.data_font.render("+%d"%self_exp_delta, True, (0, 0, 0))

        if target_spirit_delta - sc_cost_target >= 0:
            text_sc_delta_target = self.map.engine.data_font.render("+%d"%(target_spirit_delta - sc_cost_target), True, (0, 0, 0))
        else:
            text_sc_delta_target = self.map.engine.data_font.render("%d"%(target_spirit_delta - sc_cost_target), True, (0, 0, 0))

        text_exp_delta_target = self.map.engine.data_font.render("+%d"%target_exp_delta, True, (0, 0, 0))

        text_level_up = self.map.engine.data_font.render("+1", True, (0, 0, 0))

        # This function draws any non-changing portions of the image
        def draw_static_components():
            self.map.render_background()
            self.map.render_all_units()
            self.map.render_cursor()
            self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
            self.map.engine.surface.blit(self.map.engine.results_panel, (280, 140))

            # Draws all the blank panels for this unit
            self.map.engine.surface.blit(name_panel, (295, 155))
            self.map.engine.surface.blit(level_panel, (475, 155))
            self.map.engine.surface.blit(meter_panel, (295, 195))
            self.map.engine.surface.blit(meter_panel, (295, 235))
            self.map.engine.surface.blit(meter_outline_surface, (365, 200))
            self.map.engine.surface.blit(meter_outline_surface, (365, 240))

            # The unit data is only drawn if the unit is alive
            if self.alive:
                self.map.engine.surface.blit(text_name, (295 + name_panel.get_width()/2 - text_name.get_width()/2,
                                                         155 + name_panel.get_height()/2 - text_name.get_height()/2))
                self.map.engine.surface.blit(text_lv, (475 + 9,
                                                        157 + level_panel.get_height()/2 - text_lv.get_height()/2))
                self.map.engine.surface.blit(text_lv_value, (475 + level_panel.get_width()*3/4 - text_lv_value.get_width()/2,
                                                        155 + level_panel.get_height()/2 - text_lv_value.get_height()/2))

                self.map.engine.surface.blit(text_SC, (295 + meter_panel.get_width()/2 - text_SC.get_width()/2,
                                                        195 + meter_panel.get_height()/2 - text_SC.get_height()/2))

                self.map.engine.surface.blit(text_EXP, (295 + meter_panel.get_width()/2 - text_EXP.get_width()/2,
                                                        235 + meter_panel.get_height()/2 - text_EXP.get_height()/2))

            # Draws all the blank panels for the target
            self.map.engine.surface.blit(name_panel, (295, 290))
            self.map.engine.surface.blit(level_panel, (475, 290))
            self.map.engine.surface.blit(meter_panel, (295, 330))
            self.map.engine.surface.blit(meter_panel, (295, 370))
            self.map.engine.surface.blit(meter_outline_surface, (365, 335))
            self.map.engine.surface.blit(meter_outline_surface, (365, 375))

            if target.alive and self != target:
                self.map.engine.surface.blit(text_target_name, (295 + name_panel.get_width()/2 - text_target_name.get_width()/2,
                                                         290 + name_panel.get_height()/2 - text_target_name.get_height()/2))
                self.map.engine.surface.blit(text_lv, (475 + 9,
                                                        292 + level_panel.get_height()/2 - text_lv.get_height()/2))
                self.map.engine.surface.blit(text_target_lv_value, (475 + level_panel.get_width()*3/4 - text_target_lv_value.get_width()/2,
                                                        290 + level_panel.get_height()/2 - text_lv_value.get_height()/2))
                self.map.engine.surface.blit(text_SC, (295 + meter_panel.get_width()/2 - text_SC.get_width()/2,
                                                        330 + meter_panel.get_height()/2 - text_SC.get_height()/2))

                self.map.engine.surface.blit(text_EXP, (295 + meter_panel.get_width()/2 - text_EXP.get_width()/2,
                                                        370 + meter_panel.get_height()/2 - text_EXP.get_height()/2))

        smoothstep = lambda v: (v*v*(3-2*v))

        self_sc_meter_before = int((self.spirit - self_spirit_delta + sc_cost_user)*meter_width/900)
        self_sc_meter_after = int(self.spirit*meter_width/900)
        self_sc_meter_delta = self_sc_meter_after - self_sc_meter_before

        target_sc_meter_before = int((target.spirit - target_spirit_delta + sc_cost_target)*meter_width/900)
        target_sc_meter_after = int(target.spirit*meter_width/900)
        target_sc_meter_delta = target_sc_meter_after - target_sc_meter_before

        self_starting_exp = self.exp - self_exp_delta + 100*self_level_up
        target_starting_exp = target.exp - target_exp_delta + 100*target_level_up
        self_exp_meter_before = int(self_starting_exp*meter_width/100)
        target_exp_meter_before = int((target_starting_exp)*meter_width/100)


        # Shows this unit's SC change
        max_frames = 30

        self_sc_meter_done = False
        self_exp_meter_done = False
        target_sc_meter_done = False
        target_exp_meter_done = False

        while not self_sc_meter_done or not self_exp_meter_done or not target_sc_meter_done or not target_exp_meter_done:


            # If this unit is dead, ignore it
            if self.alive:

                # Determines the current point to bring the EXP meter up to on this cycle. The meter only fills to 100%.
                self_intermediate_exp = min(100, self_starting_exp + self_exp_delta)

                # Determines how much of the positions of the EXP meters
                self_used_exp = self_intermediate_exp - self_starting_exp
                self_exp_meter_after = int(self_intermediate_exp*meter_width/100)
                self_exp_meter_delta = self_exp_meter_after - self_exp_meter_before
            else:
                self_used_exp = 0
                self_exp_meter_after = 0
                self_intermediate_exp = 0

            # If this unit is targetting itself or there was a successful kill, do not do anything with this unit's EXP
            if target.alive and target != self:
                target_intermediate_exp = min(100, target_starting_exp + target_exp_delta)
                target_used_exp = target_intermediate_exp - target_starting_exp
                target_exp_meter_after = int(target_intermediate_exp*meter_width/100)
                target_exp_meter_delta = target_exp_meter_after - target_exp_meter_before

            else:
                target_used_exp = 0
                target_exp_meter_after = 0
                target_intermediate_exp = 0



            for frame_num in xrange(0, max_frames):

                # Implements a smoothstep transition for the animation
                v = float(frame_num)/float(max_frames)
                v = smoothstep(v)

                # looks for event type data to select interaction
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                        exit()

                draw_static_components()

                # the unit bar's final state is drawn and then a solid rectangle is placed on top to show a transition between before and after.
                # This technique is used in all four segments
                if self.alive:


                    self_sc_meter_step = abs(int(v*self_sc_meter_delta))

                    self_exp_meter_step = abs(int(v*self_exp_meter_delta))

                    self.map.engine.surface.blit(self.map.engine.big_sc_meter, (367, 202), (0, 0, self_sc_meter_after ,21))
                    self.map.engine.surface.blit(self.map.engine.big_exp_meter, (367, 242), (0, 0, self_exp_meter_after ,21))

                    # Draw Numerical Difference Boxes
                    # Spirit Charge Difference
                    self.map.engine.surface.blit(meter_panel, (550, 195))
                    self.map.engine.surface.blit(text_sc_delta_self, (550 + meter_panel.get_width()/2 - text_sc_delta_self.get_width()/2,
                                                                  195 + meter_panel.get_height()/2 - text_sc_delta_self.get_height()/2))
                    # EXP Difference
                    self.map.engine.surface.blit(meter_panel, (550, 235))
                    self.map.engine.surface.blit(text_exp_delta_self, (550 + meter_panel.get_width()/2 - text_exp_delta_self.get_width()/2,
                                                                      235 + meter_panel.get_height()/2 - text_exp_delta_self.get_height()/2))


                    # Draw animation of spirit charge difference for this unit
                    if not self_sc_meter_done:
                        if abs(self_sc_meter_delta - self_sc_meter_step) > 1:
                            if self_sc_meter_delta < 0:
                                pygame.draw.rect(self.map.engine.surface, sc_color, (367 + self_sc_meter_after -1, 202, -1*self_sc_meter_delta - self_sc_meter_step, 21))
                            else:
                                pygame.draw.rect(self.map.engine.surface, sc_color, (367 + self_sc_meter_after -1, 202, -1*(self_sc_meter_delta - self_sc_meter_step), 21))


                    # Draw animation of experience difference for this unit
                    if not self_exp_meter_done:
                        pygame.draw.rect(self.map.engine.surface, exp_color, (367 + self_exp_meter_after -1, 242, -1*(self_exp_meter_delta - self_exp_meter_step) + 2, 21))


                if target.alive and target!= self:

                    target_sc_meter_step = abs(int(v*target_sc_meter_delta))

                    target_exp_meter_step = abs(int(v*target_exp_meter_delta))

                    self.map.engine.surface.blit(self.map.engine.big_sc_meter, (367, 337), (0, 0, target_sc_meter_after ,21))
                    self.map.engine.surface.blit(self.map.engine.big_exp_meter, (367, 377), (0, 0, target_exp_meter_after ,21))


                    # Draw Numerical Difference Boxes
                    # Spirit Charge Difference
                    self.map.engine.surface.blit(meter_panel, (550, 330))
                    self.map.engine.surface.blit(text_sc_delta_target, (550 + meter_panel.get_width()/2 - text_sc_delta_target.get_width()/2,
                                                                      330 + meter_panel.get_height()/2 - text_sc_delta_target.get_height()/2))
                     # EXP Difference
                    self.map.engine.surface.blit(meter_panel, (550, 370))
                    self.map.engine.surface.blit(text_exp_delta_target, (550 + meter_panel.get_width()/2 - text_exp_delta_target.get_width()/2,
                                                                      370 + meter_panel.get_height()/2 - text_exp_delta_target.get_height()/2))

                    # Draw animation of spirit charge difference for this unit
                    if not target_sc_meter_done:
                        if abs(target_sc_meter_delta - target_sc_meter_step) > 1:
                            if target_sc_meter_delta < 0:
                                pygame.draw.rect(self.map.engine.surface, sc_color, (367 + target_sc_meter_after -1, 337, -1*target_sc_meter_delta - target_sc_meter_step, 21))
                            else:
                                pygame.draw.rect(self.map.engine.surface, sc_color, (367 + target_sc_meter_after -1, 337, -1*(target_sc_meter_delta - target_sc_meter_step), 21))


                    # Draw animation of experience difference for this unit
                    if not target_exp_meter_done:
                        pygame.draw.rect(self.map.engine.surface, exp_color, (367 + target_exp_meter_after -1, 377, -1*(target_exp_meter_delta - target_exp_meter_step) + 2, 21))


                pygame.display.flip()
                self.map.engine.clock.tick(60)


            # If this unit's current EXP is at 100, empty the meter and increase the displayed level by 1
            if self_intermediate_exp == 100:
                self_display_level += 1
                text_lv_value = self.map.engine.data_font.render('%d'%self_display_level, True, (0, 0, 0))
                self.map.engine.sfx_system.sound_catalog['levelup'].play()

                self.map.engine.surface.blit(meter_panel, (550, 155))
                self.map.engine.surface.blit(text_level_up, (550 + meter_panel.get_width()/2 - text_level_up.get_width()/2,
                                                                      155 + meter_panel.get_height()/2 - text_level_up.get_height()/2))

                pygame.display.flip()
                self.map.engine.clock.tick(60)
                self.map.engine.pause(0.75)

                self_starting_exp = 0
                self_exp_meter_before = 0

            # If the target unit's current EXP is at 100, empty the meter and increase the displayed level by 1
            if target_intermediate_exp == 100:


                self.map.engine.surface.blit(meter_panel, (550, 370))
                self.map.engine.surface.blit(text_exp_delta_target, (550 + meter_panel.get_width()/2 - text_exp_delta_target.get_width()/2,
                                                                  370 + meter_panel.get_height()/2 - text_exp_delta_target.get_height()/2))

                target_display_level += 1
                text_target_lv_value = self.map.engine.data_font.render('%d'%target_display_level, True, (0, 0, 0))
                self.map.engine.sfx_system.sound_catalog['levelup'].play()


                self.map.engine.surface.blit(meter_panel, (550, 290))
                self.map.engine.surface.blit(text_level_up, (550 + meter_panel.get_width()/2 - text_level_up.get_width()/2,
                                                                      290 + meter_panel.get_height()/2 - text_level_up.get_height()/2))
                self.map.engine.pause(0.75)

                target_starting_exp = 0
                target_exp_meter_before = 0


            # SC changes will always finish after one cycle
            self_sc_meter_done = True
            target_sc_meter_done = True


            if self.alive:

                # Check if this unit encountered a level-up situation, if so, go for another cycle.
                self_exp_delta -= self_used_exp
                if self_exp_delta > 0:
                    self_exp_meter_done = False
                else:
                    self_exp_meter_done = True
            else:
                self_exp_meter_done = True


            if target.alive and target!= self:

                # Check if the target unit encountered a level-up situation, if so, go for another cycle.
                target_exp_delta -= target_used_exp
                if target_exp_delta > 0:
                    target_exp_meter_done = False
                else:
                    target_exp_meter_done = True
            else:
                target_exp_meter_done = True

        # Pause to show the final result for 1.25s
        self.map.engine.pause(1.25)


    def post_battle_event(self, target):
        '''
        # Function Name: Post-battle Event
        # Purpose: Processes post battle stats updates like lowering spell use counts
        # Inputs: Target - other participant in the battle
        '''

        # Lowers life of the spell action by 1
        self.spell_actions[self.equipped].livesleft -= 1

        # Takes off SC cost of the spell action
        if self.spell_actions[self.equipped].sc_cost > 0:
            self.spirit -= self.spell_actions[self.equipped].sc_cost
            if self.spirit < 0:
                self.spirit = 0

        # If lives left are 0, replaces the equipped slot with empty
        if self.spell_actions[self.equipped].livesleft == 0:
            self.map.display_alert('Spell Action Used Up!', "%s's %s has run out of uses!" % (self.name, self.spell_actions[self.equipped].namesuffix))
            if self.spell_actions[self.equipped].consumable == True:
                self.spell_actions[self.equipped] = None


        # Checks the opponent if they have an equipped spell and if it was used in a counterattack
        delta_pos = self.location_tile - target.location_tile
        if (target.spell_actions[target.equipped] and target.alive == True
           and target.spell_actions[target.equipped].livesleft > 0
           and target.spell_actions[target.equipped].counterattack == True
           and tuple(delta_pos) in target.spell_actions[target.equipped].validattacks
           and target.spirit >= target.spell_actions[target.equipped].unlock):
            # Lowers life of the spell action by 1
            target.spell_actions[target.equipped].livesleft -= 1


            # Takes off SC cost of the spell action
            if target.spell_actions[target.equipped].sc_cost > 0:
                target.spirit -= target.spell_actions[target.equipped].sc_cost
                if target.spirit < 0:
                    target.spirit = 0

            # If lives left are 0, replaces the equipped slot with empty
            if target.spell_actions[target.equipped].livesleft == 0:
                self.map.display_alert('Spell Action Used Up!', "%s's %s has run out of uses!" % (target.name, target.spell_actions[target.equipped].namesuffix))
                if target.spell_actions[target.equipped].consumable == True:
                    target.spell_actions[target.equipped] = None

    def can_counterattack(self, target):
        """
        # Fuction name: can_counterattack
        # Purpose: checks if a unit is able to counterattack (spell permits / status effects permits
        # Outputs:    True if unit is able to counter
        #             False if unit is not able to counter
        """
        # Spell Conditions
        #    - A spell is equipped
        #    - A spell has enough uses left
        #    - Spell can counterattack
        #    - SC requirements are met

        if self.spell_actions[self.equipped]:
            can_use_spell = self.spell_actions[self.equipped].livesleft > 0 and self.spell_actions[self.equipped].counterattack == True and self.spirit >= self.spell_actions[self.equipped].unlock

            # Target is in range
            delta_pos = self.location_tile - target.location_tile
            target_in_range =  tuple(delta_pos) in self.spell_actions[self.equipped].validattacks

        else:
            can_use_spell = False
            target_in_range = False

        # Does not have any blocking status effects
        blocking_status_list = ['Stun', 'Invisible']
        can_attack = True
        # If unit has at least one bocking status, unit cannot attack
        for status in blocking_status_list:
            if status in self.status.keys():
                can_attack = False

        return self.alive and can_use_spell and target_in_range and can_attack

    #############################
    # Character Event Methods
    #############################

    def map_heal(self, target, action, effect=0, bullet_id='Auto'):

        """
        # Function name: map_heal
        # Purpose: Plots an animation for a character healing herself. Also applicable for healingitems
        # Inputs:
        #       target - target to show effect on
        #       action - name of healing action
        #       effect - How much HP is healed (0 if it is relying on a spell/item)
        #       bullet_id - bullet to use for animation
        """

        # Generates name of the spell at the top
        text_name = self.map.engine.section_font.render(action, True, (0, 0, 0))

        if text_name.get_width > self.map.engine.map_spell_board.get_width() - 50:
            text_name = self.map.engine.sfont.render(action, True, (0, 0, 0))



        half_width = text_name.get_width()/2

        spell_used = False

        if effect == 0:
            # Designates that a spell was used in this sequence
            spell_used = True
            effect = self.spell_actions[self.equipped].get_effect(self, target)
            sc_cost = self.spell_actions[self.equipped].sc_cost
            self.spell_actions[self.equipped].livesleft -= 1
        else:
            sc_cost = 0


        # Origin
        x_o = (target.location_pixel.x)
        y_o = (target.location_pixel.y)

        effect_text = self.map.engine.render_outlined_text(str(effect), self.map.engine.cfont, (100, 255, 100), (0, 0, 0))

        # Play the sound effect of a healing item
        self.map.engine.sfx_system.sound_catalog['item'].play()

        # Shows animation if animation option is set to true
        if self.map.engine.options.battle_anim == True:
            # Shows the equipped bullet flying in a circle around the user
            # Uses parametric equation for a circle to animate
            for i in xrange(0, 21):

                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                        exit()

                self.map.render_background()
                self.map.render_all_units()
                self.map.render_cursor()
                self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
                self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
                self.map.engine.surface.blit(text_name, (420-half_width, 20))
                self.plot_stats()

                x = x_o+30*sin(i*pi/5)
                y = y_o+30*cos(i*pi/5)

                self.map.engine.surface.blit(self.map.engine.heal_bullet, ((x, y)-self.map.screen_shift*self.map.engine.tilesize))
                pygame.display.flip()
                self.map.engine.clock.tick(60)
        else:

            self.map.render_background()
            self.map.render_all_units()
            self.map.render_cursor()
            self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
            self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
            self.map.engine.surface.blit(text_name, (420-half_width, 20))
            self.plot_stats()

        rhs_hp_before = target.HP
        target.HP += effect

        if target.HP > target.maxHP:
            target.HP = target.maxHP


        # Only renders the value of the healing if the effect is nonzero
        if effect > 0:
            self.map.render_background()
            self.map.render_all_units()
            self.map.render_cursor()
            self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
            self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
            self.map.engine.surface.blit(text_name, (420-half_width, 20))
            self.plot_stats()
            self.map.engine.surface.blit(effect_text, ((target.location_pixel.x+18-effect_text.get_width()/2, target.location_pixel.y-25)-self.map.screen_shift*self.map.engine.tilesize))

            pygame.display.flip()
            self.map.engine.clock.tick(60)
            self.map.engine.pause(1)

            rhs_hp_after = target.HP
            target.render_hp_change(rhs_hp_before, rhs_hp_after)

        if spell_used == True:
            # If lives left are 0, replaces the equipped slot with empty
            if self.spell_actions[self.equipped].livesleft == 0:
                self.map.display_alert('Spell Action Used Up!', "%s's %s has run out of uses!" % (self.name, self.spell_actions[self.equipped].namesuffix))
                if self.spell_actions[self.equipped].consumable == True:
                    self.spell_actions[self.equipped] = None

        return effect, sc_cost

    #############################
    # Interaction Methods
    #############################


    def move_to(self, destination):
        """
        # Function Name: move_to
        # Purpose: Move a unit from one place to another. Used in scripted movements
        # Inputs: destination - destination to move a unit to
        """

        path = []
        # Intermediate step current position
        step_pos = self.location_tile
        delta = Vector2(destination) - self.location_tile

        # Gets all the moves in X
        while delta.x != 0:
            if delta.x > 0:
                path.append(Vector2(1, 0))
                step_pos.x += 1
            elif delta.x < 0:
                step_pos.x -= 1
                path.append(Vector2(-1, 0))
            delta =  Vector2(destination) - step_pos
        # gets all the moves in Y
        while delta.y != 0:
            if delta.y > 0:
                step_pos.y += 1
                path.append(Vector2(0, 1))
            elif delta.y < 0:
                step_pos.y -= 1
                path.append(Vector2(0, -1))
            delta = Vector2(destination) - step_pos
        self.render_walk(path)

        self.update_location(*destination)


    def menu_loop(self, can_move = True, can_act = True):

        """
        # Function Name: menu_loop
        # Purpose: The unit's first level menu:
        #       Allows selection of: Move, Spell, traits Stats, Wait, and Cancel if possible
        """

        menu_flag = True
        menu_pos = 0

        options_panel = get_ui_panel((180, 35), border_color, panel_color)
        disabled_panel = get_ui_panel((180, 35), border_color, disabled_color)

        # Conditions for using a SC or Wait: Has not used a spell yet, is alive
        # Conditions for moving: Has not moved yet, has not used a spell yet, is alive
        options = []

        # List of panels to gray out indicating that they are disabled
        gray_out = []

        options.append(self.map.engine.section_font.render("Move", True, (0, 0, 0)))
        if 'Immobilize' in self.status.keys():
            can_move = False

        if not can_move  or self.turnend:
            gray_out.append(0)

        options.append(self.map.engine.section_font.render("Spells", True, (0, 0, 0)))
        if not can_act or  self.turnend:
            gray_out.append(1)

        skills_available = []
        for trait in self.traits:
            if trait and trait.variation == "Trait Skill":
                skill = self.map.engine.trait_actions_catalog[trait.name]
                skills_available.append(skill)
                skill_option = skill.name

                if skill.check_usability(self):
                    if self.turnend or not can_act:
                        gray_out.append(2 + len(skills_available) - 1)

                else:
                    gray_out.append(2 + len(skills_available) - 1)

                text_skill = self.map.engine.section_font.render(skill_option, True, (0, 0, 0))
                if text_skill.get_width() > options_panel.get_width() - 20:
                    text_skill = self.map.engine.sfont.render(skill_option, True, (0, 0, 0))

                options.append(text_skill)

        options.append(self.map.engine.section_font.render("Stats", True, (0, 0, 0)))
        options.append(self.map.engine.section_font.render("Wait", True, (0, 0, 0)))
        options.append(self.map.engine.section_font.render("Cancel", True, (0, 0, 0)))

        max_menu_pos = len(options)-1

        update = True

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    update = True
                    # if either the Up or Right keys are pressed, and the menu position
                    # is not at the top, move the menu position up one.
                    if ( event.key == K_UP or event.key == K_LEFT ):
                        if menu_pos > 0:
                            menu_pos -= 1
                        elif menu_pos == 0:
                            menu_pos = max_menu_pos
                    if ( event.key == K_DOWN or event.key == K_RIGHT ):
                        if menu_pos < max_menu_pos:
                            menu_pos += 1
                        elif menu_pos == max_menu_pos:
                            menu_pos = 0

                    if ( event.key == K_z or event.key == K_RETURN):


                        # This option sends the user to the character's move select loop
                        # Conditions for moving: Has not moved yet, has not used a spell yet, is alive
                        if menu_pos == 0 and can_move and not self.turnend and self.alive:

                            confirmedmove = self.move_loop()
                            # updates location after a move has been made

                            if self.turnend == True:
                                self.map.get_all_moves()
                                menu_flag = False


                        # This option sends the user to the character's spell select loop
                        # Conditions for using an action: Has not used a spell yet, is alive
                        if menu_pos == 1 and can_act and not self.turnend and self.alive:

                            confirmedattack = self.spell_loop_a()
                            if confirmedattack:
                                self.map.get_all_moves()

                                if self.has_trait_property('Attack Move') and self.alive and not self.moved and confirmedattack != "Waited":
                                    self.move_loop(can_act = False)

                                self.turnend = True
                                menu_flag = False

                        # This option sends the user to the character's trait switching loop
                        # Conditions for swapping trait: Traits may be swapped any time before a unit commits to an action
                        if skills_available and can_act and menu_pos > 1 and menu_pos < len(options)-3 and self.turnend == False and self.alive == True:
                            skill_index = menu_pos - 2
                            if skills_available[skill_index].check_usability(self):
                                starting_spirit = self.spirit

                                # Subtracts off the cost of this action
                                self.spirit -= skills_available[skill_index].sc_cost
                                self.check_spirit_range()
                                skill_used, skill_exp = skills_available[skill_index].player_interface(self)
                                if skill_used or self.turnend:
                                    spirit_delta = skills_available[skill_index].sc_cost

                                    # If the skill gives EXP, show the results
                                    if skill_exp or spirit_delta != 0:

                                        # Trait EXP bonus
                                        skill_exp = int(skill_exp*(1+sum([trait.expmod for trait in self.traits if trait])))

                                        # EXP Cap of 200 EXP
                                        if skill_exp > 200:
                                            skill_exp = 200

                                        self.exp += skill_exp

                                        level_up = self.level_up_check()

                                        self.plot_results(self, skill_exp, level_up, 0, False, 0, 0, spirit_delta, 0)

                                    self.map.cursor_pos = Vector2(tuple(self.location_tile))
                                    self.turnend = True
                                    menu_flag = False
                                else:
                                    self.spirit += skills_available[skill_index].sc_cost
                                    self.check_spirit_range()

                        if menu_pos == len(options)-3:
                            self.map.stats_interface(self)

                        # This option ends the character's turn
                        if menu_pos == len(options)-2 and self.turnend == False and self.alive == True:
                            self.turnend = True
                            menu_flag = False


                        # This option cancels without ending the turn
                        if menu_pos == len(options)-1:
                            menu_flag = False
                    if ( event.key == K_x ):
                        menu_flag = False

            if menu_flag:

                if update:
                    self.map.render_background()
                    self.map.render_all_units()
                    self.map.render_cursor()
                    self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
                    pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                               %(self.map.cursor_pos.x, self.map.cursor_pos.y, self.map.screen_shift.x, self.map.screen_shift.y))

                    # If unit is on the one side of the screen currently, draw the menu on the opposite side.
                    if self.location_pixel.x - self.map.screen_shift.x*35 > 420:
                        menu_x = 35
                    else:
                        menu_x = 840 - self.map.engine.vertical_panel.get_width() - 35

                    self.map.engine.surface.blit(self.map.engine.vertical_panel, (menu_x, 70))

                    # Checks if there is a unit underneath the cursor, and if there is, plots the unit's data.
                    selected = False
                    selected = self.map.cursor_key_search()
                    if selected is not False:
                        self.map.all_units_by_name[selected].plot_stats()

                    # Calculates the position where the top of the menu is drawn
                    menu_y = 70 + self.map.engine.vertical_panel.get_height()/2  - len(options)*45/2

                    for index, option_text in enumerate(options):

                        # If this action is unavailable, use a grayed out box
                        if index in gray_out:
                            self.map.engine.surface.blit(disabled_panel, (menu_x + self.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2,
                                                                     menu_y + index*45))
                        else:
                            self.map.engine.surface.blit(options_panel, (menu_x + self.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2,
                                                                     menu_y + index*45))

                        # Draws a dark border around the currently selected option
                        if index == menu_pos:
                            padlib_rounded_rect(self.map.engine.surface, selected_color, (menu_x + self.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2 - 2,
                                                                     menu_y + index*45 -2, 180 + 4, 35 + 4), 6, 5)


                        self.map.engine.surface.blit(option_text, (menu_x + self.map.engine.vertical_panel.get_width()/2 - option_text.get_width()/2,
                                                                     menu_y + 2 + options_panel.get_height()/2 - option_text.get_height()/2 + index*45))

                    pygame.display.flip()
                    update = False

                self.map.engine.clock.tick(60)


    def move_loop(self, can_act = True):

        """
        # Function Name: move_loop
        # Purpose: The unit's second level move loop:
        #      Allows the player to select where they want to move a unit
        # Output: moved_flag = True if a selection has been made, False if one has not been made
        """

        self.start_pos = tuple(self.location_tile)
        self.get_moves_path()
        menu_flag = True
        self.map.framenum = 0
        while menu_flag:
            # Frame counter for holding down the keys to move
            if self.map.framenum == 10:
                self.map.framenum = 0
            self.map.framenum += 1

            arrowkeys = False
            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:


                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        self.map.cursor_arrows(event)
                        arrowkeys = True
                        # Resets the frame counter
                        self.map.framenum = 0

                    if event.key == K_x:
                        menu_flag = False

                        self.map.center_on(self)

                    if event.key == K_z or event.key == K_RETURN:

                        # If the Z key is pressed, it will calculate the vector between the current position
                        # of the cursor and the unit's location. If that vector is part of the valid moves,
                        # the unit is moved there.
                        delta_pos = self.map.cursor_pos - self.location_tile
                        new_pos = self.map.cursor_pos
                        if self.validmoves.has_key(tuple(delta_pos)):
                            path = self.get_path(tuple(delta_pos))
                            if new_pos != self.location_tile:
                                self.render_walk(path)
                            self.update_location(new_pos.x, new_pos.y)
                            self.moved = True
                            # Enters menu loop:
                            #   can_move is set to False since unit cannot make another movement after this one
                            #   can_act is set to False in the event that the enemy can only wait at the destination
                            self.menu_loop(can_move=False, can_act = can_act)

                            if self.turnend:
                                menu_flag = False
                            else:
                                self.update_location(self.start_pos[0], self.start_pos[1])
                                self.moved = False

                            self.map.cursor_pos = Vector2(tuple(self.location_tile))



            # if there is not a tap detected, check if the key is being held down
            if arrowkeys == False and self.map.framenum == 9:
                self.map.cursor_arrows_hold()


            if menu_flag:
                pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                       %(self.map.cursor_pos.x, self.map.cursor_pos.y, self.map.screen_shift.x, self.map.screen_shift.y))

                self.map.render_background()

                self.plot_valid_moves()

                self.map.render_all_units()
                self.map.render_cursor()

                self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
                self.map.render_current_terrain_data()

                # Checks if there is a unit underneath the cursor, and if there is, plots the unit's data.
                selected = False
                selected = self.map.cursor_key_search()
                if selected is not False:
                    self.map.all_units_by_name[selected].plot_stats()

                pygame.display.flip()
                self.map.engine.clock.tick(60)

    def spell_loop_a(self):
        """
        # Function Name: Spell Loop A
        # Purpose: The unit's second level spell loop:
        #      Allows the player to select a spell to use
        # Output: attacked_flag = True if an attack has been made, False if one has not been made
        """

        menu_flag = True
        menu_pos = 0

        options_panel = get_ui_panel((220, 41), border_color, panel_color)
        small_icon_panel = get_ui_panel((41, 41), border_color, panel_color)
        sc_panel = get_ui_panel((130, 41), border_color, panel_color)
        disabled_equip_panel = get_ui_panel((130, 41), border_color, disabled_color)
        equip_panel = get_ui_panel((150, 105), border_color, (220, 220, 70))

        disabled_options = []
        spell_names = []
        spell_uses = []
        spell_costs = []

        # Generates text surfaces for all spells in the inventory
        for index, spell_action in enumerate(self.spell_actions):
            if spell_action:

                # Gray out spell if it can't be used
                if spell_action.livesleft == 0 or spell_action.unlock > self.spirit:

                    disabled_options.append(index)

                    spell_name_text = self.map.engine.data_font.render(spell_action.namesuffix, True, (150, 150, 150))
                    if spell_name_text.get_width() > options_panel.get_width() - 20:
                        spell_name_text = self.map.engine.message_font.render(spell_action.namesuffix, True, (150, 150, 150))

                else:

                    spell_name_text = self.map.engine.data_font.render(spell_action.namesuffix, True, (0, 0, 0))
                    if spell_name_text.get_width() > options_panel.get_width() - 20:
                        spell_name_text = self.map.engine.message_font.render(spell_action.namesuffix, True, (0, 0, 0))


                spell_names.append(spell_name_text)

                spell_uses.append(self.map.engine.data_font.render('%d'%spell_action.livesleft, True, (0, 0, 0)))

                if self.spirit > spell_action.unlock:
                    # SC changes for spirit saver and spirit booster traits
                    SAVER_MOD = 0.8
                    BOOSTER_MOD = 1.2

                    if self.has_trait_property('Spirit Saver'):
                        sc_cost = int(spell_action.sc_cost*SAVER_MOD)
                    elif self.has_trait_property('Spirit Booster'):
                        sc_cost = int(spell_action.sc_cost*BOOSTER_MOD)
                    else:
                        sc_cost = spell_action.sc_cost

                    if sc_cost > 0:
                        spell_costs.append(self.map.engine.data_font.render("-%d SC"%sc_cost, True, (0,0,0)))
                    else:
                        spell_costs.append(None)
                else:
                    spell_costs.append(self.map.engine.data_font.render("SC > %d"%spell_action.unlock, True, (0,0,0)))

            # Gray out spell box if nothing is available
            else:
                disabled_options.append(index)
                spell_names.append (self.map.engine.data_font.render('Empty', True, (150, 150, 150)))
                spell_uses.append(None)
                spell_costs.append(None)
        wait_text = self.map.engine.section_font.render('Wait', True, (0, 0, 0))
        cancel_text = self.map.engine.section_font.render('Cancel', True, (0, 0, 0))
        use_text = self.map.engine.section_font.render('Use', True, (0, 0, 0))
        equip_text = self.map.engine.section_font.render('Equip', True, (0, 0, 0))

        update = True

        # Sub menu-flag for selecting whether to equip or use a spell
        equip_mode = False
        equip_cursor = 0

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                update = True
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    # If a spell has not been designated, allow player to go through options
                    if not equip_mode:

                        if ( event.key == K_UP or event.key == K_LEFT ):
                            if menu_pos > 0:
                                menu_pos -= 1
                            elif menu_pos == 0:
                                menu_pos = 6
                        if ( event.key == K_DOWN or event.key == K_RIGHT ):
                            if menu_pos < 6:
                                menu_pos += 1
                            elif menu_pos == 6:
                                menu_pos = 0


                    # Otherwise, alternate between Use / Equip settings
                    else:
                        if event.key in (K_UP, K_DOWN, K_RIGHT, K_LEFT):
                            if equip_cursor == 0:
                                equip_cursor = 1
                            else:
                                equip_cursor = 0

                    if  event.key == K_z  or event.key == K_RETURN:

                        if menu_pos < 5 and equip_mode:
                            # Selection made to use spell
                            if equip_cursor == 0:

                                # Conditions for selecting a spellcard:
                                #   -Position of the menu is between 1 and 5,
                                #   -the spell does not correspond to an empty slot, and the number of uses left is > 0.
                                #   -the spell's spirit charge unlock is lower than or equal to the user's spirit charge
                                if self.spell_actions[menu_pos] and self.spell_actions[menu_pos].livesleft > 0 and self.spirit >= self.spell_actions[menu_pos].unlock:
                                    self.equipped = menu_pos

                                    self.get_valid_spell_range()
                                    action_confirmed = self.spell_loop_b()
                                    if action_confirmed:
                                        return action_confirmed
                                    else:
                                        equip_mode = False
                                        equip_cursor = 0
                                        break

                            # Option to equip but not use the spell
                            if equip_cursor == 1:

                                self.equipped = menu_pos
                                equip_mode = False
                                equip_cursor = 0
                                break

                        # If a spell is selected, go to the spell equip options menu
                        if menu_pos < 5 and not equip_mode:
                                equip_mode = True

                        # Wait option
                        if menu_pos == 5:
                            return "Waited"

                        # Cancel option
                        if menu_pos == 6:
                            menu_flag = False

                    # X drops you out of the equip menu or cancels to the previous menu.
                    if  event.key == K_x :

                        if equip_mode:
                            equip_mode = False
                            equip_cursor = 0
                        else:
                            menu_flag = False

            if menu_flag:

                if update:
                    update = False

                    self.map.render_background()
                    self.map.render_all_units()
                    self.map.render_cursor()
                    self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
                    self.plot_stats()

                    self.map.engine.surface.blit(self.map.engine.spell_select_panel, (175, 70))

                    for index, spell in enumerate(self.spell_actions):

                        current_x = 190

                        # Draw spell icon
                        self.map.engine.surface.blit(small_icon_panel, (current_x, 85 + 50*index))

                        if spell:
                            spell_icon_position = (190+small_icon_panel.get_width()/2-self.map.engine.spell_type_icons['Healing'].get_width()/2,
                                                85+small_icon_panel.get_height()/2-self.map.engine.spell_type_icons['Healing'].get_height()/2+index*50)

                            if spell.type in ('healing', 'support'):
                                self.map.engine.surface.blit(self.map.engine.spell_type_icons['Healing'], spell_icon_position)
                            elif spell.type == "healingitem":
                                self.map.engine.surface.blit(self.map.engine.spell_type_icons['Item'], spell_icon_position)
                            else:
                                self.map.engine.surface.blit(self.map.engine.spell_type_icons[self.spell_actions[index].affinity], spell_icon_position)
                        current_x += small_icon_panel.get_width() + 10

                        # Draw spell name (on a grayed out panel if spell can't be used)
                        self.map.engine.surface.blit(options_panel, (current_x, 85 + 50*index))
                        self.map.engine.surface.blit(spell_names[index], (current_x + options_panel.get_width()/2 - spell_names[index].get_width()/2,
                                                                          85 + options_panel.get_height()/2 - spell_names[index].get_height()/2 + 50*index))

                        # Draws the uses for this spell
                        current_x += options_panel.get_width() + 10

                        self.map.engine.surface.blit(small_icon_panel, (current_x, 85 + 50*index))
                        if spell:
                            self.map.engine.surface.blit(spell_uses[index], (current_x + small_icon_panel.get_width()/2 - spell_uses[index].get_width()/2,
                                                                          85 + small_icon_panel.get_height()/2 - spell_uses[index].get_height()/2 + 50*index))

                        # Draws SC data
                        #   1. If the spell uses no SC / has no SC requirement, draw a blank
                        #   2. If the user does not have enough SC to use, draw the minimum SC needed.
                        #   3. If the user has enough SC to use, draw the SC cost
                        current_x += small_icon_panel.get_width() + 10
                        self.map.engine.surface.blit(sc_panel, (current_x, 85 + 50*index))

                        if spell_costs[index]:
                            self.map.engine.surface.blit(spell_costs[index], (current_x + sc_panel.get_width()/2 - spell_costs[index].get_width()/2,
                                                                          85 + sc_panel.get_height()/2 - spell_costs[index].get_height()/2 + 50*index))

                    # Draw the wait and cancel options
                    self.map.engine.surface.blit(options_panel, (190, 85 + 50*(index + 1)))
                    self.map.engine.surface.blit(wait_text, (190 + options_panel.get_width()/2 - wait_text.get_width()/2,
                                                               87 + 50*(index + 1) + options_panel.get_height()/2 - wait_text.get_height()/2 ))

                    self.map.engine.surface.blit(options_panel, (650 - options_panel.get_width(), 85 + 50*(index + 1)))
                    self.map.engine.surface.blit(cancel_text, (650 - options_panel.get_width()/2 - cancel_text.get_width()/2,
                                                               87 + 50*(index + 1) + options_panel.get_height()/2 - cancel_text.get_height()/2 ))

                    # Draw a solid border around the selection
                    if menu_pos < 5:
                            padlib_rounded_rect(self.map.engine.surface, selected_color, (239, 83+menu_pos*50, options_panel.get_width()+4, options_panel.get_height()+4), 5, 5)
                    elif menu_pos == 5:
                            padlib_rounded_rect(self.map.engine.surface, selected_color, (190 - 2, 83+menu_pos*50, options_panel.get_width()+4, options_panel.get_height()+4), 5, 5)
                    else:
                            padlib_rounded_rect(self.map.engine.surface, selected_color, (650 - options_panel.get_width() - 2, 83+(menu_pos-1)*50, options_panel.get_width()+4, options_panel.get_height()+4), 5, 5)

                    # If the equip menu is used, draw the equip panel at the bottom right of the selected spell
                    if equip_mode:
                        current_x = 580

                        # Draw the background panel
                        self.map.engine.surface.blit(equip_panel, (current_x, 90 + sc_panel.get_height() + 50*menu_pos))

                        # Draw the use option, normal color if usable, grayed out if unusable or empty
                        if menu_pos not in disabled_options and self.spell_actions[menu_pos]:
                            self.map.engine.surface.blit(sc_panel, (current_x + 10, 100 + sc_panel.get_height() + 50*menu_pos))
                        else:
                            self.map.engine.surface.blit(disabled_equip_panel, (current_x + 10, 100 + sc_panel.get_height() + 50*menu_pos))

                        self.map.engine.surface.blit(use_text, (current_x + 10 + sc_panel.get_width()/2 - use_text.get_width()/2,
                                                               102 + 1.5*sc_panel.get_height() + 50*menu_pos - cancel_text.get_height()/2 ))

                        # Draw the equip option. Any spell may be equipped even if it cannot be used.
                        self.map.engine.surface.blit(sc_panel, (current_x + 10, 95 + sc_panel.get_height() + 50*(menu_pos+1)))
                        self.map.engine.surface.blit(equip_text, (current_x + 10 + sc_panel.get_width()/2 - equip_text.get_width()/2,
                                                                98 + 1.5*sc_panel.get_height() + 50*(menu_pos + 1) - equip_text.get_height()/2 ))

                        # Draw a dark border around the current selection
                        padlib_rounded_rect(self.map.engine.surface, selected_color, (current_x + 8,
                                                                                       100 + sc_panel.get_height() + equip_cursor*45+ 50*(menu_pos),
                                                                                       sc_panel.get_width()+3,
                                                                                       sc_panel.get_height()), 5, 5)

                    pygame.display.flip()

            self.map.engine.clock.tick(60)

    def spell_loop_b(self):
        """
        # Function Name: Spell Loop B
        # Purpose: The unit's third level spell loop:
        #      Allows the player to select a target to use a spell on
        # Output: attacked_flag = True if an attack has been made, False if one has not been made
        """

        menu_flag = True
        action_confirmed = False
        self.map.framenum = 0

        target_list = []

        # Determine a list of available targets
        if self.spell_actions[self.equipped].type == 'attack':

            for target in self.map.team2:
                # checks if target is in range
                delta_pos = self.location_tile - target.location_tile
                target_in_range =  tuple(delta_pos) in self.spell_actions[self.equipped].validattacks
                if target_in_range:
                    target_list.append(target)

        else:

            for target in self.map.team1:
                # checks if target is in range
                delta_pos = self.location_tile - target.location_tile
                target_in_range =  tuple(delta_pos) in self.spell_actions[self.equipped].validattacks
                if target_in_range:

                    # Conditions for using a support spell:
                    # Any ally in range may be targetted.
                    if self.spell_actions[self.equipped].type == 'support':
                        target_list.append(target)

                    # For healing spells:
                    elif self.spell_actions[self.equipped].type in ('healing', 'healingitem'):

                        # If this spell heals HP, check that the target's HP is less than max HP
                        if self.spell_actions[self.equipped].effect and target.HP < target.maxHP:
                            target_list.append(target)

                        # If this spell cures status effects, check if target has any status effects
                        elif self.spell_actions[self.equipped].status_effects:
                            print self.spell_actions[self.equipped].status_effects, target.status.keys()


                            if any(status in self.spell_actions[self.equipped].status_effects for status in target.status.keys()):
                                target_list.append(target)




        current_target = 0
        if target_list:
            selected = target_list[0]
        else:
            selected = None
        if selected:
            self.map.center_on(selected, battle_board = True, lhs_unit = self, rhs_unit = selected, draw_range = self)

        # If there is only one valid target, skip straight to spell loop C
        if len(target_list) == 1:
            action_confirmed = self.spell_loop_c(selected)
            if action_confirmed:
                self.map.cursor_pos = Vector2(tuple(self.location_tile))
            return action_confirmed



        while menu_flag:

            arrowkeys = False
            if self.map.framenum == 10:
                self.map.framenum = 0
            self.map.framenum += 1

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if target_list:
                        if event.key == K_LEFT or event.key == K_UP:
                            if current_target == 0:
                                current_target = len(target_list) - 1
                            else:
                                current_target -= 1
                            selected = target_list[current_target]
                            self.map.center_on(selected, battle_board = True, lhs_unit = self, rhs_unit = selected, draw_range = self)

                        elif event.key == K_RIGHT or event.key == K_DOWN:
                            if current_target == len(target_list) - 1:
                                current_target = 0
                            else:
                                current_target += 1

                            selected = target_list[current_target]
                            self.map.center_on(selected, battle_board = True, lhs_unit = self, rhs_unit = selected, draw_range = self)

                    if event.key == K_x:
                        self.map.center_on(self)
                        return action_confirmed
                    if event.key == K_z or event.key == K_RETURN:

                        # If a target is found
                        if selected:
                            action_confirmed = self.spell_loop_c(selected)
                            if action_confirmed:
                                self.map.cursor_pos = Vector2(tuple(self.location_tile))
                                return action_confirmed

            # Plots the valid attack tiles
            if menu_flag:

                pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                           %(self.map.cursor_pos.x, self.map.cursor_pos.y, self.map.screen_shift.x, self.map.screen_shift.y))

                self.map.render_background()
                self.plot_attacks()

                self.map.render_all_units()
                self.map.render_cursor()
                self.map.engine.surface.blit(self.map.engine.battle_board, (0, 490))
                self.plot_stats()

                # Display for combat statistics
                # Checks if there is a unit is selected, and if there is, plots the unit's data.
                if selected:
                    #Plots predictor system
                    selected.plot_stats(rhs = True)
                    self.plot_predictor(selected)


                pygame.display.flip()
                self.map.engine.clock.tick(60)



    def spell_loop_c(self, target):

        """
        # Function Name: Spell Loop C
        # Purpose: Confirmation of action.
        # Input: selected = The target the spell will be cast to
        """

        menu_flag = True
        menu_pos = 0

        text_confirm = self.map.engine.section_font.render("Confirm", True, (0, 0, 0))
        text_cancel = self.map.engine.section_font.render("Cancel", True, (0, 0, 0))

        action_confirmed = False

        confirm_panel = get_ui_panel((150, 105), border_color, (220, 220, 70))
        options_panel = get_ui_panel((130, 41), border_color, panel_color)

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
                        if menu_pos == 0:
                            menu_pos = 1
                        else:
                            menu_pos = 0

                    if event.key == K_x:
                        menu_flag = False

                    if event.key == K_z or event.key == K_RETURN:

                        if menu_pos == 0:
                            self.spell_actions[self.equipped].action(self, target)
                            menu_flag = False

                            self.map.cursor_pos = Vector2(tuple(self.location_tile))
                            self.map.center_on(self)

                            action_confirmed = True
                            return action_confirmed

                        if menu_pos == 1:
                            menu_flag = False
                            return action_confirmed


            # Plots the valid attack tiles
            if menu_flag:

                pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                           %(self.map.cursor_pos.x, self.map.cursor_pos.y, self.map.screen_shift.x, self.map.screen_shift.y))

                self.map.render_background()
                self.plot_attacks()

                self.map.render_all_units()
                self.map.render_cursor()
                self.map.engine.surface.blit(self.map.engine.battle_board, (0, 490))
                self.plot_stats()

                # Display for combat statistics
                target.plot_stats(rhs = True)
                self.plot_predictor(target)

                # If unit is on the one side of the screen currently, draw the menu on the opposite side.
                if self.location_pixel.x - self.map.screen_shift.x*35 > 420:
                    menu_x = 35 + 185
                else:
                    menu_x = 840 - self.map.engine.vertical_panel.get_width() - 10 - confirm_panel.get_width()

                self.map.engine.surface.blit(confirm_panel, (menu_x, 285))
                self.map.engine.surface.blit(options_panel, (menu_x + 10, 295))
                self.map.engine.surface.blit(text_confirm, (menu_x + 10 + options_panel.get_width()/2 - text_confirm.get_width()/2,
                                                            297 + options_panel.get_height()/2 - text_confirm.get_height()/2))

                self.map.engine.surface.blit(options_panel, (menu_x + 10, 340))
                self.map.engine.surface.blit(text_cancel, (menu_x + 10 + options_panel.get_width()/2 - text_cancel.get_width()/2,
                                                            342 + options_panel.get_height()/2 - text_cancel.get_height()/2))



                # Plots selection border
                padlib_rounded_rect(self.map.engine.surface, selected_color, (menu_x + 8,
                                                                               295 + menu_pos*45,
                                                                               options_panel.get_width()+3,
                                                                               options_panel.get_height()), 5, 5)

                pygame.display.flip()
                self.map.engine.clock.tick(60)

    def stats_loop(self):
        """
        Function name: Stats loop

        Purpose: displays a basic overview of a unit's stats

        Output: Arrow keys so switching between units and stats data screens can be done

        """

        menu_flag = True

        update_screen = True


        text_name = self.map.engine.title_font.render(self.name, True,  (0,0,0))
        if text_name.get_width() > 160:
            text_name = self.map.engine.section_font.render(self.name, True,  (0,0,0))



        text_level1 = self.map.engine.section_font.render("Lv.", True, (0,0,0))
        text_level2 = self.map.engine.data_font.render("%d"%self.level, True, (0,0,0))

        text_hp = self.map.engine.section_font.render("HP", True, (0, 0, 0))
        text_hp_value = self.map.engine.data_font.render('%d / %d'%(self.HP, self.maxHP), True, (255,255,255))

        text_exp = self.map.engine.section_font.render("EXP", True, (0, 0, 0))
        text_exp_value = self.map.engine.data_font.render('%d / 100'%(self.exp), True, (255,255,255))

        text_sc = self.map.engine.section_font.render("SC", True, (0, 0, 0))
        text_sc_value = self.map.engine.data_font.render('%d / 900'%(self.spirit), True, (255,255,255))

        text_move = self.map.engine.section_font.render("MOV", True, (0,0,0))
        text_move_value = self.map.engine.data_font.render('%d'%self.moves, True, (0,0,0))

        text_talent = self.map.engine.section_font.render("Talent", True, (0, 0, 0))

        text_stats = self.map.engine.section_font.render("Stats", True, (0, 0, 0))
        text_spells_footer = self.map.engine.section_font.render("Spells", True, (0, 0, 0))

        meter_width = 265

        name_panel = get_ui_panel((190, 50), border_color, panel_color)
        stat_panel = get_ui_panel((100, 35), border_color, panel_color)
        small_icon_panel = get_ui_panel((41, 41), border_color, panel_color)
        spell_name_panel = get_ui_panel((230, 35), border_color, panel_color)
        trait_name_panel = get_ui_panel((275, 35), border_color, panel_color)

        stat_names = [self.map.engine.section_font.render(item, True, (0, 0, 0))
                      for item in ('STR', 'MAG', 'ACC','DEF', 'MDF', 'AGL')]
        stat_values = [self.map.engine.data_font.render(str(value), True,(0, 0, 0 ))
                       for value in (self.STR, self.MAG, self.ACC, self.DEF, self.MDEF, self.AGL)  ]

        text_spells = self.map.engine.section_font.render("Spell Actions", True, (0,0,0))
        text_spell_list = []
        text_uses_list = []
        for spell in self.spell_actions:
            if spell:
                text_spell_list.append(self.map.engine.data_font.render(spell.namesuffix, True, (0, 0, 0)))
                text_uses_list.append(self.map.engine.data_font.render(str(spell.livesleft), True, (0, 0, 0)))
            else:
                text_spell_list.append(self.map.engine.data_font.render("Empty", True, (150, 150, 150)))
                text_uses_list.append(None)

        text_traits = self.map.engine.section_font.render("Traits", True, (0,0,0))


        text_trait_names = []
        for trait in self.traits:
            if trait:
                text_trait_names.append(self.map.engine.data_font.render(trait.name, True, (0, 0, 0)) )
            else:
                text_trait_names.append(self.map.engine.data_font.render("Empty", True, (150, 150, 150)) )


        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN and event.key in (K_x, K_DOWN, K_UP, K_LEFT, K_RIGHT):
                    return event


            if update_screen:
                self.map.engine.surface.blit(self.map.engine.stats_bg, (0, 0))
                self.map.engine.surface.blit(self.av, (50, 50))
                self.map.engine.surface.blit(name_panel, (185, 65))
                self.map.engine.surface.blit(text_name, (185 + name_panel.get_width()/2 - text_name.get_width()/2,
                                                         67 + name_panel.get_height()/2 - text_name.get_height()/2))

                # Stats / Traits / Spells current page indicator
                self.map.engine.surface.blit(stat_panel, (-10, 600))
                self.map.engine.surface.blit(text_traits, (-10 + stat_panel.get_width()/2 - text_traits.get_width()/2, 603))
                self.map.engine.surface.blit(stat_panel, (840/2 - stat_panel.get_width()/2, 600))
                padlib_rounded_rect(self.map.engine.surface, selected_color, (840/2 - stat_panel.get_width()/2, 600,
                    stat_panel.get_width(), stat_panel.get_height()), 5, 4)
                self.map.engine.surface.blit(text_stats, (840/2 - text_stats.get_width()/2, 603))

                self.map.engine.surface.blit(stat_panel, (840 - stat_panel.get_width() + 10, 600))
                self.map.engine.surface.blit(text_spells_footer, (846 - stat_panel.get_width()/2 - text_spells_footer.get_width()/2, 603))


                # Level
                self.map.engine.surface.blit(stat_panel, (230, 120))
                self.map.engine.surface.blit(text_level1, (245, 122 + stat_panel.get_height()/2 - text_level1.get_height()/2))
                self.map.engine.surface.blit(text_level2, (215+stat_panel.get_width()-text_level2.get_width(),
                                                           120+stat_panel.get_height()/2-text_level2.get_height()/2))

                # HP meter
                self.map.engine.surface.blit(text_hp, (50,  180 + 25/2 - text_hp.get_height()/2))

                # Draws the outline
                self.map.engine.surface.blit(self.map.engine.meter_outline, (100, 180), (0, 0, meter_width+2, 25))
                self.map.engine.surface.blit(self.map.engine.meter_outline, (102 + meter_width, 180), (298, 0,  2, 25))

                hp_meter_width = int(meter_width*float(self.HP)/self.maxHP)

                # Draws a black background, the meter, and the text value
                pygame.draw.rect(self.map.engine.surface, (0, 0, 0), (102, 182, meter_width, 21))
                self.map.engine.surface.blit(self.map.engine.big_hp_meter, (102, 182), (0, 0,  hp_meter_width, 21))
                self.map.engine.surface.blit(text_hp_value, (102+meter_width/2-text_hp_value.get_width()/2, 177))

                # EXP meter
                self.map.engine.surface.blit(text_exp, (50, 210 + 25/2 - text_exp.get_height()/2))
                exp_meter_width = int(meter_width*float(self.exp)/100)
                self.map.engine.surface.blit(self.map.engine.meter_outline, (100, 210), (0, 0, meter_width+2, 25))
                self.map.engine.surface.blit(self.map.engine.meter_outline, (102 + meter_width, 210), (298, 0,  2, 25))
                pygame.draw.rect(self.map.engine.surface, (0, 0, 0), (102, 212, meter_width, 21))
                self.map.engine.surface.blit(self.map.engine.big_exp_meter, (102, 212), (0, 0,  exp_meter_width, 25))
                self.map.engine.surface.blit(text_exp_value, (100+meter_width/2-text_exp_value.get_width()/2, 207))

                # Spirit meter
                self.map.engine.surface.blit(text_sc, (50, 240 + + 25/2 - text_sc.get_height()/2))

                self.map.engine.surface.blit(self.map.engine.meter_outline, (100, 240), (0, 0, meter_width+2, 25))
                self.map.engine.surface.blit(self.map.engine.meter_outline, (102 + meter_width, 240), (298, 0,  2, 25))
                pygame.draw.rect(self.map.engine.surface, (0, 0, 0), (102, 242, meter_width, 21))
                sc_meter_width = int(meter_width*float(self.spirit)/900)
                self.map.engine.surface.blit(self.map.engine.big_sc_meter, (102, 242), (0, 0,  sc_meter_width, 25))
                self.map.engine.surface.blit(text_sc_value, (100+meter_width/2-text_sc_value.get_width()/2, 237))

                for x in xrange(0,3):
                    for y in xrange(0,2):

                        self.map.engine.surface.blit(self.map.engine.stats_icons, (75 + 110*x, 275+110*y), (50*x, 50*y, 50, 50))

                        self.map.engine.surface.blit(stat_panel, (50+110*x, 335+110*y))
                        index = x+3*y
                        self.map.engine.surface.blit(stat_names[index], (60+110*x, 340+110*y))

                        self.map.engine.surface.blit(stat_values[index],
                                                     (40+110*x+stat_panel.get_width()-stat_values[index].get_width(),
                                                      337+110*y))

                # Movement range
                self.map.engine.surface.blit(self.map.engine.movement_range_icon, (125, 495))
                self.map.engine.surface.blit(stat_panel, (100, 555))
                self.map.engine.surface.blit(text_move, (110, 560))
                self.map.engine.surface.blit(text_move_value, (90+stat_panel.get_width()-text_move_value.get_width(), 557))

                self.map.engine.surface.blit(stat_values[index],
                                             (40+110*x+stat_panel.get_width()-stat_values[index].get_width(),
                                              337+110*y))

                self.map.engine.surface.blit(self.map.engine.spell_type_icons_big[self.spell_preference], (235, 495))
                self.map.engine.surface.blit(stat_panel, (210, 555))
                self.map.engine.surface.blit(text_talent, (210+stat_panel.get_width()/2-text_talent.get_width()/2, 560))

                # Spells
                self.map.engine.surface.blit(text_spells, (455+175-text_spells.get_width()/2, 50))
                for index in xrange(0,5):



                    # Draws 3 boxes: type, name, and uses
                    self.map.engine.surface.blit(small_icon_panel, (470, 98+45*index))
                    self.map.engine.surface.blit(spell_name_panel, (515, 100+45*index))
                    self.map.engine.surface.blit(small_icon_panel, (750, 98+45*index))

                    # If this spell is equpped, draw a box around it
                    if index == self.equipped:

                        padlib_rounded_rect(self.map.engine.surface, selected_color, (515, 100+45*index, 230, 35), 5, 4)

                    # Draw the spell type, name, and uses remaining
                    self.map.engine.surface.blit(text_spell_list[index], (515+spell_name_panel.get_width()/2-text_spell_list[index].get_width()/2, 102+45*index))
                    if self.spell_actions[index]:
                        spell_icon_position = (470+small_icon_panel.get_width()/2-self.map.engine.spell_type_icons['Healing'].get_width()/2,
                                            98+small_icon_panel.get_height()/2-self.map.engine.spell_type_icons['Healing'].get_height()/2+index*45)

                        if self.spell_actions[index].type in ('healing', 'support'):
                            self.map.engine.surface.blit(self.map.engine.spell_type_icons['Healing'], spell_icon_position)
                        elif self.spell_actions[index].type == "healingitem":
                            self.map.engine.surface.blit(self.map.engine.spell_type_icons['Item'], spell_icon_position)
                        else:
                            self.map.engine.surface.blit(self.map.engine.spell_type_icons[self.spell_actions[index].affinity], spell_icon_position)


                        self.map.engine.surface.blit(text_uses_list[index], (751+small_icon_panel.get_width()/2-text_uses_list[index].get_width()/2, 102+45*index))


                self.map.engine.surface.blit(text_traits, (455+175-text_traits.get_width()/2, 330))

                for index, trait_name in enumerate(text_trait_names):

                    # Draws 2 boxes: type, name
                    self.map.engine.surface.blit(small_icon_panel, (468, 360+45*index))
                    self.map.engine.surface.blit(trait_name_panel, (515, 362+45*index))

                    if self.traits[index]:
                        trait_icon = self.map.engine.trait_type_icons[self.traits[index].variation]
                        trait_icon_position = (468 + small_icon_panel.get_width()/2 - trait_icon.get_width()/2,
                                                360 + small_icon_panel.get_height()/2 - trait_icon.get_height()/2 + 45*index)

                        self.map.engine.surface.blit(trait_icon, trait_icon_position)



                    self.map.engine.surface.blit(trait_name, (515+trait_name_panel.get_width()/2-trait_name.get_width()/2, 363+45*index))

                pygame.display.flip()
                update_screen = False

            self.map.engine.clock.tick(60)

    def traits_stats_loop(self):

        """
        function name: traits_stats_loop
        Purpose: Shows the traits of this unit on a static screen
        """

        text_stats = self.map.engine.section_font.render("Stats", True, (0, 0, 0))
        text_spells_footer = self.map.engine.section_font.render("Spells", True, (0, 0, 0))
        text_traits = self.map.engine.section_font.render("Traits", True, (0,0,0))

        stat_panel = get_ui_panel((100, 35), border_color, panel_color)

        text_title = self.map.engine.title_font.render("Traits", True, (0,0,0))

        text_trait_names = []
        for trait in self.traits:
            if trait:
                text_trait_names.append(self.map.engine.section_font.render(trait.name, True, (0, 0, 0)) )
            else:
                text_trait_names.append(self.map.engine.section_font.render("Empty", True, (150, 150, 150)) )


        selected_panel = get_ui_panel((320, 45), border_color, panel_color)
        unselected_panel = get_ui_panel((280, 40), border_color, panel_color)

        menu_flag = True
        update = True
        selected_trait = 0
        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN and event.key in (K_x, K_LEFT, K_RIGHT):
                    return event
                if event.type == KEYDOWN and event.key in (K_UP, K_DOWN):
                    if event.key == K_UP:
                        if selected_trait == 0:
                            selected_trait = len(self.spell_actions) - 1
                        else:
                            selected_trait -= 1
                        update = True
                    elif event.key == K_DOWN:
                        if selected_trait == len(self.spell_actions) - 1:
                            selected_trait = 0
                        else:
                            selected_trait += 1
                        update = True

            if update:
                self.map.engine.surface.blit(self.map.engine.stats_bg, (0,0))

                # Stats / Traits / Spells current page indicator
                self.map.engine.surface.blit(stat_panel, (-10, 600))
                self.map.engine.surface.blit(text_spells_footer, (-10 + stat_panel.get_width()/2 - text_spells_footer.get_width()/2, 603))
                self.map.engine.surface.blit(stat_panel, (840/2 - stat_panel.get_width()/2, 600))
                padlib_rounded_rect(self.map.engine.surface, selected_color, (840/2 - stat_panel.get_width()/2, 600,
                                                                              stat_panel.get_width(), stat_panel.get_height()), 5, 4)
                self.map.engine.surface.blit(text_traits, (840/2 - text_traits.get_width()/2, 603))

                self.map.engine.surface.blit(stat_panel, (840 - stat_panel.get_width() + 10, 600))
                self.map.engine.surface.blit(text_stats, (846 - stat_panel.get_width()/2 - text_stats.get_width()/2, 603))

                self.map.engine.surface.blit(text_title, (35 + 700/4 - text_title.get_width()/2, 50))

                for index, spell in enumerate(self.traits):

                    # Use a bigger box if trait is being examined
                    if selected_trait == index:
                        name_position = (50+selected_panel.get_width()/2-text_trait_names[index].get_width()/2,
                                         108+selected_panel.get_height()/2-text_trait_names[index].get_height()/2+70*index)
                        self.map.engine.surface.blit(selected_panel, (50, 105+ 70*index))
                        self.map.engine.surface.blit(text_trait_names[index], name_position)

                    else:
                        name_position = (70+unselected_panel.get_width()/2-text_trait_names[index].get_width()/2,
                                         106+unselected_panel.get_height()/2-text_trait_names[index].get_height()/2+70*index)
                        self.map.engine.surface.blit(unselected_panel, (70, 105+ 70*index))
                        self.map.engine.surface.blit(text_trait_names[index], name_position)

                if self.traits[selected_trait]:
                    self.map.engine.draw_trait_data(self.traits[selected_trait])

                pygame.display.flip()
                update = False

            self.map.engine.clock.tick()


    def spell_stats_loop(self):

        """
        function name: spell_stats_loop
        Purpose: Shows the spells of this unit on a static screen

        """


        text_stats = self.map.engine.section_font.render("Stats", True, (0, 0, 0))
        text_spells_footer = self.map.engine.section_font.render("Spells", True, (0, 0, 0))
        text_traits = self.map.engine.section_font.render("Traits", True, (0,0,0))

        stat_panel = get_ui_panel((100, 35), border_color, panel_color)
        unselected_panel = get_ui_panel((280, 50), border_color, panel_color)

        text_title = self.map.engine.title_font.render("Spell Actions", True, (0,0,0))


        menu_flag = True
        update = True
        selected_spell = 0

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN and event.key in (K_x, K_LEFT, K_RIGHT):
                    return event
                if event.type == KEYDOWN and event.key in (K_UP, K_DOWN):
                    if event.key == K_UP:
                        if selected_spell == 0:
                            selected_spell = len(self.spell_actions) - 1
                        else:
                            selected_spell -= 1
                        update = True
                    elif event.key == K_DOWN:
                        if selected_spell == len(self.spell_actions) - 1:
                            selected_spell = 0
                        else:
                            selected_spell += 1
                        update = True



            if update:
                self.map.engine.surface.blit(self.map.engine.stats_bg, (0,0))

                # Stats / Traits / Spells current page indicator
                self.map.engine.surface.blit(stat_panel, (-10, 600))
                self.map.engine.surface.blit(text_stats, (-10 + stat_panel.get_width()/2 - text_stats.get_width()/2, 603))
                self.map.engine.surface.blit(stat_panel, (840/2 - stat_panel.get_width()/2, 600))
                padlib_rounded_rect(self.map.engine.surface, selected_color, (840/2 - stat_panel.get_width()/2, 600,
                                                                              stat_panel.get_width(), stat_panel.get_height()), 5, 4)
                self.map.engine.surface.blit(text_spells_footer, (840/2 - text_spells_footer.get_width()/2, 603))

                self.map.engine.surface.blit(stat_panel, (840 - stat_panel.get_width() + 10, 600))
                self.map.engine.surface.blit(text_traits, (846 - stat_panel.get_width()/2 - text_traits.get_width()/2, 603))

                self.map.engine.surface.blit(text_title, (35 + 700/4 - text_title.get_width()/2, 50))
                self.draw_spell_select()
                padlib_rounded_rect(self.map.engine.surface, selected_color,
                            (108, 103+60*selected_spell, 264, 44), 6, 5)

                if self.spell_actions[selected_spell]:
                    self.map.engine.draw_spell_action_data(self.spell_actions[selected_spell])

                pygame.display.flip()
                update = False

            self.map.engine.clock.tick()

    def get_text_trait_data(self):
        """
        # Function name: get_text_trait_data
        # Purpose: From a unit's traits, returns a list of text objects with the data
        # Inputs: None
        # Outputs: text_trait_data - a list containing the text objects for the unit's traits
        """

        text_trait_data = [self.map.engine.get_text_selected_trait(trait) for trait in self.traits]

        return text_trait_data

    def update_trait_learning_data(self):

        # Update Branch 0 and 1
        if self.trait_learning_catalog:
            for branch in xrange(0, 2):
                for index, trait_data in enumerate(self.trait_learning_catalog[branch][1]):
                    level, trait = trait_data
                    if self.level >= level:
                        self.reserve_traits[branch][index] = trait
                    else:
                        self.reserve_traits[branch][index] = None

            # Updates equipped traits
            for index, trait in enumerate(self.traits):
                # Case 1: Unit has a trait equipped, but no trait available in branches
                if trait and not self.reserve_traits[0][index] and not self.reserve_traits[1][index]:
                    self.traits[index] = None

                # Case 2: Trait does not match either of the two branch options. Replace with branch 0
                elif trait and trait.name != self.reserve_traits[0][index].name and trait.name != self.reserve_traits[1][index].name:
                    print "Trait does not match existing branch"
                    self.add_trait(self.reserve_traits[0][index])

                # Case 3: Trait is empty. Assign trait branch 0's trait to unit
                elif not trait and self.reserve_traits[0][index]:
                    self.add_trait(self.reserve_traits[0][index])




    def spell_swap_menu(self):
        """
        # Function name: spell_swap_menu
        # Purpose: Allows spell to be swapped out from unit
        """

        spell_panel = get_ui_panel((260, 40), border_color, panel_color)
        confirm_panel = get_ui_panel((110, 160), border_color,  (220, 220, 70) )
        confirm_option_panel = get_ui_panel((90, 35), border_color, panel_color )
        dis_option_panel = get_ui_panel((90, 35), border_color, disabled_color )


        text_title = self.map.engine.title_font.render("Set Spell Actions", True, (0,0,0))
        confirm_options = (self.map.engine.message_font.render("Change", True, (0,0,0)),
                           self.map.engine.message_font.render("Equip", True, (0,0,0)),
                           self.map.engine.message_font.render("Remove", True, (0,0,0)),
                            )

        text_cancel = self.map.engine.message_font.render("Cancel", True, (0, 0, 0))


        menu_flag = True
        update = True
        menu_pos = 0
        confirm_mode = False
        confirm_pos = 0


        while menu_flag:
            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP or event.key == K_LEFT:

                        # If in the sub-menu, scroll down among the three possible sub-options
                        if confirm_mode:
                            if confirm_pos > 0:
                                confirm_pos -= 1
                            elif confirm_pos == 0:
                                confirm_pos = 2

                        # Otherwise, scroll down among the possible spell options + cancel
                        else:
                            if menu_pos > 0:
                                menu_pos -= 1
                            elif menu_pos == 0:
                                menu_pos = 5

                        update = True

                    if event.key == K_DOWN or event.key == K_RIGHT:


                        if confirm_mode:
                            if confirm_pos < 2:
                                confirm_pos += 1
                            elif confirm_pos == 2:
                                confirm_pos = 0
                        else:
                            if menu_pos < 5:
                                menu_pos += 1
                            elif menu_pos == 5:
                                menu_pos = 0

                        update = True


                    if event.key == K_z  or event.key == K_RETURN:
                        if menu_pos < 5:

                            # goes into the sub menu
                            if not confirm_mode:
                                confirm_mode = True
                                confirm_pos = 0
                                update = True

                            else:

                                # Switches the spell for another one
                                if confirm_pos == 0:


                                    selection_result = self.map.engine.spell_swap_inventory(self)
                                    if selection_result:
                                        # Append the current spell to the inventory if it is an a real spell
                                        if self.spell_actions[menu_pos]:
                                            self.map.engine.player.add_item(self.spell_actions[menu_pos])
                                        # Replace the selected spell into the unit's slot
                                        self.spell_actions[menu_pos] = selection_result[0]

                                        selection_result[0].get_attack_range(self)

                                        confirm_mode = False

                                    update = True


                                # Equips the spell
                                elif confirm_pos == 1:

                                    if self.spell_actions[menu_pos]:
                                        self.equipped = menu_pos
                                    update = True
                                    confirm_mode = False

                                # Unequips the spell
                                else:
                                    if self.spell_actions[menu_pos]:
                                        self.map.engine.player.add_item(self.spell_actions[menu_pos])
                                        # Replace the selected spell into the unit's slot with None
                                        self.spell_actions[menu_pos] = None

                                    update = True
                                    confirm_mode = False

                        elif menu_pos == 5:
                            return

                    if event.key == K_x:
                        if confirm_mode:
                            confirm_mode = False
                            update = True
                        else:
                            return

            if menu_flag:

                if update:
                    update = False


                    # Spell_data
                    self.map.engine.surface.blit(self.map.engine.stats_bg, (0, 0))
                    self.map.engine.surface.blit(text_title, (35 + 700/4 - text_title.get_width()/2, 50))
                    self.draw_spell_select()

                    # Draw cancel button
                    self.map.engine.surface.blit(spell_panel, (80, 405))
                    self.map.engine.surface.blit(text_cancel, (80 + spell_panel.get_width()/2 - text_cancel.get_width()/2,
                                                               405 + spell_panel.get_height()/2 - text_cancel.get_height()/2))

                    # Data display
                    if menu_pos < 5 and self.spell_actions[menu_pos]:
                        self.map.engine.draw_spell_action_data(self.spell_actions[menu_pos])

                    # Draw cursor
                    if menu_pos < 5:
                        padlib_rounded_rect(self.map.engine.surface, selected_color,
                            (108, 103+60*menu_pos, spell_panel.get_width() + 4, spell_panel.get_height()+4), 6, 5)
                    else:
                        padlib_rounded_rect(self.map.engine.surface, selected_color,
                            (78, 403, spell_panel.get_width() + 4, spell_panel.get_height()+4), 6, 5)

                    # If in the sub menu, draw the sub menu
                    if confirm_mode:

                        # Draw submenu options
                        self.map.engine.surface.blit(confirm_panel, (355, 90 + 60*menu_pos ))
                        for index, text_confirm in enumerate(confirm_options):

                            # If spell slot is empty, show a grayed out box for unequip and equip
                            if index < 1 or self.spell_actions[menu_pos]:
                                self.map.engine.surface.blit(confirm_option_panel, (365, 100 + 50*index + 60*menu_pos ))
                            else:
                                self.map.engine.surface.blit(dis_option_panel, (365, 100 + 50*index + 60*menu_pos ))

                            self.map.engine.surface.blit(text_confirm, (365 + confirm_option_panel.get_width()/2 - text_confirm.get_width()/2,
                                                                        100 + confirm_option_panel.get_height()/2 - text_confirm.get_height()/2 + 50*index + 60*menu_pos))
                        # Draw cursor for submenu
                        padlib_rounded_rect(self.map.engine.surface, selected_color,
                                                    (363, 98 + 50*confirm_pos + 60*menu_pos, confirm_option_panel.get_width()+4, confirm_option_panel.get_height()+4), 6, 5)


                    pygame.display.flip()
                self.map.engine.clock.tick(60)


    def draw_spell_select(self):

        """
        draw_spell_select

        Purpose: Draw a list of spells and which one is equipped

        """

        unselected_panel = get_ui_panel((260, 40), border_color, panel_color)
        small_icon_panel = get_ui_panel((40,40), border_color, panel_color)

        # Text of the letter E represents currently equipped spell
        text_E = self.map.engine.section_font.render("E", True, (0, 0, 0))


        # Generates names for available spells on this unit
        text_spell_list = []
        for spell in self.spell_actions:
            if spell:
                text_spell_list.append(self.map.engine.message_font.render(spell.namesuffix, True, (0, 0, 0)))
            else:
                text_spell_list.append(self.map.engine.message_font.render("Empty", True, (150, 150, 150)))

        # Plots the spells
        for index, option_name in enumerate(text_spell_list):
            name_position = (110+unselected_panel.get_width()/2-option_name.get_width()/2,
                             105+unselected_panel.get_height()/2-option_name.get_height()/2+60*index)
            self.map.engine.surface.blit(small_icon_panel, (50, 105+ 60*index))
            self.map.engine.surface.blit(unselected_panel, (110, 105+ 60*index))
            self.map.engine.surface.blit(option_name, name_position)

        # Plots the one which is equipped
        self.map.engine.surface.blit(text_E, (50 + small_icon_panel.get_width()/2 - text_E.get_width()/2,
                                              105 + small_icon_panel.get_height()/2 - text_E.get_height()/2 + 60*self.equipped))
        padlib_rounded_rect(self.map.engine.surface, selected_color,
                            (48, 103+60*self.equipped, small_icon_panel.get_width()+4, small_icon_panel.get_height()+4), 6, 5)

    def trait_swap_menu(self):
        """
        # Function Name: trait swap menu
        # Purpose: Allows selection of traits to be swaped in and out of a unit's
        #   reserved traits
        """

        menu_flag = True
        menu_pos = 0

        text_branch0 = self.map.engine.speaker_font.render(self.trait_learning_catalog[0][0], True, (0, 0, 0))
        text_branch1 = self.map.engine.speaker_font.render(self.trait_learning_catalog[1][0], True, (0, 0, 0))

        small_icon_panel = get_ui_panel((41, 41), border_color, panel_color)
        enabled_panel = get_ui_panel((270, 40), border_color, panel_color)
        disabled_panel = get_ui_panel((270, 40), border_color, disabled_color)
        description_panel = get_ui_panel((310, 120), border_color, panel_color)

        trait_type_panel = get_ui_panel((260, 35), border_color, panel_color)
        full_width_panel = get_ui_panel((310, 40), border_color, panel_color)

        branch_data = []
        for index, branch in enumerate(self.trait_learning_catalog):
            branch_data.append([])
            for trait in branch[1]:
                # Unit can use this trait
                if trait and self.level >= trait[0]:

                    branch_display_info = []

                    current_trait = trait[1]

                    # Trait name
                    branch_display_info.append(self.map.engine.section_font.render(current_trait.name, True, (0, 0, 0)))

                    # Trait icon
                    branch_display_info.append(self.map.engine.trait_type_icons[current_trait.variation])

                    # Trait Type
                    if current_trait.variation == 'Support':
                        branch_display_info.append(self.map.engine.message_font.render('Support Trait', True, (0, 0, 0)))
                    elif current_trait.variation == 'Trait Skill':
                        branch_display_info.append(self.map.engine.message_font.render('Trait Skill', True, (0, 0, 0)))
                    elif current_trait.variation == 'Proximity':
                        branch_display_info.append(self.map.engine.message_font.render('Proximity Trait', True, (0, 0, 0)))
                    else:
                        branch_display_info.append(self.map.engine.message_font.render('Other', True, (0, 0, 0)))

                    # Trait description
                    branch_display_info.append(current_trait.desc)

                    branch_data[index].append(branch_display_info)

                # Unit not high level enough to use this trait
                elif trait and self.level < trait[0]:
                    branch_data[index].append(None)

        # Determines what the position of the traits are.
        def update_equipped_traits():
            trait_indicator_pos = []
            for index, trait in enumerate(self.traits):
                # Trait is in branch 0
                if trait and trait.name == self.reserve_traits[0][index].name:
                    trait_indicator_pos.append(0)

                # Trait is in branch 1
                elif trait and trait.name == self.reserve_traits[1][index].name:
                    trait_indicator_pos.append(1)
                else:
                    pass
            return trait_indicator_pos

        trait_indicator_pos = update_equipped_traits()

        # Determines the max number of available branch slots available
        max_traits = len([trait_data for trait_data in branch_data[0] if trait_data])

        update = True
        while menu_flag:
            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if ( event.key == K_UP):
                        if menu_pos > 0:
                            menu_pos -= 1
                        elif menu_pos == 0:
                            menu_pos = max_traits - 1
                        update = True
                    if ( event.key == K_DOWN):
                        if menu_pos < max_traits - 1:
                            menu_pos += 1
                        elif menu_pos == max_traits -1:
                            menu_pos = 0
                        update = True
                    if (event.key == K_LEFT or event.key == K_RIGHT):
                        if self.traits[menu_pos]:
                            self.swap_trait(menu_pos)
                            trait_indicator_pos = update_equipped_traits()
                            update = True


                    if event.key == K_x:
                        menu_flag = False

            if menu_flag:

                # Saves CPU. Only draws if needed.
                if update:
                    self.map.engine.surface.blit(self.map.engine.stats_bg, (0, 0))

                    # Branch 0 Traits
                    self.map.engine.surface.blit(full_width_panel, (210 - full_width_panel.get_width()/2, 15))
                    self.map.engine.surface.blit(text_branch0,(210-text_branch0.get_width()/2,
                                                               15 + full_width_panel.get_height()/2 - text_branch0.get_height()/2))

                    # Draws the trait data for branch 0
                    for index, trait_data in enumerate(branch_data[0]):

                        # Checks if trait branch is available
                        if trait_data:

                            # Draws the trait name
                            if trait_indicator_pos[index] == 0:
                                self.map.engine.surface.blit(enabled_panel, (100 ,70+50*index))
                            else:
                                self.map.engine.surface.blit(disabled_panel, (100, 70+50*index))

                            self.map.engine.surface.blit(trait_data[0], (100 + enabled_panel.get_width()/2 - trait_data[0].get_width()/2,
                                                                         72 + enabled_panel.get_height()/2 - trait_data[0].get_height()/2 + 50*index))

                            # Draws the icon for the trait
                            self.map.engine.surface.blit(small_icon_panel, (50,70+50*index))
                            self.map.engine.surface.blit(trait_data[1], (50 + small_icon_panel.get_width()/2 - trait_data[1].get_width()/2,
                                                                         70 +  small_icon_panel.get_height()/2 - trait_data[1].get_height()/2 + 50*index))

                        else:

                            # If no trait available, draw just the panels
                            self.map.engine.surface.blit(small_icon_panel, (50,70+50*index))
                            self.map.engine.surface.blit(enabled_panel, (100 ,70+50*index))


                    # Branch 1 Traits
                    self.map.engine.surface.blit(full_width_panel, (630 - full_width_panel.get_width()/2, 15))
                    self.map.engine.surface.blit(text_branch1,(630-text_branch1.get_width()/2,
                                                               15 + full_width_panel.get_height()/2 - text_branch1.get_height()/2))

                    # Draws the trait data for branch 1
                    for index, trait_data in enumerate(branch_data[1]):


                        # Checks if trait branch is available
                        if trait_data:

                            # Draws the trait name
                            if trait_indicator_pos[index] == 1:
                                self.map.engine.surface.blit(enabled_panel, (520 ,70+50*index))
                            else:
                                self.map.engine.surface.blit(disabled_panel, (520, 70+50*index))

                            self.map.engine.surface.blit(trait_data[0], (520 + enabled_panel.get_width()/2 - trait_data[0].get_width()/2,
                                                                         72 + enabled_panel.get_height()/2 - trait_data[0].get_height()/2 + 50*index))

                            # Draws the icon for the trait
                            self.map.engine.surface.blit(small_icon_panel, (470,70+50*index))
                            self.map.engine.surface.blit(trait_data[1], (470 + small_icon_panel.get_width()/2 - trait_data[1].get_width()/2,
                                                                         70 +  small_icon_panel.get_height()/2 - trait_data[1].get_height()/2 + 50*index))

                        else:

                            # If no trait available, draw just the panels
                            self.map.engine.surface.blit(small_icon_panel, (470,70+50*index))
                            self.map.engine.surface.blit(enabled_panel, (520 ,70+50*index))

                    # Draws the panels for the bottom descriptions
                    self.map.engine.surface.blit(full_width_panel, (210 - full_width_panel.get_width()/2, 330))
                    self.map.engine.surface.blit(full_width_panel, (630 - full_width_panel.get_width()/2, 330))
                    self.map.engine.surface.blit(trait_type_panel, (210 - trait_type_panel.get_width()/2, 380))
                    self.map.engine.surface.blit(trait_type_panel, (630 - trait_type_panel.get_width()/2, 380))
                    self.map.engine.surface.blit(description_panel, (210 - description_panel.get_width()/2, 425))
                    self.map.engine.surface.blit(description_panel, (630 - description_panel.get_width()/2, 425))


                    if branch_data[0][menu_pos]:

                        # Draws the names of both currently available options

                        self.map.engine.surface.blit(branch_data[0][menu_pos][0], (210 - branch_data[0][menu_pos][0].get_width()/2,
                                                     332 + full_width_panel.get_height()/2 - branch_data[0][menu_pos][0].get_height()/2))
                        self.map.engine.surface.blit(branch_data[1][menu_pos][0], (630 - branch_data[1][menu_pos][0].get_width()/2,
                                                     332 + full_width_panel.get_height()/2 - branch_data[1][menu_pos][0].get_height()/2))

                        # Draws the trait types

                        self.map.engine.surface.blit(branch_data[0][menu_pos][2], (210 - branch_data[0][menu_pos][2].get_width()/2,
                                                     380 + trait_type_panel.get_height()/2 - branch_data[0][menu_pos][2].get_height()/2))
                        self.map.engine.surface.blit(branch_data[1][menu_pos][2], (630 - branch_data[1][menu_pos][2].get_width()/2,
                                                     380 + trait_type_panel.get_height()/2 - branch_data[1][menu_pos][2].get_height()/2))

                        # Draws the descriptions

                        draw_aligned_text(self.map.engine.surface, branch_data[0][menu_pos][3],
                                          self.map.engine.message_font, (0, 0, 0), (225 - description_panel.get_width()/2, 435), description_panel.get_width() - 30)
                        draw_aligned_text(self.map.engine.surface, branch_data[1][menu_pos][3],
                                          self.map.engine.message_font, (0, 0, 0), (645 - description_panel.get_width()/2, 435), description_panel.get_width() - 30)

                    # Draws the cursor:
                    if trait_indicator_pos[menu_pos] == 0:
                        padlib_rounded_rect(self.map.engine.surface, selected_color, (98, 68 + 50*menu_pos, enabled_panel.get_width() + 4, enabled_panel.get_height() + 4 ), 6, 5)
                    else:
                        padlib_rounded_rect(self.map.engine.surface, selected_color, (518, 68 + 50*menu_pos, enabled_panel.get_width() + 4, enabled_panel.get_height() + 4 ), 6, 5)


                    pygame.display.flip()
                    update = False
                self.map.engine.clock.tick(60)

class Doll(Unit):
    def __init__(self, name, image, avatar, moves, growthvector, level, spell_preference,
                 chartype, unitclass, animation, deathquote):
        Unit.__init__(self, name, image, avatar, moves, growthvector, level, spell_preference, chartype, unitclass, animation, deathquote)
        self.is_proxy_unit = True

    def experience(self, enemy, damage):
        return self.parentunit.experience(enemy, damage)

    def battle_spirit(self, target, effect, critical):
        return self.parentunit.battle_spirit(target, effect, critical)

    def plot_results(self, target, self_exp_delta, self_level_up,
                     enemy_exp_delta, enemy_level_up, self_spirit_delta, enemy_spirit_delta,
                     sc_cost_user, sc_cost_target):

        """
        # Function Name: plot_results
        # Purpose: Displays the battle's results
        # Inputs:   enemy = The opponent
        #           damage = How much damage the unit has taken, or if the unit was missed, the text "miss"
        #           self_exp_delta, enemy_exp_delta = experience points gained
        #           self_spirit_delta, enemy_spirit_delta = spirit charge change
        #           sc_cost_user, sc_cost_target = spirit charge cost for spells
        """

        self.parentunit.plot_results(target, self_exp_delta, self_level_up,
                     enemy_exp_delta, enemy_level_up, self_spirit_delta, enemy_spirit_delta,
                     sc_cost_user, sc_cost_target)

    # Unit set to be the parent unit of the doll unit
    def set_parentunit(self, parentunit):
        self.parentunit = parentunit

class UnitCircleSprite(pygame.sprite.Sprite):

    def __init__(self, unit):
        """
        # Function: __init__
        # Purpose: Creates a sprite for the circle underneath the unit
        # Inputs: unit - unit to initialize from
        """
        pygame.sprite.Sprite.__init__(self)
        self.unit = unit
        self.hold = False   # Hold position
                            # Used for animating vertical movements. Set this to True)

        team_panels = pygame.image.load(os.path.join('images', 'team_panels.png')).convert_alpha()

        # Initialize Sprites
        if unit.chartype == 'boss':
            self.original_image = team_panels.subsurface((70, 0, 35, 35))
        elif self.unit.chartype == 'npc':
            self.original_image = team_panels.subsurface((105, 0, 35, 35))
        elif self.unit.chartype == 'pc':
            self.original_image = team_panels.subsurface((0, 0, 35, 35))
        elif self.unit.chartype == 'enemy':
            self.original_image = team_panels.subsurface((35, 0, 35, 35))

        self.image = self.original_image
        self.rect = self.image.get_rect()


    def update(self):
        """
        # Function: update
        # Purpose: Updates sprite to current location of the unit (pixel)
        """
        if not self.hold:
            self.image = self.original_image
            self.rect.topleft = tuple(self.unit.location_pixel-self.unit.map.screen_shift*35)

        # Do not draw the image if unit is outside the bounds of the screen
        if (self.rect.topleft[0] >= 875 or self.rect.topleft[0] < -35
             or self.rect.topleft[1] >= 490 or self.rect.topleft[1] < -35):
            self.rect.topleft = (-35, -35)


        # Draw only a portion of the sprite if the unit is getting cut off by the menu panel
        if self.rect.topleft[1] > 455 and self.rect.topleft[1] < 490:

            cutoff_y = 35 - (self.rect.topleft[1] - 455)
            self.image = self.original_image.subsurface((0, 0, 35, cutoff_y))



class UnitMapSprite(pygame.sprite.Sprite):

    def __init__(self, unit):
        """
        # Function: __init__
        # Purpose: Creates a sprite for the map sprite
        # Inputs: unit - unit to initialize from
        """
        pygame.sprite.Sprite.__init__(self)
        self.unit = unit

        self.active_image = unit.image.subsurface((0, 0, 35, 35))
        self.wait_image =  unit.image.subsurface((105, 0, 35, 35))
        self.transparent_image = unit.image.subsurface(140, 0, 35, 35)

        # This flag is used to force the image displayed to be the transparent one
        # Used in the deploy screen
        self.transparent_flag = False

        self.image = self.active_image
        self.rect = self.image.get_rect()


    def update(self):
        """
        # Function: update
        # Purpose: Updates sprite to current location of the unit (pixel)
        """

        if self.transparent_flag:
            self.image = self.transparent_image
        elif self.unit.turnend == False or self.unit.map.currentplayer != self.unit.team:
            self.image = self.active_image
        else:
            self.image = self.wait_image
        self.rect.topleft = tuple(self.unit.location_pixel-self.unit.map.screen_shift*35)


        # Do not draw the image if unit is outside the bounds of the screen
        if (self.rect.topleft[0] >= 875 or self.rect.topleft[0] < -35
             or self.rect.topleft[1] >= 490 or self.rect.topleft[1] < -35):

            self.rect.topleft = (-35, -35)

        # Draw only a portion of the sprite if the unit is getting cut off by the menu panel
        if self.rect.topleft[1] > 455 and self.rect.topleft[1] < 490:

            cutoff_y = 35 - (self.rect.topleft[1] - 455)
            self.image = self.active_image.subsurface((0, 0, 35, cutoff_y))

class UnitStatusSprite(pygame.sprite.Sprite):

    def __init__(self, unit):
        """
        # Function: __init__
        # Purpose: Creates a sprite for the unit's status bubble
        # Inputs: unit - unit to initialize bubble for from
        """
        pygame.sprite.Sprite.__init__(self)
        self.unit = unit

        # Blank Surface
        self.blank = pygame.surface.Surface((18, 18)).convert_alpha()
        self.blank.fill((0, 0, 0, 0))
        self.status_queue = [self.blank]
        self.image = self.blank
        self.rect = self.image.get_rect()
        self.counter = 0

    def update_queue(self):

        # Generate new status queue
        self.status_queue = [self.unit.map.engine.status_effects_catalog[status_effect].icon
                            for status_effect in self.unit.status.keys()]
        if not self.status_queue:
            self.status_queue = [self.blank]

        # Draw next image from front of the line
        self.image = self.status_queue.pop(0)
        self.rect = self.image.get_rect()

    def update(self):
        # Change image every 60 frames
        if self.counter == 61:
            # Append current image to back of the line
            self.status_queue.append(self.image)
            # Draw next image from front of the line
            self.image = self.status_queue.pop(0)
            self.rect = self.image.get_rect()

            # Reset Counter
            self.counter = 0

        self.counter += 1
        self.rect.topleft = tuple(Vector2(17, -5)+self.unit.location_pixel-self.unit.map.screen_shift*35)

        # Do not draw the image if unit is outside the bounds of the screen
        if (self.rect.topleft[0] >= 840 or self.rect.topleft[0] < -35
             or self.rect.topleft[1] >= 455 or self.rect.topleft[1] < -35):
            self.rect.topleft = (-35, -35)




