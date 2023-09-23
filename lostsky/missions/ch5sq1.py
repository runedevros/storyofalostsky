__author__ = 'Fawkes'

from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, SSPStateTrigger, TurnNumTrigger, UnitHPBelowTrigger, UnitAliveTrigger, MAETrigger, ArrivalTrigger
from lostsky.battle.mapobj import LightSource, SpiritSourcePoint
from lostsky.core.linalg import Vector2

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'Swarming Light'
        location = 'Misty Lake'
        id_string = 'CH5SQ1'
        prereqs = ['CH5ST1']
        show_rewards = True
        desc = "The Kodama Lord Kotone has started her own little kingdom here at Misty Lake. The small youkai have reported that she's evicted all of them! Except valiant Wriggle, the last one standing! She's boldly requested we take that bully down once and for all!"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch5sq1.txt'
        mission_type = 'battle'
        ssp_list = [

                    ]

        objective = {'type':'Defeat All',
                     'desc':'Defeat All Enemies!'
                     }

        deploy_data = {'enable':True,
                       'max_units':18,
                       'preset_units':{'Wriggle':(23,6)},
                       'default_locations':{
                             'Marisa':(7,14),
                             'Aya':(7,16),

                             'Youmu':(5,15),
                             'Yuyuko':(5,16),
                             'Reimu':(5,17),
                             'Ran':(4,16),
                             'Chen':(4,15),
                             'Yukari':(4,17),

                             'Keine':(3,15),
                             'Mokou':(3,17),
                             'Alice':(3,16),
                             'Kaguya':(2,15),
                             'Reisen':(2,16),
                             'Eirin':(2,17),

                                               },
                       'boxes':[(2, 14, 6, 4)]
                       }


        reward_list = [('spell_action', 'Chestnut Meteor')
                   ]


        # Enemy Unit Data
        enemy_unit_data = [
                            {'template_name': 'Kotone',
                                'unit_name': 'Kotone',
                                    'level': 27
                                },


                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 22},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 22},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 22},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy D',
                                    'level': 22},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy E',
                                    'level': 22},

                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 24},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 24},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 24},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree D',
                                    'level': 24},


                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel A',
                                    'level': 22},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel B',
                                    'level': 22},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel C',
                                    'level': 22},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel D',
                                    'level': 22},


                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly A',
                                    'level': 23},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly B',
                                    'level': 23},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly C',
                                    'level': 23},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly D',
                                    'level': 25},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly E',
                                    'level': 25},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly F',
                                    'level': 25},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly G',
                                    'level': 25},


                            ]

        initial_spells = {   'Kotone':['Chestnut Meteor', 'Leaf Crystal'],
                             'Walking Tree A':['Leaf Crystal'],
                             'Walking Tree B':['Leaf Crystal'],
                             'Walking Tree C':['Leaf Crystal'],
                             'Walking Tree D':['Leaf Crystal'],

                             'Fairy A':['Holy Amulet'],
                             'Fairy B':['Dagger Throw'],
                             'Fairy C':['Leaf Crystal'],
                             'Fairy D':['Fireball'],

                             'Fairy E':['Holy Amulet'],

                             'Wind Weasel A':['Leaf Crystal'],
                             'Wind Weasel B':['Dagger Throw'],
                             'Wind Weasel C':['Leaf Crystal'],
                             'Wind Weasel D':['Dagger Throw'],

                             'Firefly A':['Poison Dust'],
                             'Firefly B':['Poison Dust'],
                             'Firefly C':['Poison Dust'],
                             'Firefly D':['Poison Dust'],
                             'Firefly E':['Fireball'],
                             'Firefly F':['Poison Dust'],
                             'Firefly G':['Fireball'],




                            }
        initial_traits = {'Kotone':['Magic+ Lv.2'],
                          'Walking Tree A':['Fog Veil'],
                          'Walking Tree B':['Fog Veil'],
                          'Walking Tree C':['Fog Veil'],
                          'Walking Tree D':['Fog Veil'],

                          'Firefly A':['Flight'],
                          'Firefly B':['Flight'],
                          'Firefly C':['Flight'],
                          'Firefly D':['Flight'],
                          'Firefly E':['Flight'],
                          'Firefly F':['Flight'],
                          'Firefly G':['Flight'],
                          }
        initial_ai_states = { 'Kotone':'Defend',
                              'Fairy E':'Attack',
                              'Fairy A':'Defend',
                              'Fairy B':'Defend',
                              'Fairy C':'Defend',
                              'Fairy D':'Defend',

                              'Firefly A':'Pursuit',
                              'Firefly B':'Pursuit',
                              'Firefly C':'Pursuit',
                              'Firefly D':'Pursuit',
                              'Firefly E':'Pursuit',
                              'Firefly F':'Pursuit',
                              'Firefly G':'Pursuit',

                              'Wind Weasel A':'Attack',
                              'Wind Weasel B':'Attack',
                              'Wind Weasel C':'Attack',
                              'Wind Weasel D':'Attack',

                              'Walking Tree A':'Attack',
                              'Walking Tree B':'Attack',
                              'Walking Tree C':'Attack',
                              'Walking Tree D':'Attack',


                            }
        initial_locations = {
                             'Kotone':(21, 4),
                             'Fairy A':(23, 4),
                             'Fairy B':(19, 4),
                             'Fairy C':(21, 2),
                             'Fairy D':(21, 6),
                             'Fairy E':(28, 16),


                             'Walking Tree A':(23, 8),
                             'Walking Tree B':(25, 8),
                             'Walking Tree C':(25, 6),
                             'Walking Tree D':(27, 10),

                             'Wind Weasel A':(12, 23),
                             'Wind Weasel B':(14, 19),
                             'Wind Weasel C':(9, 20),
                             'Wind Weasel D':(10, 17),

                             'Firefly A':(5,5),
                             'Firefly B':(7,6),
                             'Firefly C':(9,5),

                             'Marisa':(7,14),
                             'Aya':(7,16),

                             'Youmu':(5,15),
                             'Yuyuko':(5,16),
                             'Reimu':(5,17),
                             'Ran':(4,16),
                             'Chen':(4,15),
                             'Yukari':(4,17),

                             'Keine':(3,15),
                             'Mokou':(3,17),
                             'Kaguya':(2,15),
                             'Reisen':(2,16),
                             'Eirin':(2,17),


                             }
        reserve_units = ['Firefly D', 'Firefly E', 'Firefly F', 'Firefly G']
        all_landmarks = [


                         {'name':'banner1',
                          'id_string':'starbanner',
                          'location':(20, 3)},
                         {'name':'banner2',
                          'id_string':'starbanner',
                          'location':(22, 3)},
                         {'name':'banner11',
                          'id_string':'starbanner',
                          'location':(20, 5)},
                         {'name':'banner12',
                          'id_string':'starbanner',
                          'location':(22, 5)},


                         {'name':'treasure_shrine',
                          'id_string':'minishrine',
                          'location':(7, 5)},

        ]


        required_starters = ['Aya', 'Marisa', 'Youmu', 'Keine', 'Ran', 'Chen', 'Reimu', 'Mokou','Eirin','Reisen','Kaguya', 'Yukari', 'Yuyuko']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [SouthLampSwitchOn(), NorthLampSwitchOn(), DeployFireflies(), CheckWriggleRemoved(), TreasureFoundMAE()]
        required_survivors = ['Aya', 'Marisa', 'Youmu', 'Keine', 'Ran', 'Chen', 'Reimu', 'Mokou', 'Eirin', 'Reisen','Kaguya', 'Yukari', 'Yuyuko', 'Wriggle', 'Kotone', 'Firefly A', 'Firefly B']
        post_mission_MAE = PostMissionMAE()

        self.map_data = MapData(map_name, mission_type, objective,
                                deploy_data, reward_list, enemy_unit_data,
                                initial_spells, initial_traits, initial_ai_states,
                                initial_locations, reserve_units, all_landmarks,
                                required_starters, pre_mission_MAE, mid_mission_MAE_list,
                                required_survivors, post_mission_MAE)


class SouthLampSwitchOn(MapActionEvent):

    def __init__(self):

        triggers = [ArrivalTrigger((16,17,1,1), 1, unit='Wriggle')]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):


        if not self.map.all_landmarks['South Lantern'].lit:

            self.center_on('Wriggle')
            self.say("Lucky for us, shining light through this fog is no problem for fireflies.",
                 "Wriggle",
                 "Wriggle")

            self.play_sfx('shimmer')
            self.show_animation('light_spell', (18,18))
            self.play_sfx('shimmer')
            self.show_animation('light_spell', (14,18))
            self.play_sfx('shimmer')
            self.show_animation('light_spell', (12,22))
            self.play_sfx('shimmer')
            self.show_animation('light_spell', (20,22))

            self.map.all_landmarks['South Lantern'].switch_state(True)
            self.map.all_landmarks['South Lantern 2'].switch_state(True)
            self.map.all_landmarks['South Lantern 3'].switch_state(True)
            self.map.all_landmarks['South Lantern 4'].switch_state(True)

        else:

            if self.map.all_landmarks['South Lantern'].light_range < 8:

                self.center_on('Wriggle')
                self.say("Ok, everyone! Keep pushing! We need to make this light even brighter!",
                         "Wriggle",
                         "Wriggle")

                self.play_sfx('shimmer')
                self.show_animation('light_spell', (18,18))
                self.play_sfx('shimmer')
                self.show_animation('light_spell', (14,18))
                self.play_sfx('shimmer')
                self.show_animation('light_spell', (12,22))
                self.play_sfx('shimmer')
                self.show_animation('light_spell', (20,22))


                self.map.all_landmarks['South Lantern'].light_range += 2
                self.map.all_landmarks['South Lantern'].lit_tiles = self.map.all_landmarks['South Lantern'].generate_range()

            if self.map.all_landmarks['South Lantern 2'].light_range < 8:
                self.map.all_landmarks['South Lantern 2'].light_range += 2
                self.map.all_landmarks['South Lantern 2'].lit_tiles = self.map.all_landmarks['South Lantern 2'].generate_range()
            if self.map.all_landmarks['South Lantern 3'].light_range < 8:
                self.map.all_landmarks['South Lantern 3'].light_range += 2
                self.map.all_landmarks['South Lantern 3'].lit_tiles = self.map.all_landmarks['South Lantern 3'].generate_range()
            if self.map.all_landmarks['South Lantern 4'].light_range < 8:
                self.map.all_landmarks['South Lantern 4'].light_range += 2
                self.map.all_landmarks['South Lantern 4'].lit_tiles = self.map.all_landmarks['South Lantern 4'].generate_range()

            self.map.update_fog_map()


class CheckWriggleRemoved(MapActionEvent):

    def __init__(self):

        triggers = []
        MapActionEvent.__init__(self, triggers, repeat = True)

    def execute(self):

        # Disables South Lanterns
        if self.map.check_occupancy((16, 17)) != 'Wriggle':
            if self.map.all_landmarks['South Lantern'].lit:

                self.map.all_landmarks['South Lantern'].light_range = 2
                self.map.all_landmarks['South Lantern'].lit_tiles = self.map.all_landmarks['South Lantern'].generate_range()
                self.map.all_landmarks['South Lantern'].switch_state(False)

            if self.map.all_landmarks['South Lantern 2'].lit:

                self.map.all_landmarks['South Lantern 2'].light_range = 2
                self.map.all_landmarks['South Lantern 2'].lit_tiles = self.map.all_landmarks['South Lantern 2'].generate_range()
                self.map.all_landmarks['South Lantern 2'].switch_state(False)

            if self.map.all_landmarks['South Lantern 3'].lit:

                self.map.all_landmarks['South Lantern 3'].light_range = 2
                self.map.all_landmarks['South Lantern 3'].lit_tiles = self.map.all_landmarks['South Lantern 3'].generate_range()
                self.map.all_landmarks['South Lantern 3'].switch_state(False)

            if self.map.all_landmarks['South Lantern 4'].lit:

                self.map.all_landmarks['South Lantern 4'].light_range = 2
                self.map.all_landmarks['South Lantern 4'].lit_tiles = self.map.all_landmarks['South Lantern 4'].generate_range()
                self.map.all_landmarks['South Lantern 4'].switch_state(False)


        # Disable Northern Lanterns
        if self.map.check_occupancy((29, 11)) != 'Wriggle':
            if self.map.all_landmarks['North Lantern'].lit:

                self.map.all_landmarks['North Lantern'].light_range = 2
                self.map.all_landmarks['North Lantern'].lit_tiles = self.map.all_landmarks['North Lantern'].generate_range()
                self.map.all_landmarks['North Lantern'].switch_state(False)

            if self.map.all_landmarks['North Lantern 2'].lit:

                self.map.all_landmarks['North Lantern 2'].light_range = 2
                self.map.all_landmarks['North Lantern 2'].lit_tiles = self.map.all_landmarks['North Lantern 2'].generate_range()
                self.map.all_landmarks['North Lantern 2'].switch_state(False)

            if self.map.all_landmarks['North Lantern 3'].lit:

                self.map.all_landmarks['North Lantern 3'].light_range = 2
                self.map.all_landmarks['North Lantern 3'].lit_tiles = self.map.all_landmarks['North Lantern 3'].generate_range()
                self.map.all_landmarks['North Lantern 3'].switch_state(False)


class NorthLampSwitchOn(MapActionEvent):

    def __init__(self):

        triggers = [ArrivalTrigger((29,11,1,1), 1, unit='Wriggle')]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if not self.map.all_landmarks['North Lantern'].lit:

            self.center_on('Wriggle')

            self.say("Listen up, everyone. I need you to lend me your strength to light up this fog, okay?",
                 "Wriggle",
                 "Wriggle")

            self.play_sfx('shimmer')
            self.show_animation('light_spell', (24,10))
            self.play_sfx('shimmer')
            self.show_animation('light_spell', (31,13))
            self.play_sfx('shimmer')
            self.show_animation('light_spell', (27,7))

            self.map.all_landmarks['North Lantern'].switch_state(True)
            self.map.all_landmarks['North Lantern 2'].switch_state(True)
            self.map.all_landmarks['North Lantern 3'].switch_state(True)

        else:

            if self.map.all_landmarks['North Lantern'].light_range < 8:

                self.center_on('Wriggle')
                self.say("Come on! More! This light needs to grow brighter!",
                         "Wriggle",
                         "Wriggle")

                self.play_sfx('shimmer')
                self.show_animation('light_spell', (24,10))
                self.play_sfx('shimmer')
                self.show_animation('light_spell', (31,13))
                self.play_sfx('shimmer')
                self.show_animation('light_spell', (27,7))


                self.map.all_landmarks['North Lantern'].light_range += 2
                self.map.all_landmarks['North Lantern'].lit_tiles = self.map.all_landmarks['North Lantern'].generate_range()

            if self.map.all_landmarks['North Lantern 2'].light_range < 8:
                self.map.all_landmarks['North Lantern 2'].light_range += 2
                self.map.all_landmarks['North Lantern 2'].lit_tiles = self.map.all_landmarks['North Lantern 2'].generate_range()

            if self.map.all_landmarks['North Lantern 3'].light_range < 8:
                self.map.all_landmarks['North Lantern 3'].light_range += 2
                self.map.all_landmarks['North Lantern 3'].lit_tiles = self.map.all_landmarks['North Lantern 3'].generate_range()

            self.map.update_fog_map()


class DeployFireflies(MapActionEvent):

    def __init__(self):

        triggers = [TurnNumTrigger(6), UnitAliveTrigger('Kotone', True)]

        MapActionEvent.__init__(self, triggers)

    def execute(self):
        self.center_on('Kotone')

        self.say("I'm not done yet! Have at thee, you fireflies!",
                 "Kotone",
                 "Kotone")

        self.fade_to_color('black', 1)
        self.deploy_unit('Firefly D', (26, 1))
        self.deploy_unit('Firefly E', (28, 3))
        self.deploy_unit('Firefly F', (30, 5))
        self.deploy_unit('Firefly G', (32, 7))

class PreMissionMAE(MapActionEvent):

    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Prologue event
        """
        self.set_fog_state(True)

        self.set_cursor_state(False)
        self.set_stats_display(False)


        self.map.add_ssp(SpiritSourcePoint('North SSP', (29, 11), 2))
        self.map.add_ssp(SpiritSourcePoint('South SSP', (16, 17), 2))
        self.map.add_light_source(LightSource('South Lantern', (18, 18), False, 2))
        self.map.add_light_source(LightSource('South Lantern 2', (14, 18), False, 2))
        self.map.add_light_source(LightSource('South Lantern 3', (12, 22), False, 2))
        self.map.add_light_source(LightSource('South Lantern 4', (20, 22), False, 2))
        self.map.add_light_source(LightSource('North Lantern', (24, 10), False, 2))
        self.map.add_light_source(LightSource('North Lantern 2', (31, 13), False, 2))
        self.map.add_light_source(LightSource('North Lantern 3', (27, 7), False, 2))

        # Add Wriggle to map
        self.add_temporary_ally('Wriggle')
        self.assign_spell('Wriggle', 'Fireball')
        self.assign_spell('Wriggle', 'Poison Dust')
        self.assign_trait('Wriggle', 'Magic+ Lv.1')

        self.set_unit_pos('Wriggle', (23,6))

        self.play_music('battle03')

        self.center_on('Wriggle')

        self.say("Hey, you! This is our turf and those are my bugs and you're being rude!",
                 'Wriggle',
                 'Wriggle')
        self.say("Yes, and? What are you going to do about it? After all, I, the great Kodama Lord Kotone, claim this land for my own!",
                 'Kotone',
                 'Kotone')
        self.say("Well, I have help coming, but for now I'll fight you myself if I have to!",
                 'Wriggle',
                 'Wriggle')
        self.emote('Kotone', 'lightbulb')
        self.say("Oh, one moment. How about we make a deal? If I win, then those bugs stay with me. For good.",
                 'Kotone',
                 'Kotone')
        self.startle('Wriggle')
        self.say("And if I win, those bugs return to me.",
                 'Wriggle',
                 'Wriggle')
        self.say("Then we're agreed. Walking trees, begin the attack!",
                 'Kotone',
                 'Kotone')

        self.move_unit('Walking Tree A', (23, 7))
        self.move_unit('Walking Tree B', (24, 7))
        self.move_unit('Walking Tree C', (24, 6))

        self.script_battle('Walking Tree A',
                               'Wriggle',
                               {'lhs_hit':False,
                                'rhs_hit':False,
                                'lhs_equip':0,
                                'rhs_equip':0,
                                'lhs_crit':False,
                                'rhs_crit':False,
                                }, plot_results=False)

        self.say("Darn! I can't hit them! Just what are you trying to pull, Kotone?",
                 'Wriggle',
                 'Wriggle')
        self.say("I'll tell, since you're pathetic. These trees that grow near Misty Lake have the same mist shield as Ayaka's trees. Not to mention, they're a lot easier to control.",
                 'Kotone',
                 'Kotone')
        self.say("Fine then. Well, if there's one thing bugs are good at...",
                 'Wriggle',
                 'Wriggle')
        self.startle('Wriggle')
        self.say("It's running away!",
                 'Wriggle',
                 'Wriggle')
        self.move_unit('Wriggle', (23,5))
        self.move_unit('Wriggle', (27,5))
        self.move_unit('Wriggle', (27,9))
        self.startle('Wriggle')
        self.emote('Walking Tree D', 'annoyed')
        self.emote('Wriggle', 'exclamation')
        self.fade_to_color('white', 0.1)
        self.set_unit_pos('Wriggle', (27,10))
        self.set_unit_pos('Walking Tree D', (27,9))
        self.fade_from_color('white', 0.1)

        self.startle('Wriggle')
        self.move_unit('Wriggle', (27, 14))

        self.say("She really is pathetic! Walking Trees! After her!",
                 'Kotone',
                 'Kotone')

        self.fade_to_color('black', 1.0)
        self.set_unit_pos('Walking Tree A', (26, 22))
        self.set_unit_pos('Walking Tree B', (25, 16))
        self.set_unit_pos('Walking Tree C', (31, 19))
        self.set_unit_pos('Walking Tree D', (24, 20))
        self.set_unit_pos('Wriggle', (31, 22))
        self.fade_from_color('black', 1.0)

        self.center_on('Wriggle')
        self.say("Finally. We have her cornered.",
                 'Fairy',
                 'Fairy')

        self.center_on('Marisa')

        self.say("Ugh, seriously? More fog? Look, couldn't we have picked a better time to arrive?",
                 'Reimu',
                 'Reimu')

        self.say("Well, this area's enveloped by fog every day at noon, but that's when Wriggle said she was going to fight Kotone.",
                 'Ran',
                 'Ran')

        self.center_on('Wriggle')

        self.say("It appears that the fight has not gone in Wriggle's favor.",
                 'Youmu',
                 'Youmu')
        self.say("You got that right! Perfect timing. Look, I no longer have my big fireflies, but if I can get to those spirit sources I should be able to summon my little fireflies to clear some of this fog!",
                 'Wriggle',
                 'Wriggle')

        self.center_on_coords((16, 17))

        self.set_cursor_state(True)

        self.say("Those lanterns aren't moonstone lanterns, so we need Wriggle there to activate them. Of course, my arrows are still effective in this fog, so count me in.",
                 'Eirin',
                 'Eirin')

        self.set_status_effect('Walking Tree A', 'Fog Veil')
        self.set_status_effect('Walking Tree B', 'Fog Veil')
        self.set_status_effect('Walking Tree C', 'Fog Veil')
        self.set_status_effect('Walking Tree D', 'Fog Veil')

        self.set_spirit_charge('Kotone', 700)

        # self.set_bg_overlay('Night')


class TreasureFoundMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((7, 5, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Player has discovered treasure under cherry blossom tree
        """

        self.say("Hidden beneath some bushes beside the small island shrine is a beat up old box.",
                None,
                None)
        self.say("Acquired Treasure Item: Lucky Cat!",
                None,
                None)
        self.add_item('treasure', '012_luckycat', 1)

class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.set_fog_state(False)
        self.remove_all_enemies()
        self.set_unit_pos('Kotone', (16, 17))
        self.set_unit_pos('Wriggle', (16, 19))
        self.set_unit_pos('Youmu', (17, 19))

        self.set_unit_pos('Reimu', (13, 21))
        self.set_unit_pos('Marisa', (14, 21))
        self.set_unit_pos('Keine', (15, 21))
        self.set_unit_pos('Yuyuko', (16, 21))
        self.set_unit_pos('Yukari', (17, 21))
        self.set_unit_pos('Ran', (18, 21))
        self.set_unit_pos('Chen', (19, 21))

        self.set_unit_pos('Mokou', (14,  22))
        self.set_unit_pos('Kaguya', (15, 22))
        self.set_unit_pos('Reisen', (16, 22))
        self.set_unit_pos('Eirin', (17, 22))
        self.set_unit_pos('Aya', (18, 22))
        self.set_unit_pos('Firefly A', (15, 17))
        self.set_unit_pos('Firefly B', (17, 17))


    def execute(self):

        self.set_stats_display(False)
        self.set_cursor_state(False)

        self.play_music('event01')

        self.center_on('Kotone')
        self.say("Go with her. I must keep my word.",
                 'Kotone',
                 'Kotone')
        self.move_unit('Firefly A', (15, 19))
        self.move_unit('Firefly B', (14, 19))

        self.say("Ha! I cannot believe how often I've lost to you.",
                 'Kotone',
                 'Kotone')
        self.say("I hate to admit it, but you're pretty tough. We could use someone like you.",
                 'Wriggle',
                 'Wriggle')

        self.say("I don't believe that's a good idea Wriggle. She could form another army against you, just like before!",
                 'Youmu',
                 'Youmu')
        self.say("Ah, well. If they're going to cause the next big crisis in Gensokyo, then youkai like me simply aren't working hard enough to cause trouble.",
                 'Yukari',
                 'Yukari')
        self.say("I...I do agree with you, Lady Yakumo.",
                 'Youmu',
                 'Youmu')
        self.say("Besides, at least this way will save us the trouble of having another out of control Kodama like Ayaka.",
                 'Ran',
                 'Ran')


        self.say("Ha! As if I would join forces with your pitiful team!",
                 'Kotone',
                 'Kotone')
        self.emote('Wriggle', 'annoyed')

        self.say("Calm down! Fine, whatever. Go and fend for yourself against everyone then. I'm sure that ridiculously violent miko would be happy to keep you company.",
                 'Wriggle',
                 'Wriggle')
        self.emote('Reimu', 'scribble')
        self.say("Ridiculously violent? Hey you, watch it, or I'll...",
                 'Reimu',
                 'Reimu')
        self.say("I heard she wiped out all the youkai at the east side of Gensokyo. She sure sounds like fun, right? So lemme ask again. You sure you won't join us?",
                 'Wriggle',
                 'Wriggle')
        self.say("I, er. Wait. Wait. A-Ayaka never told me a genocidal maniac like Reimu was working with them. I...I concede. I accept your offer.",
                 'Kotone',
                 'Kotone')
        self.emote('Wriggle', 'musicnote')
        self.say("Ok! That's what I like to hear. Welcome aboard, Kotone.",
                 'Wriggle',
                 'Wriggle')

        self.say("You have our gratitude for taking care of her for us.",
                 'Youmu',
                 'Youmu')
        self.say("What? No way! I should be thanking you for saving me back there today, Youmu! Really.",
                 'Wriggle',
                 'Wriggle')


        self.say("Wait. Youmu, there's just one more thing...if you don't mind.",
                 'Kotone',
                 'Kotone')
        self.move_unit('Youmu', (16, 18))

        self.say("I know we've fought again and again, and I begrudgingly admit that I recognize you as the stronger one.",
                 'Kotone',
                 'Kotone')
        self.say("As such, I won't need this spellcard anymore. I'm sure you'll be able to find a use for it in your coming battles.",
                 'Kotone',
                 'Kotone')
        self.say("I'll craft a new spellcard. More powerful than even Ayaka's.",
                 'Kotone',
                 'Kotone')
        self.say("Done there, Kotone? Okay, let's go grab Cirno, Rumia, and Mystia. We're gonna train until we're the strongest youkai ever!",
                 'Wriggle',
                 'Wriggle')
