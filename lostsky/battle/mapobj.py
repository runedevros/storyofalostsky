import pygame
from pygame.locals import *
from lostsky.core.linalg import Vector2
from lostsky.core.utils import draw_aligned_text, padlib_rounded_rect, get_ui_panel
from lostsky.core.colors import panel_color, border_color, selected_color, scroll_bar_color, disabled_color
import string
from sys import exit
from random import randint

class Map(object):

    def __init__(self, engine, terrainfile, pre_map_MAE=None, mid_mission_MAE_list=[], post_map_MAE=None):

        """
        # Function Name: __init__
        # Purpose: Intializes the map
        # Inputs: engine = associates the map with the game system's engine
        #         map_size = the size of the map in terms of tile numbers
        #         pre_map_MAE = pre-mission map action event
        #         post_map_MAE = post-mission map action event
        """

        self.all_units = {}
        self.all_units_total = {}       # Tracks all units in the map, including those that are dead
        self.all_units_by_name = {}
        self.reserve_units = {}
        self.unit_id = 1
        self.all_landmarks = {}
        self.all_ssps = {}
        self.cursor_pos = Vector2(0, 0)
        self.screen_shift = Vector2(0, 0)
        self.engine = engine
        self.terrainfilename = terrainfile
        self.team1 = []
        self.team2 = []

        # Sprite groups
        self.sg_unitcircles = pygame.sprite.RenderUpdates()
        self.sg_units = pygame.sprite.RenderUpdates()
        self.sg_status = pygame.sprite.RenderUpdates()
        self.sg_moving_unit = pygame.sprite.RenderUpdates()

        # Pre-map Map Action Event
        self.pre_map_MAE = pre_map_MAE
        if pre_map_MAE != None:
            self.pre_map_MAE.map = self
        # Post-map Map Action Event
        self.post_map_MAE = post_map_MAE
        if post_map_MAE != None:
            self.post_map_MAE.map = self

        # Mid-mission Map Action Events
        self.all_mid_mission_MAEs = []
        for MAE in mid_mission_MAE_list:
            self.add_MAE(MAE)

        # Custom Variables checked/set by map actions
        self.cust_var = {}
        self.conv_images = {}

        # Deployment variables
        self.preset_units = {}
        self.default_locations = {}
        self.deploy_locations = []

        # Highlighted tiles
        self.all_highlighted_tiles = []

        # New party members list
        self.new_party_members = []

        # Flag for conversation only maps. Instantly jumps to the end of a battle after the prestart section
        self.nobattle = False
        #Initializes terrain map
        self.generate_terrain()
        self.setup_background()

        # Turn counter
        self.turn_count = 0

        # Frame number for animations
        self.framenum = 0

        # Background Overlays for time of day info
        self.bg_overlay = False

        # Flag to enable showing the deployment tiles
        self.deploy_mode = False

        # Enable Display of Cursor
        self.enable_cursor = True

        # Enable Display of stats/battle panel
        self.enable_stats_panel = True

        # Flag to indicate that this is a battle map
        # Used to check during forced update of traits
        self.is_battle_map = True

        # Animation Counter - heartbeat for animated objects on the map
        self.animation_counter = 0

        # Items received (Items received during battle are added in at the end)
        self.items_received = []

        # Enable Fog Flag
        self.enable_fog = False
        self.light_sources = {}
        self.temporary_light_sources = []
        self.lit_tiles = []

    def add_landmark(self, landmark):
        """
        # Function Name: Add landmark
        # Purpose: Adds an landmark to the map
        # Inputs: Landmark - map action event to be added
        """

        self.all_landmarks[landmark.name] = landmark
        landmark.map = self
        # Adds in any prohibited tiles from landmarks
        if not landmark.can_pass:
            self.map_walk_prohibited.extend(landmark.occupied_tiles)

    def add_MAE(self, MAE):
        """
        # Function Name: Add MAE
        # Purpose: Adds an MAE to the map
        # Inputs: MAE - map action event to be added
        """

        self.all_mid_mission_MAEs.append(MAE)
        MAE.map = self

    def check_all_MAE(self):
        """
        # Function Name: Check all MAEs
        # Purpose: Check all map action events and execute them if needed
        """

        for MAE in self.all_mid_mission_MAEs:
            if MAE.done == False:
                MAE.check_triggers()


    def store_unit(self, unit, team):
        """
        # Function Name: store unit
        # Purpose: Stores the unit to the map's master dictionary of units and
        #       assigns each an id key. Also runs the unit's get moves / update stats
        #       commands.
        # Inputs: unit = The unit to be assigned.
        #         team = the team to be assigned to
        """

        self.all_units_total[unit.name] = unit
        self.all_units_by_name[unit.name] = unit
        unit.id = self.unit_id
        unit.map = self
        unit.in_battle = True
        unit.update_stats()
        unit.HP = unit.maxHP
        self.store_team(unit, team)
        self.sg_units.add(unit.sprite)
        self.sg_unitcircles.add(unit.circle)
        self.sg_status.add(unit.status_bubble)
        unit.get_moves_path()

    def store_team(self, unit, team):
        """
        # Function Name: store team
        # Purpose: Stores a unit to a specific team
        # Inputs: unit = The unit to be assigned.
        #         team = The team to which a unit is to be assigned (1, 2)
        """
        if team == 1:
            self.team1.append(unit)
            unit.team = 1
            unit.team_color = (255, 0, 0)

        elif team == 2:
            self.team2.append(unit)
            unit.team = 2
            unit.team_color = (0, 0, 255)

    def get_all_moves(self):
        """
        # Function Name: get all moves
        # Purpose: iterates through all units and runs their get moves method
        """
        for unit in self.all_units_by_name.values():
            unit.get_moves_path()

    def generate_terrain(self):
        """
        # Function: generate terrain
        # Purpose: Loads the map's terrain text file and generates the terrain dictionary    #
        """


        def str_2_tuple(coord):
            """
            Converts a string of the form '(x, y, z)' to a tuple of integers
            """
            # Remove linebreaks
            coord = string.strip(coord)
            # Splits the string by commas
            split_string = string.split(coord[1:-1], ', ')

            return tuple([int(entry) for entry in split_string])

        self.terrainmap = {}
        self.layer_2_terrain = {}
        self.upper_layer = {}
        self.map_walk_prohibited = []
        self.map_fly_prohibited = []

        # Loads the terrain file
        tilefile = open(self.terrainfilename)

        # Reads the first two lines that correspond to the map's size in x and y

        self.map_x = int(tilefile.readline())
        self.map_y = int(tilefile.readline())

        # Reads each set of lines which correspond to a line of terrain tiles
        for y in xrange(0, self.map_y):
            line = tilefile.readline()
            for x in xrange(0, self.map_x):
                # Matches terrain line
                terrain = self.engine.terrain_data_by_symbol[line[x]]
                self.terrainmap[(x, y)] = [terrain, [], []]
                if not terrain.walk:
                    self.map_walk_prohibited.append((x, y))
                if not terrain.fly:
                    self.map_fly_prohibited.append((x, y))

        # Defines the shift vectors in the format [Vector, Corresponding Binary Value]
        side_vectors = [[Vector2(-1, 0), 1], [Vector2(0, -1), 2], [Vector2(1, 0), 4], [Vector2(0, 1), 8]]
        corner_vectors = [[Vector2(-1, -1), 1], [Vector2(1, -1), 2], [Vector2(1, 1), 4], [Vector2(-1, 1), 8]]



        #####################################################################
        # Generates the terrain transition values
        # Algorithm based on: David Michael's Terrain Transitions Article
        #   http://www.gamedev.net/reference/articles/article934.asp
        #####################################################################

        for x in xrange(0, self.map_x):
            for y in xrange(0, self.map_y):

                # Note: Deep water always has lower priority than everything else so we don't iterate over that
                for layer in xrange(1, len(self.engine.terrain_types)):
                    # Transition variables for side and corner transitions - 4 bit binary number
                    s = 0
                    c = 0

                    # Checks if the tile type has a higher placement priority than the current tile
                    if layer > self.terrainmap[(x, y)][0].ident:
                        # check sides
                        for vector in side_vectors:
                            new_pos = tuple(Vector2(x, y)+vector[0])
                            # Only performs operations if the new position is actually on the map
                            if self.terrainmap.has_key(new_pos):
                                # if the position is of the same type as the one being processed,
                                # bitwise OR it with the associated binary value
                                if self.terrainmap[new_pos][0].ident == layer:
                                    s |= vector[1]

                        # check corners
                        for vector in corner_vectors:
                            new_pos = tuple(Vector2(x, y)+vector[0])
                            # Only performs operations if the new position is actually on the map
                            if self.terrainmap.has_key(new_pos):
                                # if the position is of the same type as the one being processed,
                                # bitwise OR it with the associated binary value
                                if self.terrainmap[new_pos][0].ident == layer:
                                    c |= vector[1]

                    self.terrainmap[(x, y)][1].append(s)
                    self.terrainmap[(x, y)][2].append(c)

                            # Loads cliff layer data
        for y in xrange(0, self.map_y):
            line = tilefile.readline()
            # Tile within horizontal slice
            for x, tile in enumerate(string.split(line, '|')):
                # x indicates an empty tile
                if tile and tile != 'x' and tile != "x\n" and tile != 'x\r\n':
                    layer_2_tile_id = str_2_tuple(tile)

                    # Adds the cliff tile to the map
                    self.layer_2_terrain[(x, y)] = layer_2_tile_id


                    # Sets the terrain for the tile according to the overide case
                    if self.engine.layer_2_terrain_data[layer_2_tile_id]:
                        # Override case: Replace with a non-walkable cliff tile

                        overwrite_symbol = self.engine.layer_2_terrain_data[layer_2_tile_id]

                        self.terrainmap[(x, y)].append(self.terrainmap[(x, y)][0])

                        self.terrainmap[(x, y)][0] = self.engine.terrain_data_by_symbol[overwrite_symbol]


                        if self.terrainmap[(x, y)][0].walk and (x, y) in self.map_walk_prohibited:
                            self.map_walk_prohibited.remove((x, y))
                        if self.terrainmap[(x, y)][0].fly and (x, y) in self.map_fly_prohibited:
                            self.map_fly_prohibited.remove((x, y))


                        if not self.terrainmap[(x, y)][0].walk:
                            self.map_walk_prohibited.append((x, y))
                        if not self.terrainmap[(x, y)][0].fly:
                            self.map_fly_prohibited.append((x, y))

        tilefile.close()


    def add_ssp(self, ssp):
        """
        # Function Name: add_ssp
        # Purpose: Adds a spirit source point to the map
        # Inputs: ssp - spirit source point to be added
        """
        self.all_ssps[tuple(ssp.location)] = ssp
        # Adds the SSP to the landmark set
        self.add_landmark(ssp)

    def update_ssps(self):
        """
        # Function Name: add_ssp
        # Purpose: Updates status of all Spirit Source Points
        """
        for ssp in self.all_ssps.values():
            # Checks if there's a unit at each ssp location
            unit_name = self.check_occupancy(ssp.location)
            if unit_name:
                ssp.capture_state = self.all_units_by_name[unit_name].team

    def add_light_source(self, lightsource):
        """
        Function Name: add light source
        Purpose: adds a light source to the map for fog enabled maps
        """
        self.light_sources[lightsource.name] = lightsource
        self.add_landmark(lightsource)
        self.update_fog_map()

    def add_temporary_light_source(self, coords, light_range):
        """
        Function Name: add temporary light source
        Purpose: adds a light source that lasts for only one turn

        """

        lightsource = TemporaryLightSource('tempLS'+str(len(self.temporary_light_sources)), coords, light_range)
        self.temporary_light_sources.append(lightsource)
        self.add_light_source(lightsource)


    def remove_temporary_light_sources(self):
        """
        Function name: rempove temporary light sources
        Purpose: removes all temporary light sources from the map

        """

        # Deletes the light source from the master light source dictionary and from the landmarks catalog
        for lightsource in self.temporary_light_sources:
            del self.light_sources[lightsource.name]
            del self.all_landmarks[lightsource.name]

        # Clears out the temporary light source list
        self.temporary_light_sources = []

        self.update_fog_map()

    def update_fog_map(self):
        """
        Function name: updates fog map

        Purpose: regenerates the set of lit and cloaked tiles based on available light sources

        """


        # Clears fog map
        self.lit_tiles = []

        # Goes through light source updating fog map.
        for light_source in self.light_sources.values():
            if light_source.lit:

                # Only adds a tile to light source if it's not already in the list
                for tile in light_source.lit_tiles:
                    if tile not in self.lit_tiles:
                        self.lit_tiles.append(tuple(tile))

    def check_occupancy(self, coords):
        """
        # Function Name: check_occupancy
        # Purpose: Checks if a unit occupies a certain location
        """
        for unit in self.all_units_by_name.values():
            if tuple(coords) == tuple(unit.location_tile):
                return unit.name

        # If no unit has been detected, returns False
        return False

    def run_status_effects(self, unit):
        """
        # Function Name: run_status_effects
        # Purpose: Checks and executs effects of any statuses a unit might have
        """
        for status_effect in unit.status.keys():

            hp_before = unit.HP
            sc_before = unit.spirit

            # Executes effects of the S.E.
            effect = self.engine.status_effects_catalog[status_effect].execute_effect(unit)

            # if unit's HP is different show the change.
            if self.engine.status_effects_catalog[status_effect].HP_change:
                # Draw HP difference as green if it is a recovery, red if it is damage
                if effect > 0:
                    text_effect = self.engine.render_outlined_text(str(effect), self.engine.cfont, (100, 255, 100), (0, 0, 0))
                else:
                    text_effect = self.engine.render_outlined_text(str(-1*effect), self.engine.cfont, (255, 0, 0), (255, 255, 255))
            elif self.engine.status_effects_catalog[status_effect].SC_change:


                # Draw SC difference as lightblue if it is recovery
                if effect > 0:
                    text_effect = self.engine.render_outlined_text(str(effect), self.engine.cfont, (128, 255, 255), (0, 0, 0))
                else:
                    text_effect = self.engine.render_outlined_text(str(-1*effect), self.engine.cfont, (255, 0, 255), (255, 255, 255))



            if self.engine.status_effects_catalog[status_effect].show_change and effect != 0:
                self.center_on(unit)

                text_status_effect = self.engine.section_font.render(status_effect, True, (0, 0, 0))

                self.render_background()
                self.render_all_units()
                self.render_cursor()
                self.engine.surface.blit(self.engine.map_spell_board, (175, 0))
                self.engine.surface.blit(text_status_effect, (420-text_status_effect.get_width()/2, 20))
                self.engine.surface.blit(self.engine.menu_board, (0, 490))
                unit.plot_stats()
                self.engine.surface.blit(text_effect, ((unit.location_pixel.x+18-text_effect.get_width()/2, unit.location_pixel.y-25)-self.screen_shift*self.engine.tilesize))
                self.engine.pause(1)

            if self.engine.status_effects_catalog[status_effect].HP_change and (hp_before != unit.HP):
                unit.render_hp_change(hp_before, unit.HP)

            if self.engine.status_effects_catalog[status_effect].SC_change and (sc_before != unit.spirit):
                unit.render_sc_change(sc_before, unit.spirit)


            # Checks if a unit has recovered
            recovery = self.engine.status_effects_catalog[status_effect].check_recovery(unit)

            if recovery and unit.alive:
                unit.remove_status(status_effect)
                self.display_alert("Status Effect Ended!", "%s's %s status has worn off."%(unit.name, status_effect))

        if unit.alive == False:
            if unit.deathquote:
                rand_num = randint(0, len(unit.deathquote)-1)
                self.say(unit.deathquote[rand_num]['line'], unit.name, unit.deathquote[rand_num]['portrait'])

            if not unit.ressurected and (unit.has_trait_property('Revive Lv.1') or unit.has_trait_property('Revive Lv.2') or unit.has_trait_property('Revive Lv.3')):
                self.check_map_event_revive(unit)
            else:
                self.kill(unit, render_fadeout=True)


    def run_ssp_sc_regen(self, team):
        """
        run_ssp_sc_regen

        Checks if any of the SSPs are occupied by any units. If so and if their SC is under a certain value,
        regenerate a constant amount of SC as long as they are on the SSP.
        """
        sc_regen_value = 50
        sc_max = 500
        if team == 1:
            current_team = self.team1
        else:
            current_team = self.team2


        for ssp_coord in self.all_ssps.keys():

            unit_name = self.check_occupancy(ssp_coord)

            if (unit_name and self.all_units_by_name[unit_name] in current_team
                and self.all_units_by_name[unit_name].spirit < sc_max):
                unit = self.all_units_by_name[unit_name]
                unit.sc_regen("Spirit Source Bonus!", sc_regen_value, sc_max)


    def check_map_event_revive(self, unit):

        """
        # Function Name: check_map_event_revive
        # Purpose: If a unit is killed during map events (Poison, scripted events) use this to try and revive them
        # Inputs: user - The person who is using this trait
        """

        if any((unit.has_trait_property('Revive Lv.1'), unit.has_trait_property('Revive Lv.2'), unit.has_trait_property('Revive Lv.3'))):

            if unit.has_trait_property('Revive Lv.1'):
                # HP to revive to (multiply to Max HP)
                HP_ressurect = 0.05
                # SC pentalty
                SC_penalty = 300

                trait_name = self.engine.render_outlined_text("Revive Lv.1!", self.engine.cfont, (255, 0, 0), (255, 255, 255))

            if unit.has_trait_property('Revive Lv.2'):
                HP_ressurect = 0.50
                SC_penalty = 600
                trait_name = self.engine.render_outlined_text("Revive Lv.2!", self.engine.cfont, (255, 0, 0), (255, 255, 255))


            if unit.has_trait_property('Revive Lv.3'):
                HP_ressurect = 1
                SC_penalty = 900
                trait_name = self.engine.render_outlined_text("Revive Lv.3!", self.engine.cfont, (255, 0, 0), (255, 255, 255))

        else:
            print "ERROR: No revive trait available?"
            return


        unit.alive = True
        unit.ressurected = True
        unit.spirit -= SC_penalty
        recovery = int(HP_ressurect*unit.maxHP)
        unit.HP = recovery

        if unit.spirit < 0:
            unit.spirit = 0



        self.render_background()
        self.engine.surface.blit(self.engine.menu_board, (0, 490))
        self.render_all_units()
        self.render_cursor()
        unit.plot_stats()

        self.engine.surface.blit(trait_name,
                                 (unit.location_pixel.x+18-trait_name.get_width()/2-35*self.screen_shift.x,
                                  unit.location_pixel.y-25-35*self.screen_shift.y))

        pygame.display.flip()

        self.engine.pause(1.0)

        unit.render_hp_change(0, unit.HP)


    #############################
    # Graphical Methods
    #############################

    def center_on(self, unit, text_board=False,  battle_board = False, lhs_unit = None, rhs_unit = None, draw_range = None):
        """
        # Function Name: center_on
        # Purpose: Centers the current viewfield on a unit
        # Inputs:       unit - The unit to be centered upon
        #               text_board - True if using the text display board,
        #               battle_board - True if using the two-unit battle board
        #                   If neither of the above are enabled, draw the standard interface.
        #               lhs_unit = unit to draw on LHS of board
        #               rhs_unit = unit to draw on RHS of board
        #               draw_range = whether to draw a unit's attack range during this transition
        #
        """
        self.center_cursor(unit.location_tile, text_board, battle_board, lhs_unit, rhs_unit, draw_range)

    def center_cursor(self, destination, text_board=False, battle_board = False, lhs_unit = None, rhs_unit = None, draw_range = None):
        """
        # Function Name: center_cursor
        # Purpose: Centers the current viewfield on a set of coords
        # Inputs:       unit - The unit to be centered upon
        #               text_board - True if using the text display board,
        #               battle_board - True if using the two-unit battle board
        #                   If neither of the above are enabled, draw the standard interface.
        #               lhs_unit = unit to draw on LHS of board
        #               rhs_unit = unit to draw on RHS of board
        #               draw_range = whether to draw a unit's attack range during this transition
        # Function modification by Beanbeanman29 - 8/20
        """

        self.cursor_pos = Vector2(tuple(destination))

        # Includes a correction so that the shift doesn't go too far
        final_x = min(max(0, int(destination.x-12)), self.map_x-24)
        final_y = min(max(0, int(destination.y-7)), self.map_y-14)
        # Relative displacement vector between initial and final positions
        delta_pos = Vector2(final_x, final_y) - self.screen_shift

        # Only draw animation if the new position of the screen is different than the old position
        if delta_pos.get_magnitude() > 0:

            velocity = 0.4*delta_pos.get_normalized()

            max_frames = int(delta_pos.get_magnitude()/velocity.get_magnitude())
            for frame in xrange(0, max_frames):
                self.screen_shift += velocity

                self.render_background()
                self.render_all_units()
                self.render_cursor()
                if text_board:
                    self.engine.surface.blit(self.engine.text_board, (0, 490))
                elif battle_board:
                    self.engine.surface.blit(self.engine.battle_board, (0, 490))

                    if lhs_unit:
                        lhs_unit.plot_stats()
                    if rhs_unit:
                        rhs_unit.plot_stats(rhs = True)
                    if draw_range:
                        draw_range.plot_attacks()
                    if lhs_unit and rhs_unit:
                        lhs_unit.plot_predictor(rhs_unit)

                else:
                    self.engine.surface.blit(self.engine.menu_board, (0, 490))


                pygame.display.flip()
                self.engine.clock.tick(60)

            # Locks in final screen position to final quantities since the values may not be whole numbers at the end
            # of the animation
            self.screen_shift.x = final_x
            self.screen_shift.y = final_y

    def kill(self, unit, render_fadeout = False):
        """
        # Function Name: Kill
        # Purpose: Removes a unit from the map
        """

        # Display unit's death animation.
        if render_fadeout:
            self.sg_status.remove(unit.status_bubble)
            unit.render_fadeout()


        # Removes unit
        del self.all_units_by_name[unit.name]
        if unit.team == 1:
            self.team1.remove(unit)
        else:
            self.team2.remove(unit)

        # Remove sprite from unit sprite group
        self.sg_units.remove(unit.sprite)
        self.sg_unitcircles.remove(unit.circle)
        self.sg_status.remove(unit.status_bubble)

    def setup_background(self):
        """
        # Function Name: setup background
        # Purpose: renders a background with all the tiles.
        """
        self.background = pygame.Surface((self.map_x*35, self.map_y*35))

        def render_tile(x, y):
            """
            # Function Name: render_tile
            # Purpose: renders a tile at location (x, y)
            """
            # Draws base background tile
            # If the terrain has been overwritten, draw the original background tile first
            if len(self.terrainmap[(x, y)]) == 3:
                self.background.blit(self.engine.terrain_img, (x*35, y*35), (0, self.terrainmap[(x, y)][0].ident*70, 35, 35))
            elif len(self.terrainmap[(x, y)]) == 4:
                self.background.blit(self.engine.terrain_img, (x*35, y*35), (0, self.terrainmap[(x, y)][3].ident*70, 35, 35))


            for terrain_type in xrange(1, len(self.engine.terrain_types)):
                # Draws Corner Transitions
                if self.terrainmap[(x, y)][2][terrain_type-1] != 0:
                    self.background.blit(self.engine.terrain_img, (x*35, y*35), (int(self.terrainmap[(x, y)][2][terrain_type-1]*35), terrain_type*70+35, 35, 35))
                # Draws Side transitions
                if self.terrainmap[(x, y)][1][terrain_type-1] != 0:
                    self.background.blit(self.engine.terrain_img, (x*35, y*35), (int(self.terrainmap[(x, y)][1][terrain_type-1]*35), terrain_type*70, 35, 35))
                # Draw layer 2 tiles
                if (x, y) in self.layer_2_terrain.keys():
                    self.background.blit(self.engine.layer_2_img, (x*35, y*35), (self.layer_2_terrain[(x, y)][0]*35, self.layer_2_terrain[(x, y)][1]*35, 35, 35))

        [render_tile(x, y) for x in xrange(0, self.map_x) for y in xrange(0, self.map_y)]

    def render_menu_panel(self):
        """
        # Function Name: render menu panel
        # Purpose: draws the menu panel at the bottom of the screen
        """
        if self.enable_stats_panel:
            self.engine.surface.blit(self.engine.menu_board, (0, 490))
        else:
            self.engine.surface.blit(self.engine.text_board, (0, 490))

    def render_background(self):
        """
        # Function Name: render background
        # Purpose: draws background onto the screen
        #          surface = target surface to render to (Default is game screen surface)
        """
        xmin = self.screen_shift.x
        xmax = min(self.screen_shift.x+24, self.map_x)
        ymin = self.screen_shift.y
        ymax = min(self.screen_shift.y+14, self.map_y)

        self.engine.surface.blit(self.background, (0, 0), (int(xmin*35), int(ymin*35), 840, 490))

        self.render_landmarks([xmin, xmax, ymin, ymax])

        # Draws the fog if enabled on the map
        if self.enable_fog:
            # a +/- 1 buffer is added to the shift to account for non-integer shifts when camera pans.
            for y in xrange(int(self.screen_shift.y)-1, int(self.screen_shift.y+14)+1):
                for x in xrange(int(self.screen_shift.x)-1, int(self.screen_shift.x+24)+1):

                    # If this tile is not contained in the fog array of lit
                    if (x, y) not in self.lit_tiles:

                        fog_coord_x = 35*(x%self.engine.fog_panel_x)
                        fog_coord_y = 35*(y%self.engine.fog_panel_y)


                        self.engine.surface.blit(self.engine.fog_panel,( (x-self.screen_shift.x)*35, (y-self.screen_shift.y)*35), (fog_coord_x, fog_coord_y, 35, 35))

        if self.engine.options.grid == True:
            for x in xrange(0, 24):
                pygame.draw.line(self.engine.surface, (200, 200, 200), (x*35, 0), (x*35, 490))
            for y in xrange(0, 14):
                pygame.draw.line(self.engine.surface, (200, 200, 200), (0, y*35), (840, y*35))

        # Background Color Tint Overlays
        if self.bg_overlay == "Night":
            self.engine.surface.blit(self.engine.night_overlay, (0, 0))
        elif self.bg_overlay == "Sunset":
            self.engine.surface.blit(self.engine.sunset_overlay, (0, 0))

        if self.deploy_mode:
            self.render_deploy_locations()

        # Updates animation counter
        self.animation_counter += 1
        if self.animation_counter == 121:
            self.animation_counter = 0


    def render_landmarks(self, bounds):
        """
        # Function Name: Render Landmark
        # Purpose: Draws all the landmarks and highlights on the screen
        #          Bounds = the current xmin, xmax, ymin, ymax boundaries of the world map
        """
        xmin, xmax, ymin, ymax = bounds

        # Increases bounds by 35 pixels in all directions to allow for scrolling behavior
        xmin -= 35
        xmax += 35
        ymin -= 35
        ymax += 35

        for landmark in self.all_landmarks.values():

            # checks if the landmark is within the bounds of the currently viewed map
            if landmark.location.x >= xmin and landmark.location.x < xmax and landmark.location.y >= ymin and landmark.location.y < ymax:
                landmark.render()

        for highlight_tile in self.all_highlighted_tiles:
            if highlight_tile.x >= xmin and highlight_tile.x < xmax and highlight_tile.y >= ymin and highlight_tile.y < ymax:
                x, y = highlight_tile*35
                self.engine.surface.blit(self.engine.highlight_tile, ((x, y)-self.screen_shift*35))


    def render_deploy_locations(self):
        """
        # Function Name: Render Deploy Locations
        # Purpose: Draws the valid deployment locations onto the map
        """

        xmin = int(self.screen_shift.x)
        xmax = min(int(self.screen_shift.x)+24, self.map_x)
        ymin = int(self.screen_shift.y)
        ymax = min(int(self.screen_shift.y)+14, self.map_y)
        bounds = [xmin, xmax, ymin, ymax]

        [self.engine.surface.blit(self.engine.deploy_tile, ((location[0]-self.screen_shift.x)*35, (location[1]-self.screen_shift.y)*35)) for location in self.deploy_locations if location[0] >= bounds[0] and location[0] < bounds[1] and location[1] >= bounds[2] and location[1] < bounds[3]]


    def render_all_units(self, bubbles = True):
        """
        # Function Name: render all units
        # Purpose: iterates through all units and runs their render method
        # Inputs: bubbles - T/F enable rendering of status bubbles
        """
        self.sg_unitcircles.update()
        self.sg_units.update()
        self.sg_status.update()

        rects = self.sg_unitcircles.draw(self.engine.surface)
        rects += self.sg_units.draw(self.engine.surface)
        if bubbles:
            rects += self.sg_status.draw(self.engine.surface)
        return rects

    def render_current_terrain_data(self):
        """
        # Function Name: render current terrain data
        # Purpose: draws information about the current tile under the unit's cursor
        """

        # Draws current terrain tile info
        terrain_icon_panel = get_ui_panel((70, 70), border_color, panel_color)
        stat_panel = get_ui_panel((130, 35), border_color, panel_color)
        terrain_name_panel = get_ui_panel((200, 35), border_color, panel_color)


        evade_mod = self.terrainmap[tuple(self.cursor_pos)][0].evade_mod
        if self.enable_fog and tuple(self.cursor_pos) not in self.lit_tiles:
            fog_tile = True
            evade_mod += 33
        else:
            fog_tile = False

        if fog_tile:
            text_current_terrain_type = self.engine.speaker_font.render(self.terrainmap[tuple(self.cursor_pos)][0].name + " (Fog)", True, (0, 0, 0))
        else:
            text_current_terrain_type = self.engine.speaker_font.render(self.terrainmap[tuple(self.cursor_pos)][0].name, True, (0, 0, 0))


        if self.terrainmap[tuple(self.cursor_pos)][0].damage_mod > 0:
            text_dmg_value = self.engine.data_font.render("%d"%(-1*self.terrainmap[tuple(self.cursor_pos)][0].damage_mod)+"%", True, (0, 0, 0))
            dmg_icon1 = self.engine.status_effects_catalog['DEF Down'].icon
            dmg_icon2 = self.engine.status_effects_catalog['MDEF Down'].icon

        else:
            text_dmg_value = self.engine.data_font.render("+%d"%(-1*self.terrainmap[tuple(self.cursor_pos)][0].damage_mod)+"%", True, (0, 0, 0))
            dmg_icon1 = self.engine.status_effects_catalog['DEF Up'].icon
            dmg_icon2 = self.engine.status_effects_catalog['MDEF Up'].icon

        if evade_mod >= 0:
            text_eva_value = self.engine.data_font.render("+%d"%(evade_mod)+"%", True, (0, 0, 0))
            eva_icon = self.engine.status_effect_icons.subsurface((5*24, 24, 24, 24))
        else:
            text_eva_value = self.engine.data_font.render("%d"%(evade_mod)+"%", True, (0, 0, 0))
            eva_icon = self.engine.status_effect_icons.subsurface((5*24, 2*24, 24, 24))



        self.engine.surface.blit(terrain_name_panel, (630 - terrain_name_panel.get_width()/2, 505))
        self.engine.surface.blit(text_current_terrain_type, (630 - text_current_terrain_type.get_width()/2,
                                                             505 + stat_panel.get_height()/2 - text_current_terrain_type.get_height()/2))



        self.engine.surface.blit(terrain_icon_panel, (595, 545))
        self.engine.surface.blit(self.engine.terrain_icon, (605, 555), (self.terrainmap[tuple(self.cursor_pos)][0].icon*50, 0, 50, 50))

        # If this terrain has damage or evade bonuses, draw them

        if self.terrainmap[tuple(self.cursor_pos)][0].damage_mod:
            self.engine.surface.blit(stat_panel, (460, 563))
            self.engine.surface.blit(dmg_icon1, (470,
                                                    563 + stat_panel.get_height()/2 - dmg_icon1.get_height()/2))
            self.engine.surface.blit(dmg_icon2, (495,
                                                    563 + stat_panel.get_height()/2 - dmg_icon2.get_height()/2))

            self.engine.surface.blit(text_dmg_value, (580 - text_dmg_value.get_width(),
                                                563 + stat_panel.get_height()/2 - text_dmg_value.get_height()/2))

        if evade_mod != 0:
            self.engine.surface.blit(stat_panel, (670, 563))
            self.engine.surface.blit(eva_icon, (690,
                                                    563 + stat_panel.get_height()/2 - eva_icon.get_height()/2))
            self.engine.surface.blit(text_eva_value, (780 - text_eva_value.get_width(),
                                                563 + stat_panel.get_height()/2 - text_eva_value.get_height()/2))

    def render_cursor(self):
        """
        # Function Name: render cursor
        # Purpose: plots the cursor update
        """
        if self.enable_cursor:
            self.engine.surface.blit(self.engine.cursor_img,
                                 (self.cursor_pos*self.engine.tilesize-self.screen_shift*self.engine.tilesize))

    def show_animation(self, id_string, coords):

        """
        # Function name: render canned animation
        # Purpose: draws a canned spell animation on the screen
        """

        # load spell image
        effect_image = self.engine.effect_animations[id_string]['image']
        frame_width = self.engine.effect_animations[id_string]['frame_width']
        frame_height = self.engine.effect_animations[id_string]['frame_height']
        max_frames_x = effect_image.get_width()/frame_width
        max_frames_y = effect_image.get_height()/frame_height
        delay = self.engine.effect_animations[id_string]['delay']
        vector_coords = Vector2(coords)
        for frame_num_y in xrange(0, max_frames_y):
            for frame_num_x in xrange(0, max_frames_x):

                self.render_background()
                self.render_all_units()
                self.render_cursor()
                self.render_menu_panel()

                # Draws emoticon frame
                self.engine.surface.blit(effect_image,
                    35*vector_coords+Vector2(18, 18)-Vector2(frame_width/2, frame_height/2)-35*self.screen_shift, (frame_width*frame_num_x, frame_height*frame_num_y, frame_width, frame_height))
                pygame.display.flip()
                self.engine.clock.tick(60)
                # Delay between frames
                if delay > 0:
                    self.engine.pause(delay)





    def say(self, line, speaker=None, portrait=None):
        """
        # Function name: say
        # Purpose: Displays a line of text and awaits for the player to press Z to continue
        # Inputs: line = The string of text to be displayed
        #         speaker = The name of the person saying it
        #         portrait = The portrait to display, if any
        """


        # generates the text for each line
        menu_flag = True
        update = True

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN and (event.key == K_z or event.key == K_RETURN):
                    menu_flag = False

            # Hold down C to skip through the game.
            keys = pygame.key.get_pressed()
            if keys[K_c]:
                menu_flag = False

            if update:
                self.render_background()
                self.render_all_units()
                self.render_cursor()
                for conversation_image in self.conv_images.values():
                    self.engine.surface.blit(conversation_image[0], conversation_image[1])
                self.engine.draw_conversation_message(line, speaker, portrait)

                pygame.display.flip()
                update = False

            self.engine.clock.tick(60)

    def choice(self, query, responses):
        """
        # Function name: Choice
        # Purpose: Displays a question for the player to answer
        # Inputs: string = The string of text to be displayed (e.g. do you like pie?)
        #         responses = A list of (at most 2) options given to the player
        """

        menu_flag = True
        menu_pos = 0

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP or event.key == K_LEFT:
                        if menu_pos > 0:
                            menu_pos -= 1
                        elif menu_pos == 0:
                            menu_pos = len(responses)-1
                    if event.key == K_DOWN or event.key == K_RIGHT:
                        if menu_pos < len(responses)-1:
                            menu_pos += 1
                        elif menu_pos == len(responses)-1:
                            menu_pos = 0

                    if (event.key == K_z or event.key == K_RETURN):
                        menu_flag = False
                        return responses[menu_pos]

            if menu_flag:
                self.render_background()
                self.render_all_units()
                self.render_cursor()
                self.engine.draw_choice_prompt(query, responses)
                padlib_rounded_rect(self.engine.surface, selected_color, (138, 533 + menu_pos*45, 554, 39), 6, 5)

                pygame.display.flip()
                self.engine.clock.tick(60)


    #############################
    # Interaction Methods
    #############################


    def user_input(self):
        """
        # Function Name: user input
        # Purpose: top level interaction. Checks if there is any input by the user
        #   and allows the user to move around the cursor with the arrow keys and select a unit
        #   if there is one under the mouse
        """
        arrowkeys = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                    self.cursor_arrows(event)
                    arrowkeys = True
                    self.framenum = 0
                if event.key == K_z or event.key == K_RETURN:

                    selected = self.cursor_key_search()

                    # Sends the player to the unit's top level menu
                    if selected is not False:
                        if self.all_units_by_name[selected].team == 1 and not self.all_units_by_name[selected].turnend:
                            self.all_units_by_name[selected].menu_loop()

                        else:
                            self.stats_interface(self.all_units_by_name[selected])

                    # Sends the player to the map's menu
                    elif selected == False:
                        self.map_menu()


                if event.key == K_a:

                    # Checks to make sure the counter is within the bounds of the team 1 list
                    if self.ally_center > len(self.team1) - 1:
                        self.ally_center = len(self.team1) - 1

                    if self.ally_center > 0:
                        self.ally_center -= 1
                    else:
                        self.ally_center = len(self.team1) - 1
                    self.center_on(self.team1[self.ally_center])

                if event.key == K_s:

                    # Checks to make sure the counter is within the bounds of the team 1 list
                    if self.ally_center > len(self.team1) - 1:
                        self.ally_center = len(self.team1) - 1

                    if self.ally_center < len(self.team1) - 1:
                        self.ally_center += 1
                    else:
                        self.ally_center = 0
                    self.center_on(self.team1[self.ally_center])

                if event.key == K_q and self.team2:
                    # Checks to make sure the counter is within the bounds of the team 2 list
                    if self.enemy_center > len(self.team2) - 1:
                        self.enemy_center = len(self.team2) - 1

                    if self.enemy_center > 0:
                        self.enemy_center -= 1
                    else:
                        self.enemy_center = len(self.team2) - 1
                    self.center_on(self.team2[self.enemy_center])
                if event.key == K_w and self.team2:
                    # Checks to make sure the counter is within the bounds of the team 2 list
                    if self.enemy_center > len(self.team2) - 1:
                        self.enemy_center = len(self.team2) - 1

                    if self.enemy_center < len(self.team2) - 1:
                        self.enemy_center += 1
                    else:
                        self.enemy_center = 0
                    self.center_on(self.team2[self.enemy_center])

        # Use C to toggle displaying movement range
        keys = pygame.key.get_pressed()
        if keys[K_c]:
            self.move_plot = True
        else:
            self.move_plot = False

        # if there is not a tap detected, check if the key is being held down
        if arrowkeys == False and self.framenum == 9:
            self.cursor_arrows_hold()


    def cursor_key_search(self):
        """
        # Function Name: cursor key search
        # Purpose: checks if there is a unit under the cursor
        # Output: Unit name if there is a unit under the cursor, False otherwise
        """
        # Checks if there is a unit under the cursor
        return self.check_occupancy(self.cursor_pos)

    def cursor_arrows(self, event):
        """
        # Function Name: cursor_arrows
        # Purpose: allows a user to move the arrows around by tapping down a key
        """
        if event.key == K_LEFT:
            # Checks if the x position of the cursor is at the edge of the map.
            if self.cursor_pos.x > 0:
                self.cursor_pos.x += -1
            # If it is at the edge of the screen, but not the map, do a screen shift
            if self.cursor_pos.x > 0 and self.cursor_pos.x - self.screen_shift.x == 0:
                self.screen_shift.x += -1

        elif event.key == K_RIGHT:
            if self.cursor_pos.x < self.map_x-1:
                self.cursor_pos.x += +1
            if self.cursor_pos.x < self.map_x-1 and self.cursor_pos.x - self.screen_shift.x == self.engine.size_x-1:
                self.screen_shift.x += +1

        if event.key == K_UP:
            if self.cursor_pos.y > 0:
                self.cursor_pos.y += -1
            if self.cursor_pos.y > 0 and self.cursor_pos.y - self.screen_shift.y == 0:
                self.screen_shift.y += -1

        elif event.key == K_DOWN:
            if self.cursor_pos.y < self.map_y-1:
                self.cursor_pos.y += +1
            if self.cursor_pos.y < self.map_y-1 and self.cursor_pos.y - self.screen_shift.y == self.engine.size_y-5:
                self.screen_shift.y += +1


    def cursor_arrows_hold(self):
        """
        # Function Name: cursor_arrows_hold
        # Purpose: allows a user to move the arrows around by holding the key
        """
        key = pygame.key.get_pressed()

        if key[K_LEFT]:
            # Checks if the x position of the cursor is at the edge of the map.
            if self.cursor_pos.x > 0:
                self.cursor_pos.x += -1
            # If it is at the edge of the screen, but not the map, do a screen shift
            if self.cursor_pos.x > 0 and self.cursor_pos.x - self.screen_shift.x == 0:
                self.screen_shift.x += -1

            # Reset Frame counter to 6
            self.framenum = 6

        elif key[K_RIGHT]:
            if self.cursor_pos.x < self.map_x-1:
                self.cursor_pos.x += +1
            if self.cursor_pos.x < self.map_x-1 and self.cursor_pos.x - self.screen_shift.x == self.engine.size_x-1:
                self.screen_shift.x += +1

            # Reset Frame counter to 6
            self.framenum = 6

        if key[K_UP]:
            if self.cursor_pos.y > 0:
                self.cursor_pos.y += -1
            if self.cursor_pos.y > 0 and self.cursor_pos.y - self.screen_shift.y == 0:
                self.screen_shift.y += -1

            # Reset Frame counter to 6
            self.framenum = 6

        elif key[K_DOWN]:
            if self.cursor_pos.y < self.map_y-1:
                self.cursor_pos.y += +1
            if self.cursor_pos.y < self.map_y-1 and self.cursor_pos.y - self.screen_shift.y == self.engine.size_y-5:
                self.screen_shift.y += +1

            # Reset Frame counter to 6
            self.framenum = 6

        pygame.event.clear()


    def map_menu(self):

        """
        # Function Name: map menu
        # Purpose: Map level menu (End Turn, Unit Stats, Options)
        """
        menu_flag = True
        menu_pos = 0

        options_panel = get_ui_panel((180, 35), border_color, panel_color)
        confirm_panel = get_ui_panel((200, 105), border_color, panel_color)

        confirm_mode = False
        confirm_selection = True

        options = [self.engine.section_font.render("End Turn", True, (0, 0, 0)),
                   self.engine.section_font.render("Objective", True, (0, 0, 0)),
                   self.engine.section_font.render("Unit Stats", True, (0, 0, 0)),
                   self.engine.section_font.render("Options", True, (0, 0, 0)),
                   self.engine.section_font.render("Quit Mission", True, (0, 0, 0)),
                   self.engine.section_font.render("Cancel", True, (0, 0, 0)),

                   ]


        text_confirm = self.engine.section_font.render("Confirm", True, (0, 0, 0))
        text_cancel = self.engine.section_font.render("Cancel", True, (0, 0, 0))

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if not confirm_mode:
                        # if either the Up or Right keys are pressed, and the menu position
                        # is not at the top, move the menu position up one.
                        if ( event.key == K_UP or event.key == K_LEFT )and menu_pos > 0:
                            menu_pos -= 1
                        elif ( event.key == K_UP or event.key == K_LEFT )and menu_pos == 0:
                            menu_pos = len(options) - 1
                        if ( event.key == K_DOWN or event.key == K_RIGHT ) and menu_pos < len(options) - 1:
                            menu_pos += 1
                        elif ( event.key == K_DOWN or event.key == K_RIGHT ) and menu_pos == len (options) - 1:
                            menu_pos = 0
                    else:
                        # Any arrow key inverts the currently selected confirmation option
                        if event.key in (K_UP, K_LEFT, K_RIGHT, K_DOWN):
                            confirm_selection = not confirm_selection


                    if event.key == K_z or event.key == K_RETURN:

                        # End Turn
                        if menu_pos == 0:

                            if not confirm_mode:
                                confirm_mode = True
                            else:
                                if confirm_selection:
                                    self.allmoved1 = True
                                    menu_flag = False
                                else:
                                    confirm_mode = False
                                    confirm_selection = True

                        # Display objectives
                        elif menu_pos == 1:

                            self.display_alert('Objective', self.objective.desc)

                        # Display unit stats screen
                        elif menu_pos == 2:


                            end_menu = self.unit_stats_loop()
                            if end_menu == True:
                                menu_flag = False

                        # Game Options
                        elif menu_pos == 3:

                            self.engine.options_menu()

                        # Quit mission
                        elif menu_pos == 4:


                            if not confirm_mode:
                                confirm_mode = True
                            else:
                                if confirm_selection:
                                    menu_flag = False
                                    # Ends the mission
                                    self.victory_condition = True
                                    self.battle_end = 'team2victory'

                                    menu_flag = False
                                else:
                                    confirm_mode = False
                                    confirm_selection = True

                        # Cancel
                        elif menu_pos == 5:
                            menu_flag = False

                    if event.key == K_x:
                        menu_flag = False

            self.render_background()
            self.render_all_units()
            self.render_cursor()
            self.engine.surface.blit(self.engine.menu_board, (0, 490))


            # If unit is on the one side of the screen currently, draw the menu on the opposite side.
            if self.cursor_pos.x*35 - self.screen_shift.x*35 > 420:
                menu_x = 35
            else:
                menu_x = 840 - self.engine.vertical_panel.get_width() - 35


            self.engine.surface.blit(self.engine.vertical_panel, (menu_x, 70))

            # Calculates the position where the top of the menu is drawn
            menu_y = 70 + self.engine.vertical_panel.get_height()/2  - len(options)*45/2

            for index, option_text in enumerate(options):

                # If this action is unavailable, use a grayed out box
                self.engine.surface.blit(options_panel, (menu_x + self.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2,
                                                             menu_y + index*45))

                # Draws a dark border around the currently selected option
                if index == menu_pos:
                    padlib_rounded_rect(self.engine.surface, selected_color, (menu_x + self.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2 - 2,
                                                             menu_y + index*45 -2, 180 + 4, 35 + 4), 6, 5)


                self.engine.surface.blit(option_text, (menu_x + self.engine.vertical_panel.get_width()/2 - option_text.get_width()/2,
                                                             menu_y + 2 + options_panel.get_height()/2 - option_text.get_height()/2 + index*45))


            if confirm_mode:

                if self.cursor_pos.x*35 - self.screen_shift.x*35 > 420:
                    menu_x = 35 + 200
                else:
                    menu_x = 840 - self.engine.vertical_panel.get_width() - 35 - 190

                menu_y += menu_pos*45

                self.engine.surface.blit(confirm_panel, (menu_x, menu_y))
                self.engine.surface.blit(options_panel, (menu_x + 10, menu_y + 10))
                self.engine.surface.blit(text_confirm, (menu_x + 10 + options_panel.get_width()/2 - text_confirm.get_width()/2,
                                                            menu_y + 12 + options_panel.get_height()/2 - text_confirm.get_height()/2))

                self.engine.surface.blit(options_panel, (menu_x + 10, menu_y + 55))
                self.engine.surface.blit(text_cancel, (menu_x + 10 + options_panel.get_width()/2 - text_cancel.get_width()/2,
                                                            menu_y + 57 + options_panel.get_height()/2 - text_cancel.get_height()/2))


                # Plots selection border
                padlib_rounded_rect(self.engine.surface, selected_color, (menu_x + 8,
                                                                               menu_y + 10 + (not confirm_selection)*45,
                                                                               options_panel.get_width()+3,
                                                                               options_panel.get_height()), 5, 5)

            pygame.display.flip()
            self.engine.clock.tick(60)

    def prestart(self):
        """
        # Function Name: Prestart
        # Purpose: Runs any prestart events if applicable
        """

        # Resetst the completion state of all map action events in the case of a mission redo
        for MAE in self.all_mid_mission_MAEs:
            MAE.done = False

        self.currentplayer = 0

        for unit in self.team1:
            unit.moved = False
            unit.turnend = False

        self.allmoved1 = False

        # Resets list of items received
        self.items_received = []

        if self.pre_map_MAE:
            self.pre_map_MAE.execute()
        self.check_all_MAE()

    def display_alert(self, title, line):
        """
        # Function Name: Displays alert
        # Purpose: Displays an alert message
        # Inputs:   Title - Title of alert
        #           Line - Alert text
        """
        menu_flag = True

        alert_image = self.engine.small_text_board.copy()
        text_title = self.engine.speaker_font.render(title, True, (0, 0, 0))
        text_instructions = self.engine.sfont.render("Press Z to continue.", True, (20, 20, 20))

        # Draws the lines on the alert image
        alert_image.blit(text_title, (alert_image.get_width()/2 - text_title.get_width()/2, 10))
        alert_image.blit(text_instructions, (alert_image.get_width() - text_instructions.get_width() -15, 110))

        draw_aligned_text(alert_image, line, self.engine.message_font, (0, 0, 0), (15, 45), alert_image.get_width() - 40)

        while menu_flag:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN and (event.key == K_z or event.key == K_RETURN):
                    menu_flag = False

            self.render_background()
            self.render_all_units()
            self.render_cursor()
            self.engine.surface.blit(self.engine.menu_board, (0, 490))
            self.engine.surface.blit(alert_image, (245, 140))
            pygame.display.flip()
            self.engine.clock.tick(60)

    def deploy_screen_main(self):

        """
        # Function Name: deploy screen main
        # Purpose: Top level deploy screen
        """

        # Enables drawing of deployment tiles
        self.deploy_mode = True

        menu_flag = True
        menu_pos = 0

        header_panel = get_ui_panel((190, 35), border_color, panel_color)
        options_panel = get_ui_panel((160, 35), border_color, panel_color)

        text_header = self.engine.speaker_font.render("Deploy Units", True, (0, 0, 0))


        options = [self.engine.section_font.render("Set Positions", True, (0, 0, 0)),
                   self.engine.section_font.render("View Party", True, (0, 0, 0)),
                   self.engine.section_font.render("Start Battle!", True, (0, 0, 0)),
                   ]

        self.engine.fade_to('black')
        # Clears out the units that are not auto-set to deploy to a certain spot
        # Deletes any unit not in the current map
        for unit in list(self.team1):
            if unit.name not in self.preset_units.keys():
                self.kill(unit)
                del(self.all_units_total[unit.name])

        # Places pre_deployed units
        extra_units = []

        for unit_name in self.engine.player_units_by_name.keys():

            # Case 1 : Unit is in a preset location and cannot be moved
            if unit_name in self.preset_units.keys():
                # Checks if the unit is already on the map
                if unit_name not in self.all_units_by_name.keys():
                    self.store_unit(self.engine.player_units_by_name[unit_name], 1)
                self.all_units_by_name[unit_name].update_location(*self.preset_units[unit_name])

            # Case 2 : Unit is in a default location and can be moved
            elif unit_name in self.default_locations.keys():
                if unit_name not in self.all_units_by_name.keys():
                    self.store_unit(self.engine.player_units_by_name[unit_name], 1)
                self.all_units_by_name[unit_name].update_location(*self.default_locations[unit_name])

            else:
                extra_units.append(unit_name)

        # Case 3: no default position specified, so put this unit in the first available location
        for unit_name in extra_units:
            print "Assigning "+unit_name+" to first available location"

            for location in self.deploy_locations:
                if not self.check_occupancy(location):

                    if unit_name not in self.all_units_by_name.keys():
                        self.store_unit(self.engine.player_units_by_name[unit_name], 1)
                    self.all_units_by_name[unit_name].update_location(*location)



        # Flag to see if this is the first time that the unit cap has been hit
        self.all_deployed = False

        while menu_flag:

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP or event.key == K_LEFT:
                        if menu_pos > 0:
                            menu_pos -= 1
                        elif menu_pos == 0:
                            menu_pos = 2
                    if event.key == K_DOWN or event.key == K_RIGHT:
                        if menu_pos < 2:
                            menu_pos += 1
                        elif menu_pos == 2:
                            menu_pos = 0
                    if event.key == K_z or event.key == K_RETURN:
                        if menu_pos == 0:
                            # self.deploy_screen_select()
                            # # Updates number of deployed units
                            # text_num_deployed = self.engine.sfont.render("Number of Units: %s/%s"%(str(self.num_deployed), str(self.max_deployed_units)), True, (0, 0, 0))
                            self.deploy_screen_swap()
                        elif menu_pos == 1:
                            self.engine.worldmap.party_menu()
                        elif menu_pos == 2 and self.team1:
                            self.deploy_mode = False
                            menu_flag = False

            if menu_flag:
                self.render_background()
                self.render_all_units()
                self.render_cursor()
                self.engine.surface.blit(self.engine.menu_board, (0, 490))


                # If cursor is on the one side of the screen currently, draw the menu on the opposite side.
                if self.cursor_pos.x*35 - self.screen_shift.x*35 > 420:
                    menu_x = 35
                else:
                    menu_x = 840 - self.engine.vertical_panel.get_width() - 35

                self.engine.surface.blit(self.engine.vertical_panel, (menu_x, 175), (0, 130, self.engine.vertical_panel.get_width(), 200))

                # Calculates the position where the top of the menu is drawn
                menu_y = 175 + 60
                self.engine.surface.blit(header_panel, (menu_x + self.engine.vertical_panel.get_width()/2 - header_panel.get_width()/2,
                                                             185))
                self.engine.surface.blit(text_header, (menu_x + self.engine.vertical_panel.get_width()/2 - text_header.get_width()/2,
                                                             185 + options_panel.get_height()/2 - text_header.get_height()/2))

                for index, option_text in enumerate(options):

                    # If this action is unavailable, use a grayed out box
                    self.engine.surface.blit(options_panel, (menu_x + self.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2,
                                                                 menu_y + index*45))

                    # Draws a dark border around the currently selected option
                    if index == menu_pos:
                        padlib_rounded_rect(self.engine.surface, selected_color, (menu_x + self.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2 - 2,
                                                                 menu_y + index*45 -2, options_panel.get_width() + 4, options_panel.get_height() + 4), 6, 5)

                    self.engine.surface.blit(option_text, (menu_x + self.engine.vertical_panel.get_width()/2 - option_text.get_width()/2,
                                                                 menu_y + 2 + options_panel.get_height()/2 - option_text.get_height()/2 + index*45))

                pygame.display.flip()
                self.engine.clock.tick(60)

    def deploy_screen_view(self):

        """
        # Function Name: deploy screen view
        # Purpose: View the map in deploy screen
        """

        menu_flag = True

        self.get_all_moves()
        while menu_flag:
            if self.framenum == 10:
                self.framenum = 0
            self.framenum += 1

            arrowkeys = False
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        self.cursor_arrows(event)
                        arrowkeys = True
                        self.framenum = 0
                    if event.key == K_z or event.key == K_RETURN:

                        selected = self.cursor_key_search()

                        # Sends the player to the unit's top level menu
                        if selected is not False:
                            self.stats_interface(self.all_units_by_name[selected])

                    if event.key == K_a and self.team1:
                        if self.ally_center > 0:
                            self.ally_center -= 1
                        else:
                            self.ally_center = len(self.team1) - 1
                        self.center_on(self.team1[self.ally_center])

                    if event.key == K_s and self.team1:
                        if self.ally_center < len(self.team1) - 1:
                            self.ally_center += 1
                        else:
                            self.ally_center = 0
                        self.center_on(self.team1[self.ally_center])

                    if event.key == K_q:
                        if self.enemy_center > 0:
                            self.enemy_center -= 1
                        else:
                            self.enemy_center = len(self.team2) - 1
                        self.center_on(self.team2[self.enemy_center])

                    if event.key == K_w:
                        if self.enemy_center < len(self.team2) - 1:
                            self.enemy_center += 1
                        else:
                            self.enemy_center = 0
                        self.center_on(self.team2[self.enemy_center])

                    if event.key == K_x:
                        menu_flag = False

            # Use C to toggle displaying movement range
            keys = pygame.key.get_pressed()
            if keys[K_c]:
                self.move_plot = True
            else:
                self.move_plot = False

            # if there is not a tap detected, check if the key is being held down
            if arrowkeys == False and self.framenum == 9:
                self.cursor_arrows_hold()
                self.framenum = 6

            # Checks if there is a unit underneath the cursor, and if there is, plots the unit's data.
            selected = False
            selected = self.cursor_key_search()

            self.render_background()

            # Renders the unit's valid moves if C is pressed.
            if selected != False and self.move_plot == True:
                self.all_units_by_name[selected].plot_moves_and_attacks()

            self.render_deploy_locations()
            self.render_all_units()
            self.render_cursor()
            self.engine.surface.blit(self.engine.menu_board, (0, 490))
            self.render_current_terrain_data()

            if selected != False:
                self.all_units_by_name[selected].plot_stats()

            pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                               %(self.cursor_pos.x, self.cursor_pos.y, self.screen_shift.x, self.screen_shift.y))

            pygame.display.flip()
            self.engine.clock.tick(60)

    def deploy_screen_swap(self):

        """
        # Function Name: deploy screen place
        # Purpose: Place unit on map
        """

        menu_flag = True
        self.get_all_moves()

        current_unit = None

        while menu_flag:
            if self.framenum == 10:
                self.framenum = 0
            self.framenum += 1

            arrowkeys = False
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        self.cursor_arrows(event)
                        arrowkeys = True
                        self.framenum = 0
                    if event.key == K_z or event.key == K_RETURN:
                        unit = self.cursor_key_search()

                        # No unit is currently selected: Add
                        if not current_unit:
                            if unit and self.all_units_by_name[unit].team == 1 and unit not in self.preset_units.keys():
                                current_unit = self.all_units_by_name[unit]
                                current_unit.sprite.transparent_flag = True

                        else:
                            # Another unit is occupying selected position: Swap units
                            if unit and unit != current_unit.name:
                                #Swap current and destination units
                                destination_unit = self.all_units_by_name[unit]
                                destination_coords = (destination_unit.location_tile.x, destination_unit.location_tile.y)
                                origin_coords = (current_unit.location_tile.x, current_unit.location_tile.y)
                                self.render_swap(current_unit, destination_unit)
                                destination_unit.update_location(*origin_coords)
                                current_unit.update_location(*destination_coords)
                                
                                current_unit.sprite.transparent_flag = False
                                current_unit = None

                            # Nobody is occupying this position: Move unit to new location
                            elif not unit and self.cursor_pos in self.deploy_locations:

                                delta = self.cursor_pos - current_unit.location_tile
                                current_unit.render_walk([delta])

                                current_unit.update_location(self.cursor_pos.x, self.cursor_pos.y)
                                current_unit.sprite.transparent_flag = False
                                current_unit = None

                            # Selected unit is same as current unit: Put unit down
                            elif unit and unit == current_unit.name:

                                current_unit.sprite.transparent_flag = False
                                current_unit = None

                            else:
                                # invalid position
                                pass

                    if event.key == K_x:

                        if current_unit:
                            self.cursor_pos.x = current_unit.location_tile.x
                            self.cursor_pos.y = current_unit.location_tile.y
                            current_unit.sprite.transparent_flag = False
                            current_unit = None
                        else:
                            menu_flag = False


            # if there is not a tap detected, check if the key is being held down
            if arrowkeys == False and self.framenum == 9:
                self.cursor_arrows_hold()
                self.framenum = 6

            if menu_flag:
                # Checks if there is a unit underneath the cursor, and if there is, plots the unit's data.
                selected = self.cursor_key_search()

                self.render_background()
                self.render_all_units()
                self.render_cursor()
                self.engine.surface.blit(self.engine.battle_board, (0, 490))

                if current_unit:
                    self.engine.surface.blit(current_unit.image, (self.cursor_pos*self.engine.tilesize-self.screen_shift*self.engine.tilesize), (0, 0, 35, 35))
                    current_unit.plot_stats()
                    if selected and selected != current_unit.name:
                        self.all_units_by_name[selected].plot_stats(rhs = True)

                else:
                    if selected:
                        self.all_units_by_name[selected].plot_stats()


                pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                                   %(self.cursor_pos.x, self.cursor_pos.y, self.screen_shift.x, self.screen_shift.y))

                pygame.display.flip()
                self.engine.clock.tick(60)

    def render_swap(self, first_unit, second_unit):
        """
        function name: render_swap

        Purpose: draw two units directly swapping positions with each other

        Inputs: first_unit - First unit to move
                second_unit - Second unit to move
        """

        delta = Vector2(second_unit.location_tile) - Vector2(first_unit.location_tile)
        first_unit.render_walk([delta])
        second_unit.render_walk([-delta])

    def player_turn(self):
        """
        # Function Name: player_turn
        # Purpose: Handles the human player's turn
        """

        self.currentplayer = 1

        # Increments the turn counter by 1 at the start of the turn
        self.turn_count += 1

        for unit in self.team1:
            unit.moved = False
            unit.turnend = False

        self.allmoved1 = False

        # Checks all map action events

        # Resets done state for any map action events that repeat each turn cycle
        for MAE in self.all_mid_mission_MAEs:
            if MAE.repeat:
                MAE.done = False


        self.check_all_MAE()

        self.center_on(self.team1[0])

        self.render_background()
        self.render_all_units()
        self.engine.surface.blit(self.engine.menu_board, (0, 490))
        pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                   %(self.cursor_pos.x, self.cursor_pos.y, self.screen_shift.x, self.screen_shift.y))

        # Displays a message for player 1.
        self.engine.surface.blit(self.engine.p1turn, (105, 140))
        pygame.display.flip()
        # Waits one second
        self.engine.pause(1)

        # processes all trait actions
        self.trait_turn_process(self.team1)
        for unit in list(self.team1):
            self.run_status_effects(unit)
        self.run_ssp_sc_regen(1)

        # Removes all temporary light sources
        if self.enable_fog:
            self.remove_temporary_light_sources()


        # Checks if any status effects managed to complete the mission objective

        self.update_ssps()
        self.battle_end = self.objective.check(self)
        if self.battle_end != False:
            self.victory_condition = True

        if self.team1:
            self.center_on(self.team1[0])

        # Clears the events before the turn starts.
        pygame.event.clear()

        self.framenum = 0

        self.get_all_moves()
        while self.allmoved1 == False and not self.victory_condition:

            if self.framenum == 10:
                self.framenum = 0
            self.framenum += 1

            self.user_input()

            # Checks if there is a unit underneath the cursor, and if there is, plots the unit's data.
            selected = False
            selected = self.cursor_key_search()

            self.render_background()

            # Renders the unit's valid moves if C is pressed.
            if selected != False and self.move_plot == True:
                self.all_units_by_name[selected].plot_moves_and_attacks()

            self.render_all_units()
            self.render_cursor()
            self.engine.surface.blit(self.engine.menu_board, (0, 490))
            self.render_current_terrain_data()

            if selected != False:
                self.all_units_by_name[selected].plot_stats()
                for index, trait in enumerate(self.all_units_by_name[selected].traits):
                    if trait and trait.variation == 'Proximity':
                        self.all_units_by_name[selected].render_proximity_range(trait)
                        break


            pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                               %(self.cursor_pos.x, self.cursor_pos.y, self.screen_shift.x, self.screen_shift.y))

            pygame.display.flip()
            self.engine.clock.tick(60)

            unitsended = 0
            # Checks if all units have ended their turn.
            for unit in self.team1:
                if unit.turnend == True or unit.alive == False:
                    unitsended += 1

            self.update_ssps()
            self.battle_end = self.objective.check(self)
            if self.battle_end != False:
                self.victory_condition = True

            # If all the units that can move have turn ended, end player 1's turn
            if self.engine.options.turn_end == True:
                if len(self.team1) == unitsended:
                    self.allmoved1 = True

            # Checks all map action events
            self.check_all_MAE()

        # Ends the remaining characters in team 1.
        for unit in self.team1:
            unit.turnend = True

    def ai_turn(self):
        """
        # Function Name: ai_turn
        # Purpose: Runs the AI's turn
        """


        self.currentplayer = 2

        if self.victory_condition == False:

            self.currentplayer = 2

            for unit in self.team2:
                unit.moved = False
                unit.turnend = False

            self.allmoved2 = False


            self.render_background()
            self.render_all_units()
            self.engine.surface.blit(self.engine.menu_board, (0, 490))
            pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                       %(self.cursor_pos.x, self.cursor_pos.y, self.screen_shift.x, self.screen_shift.y))

            # Displays a message for player 2.
            self.engine.surface.blit(self.engine.p2turn, (105, 140))
            pygame.display.flip()
            # Waits two seconds
            self.engine.pause(1)

            self.trait_turn_process(self.team2)

            # Processes status effects
            for unit in list(self.team2):
                self.run_status_effects(unit)

            self.run_ssp_sc_regen(2)


            # Checks all map action events.
            self.check_all_MAE()


            self.battle_end = self.objective.check(self)
            if self.battle_end != False:
                self.victory_condition = True

        while not self.allmoved2 and not self.victory_condition:

            unit_move_list = []
            standby_list = []
            # FSM state updates for everyone first

            [unit.ai.update_state() for unit in self.team2]

            # 1st Priority: All retreating units take their turn
            [unit_move_list.append(unit) for unit in self.team2
                if (unit.ai.current_state.name == 'AttackRetreat'
                    or unit.ai.current_state.name == 'PursuitRetreat')
                and unit.turnend == False
                and unit not in unit_move_list]

            # 2nd Priority: Healers take their turn
            [unit_move_list.append(unit) for unit in self.team2
                if (unit.ai.current_state.name == 'HealerSOS'
                    or unit.ai.current_state.name == 'HealerStandby')
                and unit.turnend == False
                and unit not in unit_move_list]

            # 3rd Priority: Everyone Else
            [unit_move_list.append(unit) for unit in self.team2
                if unit.turnend == False
                and unit not in unit_move_list]

            # Executes all units in priority order
            for unit in list(unit_move_list):

                if unit.alive and not self.victory_condition:

                    self.render_background()
                    self.render_all_units()
                    self.engine.surface.blit(self.engine.menu_board, (0, 490))
                    pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                               %(self.cursor_pos.x, self.cursor_pos.y, self.screen_shift.x, self.screen_shift.y))

                    pygame.display.flip()
                    self.engine.clock.tick(60)

                    if unit.alive:

                        # Asks the unit to carry out move
                        unit_acted = unit.ai.execute_turn()

                        if unit_acted:
                            unit.turnend = True

                        # If unit does take any actions, append them to a standby list
                        # so they can try again after everyone else has moved.
                        else:
                            standby_list.append(unit)


                    self.render_background()
                    self.render_all_units()
                    self.engine.surface.blit(self.engine.menu_board, (0, 490))
                    pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                               %(self.cursor_pos.x, self.cursor_pos.y, self.screen_shift.x, self.screen_shift.y))

                    pygame.display.flip()
                    self.engine.clock.tick(60)

                    # Checks if the battle is over and if one side's objectives have been fulfilled
                    self.update_ssps()
                    self.battle_end = self.objective.check(self)
                    if self.battle_end != False:
                        self.victory_condition = True
                        break

                    # Checks all map action events
                    self.check_all_MAE()

                    self.battle_end = self.objective.check(self)
                    if self.battle_end != False:
                        self.victory_condition = True

            for unit in list(standby_list):

                if unit.alive == True and self.victory_condition == False:
                    pygame.display.flip()
                    self.engine.clock.tick(60)

                    if unit.alive:

                        # Asks the unit to carry out move
                        unit_acted = unit.ai.execute_turn()

                        unit.turnend = True


                    pygame.display.flip()
                    self.engine.clock.tick(60)

                    # Checks if the battle is over and if one side's objectives have been fulfilled

                    self.update_ssps()
                    self.battle_end = self.objective.check(self)
                    if self.battle_end != False:
                        self.victory_condition = True
                        break

                    # Checks all map action events
                    self.check_all_MAE()

                    self.battle_end = self.objective.check(self)
                    if self.battle_end != False:
                        self.victory_condition = True

            self.allmoved2 = True
            pygame.display.flip()
            self.engine.clock.tick(60)


        # Ends the remaining characters in team 2.
        if self.team2 != []:
            for unit in self.team2:
                unit.turnend = True
    def victory_scene(self):
        """
        # function name: victory scene
        # Purpose: sets up and runs the runs the post mission MAE
        """


        if self.post_map_MAE:

            self.engine.fade_to('black', 0.5)

            for unit_name in self.required_survivors:
                if unit_name not in self.all_units_total.keys():
                    self.store_unit(self.engine.player_units_by_name[unit_name], 1)

                unit = self.all_units_total[unit_name]
                unit.spirit_stats = 'normal'
                unit.clear_status()
                unit.turnend = False

                if unit.alive == False:
                    unit.alive = True
                    unit.HP = unit.maxHP
                    self.all_units_by_name[unit.name] = unit
                    if unit.team == 1:
                        self.team1.append(unit)
                    elif unit.team == 2:
                        self.team2.append(unit)
                    # Adds unit sprite back in
                    self.sg_units.add(unit.sprite)
                    self.sg_unitcircles.add(unit.circle)
                    self.sg_status.add(unit.status_bubble)

            for unit in self.team1:
                # If a player unit is not required for the ending scenes, remove it from the map
                if unit.name not in self.required_survivors:
                    self.kill(unit)

            # Does any rearranging of units before the
            self.post_map_MAE.pre_exec()

            self.post_map_MAE.fade_from_color('black', 0.5)

            self.post_map_MAE.execute()
            pygame.mixer.music.stop()

    def render_mission_end_banner(self):
        """
        # function name: render_mission_end_banner
        # purpose: Draw the animation of the "Victory / Mission Failed" banner at the end of a mission
        """
        if self.battle_end == 'team1victory':
            mission_end_banner = self.engine.mission_victory
        else:
            mission_end_banner = self.engine.mission_failure

        smoothstep = lambda v: (v*v*(3-2*v))

        start_pos = Vector2(-525, 140)

        frame_count = 45
        step_vector = Vector2(1, 0)
        for t in xrange(0, frame_count+1):
            v = float(t)/float(frame_count)
            v = smoothstep(v)
            scale_term = int(630*v)
            intermediate_step = scale_term*step_vector
            current_pos = start_pos + intermediate_step

            self.render_background()
            self.render_all_units()
            self.render_cursor()
            self.engine.surface.blit(self.engine.menu_board, (0, 490))
            self.engine.surface.blit(mission_end_banner, current_pos)

            pygame.display.flip()
            self.engine.clock.tick(60)
        self.engine.pause(0.5)
        frame_count = 45
        start_pos = current_pos.copy()
        for t in xrange(0, frame_count+1):
            v = float(t)/float(frame_count)
            v = smoothstep(v)
            scale_term = int(730*v)
            intermediate_step = scale_term*step_vector
            current_pos = start_pos + intermediate_step

            self.render_background()
            self.render_all_units()
            self.render_cursor()
            self.engine.surface.blit(self.engine.menu_board, (0, 490))
            self.engine.surface.blit(mission_end_banner, current_pos)

            pygame.display.flip()
            self.engine.clock.tick(60)


    def turn_loop(self):
        """
        # Function Name: turn loop
        # Purpose: The main loop in a battle map that drives the game by alternating between player turns.
        """

        self.prestart()

        # Values for "Center to the next unit"
        self.ally_center = 0
        self.enemy_center = 0
        self.turn_count = 0
        self.allmoved1 = False
        self.allmoved2 = False
        self.move_plot = False

        # If the event is a conversation event, exits the function immediately without executing the
        # battle events

        if self.nobattle == False:
            self.victory_condition = False
            self.battle_end = False

            self.display_alert('Objective', self.objective.desc)
            if self.enable_deploy:
                self.deploy_screen_main()

            # Debug mode: Win instantly
            if self.engine.single_turn_win == True:
                self.victory_condition = True
                self.battle_end = 'team1victory'


            # Alternates between player and AI turns
            while not self.victory_condition:
                # Player's turn
                self.player_turn()

                # If team 2 is defeated but the objective hasn't been completed,
                # jump back to player 1
                if self.team2 and not self.engine.disable_ai:
                    self.ai_turn()

            self.render_mission_end_banner()

            # Completion MAE event
            [unit.clear_status() for unit in self.team1]
            if self.battle_end == 'team1victory':
                self.victory_scene()


        # Resets all units to max HP / spirit 300 / alive
        self.mission_end()

        # Resets all SSPs
        for ssp in self.all_ssps.values():
            ssp.capture_state = ssp.starting_state

        # Removes any added player characters in case the mission is failed
        if self.objective and self.battle_end != 'team1victory':

            for unit in self.new_party_members:

                # clears out all spell actions, traits, exp, tp stuff
                unit.reset_state()

                # Delete unit from party roster
                del(self.engine.player_units[self.engine.player_units.index(unit)])
                del(self.engine.player_units_by_name[unit.name])
                # Delete unit from save data
                del(self.engine.player.all_unit_data[unit.name])
                # Delete unit name from save data
                del(self.engine.player.party_members[self.engine.player.party_members.index(unit.name)])


        # Returns a completion string if mission was a success
        if self.objective != None:
            return self.battle_end


    def unit_stats_loop(self):


        """
        # Function Name: unit_stats_loop
        # Purpose: birdseye view of all the ally and enemy units
        """

        menu_flag = True
        # The menu position variable: [ 0 = player ; 1 = enemy, X = position of selected unit in team list]
        menu_pos = [0, 0]

        # Only a maximum number of units is displayed, these variables determine the shift in position of
        # the visible units relative to the start of the list.
        shift_ally = 0
        shift_enemy = 0

        # Generates fixed text objects for use in this screen
        text_lv = self.engine.section_font.render('Lv.', True, (0, 0, 0))
        text_ally_header = self.engine.speaker_font.render('Player Team', True, (0, 0, 0))
        text_enemy_header = self.engine.speaker_font.render('Enemy Team', True, (0, 0, 0))

        unit_panel_color = scroll_bar_color

        header_panel =  get_ui_panel((200, 35), border_color, panel_color)
        unit_panel =  get_ui_panel((300, 100), border_color, panel_color)
        small_icon_panel =  get_ui_panel((41, 41), border_color, panel_color)
        name_panel =  get_ui_panel((150, 35), border_color, panel_color)
        spell_panel =  get_ui_panel((179, 35), border_color, panel_color)
        level_panel =  get_ui_panel((70, 35), border_color, panel_color)


        # Maximum number of units present in a column
        MAX_UNITS = 5

        # Generates the main scroll bar image based on the number of displayed panels
        panel_spacing = unit_panel.get_height()+10

        SCROLL_BAR_LENGTH = MAX_UNITS*(panel_spacing)-10    # The - 10 is because panel spacing includes an
                                                            # extra 10 pixels at the bottom of each panel and
                                                            # we want the scroll bar flush with the last panel

        scroll_bar = get_ui_panel((20, SCROLL_BAR_LENGTH), border_color, panel_color)


        # Generates the image for the scroll bar visible section indicator.
        if self.team1:
            scroll_section_height_ally = SCROLL_BAR_LENGTH*MAX_UNITS/len(self.team1)
        else:
            scroll_section_height_ally = 0

        if self.team2:
            scroll_section_height_enemy = SCROLL_BAR_LENGTH*MAX_UNITS/len(self.team2)
        else:
            scroll_section_height_enemy = 0

        if MAX_UNITS < len(self.team1):
            scroll_bar_ally =  get_ui_panel((20, scroll_section_height_ally), border_color, scroll_bar_color)
        else:
            scroll_bar_ally = None
        if MAX_UNITS < len(self.team2):
            scroll_bar_enemy = get_ui_panel((20, scroll_section_height_enemy), border_color, scroll_bar_color)
        else:
            scroll_bar_enemy = None

        if self.team1:
            scroll_delta_ally = SCROLL_BAR_LENGTH/len(self.team1)
        else:
            scroll_delta_ally = 0

        if self.team2:
            scroll_delta_enemy = SCROLL_BAR_LENGTH/len(self.team2)
        else:
            scroll_delta_enemy = 0

        # Generates text data for all ally units
        ally_units_names = []
        ally_units_hp = []
        ally_units_levels = []
        ally_units_spells = []
        ally_spell_icons = []

        for unit in self.team1:

            unit_name_text = self.engine.speaker_font.render(unit.name, True, (0, 0, 0))
            if unit_name_text.get_width() > name_panel.get_width() - 20:
                unit_name_text = self.engine.sfont.render(unit.name, True, (0, 0, 0))

            ally_units_names.append(unit_name_text)


            ally_units_hp.append(self.engine.data_font.render("%d"%unit.HP, True, (0, 0, 0)))
            ally_units_levels.append(self.engine.data_font.render("%d"%unit.level, True, (0, 0, 0)))
            if unit.spell_actions[unit.equipped]:

                spell_name_text = self.engine.data_font.render(unit.spell_actions[unit.equipped].namesuffix, True, (0, 0, 0))
                if spell_name_text.get_width() > spell_panel.get_width() - 20:
                    spell_name_text = self.engine.sfont.render(unit.spell_actions[unit.equipped].namesuffix, True, (0, 0, 0))


                ally_units_spells.append(spell_name_text)
                if unit.spell_actions[unit.equipped].type in ('healing', 'support'):
                    ally_spell_icons.append(self.engine.spell_type_icons['Healing'])
                elif unit.spell_actions[unit.equipped].type == "healingitem":
                    ally_spell_icons.append(self.engine.spell_type_icons['Item'])
                else:
                    ally_spell_icons.append(self.engine.spell_type_icons[unit.spell_actions[unit.equipped].affinity])

            else:
                ally_units_spells.append(self.engine.data_font.render("Empty", True, (0, 0, 0)))
                ally_spell_icons.append(None)

        # Generates text data for all enemy units
        enemy_units_names = []
        enemy_units_hp = []
        enemy_units_levels = []
        enemy_units_spells = []
        enemy_spell_icons = []

        for unit in self.team2:


            unit_name_text = self.engine.speaker_font.render(unit.name, True, (0, 0, 0))
            if unit_name_text.get_width() > name_panel.get_width() - 20:
                unit_name_text = self.engine.sfont.render(unit.name, True, (0, 0, 0))

            enemy_units_names.append(unit_name_text)

            enemy_units_hp.append(self.engine.data_font.render("%d"%unit.HP, True, (0, 0, 0)))
            enemy_units_levels.append(self.engine.data_font.render("%d"%unit.level, True, (0, 0, 0)))
            if unit.spell_actions[unit.equipped]:


                spell_name_text = self.engine.data_font.render(unit.spell_actions[unit.equipped].namesuffix, True, (0, 0, 0))
                if spell_name_text.get_width() > spell_panel.get_width() - 20:
                    spell_name_text = self.engine.sfont.render(unit.spell_actions[unit.equipped].namesuffix, True, (0, 0, 0))

                enemy_units_spells.append(spell_name_text)
                if unit.spell_actions[unit.equipped].type in ('healing', 'support'):
                    enemy_spell_icons.append(self.engine.spell_type_icons['Healing'])
                elif unit.spell_actions[unit.equipped].type == "healingitem":
                    enemy_spell_icons.append(self.engine.spell_type_icons['Item'])
                else:
                    enemy_spell_icons.append(self.engine.spell_type_icons[unit.spell_actions[unit.equipped].affinity])

            else:
                enemy_units_spells.append(self.engine.data_font.render("Empty", True, (0, 0, 0)))
                enemy_spell_icons.append(None)

        # Flag to know when to redraw the screen
        update = True

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    update = True
                    # Toggles sides
                    # Only allows checking the other side if there are units on the other side
                    if (event.key == K_LEFT or event.key == K_RIGHT) and self.team2:
                        if menu_pos[0] == 0:
                            menu_pos[0] = 1
                            menu_pos[1] = shift_enemy
                            if menu_pos[1] < shift_enemy:
                                menu_pos[1] = shift_enemy
                            if menu_pos[1] > len(self.team2)-1:
                                menu_pos[1] = len(self.team2)-1
                                shift_enemy = max(0, len(self.team2)-6)
                        elif menu_pos[0] == 1:
                            menu_pos[0] = 0
                            menu_pos[1] = shift_ally
                            if menu_pos[1] < shift_ally:
                                menu_pos[1] = shift_ally
                            if menu_pos[1] > len(self.team1)-1:
                                menu_pos[1] = len(self.team1)-1
                                shift_ally = max(0, len(self.team1)-6)


                    if event.key == K_UP:
                        # Top of the list of units: Jumps to bottom
                        if menu_pos[1] == 0:
                            if menu_pos[0] == 0:
                                menu_pos[1] = len(self.team1)-1
                                shift_ally = max(0, len(self.team1)-MAX_UNITS)
                            if menu_pos[0] == 1:
                                menu_pos[1] = len(self.team2)-1
                                shift_enemy = max(0, len(self.team2)-MAX_UNITS)
                        # Top of interval, advances shift up
                        elif menu_pos[0] == 0 and menu_pos[1] == shift_ally:
                            menu_pos[1] -= 1
                            shift_ally -= 1
                        elif menu_pos[0] == 1 and menu_pos[1] == shift_enemy:
                            menu_pos[1] -= 1
                            shift_enemy -= 1
                        # Within the interval, advances cursor only
                        elif menu_pos[1] > 0:
                            menu_pos[1] -= 1

                    if event.key == K_DOWN:
                        # Bottom of the list of units: Jumps to top
                        if (menu_pos[0] == 0 and menu_pos[1] == len(self.team1)-1):
                            menu_pos[1] = 0
                            shift_ally = 0

                        elif (menu_pos[0] == 1 and menu_pos[1] == len(self.team2)-1):
                            menu_pos[1] = 0
                            shift_enemy = 0

                        # Bottom of the interval. Advance shift downward
                        elif menu_pos[0] == 0 and menu_pos[1] == MAX_UNITS+shift_ally-1:
                            menu_pos[1] += 1
                            shift_ally += 1

                        elif menu_pos[0] == 1 and menu_pos[1] == MAX_UNITS+shift_enemy-1:
                            menu_pos[1] += 1
                            shift_enemy += 1

                        # Between intervals. Advances downward.
                        else:
                            menu_pos[1] += 1

                    if event.key == K_z or event.key == K_RETURN:
                        if menu_pos[0] == 0:
                            self.stats_interface(self.team1[menu_pos[1]])
                        elif menu_pos[0] == 1 and self.team2:
                            self.stats_interface(self.team2[menu_pos[1]])


                    if event.key == K_x:
                        menu_flag = False
                    if event.key == K_c:
                        menu_flag = False
                        if menu_pos[0] == 0:
                            self.center_on(self.team1[menu_pos[1]])
                        elif menu_pos[0] == 1:
                            self.center_on(self.team2[menu_pos[1]])
                        # Automatically exits the map_menu loop
                        return True


            if menu_flag:

                if update:
                    # Background, Headers
                    self.engine.surface.blit(self.engine.stats_bg, (0, 0))
                    self.engine.surface.blit(header_panel, ( 210 - header_panel.get_width()/2, 10))
                    self.engine.surface.blit(text_ally_header, (210 - text_ally_header.get_width()/2,
                                                                10 + header_panel.get_height()/2 - text_ally_header.get_height()/2))
                    self.engine.surface.blit(header_panel, ( 630 - header_panel.get_width()/2, 10))
                    self.engine.surface.blit(text_enemy_header, (630 - text_enemy_header.get_width()/2,
                                                                10 + header_panel.get_height()/2 - text_ally_header.get_height()/2))

                    # If the number of units in the ally team exceeds the max units to be displayed, include a scrollbar
                    if MAX_UNITS < len(self.team1):
                        x_position_ally = 45
                    # Otherwise, center the displayed panels
                    else:
                        x_position_ally = 210 - unit_panel.get_width()/2

                    # Draws the panels for the ally team
                    for index in xrange(0, min(MAX_UNITS, len(self.team1))):
                        unit = self.team1[index + shift_ally]

                        # Draws the panel and the unit's sprite
                        self.engine.surface.blit(unit_panel, (x_position_ally, 50 + panel_spacing*index))
                        self.engine.surface.blit(small_icon_panel, (x_position_ally + 10,
                                                                    50 + unit_panel.get_height()/2 - small_icon_panel.get_height()/2 + panel_spacing*index))
                        self.engine.surface.blit(unit.sprite.image, (x_position_ally + 11 + small_icon_panel.get_width()/2 - unit.sprite.image.get_width()/2,
                                                                    50 + unit_panel.get_height()/2 - unit.sprite.image.get_height()/2 + panel_spacing*index))

                        # Draw the unit's name and level
                        self.engine.surface.blit(name_panel, (x_position_ally + 60,
                                                                    60 + panel_spacing*index))
                        self.engine.surface.blit(ally_units_names[index + shift_ally], (x_position_ally + 60 + name_panel.get_width()/2 - ally_units_names[index + shift_ally].get_width()/2,
                                                                                        60 + name_panel.get_height()/2 - ally_units_names[index + shift_ally].get_height()/2 + panel_spacing*index))
                        self.engine.surface.blit(level_panel, (x_position_ally + 220,
                                                                    60 + panel_spacing*index))
                        self.engine.surface.blit(text_lv, (x_position_ally + 229,
                                                                62 + level_panel.get_height()/2 - text_lv.get_height()/2 + index*panel_spacing))
                        self.engine.surface.blit(ally_units_levels[index + shift_ally], (x_position_ally + 220 + level_panel.get_width()*3/4 - ally_units_levels[index + shift_ally].get_width()/2,
                                                                60 + level_panel.get_height()/2 - ally_units_levels[index + shift_ally].get_height()/2  + index*panel_spacing))

                        # Draws the icon for the spell and the name of the spell
                        self.engine.surface.blit(small_icon_panel, (x_position_ally + 60,
                                                                    100 + panel_spacing*index))
                        if unit.spell_actions[unit.equipped]:
                            self.engine.surface.blit(ally_spell_icons[index + shift_ally], (x_position_ally + 60 + small_icon_panel.get_width()/2 - ally_spell_icons[index + shift_ally].get_width()/2,
                                                                        100 + small_icon_panel.get_height()/2
                                                                        - ally_spell_icons[index + shift_ally].get_height()/2 + panel_spacing*index))
                        self.engine.surface.blit(spell_panel, (x_position_ally + 111, 102 + panel_spacing*index))
                        self.engine.surface.blit(ally_units_spells[index + shift_ally], (x_position_ally + 111 + spell_panel.get_width()/2 - ally_units_spells[index + shift_ally].get_width()/2,
                                                                                         102 + spell_panel.get_height()/2 - ally_units_spells[index + shift_ally].get_height()/2 + panel_spacing*index))

                    if MAX_UNITS < len(self.team2):
                        x_position_enemy = 465
                    else:
                        x_position_enemy = 630 - unit_panel.get_width()/2

                    # Draws the panels for the enemy team
                    for index in xrange(0, min(MAX_UNITS, len(self.team2))):
                        unit = self.team2[index + shift_enemy]

                        # Draws the panel and the unit's sprite
                        self.engine.surface.blit(unit_panel, (x_position_enemy, 50 + panel_spacing*index))
                        self.engine.surface.blit(small_icon_panel, (x_position_enemy + 10,
                                                                    50 + unit_panel.get_height()/2 - small_icon_panel.get_height()/2 + panel_spacing*index))
                        self.engine.surface.blit(unit.sprite.image, (x_position_enemy + 11 + small_icon_panel.get_width()/2 - unit.sprite.image.get_width()/2,
                                                                    50 + unit_panel.get_height()/2 - unit.sprite.image.get_height()/2 + panel_spacing*index))

                        # Draw the unit's name and level
                        self.engine.surface.blit(name_panel, (x_position_enemy + 60,
                                                                    60 + panel_spacing*index))
                        self.engine.surface.blit(enemy_units_names[index + shift_enemy], (x_position_enemy + 60 + name_panel.get_width()/2 - enemy_units_names[index + shift_enemy].get_width()/2,
                                                                                        60 + name_panel.get_height()/2 - enemy_units_names[index + shift_enemy].get_height()/2 + panel_spacing*index))
                        self.engine.surface.blit(level_panel, (x_position_enemy + 220,
                                                                    60 + panel_spacing*index))
                        self.engine.surface.blit(text_lv, (x_position_enemy + 229,
                                                                62 + level_panel.get_height()/2 - text_lv.get_height()/2 + index*panel_spacing))
                        self.engine.surface.blit(enemy_units_levels[index + shift_enemy], (x_position_enemy + 220 + level_panel.get_width()*3/4 - enemy_units_levels[index + shift_enemy].get_width()/2,
                                                                60 + level_panel.get_height()/2 - enemy_units_levels[index + shift_enemy].get_height()/2  + index*panel_spacing))

                        # Draws the icon for the spell and the name of the spell
                        self.engine.surface.blit(small_icon_panel, (x_position_enemy + 60,
                                                                    100 + panel_spacing*index))
                        if unit.spell_actions[unit.equipped]:
                            self.engine.surface.blit(enemy_spell_icons[index + shift_enemy], (x_position_enemy + 60 + small_icon_panel.get_width()/2 - enemy_spell_icons[index + shift_enemy].get_width()/2,
                                                                        100 + small_icon_panel.get_height()/2
                                                                        - enemy_spell_icons[index + shift_enemy].get_height()/2 + panel_spacing*index))
                        self.engine.surface.blit(spell_panel, (x_position_enemy + 111, 102 + panel_spacing*index))
                        self.engine.surface.blit(enemy_units_spells[index + shift_enemy], (x_position_enemy + 111 + spell_panel.get_width()/2 - enemy_units_spells[index + shift_enemy].get_width()/2,
                                                                                         102 + spell_panel.get_height()/2 - enemy_units_spells[index + shift_enemy].get_height()/2 + panel_spacing*index))

                    # Only draws a scroll bar if the number displayed simultaneously is smaller than the total number units

                    # Scroll bar for ally side
                    if MAX_UNITS < len(self.team1):

                        self.engine.surface.blit(scroll_bar, (355, 50))
                        if shift_ally == len(self.team1)-MAX_UNITS:
                            self.engine.surface.blit(scroll_bar_ally, (355, 50 + SCROLL_BAR_LENGTH - scroll_section_height_ally))
                        else:
                            self.engine.surface.blit(scroll_bar_ally, (355, 50 + scroll_delta_ally*shift_ally))

                    # Scroll bar for enemy side
                    if MAX_UNITS < len(self.team2):

                        self.engine.surface.blit(scroll_bar, (775, 50))
                        if shift_enemy == len(self.team2)-MAX_UNITS:
                            self.engine.surface.blit(scroll_bar_enemy, (775, 50 + SCROLL_BAR_LENGTH - scroll_section_height_enemy))
                        else:
                            self.engine.surface.blit(scroll_bar_enemy, (775, 50 + scroll_delta_enemy*shift_enemy))

                    # Draws a border box around the selected unit
                    if menu_pos[0] == 0:
                        padlib_rounded_rect(self.engine.surface, selected_color, (x_position_ally - 2,
                                                             48 + (menu_pos[1]-shift_ally)*panel_spacing, unit_panel.get_width() + 4, unit_panel.get_height()+4), 6, 5)
                    else:
                        padlib_rounded_rect(self.engine.surface, selected_color, (x_position_enemy - 2,
                                                             48 + (menu_pos[1]-shift_enemy)*panel_spacing, unit_panel.get_width() + 4, unit_panel.get_height()+4), 6, 5)


                    pygame.display.flip()

                    update = False

                self.engine.clock.tick(60)

        # Does not automatically exits the map_menu loop
        return False

    def stats_interface(self, unit):

        if unit.team == 1:
            team = self.team1
        else:
            team = self.team2

        # Records the unit's position in the team list
        index = team.index(unit)

        menu_flag = True
        # page 0 (traits), page 1 (stats, default), page 2 (spells)
        page = 1

        while menu_flag:

            # Calls a unit's stats data loop

            if page == 0:
                event = unit.traits_stats_loop()
            elif page == 1:
                event = unit.stats_loop()
            else:
                event = unit.spell_stats_loop()

            if event.key == K_x:
                menu_flag = False

            # Up and down keys traverse the list of units in a team
            elif event.key == K_DOWN:
                index += 1
                if index > len(team)-1:
                    index = 0
                self.engine.fade_to('black', 0.10)
                unit = team[index]
            elif event.key == K_UP:
                index -= 1
                if index < 0:
                    index = len(team)- 1
                unit = team[index]
                self.engine.fade_to('black', 0.10)
            elif event.key == K_LEFT:
                page -= 1
                if page < 0:
                    page = 2
                self.engine.fade_to('black', 0.10)
            elif event.key == K_RIGHT:
                page += 1
                if page > 2:
                    page = 0
                self.engine.fade_to('black', 0.10)


    def trait_turn_process(self, team):
        """
        # Function Name: trait_turn_process
        # Purpose: For every unit in a team, processes their "Every Turn" traits
        # Inputs: Team (team1, team2)
        """

        for unit in team:
            # Checks action
            for trait in unit.traits:
                if trait and "Every Turn" in trait.properties and trait.turn_check(unit):

                    self.center_on(unit)
                    self.render_background()
                    self.render_all_units()
                    self.render_cursor()
                    pygame.display.flip()
                    trait.turn_execute(unit)

    def mission_end(self):

        """
        # Function Name: Mission end
        # Purpose: Process post map reset stuff. At the end of each battle, resets each unit's HP/Spirit settings,
        #           and de-associates them with the map
        """

        for unit in self.all_units_total.values():

            unit.HP = unit.maxHP
            unit.alive = True
            unit.spirit = 300
            unit.map = None
            unit.ressurected = False
            unit.spirit_stats = 'normal'
            unit.clear_status()
            unit.draw_status = 0
            unit.proxy_units = 0
            unit.equipped = 0
            # Fully recharges any spell card class
            for spell in unit.spell_actions:
                if spell and spell.consumable == False:
                    spell.livesleft = spell.lives


class Landmark(object):

    def __init__(self, name, location, size, img_coords, can_pass):

        """
        # Function Name: __init__
        # Purpose: Creates a landmark object
        # Inputs: Name - the name of the object
        #         Img_coords - coordinates (X, Y) within the landmarks image file
        #         Size: Size of the object in (X, Y) tiles
        #         Location: Top Left coordinate of the image
        #         Can_pass: whether the landmark can be passed through
        """
        self.name = name
        self.location = Vector2(location)
        self.location_pixel = self.location*35
        size_x, size_y = size
        self.size = Vector2(size)
        self.occupied_tiles = []
        [self.occupied_tiles.append((int(self.location.x+delta_x), int(self.location.y+delta_y))) for delta_x in xrange(0, size_x) for delta_y in xrange(0, size_y)]

        self.img_coords = Vector2(img_coords)
        self.can_pass = can_pass

    def render(self):

        """
        # Function Name: render
        # Purpose: draws the landmark on the screen at its location
        """

        x, y = self.location_pixel
        self.map.engine.surface.blit(self.map.engine.landmark_img, ((x, y)-self.map.screen_shift*35), (self.img_coords.x, self.img_coords.y, 35*self.size.x, 35*self.size.y))

class LightSource(Landmark):

    def __init__(self, name, location, lit_state, light_range):
        """
        function name:        __init__
        purpose: initiates a light source
        inputs:     name - name of light source
                    location - (x,y) location for light source
                    lit_state - starting lit state for source
                    light_range - range where light can reach
        """


        self.lit = lit_state
        self.light_range = light_range

        # Lantern image position
        self.unlit_image = Vector2(35*4,35)
        self.lit_image = Vector2(35*5,35)

        # Update image state
        if self.lit:
            img_coords = self.lit_image
        else:
            img_coords = self.unlit_image

        can_pass = True

        Landmark.__init__(self, name, location, (1,1), img_coords, can_pass)
        self.lit_tiles = self.generate_range()

    def generate_range(self):
        """
        Function name: Generate range
        Purpose: generates the range of tiles for this light source
        Output: list of tiles this light source covers

        """

        # Calculates the position deltas first
        deltas = []

        for diagonal_row_num in xrange(0, self.light_range + 1):
            for index in xrange(0, diagonal_row_num + 1):
                deltas.append((diagonal_row_num-index, index))


        # generates the valid moveset for 2nd, 3rd, 4th quadrants
        for coord in list(deltas):

            deltas.append((-coord[0], coord[1]))
            deltas.append((-coord[0], -coord[1]))
            deltas.append((coord[0], -coord[1]))

        lit_tiles = []

        # Computes the final set of coordinates from the deltas by doing a vector addition to the
        # light source's range
        for coord in deltas:
            lit_tiles.append(self.location+Vector2(coord))

        return lit_tiles


    def switch_state(self, state):
        """
        Function: switch_state
        Purpose: turns the light source on and off.
        """

        self.lit = state

        # Update image
        if self.lit:
            self.img_coords = self.lit_image
        else:
            self.img_coords = self.unlit_image

        # Asks map to update the entire fog map.
        self.map.update_fog_map()

class TemporaryLightSource(LightSource):

    def __init__(self, name, location, light_range):
        """
        A type of light source that lasts one turn
        """

        lit_state = True
        LightSource.__init__(self, name, location, lit_state, light_range)

        self.img_coords = Vector2(35*6,35*2)


class SpiritSourcePoint(Landmark):

    def __init__(self, name, location, preset):
        """
        # Function Name: __init__
        # Purpose: Creates a landmark object
        # Inputs: Name - the name of the object
        #         Location: coordinates of SSP
        #         Preset:  Preset capture state (0 unclaimed, 1 ally, 2 enemy)
        """

        self.name = name
        self.location = Vector2(location)

        # Capture state of the location:
            # 0 - Unclaimed
            # 1 - Ally
            # 2 - Enemy
        self.capture_state = preset
        self.starting_state = preset
        Landmark.__init__(self, name, location, (1, 1), (0, 105), True)

    def render(self):

        """
        # Function Name: render
        # Purpose: draws the landmark on the screen at its location
        """

        x, y = self.location_pixel
        if self.capture_state == 0:
            img_coords = (0, 70, 35, 35)
        elif self.capture_state == 1:
            img_coords = (35, 70, 35, 35)
        elif self.capture_state == 2:
            img_coords = (70, 70, 35, 35)

        #print [x, y, img_coords]

        self.map.engine.surface.blit(self.map.engine.landmark_img, ((x, y)-self.map.screen_shift*35), img_coords)

