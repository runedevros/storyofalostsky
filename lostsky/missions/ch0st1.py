from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, TurnNumTrigger
from lostsky.battle.mapobj import LightSource

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'Sandbox Mission'
        location = 'Hakugyoukurou'
        id_string = 'CH0ST1'
        prereqs = []
        show_rewards = True
        desc = "This is a testing mission for trying out new features."

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch5st2.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat All',
                     'desc':'Defeat All Enemies'
                     }

        deploy_data = {'enable':True,
                       'max_units':18,
                       'preset_units':{},
                       'default_locations':{'Youmu':(4,7),
                                            'Ran':(3,5),
                                            'Chen':(3,6),
                                            'Reimu':(3,8),
                                            'Marisa':(3,9),
                                            'Keine':(2,6),
                                            'Mokou':(2,7),
                                            'Alice':(2,8),
                                            'Aya':(2,9),
                                               },
                       'boxes':[(2, 4, 3, 7)]
                       }


        reward_list = [('spell_action', 'Rice Cake')
                   ]


        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Lord Fuzzy',
                                'unit_name': 'Lord Fuzzy',
                                    'level': 14
                                 }, #{'template_name': 'Kodama Lord',
                                # 'unit_name': 'Kodama Lord A',
                                #     'level': 25
                                # },
                                {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 12
                                },
#                           {'template_name': 'Fairy',
#                                'unit_name': 'Fairy D',
#                                    'level': 5
#                                },
                            #

                            ]

        initial_spells = {'Lord Fuzzy':['Great Mother Tree', 'Withering Fall'],
                          # 'Kodama Lord A':['Evergreen Branch'],
                          'Fairy C':['Evergreen Branch'],
#                          'Fairy D':['Fireball'],
                          #'Kodama Lord A':['Healing Drop'],
#                          'Fairy D':['Fireball'],
#
                            }
        initial_traits = {'Fairy A':[]}
        initial_ai_states = {'Lord Fuzzy':'Attack',
#                              'Kodama Lord A':'HealerStandby',
                             'Fairy C':'HealerStandby',
# #                             'Fairy D':'Attack',

                             #'Kodama Lord A':'HealerStandby'
#                             'Fairy D':'Attack',
#
                            }
        initial_locations = {'Lord Fuzzy':(6, 9),
#                              'Kodama Lord A':(6, 5),
                              'Fairy C':(4, 15),
# #                             'Fairy D':(23, 7),
#                             'Fairy D':(8, 11),
                             }
        reserve_units = []#[list of unit names to deploy later in mission]
        all_landmarks = []
        all_landmarks = [{'name':'Eientei',
                          'id_string':'eientei',
                          'location':(5, 7)}]

        required_starters = ['Youmu', 'Aya', 'Marisa', 'Chen', 'Keine', 'Reimu']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = []
        required_survivors = ['Youmu']
        post_mission_MAE = PostMissionMAE()

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
        Prologue event
        """

        # lantern = LightSource('Lantern 1', (5,5), False, 5)
        # lantern2 = LightSource('Lantern 2', (8,5), False, 3)
        # self.map.add_light_source(lantern)
        # self.map.add_light_source(lantern2)


        self.center_on('Youmu')

#        self.set_spirit_charge('Youmu', 825)
#        self.assign_spell('Momiji', 'Spirit Recharge')
#        self.set_unit_pos('Momiji', (5, 10))

        # self.map.enable_fog = True
        # self.map.update_fog_map()
        # self.say('Light 1 off and 2 off', None, None)
        # lantern.switch_state(True)
        self.set_spell_lock('Fuyuhana', True)
        self.set_spirit_charge('Marisa', 800)
        self.set_equip('Fuyuhana', 'Withering Fall')
        pass


class PostMissionMAE(MapActionEvent):
    def __init__(self):
        # Triggers on turn 2


        triggers = []
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        self.center_on('Youmu')
        self.say("Mission is Over!", 'Youmu', "Youmu")
