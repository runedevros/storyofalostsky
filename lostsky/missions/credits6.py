from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Credits 6'
        location = 'Human Village'
        id_string = 'Credits6'
        prereqs = ['CH5ST2']
        show_rewards = False
        desc = ''

        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch1st1.txt'
        mission_type = 'conversation'
        objective = None
        deploy_data = {}
        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = [
                              {'template_name': 'Wriggle',
                                 'unit_name': 'Wriggle',
                                     'level': 5 },
                              {'template_name': 'Kotone',
                                 'unit_name': 'Kotone',
                                     'level': 5 },
                              {'template_name': 'Miu',
                                 'unit_name': 'Miu',
                                     'level': 5 },
                              {'template_name': 'Lord Fuzzy',
                                 'unit_name': 'Lord Fuzzy',
                                     'level': 5 },

                              {'template_name': 'Fuzzball',
                                 'unit_name': 'Fuzzball A',
                                     'level': 5 },
                              {'template_name': 'Fuzzball',
                                 'unit_name': 'Fuzzball B',
                                     'level': 5 },


                              {'template_name': 'Firefly',
                                 'unit_name': 'Firefly A',
                                     'level': 5 },
                              {'template_name': 'Firefly',
                                 'unit_name': 'Firefly B',
                                     'level': 5 },


                              {'template_name': 'Haruna',
                                 'unit_name': 'Haruna',
                                     'level': 5 },


                              {'template_name': 'Asa',
                                 'unit_name': 'Asa',
                                     'level': 5 },

        ]

        initial_spells = {}
        initial_traits = {}
        initial_ai_states = {}
        initial_locations = {'Haruna':(-1, -1),
                             'Kotone':(10, -1),
                             'Asa':(-1, -1),
                             'Firefly A':(9, -1),
                             'Firefly B':(11, -1),
                             'Kotone':(-1, -1),
                             'Miu':(10, -1),
                             'Wriggle':(10,-1),

                             'Lord Fuzzy':(12, 7),
                             'Fuzzball A':(10, 8),
                             'Fuzzball B':(14, 8),



                             }

        reserve_units = []
        all_landmarks = [{'name':'Mushroom 1',
                          'id_string':'mushroom',
                          'location':(7, 8)},
                         {'name':'Mushroom 2',
                          'id_string':'mushroom',
                          'location':(18, 8)},
                         {'name':'Mushroom 3',
                          'id_string':'mushroom',
                          'location':(9, 5)},
                         {'name':'Mushroom 4',
                          'id_string':'mushroom',
                          'location':(3, 12)},]


        required_starters = []
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
        Kotone and Lord Fuzzy encounter each other.

        Before a fight can start, Miu and Haruna arrive. If the first CH5SQ1 is done, Wriggle arrives too.
        Miu difuses the situation and the Youkai return to the forest.

        If CH5SQ3 is done, Haruna receives a message from Asa.

        """
        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.fade_from_color('black', 2.0)

        self.center_on('Lord Fuzzy')
        self.move_unit('Kotone', (10, 5))
        self.move_unit('Firefly A', (9, 5))
        self.move_unit('Firefly B', (11, 5))

        self.startle('Kotone')
        self.emote('Kotone', 'annoyed')

        self.startle('Lord Fuzzy')
        self.emote('Lord Fuzzy', 'scribble')

        self.move_unit('Miu', (10, 3))
        self.move_unit('Haruna', (9, 3))

        if self.map.engine.check_event_completion(['CH5SQ1']):
            self.move_unit('Wriggle', (11, 3))

        self.move_unit('Miu', (13, 3))
        self.move_unit('Miu', (13, 7))

        self.startle('Miu')
        self.emote('Kotone', 'questionmark')
        self.emote('Miu', 'lightbulb')
        self.emote('Kotone', 'dotdotdot')
        self.emote('Lord Fuzzy', 'dotdotdot')
        self.emote('Lord Fuzzy', 'musicnote')
        self.emote('Kotone', 'musicnote')

        if self.map.engine.check_event_completion(['CH5SQ1']):
            self.move_unit('Wriggle', (11, 3))
            self.emote('Wriggle', 'musicnote')

        self.emote('Haruna', 'musicnote')

        self.move_unit('Lord Fuzzy', (12, -1))
        self.move_unit('Fuzzball A', (10, -1))
        self.move_unit('Fuzzball B', (14, -1))

        if self.map.engine.check_event_completion(['CH5SQ1']):
            self.move_unit('Wriggle', (11, -1))

        if self.map.engine.check_event_completion(['CH5SQ3']):
            self.emote('Haruna', 'questionmark')
            self.show_animation('magic_cast', (10, 7))
            self.set_unit_pos('Asa', (10, 7))
            self.emote('Miu', 'exclamation')
            self.move_unit('Haruna', (10, 6))

            self.startle('Asa')
            self.startle('Asa')
            self.startle('Asa')
            self.emote('Asa', 'musicnote')
            self.emote('Haruna', 'heart')
            self.emote('Haruna', 'musicnote')


        self.fade_to_color('black', 2.0)


        self.set_cursor_state(True)
        self.set_stats_display(True)
        self.done = True
