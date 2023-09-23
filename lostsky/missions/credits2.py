from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Credits 2'
        location = 'Human Village'
        id_string = 'Credits2'
        prereqs = ['CH5ST2']
        show_rewards = False
        desc = ''

        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch2st2.txt'
        mission_type = 'conversation'
        objective = None
        deploy_data = {}
        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Akyu',
                                 'unit_name': 'Akyu',
                                     'level': 5 },
                          {'template_name': 'Nitori',
                                 'unit_name': 'Nitori',
                                     'level': 5 },
                          ]

        initial_spells = {}
        initial_traits = {}
        initial_ai_states = {}
        initial_locations = {'Akyu':(18, 8),
                             'Keine':(19, 7),

                             'Nitori':(20, 5),
                             'Marisa':(18, 16)

                             }

        reserve_units = []
        all_landmarks = [{'name':'Akyu\'s House',
                          'id_string':'house_1',
                          'location':(14, 9)},

                          {'name':'House 2',
                          'id_string':'house_1',
                          'location':(10, 8)},
                          {'name':'House 3',
                          'id_string':'house_1',
                          'location':(14, 14)},
                          {'name':'House 4',
                          'id_string':'house_2',
                          'location':(10, 14)},
                          {'name':'House 5',
                          'id_string':'house_1',
                          'location':(5, 8)},
                          {'name':'House 6',
                          'id_string':'house_2',
                          'location':(18, 6)},
                          {'name':'House 7',
                          'id_string':'house_2',
                          'location':(24, 6)},
                          {'name':'House 8',
                          'id_string':'house_1',
                          'location':(25, 14)},
                          {'name':'House 9',
                          'id_string':'house_2',
                          'location':(5, 6)},

                          {'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(10, 9)},
                          {'name':'CB2',
                          'id_string':'cherryblossom_tree',
                          'location':(13, 8)},
                         ]

        required_starters = ['Keine', 'Marisa']
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
        Akyu and Keine discuss something about the river with Nitori
        Marisa arrives to fetch them.
        """
        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.fade_from_color('black', 2.0)


        self.center_on('Akyu')
        self.startle('Nitori')
        self.emote('Akyu', 'questionmark')
        self.emote('Keine', 'dotdotdot')
        self.emote('Nitori', 'scribble')
        self.move_unit('Nitori', (19, 6))
        self.emote('Nitori', 'questionmark')
        self.emote('Keine', 'exclamation')
        self.move_unit('Akyu', (18, 7))
        self.emote('Akyu', 'lightbulb')

        self.move_unit('Marisa', (18, 9))
        self.startle('Marisa')
        self.emote('Akyu', 'musicnote')
        self.emote('Keine', 'musicnote')
        self.emote('Nitori', 'musicnote')


        self.fade_to_color('black', 2.0)


        self.set_cursor_state(True)
        self.set_stats_display(True)
        self.done = True
