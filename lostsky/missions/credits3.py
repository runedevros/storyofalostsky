from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Credits 3'
        location = 'Human Village'
        id_string = 'Credits3'
        prereqs = ['CH5ST2']
        show_rewards = False
        desc = ''

        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch3st5.txt'
        mission_type = 'conversation'
        objective = None
        deploy_data = {}
        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Tsubaki',
                                 'unit_name': 'Tsubaki',
                                     'level': 5 },
                          {'template_name': 'Misaki',
                                 'unit_name': 'Misaki',
                                     'level': 5 },
                          {'template_name': 'Momiji',
                                 'unit_name': 'Momiji',
                                     'level': 5 },
                          {'template_name': 'Wolf Tengu',
                                 'unit_name': 'WT1',
                                     'level': 5 },
                          {'template_name': 'Wolf Tengu',
                                 'unit_name': 'WT2',
                                     'level': 5 },
                         {'template_name': 'Wolf Tengu',
                                 'unit_name': 'WT3',
                                     'level': 5 },
                         {'template_name': 'Wolf Tengu',
                                 'unit_name': 'WT4',
                                     'level': 5 },
                         {'template_name': 'Wolf Tengu',
                                 'unit_name': 'WT5',
                                     'level': 5 },

                         {'template_name': 'Crow Tengu',
                                 'unit_name': 'CT1',
                                     'level': 5 },
                         {'template_name': 'Crow Tengu',
                                 'unit_name': 'CT2',
                                     'level': 5 },
                         {'template_name': 'Crow Tengu',
                                 'unit_name': 'CT3',
                                     'level': 5 },
                         {'template_name': 'Crow Tengu',
                                 'unit_name': 'CT4',
                                     'level': 5 },
                         {'template_name': 'Crow Tengu',
                                 'unit_name': 'CT5',
                                     'level': 5 },
                         {'template_name': 'Crow Tengu',
                                 'unit_name': 'CT6',
                                     'level': 5 },





                          ]

        initial_spells = {}
        initial_traits = {}
        initial_ai_states = {}
        initial_locations = {'Misaki':(12, 13),

                              'Tsubaki':(12, 28),
                              'Aya':(12, 28),
                              'Momiji':(12, 23),
                              'WT1':(13, 20),
                              'CT1':(11, 22),
                              'CT2':(14, 22),
                              'WT2':(10, 19),
                              'WT3':(13, 22),
                              'CT3':(11, 23),
                              'CT4':(14, 21),
                              'WT4':(10, 23),
                              'WT5':(11, 24),
                              'CT5':(11, 19),
                              'CT6':(14, 19),




                             }

        reserve_units = []
        all_landmarks = [
                            {'name':'Torii',
                             'id_string':'small_torii',
                             'location':(12, 8)
                        },
                            {'name':'Tree',
                             'id_string':'cherryblossom_tree',
                             'location':(12, 7)
                        },

        ]

        required_starters = ['Aya']
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
        At the top of Youkai Mountain Momiji and a unified Crow/Wolf brigade are standing guard.
        She calls them to attention as Tsubaki and Aya arrive.

        Tsubaki and Aya report the events of the game to Misaki who is pleased
        """
        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.fade_from_color('black', 2.0)


        self.center_on('Momiji')
        self.emote('WT2', 'musicnote')
        self.emote('CT5', 'heart')
        self.emote('WT2', 'dotdotdot')

        self.startle('Momiji')
        self.emote('Momiji', 'annoyed')
        self.startle('Momiji')

        unit_pos = { 'WT1':(11, 19),
                     'CT1':(11, 20),
                     'CT2':(13, 20),
                     'WT2':(11, 21),
                     'WT3':(13, 21),
                     'CT3':(11, 22),
                     'CT4':(13, 22),
                     'WT4':(11, 23),
                     'WT5':(13, 23),
                     'CT5':(11, 18),
                     'CT6':(13, 18),

        }
        for unit in [ 'CT5', 'CT6',  'WT1', 'WT2', 'CT1', 'CT2', 'WT3', 'CT3', 'CT4', 'WT4', 'WT5',]:
            self.move_unit(unit, unit_pos[unit])

        self.startle('Momiji')
        self.move_unit('Momiji', (12, 22))
        self.move_unit('Tsubaki', (12, 23))
        self.move_unit('Aya', (12, 24))
        self.emote('Momiji', 'sweatdrop')
        self.move_unit('Momiji', (12, 19))

        self.move_unit('Tsubaki', (12, 21))
        self.move_unit('Aya', (12, 22))

        self.emote('Aya', 'dotdotdot')
        self.emote('Tsubaki', 'musicnote')

        self.move_unit('Momiji', (13, 19))

        self.move_unit('Tsubaki', (12, 18))
        self.move_unit('Aya', (12, 19))
        self.emote('Tsubaki', 'heart')

        self.center_on('Misaki')

        self.move_unit('Tsubaki', (12, 15))
        self.move_unit('Aya', (11, 15))

        self.emote('Misaki', 'questionmark')
        self.startle('Aya')
        self.emote('Tsubaki', 'dotdotdot')
        self.emote('Tsubaki', 'exclamation')
        self.emote('Aya', 'lightbulb')
        self.startle('Tsubaki')
        self.emote('Tsubaki', 'musicnote')

        self.emote('Misaki', 'musicnote')

        self.fade_to_color('black', 2.0)


        self.set_cursor_state(True)
        self.set_stats_display(True)
        self.done = True
