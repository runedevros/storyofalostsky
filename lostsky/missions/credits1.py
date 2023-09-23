from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Credits 1'
        location = 'Western Village Path'
        id_string = 'Credits1'
        prereqs = ['CH5ST2']
        show_rewards = False
        desc = "No Description"
        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'credits1.txt'
        mission_type = 'conversation'
        objective = None

        deploy_data = {'enable':False,
                       'max_units':None,
                       'preset_units':None,
                       'boxes':[]
                       }

        reward_list = []


        enemy_unit_data = [{'template_name': 'CreditsAlice',
                                 'unit_name': 'Alice',
                                     'level': 5 },]

        initial_spells = {}

        initial_traits = {}

        initial_ai_states = {}

        initial_locations = {'Reimu':(11, 8),
                             'Marisa':(11, 14),
                             'Alice':(-1, -1)

                             }

        reserve_units = []#[list of unit names to deploy later in mission]

        all_landmarks = [
                         {'name':'Shrine',
                         'id_string':'shrine',
                         'location':(11, 7)},

                         {'name':'Torii',
                         'id_string':'small_torii',
                         'location':(11, 10)},

                         {'name':'RHouse',
                         'id_string':'house_1',
                         'location':(13, 4)},


                          {'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(7, 7)},

                          {'name':'CB2',
                          'id_string':'cherryblossom_tree',
                          'location':(8, 4)},

                          {'name':'CB3',
                          'id_string':'cherryblossom_tree',
                          'location':(14, 5)},

                          {'name':'CB4',
                          'id_string':'cherryblossom_tree',
                          'location':(17, 8)},

                          {'name':'lp1',
                          'id_string':'lilypad',
                          'location':(10, 3)},

                         ]

        required_starters = ['Reimu', 'Marisa']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = []
        required_survivors = []
        post_mission_MAE = None

        self.map_data = MapData(map_name, mission_type, objective,
                                deploy_data, reward_list, enemy_unit_data,
                                initial_spells, initial_traits, initial_ai_states,
                                initial_locations, reserve_units, all_landmarks,
                                required_starters, pre_mission_MAE, mid_mission_MAE_list,
                                required_survivors, post_mission_MAE)

class PreMissionMAE(MapActionEvent):

    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Reimu and Marisa at the shrine. Marisa arrives to try and organize a party. She runs off to get people.
        """

        self.set_cursor_state(False)
        self.set_stats_display(False)

        # Use the sunset color overlay

        self.fade_from_color('black', 2.0)

        self.move_unit('Marisa', (11, 9))
        self.startle('Reimu')
        self.emote('Reimu', 'questionmark')
        self.emote('Marisa', 'musicnote')
        self.emote('Reimu', 'dotdotdot')
        self.emote('Reimu', 'lightbulb')
        self.startle('Marisa')
        self.move_unit('Marisa', (11, 20))

        if self.map.engine.check_event_completion(['CH2SQ2']):
            self.set_unit_pos('Alice', (11, 14))
            self.move_unit('Alice', (11, 11))
            self.startle('Alice')
            self.emote('Alice', 'scribble')
            self.emote('Reimu', 'questionmark')
            self.emote('Alice', 'exclamation')

            self.move_unit('Alice', (11, 20))

        self.fade_to_color('black', 2.0)

        self.done = True