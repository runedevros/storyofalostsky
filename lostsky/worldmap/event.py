import pygame
import os
from pygame.locals import *
from lostsky.battle.mapobj import Map, Landmark
from lostsky.battle.ai_fsm import UnitAI
from lostsky.battle.objectives import Rout, Headhunt, Protect, Survive, Escape
from lostsky.battle.objectives import DefeatAndArrive, CaptureSpiritSource, TurnCapture
from lostsky.battle.objectives import TerritoryDefenseBoss, TerritoryDefenseRout
from lostsky.core.utils import get_ui_panel
from lostsky.core.colors import panel_color, border_color

#############################
# Generic Event Class
#############################
class Event(object):

    def __init__(self, name, location_name, event_id, prereq, show_rewards, desc):
        """
        # Function Name: __init__
        # Purpose: Intializes an event
        # Inputs: name - the name of the event
        #         location_name - the name of the location of the event
        #         event_id - an identification string for the event
        #           (e.g. CH2ST1 for chapter 2 story mission 1 or CH2SQ1 for chapter 2 side quest 1)
        #         prereq - prerequisite event event_id string
        #         show_rewards - whether to show post-battle rewards
        """
        self.name = name
        self.map = None
        self.map_data = None
        self.location = None
        self.done = False

        self.prereq = prereq
        self.manual_cancel = False

        self.desc = desc
        self.show_rewards = show_rewards

        # If there are no prerequisites, set the availablity as false
        if self.prereq != None:
            self.available = False

        else:
            self.available = True

        # Sets the sign up flag if there are no prerequisites, otherwise it will be activated when the prerequisites are met
        if not self.prereq:
            self.sign_up = True
        else:
            self.sign_up = False



        self.event_id = event_id
        self.location_name = location_name
        self.index = 0

    def execute(self):

        """
        # Function Name: execute
        # Purpose: executes the actions within the event
        """

        pass

    def map_init(self):

        """
        # Function Name: map_init
        # Purpose: Initializes the battle map
        """

        self.map = Map(self.location.region.engine,
                       os.path.join('maps', self.map_data.text_map),
                       self.map_data.pre_mission_MAE,
                       self.map_data.mid_mission_MAE_list,
                       self.map_data.post_mission_MAE)

        enemy_units = [self.map.engine.enemynpc_units_catalog.construct_unit(unit_attribute)
                       for unit_attribute in self.map_data.enemy_unit_data]

        # Assigns required survivors to be brought back for the post mission events.
        self.map.required_survivors = self.map_data.required_survivors
        self.map.preset_units = self.map_data.preset_units


        # Sets up all units present at start of a mission
        [self.map.store_unit(player_unit, 1) for player_unit in self.location.region.engine.player_units if player_unit.name in self.map_data.required_starters]
        [self.map.store_unit(enemy_unit, 2) for enemy_unit in enemy_units if enemy_unit.name not in self.map_data.reserve_units]
        for enemy_unit in enemy_units:
            if enemy_unit.name in self.map_data.reserve_units:
                self.map.reserve_units[enemy_unit.name] = enemy_unit

        # Adds all landmarks
        for landmark in self.map_data.all_landmarks:
            landmark_id = landmark['id_string']
            self.map.add_landmark(Landmark(landmark['name'],
                     landmark['location'],
                     self.map.engine.landmark_catalog[landmark_id]['size'],
                     (self.map.engine.landmark_catalog[landmark_id]['img_coords'][0]*35,
                         self.map.engine.landmark_catalog[landmark_id]['img_coords'][1]*35),
                     self.map.engine.landmark_catalog[landmark_id]['passable']))

        # # Assigns animation data
        for unit in enemy_units:
            if unit.animation_enable:
                unit.anim_frames = self.map.engine.unit_anim_catalog[unit.anim_id_string]

        # Initializes all spells
        for unit_name in self.map_data.initial_spells.keys():
            if unit_name in self.map.all_units_by_name.keys():
                [self.map.all_units_by_name[unit_name].add_spell(self.map.engine.spell_catalog[spell_name].construct_spell()) for spell_name in self.map_data.initial_spells[unit_name]]
            elif unit_name in self.map.reserve_units.keys():
                [self.map.reserve_units[unit_name].add_spell(self.map.engine.spell_catalog[spell_name].construct_spell()) for spell_name in self.map_data.initial_spells[unit_name]]

        # Initializes all traits
        for unit_name in self.map_data.initial_traits.keys():
            if unit_name in self.map.all_units_by_name.keys():
                [self.map.all_units_by_name[unit_name].add_trait(self.map.engine.trait_catalog[trait]) for trait in self.map_data.initial_traits[unit_name]]
            elif unit_name in self.map.reserve_units.keys():
                [self.map.reserve_units[unit_name].add_trait(self.map.engine.trait_catalog[trait]) for trait in self.map_data.initial_traits[unit_name]]

        # Initializes all AI states
        for unit_name in self.map_data.initial_AI.keys():
            if unit_name in self.map.all_units_by_name.keys():
                self.map.all_units_by_name[unit_name].ai = UnitAI(self.map.all_units_by_name[unit_name], self.map_data.initial_AI[unit_name])
            elif unit_name in self.map.reserve_units.keys():
                self.map.reserve_units[unit_name].ai = UnitAI(self.map.reserve_units[unit_name], self.map_data.initial_AI[unit_name])

        # Initializes all starting locations
        for unit_name in self.map_data.initial_locations.keys():
            self.map.all_units_by_name[unit_name].update_location(*self.map_data.initial_locations[unit_name])

        # Adds the objective
        if self.type == 'Mission':

            if self.map_data.objective['type'] == 'Defeat All':
                self.map.objective = Rout(self.map_data.objective['desc'])
            elif self.map_data.objective['type'] == 'Defeat Boss':
                if self.map_data.objective['target'] not in self.map_data.reserve_units:
                    self.map.objective = Headhunt(self.map.all_units_by_name[self.map_data.objective['target']], self.map_data.objective['desc'])
                else:
                    self.map.objective = Headhunt(self.map.reserve_units[self.map_data.objective['target']], self.map_data.objective['desc'])

            elif self.map_data.objective['type'] == 'Defeat All and Protect':
                self.map.objective = Protect(self.map.all_units_by_name[self.map_data.objective['target']], self.map_data.objective['desc'])
            elif self.map_data.objective['type'] == 'Survive':
                self.map.objective = Survive(self.map_data.objective['turns'], self.map_data.objective['desc'])
            elif self.map_data.objective['type'] == 'Escape':
                self.map.objective = Escape(self.map_data.objective['turns'], self.map_data.objective['location_box'], self.map_data.objective['location_name'], self.map_data.objective['desc'])
            elif self.map_data.objective['type'] == 'Arrive and Defeat Boss':
                if self.map_data.objective['target'] not in self.map_data.reserve_units:
                    self.map.objective = DefeatAndArrive(self.map.all_units_by_name[self.map_data.objective['target']], self.map_data.objective['location_box'], self.map_data.objective['location_name'], self.map_data.objective['desc'])
                else:
                    self.map.objective = DefeatAndArrive(self.map.reserve_units[self.map_data.objective['target']], self.map_data.objective['location_box'], self.map_data.objective['location_name'], self.map_data.objective['desc'])
            elif self.map_data.objective['type'] == 'Defend and Defeat Boss':

                if self.map_data.objective['target'] not in self.map_data.reserve_units:
                    self.map.objective = TerritoryDefenseBoss(self.map.all_units_by_name[self.map_data.objective['target']], self.map_data.objective['location_box'], self.map_data.objective['location_name'], self.map_data.objective['desc'])
                else:
                    self.map.objective = TerritoryDefenseBoss(self.map.reserve_units[self.map_data.objective['target']], self.map_data.objective['location_box'], self.map_data.objective['location_name'], self.map_data.objective['desc'])
            elif self.map_data.objective['type'] == 'Defend and Defeat All':
                self.map.objective = TerritoryDefenseRout(self.map_data.objective['location_box'], self.map_data.objective['location_name'], self.map_data.objective['desc'])


            elif self.map_data.objective['type'] == 'Capture Spirit Sources':
                [self.map.add_ssp(ssp) for ssp in self.map_data.objective['ssps']]
                self.map.objective = CaptureSpiritSource(self.map_data.objective['number'], self.map_data.objective['desc'])
            elif self.map_data.objective['type'] == 'Turn Capture':
                [self.map.add_ssp(ssp) for ssp in self.map_data.objective['ssps']]
                self.map.objective = TurnCapture(self.map_data.objective['turn_limit'],
                                                 self.map_data.objective['number'],
                                                 self.map_data.objective['desc'])

            # Sets up deploy locations
            if self.map_data.enable_deploy:
                self.map.enable_deploy = True
                self.map.max_deployed_units = self.map_data.max_deployed_units
                self.map.deploy_locations = []
                self.map.default_locations = self.map_data.default_locations
                for deploy_box in self.map_data.deploy_boxes:
                    x1, y1, x2, y2 = deploy_box
                    [self.map.deploy_locations.append((x1+delta_x, y1+delta_y)) for delta_x in xrange(0, x2) for delta_y in xrange(0, y2)]
            else:
                self.map.enable_deploy = False

        elif self.type == 'Conversation':
            self.map.objective = None

    def results_loop(self, completed):
        """
        # Name: results_loop
        # Purpose: Displays the results of the event
        # Inputs: completed - was the mission successfully done?
        """

        menu_flag = True
        engine = self.location.region.engine



        text_mission_name = engine.speaker_font.render(self.name, True, (0, 0, 0))
        if completed:
            text_completed = engine.section_font.render("Mission completed!", True, (0, 0, 0))
            self.map.engine.play_music('victory_theme')
        else:
            text_completed = engine.section_font.render("Mission failed!", True, (0, 0, 0))

        top_panel = get_ui_panel((250, 40), border_color, panel_color)
        rewards_panel = get_ui_panel((250, 150), border_color, panel_color)


        text_rewards = engine.speaker_font.render("Rewards", True, (0, 0, 0))
        text_rewards_list = []
        # Processes Mission Rewards
        for reward in self.map_data.rewards_list:
            if reward[0] == "spell_action":
                text_rewards_list.append(engine.message_font.render(reward[1], True, (0, 0, 0)))
            elif reward[0] == "treasure":
                text_rewards_list.append(engine.message_font.render(engine.treasure_catalog[reward[1]].name, True, (0, 0, 0)))

        self.location.render_updated_map()

        while menu_flag == True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN and (event.key == K_z  or event.key == K_RETURN):
                    menu_flag = False
            if menu_flag:

                engine.surface.blit(engine.results_panel, (280, 140))
                engine.surface.blit(top_panel, (420 - top_panel.get_width()/2, 155))
                engine.surface.blit(text_mission_name, (420 - text_mission_name.get_width()/2,
                                                        155 + top_panel.get_height()/2 - text_mission_name.get_height()/2))
                engine.surface.blit(top_panel, (420 - top_panel.get_width()/2, 200))
                engine.surface.blit(text_completed, (420 - text_completed.get_width()/2,
                                                        202 + top_panel.get_height()/2 - text_completed.get_height()/2))




                # engine.surface.blit(text_completed, (315, 210))
                #
                if completed:
                    engine.surface.blit(rewards_panel, (420 - rewards_panel.get_width()/2, 250))
                    engine.surface.blit(text_rewards, (420 - text_rewards.get_width()/2, 255))

                    for index, reward in enumerate(text_rewards_list):
                        engine.surface.blit(reward, (420 - reward.get_width()/2,
                                                     280 + index*30))

                pygame.display.flip()
                engine.clock.tick(60)

###############################
# Battle Event Class
###############################
class BattleEvent(Event):
    def __init__(self, name, location_name, event_id, prereq = None, show_reward=True, desc=None):


        """
        # Function Name: __init__
        # Purpose: Intializes a battle event
        # Inputs: name - the name of the event
        #         location_name - the name of the location of the event
        #         event_id - an identification string for the event
        #           (e.g. CH2ST1 for chapter 2 story mission 1 or CH2SQ1 for chapter 2 side quest 1)
        #         prereq - prerequisite event
        #        auto_signup - Automatically sign up for mission
        #        cancellable - Able to cancel mission
        #        desc - Mission description
        #        show_reward - Display reward in signup/current missions page.
        """
        Event.__init__(self, name, location_name, event_id, prereq, show_reward, desc)
        self.type = 'Mission'

    def execute(self):
        """
        # Function Name: execute
        # Purpose: Initializes the map, starts the turn loop, etc
        """

        pygame.mixer.music.stop()

        self.map_init()
        battle_result = self.map.turn_loop()
        if battle_result == 'team1victory':
            self.done = True
            for reward in self.map_data.rewards_list:
                if reward[0] == 'spell_action':
                    print "Adding spell action to inventory: "+reward[1]
                    spell_action = self.location.region.engine.spell_catalog[reward[1]].construct_spell()
                    self.location.region.engine.player.add_item(spell_action)
                elif reward[0] == 'treasure':
                    print "Adding treasure to inventory. Id string: "+reward[1]
                    self.location.region.engine.player.add_treasure(reward[1])
            # Processes Items Received in Missions
            for item_type, item_id, quantity in self.map.items_received:
                if item_type == 'treasure':
                    self.location.region.engine.player.add_treasure(item_id, quantity)
                elif item_type == 'spell_action':
                    [self.location.region.engine.player.add_item(self.location.region.engine.spell_catalog[item_id].construct_spell()) for counter in xrange(0, quantity)]

        if self.event_id == 'CH5ST2' and self.done:
            return

        else:

            self.results_loop(self.done)

            self.location.region.engine.play_music('overworld')
            pygame.display.set_caption("Story of a Lost Sky - v%s"%(self.map.engine.game_version))


            self.location.region.engine.update_player_data()
            # Associates every unit with the world map
            self.location.region.wm_parent.unit_associate()




######################################
# Conversation Event Class
######################################
class ConversationEvent(Event):

    def __init__(self, name, location_name, event_id, prereq=None, show_rewards=True, desc=None):
        """
        # Function Name: __init__
        # Purpose: Intializes a conversation event
        # Inputs: name - the name of the event
        #         location_name - the name of the location of the event
        #         id - an identification string for the event
        #           (e.g. CH2ST1 for chapter 2 story mission 1 or CH2SQ1 for chapter 2 side quest 1)
        #        prereq - Missions that need to be completed before this mission is available
        #        auto_signup - Automatically sign up for mission
        #        cancellable - Able to cancel mission
        #        desc - Mission description
        #        show_rewards - Display reward in signup/current missions page.
        """
        Event.__init__(self, name, location_name, event_id, prereq, show_rewards, desc)

        self.type = 'Conversation'

    def execute(self):
        """
        # Function Name: execute
        # Purpose: executes the actions within the event
        """

        if "Credits" not in self.name:
            pygame.mixer.music.stop()

        self.map_init()
        # Sets the no battle flag to skip the battle since this is a conversation event
        self.map.nobattle = True
        self.map.turn_loop()
        self.done = True
        # Processes Items Received in Missions
        for item_type, item_id, quantity in self.map.items_received:
            if item_type == 'treasure':
                self.location.region.engine.player.add_treasure(item_id, quantity)
            elif item_type == 'spell_action':
                [self.location.region.engine.player.add_item(self.location.region.engine.spell_catalog[item_id].construct_spell()) for counter in xrange(0, quantity)]

        if self.event_id != "Prologue" and "Credits" not in self.name:
            self.location.region.engine.play_music('overworld')
        pygame.display.set_caption("Story of a Lost Sky - v%s"%(self.map.engine.game_version))

        self.location.region.engine.update_player_data()
        # Associates every unit with the world map
        self.location.region.wm_parent.unit_associate()

