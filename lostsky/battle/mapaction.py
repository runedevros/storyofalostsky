import pygame
import os
from random import choice
from lostsky.core.linalg import Vector2

class MapActionEvent(object):
    #############################
    # Map action event class
    # Purpose: handles scripting of events on the battle map
    #############################


    def __init__(self, triggers, repeat = False):
        """
        # function name = __init__
        # Purpose: Creates a map action event
        # Inputs:   Triggers - conditions necessary for the triggering of an event
        #           Repeat - T/F if a MAE is to be activated once every turn cycle
        """

        self.triggers = []
        [self.add_trigger(trigger) for trigger in triggers]
        self.map = None
        self.done = False
        self.repeat = repeat

    def add_trigger(self, trigger):
        """
        # function name = add_trigger
        # Purpose: Adds a trigger
        # Inputs:   Trigger - condition necessary for the triggering of an event
        """

        self.triggers.append(trigger)
        trigger.MAE_parent = self

    def check_triggers(self):
        """
        # function name = check_triggers
        # Purpose: checks all triggers and calls the execute command if conditions are met
        """

        triggers_cleared = 0
        # checks all the triggers

        for trigger in self.triggers:
            if trigger.check_conditions() == True:
                triggers_cleared += 1
        if triggers_cleared == len(self.triggers):
            self.execute()
            self.done = True

    def pre_exec(self):
        """
        Function name: pre_exec
        Purpose: Runs some setup of the units on the map before the actual MAE begins. Call any actions that do not
        involve drawing things (e.g. setting unit HP and positions) here.
        """
        pass

    def execute(self):
        """
        # function name = execute
        # Purpose: executes all sub actions
        # Inherited classes of MapActionEvent should override this method
        """

        pass


    def choice(self, query, options):
        """
        # Function Name: Choice
        # Purpose: Allows the player to select a response to a query
        # Inputs: query - a string that describes the choice
        #         options - a list of strings representing possible selections (should be less than 4)
        # Outputs: response - the string the player has selected
        """
        return self.map.choice(query, options)

    def hide_image(self, id_string):
        """
        # Function Name: hide_image
        # Purpose: hides a conversation image
        # Inputs: id_string - conversation image's ID string
        """
        del(self.map.conv_images[id_string])


    def say(self, message, speaker, portrait):
        """
        # Function Name: say
        # Purpose: display a line of speech
        # Inputs: message - the body of the speech to say
        #         speaker - the name of the speaker of the message. Supply None for no speaker
        #         portrait - the ID string for the portrait to use for the message. Supply None for no speaker
        """

        self.map.say(message, speaker, portrait)


    def show_image(self, id_string, img_file, coords):
        """
        # Function Name: show_image
        # Purpose: display a conversation image
        # Inputs: id_string - a name to identify this image by. This is used to delete the image with the hide_image
        #         img_file - filename in /images/conversation_img of the image to display
        #         coords - (x, y) pixel coordinates of the top left corner to display the image
        """

        # If .png, use alpha channel
        if img_file.endswith('png'):
            img_surf = pygame.image.load(os.path.join('images', 'conversation_img', img_file)).convert_alpha()
        else:
            img_surf = pygame.image.load(os.path.join('images', 'conversation_img', img_file))

        self.map.conv_images[id_string] = [img_surf, coords]

    ################################
    # Map / Engine type Sub actions
    ################################

    def add_highlight(self, coords):
        """
        # function name - add_highlight
        # purpose: Draw a "here" indicator on the coordinates
        # input: coords - (x, y) map coordinates to highlight
        """
        self.map.all_highlighted_tiles.append(Vector2(coords))

    def add_item(self, item_type, item_id, quantity):
        """
        # function name - add_item
        # purpose: add an item to the player's inventory
        # input: item_type - either "treasure" or "spell_action"
        #        item_id - the ID string of the item
        #        quanity - how many to give
        """
        self.map.items_received.append([item_type, item_id, quantity])

    def add_recipe(self, recipe_name):

        """
        # function name - add_item
        # purpose: adds a new recipe to the player's list of known recipes
        # input: recipe_name - ID string of the recipe
        """
        self.map.engine.spell_synthesis_system.add_recipe(recipe_name)

    def center_on(self, unit):
        """
        # function name: center_on
        # purpose: center on a unit
        # Input: unit - unit to center on
        """
        try:
            self.map.center_on(self.map.all_units_by_name[unit], True)
        except IndexError:
            print "ERROR: Unit name mismatch in "+unit+" subaction"

    def center_on_coords(self, destination):
        """
        # function name: center_on_coords
        # purpose: center on a set of coordinates
        # Input: destination - (X, Y) map coordinates to center on
        """
        self.map.center_cursor(Vector2(destination), True)

    def fade_to_color(self, color, time):
        """
        # function_name: fade_to_color
        # input: color - either (R, G, B) or the special words 'black', 'white'
        #        time - how long (sec) this fade effect lasts
        """
        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.render_menu_panel()
        for conversation_image in self.map.conv_images.values():
            self.map.engine.surface.blit(conversation_image[0], conversation_image[1])
        self.map.engine.fade_to(color, time)

    def fade_from_color(self, color, time):
        """
        # function_name: fade_from_color
        # input: color - either (R, G, B) or the special words 'black', 'white'
        #        time - how long (sec) this fade effect lasts
        """
        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.render_menu_panel()
        for conversation_image in self.map.conv_images.values():
            self.map.engine.surface.blit(conversation_image[0], conversation_image[1])
        self.map.engine.fade_from(color, time)

    def pause(self, time):
        """
        # function_name: pause
        # input: time - duration of pause (seconds)
        """
        self.map.engine.pause(time)


    def play_music(self, id_string):
        """
        # function name: play_music
        # purpose: start playing a song
        # input: id_string - ID string identifying the song
        """
        self.map.engine.play_music(id_string)

    def play_sfx(self, id_string):
        """
        Function name: play_sfx
        Purpose: Plays a sound effect
        Input: sound effect name
        """

        self.map.engine.sfx_system.sound_catalog[id_string].play()

    def remove_all_enemies(self):
        """
        # function name: remove_all_enemies
        # purpose: Removes all enemies except for required survivors
        """
        [self.map.kill(unit) for unit in self.map.all_units_by_name.values()
            if unit in self.map.team2
            and unit.name not in self.map.required_survivors
            and unit.alive]

    def remove_highlight(self, coords):
        """
        # function name: remove_highlight
        # input: coords - (X, Y) map coordinates to remove highlight from
        """
        try:
            del(self.map.all_highlighted_tiles[self.map.all_highlighted_tiles.index(coords)])
        except IndexError:
            print "ERROR: Attempted to delete a non existing highlight tile"

    def set_bg_overlay(self, overlay):
        """
        # function name: set_bg_overlay
        # purpose: sets a tinted overlay of the battle map to represent
        #         different times of day
        # overlay - "sunset", "night", or None
        """
        if overlay:
            self.map.bg_overlay = overlay
        else:
            self.map.bg_overlay = False

    def set_cursor_state(self, show_cursor):
        """
        # set_cursor_state: set_cursor_state
        # purpose: show or hide the corsor
        # input: show_cursor - True or False as to whether to display the map cursor
        """
        self.map.enable_cursor = show_cursor

    def set_cust_var(self, cust_var_name, value):
        """
        # function_name: set_custom_variable
        # purpose: set the value of a custom variable for the map
        #          can be used to set flags if a certain event happened
        # inputs:  custom_var_name - name of the place to save the variable
        #          value - what value to set the custom variable to.
        """
        self.map.cust_var[cust_var_name] = value

    def set_ssp_state(self, ssp_name, capture_state):
        """
        function_name: set_ssp_state
        sets the Spirit Source point identified by ssp_name to capture_state
        capture state: 0 for unclaimed, 1 for player team, 2 for enemy team.
        """

        try:
            self.map.all_landmarks[ssp_name].capture_state = capture_state
        except KeyError:
            print "ERROR: Attempted to check a nonexistent SSP"

    def set_stats_display(self, enable_stats):
        """
        # function name: set_stats_display
        # purpose: Sets whether to show the stats panel during scenes
        # inputs: enable_stats - True / False as to whether to display the unit stats panel
        """
        self.map.enable_stats_panel = enable_stats

    def show_chapter_title(self, chapter_number):
        """
        # function name: show_chapter_title
        # chapter_number - Integer indicating what chapter number to display the title of (1 to 6)
        """
        if chapter_number > 5 or chapter_number < 1:
            print "Error: Select chapter between 1 and 5"
            return

        smoothstep = lambda v: (v*v*(3-2*v))

        # Positions for the vertical banner and horizontal image
        start_pos_pic = Vector2(-35, 140)
        start_pos_text = Vector2(840, 210)

        frame_count = 30
        step_vector_pic = Vector2(1, 0)
        step_vector_text = Vector2(-1, 0)
        for t in xrange(0, frame_count+1):
            v = float(t)/float(frame_count)
            v = smoothstep(v)
            scale_term_pic = int(395*v)
            scale_term_text = int(420*v)
            intermediate_step_pic = scale_term_pic*step_vector_pic
            intermediate_step_text = scale_term_text*step_vector_text
            current_pos_pic = start_pos_pic + intermediate_step_pic
            current_pos_text = start_pos_text + intermediate_step_text

            self.map.render_background()
            self.map.render_all_units()
            self.map.render_cursor()
            self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
            # Picture
            self.map.engine.surface.blit(self.map.engine.chapter_title, current_pos_pic, (35*(chapter_number-1), 0, 35, 175))

            # Chapter Number
            self.map.engine.surface.blit(self.map.engine.chapter_title, current_pos_text, (210, 35*(chapter_number-1), 140, 35))
            # Separator Image
            self.map.engine.surface.blit(self.map.engine.chapter_title, current_pos_text+Vector2(0, 35), (0, 175, 210, 35))
            # Chapter Title
            self.map.engine.surface.blit(self.map.engine.chapter_title, current_pos_text+Vector2(0, 70), (0, 175+35*(chapter_number), 420, 35))


            pygame.display.flip()
            self.map.engine.clock.tick(60)

        self.map.engine.pause(1.5)
        frame_count = 30

        # Renders image exit
        start_pos_pic = current_pos_pic.copy()
        start_pos_text = current_pos_text.copy()
        for t in xrange(0, frame_count+1):
            v = float(t)/float(frame_count)
            v = smoothstep(v)
            scale_term = int(730*v)
            intermediate_step_pic = scale_term*step_vector_pic
            intermediate_step_text = scale_term*step_vector_text
            current_pos_pic = start_pos_pic + intermediate_step_pic
            current_pos_text = start_pos_text + intermediate_step_text

            self.map.render_background()
            self.map.render_all_units()
            self.map.render_cursor()
            self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
            # Picture
            self.map.engine.surface.blit(self.map.engine.chapter_title, current_pos_pic, (35*(chapter_number-1), 0, 35, 175))

            # Chapter Number
            self.map.engine.surface.blit(self.map.engine.chapter_title, current_pos_text, (210, 35*(chapter_number-1), 140, 35))
            # Separator Image
            self.map.engine.surface.blit(self.map.engine.chapter_title, current_pos_text+Vector2(0, 35), (0, 175, 210, 35))
            # Chapter Title
            self.map.engine.surface.blit(self.map.engine.chapter_title, current_pos_text+Vector2(0, 70), (0, 175+35*(chapter_number), 210, 35))


            pygame.display.flip()
            self.map.engine.clock.tick(60)

    def show_animation(self, id_string, coords):
        """
        # function name: show_animation
        # purpose: display a prerendered animation
        # inputs: id_string - ID string identifying animation
        #         coords - (X, Y) map coordinates to display the animation
        """
        try:
            self.map.show_animation(id_string, coords)

        except KeyError:
            print "ERROR: Name Mismatch in show_animation: id_string: "+id_string



    def stop_music(self):
        """
        # function name: stop_music
        # purpose: stops any music playing
        """
        pygame.mixer.music.stop()

    def set_fog_state(self, fog_state):
        """
        function name: set fog state

        purpose: toggles fog on and off

        """

        self.map.enable_fog = fog_state
        self.map.update_fog_map()

    def set_lantern_state(self, lantern_id, lantern_state):
        """
        function name: set lantern state

        purpose: sets the lantern to be lit (True) or unlit (false)
        """

        try:
            self.map.all_landmarks[lantern_id].switch_state(lantern_state)
        except KeyError:
            print "Error! Lantern name incorrect"


    ################################
    # Unit type sub_actions
    #################################

    def add_to_party(self, unit_name):
        """
        # function_name: add_to_party
        # input: unit_name - Name of the unit to add to the party
        """
        try:
            print unit_name+" joined your party!"
            self.map.engine.player_units.append(self.map.engine.player_units_catalog[unit_name])
            self.map.engine.player_units_by_name[unit_name] = self.map.engine.player_units_catalog[unit_name]
            self.map.engine.player.add_unit_data(self.map.engine.player_units_catalog[unit_name])
            self.map.store_unit(self.map.engine.player_units_catalog[unit_name], 1)
            self.map.engine.player_units_catalog[unit_name].turnend = False
            self.map.new_party_members.append(self.map.engine.player_units_catalog[unit_name])

        except KeyError:
            print "ERROR: Unit name mismatch in add to party subaction: "+unit_name



    def add_temporary_ally(self, unit_name):
        """
        # function_name: add_temporary_ally
        # input: unit_name - Add a unit to the party only for the duration of the mission
        """
        try:
            print unit_name+" temporarily joined your party!"
            self.map.store_unit(self.map.engine.player_units_catalog[unit_name], 1)
            self.map.engine.player_units_catalog[unit_name].reset_state()
            self.map.engine.player_units_catalog[unit_name].turnend = False

        except KeyError:
            print "ERROR: Unit name mismatch in add temporary unit subaction: "+unit_name


    def assign_spell(self, unit_name, spell):
        """
        # function name: assign_spell
        # purpose: assigns a spell to a unit (Assuming the unit has a free spell slot)
        # input: unit_name - name of the unit to assign to
        #        spell - name of the spell to assign
        """
        try:
            self.map.all_units_by_name[unit_name].add_spell(self.map.engine.spell_catalog[spell].construct_spell())
        except KeyError:
            print "ERROR: Unit name mismatch in assign_spell subaction" + unit_name + " " + spell

    def assign_trait(self, unit_name, trait):
        """
        # function name: assign_trait
        # purpose: assign a trait to a unit
        # inputs: unit_name - name of the unit to assign to
        #         trait - name of the trait to assign
        """
        try:
            self.map.all_units_by_name[unit_name].add_trait(self.map.engine.trait_catalog[trait])
        except KeyError:
            print "ERROR: Unit name mismatch in assign trait subaction" + unit_name + " " + trait

    def emote(self, unit_name, id_string):
        """
        # function name: emote
        # purpose: display an emote animation over a unit
        # inputs: unit_name - name of unit to display animation over
        #         id_string - ID string identifying the emote animation
        """
        try:
            self.map.all_units_by_name[unit_name].render_emote(id_string)
        except KeyError:
            print "ERROR: Name mismatch in draw emote subaction. Unit: %s ; Emotion: %s" % (unit_name, id_string)

    def end_unit_turn(self, unit_name):
        """
        # function name: end_unit_turn
        # inputs: unit_name - unit to end the turn of
        # (Note: has no effect if unit has already finished its turn)
        """
        try:
            self.map.all_units_by_name[unit_name].turnend = True
        except KeyError:
            print "ERROR: Unit name mismatch in end unit turn subaction "+unit_name

    def deploy_unit(self, unit_name, destination):
        """
        # function_name: deploy_unit
        # purpose: Deploy a reserved unit to the map
        # inputs: unit_name - name of the unit to deploy
        #         destination - (X, Y) map coordinates to place the unit
        """
        try:
            if unit_name not in self.map.all_units_by_name.keys():


                self.map.store_unit(self.map.reserve_units[unit_name], 2)
                self.map.all_units_by_name[unit_name].turnend = False
                self.map.all_units_by_name[unit_name].update_location(*destination)
                self.map.all_units_by_name[unit_name].get_moves_path()


            else:
                print "UNIT %s ALREADY IN MAP!" % unit_name

        except KeyError:
            print "ERROR: Unit name mismatch in end unit turn subaction "+unit_name

    def kill_unit(self, unit_name):
        """
        # function name: kill_unit
        # purpose: Remove the unit from the map
        # inputs: unit_name - unit to remove
        """
        try:
            unit = self.map.all_units_total[unit_name]
            if unit.alive:
                unit.alive = False
                self.map.kill(unit)
                if unit.name not in self.map.required_survivors:
                    del(self.map.all_units_total[unit.name])
            else:
                print "ERROR: "+unit.name+" is already dead."
        except KeyError:
            print "ERROR: Unit name mismatch in kill unit subaction "+unit_name

    def move_unit(self, unit_name, destination):
        """
        # function name: move_unit
        # purpose: move a unit across the map
        # inputs: unit_name - name of unit to move
        #         destination - (X, Y) map coordinates of location to move to
        """
        try:
            if tuple(destination) != tuple(self.map.all_units_by_name[unit_name].location_tile):
                self.map.all_units_by_name[unit_name].move_to(destination)
        except KeyError:
            print "ERROR: Unit name mismatch in move unit subaction "+unit_name

    def random_teleport(self, unit_name, destination_box):
        """
        # function name: random_teleport
        # purpose: randomly teleports a unit to an unoccupied, traversible location in the map.
        # inputs: unit_name - name of the unit to teleport
        # destination: (X, Y, dx, dy) range
        """
        def check_walkable(coord):
            return self.map.terrainmap[coord][0].walk and self.map.terrainmap[coord][0].fly

        def check_unoccupied(coord):
            return not self.map.check_occupancy(coord)

        # generate valid teleportation slots

        x1, y1, x2, y2 = destination_box
        candidate_destinations = [(x1+delta_x, y1+delta_y) for delta_x in xrange(0, x2) for delta_y in xrange(0, y2)]

        unoccupied_destinations = filter(check_unoccupied, candidate_destinations)
        traversible_destinations = filter(check_walkable, unoccupied_destinations)

        if traversible_destinations:
            self.set_unit_pos(unit_name, choice(traversible_destinations))
        else:
            print "ERROR: No available positions to teleport to."

    def remove_spell(self, unit_name, spell_action):
        """
        # function name: remove_spell
        # purpose: remove one instance of a spell of a certain name from unit inventory
        # inputs: unit_name - name of unit to remove spell from
        #         spell_action - name of spell to remove
        """
        for spell_index, spell in self.map.all_units_by_name[unit_name].spell_actions.items():
            if spell and spell.namesuffix == spell_action:
                self.map.all_units_by_name[unit_name].spell_actions[spell_index] = None
                break
            print "No spell of %s found on character %s" % (spell_action, unit_name)


    def set_equip(self, unit_name, spell_name):
        """
        function name: set_equip
        purpose: set the unit to equip the first available spell of spell_name
        """

        try:
            unit = self.map.all_units_by_name[unit_name]
            for index, spell in enumerate(unit.spell_actions):
                if spell and spell.namesuffix == spell_name:
                    unit.equipped = index
                    break
            else:
                print "Cannot find spell name %s" % spell_name

        except KeyError:
            print "ERROR: Mame mismatch in set_equip sub action: %s %s" % (unit_name, spell_name)



    def set_ai_state(self, unit_name, ai_state):
        """
        # function name: set_ai_state
        # purpose: Switches the AI to a certain state
        # inputs: unit_name - name of unit to modify AI
        #         ai_state - name of the AI state to switch to
        """
        try:
            if self.map.all_units_by_name[unit_name] not in self.map.team1:
                self.map.all_units_by_name[unit_name].ai.current_state = self.map.all_units_by_name[unit_name].ai.all_states[ai_state]
            else:
                print "ERROR: Cannot assign AI to unit in the player's party."
        except KeyError:
            print "ERROR: Mame mismatch in set ai_state subaction: %s %s" % (unit_name, ai_state)


    def set_spell_lock(self, unit_name, lock_state):
        """
        # function name: set_spell_lock
        # purpose: Switches the AI to a certain state
        # inputs: unit_name - name of unit to modify AI
        #         lock_state - TRUE if unit is not allowed to switch spells, FALSE if unit is free to
        """
        try:
            if self.map.all_units_by_name[unit_name] not in self.map.team1:
                self.map.all_units_by_name[unit_name].ai.spell_lock = lock_state
            else:
                print "ERROR: Cannot assign AI to unit in the player's party."
        except KeyError:
            print "ERROR: Mame mismatch in set ai_state subaction: %s"% (unit_name)


    def set_hp(self, unit_name, hp):
        """
        # function name: set_hp
        # purpose: set the unit's HP to a certain value
        # inputs:  unit_name - name of unit to modify HP
        #          hp - integer value of the HP to set HP to
        """
        try:
            self.map.all_units_by_name[unit_name].HP = hp

        except KeyError:
            print "ERROR: Unit name mismatch in set HP subaction "+unit_name


    def set_invincibility_state(self, unit_name, invincible):
        """
        # function name: set_hp
        # purpose: set the unit's invincibility state to T/F
        # inputs:  unit_name - name of unit to modify HP
        #          invincible - True for invincibility enabled / False for not enabled.
        """
        try:
            self.map.all_units_by_name[unit_name].invincible = invincible

        except KeyError:
            print "ERROR: Unit name mismatch in set invincibility state "+unit_name





    def set_spell_uses(self, unit_name, spell_name, uses):
        """
        # function name: set_unit_spell_uses
        # purpose: set a unit's spell to have a certain amount of uses
        # inputs: unit_name - unit to modify spells of
        #         spell_name - name of spell to change
        #         uses - integer number of uses to change spell to possess
        """
        try:
            unit = self.map.all_units_by_name[unit_name]
            for spell_action in unit.spell_actions:
                if spell_action and spell_action.namesuffix == spell_name:
                    spell_action.livesleft = uses

        except KeyError:
            print "ERROR: Unit name mismatch in set spell uses subaction "+unit_name+" "+spell_name+" "+uses

    def set_spell_max_uses(self, unit_name, spell_name, max_uses):
        """
        # function name: set_unit_spell_max_uses
        # purpose: set a unit's spell to have a certain amount of max uses
        # inputs: unit_name - unit to modify spells of
        #         spell_name - name of spell to change
        #         max_uses - integer number of max uses to change spell to possess
        """
        try:
            unit = self.map.all_units_by_name[unit_name]
            for spell_action in unit.spell_actions.values():
                if spell_action and spell_action.namesuffix == spell_name:
                    spell_action.lives = max_uses
                    if spell_action.livesleft > spell_action.lives:
                        spell_action.livesleft = spell_action.lives

        except KeyError:
            print "ERROR: Unit name mismatch in set spell max uses subaction "+unit_name+" "+spell_name+" "+max_uses

    def set_spirit_charge(self, unit_name, sc):
        """
        # function name: set_spirit_charge
        # purpose: set's a unit's spirit charge
        # inputs: unit_name - name of the unit to modify SC
        #         sc - integer value of SC to change to
        """
        try:
            unit = self.map.all_units_by_name[unit_name]
            unit.spirit = sc
            unit.check_spirit_range()
        except KeyError:
            print "ERROR: Unit name mismatch in set spirit charge "+unit_name

    def set_status_effect(self, unit_name, status_effect):
        """
        # Case: set_unit_status_effect
        # Purpose: gives a unit a status effect
        # inputs: unit_name - name of unit to give status effect to
        #         status_effect - name of status effect
        """
        try:
            self.map.all_units_by_name[unit_name].give_status(status_effect)
        except KeyError:
            print "ERROR: Unit name mismatch in set status effect subaction "+unit_name




    def set_unit_pos(self, unit_name, destination):
        """
        # function name: set_unit_pos
        # purpose: set a unit immediately to a position (do not show the movement)
        # inputs: unit_name - name of the unit to move
        #         destination - (X, Y) map coordinates to move to
        """
        try:
            self.map.all_units_by_name[unit_name].update_location(*destination)
        except KeyError:
            print "ERROR: Unit name mismatch in set unit pos subaction "+unit_name

    def script_battle(self, lhs_name, rhs_name, script_dict, plot_results = False):
        """
        # function name: script_battle
        # purpose: run a scripted battle between two units
        # inputs: lhs_name - name of LHS unit
        #         rhs_name - name of RHS unit
        #         script_dict - Dictionary in the form of:
        #                {'lhs_equip': index of LHS unit's equipped spell,
        #                'rhs_equip': index of RHS unit's equipped spell,
        #                'lhs_hit': True/False as to whether LHS unit's spell hit,
        #                'rhs_hit': True/False as to whether RHS unit's spell hit,
        #                'lhs_crit': True/False as to whether LHS unit's action was a critical hit,
        #                'rhs_crit': True/False as to whether RHS unit's action was a critical hit}
        """
        try:

            attacker = self.map.all_units_by_name[lhs_name]
            defender = self.map.all_units_by_name[rhs_name]
            attacker_temp_equip = attacker.equipped
            defender_temp_equip = defender.equipped
            attacker.equipped = script_dict['lhs_equip']
            defender.equipped = script_dict['rhs_equip']

            effect, counterdamage, critical, countercrit, sc_cost_user, sc_cost_target = self.map.engine.battle_event_system.battle_event(attacker, defender, script_dict)

            # Runs the attacker's EXP function
            attacker_exp_delta, attacker_level_up = attacker.experience(defender, effect)

            # Runs the attacker's Spirit function
            attacker_spirit_delta , defender_spirit_delta  = attacker.battle_spirit(defender, effect, critical)

            defender_exp_delta = 0
            defender_level_up = False
            if counterdamage != 'n/a':
                # Runs the defender's EXP function
                defender_exp_delta, defender_level_up = defender.experience(attacker, counterdamage)

                # Runs the defenders's Spirit function
                spirit_enemy_counter, spirit_self_counter = defender.battle_spirit(attacker, counterdamage, countercrit)
                attacker_spirit_delta += spirit_self_counter
                defender_spirit_delta += spirit_enemy_counter

            # If a unit is defeated, remove it from the map
            if attacker.alive == False:
                self.map.kill(attacker)
            if defender.alive == False:
                self.map.kill(defender)

            # By default, plotting the battle results is suppressed
            if plot_results:
                attacker.plot_results(defender, attacker_exp_delta, attacker_level_up, defender_exp_delta, defender_level_up, attacker_spirit_delta , defender_spirit_delta, sc_cost_user, sc_cost_target )

            attacker.equipped = attacker_temp_equip
            defender.equipped = defender_temp_equip

        except KeyError:
            print "ERROR: Unit name mismatch in script battle subaction "+lhs_name+" "+rhs_name+" "+str(script_dict)


    def startle(self, unit_name):
        """
        # function name: startle
        # purpose: make the unit jump a couple of times
        # inputs: unit_name - name of the unit to startle
        """
        try:
            self.map.all_units_by_name[unit_name].render_startle()
        except KeyError:
            print "ERROR: Unit name mismatch in startle subaction "+unit_name


class MAETrigger(object):
    """
    # Base class for MAE triggers
    """
    def __init__(self):
        """
        # Function: __init__
        # Purpose: Creates a map action event trigger
        """
        self.MAE_parent = None

    def check_conditions(self):
        """
        # Function: check
        # Purpose: checks the map action events
        """
        pass

class CustVarTrigger(MAETrigger):

    def __init__(self, cust_var_name, value):
        """
        # Function name = __init__
        # Purpose: Creates a custom variable trigger
        # Inputs:   Custom variable name = name of the custom variable in parent map's cust_var dictionary
        #                Value - Value upon the trigger's executing
        """
        self.cust_var_name = cust_var_name
        self.value = value
        MAETrigger.__init__(self)

    def check_conditions(self):
        """
        # Function name = check
        # Purpose: checks if the conditions are met
        # Outputs: True if the custom variable matches the desired value
        #                False if the custom variable does not match the desired value or has not yet been assigned
        """

        if self.MAE_parent.map.cust_var.has_key(self.cust_var_name):
            return self.MAE_parent.map.cust_var[self.cust_var_name] == self.value
        else:
            return False

class UnitAliveTrigger(MAETrigger):
    def __init__(self, unit_name, alive_state):
        """
        # Function: __init__
        # Purpose: Trigger if unit is alive
        #          unit_name - unit to check
        """
        self.unit_name = unit_name
        self.alive_state = alive_state
        MAETrigger.__init__(self)

    def check_conditions(self):
        """
        # Function: check
        # Purpose: True if unit's alive status matches the trigger
        #          False if unit's alive status does not match the trigger
        """
        if self.unit_name in self.MAE_parent.map.all_units_total.keys() and self.MAE_parent.map.all_units_total[self.unit_name].alive == self.alive_state:
            return True
        else:
            return False

class UnitHPBelowTrigger(MAETrigger):
    def __init__(self, unit_name, hp, invert = False):
        """
        # Function: __init__
        # Purpose: Trigger if unit is alive
        #          unit_name - unit to check
        """
        self.unit_name = unit_name
        self.hp = hp
        MAETrigger.__init__(self)

    def check_conditions(self):
        """
        # Function: check
        # Purpose: True if unit's hp is below a certain level
        #          False if unit's hp is above a certain level
        """
        if self.unit_name in self.MAE_parent.map.all_units_total.keys() and self.MAE_parent.map.all_units_total[self.unit_name].HP <= self.hp:
            return True
        else:
            return False


class ArrivalTrigger(MAETrigger):

    def __init__(self, box, team, unit=None):
        """
        # Function name = __init__
        # Purpose: Creates an arrival trigger
        # Inputs:   Custom variable name = name of the custom variable in parent map's cust_var dictionary
        #                Box (x1, y1, x2, y2) - a box that defines the trigger location (x1, y1 defines top left corner; x2, y2 defines vector to lower right corner
        #                Team (1, 2) - a unit from team 1 or team 2 arrives
        #                Unit - a specific unit name (None if omitted)
        """
        x1, y1, x2, y2 = box
        self.box = box
        self.trigger_locations = []
        [self.trigger_locations.append((x1+delta_x, y1+delta_y)) for delta_x in xrange(0, x2) for delta_y in xrange(0, y2)]

        self.team = team
        self.unit_name = unit
        MAETrigger.__init__(self)

    def check_conditions(self):
        """
        # Function name = check
        # Purpose: checks if the conditions are met
        # Outputs: True if the custom variable matches the desired value
        #                False if the custom variable does not match the desired value or has not yet been assigned
        """
        if self.team == 1:
            team = self.MAE_parent.map.team1
        elif team == 2:
            team = self.MAE_parent.map.team2

        for unit in team:
            if tuple(unit.location_tile) in self.trigger_locations:
                if self.unit_name == None or unit.name == self.unit_name:
                    return True

        # Nobody is in the trigger locations
        return False

class TurnNumTrigger(MAETrigger):
    def __init__(self, turn_num):
        """
        # Function: __init__
        # Purpose: Trigger if X turns have passed
        #          turn_num - turn number to trigger on
        """
        MAETrigger.__init__(self)
        self.turn_num = turn_num

    def check_conditions(self):
        """
        # Function: check
        # Purpose: True if it is the specified turn number
        #          False otherwise
        """
        if self.MAE_parent.map.turn_count == self.turn_num:
            return True
        else:
            return False


class SSPStateTrigger(MAETrigger):

    def __init__(self, name, capture_state):
        """
        # Function: __init__
        # Purpose: Trigger if a certain SSP has been captured
        #          name - name of SSP
        #          capture_state - 0 - neutral, 1 - player, 2 enemy
        """
        MAETrigger.__init__(self)
        self.ssp_name = name
        self.capture_state = capture_state

    def check_conditions(self):
        """
        # Function: check
        # Purpose: True if it is the specified turn number
        #          False otherwise
        """
        if self.ssp_name in self.MAE_parent.map.all_landmarks.keys() and self.MAE_parent.map.all_landmarks[self.ssp_name].capture_state == self.capture_state:
            return True
        else:
            return False

class TeamTurnTrigger(MAETrigger):


    def __init__(self, team_number):
        """
        # Function: __init__
        # Purpose: Triggers if it is currently the player or enemy team's turn
        #          team_number = 1 for player team, 2 for enemy team
        """
        MAETrigger.__init__(self)
        self.team_number = team_number


    def check_conditions(self):

        if self.MAE_parent.map.currentplayer == self.team_number:
            return True
        else:
            return False
