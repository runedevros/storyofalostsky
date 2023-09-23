import pygame
from pygame.locals import *
from lostsky.core.linalg import Vector2
from lostsky.core.utils import padlib_rounded_rect, get_ui_panel
from lostsky.core.colors import panel_color, selected_color, disabled_color, border_color
from random import randint, choice
from sys import exit
from math import sin, cos, pi
import os



def get_catalog():
    catalog = {'TS Test Trait': Purify(),
               'Airlift': AirLift(),
               'Dizzy Attack': DizzyAttack(),
               'Cat\'s Curse': CatsCurse(),
               'Illusion Field': IllusionField(),
               'Focused Movement': FocusedMovement(),
               'Teleport': Teleport(),
               'Double Action': DoubleAction(),
               'Summon Doll': SummonDoll(),
               'Magic Fortress': MagicFortress(),
               'Field Medic': FieldMedic(),
               'Dispel History': DispelHistory(),
               'Unleash Grimoire': UnleashGrimoire(),
               'Purify': Purify(),
               'Self Destruct':SelfDestruct(),
               'Hypnotize':Hypnotize(),
               'Moonglow':Moonglow(),
               'Regeneration Field':RegenField(),
               'Poison Cloud':PoisonCloud(),
               'Secret Formula':SecretFormula(),
               'False Image':FalseImage(),
               'Antidote Cloud':AntidoteCloud(),
               'Moonstone Arrow':MoonstoneArrow(),
               'Reactivate':Reactivate(),
               'Portal Express':PortalExpress(),
               'Spirit Away':SpiritAway(),
               'Butterfly Storm':ButterflyStorm(),
                'Spirit Blossom':SpiritBlossom(),
                }
    return catalog


class Skill(object):

    def __init__(self, name, desc, sc_minimum, sc_cost):

        """
        Base class for all Trait Skills

        # Inputs:   name - name of trait
                    desc - description of trait
                    sc_minimum - minimum SC needed to use this trait
                    sc_cost - SC cost used in this trait

        """
        self.name = name
        self.desc = desc
        self.sc_minimum = sc_minimum
        self.sc_cost = sc_cost
        # Flag to show the range of this skill in the stats display
        self.show_range = False
        self.minrange = 0
        self.maxrange = 0

    def player_interface(self, unit):

        """
        Base class: no player interface available

        """
        pass


    def check_usability(self, unit):
        """
        Checks whether a unit can use a certain skill. Default is to check for enough spirit charge.
        """
        if unit.spirit >= self.sc_cost and unit.spirit >= self.sc_minimum:
            return True

    def check_criteria(self, unit, target):

        """
        Checks whether a given target is a valid selection for this skill
        """
        return False

    def generate_skill_range(self, minimum_range, maximum_range):

        """
        # Function Name: get_attack_range
        # Purpose: generates the valid range of attack tiles for a spell
        """

        validattacks = []

        # generates the valid moveset for 1st quadrant
        # General Pattern:
        #
        #  X123
        #  123
        #  23
        #  3
        #

        for diagonal_row_num in xrange(minimum_range, maximum_range+1):
            for index in xrange(0, diagonal_row_num+1):
                validattacks.append((diagonal_row_num-index, index))

        # generates the valid moveset for 2nd, 3rd, 4th quadrants
        for coord in list(validattacks):

            validattacks.append((-coord[0], coord[1]))
            validattacks.append((-coord[0], -coord[1]))
            validattacks.append((coord[0], -coord[1]))

        # Removes duplicates
        return list(set(validattacks))


    def generate_move_range(self, unit, maximum_range):
        """
        Generates a movement range based on a given maximum number of tiles from the target. Used for teleport spells.
        """


        move_range = self.generate_skill_range(1, maximum_range)

        for destination in list(move_range):
            if unit.map.check_occupancy(destination):
                move_range.remove(destination)

        return move_range


    def plot_skill_range(self, unit, skill_range, tile_type):
        """
        # Function Name: plot_attack
        # Purpose: Plots the valid attack range for the skill
        # Inputs: input: selection_range -
        """

        for tile in skill_range:
            if tile_type == 'attack':
                unit.map.engine.surface.blit(unit.map.engine.attack_tile, (Vector2(tile)*35+unit.location_pixel-unit.map.screen_shift*35))
            elif tile_type == 'healing':
                unit.map.engine.surface.blit(unit.map.engine.heal_tile, (Vector2(tile)*35+unit.location_pixel-unit.map.screen_shift*35))
            elif tile_type == 'move':
                unit.map.engine.surface.blit(unit.map.engine.move_tile, (Vector2(tile)*35+unit.location_pixel-unit.map.screen_shift*35))



    def select_unit(self, unit, skill_range, tile_type):

        menu_flag = True
        unit.map.framenum = 0


        target_list = [candidate for candidate in unit.map.team1 + unit.map.team2 if self.check_criteria(unit, candidate)]
        current_target = 0
        if target_list:
            selected = target_list[0]
            unit.map.center_cursor(selected.location_tile)


        while menu_flag:

            arrowkeys = False
            if unit.map.framenum == 10:
                unit.map.framenum = 0
            unit.map.framenum += 1

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
                            unit.map.center_cursor(selected.location_tile)

                        elif event.key == K_RIGHT or event.key == K_DOWN:
                            if current_target == len(target_list) - 1:
                                current_target = 0
                            else:
                                current_target += 1

                            selected = target_list[current_target]
                            unit.map.center_cursor(selected.location_tile)

                    if event.key == K_x:
                        menu_flag = False
                        unit.map.center_on(unit)
                    if event.key == K_z or event.key == K_RETURN:

                        # If the Z key is pressed, it will calculate the vector between the current position
                        # of the cursor and the unit's location. If that vector is part of the valid moves,
                        # the unit is moved there.
                        if target_list:
                            return selected

            # Plots the valid attack tiles
            if menu_flag:

                pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                %(unit.map.cursor_pos.x, unit.map.cursor_pos.y, unit.map.screen_shift.x, unit.map.screen_shift.y))

                unit.map.render_background()
                self.plot_skill_range(unit, skill_range, tile_type)

                unit.map.render_all_units()
                unit.map.render_cursor()
                unit.map.engine.surface.blit(unit.map.engine.battle_board, (0, 490))
                unit.plot_stats()
                if target_list:
                    selected.plot_stats(rhs = True)

                pygame.display.flip()
                unit.map.engine.clock.tick(60)

    def select_nearby_units(self, unit, team, max_range):

        """
        Selects nearby units:

        Input:  unit - unit using this skill
                same_team - 'ally' for identify nearby allies, 'enemy' for identify nearby enemies, 'both'
        """


        if unit.team == 1:
            if team == 'ally':
                search_team = unit.map.team1
            elif team == 'enemy':
                search_team = unit.map.team2
            elif team == 'both':
                search_team = unit.map.team1 + unit.map.team2
            else:
                search_team = []

        else:
            if team == 'ally':
                search_team = unit.map.team2
            elif team == 'enemy':
                search_team = unit.map.team1
            elif team == 'both':
                search_team = unit.map.team1 + unit.map.team2
            else:
                search_team = []

        nearby_units = []

        search_range_delta = self.generate_skill_range(0, max_range)
        search_range_absolute = [unit.location_tile + Vector2(delta) for delta in search_range_delta]


        for target in search_team:
            if target.location_tile in search_range_absolute:
                nearby_units.append(target)

        return nearby_units


    def select_move(self, unit, move_range):

        """
        # Function Name: move_loop
        # Purpose: The unit's second level move loop:
        #      Allows the player to select where they want to move a unit
        # Output: moved_flag = True if a selection has been made, False if one has not been made
        """

        menu_flag = True
        unit.map.framenum = 0
        while menu_flag:
            # Frame counter for holding down the keys to move
            if unit.map.framenum == 10:
                unit.map.framenum = 0
            unit.map.framenum += 1

            arrowkeys = False
            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        unit.map.cursor_arrows(event)
                        arrowkeys = True
                        # Resets the frame counter
                        unit.map.framenum = 0

                    if event.key == K_x:
                        menu_flag = False

                        unit.map.center_on(unit)
                        return False

                    if event.key == K_z or event.key == K_RETURN:

                        # If the Z key is pressed, it will calculate the vector between the current position
                        # of the cursor and the unit's location. If that vector is part of the valid moves,
                        # the unit is moved there.
                        delta_pos = unit.map.cursor_pos - unit.location_tile
                        new_pos = unit.map.cursor_pos
                        if tuple(delta_pos) in move_range and not unit.map.check_occupancy(new_pos):
                            return new_pos


            # if there is not a tap detected, check if the key is being held down
            if arrowkeys == False and unit.map.framenum == 9:
                unit.map.cursor_arrows_hold()

            if menu_flag:
                pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                %(unit.map.cursor_pos.x, unit.map.cursor_pos.y, unit.map.screen_shift.x, unit.map.screen_shift.y))

                unit.map.render_background()

                self.plot_skill_range(unit, move_range, 'move')

                unit.map.render_all_units()
                unit.map.render_cursor()

                unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
                unit.map.render_current_terrain_data()

                # Checks if there is a unit underneath the cursor, and if there is, plots the unit's data.
                selected = False
                selected = unit.map.cursor_key_search()
                if selected is not False:
                    unit.map.all_units_by_name[selected].plot_stats()

                pygame.display.flip()
                unit.map.engine.clock.tick(60)

    def select_target_unrestricted(self, unit):
        """
        # Function Name: select_target_unrestricted
        # Purpose: Lets player select any tile on the map
        """

        menu_flag = True
        unit.map.framenum = 0
        while menu_flag:
            # Frame counter for holding down the keys to move
            if unit.map.framenum == 10:
                unit.map.framenum = 0
            unit.map.framenum += 1

            arrowkeys = False
            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        unit.map.cursor_arrows(event)
                        arrowkeys = True
                        # Resets the frame counter
                        unit.map.framenum = 0

                    if event.key == K_x:
                        unit.map.center_on(unit)
                        return False

                    if event.key == K_z or event.key == K_RETURN:

                        return unit.map.cursor_pos


            # if there is not a tap detected, check if the key is being held down
            if arrowkeys == False and unit.map.framenum == 9:
                unit.map.cursor_arrows_hold()

            if menu_flag:
                pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                %(unit.map.cursor_pos.x, unit.map.cursor_pos.y, unit.map.screen_shift.x, unit.map.screen_shift.y))

                unit.map.render_background()

                unit.map.render_all_units()
                unit.map.render_cursor()

                unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
                unit.map.render_current_terrain_data()

                # Checks if there is a unit underneath the cursor, and if there is, plots the unit's data.
                selected = unit.map.cursor_key_search()
                if selected is not False:
                    unit.map.all_units_by_name[selected].plot_stats()

                pygame.display.flip()
                unit.map.engine.clock.tick(60)



    def confirm_proximity_action(self, unit, target_list, skill_range, tile_type):


        text_name = unit.map.engine.speaker_font.render(self.name, True, (0, 0, 0) )
        if text_name.get_width()  > 160:
            text_name = unit.map.engine.sfont.render(self.name, True, (0, 0, 0) )

        text_yes = unit.map.engine.section_font.render('Confirm', True, (0, 0, 0) )
        text_no = unit.map.engine.section_font.render('Cancel', True, (0, 0, 0) )

        name_panel = get_ui_panel((180, 35), border_color, panel_color)
        name_panel.blit(text_name, (name_panel.get_width()/2 - text_name.get_width()/2,
                                    name_panel.get_height()/2 - text_name.get_height()/2))

        options_panel =  get_ui_panel((140, 35), border_color, panel_color)
        disabled_panel = get_ui_panel((140, 35), border_color, disabled_color)

        confirm_action = True

        menu_flag = True
        while menu_flag:
            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        confirm_action = not confirm_action
                    if event.key == K_x:
                        unit.map.center_on(unit)
                        return False

                    if event.key == K_z or event.key == K_RETURN:
                        # Can only confirm if targets are actually present
                        if target_list:
                            unit.map.center_on(unit)
                            return confirm_action
                        elif not confirm_action:
                            unit.map.center_on(unit)
                            return False
                        else:
                            pass

            if menu_flag:
                pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                %(unit.map.cursor_pos.x, unit.map.cursor_pos.y, unit.map.screen_shift.x, unit.map.screen_shift.y))

                unit.map.render_background()

                self.plot_skill_range(unit, skill_range, tile_type)
                unit.map.render_all_units()


                for target in target_list:
                    unit.map.cursor_pos = target.location_tile
                    unit.map.render_cursor()

                unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))

                # If unit is on the one side of the screen currently, draw the menu on the opposite side.
                if unit.location_pixel.x - unit.map.screen_shift.x*35 > 420:
                    menu_x = 35
                else:
                    menu_x = 840 - unit.map.engine.vertical_panel.get_width() - 35

                unit.map.engine.surface.blit(unit.map.engine.vertical_panel, (menu_x, 175), (0, 0, 280, 140))
                unit.map.engine.surface.blit(name_panel, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - name_panel.get_width()/2,
                                                             185))


                if target_list:
                    unit.map.engine.surface.blit(options_panel, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2,
                                                             225))
                else:
                    unit.map.engine.surface.blit(disabled_panel, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2,
                                                             225))
                unit.map.engine.surface.blit(text_yes, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - text_yes.get_width()/2,
                                                            227 + options_panel.get_height()/2 - text_yes.get_height()/2 ))


                unit.map.engine.surface.blit(options_panel, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2,
                                                         270))
                unit.map.engine.surface.blit(text_no, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - text_no.get_width()/2,
                                                            272 + options_panel.get_height()/2 - text_no.get_height()/2 ))

                if confirm_action:
                    padlib_rounded_rect(unit.map.engine.surface, selected_color, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2 - 2,
                                                             223, 140 + 4, 35 + 4), 6, 5)
                else:
                    padlib_rounded_rect(unit.map.engine.surface, selected_color, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2 - 2,
                                                             268, 140 + 4, 35 + 4), 6, 5)


                # Checks if there is a unit underneath the cursor, and if there is, plots the unit's data.
                selected = unit.map.cursor_key_search()
                if selected is not False:
                    unit.map.all_units_by_name[selected].plot_stats()

                pygame.display.flip()
                unit.map.engine.clock.tick(60)




    def confirm_generic_action(self, unit):
        """
        Function name: confirm_generic_action
        Purpose: Brings up a menu to confirm whether the unit wants to carry out the action.

        """


        text_name = unit.map.engine.speaker_font.render(self.name, True, (0, 0, 0) )
        if text_name.get_width()  > 160:
            text_name = unit.map.engine.sfont.render(self.name, True, (0, 0, 0) )

        text_yes = unit.map.engine.section_font.render('Confirm', True, (0, 0, 0) )
        text_no = unit.map.engine.section_font.render('Cancel', True, (0, 0, 0) )

        name_panel = get_ui_panel((180, 35), border_color, panel_color)
        name_panel.blit(text_name, (name_panel.get_width()/2 - text_name.get_width()/2,
                                    name_panel.get_height()/2 - text_name.get_height()/2))

        options_panel =  get_ui_panel((140, 35), border_color, panel_color)

        confirm_action = True

        menu_flag = True
        while menu_flag:
            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        confirm_action = not confirm_action
                    if event.key == K_x:
                        unit.map.center_on(unit)
                        return False

                    if event.key == K_z or event.key == K_RETURN:
                        unit.map.center_on(unit)
                        return confirm_action

            if menu_flag:
                pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                %(unit.map.cursor_pos.x, unit.map.cursor_pos.y, unit.map.screen_shift.x, unit.map.screen_shift.y))

                unit.map.render_background()

                unit.map.render_all_units()

                unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))

                # If unit is on the one side of the screen currently, draw the menu on the opposite side.
                if unit.location_pixel.x - unit.map.screen_shift.x*35 > 420:
                    menu_x = 35
                else:
                    menu_x = 840 - unit.map.engine.vertical_panel.get_width() - 35

                unit.map.engine.surface.blit(unit.map.engine.vertical_panel, (menu_x, 175), (0, 0, 280, 140))
                unit.map.engine.surface.blit(name_panel, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - name_panel.get_width()/2,
                                                             185))

                unit.map.engine.surface.blit(options_panel, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2,
                                                         225))
                unit.map.engine.surface.blit(text_yes, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - text_yes.get_width()/2,
                                                            227 + options_panel.get_height()/2 - text_yes.get_height()/2 ))


                unit.map.engine.surface.blit(options_panel, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2,
                                                         270))
                unit.map.engine.surface.blit(text_no, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - text_no.get_width()/2,
                                                            272 + options_panel.get_height()/2 - text_no.get_height()/2 ))

                if confirm_action:
                    padlib_rounded_rect(unit.map.engine.surface, selected_color, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2 - 2,
                                                             223, 140 + 4, 35 + 4), 6, 5)
                else:
                    padlib_rounded_rect(unit.map.engine.surface, selected_color, (menu_x + unit.map.engine.vertical_panel.get_width()/2 - options_panel.get_width()/2 - 2,
                                                             268, 140 + 4, 35 + 4), 6, 5)


                # Checks if there is a unit underneath the cursor, and if there is, plots the unit's data.
                selected = unit.map.cursor_key_search()
                if selected is not False:
                    unit.map.all_units_by_name[selected].plot_stats()

                pygame.display.flip()
                unit.map.engine.clock.tick(60)



class AirLift(Skill):

    def __init__(self):
        """

        function name: __init__

        purpose: initializes the Skill and defines relevant variables

        """


        desc = "Tengu Air Lift"
        name = "Air Lift"
        minimum = 0
        cost = 0
        Skill.__init__(self, name, desc, minimum, cost)
        self.show_range = True
        self.minrange = 1
        self.maxrange = 1


    def check_usability(self, unit):
        """
        Function name: check_usability:

        A unit can only use this skill if they have the trait property Flight and has not moved yet.
        """


        if unit.has_trait_property('Flight') and not unit.moved:
            return True
        else:
            return False


    def check_criteria(self, unit, target):
        """
        Function name: check_criteria: checks if a unit can be picked up.

        Inputs: unit, target
                unit - unit performing this action
                target - unit attempting to be picked up

        Checks whether unit is on the same team and is within the minimum specified range.


        """

        if target.team == unit.team:
            distance = (target.location_tile - unit.location_tile).get_magnitude()
            if distance >= self.minrange and distance <= self.maxrange:
                return True
            else:
                return False
        else:
            return False

    def player_interface(self, unit):
        """
        Function name: Player_interface

        Purpose: Method called in order for the player to carry out this skill.

        inputs: unit - unit performing this action

        output: T/F - whether this action was executed (T) or cancelled (F)
                EXP - how much EXP this unit gets

        """

        # A unit performing this action gains 0 EXP
        EXP = 0

        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        drop_range = self.generate_move_range(unit, 1)

        while True:


            passenger = self.select_unit(unit, skill_range, 'healing')

            if passenger:


                unit_old = unit.location_tile.copy()
                passenger_old = passenger.location_tile.copy()

                passenger.move_to(unit.location_tile)
                # Hides passenger temporarily
                passenger.update_location(-1, -1)

                unit.get_moves_path()

                move_aborted = False

                while not move_aborted:

                    destination = self.select_move(unit, unit.validmoves)

                    if destination:
                        unit.move_to(destination)

                        drop_aborted = False
                        while not drop_aborted:
                            drop_destination = self.select_move(unit, drop_range)
                            if drop_destination:
                                passenger.update_location(*unit.location_tile)
                                passenger.move_to(drop_destination)
                                return True, EXP

                            else:
                                unit.move_to(unit_old)
                                drop_aborted = True

                    else:
                        unit.update_location(*unit_old)
                        passenger.update_location(*unit_old)
                        passenger.move_to(passenger_old)
                        move_aborted = True

            else:
                return False, 0


class DizzyAttack(Skill):

    def __init__(self):


        """
        function name: __init__


        purpose: initializes the Skill and defines relevant variables

        """


        desc = "Dizzy Attack test"
        name = "Dizzy Attack"
        minimum = 400
        cost = 100

        Skill.__init__(self, name, desc, minimum, cost)

        self.star_image = [pygame.image.load(os.path.join('images', 'bullets', 'star_blue.png')).convert_alpha(),
                      pygame.image.load(os.path.join('images', 'bullets', 'star_teal.png')).convert_alpha(),
                      pygame.image.load(os.path.join('images', 'bullets', 'star_red.png')).convert_alpha(),
                      pygame.image.load(os.path.join('images', 'bullets', 'star_green.png')).convert_alpha(),
                      ]

        self.show_range = True
        self.minrange = 0
        self.maxrange = 2


    def animation(self, unit, target):
        """
        function name: animation


        purpose: Draws stars exploding over the target.
        """

        star_group = pygame.sprite.RenderUpdates()

        num_stars = 5
        for i in xrange(0,num_stars):
            start_coord = target.location_pixel + Vector2(17,0) - 35* unit.map.screen_shift
            # Stars emtited from a 90 degree angle above target.
            angle = -1*(90-randint(-20,20))*3.14/180
            speed = 5
            velocity = speed*Vector2(cos(angle), sin(angle))

            star_group.add(StarSprite(choice(self.star_image), start_coord, velocity))


        # First Frame

        unit.map.render_background()
        unit.map.render_all_units()
        unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
        unit.map.engine.surface.blit(unit.map.engine.map_spell_board, (175, 0))
        unit.plot_stats()

        bg_surface = unit.map.engine.surface.copy()

        star_group.clear(unit.map.engine.surface, bg_surface)
        star_group.draw(unit.map.engine.surface)

        pygame.display.flip()
        unit.map.engine.clock.tick(60)


        for tick in xrange(0,60):

            star_group.clear(unit.map.engine.surface, bg_surface)
            star_group.update()

            rects = star_group.draw(unit.map.engine.surface)

            pygame.display.update(rects)
            unit.map.engine.clock.tick(60)



    def player_interface(self, unit):


        """
        Function name: Player_interface

        Purpose: Method called in order for the player to carry out this skill.

        inputs: unit - unit performing this action

        output: T/F - whether this action was executed (T) or cancelled (F)
                EXP - how much EXP this unit gets

        """

        target_list = self.select_nearby_units(unit, 'enemy', 2)
        target_list = [target for target in target_list if not target.invincible]
        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'attack')

        # 10EXP is awarded for each unit affected.
        EXP = 0

        if confirm_action:
            # User of this skill can also become dizzy
            target_list.append(unit)

            # 75% of making target dizzy
            for target in target_list:
                roll = randint(0, 100)
                if roll > 25 and 'Dizzy' not in target.status:

                    unit.map.engine.sfx_system.sound_catalog['hit'].play()
                    self.animation(unit, target)
                    target.give_status('Dizzy')
                    EXP += 10


            return True, EXP

        else:
            return False, 0

class StarSprite(pygame.sprite.Sprite):

    def __init__(self, image, position, velocity):
        """
        Sprite for star images used in Dizzy Attack's animation
        """

        # Gravity exerts a downward acceleration.
        self.acceleration = Vector2(0,0.3)

        self.velocity = velocity
        self.image = image
        self.floor = min(position.y+50, 490)
        self.rect = self.image.get_rect()
        self.float_position = position
        self.rect.center = (int(self.float_position.x),int(self.float_position.y))

        pygame.sprite.Sprite.__init__(self)

    def update(self):

        """
        Does an Euler's method update on position based on acceleration / velocity every time function is called.
        """

        self.velocity += self.acceleration
        self.float_position += self.velocity

        self.rect.center = (int(self.float_position.x),int(self.float_position.y))

        if self.rect.bottom > self.floor:
            self.kill()

class CatsCurse(Skill):

    def __init__(self):

        desc = "Cats Curse test"
        name = "Cat\'s Curse"
        minimum = 100
        cost = 100

        Skill.__init__(self, name, desc, minimum, cost)

        self.show_range = True
        self.minrange = 1
        self.maxrange = 2

    def player_interface(self, unit):

        """
        Function name: Player_interface

        Purpose: Method called in order for the player to carry out this skill.

        inputs: unit - unit performing this action

        output: T/F - whether this action was executed (T) or cancelled (F)
                EXP - how much EXP this unit gets

        """

        target_list = self.select_nearby_units(unit, 'enemy', 2)

        targets_with_pos_status = []
        for target in target_list:
            if target.status and not target.invincible:
                for status_name in target.status.keys():
                    if status_name != "High Spirit" and unit.map.engine.status_effects_catalog[status_name].positive_status:
                        targets_with_pos_status.append(target)
                        break


        # 10EXP is awarded for each unit affected.
        EXP = 10*len(targets_with_pos_status)


        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        confirm_action = self.confirm_proximity_action(unit, targets_with_pos_status, skill_range, 'attack')

        if confirm_action:
            # Erase all positive status effects on enemy units
            for target in targets_with_pos_status:
                for status_name in target.status.keys():
                    if unit.map.engine.status_effects_catalog[status_name].positive_status:
                        target.remove_status(status_name)

            return True, EXP

        else:
            return False, 0


class IllusionField(Skill):

    def __init__(self):

        desc = "Illusion Field"
        name = "Illusion Field"
        minimum = 400
        cost = 100

        Skill.__init__(self, name, desc, minimum, cost)
        self.show_range = True
        self.minrange = 1
        self.maxrange = 2

    def player_interface(self, unit):

        target_list = self.select_nearby_units(unit, 'ally', self.maxrange)

        target_list.remove(unit)
        skill_range = self.generate_skill_range(0, 2)
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'healing')


        # 10EXP is awarded for each unit affected.
        EXP = 10*len(target_list)

        if confirm_action:


            # Erase all positive status effects on enemy units
            for target in target_list:
                if 'Illusion Veil' not in target.status.keys():

                    unit.map.engine.sfx_system.sound_catalog['support1'].play()
                    unit.map.show_animation('magic_cast',target.location_tile)
                    target.give_status("Illusion Veil")

            return True, EXP

        else:
            return False, 0

class FocusedMovement(Skill):

    def __init__(self):

        desc = "focused movement test"
        name = "Focused Movement"
        minimum = 0
        cost = 0

        Skill.__init__(self, name, desc, minimum, cost)

    def check_usability(self, unit):
        """
        Focused Movement costs 0 points
        """

        return not unit.moved

    def player_interface(self, unit):

        # No EXP is awarded for this action

        unit.focused = True
        MOVEMENT_MULTIPLIER = 0.5

        # Temporarily stores current stats
        current_moves = unit.moves
        unit.moves = int(current_moves*MOVEMENT_MULTIPLIER)

        unit.get_moves_path()
        unit.move_loop()

        # Restores unit to original states
        unit.update_stats()
        unit.moves = current_moves
        unit.get_moves_path()
        unit.focused = False

        return False, 0


class Teleport(Skill):

    def __init__(self):

        desc = "teleport test"
        name = "Teleport"
        minimum = 300
        cost = 75

        Skill.__init__(self, name, desc, minimum, cost)

    def check_usability(self, unit):
        """
        Function: Check Usability
        Purpose: Checks if the unit has enough spirit charge for one use of teleport
        """

        if unit.spirit >= self.sc_cost and unit.spirit >= self.sc_minimum and not unit.moved:
            return True
        else:
            return False

    def player_interface(self, unit):
        """
        Player selects a location to teleport to. Ends turn.
        """
        # No EXP is gained from this action

        current_position_x, current_position_y = (unit.location_tile.x, unit.location_tile.y)
        move_range = self.generate_move_range(unit, unit.moves+2)
        new_pos = self.select_move(unit, move_range)
        if new_pos:

            unit.map.engine.fade_to('white', 0.1)
            unit.update_location(new_pos.x, new_pos.y)
            unit.map.engine.fade_from('white', 0.1)
            unit.moved = True
            unit.menu_loop(can_move = False, can_act = True)

            if unit.turnend:
                return True, 0
            else:
                unit.update_location(current_position_x, current_position_y)
                unit.map.cursor_pos.x, unit.map.cursor_pos.y = current_position_x, current_position_y
                unit.moved = False
                unit.map.center_on(unit)
                return False, 0
        else:
            return False, 0



class DoubleAction(Skill):

    def __init__(self):

        desc = "test"
        name = "Double Action"
        minimum = 500
        cost = 150
        self.minrange = 2
        self.maxrange = 6

        Skill.__init__(self, name, desc, minimum, cost)

    def check_usability(self, unit):
        """
        Checks condition for using
        """
        if unit.spirit >= self.sc_minimum:
            return True

    def check_criteria(self, unit, target):
        """
        Checks whether an opposing team's unit is in range
        """

        if target.team != unit.team:
            distance = (target.location_tile - unit.location_tile).get_magnitude()
            if distance >= self.minrange and distance <= self.maxrange:
                return True
            else:
                return False
        else:
            return False

    def player_interface(self, unit):


        # No EXP is gained from this action
        action_executed = unit.spell_loop_a()

        # Case for unit being killed on first counterattack: Do not go to the next step
        if not unit.alive:
            return True, 0

        if action_executed:
            action_executed = False
            # Once an action has been committed to, force unit to select a second move.
            while not action_executed:
                action_executed = unit.spell_loop_a()
            return True, 0
        else:
            return False, 0

class SummonDoll(Skill):

    def __init__(self):

        desc = "Summons dolls to the field"
        name = "Summon Doll"
        minimum = 400
        cost = 100
        self.minrange = 1
        self.maxrange = 2
        Skill.__init__(self, name, desc, minimum, cost)

    def check_usability(self, unit):
        return not unit.moved and unit.proxy_units < 2 and unit.spirit >= self.sc_cost and unit.spirit >= self.sc_minimum

    def player_interface(self, unit):
        """
        Player selects a location to summon to. Ends turn.
        """


        # No EXP is gained from this action

        current_position_x, current_position_y = (unit.location_tile.x, unit.location_tile.y)

        # Can only summon on empty square. I am hijacking move methods for this
        # Additionally, this prevents Alice from summoning a doll behind an enemy
        summon_range = self.generate_skill_range(1, 1)
        summon_pos  = self.select_move(unit, summon_range)

        if summon_pos:

            if unit.proxy_units is 0:
                unit_name = "Shanghai"
            else:
                unit_name = "Hourai"

            try:
                # Add to party
                # (copies from mapaction.add_temporary_ally

                doll = unit.map.engine.player_units_catalog[unit_name]

                #Note: for somereason, I don't have any attack abilities.
                unit.map.store_unit(doll, 1)

                # set doll to same level as Alice
                doll.level = unit.level
                doll.update_stats()
                doll.HP = doll.maxHP


                # Summoned unit does not act on same turn
                doll.turnend = False

                # Set Doll unit's parent unit
                doll.set_parentunit(unit)

                # Increment proxy_units by 1
                unit.proxy_units += 1

                print "Summoned %s!" % unit_name
            except KeyError:
                print "ERROR: Unit name mismatch in add to party subaction:", unit_name

            # Update summoned doll location
            try:
                doll.update_location(*summon_pos)
            except KeyError:
                print "ERROR: Unit name mismatch in set unit pos subaction", unit_name

            # Update summoned doll skills

            # Clears skills and traits
            doll.spell_actions = [None, None, None, None, None]
            doll.traits = [None, None, None, None, None]

            spell = "Fireball"
            try:
                doll.add_spell(unit.map.engine.spell_catalog[spell].construct_spell())
            except KeyError:
                print "ERROR: Unit name mismatch in assign_spell subaction", unit_name, spell

            doll.add_trait(unit.map.engine.trait_catalog['Self Destruct'])

            return True, 0
        else:
            return False, 0

class MagicFortress(Skill):

    def __init__(self):
        desc = 'Test'
        name = "Magic Fortress"
        minimum = 300
        cost = 50
        Skill.__init__(self, name, desc, minimum, cost)


    def player_interface(self, unit):

        # 10 EXP is gained for this action
        EXP = 10

        target_list = [unit]
        skill_range = []
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'healing')
        if confirm_action:

            unit.map.engine.sfx_system.sound_catalog['support1'].play()
            unit.map.show_animation('barrier_spell', unit.location_tile)

            unit.give_status('Magic Fortress')
            return True, 10
        else:
            return False, 10

class FieldMedic(Skill):

    def __init__(self):

        desc = 'test'
        name = "Field Medic"
        minimum = 400
        cost = 100
        Skill.__init__(self, name, desc, minimum, cost)
        self.show_range = True
        self.minrange = 0
        self.maxrange = 2


    def player_interface(self, unit):


        target_list = self.select_nearby_units(unit, 'ally', 2)
        target_list = [target for target in target_list if target.HP < target.maxHP]

        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'healing')


        # 10 EXP is gained per unit affected
        EXP = 10*len(target_list)

        if confirm_action:
            # User of this skill can also become dizzy
            target_list.append(unit)
            for target in target_list:
                if target.HP < target.maxHP:

                    # Heals 15% of target's max HP

                    unit.map.center_on(target)
                    starting_HP = target.HP
                    healing_amount = int(0.15*target.maxHP)

                    unit.map_heal(target, 'Field Medic', healing_amount)

            return True, EXP

        else:
            return False, EXP

class DispelHistory(Skill):

    def __init__(self):

        desc = 'test'
        name = "Dispel History"
        minimum = 400
        cost = 100
        Skill.__init__(self, name, desc, minimum, cost)

        self.show_range = True
        self.minrange = 1
        self.maxrange = 1


    def player_interface(self, unit):

        target_list = self.select_nearby_units(unit, 'ally', self.maxrange)

        targets_with_neg_status = []
        for target in target_list:
            if target.status:
                for status_name in target.status.keys():
                    if unit.map.engine.status_effects_catalog[status_name].type != "Other" and not unit.map.engine.status_effects_catalog[status_name].positive_status:
                        targets_with_neg_status.append(target)
                        break

        skill_range = self.generate_skill_range(0, 1)
        confirm_action = self.confirm_proximity_action(unit, targets_with_neg_status, skill_range, 'healing')


        # 10 EXP is gained per unit affected
        EXP = 10*len(targets_with_neg_status)

        if confirm_action:

            unit.map.engine.sfx_system.sound_catalog['heal'].play()
            unit.map.show_animation('healing_spell',unit.location_tile)

            # Removes all negative status effects of nearby allies
            target_list.append(unit)
            for target in target_list:
                for status in target.status.keys():
                    if not unit.map.engine.status_effects_catalog[status].positive_status and status != 'Low Spirit':
                        target.remove_status(status)

            return True, EXP

        else:
            return False, EXP

class UnleashGrimoire(Skill):

    def __init__(self):

        desc = "test"
        name = "Unleash Grimoire"
        minimum = 500
        cost = 500

        Skill.__init__(self, name, desc, minimum, cost)

    def check_usability(self, unit):
        """
        Checks condition for using
        """
        if unit.spirit >= self.sc_cost and unit.spirit >= self.sc_minimum and not unit.moved:
            return True
        else:
            return False


    def player_interface(self, unit):

        # No EXP gained from using this action

        unit.give_status('Mega Offense')

        action_executed = unit.spell_loop_a()
        if action_executed:

            unit.remove_status('Mega Offense')
            return True, 0
        else:

            unit.remove_status('Mega Offense')
            return False, 0

class Purify(Skill):


    def __init__(self):

        """
        Removes all negative status effects from user
        """

        desc = "test"
        name = "Purify"
        minimum = 400
        cost = 50

        self.yyorb_image = pygame.image.load(os.path.join('images','bullets', 'yyorb_red.png')).convert_alpha()

        Skill.__init__(self, name, desc, minimum, cost)


    def check_usability(self, unit):
        """
        Checks condition for using
        """

        # Checks that unit has enough SC and has an existing negative status effect
        if unit.spirit >= self.sc_cost and unit.spirit >= self.sc_minimum:
            for status_name in unit.status.keys():
                if not unit.map.engine.status_effects_catalog[status_name].positive_status and  unit.map.engine.status_effects_catalog[status_name].type != "Other":
                    return True
            else:
                return False
        else:
            return False

    def animation(self, unit):

        """
        name: animation
        Purpose: draws two Ying Yang orbs orbiting around Reimu
        """

        # Origin
        x_o = (unit.location_pixel.x+35/2-self.yyorb_image.get_width()/2)
        y_o = (unit.location_pixel.y+35/2-self.yyorb_image.get_height()/2)

        for i in xrange(0, 60):

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()

            unit.map.render_background()
            unit.map.render_all_units()
            unit.map.render_cursor()
            unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
            unit.map.engine.surface.blit(unit.map.engine.map_spell_board, (175, 0))
            unit.plot_stats()

            # parametric equations for circular orbit, orbitting twice over the 60 frame animation
            x1 = x_o+(60-i)*sin(i*3.14/15)
            y1 = y_o+(60-i)*cos(i*3.14/15)
            x2 = x_o+(60-i)*sin(3.14+i*3.14/15)
            y2 = y_o+(60-i)*cos(3.14+i*3.14/15)


            position_vector1 = Vector2(x1,y1)-35*unit.map.screen_shift
            position_vector2 = Vector2(x2,y2)-35*unit.map.screen_shift

            unit.map.engine.surface.blit(self.yyorb_image, (int(position_vector1.x), int(position_vector1.y)))
            unit.map.engine.surface.blit(self.yyorb_image, (int(position_vector2.x), int(position_vector2.y)))
            pygame.display.flip()
            unit.map.engine.clock.tick(60)


    def player_interface(self, unit):

        range = self.generate_skill_range(0, 0)

        # 10 EXP is awarded
        EXP = 10

        # Cures all negative status effects other than Low Spirit
        if self.confirm_proximity_action(unit, [unit], range, 'healing'):
            unit.map.engine.sfx_system.sound_catalog['support3'].play()
            self.animation(unit)
            for status_name in unit.status.keys():
                if not unit.map.engine.status_effects_catalog[status_name].positive_status and status_name != "Low Spirit":
                    unit.remove_status(status_name)

            return True, EXP

        else:
            return False, 0

class SelfDestruct(Skill):

    def __init__(self):

        """
        Blows up and does damage to adjacent units.
        """

        desc = "test"
        name = "Self Destruct"
        minimum = 0
        cost = 0

        Skill.__init__(self, name, desc, minimum, cost)

        self.show_range = True
        self.minrange = 1
        self.maxrange = 1


    def calculate_damage(self, unit, target):

        """
        Calculates the damage done to target
        """

        # Base effect is based on unit's magic stat
        base_effect = 4
        effect = unit.MAG*base_effect

        # Shield uses standard defense calculation for spell actions against physical defense
        target_total_mods = target.compute_total_stat_mods()

        # If the defender has no equipped spell or is holding an item, the default shield effect is 1
        if target.spell_actions[target.equipped]:

            # Shield calculation for physical damage type spells
            # Shield = (Defender's DEF + Defender's DEFmod) * Defender's Base Shield
            shield = (target.DEF*(1.0+target_total_mods[1]) + target.spell_actions[target.equipped].defmod)*target.spell_actions[target.equipped].shield

        else:
            # Shield calculation for physical damage type spells
            # Shield = (Defender's DEF)
            shield = (target.DEF*(1.0+target_total_mods[1]))

        # Final damage = Effect - Shield
        damage = effect - shield
        damage *= (1+unit.map.terrainmap[tuple(target.location_tile)][0].damage_mod / 100.0)

        return int(damage)

    def player_interface(self, unit):


        target_list = self.select_nearby_units(unit, 'both', self.maxrange)

        # Does not work on units with invincibility barrier.
        target_list = [target for target in target_list if not target.invincible]

        target_list.remove(unit)

        skill_range = self.generate_skill_range(1, 1)
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'attack')



        if confirm_action:

            unit.map.engine.sfx_system.sound_catalog['explode'].play()
            unit.map.engine.fade_to('white',1.0)
            unit.map.kill(unit)

            unit.map.render_background()
            unit.map.render_all_units()
            unit.map.render_cursor()
            unit.map.render_menu_panel()

            unit.map.engine.fade_from('white',1.0)

            # Erase all positive status effects on enemy units
            for target in target_list:
                damage = self.calculate_damage(unit, target)
                old_hp = target.HP
                target.HP -= damage
                if target.HP < 0:
                    target.HP = 0


                # Draw the effect of each target getting hit

                unit.map.engine.sfx_system.sound_catalog['hit'].play()
                effect_text = unit.map.engine.render_outlined_text(str(damage), unit.map.engine.cfont, (255, 0, 0), (255, 255, 255))

                unit.map.render_background()
                unit.map.render_all_units()
                unit.map.render_cursor()
                unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
                target.plot_stats()
                unit.map.engine.surface.blit(effect_text, ((target.location_pixel.x+18-effect_text.get_width()/2, target.location_pixel.y-25)-unit.map.screen_shift*unit.map.engine.tilesize))

                pygame.display.flip()
                unit.map.engine.clock.tick(60)
                unit.map.engine.pause(1)


                target.render_hp_change(old_hp, target.HP)

                if target.HP == 0:
                    target.alive = False
                    unit.map.kill(target, True)

            if unit.is_proxy_unit and unit.parentunit.alive:
                EXP = 0
                for target in target_list:
                    if target.team == 2:
                        # 10 EXP for target still alive
                        if target.alive:
                            EXP += 10
                        # 30 EXP for target defeated
                        else:
                            EXP += 30

                unit.parentunit.exp += EXP
                level_up = unit.parentunit.level_up_check()

                unit.parentunit.plot_results(unit.parentunit, EXP, level_up, 0, False, 0, 0, 0, 0)

            return True, 0

        else:
            return False, 0


class Hypnotize(Skill):

    def __init__(self):


        """
        function name: __init__
        purpose: initializes the Skill and defines relevant variables

        """
        desc = "Hypnotize"
        name = "Hypnotize"
        minimum = 350
        cost = 50

        Skill.__init__(self, name, desc, minimum, cost)


        self.show_range = True
        self.minrange = 1
        self.maxrange = 8

    def check_criteria(self, unit, target):

        distance = abs(target.location_tile.x - unit.location_tile.x) + abs(target.location_tile.y - unit.location_tile.y)
        if target.team != unit.team and 'Dizzy' not in target.status.keys() and distance <= self.maxrange:
            return True
        else:
            return False


    def animation(self, unit, target):

        # Draws a red orb doing a pendulum like motion in front of the target
        red_orb = pygame.image.load(os.path.join('images', 'bullets', 'smallorb_red.png')).convert_alpha()

        pi = 3.14
        x_o = (target.location_pixel.x+17)-red_orb.get_width()/2
        y_o = (target.location_pixel.y-15)-red_orb.get_height()/2

        # Four back and forth swings of the pendulum are shown
        for cycle_number in xrange(0,4):


            unit.map.engine.sfx_system.sound_catalog['shoot1'].play()

            for frame_number in xrange(0, 32):

                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                        exit()

                unit.map.render_background()
                unit.map.render_all_units()
                unit.map.render_cursor()
                unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
                unit.plot_stats()

                # If even cycle number, go left, otherwise, go the other way.
                # Equations given are the parametric equation of a circle, and we are iterating over a partial arc
                if cycle_number%2 == 0:

                    x = x_o+30*sin(frame_number*pi/64 - 16*pi/64)
                    y = y_o+30*cos(frame_number*pi/64 - 16*pi/64)
                else:
                    x = x_o+30*sin(-1*frame_number*pi/64 + 16*pi/64)
                    y = y_o+30*cos(-1*frame_number*pi/64 + 16*pi/64)

                unit.map.engine.surface.blit(red_orb, ((x, y)-unit.map.screen_shift*unit.map.engine.tilesize))
                pygame.display.flip()
                unit.map.engine.clock.tick(60)

    def player_interface(self, unit):

        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        selected = self.select_unit(unit, skill_range, 'attack')

        if selected:
            self.animation(unit, selected)
            selected.give_status('Dizzy')
            selected.get_moves_path()
            EXP = 10

            return True, EXP

        else:
            return False, 0

class Moonglow(Skill):

    def __init__(self):


        """
        function name: __init__


        purpose: initializes the Skill and defines relevant variables

        """


        desc = "Moonglow"
        name = "Moonglow"
        minimum = 400
        cost = 100

        Skill.__init__(self, name, desc, minimum, cost)

        self.show_range = True
        self.minrange = 1
        self.maxrange = 8

    def check_criteria(self, unit, target):
        distance = abs(target.location_tile.x - unit.location_tile.x) + abs(target.location_tile.y - unit.location_tile.y)

        if target.team != unit.team and 'Immobilize' not in target.status.keys() and distance <= self.maxrange:
            return True
        else:
            return False

    def player_interface(self, unit):

        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        selected = self.select_unit(unit, skill_range, 'attack')

        if selected:


            unit.map.engine.sfx_system.sound_catalog['shimmer'].play()
            unit.map.show_animation('red_spell', selected.location_tile+Vector2(0, -0.3))
            selected.give_status('Immobilize')
            selected.get_moves_path()
            EXP = 10

            return True, EXP

        else:
            return False, 0

class RegenField(Skill):

    def __init__(self):

        desc = "Regeneration Field"
        name = "Regeneration Field"
        minimum = 450
        cost = 150

        Skill.__init__(self, name, desc, minimum, cost)
        self.show_range = True
        self.minrange = 1
        self.maxrange = 2

    def player_interface(self, unit):

        target_list = self.select_nearby_units(unit, 'ally', self.maxrange)

        target_list.remove(unit)
        skill_range = self.generate_skill_range(0, 2)
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'healing')


        # 10EXP is awarded for each unit affected.
        EXP = 10*len(target_list)

        if confirm_action:


            # Erase all positive status effects on enemy units
            for target in target_list:
                if 'Life Bless' not in target.status.keys():

                    unit.map.engine.sfx_system.sound_catalog['support1'].play()
                    unit.map.show_animation('magic_cast',target.location_tile)
                    target.give_status("Life Bless")

            return True, EXP

        else:
            return False, 0

class PoisonCloud(Skill):

    def __init__(self):


        """
        function name: __init__


        purpose: initializes the Skill and defines relevant variables

        """


        desc = "Poison Cloud"
        name = "Poison Cloud"
        minimum = 400
        cost = 100

        Skill.__init__(self, name, desc, minimum, cost)

        self.show_range = True
        self.minrange = 1
        self.maxrange = 3

    def player_interface(self, unit):


        """
        Function name: Player_interface

        Purpose: Method called in order for the player to carry out this skill.

        inputs: unit - unit performing this action

        output: T/F - whether this action was executed (T) or cancelled (F)
                EXP - how much EXP this unit gets

        """

        target_list = self.select_nearby_units(unit, 'enemy', 2)
        target_list = [target for target in target_list if not target.invincible]
        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'attack')

        # 10EXP is awarded for each unit affected.
        EXP = 0

        if confirm_action:

            # 66% of poisoning target
            for target in target_list:
                roll = randint(0, 100)
                if roll > 34 and 'Poison' not in target.status:

                    unit.map.engine.sfx_system.sound_catalog['support3'].play()
                    unit.map.show_animation('magic_cast',target.location_tile)
                    target.give_status('Poison')
                    EXP += 10


            return True, EXP

        else:
            return False, 0


class PoisonCloud(Skill):

    def __init__(self):


        """
        function name: __init__


        purpose: initializes the Skill and defines relevant variables

        """


        desc = "Poison Cloud"
        name = "Poison Cloud"
        minimum = 400
        cost = 100

        Skill.__init__(self, name, desc, minimum, cost)

        self.show_range = True
        self.minrange = 1
        self.maxrange = 2

    def player_interface(self, unit):


        """
        Function name: Player_interface

        Purpose: Method called in order for the player to carry out this skill.

        inputs: unit - unit performing this action

        output: T/F - whether this action was executed (T) or cancelled (F)
                EXP - how much EXP this unit gets

        """

        target_list = self.select_nearby_units(unit, 'enemy', 2)
        target_list = [target for target in target_list if not target.invincible]
        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'attack')

        # 10EXP is awarded for each unit affected.
        EXP = 0

        if confirm_action:

            # 66% of poisoning target
            for target in target_list:
                roll = randint(0, 100)
                if roll > 34 and 'Poison' not in target.status:

                    unit.map.engine.sfx_system.sound_catalog['support3'].play()
                    unit.map.show_animation('magic_cast',target.location_tile)
                    target.give_status('Poison')
                    EXP += 10


            return True, EXP

        else:
            return False, 0

class SecretFormula(Skill):

    def __init__(self):


        """
        function name: __init__


        purpose: initializes the Skill and defines relevant variables

        """


        desc = "Secret Formula"
        name = "Secret Formula"
        minimum = 400
        cost = 150

        Skill.__init__(self, name, desc, minimum, cost)

        self.show_range = True
        self.minrange = 1
        self.maxrange = 3

    def player_interface(self, unit):


        """
        Function name: Player_interface

        Purpose: Method called in order for the player to carry out this skill.

        inputs: unit - unit performing this action

        output: T/F - whether this action was executed (T) or cancelled (F)
                EXP - how much EXP this unit gets

        """

        target_list = self.select_nearby_units(unit, 'both', 2)
        target_list.remove(unit)
        target_list = [target for target in target_list if not target.invincible]
        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'attack')

        # 10EXP is awarded for each unit affected.
        EXP = 0

        status_effect_list = ['Dizzy', 'Life Bless', 'Poison', 'Illusion Veil', 'Movement Down', 'Stun',
                              'STR Down', 'MAG Down', 'DEF Down', 'MDEF Down', 'Immobilize',
                              'Tracking Shot']


        if confirm_action:

            for target in target_list:

                status_applied = False

                # 33% chance of inflicting each status effect
                for status in status_effect_list:
                    roll = randint(0, 100)
                    if roll > 33 and status not in target.status:
                        target.give_status(status)
                        status_applied = True

                if status_applied:
                    unit.map.engine.sfx_system.sound_catalog['support2'].play()
                    unit.map.show_animation('magic_cast',target.location_tile)
                    EXP += 10

            return True, EXP

        else:
            return False, 0



class FalseImage(Skill):

    def __init__(self):
        desc = 'Test'
        name = "False Image"
        minimum = 300
        cost = 50
        Skill.__init__(self, name, desc, minimum, cost)


    def player_interface(self, unit):

        # 10 EXP is gained for this action
        EXP = 10

        target_list = [unit]
        skill_range = []
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'healing')
        if confirm_action:

            unit.map.engine.sfx_system.sound_catalog['support1'].play()
            unit.map.show_animation('barrier_spell', unit.location_tile)

            unit.give_status('Invisible')
            return True, 10
        else:
            return False, 10

class AntidoteCloud(Skill):

    def __init__(self):


        """
        function name: __init__


        purpose: initializes the Skill and defines relevant variables

        """


        desc = "Antidote Cloud"
        name = "Antidote Cloud"
        minimum = 400
        cost = 100

        Skill.__init__(self, name, desc, minimum, cost)

        self.show_range = True
        self.minrange = 1
        self.maxrange = 2


    def check_criteria(self, unit, target):

        """
        Checks whether a given target is a valid selection for this skill
        """
        if unit.team == target.team and "Poison" in target.status.keys():
            return True


    def player_interface(self, unit):


        """
        Function name: Player_interface

        Purpose: Method called in order for the player to carry out this skill.

        inputs: unit - unit performing this action

        output: T/F - whether this action was executed (T) or cancelled (F)
                EXP - how much EXP this unit gets

        """

        target_list = self.select_nearby_units(unit, 'ally', 2)
        target_list = [target for target in target_list if self.check_criteria(unit, target)]

        print [target.name for target in target_list]

        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'healing')

        # 10EXP is awarded for each unit affected.
        EXP = 0

        if confirm_action:

            for target in target_list:
                if "Poison" in target.status.keys():

                    unit.map.engine.sfx_system.sound_catalog['heal'].play()
                    unit.map.show_animation('healing_spell',unit.location_tile)
                    target.remove_status("Poison")
                    EXP += 10

            return True, EXP

        else:
            return False, 0


class MoonstoneArrow(Skill):

    def __init__(self):
        desc = 'Test'
        name = "Moonstone Arrow"
        minimum = 0
        cost = 0
        Skill.__init__(self, name, desc, minimum, cost)


    def player_interface(self, unit):

        # 10 EXP is gained for this action
        EXP = 10

        target = self.select_target_unrestricted(unit)
        if not target and target != (0, 0):
            return False, 0

        if self.confirm_generic_action(unit) :
            self.execute_action(unit, target)
            return True, EXP
        else:
            return False, 0

    def execute_action(self, unit, target):

        self.arrow_animation(unit, target)
        unit.map.engine.sfx_system.sound_catalog['heal'].play()
        unit.map.show_animation('light_spell',target)
        unit.map.add_temporary_light_source(target, 4)


        # First frame - Update entire screen and save as a background image
        unit.map.render_background()
        unit.map.render_menu_panel()
        if unit.map.enable_stats_panel:
            unit.plot_stats()
        unit.map.render_all_units()
        unit.map.render_cursor()
        pygame.display.flip()
        unit.map.engine.clock.tick(60)

        # Pause for 0.5s
        unit.map.engine.pause(0.5)

        unit.map.center_on(unit)
        unit.map.engine.pause(0.25)



    def select_target_unrestricted(self, unit):
        """
        # Function Name: select_target_unrestricted
        # Purpose: Lets player select any tile on the map
        """

        light_image = unit.map.engine.landmark_img.subsurface(35*6, 35*2, 35, 35)

        menu_flag = True
        unit.map.framenum = 0
        while menu_flag:
            # Frame counter for holding down the keys to move
            if unit.map.framenum == 10:
                unit.map.framenum = 0
            unit.map.framenum += 1

            arrowkeys = False
            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        unit.map.cursor_arrows(event)
                        arrowkeys = True
                        # Resets the frame counter
                        unit.map.framenum = 0

                    if event.key == K_x:
                        unit.map.center_on(unit)
                        return False

                    if event.key == K_z or event.key == K_RETURN:

                        return unit.map.cursor_pos


            # if there is not a tap detected, check if the key is being held down
            if arrowkeys == False and unit.map.framenum == 9:
                unit.map.cursor_arrows_hold()

            if menu_flag:
                pygame.display.set_caption("Story of a Lost Sky - Pos (%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                %(unit.map.cursor_pos.x, unit.map.cursor_pos.y, unit.map.screen_shift.x, unit.map.screen_shift.y))

                unit.map.render_background()

                unit.map.render_all_units()
                unit.map.render_cursor()

                unit.map.engine.surface.blit(light_image,
                                         (unit.map.cursor_pos*unit.map.engine.tilesize-unit.map.screen_shift*unit.map.engine.tilesize))

                unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
                unit.map.render_current_terrain_data()

                # Checks if there is a unit underneath the cursor, and if there is, plots the unit's data.
                selected = unit.map.cursor_key_search()
                if selected is not False:
                    unit.map.all_units_by_name[selected].plot_stats()


                pygame.display.flip()
                unit.map.engine.clock.tick(60)

    def arrow_animation(self, unit, target):

        unit.map.center_on(unit)

        unit.map.engine.sfx_system.sound_catalog['miss'].play()

        # Sets up the upward moving arrow
        up_arrow_image = pygame.image.load(os.path.join('images', 'bullets', 'arrow_yellow.png')).convert_alpha()
        down_arrow_image = pygame.transform.flip(up_arrow_image, False, True)
        start_position_up = unit.location_pixel - 35*unit.map.screen_shift + Vector2(35/2, 35/2)
        upward_velocity = Vector2(0, -13)
        upward_arrow = ArrowSprite(up_arrow_image, start_position_up, upward_velocity,)

        # First frame - Update entire screen and save as a background image
        unit.map.render_background()
        unit.map.render_menu_panel()
        if unit.map.enable_stats_panel:
            unit.plot_stats()
        unit.map.render_all_units()
        unit.map.render_cursor()
        pygame.display.flip()
        unit.map.engine.clock.tick(60)

        background_surface = unit.map.engine.surface.copy()

        arrow_group = pygame.sprite.RenderUpdates()
        arrow_group.add(upward_arrow)
        max_frames = 60

        # Draws the arrow
        for _ in xrange(0, max_frames):

            arrow_group.clear(unit.map.engine.surface, background_surface)
            arrow_group.update()
            rects = arrow_group.draw(unit.map.engine.surface)
            pygame.display.update(rects)
            unit.map.engine.clock.tick(60)

            # If arrow has reached its boundary limit, stop the loop
            if not arrow_group.has(upward_arrow):
                break


        # Pause for 0.5s
        unit.map.engine.pause(0.5)


        # Center on the target coordinate
        unit.map.center_cursor(target)

        # Set up the downward moving arrow
        start_position_down = 35*Vector2(target) - 35*unit.map.screen_shift + Vector2(35/2, 35/2)
        start_position_down.y = -35
        downward_velocity = Vector2(0, 13)
        downward_arrow = ArrowSprite(down_arrow_image, start_position_down, downward_velocity)
        downward_arrow.floor = target[1]*35 + 35  - 35*unit.map.screen_shift.y

        # Draws the first frame by updating the entire screen, and then save it as the background image.
        unit.map.render_background()
        unit.map.render_menu_panel()
        if unit.map.enable_stats_panel:
            unit.plot_stats()
        unit.map.render_all_units()
        unit.map.render_cursor()
        pygame.display.flip()
        unit.map.engine.clock.tick(60)
        background_surface = unit.map.engine.surface.copy()

        arrow_group = pygame.sprite.RenderUpdates()
        arrow_group.add(downward_arrow)
        max_frames = 60

        # Draw downward motion of arrow
        for _ in xrange(0, max_frames):

            arrow_group.clear(unit.map.engine.surface, background_surface)
            arrow_group.update()
            rects = arrow_group.draw(unit.map.engine.surface)
            pygame.display.update(rects)
            unit.map.engine.clock.tick(60)

            # If arrow has reached its boundary limit, stop the loop
            if not arrow_group.has(downward_arrow):
                break


class ArrowSprite(pygame.sprite.Sprite):

    def __init__(self, image, start_position, velocity):
        """
        Sprite for star images used in Moonstone Arrow's animation
        """

        # Gravity exerts a downward acceleration.

        self.velocity = velocity
        self.image = image
        self.floor = min(start_position.y+50, 490)
        self.ceiling = 0
        self.rect = self.image.get_rect()
        self.float_position = start_position
        self.rect.center = (int(self.float_position.x),int(self.float_position.y))

        pygame.sprite.Sprite.__init__(self)

    def update(self):

        """
        Does an Euler's method update on position based on velocity every time function is called.
        """

        self.float_position += self.velocity

        self.rect.center = (int(self.float_position.x),int(self.float_position.y))

        if (self.rect.bottom > self.floor and self.velocity.y > 0) or (self.rect.top < self.ceiling and self.velocity.y < 0):
            self.kill()

class Reactivate(Skill):

    def __init__(self):

        """
        Reactivate:
        """

        desc = 'Test'
        name = "Reactivate"
        minimum = 400
        cost = 100
        Skill.__init__(self, name, desc, minimum, cost)

    def check_usability(self, unit):



        if unit.spirit >= self.sc_cost and unit.spirit >= self.sc_minimum and not unit.moved:

            if ('Ran' in unit.map.all_units_by_name.keys() and unit.map.all_units_by_name['Ran'].turnend) or\
                ('Chen' in unit.map.all_units_by_name.keys() and  unit.map.all_units_by_name['Chen'].turnend):
                return True
            else:
                return False

        else:
            return False


    def player_interface(self, unit):

        # 10 EXP is gained for this action
        EXP = 10


        if self.confirm_generic_action(unit) :
            self.execute_action(unit)
            return True, EXP
        else:
            return False, 0

    def execute_action(self, unit):

        # Checks if Ran and Chen have moved
        if 'Ran' in unit.map.all_units_by_name.keys() and unit.map.all_units_by_name['Ran'].turnend:
            unit.map.all_units_by_name['Ran'].turnend = False

        if 'Chen' in unit.map.all_units_by_name.keys() and unit.map.all_units_by_name['Chen'].turnend:
            unit.map.all_units_by_name['Chen'].turnend = False

class PortalExpress(Skill):

    def __init__(self):

        desc = 'Test'
        name = "Portal Express"
        minimum = 0
        cost = 0
        Skill.__init__(self, name, desc, minimum, cost)

        self.minrange = 1
        self.maxrange = 10

    def check_criteria(self, unit, target):
        """
        Function name: check_criteria: checks if a unit can be picked up.

        Inputs: unit, target
                unit - unit performing this action
                target - unit attempting to be picked up

        Checks whether unit is on the same team and is within the minimum specified range.


        """

        if target.team == unit.team:
            distance = abs(target.location_tile.x - unit.location_tile.x) + abs(target.location_tile.y - unit.location_tile.y)
            if distance >= self.minrange and distance <= self.maxrange:
                return True
            else:
                return False
        else:
            return False

    def player_interface(self, unit):


        # A unit performing this action gains 0 EXP
        EXP = 0

        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        drop_range = self.generate_move_range(unit, 1)

        while True:


            passenger = self.select_unit(unit, skill_range, 'healing')

            if passenger:

                passenger_old = passenger.location_tile.copy()

                delta = Vector2(unit.location_tile) - Vector2(passenger.location_tile)
                passenger.render_walk([delta])
                # Hides passenger temporarily
                passenger.update_location(-1, -1)

                drop_aborted = False

                unit.map.center_cursor(unit.location_tile)
                while not drop_aborted:
                    drop_destination = self.select_move(unit, drop_range)
                    if drop_destination:
                        passenger.update_location(*unit.location_tile)
                        passenger.move_to(drop_destination)
                        return True, EXP

                    else:
                        passenger.update_location(*passenger_old)
                        drop_aborted = True

            else:
                return False, 0



class SpiritAway(Skill):

    def __init__(self):

        desc = 'Test'
        name = "Spirit Away"
        minimum = 300
        cost = 50
        Skill.__init__(self, name, desc, minimum, cost)

        self.minrange = 1
        self.maxrange = 7


    def check_usability(self, unit):
        """
        Checks whether a unit can use a certain skill. Default is to check for enough spirit charge.
        """
        if unit.spirit >= self.sc_cost and unit.spirit >= self.sc_minimum and not unit.moved:
            return True


    def check_criteria(self, unit, target):
        """
        Function name: check_criteria: checks if a unit can be picked up.

        Inputs: unit, target
                unit - unit performing this action
                target - unit attempting to be picked up

        Checks whether unit is on the same team and is within the minimum specified range.


        """

        if target.team != unit.team:
            distance = abs(target.location_tile.x - unit.location_tile.x) + abs(target.location_tile.y - unit.location_tile.y)
            if distance >= self.minrange and distance <= self.maxrange:
                return True
            else:
                return False
        else:
            return False

    def player_interface(self, unit):


        # A unit performing this action gains 0 EXP
        EXP = 15

        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        drop_range = self.generate_move_range(unit, 1)

        while True:


            passenger = self.select_unit(unit, skill_range, 'attack')

            if passenger:

                passenger_old = passenger.location_tile.copy()

                delta = Vector2(unit.location_tile) - Vector2(passenger.location_tile)
                passenger.render_walk([delta])
                # Hides passenger temporarily
                passenger.update_location(-1, -1)

                drop_aborted = False

                unit.map.cursor_pos = unit.location_tile.copy()
                while not drop_aborted:
                    drop_destination = self.select_move(unit, drop_range)
                    if drop_destination:
                        passenger.update_location(*unit.location_tile)
                        passenger.move_to(drop_destination)
                        unit.map.center_on(unit)
                        return True, EXP

                    else:
                        passenger.update_location(*passenger_old)
                        drop_aborted = True

            else:
                return False, 0

class ButterflyStorm(Skill):

    def __init__(self):


        """
        function name: __init__


        purpose: initializes the Skill and defines relevant variables

        """


        desc = "Butterfly Storm"
        name = "Butterfly Storm"
        minimum = 400
        cost = 50

        Skill.__init__(self, name, desc, minimum, cost)

        self.butterflies = [pygame.image.load(os.path.join('images', 'bullets', 'butterfly_orange.png')).convert_alpha(),
                            pygame.image.load(os.path.join('images', 'bullets', 'butterfly_magenta.png')).convert_alpha(),
                      ]

        self.show_range = True
        self.minrange = 1
        self.maxrange = 3


    def animation(self, unit):
        """
        function name: animation


        purpose: Draws stars exploding over the target.
        """

        # Shows the equipped bullet flying in a circle around the user
        # Uses parametric equation for a circle to animate




        # Origin
        x_o = (unit.location_pixel.x)
        y_o = (unit.location_pixel.y)

        for i in xrange(0, 60):

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()

            unit.map.render_background()
            unit.map.render_all_units()
            unit.map.render_cursor()
            unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
            unit.plot_stats()

            x1 = x_o+80*sin(i*pi/12)
            x2 = x_o-80*sin(i*pi/12)
            y1 = y_o+80*cos(i*pi/12)
            y2 = y_o-80*cos(i*pi/12)

            unit.map.engine.surface.blit(pygame.transform.rotate(self.butterflies[0], 180*i*pi/12), (Vector2(x1, y1) - unit.map.screen_shift*unit.map.engine.tilesize))
            unit.map.engine.surface.blit(pygame.transform.rotate(self.butterflies[1], -180*i*pi/12), (Vector2(x2, y2) - unit.map.screen_shift*unit.map.engine.tilesize))
            pygame.display.flip()
            unit.map.engine.clock.tick(60)


    def player_interface(self, unit):


        """
        Function name: Player_interface

        Purpose: Method called in order for the player to carry out this skill.

        inputs: unit - unit performing this action

        output: T/F - whether this action was executed (T) or cancelled (F)
                EXP - how much EXP this unit gets

        """
        damage_effect = 0.20

        target_list = self.select_nearby_units(unit, 'enemy', self.maxrange)
        target_list = [target for target in target_list if not target.invincible]
        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'attack')

        # 10EXP is awarded for each unit affected.
        EXP = 10

        total_damage = 0

        if confirm_action:
            # User of this skill can also become dizzy

            unit.map.engine.sfx_system.sound_catalog['shoot2'].play()
            self.animation(unit)

            for target in target_list:

                # Caps drain capability at 50 damage to prevent wrecking bosses in one shot
                damage = min(int(target.maxHP*damage_effect), 50)


                old_hp = target.HP
                target.HP -= damage
                if target.HP < 0:
                    target.HP = 0


                # Draw the effect of each target getting hit

                unit.map.engine.sfx_system.sound_catalog['hit'].play()
                effect_text = unit.map.engine.render_outlined_text(str(damage), unit.map.engine.cfont, (255, 0, 0), (255, 255, 255))

                unit.map.render_background()
                unit.map.render_all_units()
                unit.map.render_cursor()
                unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
                target.plot_stats()
                unit.map.engine.surface.blit(effect_text, ((target.location_pixel.x+18-effect_text.get_width()/2, target.location_pixel.y-25)-unit.map.screen_shift*unit.map.engine.tilesize))

                pygame.display.flip()
                unit.map.engine.clock.tick(60)
                unit.map.engine.pause(1)

                target.render_hp_change(old_hp, target.HP)

                EXP += 10

                total_damage += damage


            if unit.HP < unit.maxHP:
                recovery_multiplier = 0.5
                recovery = int(recovery_multiplier*total_damage)
                old_unit_HP = unit.HP
                unit.HP += recovery
                if unit.HP > unit.maxHP:
                    unit.HP = unit.maxHP


                # Draw the effect of each target getting hit

                unit.map.engine.sfx_system.sound_catalog['heal'].play()
                effect_text = unit.map.engine.render_outlined_text(str(recovery), unit.map.engine.cfont, (100, 255, 100), (0, 0, 0))

                unit.map.render_background()
                unit.map.render_all_units()
                unit.map.render_cursor()
                unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
                unit.plot_stats()
                unit.map.engine.surface.blit(effect_text, ((unit.location_pixel.x+18-effect_text.get_width()/2, unit.location_pixel.y-25)-unit.map.screen_shift*unit.map.engine.tilesize))

                pygame.display.flip()
                unit.map.engine.clock.tick(60)
                unit.map.engine.pause(1)

                unit.render_hp_change(old_unit_HP, unit.HP)


            return True, EXP

        else:
            return False, 0

class SpiritBlossom(Skill):

    def __init__(self):


        """
        function name: __init__


        purpose: initializes the Skill and defines relevant variables

        """


        desc = "Spirit Blossom"
        name = "Spirit Blossom"
        minimum = 300
        cost = 20

        Skill.__init__(self, name, desc, minimum, cost)

        self.sprite = pygame.image.load(os.path.join('images', 'bullets', 'crystal_magenta.png')).convert_alpha()
        self.show_range = True
        self.minrange = 1
        self.maxrange = 3


    def animation(self, unit):
        """
        function name: animation


        purpose: Draws stars exploding over the target.
        """

        # Shows the equipped bullet flying in a circle around the user
        # Uses parametric equation for a circle to animate

        x0 = unit.location_pixel.x
        y0 = unit.location_pixel.y

        for i in xrange(0, 60):

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()

            unit.map.render_background()
            unit.map.render_all_units()
            unit.map.render_cursor()
            unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
            unit.plot_stats()

            x1 = x0+(40+3*i)*sin(i*pi/12)
            y1 = y0+(40+3*i)*cos(i*pi/12)
            x2 = x0-(20+2*i)*sin(i*pi/12)
            y2 = y0-(20+2*i)*cos(i*pi/12)
            x3 = x0-(60+2*i)*sin(i*pi/12)
            y3 = y0-(60+2*i)*cos(i*pi/12)

            unit.map.engine.surface.blit(pygame.transform.rotate(self.sprite, 180*i*pi/12), (Vector2(x1, y1) - unit.map.screen_shift*unit.map.engine.tilesize))
            unit.map.engine.surface.blit(pygame.transform.rotate(self.sprite, 180*i*pi/12), (Vector2(x3, y3) - unit.map.screen_shift*unit.map.engine.tilesize))
            unit.map.engine.surface.blit(pygame.transform.rotate(self.sprite, -180*i*pi/12), (Vector2(x2, y2) - unit.map.screen_shift*unit.map.engine.tilesize))
            pygame.display.flip()
            unit.map.engine.clock.tick(60)


    def player_interface(self, unit):


        """
        Function name: Player_interface

        Purpose: Method called in order for the player to carry out this skill.

        inputs: unit - unit performing this action

        output: T/F - whether this action was executed (T) or cancelled (F)
                EXP - how much EXP this unit gets

        """
        damage_effect = 0.20

        target_list = self.select_nearby_units(unit, 'enemy', self.maxrange)
        target_list = [target for target in target_list if not target.invincible]
        skill_range = self.generate_skill_range(self.minrange, self.maxrange)
        confirm_action = self.confirm_proximity_action(unit, target_list, skill_range, 'attack')

        # 10EXP is awarded for each unit affected.
        EXP = 10

        total_damage = 0

        if confirm_action:
            # User of this skill can also become dizzy

            unit.map.engine.sfx_system.sound_catalog['fire'].play()
            self.animation(unit)

            for target in target_list:

                damage = 50

                old_sc = target.spirit
                target.spirit -= damage
                if target.spirit < 0:
                    target.spirit = 0


                # Draw the effect of each target getting hit
                target.render_sc_change(old_sc, target.spirit)

                EXP += 10

                total_damage += damage


            if unit.spirit < 900:
                recovery_multiplier = 0.75
                recovery = int(recovery_multiplier*total_damage)
                old_unit_SC = unit.spirit
                unit.spirit += recovery
                if unit.spirit > 900:
                    unit.spirit = 900


                # Draw the effect of each target getting hit

                unit.map.engine.sfx_system.sound_catalog['heal'].play()
                effect_text = unit.map.engine.render_outlined_text(str(recovery), unit.map.engine.cfont, (255, 100, 255), (0, 0, 0))

                unit.map.render_background()
                unit.map.render_all_units()
                unit.map.render_cursor()
                unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
                unit.plot_stats()
                unit.map.engine.surface.blit(effect_text, ((unit.location_pixel.x+18-effect_text.get_width()/2, unit.location_pixel.y-25)-unit.map.screen_shift*unit.map.engine.tilesize))

                pygame.display.flip()
                unit.map.engine.clock.tick(60)
                unit.map.engine.pause(1)

                unit.render_sc_change(old_unit_SC, unit.spirit)


            return True, EXP

        else:
            return False, 0