__author__ = 'Fawkes'

from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, SSPStateTrigger, TurnNumTrigger, UnitHPBelowTrigger, UnitAliveTrigger, MAETrigger
from lostsky.battle.mapobj import LightSource, SpiritSourcePoint
from lostsky.core.linalg import Vector2

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'A Beacon of Light'
        location = 'Bamboo Maze'
        id_string = 'CH4ST4'
        prereqs = ['CH4ST3']
        show_rewards = True
        desc = "A new alliance has formed! Youmu and friends make a daring counterattack against the Kodama Lords preparing to advance on Eientei. By casting away the fog, they plan to take down Ayaka's unfair advantage and even the playing field."

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch4st4.txt'
        mission_type = 'battle'
        ssp_list = [SpiritSourcePoint('North SSP', (22, 1), 2),
                    SpiritSourcePoint('Center SSP', (24, 11), 2),
                    SpiritSourcePoint('South SSP', (25, 18), 2),
                    SpiritSourcePoint('West SSP', (16, 9), 2),
                    SpiritSourcePoint('East SSP', (31, 11), 2),


                    ]

        objective = {'type':'Capture Spirit Sources',
                     'ssps': ssp_list,
                     'number': 5,
                     'desc':'Capture all Spirit Source Points!'
                     }

        deploy_data = {'enable':True,
                       'max_units':18,
                       'preset_units':{'Eirin':(6,10), 'Kaguya':(6,11)},
                       'default_locations':{'Youmu':(4,10),
                                            'Ran':(4,11),
                                            'Chen':(3,9),
                                            'Reimu':(3,10),
                                            'Aya':(3,11),
                                            'Marisa':(3,12),
                                            'Keine':(2,9),
                                            'Mokou':(2,10),
                                            'Reisen':(2,11),
                                            'Alice':(2,12),
                                               },
                       'boxes':[(1, 9, 4, 4)]
                       }


        reward_list = [('spell_action', 'Weakening Amulet'),
                       ('treasure', 'synth_metal'),
                       ('treasure', 'synth_water'),
                   ]


        # Enemy Unit Data
        enemy_unit_data = [
                            {'template_name': 'Ayaka44',
                                'unit_name': 'Ayaka',
                                    'level': 26
                                },
                            {'template_name': 'Miu44',
                                'unit_name': 'Miu',
                                    'level': 20
                                },
                            {'template_name': 'Haruna44',
                                'unit_name': 'Haruna',
                                    'level': 23
                                },
                            {'template_name': 'Kotone',
                                'unit_name': 'Kotone',
                                    'level': 22
                                },

                            # Miu's Team
                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly A',
                                    'level': 20
                                },
                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly B',
                                    'level': 20
                                },
                            {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel A',
                                    'level': 20
                                },
                            {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel B',
                                    'level': 20
                                },
                            {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel C',
                                    'level': 20
                                },

                            # Miu's Turn 2 Reinforcements
                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly C',
                                    'level': 20
                                },
                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly D',
                                    'level': 20
                                },
                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly E',
                                    'level': 20
                                },
                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly F',
                                    'level': 20
                                },

                            # Kotone's Fairy Squad
                            {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy A',
                                    'level': 21
                                },
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 20
                                },
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 20
                                },
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 20
                                },
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy D',
                                    'level': 20
                                },

                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 18
                                },
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 18
                                },
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 18
                                },

                            {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree A',
                                    'level': 23
                                },
                            {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree B',
                                    'level': 23
                                },
                            {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree C',
                                    'level': 23
                                },
                            {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree D',
                                    'level': 23
                                },

                            {'template_name': 'Yukari',
                                'unit_name': 'Yukari',
                                    'level': 23
                                },

                            ]

        initial_spells = {'Ayaka':['Jubokko\'s Touch', 'Leaf Crystal'],
                              'Haruna':['Evergreen Branch', 'Healing Drop'],
                              'Miu':['Pollenating Butterfly','Leaf Crystal'],
                              'Kotone':['Chestnut Meteor', 'Leaf Crystal'],

                              'Firefly A':['Poison Dust'],
                              'Firefly B':['Poison Dust'],

                              'Firefly C':['Fireball'],
                              'Firefly D':['Poison Dust'],
                              'Firefly E':['Fireball'],
                              'Firefly F':['Poison Dust'],

                              'Wind Weasel A':['Dagger Throw'],
                              'Wind Weasel B':['Leaf Crystal'],
                              'Wind Weasel C':['Dagger Throw'],

                              'Fairy A':['Fireball'],
                              'Fairy B':['Holy Amulet'],
                              'Fairy C':['Fireball'],
                              'Fairy D':['Holy Amulet'],
                              'Healer Fairy A':['Healing Drop'],

                              'Walking Tree A':['Leaf Crystal'],
                              'Walking Tree B':['Leaf Crystal'],
                              'Walking Tree C':['Leaf Crystal'],

                              'Cursed Tree A':['Withering Fall'],
                              'Cursed Tree B':['Spirit Break'],
                              'Cursed Tree C':['Withering Fall'],
                              'Cursed Tree D':['Spirit Break'],


                            }
        initial_traits = {'Haruna':['Tactician'],
                          'Miu':['Flight'],
                          'Kotone':['Magic+ Lv.2'],
                          'Ayaka':['Fog Veil'],

                          'Firefly A':['Flight'],
                          'Firefly B':['Flight'],
                          'Firefly C':['Flight'],
                          'Firefly D':['Flight'],
                          'Firefly E':['Flight'],
                          'Firefly F':['Flight'],

                          'Cursed Tree A':['Fog Veil'],
                          'Cursed Tree B':['Fog Veil'],
                          'Cursed Tree C':['Fog Veil'],
                          'Cursed Tree D':['Fog Veil'],
                          }
        initial_ai_states = {'Ayaka':'Defend',
                             'Haruna':'HealerStandby',
                             'Miu':'Defend',
                             'Kotone':'Pursuit',

                             'Firefly A':'Attack',
                             'Firefly B':'Attack',
                             'Firefly C':'Pursuit',
                             'Firefly D':'Pursuit',
                             'Firefly E':'Pursuit',
                             'Firefly F':'Pursuit',

                             'Wind Weasel A':'Defend',
                             'Wind Weasel B':'Defend',
                             'Wind Weasel C':'Defend',

                             'Fairy A':'Attack',
                             'Fairy B':'Defend',
                             'Fairy C':'Attack',
                             'Fairy D':'Defend',
                             'Healer Fairy A':'HealerStandby',

                             'Walking Tree A':'Defend',
                             'Walking Tree B':'Defend',
                             'Walking Tree C':'Defend',

                             'Cursed Tree A':'Pursuit',
                             'Cursed Tree B':'Pursuit',
                             'Cursed Tree C':'Pursuit',
                             'Cursed Tree D':'Pursuit',

                            }
        initial_locations = {'Ayaka':(45, 10),
                             'Haruna':(25, 18),
                             'Miu':(22, 1),
                             'Kotone':(24, 11),

                             'Firefly A':(20, 1),
                             'Firefly B':(24, 1),
                             'Wind Weasel A':(16, 1),
                             'Wind Weasel B':(15, 3),
                             'Wind Weasel C':(17, 5),

                             'Fairy A':(22, 9),
                             'Fairy B':(22, 13),
                             'Fairy C':(26, 13),
                             'Fairy D':(26, 9),
                             'Healer Fairy A':(25, 11),

                             'Walking Tree A':(23, 17),
                             'Walking Tree B':(25, 16),
                             'Walking Tree C':(27, 17),

                             'Cursed Tree A':(38, 2),
                             'Cursed Tree B':(42, 7),
                             'Cursed Tree C':(45, 14),
                             'Cursed Tree D':(42, 17),

                             'Youmu':(-1,10),
                             'Ran':(-1,10),
                             'Chen':(-1,10),
                             'Marisa':(-1,10),
                             'Reimu':(-1,10),
                             'Keine':(-1,10),
                             'Mokou':(-1,10),
                             'Aya':(-1,10),
                             'Kaguya':(-1,10),
                             'Reisen':(-1,10),
                             'Eirin':(-1,10),


                             }
        reserve_units = ['Firefly C', 'Firefly D', 'Firefly E', 'Firefly F', 'Yukari']
        all_landmarks = [{'name':'banner1',
                          'id_string':'treebanner',
                          'location':(44, 9)},
                         {'name':'banner2',
                          'id_string':'treebanner',
                          'location':(46, 9)},
                         {'name':'banner3',
                          'id_string':'treebanner',
                          'location':(44, 11)},
                         {'name':'banner4',
                          'id_string':'treebanner',
                          'location':(46, 11)},
                         {'name':'banner5',
                          'id_string':'snowbanner',
                          'location':(24, 18)},
                         {'name':'banner6',
                          'id_string':'snowbanner',
                          'location':(26, 18)},
                         {'name':'banner7',
                          'id_string':'featherbanner',
                          'location':(21, 1)},
                         {'name':'banner8',
                          'id_string':'featherbanner',
                          'location':(23, 1)},
                         {'name':'banner9',
                          'id_string':'starbanner',
                          'location':(23, 10)},
                         {'name':'banner10',
                          'id_string':'starbanner',
                          'location':(23, 12)},
                         {'name':'banner11',
                          'id_string':'starbanner',
                          'location':(25, 10)},
                         {'name':'banner12',
                          'id_string':'starbanner',
                          'location':(25, 12)},
                         {'name':'west_torii',
                          'id_string':'small_torii',
                          'location':(16, 10)},
                         {'name':'cb1',
                          'id_string':'cherryblossom_tree',
                          'location':(15, 8)},
                         {'name':'cb2',
                          'id_string':'cherryblossom_tree',
                          'location':(17, 8)},

                         {'name':'east_torii',
                          'id_string':'small_torii',
                          'location':(31, 10)},
                         {'name':'cb3',
                          'id_string':'cherryblossom_tree',
                          'location':(30, 12)},
                         {'name':'cb4',
                          'id_string':'cherryblossom_tree',
                          'location':(32, 12)},

        ]

        required_starters = ['Aya', 'Marisa', 'Youmu', 'Keine', 'Ran', 'Chen', 'Reimu', 'Mokou','Eirin','Reisen','Kaguya']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [DeployFireflies(), RegenSpell(), CenterLampSwitchOff(), CenterLampSwitchOn(),
                                WestLampSwitchOff(), WestLampSwitchOn(), EastLampSwitchOff(), EastLampSwitchOn(),
                                KotoneCriticalHP(), HarunaCriticalHP(), MiuCriticalHP(), AyakaAttackSwitch()
                                ]
        required_survivors = ['Aya', 'Marisa', 'Youmu', 'Keine', 'Ran', 'Chen', 'Reimu', 'Mokou', 'Eirin', 'Reisen','Kaguya','Ayaka']
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
        self.set_fog_state(True)
        self.set_bg_overlay('Night')
        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.set_status_effect('Ayaka', 'Fog Veil')
        self.set_status_effect('Cursed Tree A', 'Fog Veil')
        self.set_status_effect('Cursed Tree B', 'Fog Veil')
        self.set_status_effect('Cursed Tree C', 'Fog Veil')
        self.set_status_effect('Cursed Tree D', 'Fog Veil')
        self.set_invincibility_state('Ayaka', True)


        self.map.add_light_source(LightSource('West Lantern', (21, 10), False, 5))
        self.map.add_light_source(LightSource('West Lantern 2', (16, 8), False, 5))
        self.map.add_light_source(LightSource('East Lantern', (28, 13), False, 5))
        self.map.add_light_source(LightSource('East Lantern 2', (31, 12), False, 5))

        self.set_spirit_charge('Haruna', 650)
        self.set_spirit_charge('Miu', 650)
        self.set_spirit_charge('Kotone', 650)
        self.set_spirit_charge('Ayaka', 650)

        self.play_music('event03')

        self.center_on('Miu')
        self.say("Shaking in your boots are you, Miu?",
                 'Kotone',
                 'Kotone')
        self.emote('Miu', 'scribble')
        self.say("Seriously? Give me a break! It's only my third battle!",
                 'Miu',
                 'Miu')
        self.say("By the way. I-is it true that the group we sent to Eientei was completely destroyed?",
                 'Miu',
                 'Miu')
        self.say("Quit worrying so much, Miu. They were just meant to weaken Eientei for our next attack. They were expendable.",
                 'Kotone',
                 'Kotone')

        self.center_on_coords((3,10))

        self.move_unit('Youmu', (4, 10))
        self.move_unit('Reimu', (2, 8))
        self.move_unit('Marisa', (2, 9))
        self.move_unit('Ran', (2, 11))
        self.move_unit('Chen', (2, 12))
        self.move_unit('Aya', (2, 10))
        self.move_unit('Mokou', (1, 8))
        self.move_unit('Keine', (1, 9))
        self.move_unit('Kaguya', (1, 11))
        self.move_unit('Reisen', (1, 12))


        self.say("We've caught them by surprise!",
                 'Youmu',
                 'Youmu')
        self.say("All right. Reisen! Where are the spirit source points?",
                 'Reimu',
                 'Reimu')
        self.center_on('Kotone')
        self.say("In the thicket directly ahead! There are three right down this path.",
                 'Reisen',
                 'Reisen')

        self.set_cursor_state(True)
        self.center_on_coords((16,9))
        self.pause(0.75)
        self.center_on('Kotone')
        self.pause(0.75)
        self.center_on_coords((31,11))
        self.pause(0.75)


        self.center_on('Miu')
        self.say("Another down the northern path protected by Miu.",
                 'Reisen',
                 'Reisen')

        self.center_on('Haruna')
        self.say("And one more down the southern path that Haruna is guarding. That's five in all.",
                 'Reisen',
                 'Reisen')


        self.set_cursor_state(False)

        self.center_on('Ayaka')
        self.say("Reporting! It's an enemy attack! Youmu's group has arrived.",
                 'Fairy',
                 'Fairy')
        self.say("It's time. Kotone, Miu, Haruna, stay close to the spirit source points! They'll want them in order to dispel our fog.",
                 'Ayaka',
                 'Ayaka')
        self.center_on('Haruna')
        self.say("You can count on me! I owe them a black eye after what they did to me. And then some!",
                 'Kotone',
                 'Kotone')
        self.say("Kotone. Maintain your composure. Charging ahead will weaken our defenses. We can't afford any mistakes!",
                 'Haruna',
                 'Haruna')


        self.center_on('Youmu')

        self.move_unit('Eirin', (1, 10))
        self.say("Forgive my tardiness, Princess.",
                 'Eirin',
                 'Eirin')
        self.say("This is the lantern oil I promised. It was easy enough to make, as expected.",
                 'Eirin',
                 'Eirin')
        self.say("Eirin, Thank you!",
                 'Youmu',
                 'Youmu')
        self.say("Ok! Now that that's done, let's hope Yukari and Yuyuko can finish their lantern fix-ups while we handle the fighting!",
                 'Marisa',
                 'Marisa')

        self.play_music('battle04')


        self.set_cursor_state(True)
        self.set_stats_display(True)


class DeployFireflies(MapActionEvent):

    def __init__(self):

        triggers = [TurnNumTrigger(2), UnitAliveTrigger('Miu', True)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):

        self.center_on('Ayaka')

        self.say("Everyone! Come on out!",
                 'Miu',
                 'Miu')

        self.fade_to_color('white', 0.5)
        self.deploy_unit('Firefly C', (47, 4))
        self.deploy_unit('Firefly D', (48, 7))
        self.deploy_unit('Firefly E', (46, 13))
        self.deploy_unit('Firefly F', (47, 16))
        self.fade_from_color('white', 0.5)

class RegenSpell(MapActionEvent):

    def __init__(self):

        triggers = [TurnNumTrigger(6), UnitAliveTrigger('Haruna', True)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):


        self.center_on('Haruna')

        self.say("This spell should ensure everyone's health! Now go, with my blessing.",
                 'Haruna',
                 'Haruna')

        # Iterates through all walking trees
        for letter in ['A', 'B', 'C']:
            if "Walking Tree "+letter in self.map.all_units_by_name.keys():
                self.play_sfx('heal')
                self.show_animation('healing_spell', self.map.all_units_by_name["Walking Tree "+letter].location_tile)
                self.set_status_effect('Walking Tree '+letter, 'Life Bless')
                self.pause(0.5)

class CenterLampSwitchOn(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('Center SSP', 1)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if not self.map.all_landmarks['West Lantern'].lit:
            self.map.all_landmarks['West Lantern'].switch_state(True)

        if not self.map.all_landmarks['East Lantern'].lit:
            self.map.all_landmarks['East Lantern'].switch_state(True)

class CenterLampSwitchOff(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('Center SSP', 2)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if self.map.all_landmarks['West Lantern'].lit:
            self.map.all_landmarks['West Lantern'].switch_state(False)

        if self.map.all_landmarks['East Lantern'].lit:
            self.map.all_landmarks['East Lantern'].switch_state(False)


class WestLampSwitchOn(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('West SSP', 1)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if not self.map.all_landmarks['West Lantern 2'].lit:
            self.map.all_landmarks['West Lantern 2'].switch_state(True)


class WestLampSwitchOff(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('West SSP', 2)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if self.map.all_landmarks['West Lantern 2'].lit:
            self.map.all_landmarks['West Lantern 2'].switch_state(False)

class EastLampSwitchOn(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('East SSP', 1)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if not self.map.all_landmarks['East Lantern 2'].lit:
            self.map.all_landmarks['East Lantern 2'].switch_state(True)


class EastLampSwitchOff(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('East SSP', 2)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if self.map.all_landmarks['East Lantern 2'].lit:
            self.map.all_landmarks['East Lantern 2'].switch_state(False)


class KotoneCriticalHP(MapActionEvent):

    def __init__(self):

        triggers = [UnitHPBelowTrigger('Kotone', 50)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):

        if 'Kotone' in self.map.all_units_by_name:

            self.center_on('Kotone')
            self.say("Curses! This is bad! I sure hope this spell will do the trick!",
                     'Kotone',
                     'Kotone')
            self.map.all_units_by_name['Kotone'].spell_actions = [None, None, None, None, None]
            self.assign_spell('Kotone','Withering Fall')
            self.map.all_units_by_name['Kotone'].equipped = 0


class MiuCriticalHP(MapActionEvent):

    def __init__(self):

        triggers = [UnitHPBelowTrigger('Miu', 50)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):

        if 'Miu' in self.map.all_units_by_name:
            self.center_on('Miu')
            self.say("Oh, no...no. This is a total mess! I...I may not hold out for much longer, but with this...I should be able to slow them down! Please!",
                     'Miu',
                     'Miu')
            self.map.all_units_by_name['Miu'].spell_actions = [None, None, None, None, None]
            self.assign_spell('Miu','Withering Fall')
            self.map.all_units_by_name['Miu'].equipped = 0

class HarunaCriticalHP(MapActionEvent):

    def __init__(self):

        triggers = [UnitHPBelowTrigger('Haruna', 50)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):

        if 'Haruna' in self.map.all_units_by_name:
            self.center_on('Haruna')
            self.say("This is all I can do to support my faithful trees. I'm sorry. But I must go on the offensive. Now!",
                     'Haruna',
                     'Haruna')
            self.map.all_units_by_name['Haruna'].spell_actions = [None, None, None, None, None]
            self.assign_spell('Haruna','Withering Fall')
            self.set_ai_state('Haruna', 'Attack')
            self.map.all_units_by_name['Haruna'].equipped = 0

class AyakaAttackSwitch(MapActionEvent):
    def __init__(self):

        triggers = [ThreeSSPsCapturedTrigger()]

        MapActionEvent.__init__(self, triggers)

    def execute(self):
        # If 3 ssps have been captured, set Ayaka into attack mode
        if 'Ayaka' in self.map.all_units_by_name:
            self.center_on('Ayaka')
            self.say("They've already taken three? I will bide my time here no longer. It is time I, too, joined the fray!",
                     'Ayaka',
                     'Ayaka')
            self.set_ai_state('Ayaka', 'Pursuit')
            self.map.all_units_by_name['Ayaka'].moves = 4
            self.map.all_units_by_name['Ayaka'].get_moves_path()


class ThreeSSPsCapturedTrigger(MAETrigger):

    def __init__(self):

        MAETrigger.__init__(self)

    def check_conditions(self):
        """
        Checks that three spirit sources have been captured by the player
        """

        number_captured = 0
        for spirit_source in self.MAE_parent.map.all_ssps.values():
            # Checks for player control of spirit source point
            if spirit_source.capture_state == 1:
                number_captured += 1

        minimum_trigger = 3
        if number_captured >= minimum_trigger:
            return True
        else:
            return False


class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.remove_all_enemies()
        self.set_unit_pos('Eirin', (24, 11))
        self.set_unit_pos('Reimu', (22, 1))
        self.set_unit_pos('Marisa', (25, 18))
        self.set_unit_pos('Ran', (16, 9))
        self.set_unit_pos('Kaguya', (31, 11))




        self.set_unit_pos('Youmu', (24, 15))
        self.set_unit_pos('Chen', (23, 15))
        self.set_unit_pos('Aya', (22, 15))
        self.set_unit_pos('Keine', (25, 15))
        self.set_unit_pos('Mokou', (26, 15))
        self.set_unit_pos('Reisen', (24, 16))


    def execute(self):

        self.set_stats_display(False)
        self.set_cursor_state(False)

        self.center_on('Eirin')
        self.say("Are you ready?",
                 'Eirin',
                 'Eirin')

        self.center_on_coords((18, 5))
        self.say("Of course. This spell won't be a problem for me.",
                 'Ran',
                 'Ran')
        self.say("Ready over here.",
                 'Reimu',
                 'Reimu')

        self.center_on_coords((28, 15))
        self.say("And here as well.",
                 'Kaguya',
                 'Kaguya')
        self.say("I've seriously had enough of this fog. Let's go already!",
                 'Marisa',
                 'Marisa')

        self.center_on('Eirin')
        self.say("Understood! Light of the eternal moon, disperse the fog! Shine before us!",
                 'Eirin',
                 'Eirin')

        self.play_sfx('shimmer')
        self.show_animation('light_spell', (24, 11))
        self.center_on_coords((18, 5))
        self.play_sfx('shimmer')
        self.show_animation('light_spell', (22, 1))
        self.play_sfx('shimmer')
        self.show_animation('light_spell', (16, 9))
        self.center_on_coords((28, 15))
        self.play_sfx('shimmer')
        self.show_animation('light_spell', (25, 18))
        self.play_sfx('shimmer')
        self.show_animation('light_spell', (31, 11))

        self.center_on('Eirin')
        self.say("Now! Begone!",
                 'Eirin',
                 'Eirin')

        self.play_sfx('shimmer2')
        self.fade_to_color('white',1.5)
        self.set_fog_state(False)
        self.fade_from_color('white',1.5)

        self.center_on('Ayaka')
        self.emote('Ayaka', 'scribble')
        self.say("No...! We failed!",
                 'Ayaka',
                 'Ayaka')
        self.say("We were so close...",
                 'Ayaka',
                 'Ayaka')
        self.say("Silence. It is too soon to give up the battle. I will not see you lose here. I will join as well.",
                 'Fuyuhana',
                 'Fuyuhana')
        self.say("Gather your forces. We will make our stand south of the Bamboo Forest. Our enemies are exhausted, but the real battle has not yet begun. The advantage is ours!",
                 'Fuyuhana',
                 'Fuyuhana')
        self.say("Yes... Yes, my mistress!",
                 'Ayaka',
                 'Ayaka')

        self.fade_to_color('white',0.5)
        self.kill_unit('Ayaka')
        self.fade_from_color('white',0.5)

        self.play_music('event01')
        self.center_on('Eirin')
        self.say("They're gone. All of them.",
                 'Eirin',
                 'Eirin')

        self.fade_to_color('white', 0.5)
        self.deploy_unit('Yukari', (23, 11))
        self.fade_from_color('white', 0.5)

        self.say("Oho. Looks like it's time for the final showdown, Youmu.",
                 'Yukari',
                 'Yukari')
        self.say("Madam Yukari!",
                 'Youmu',
                 'Youmu')
        self.say("Well done, Youmu. I see that you've obtained the lantern oil. Excellent!",
                 'Yukari',
                 'Yukari')
        self.say("It was a difficult battle, but our efforts have earned us new allies. And new strength.",
                 'Youmu',
                 'Youmu')
        self.say("Say, you said you needed it for a lantern. It's fixed now, right?",
                 'Eirin',
                 'Eirin')
        self.say("Sure is! Here you are, Youmu. It took a trip to the outside world, went shopping through seedy occult stores, and it also raided some ancient ruins!",
                 'Yukari',
                 'Yukari')
        self.say("As for Yuyuko, she was supposed to arrive through a gap, but I'm afraid we got separated. So it goes! That airhead causes so much trouble.",
                 'Yukari',
                 'Yukari')

        self.say("No! Fuyuhana herself is coming! She gave Ayaka orders to meet near the south of the forest...",
                 'Youmu',
                 'Youmu')
        self.startle('Youmu')
        self.say("We cannot afford to leave her alone out there! Let's go, everyone!",
                 'Youmu',
                 'Youmu')

        self.fade_to_color('black', 1.0)
        self.kill_unit('Youmu')
        self.kill_unit('Reimu')
        self.kill_unit('Marisa')
        self.kill_unit('Keine')
        self.kill_unit('Mokou')
        self.kill_unit('Aya')
        self.kill_unit('Eirin')
        self.kill_unit('Reisen')
        self.kill_unit('Kaguya')

        self.set_unit_pos('Yukari', (24, 12))
        self.set_unit_pos('Ran', (26, 15))
        self.set_unit_pos('Chen', (25, 15))
        self.fade_from_color('black', 1.0)

        self.emote('Yukari', 'questionmark')
        self.say("Hmmm? Ran, Ran. Tell me, what's troubling you?",
                 'Yukari',
                 'Yukari')
        self.say("Ah, well. Your portals have never sent people to the wrong place before. That means Lady Yuyuko didn't part from you unintentionally, did she?",
                 'Ran',
                 'Ran')
        self.emote('Yukari', 'lightbulb')
        self.say("Aha! An astute observation, Ran! Although I expected no less from my top class Shikigami. Good, very good.",
                 'Yukari',
                 'Yukari')
