from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Credits7'
        location = 'Netherworld Gardens'
        id_string = 'Credits7'
        prereqs = ['CH5ST2']
        show_rewards = True
        desc = ''

        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'prologue.txt'
        mission_type = 'conversation'
        objective = None
        deploy_data = {}
        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = [
                          ]

        initial_spells = {}
        initial_traits = {}
        initial_ai_states = {}
        initial_locations = {'Ran':(5, 7),

                             'Yukari':(6, 7),
                             'Chen':(7, 7),

                             'Youmu':(5, 5),
                             'Yuyuko':(4, 5)
                             }
        reserve_units = []
        all_landmarks = [{'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(2, 12)},
                          {'name':'CB2',
                          'id_string':'cherryblossom_tree',
                          'location':(6, 10)},
                          {'name':'CB3',
                          'id_string':'cherryblossom_tree',
                          'location':(3, 8)},
                          {'name':'CB4',
                          'id_string':'cherryblossom_tree',
                          'location':(8, 8)},
                          {'name':'CB5',
                          'id_string':'cherryblossom_tree',
                          'location':(3, 4)},
                          {'name':'CB6',
                          'id_string':'cherryblossom_tree',
                          'location':(4, 7)},
                          {'name':'CB7',
                          'id_string':'cherryblossom_tree',
                          'location':(8, 7)},
                          {'name':'CB8',
                          'id_string':'cherryblossom_tree',
                          'location':(12, 1)},
                          {'name':'CB9',
                          'id_string':'cherryblossom_tree',
                          'location':(14, 4)},
                          {'name':'CB10',
                          'id_string':'cherryblossom_tree',
                          'location':(10, 7)},

                          {'name':'CB11',
                          'id_string':'cherryblossom_tree',
                          'location':(16, 0)},
                          {'name':'CB12',
                          'id_string':'cherryblossom_tree',
                          'location':(17, 3)},
                          {'name':'CB13',
                          'id_string':'cherryblossom_tree',
                          'location':(18, 1)},
                          {'name':'CB14',
                          'id_string':'cherryblossom_tree',
                          'location':(19, 4)},
                          {'name':'CB15',
                          'id_string':'cherryblossom_tree',
                          'location':(22, 3)},

                         ]

        required_starters = ['Chen', 'Ran', 'Youmu', 'Yuyuko', 'Yukari']
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
        Yuyuko and Youmu meet with Ran and Chen and Yukari. Yukari invites them to the festival
        """
        self.set_bg_overlay('Sunset')
        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.fade_from_color('black', 2.0)
        self.emote('Youmu', 'questionmark')
        self.move_unit('Chen', (5, 6))
        self.startle('Chen')
        self.emote('Youmu', 'dotdotdot')
        self.emote('Yuyuko', 'musicnote')
        self.emote('Youmu', 'annoyed')
        self.startle('Chen')
        self.emote('Chen', 'lightbulb')
        self.emote('Youmu', 'musicnote')

        self.startle('Yukari')
        self.fade_to_color('white', 1.0)
        self.set_unit_pos('Youmu', (-1, -1))
        self.set_unit_pos('Chen', (-1, -1))
        self.set_unit_pos('Ran', (-1, -1))
        self.set_unit_pos('Yuyuko', (-1, -1))
        self.fade_from_color('white', 1.0)


        self.startle('Yukari')
        self.fade_to_color('white', 1.0)
        self.set_unit_pos('Yukari', (-1, -1))
        self.fade_from_color('white', 1.0)

        self.fade_to_color('black', 2.0)

        self.set_cursor_state(True)
        self.set_stats_display(True)
