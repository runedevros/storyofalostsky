from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.core.linalg import Vector2
from lostsky.battle.mapaction import MapActionEvent, UnitAliveTrigger, TeamTurnTrigger, TurnNumTrigger, CustVarTrigger, ArrivalTrigger
from random import choice
import pygame

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = "The Mirror Assembled"
        location = "Gensokyo's Border"
        id_string = 'CH5SQ3'
        prereqs = ['CH5SQ2']
        show_rewards = True
        desc = "Today we have an exclusive sneak peak into Kawashiro Lab's analysis of the artifact. We're hot in pursuit for the other fragment of the Otherworldly Mirror. The Kodama Lord Miu told us to rendezvous somewhere nearby Gensokyo's border."

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch5sq3.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat All',
                     'desc':'Defeat Asa and all her allies!'}

        deploy_data = {'enable':True,
                       'max_units':18,
                       'preset_units':{},
                       'default_locations':{

                                            'Mokou':(18, 26),
                                            'Chen':(19, 26),
                                            'Ran':(20, 26),
                                            'Yukari':(21, 26),
                                            'Youmu':(22, 26),
                                            'Yuyuko':(23, 26),
                                            'Reimu':(24, 26),
                                            'Marisa':(25, 26),
                                            'Aya':(26, 26),

                                            'Keine':(20, 27),
                                            'Kaguya':(21, 27),
                                            'Reisen':(22, 27),
                                            'Eirin':(23, 27),
                                            'Alice':(24, 27),

                                               },
                       'boxes':[(18, 26, 9, 3), ]
                       }


        reward_list = [('spell_action','Evergreen Branch'), ('spell_action','Pollenating Butterfly')
                   ]


        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Asa',
                                'unit_name': 'Asa',
                                    'level': 40},


                            # Phase 1 : Youmu and Marisa
                            {'template_name': 'Mirror Youmu',
                                'unit_name': 'Youmu?',
                                    'level': 32},
                            {'template_name': 'Mirror Marisa',
                                'unit_name': 'Marisa?',
                                    'level': 32},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 30},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 30},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 30},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy D',
                                    'level': 30},

                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel A',
                                    'level': 30},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel B',
                                    'level': 30},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel C',
                                    'level': 30},
                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy A',
                                    'level': 30},
                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy B',
                                    'level': 30},


                            # Phase 2: Lord Fuzzy / Misaki / Ayaka
                           {'template_name': 'Mirror Ayaka',
                                'unit_name': 'Ayaka?',
                                    'level': 32},
                           {'template_name': 'Mirror Misaki',
                                'unit_name': 'Misaki?',
                                    'level': 32},
                           {'template_name': 'Lord Fuzzy',
                                'unit_name': 'Lord Fuzzy?',
                                    'level': 32},


                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball A',
                                    'level': 30},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball B',
                                    'level': 30},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball C',
                                    'level': 30},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball D',
                                    'level': 30},

                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 30},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 30},


                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree A',
                                    'level': 30},
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree B',
                                    'level': 30},

                           {'template_name': 'Miu',
                                'unit_name': 'Miu',
                                    'level': 30},




                            ]

        initial_spells = {'Asa':['Reflected Temenos'],

                          # Wave 1 - Youmu and Marisa
                          'Youmu?':['Ageless Obsession', 'Dagger Throw'],
                          'Marisa?':['Master Spark', 'Fireball'],
                          'Fairy A':['Holy Amulet'],
                          'Fairy B':['Holy Amulet'],
                          'Fairy C':['Barrier Buster'],
                          'Fairy D':['Barrier Buster'],
                          'Wind Weasel A':['Dagger Throw'],
                          'Wind Weasel B':['Dagger Throw'],
                          'Wind Weasel C':['Dagger Throw'],
                          'Healer Fairy A':['Evergreen Branch'],
                          'Healer Fairy B':['Evergreen Branch'],


                          'Lord Fuzzy?':['Fuzzball Swarm'],
                          'Fuzzball A':['Shimmering Stars'],
                          'Fuzzball B':['Shimmering Stars'],
                          'Fuzzball C':['Dagger Throw'],
                          'Fuzzball D':['Dagger Throw'],

                          'Ayaka?':["Jubokko's Touch"],
                          'Cursed Tree A':['Spirit Break'],
                          'Cursed Tree B':['Spirit Break'],

                          'Misaki?':["Withering Fall"],
                          'Walking Tree A':['Leaf Crystal'],
                          'Walking Tree B':['Leaf Crystal'],

                          'Miu':["Pollenating Butterfly"]

                            }

        initial_traits = {'Youmu?':['Sharp Eyes', 'Attack+ Lv.2', 'Move+ Lv.1', 'Deadly Strike', 'Fighting Spirit'],
                          'Marisa?':['Flight', 'Magic Reactor', 'Move+ Lv.1', 'Homing Attack', 'Spirit Booster'],
                          'Lord Fuzzy':['Defense+ Lv.2', 'Danmaku Sniper'],
                          'Ayaka?':['Move+ Lv.3', 'Deadly Strike', 'Attack+ Lv.3', 'Lock On', 'Close Combat'],
                          'Misaki?':['Regen Lv.3', 'Magic+ Lv.2', 'Danmaku Sniper']

                          }
        initial_ai_states = {'Asa':'Attack',
                             'Youmu?':'Defend',
                             'Marisa?':'Pursuit',
                             'Fairy A':'Attack',
                             'Fairy B':'Attack',
                             'Fairy C':'Attack',
                             'Fairy D':'Attack',
                             'Wind Weasel A':'Attack',
                             'Wind Weasel B':'Attack',
                             'Wind Weasel C':'Attack',

                             'Healer Fairy A':'HealerStandby',
                             'Healer Fairy B':'HealerStandby',

                             'Lord Fuzzy?':'Attack',
                             'Fuzzball A':'Attack',
                             'Fuzzball B':'Attack',
                             'Fuzzball C':'Attack',
                             'Fuzzball D':'Attack',

                             'Ayaka?':'Pursuit',
                             'Cursed Tree A':'Attack',
                             'Cursed Tree B':'Attack',

                             'Misaki?':'Pursuit',
                             'Walking Tree A':'Attack',
                             'Walking Tree B':'Attack',


                            }
        initial_locations = {'Miu':(22,14),

                             'Youmu':(22, 16),
                             'Yuyuko':(23, 16),
                             'Eirin':(21, 16),

                             'Aya':(20, 18),
                             'Chen':(20, 19),
                             'Yukari':(21, 18),
                             'Ran':(21, 19),
                             'Reimu':(22, 18),
                             'Marisa':(22, 19),
                             'Mokou':(23, 18),
                             'Keine':(23, 19),
                             'Kaguya':(24,18),
                             'Reisen':(24, 19)

                             }
        reserve_units = ['Asa','Marisa?', 'Youmu?', 'Fairy A', 'Fairy B', 'Fairy C', 'Fairy D',
                         'Wind Weasel A', 'Wind Weasel B', 'Wind Weasel C',
                         'Healer Fairy A', 'Healer Fairy B',
                         'Lord Fuzzy?', 'Fuzzball A', 'Fuzzball B', 'Fuzzball C', 'Fuzzball D',
                         'Misaki?', 'Walking Tree A', 'Walking Tree B',
                         'Ayaka?', 'Cursed Tree A', 'Cursed Tree B']
        all_landmarks = [
                         {'name':'torii_N',
                          'id_string':'small_torii',
                          'location':(22, 13)},
                         {'name':'torii_S',
                          'id_string':'small_torii',
                          'location':(22, 17)},
        ]

        required_starters = ['Youmu', 'Ran', 'Chen', 'Marisa', 'Reimu', 'Keine', 'Mokou', 'Aya', 'Kaguya', 'Reisen', 'Eirin' ,'Yuyuko', 'Yukari']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [InitAsaAttack(), TagTarget(), AsaAoE(), AsaRestStage(), Phase2Start(), Phase3Start()]
        required_survivors = ['Youmu', 'Ran', 'Chen', 'Marisa', 'Reimu', 'Keine', 'Mokou', 'Aya', 'Kaguya', 'Reisen', 'Eirin', 'Yukari', 'Yuyuko', 'Asa', 'Miu']
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
        self.set_cursor_state(False)
        self.set_stats_display(False)


        self.play_music('event02')

        self.set_spirit_charge('Miu', 600)
        self.center_on('Miu')

        self.say('Aya! What did Nitori find out about the artifact?',
                 'Youmu',
                 'Youmu')


        self.say("Got it right here! Nitori says, and I quote:",
                 'Aya',
                 'Aya')

        self.say("\"It's a super cool magical device that transmits the thoughts of the user to an identical mirror via beta-sigma spiritual energy waves over a quantum subspace field!\"",
                 'Aya',
                 'Aya')

        self.emote("Youmu","questionmark")
        self.emote("Reimu","questionmark")
        self.emote("Marisa","dotdotdot")

        self.say("I-I'm sorry. In layman's terms, if possible...?",
                 'Youmu',
                 'Youmu')
        self.say('Yeah, seriously. Did Nitori say something more intelligible?',
                 'Reimu',
                 'Reimu')


        self.emote("Eirin","lightbulb")

        self.say("Oh. Lunarians used to use similar technology to communicate some centuries ago. I wonder if this mirror is something of ours.",
                 'Eirin',
                 'Eirin')
        self.say("I'll explain. Simply put, it allows anyone holding it to communicate to someone else holding an identical mirror regardless of their distance from each other.",
                 'Eirin',
                 'Eirin')
        self.say("And, based on my studies, I'm convinced it'll work for communicating with people beyond Gensokyo's border.",
                 'Eirin',
                 'Eirin')


        self.say("Much better. You're a lifesaver, Eirin.",
                 'Reimu',
                 'Reimu')
        self.say('(Those Kappa and Tengu sure love to flaunt their superior technological prowess over us humans. So annoying.)',
                 'Reimu',
                 'Reimu')


        self.say('I hold the other half of the mirror. Haruna mentioned that using it would be as simple as bringing the two halves close together. So...',
                 'Miu',
                 'Miu')
        self.move_unit("Youmu", (22, 15))
        self.emote('Youmu', 'dotdotdot')
        self.emote('Miu', 'musicnote')

        self.emote('Youmu', 'exclamation')
        self.startle('Youmu')
        self.move_unit('Youmu', (22, 16))


        self.play_sfx('shoot4')
        self.fade_to_color('white', 0.4)
        self.deploy_unit('Asa', (22, 15))
        self.fade_from_color('white', 0.4)

        self.emote('Asa', 'dotdotdot')
        self.say('Whoa, I was out like a light! How long have I been asleep?',
                 'Asa',
                 'Asa')
        self.say('Haha, ah, well. I suspected this might happen. Old artifacts do have a nasty habit of taking on minds of their own.',
                 'Yukari',
                 'Yukari')
        self.say('Good day. I am Asa, Asa of the Otherworldly Mirror.',
                 'Asa',
                 'Asa')
        self.say('Oh? Curious. Have I been stolen? You are not the prince I was destined to serve.',
                 'Asa',
                 'Asa')

        self.center_on('Youmu')
        self.show_animation('sealing_spell', (22,16))

        self.center_on('Marisa')
        self.show_animation('sealing_spell', (22, 19))
        self.say('How odd.',
                 'Asa',
                 'Asa')
        self.say('And as lore says, the older they are, the more powerful they become.',
                 'Yukari',
                 'Yukari')

        self.say('I see that you possess formidable strength based on your memories of surpassing powerful foes. Ah. Curious indeed.',
                 'Asa',
                 'Asa')


        self.play_sfx('shimmer')
        self.show_animation('magic_cast', (25, 15))
        self.deploy_unit('Marisa?', (25,15))


        self.play_sfx('shimmer')
        self.show_animation('magic_cast', (19, 15))
        self.deploy_unit('Youmu?', (19,15))


        self.play_music('battle04')
        self.say('Irrespective of your past, you shall not surpass me.',
                 'Asa',
                 'Asa')


        self.set_spirit_charge('Marisa?', 575)
        self.set_invincibility_state('Asa', True)

        self.script_battle('Marisa?',
                           'Miu',
                           {'lhs_hit':True,
                            'rhs_hit':False,
                            'lhs_equip':0,
                            'rhs_equip':0,
                            'lhs_crit':False,
                            'rhs_crit':False,
                              }, plot_results=False)



        self.say("I'm a fully fledged Kodama Lord. I won't go down that easily!",
                 'Miu',
                 'Miu')

        self.script_battle('Asa',
                           'Miu',
                           {'lhs_hit':True,
                            'rhs_hit':False,
                            'lhs_equip':0,
                            'rhs_equip':0,
                            'lhs_crit':False,
                            'rhs_crit':False,
                              }, plot_results=False)

        self.say('Spell neutralized. Barrier fully operational.',
                 'Asa',
                 'Asa')


        move_locations = {  'Mokou':(18, 26),
                            'Chen':(19, 26),
                            'Ran':(20, 26),
                            'Yukari':(21, 26),
                            'Youmu':(22, 26),
                            'Yuyuko':(23, 26),
                            'Reimu':(24, 26),
                            'Marisa':(25, 26),
                            'Aya':(26, 26),

                            'Keine':(20, 27),
                            'Kaguya':(21, 27),
                            'Reisen':(22, 27),
                            'Eirin':(23, 27),
                            'Miu':(22, 30)

                            }


        self.emote('Yukari', 'exclamation')
        self.say("She's neutralizing anything that gets near her with her magic.",
                 'Yukari',
                 'Yukari')

        self.say('Into the gap everyone!',
                 'Yukari',
                 'Yukari')

        self.fade_to_color('white', 1.5)
        for character_name, coord in move_locations.items():
            self.set_unit_pos(character_name, coord)
        self.fade_from_color('white', 1.5)

        self.center_on('Youmu')

        self.emote('Marisa', 'annoyed')
        self.say("Hey! You copycat! That's my signature spell you just stole!",
                 'Marisa',
                 'Marisa')

        self.say('Pft, "My"? You mean the spell you took from Yuuka?',
                 'Reimu',
                 'Reimu')
        self.say("Aw, come on! As they say, imitation is the finest form of flattery. So no harm done, right?",
                 'Marisa',
                 'Marisa')
        self.say("...Speak for yourself.",
                 'Reimu',
                 'Reimu')

        self.center_on('Asa')
        self.say('Unauthorized users will be deleted by the full force of my magic. Commencing.',
                 'Asa',
                 'Asa')

        phase1units = {

                                 'Fairy A':(25, 17),
                                 'Fairy B':(19, 17),
                                 'Fairy C':(28, 16),
                                 'Fairy D':(16, 16),
                                 'Wind Weasel A':(22, 18),
                                 'Wind Weasel B':(12, 17),
                                 'Wind Weasel C':(32, 17),

                                 'Healer Fairy A':(18, 14),
                                 'Healer Fairy B':(26, 14),
            }

        for name, coord in phase1units.items():

            self.play_sfx('shimmer')
            self.show_animation('magic_cast', coord)
            self.deploy_unit(name, coord)


        self.say("You know. Without a spirit source nearby, she must be using up much of her energy summoning all those copies.",
                 'Ran',
                 'Ran')
        self.say("Therefore, if we keep taking her copies down, we'll suck her energy dry so she won't have enough to defend herself!",
                 'Ran',
                 'Ran')
        self.say("I hadn't expected to be friendly with a Kodama, but Miu, take cover. Leave Asa to us!",
                 'Youmu',
                 'Youmu')
        self.say("The feeling's mutual! But...all right. ...Thanks.",
                 'Miu',
                 'Miu')

        self.kill_unit('Miu')

        self.set_spirit_charge('Youmu?', 699)
        self.set_spirit_charge('Marisa?', 475)
        self.set_spirit_charge('Healer Fairy A', 600)
        self.set_spirit_charge('Healer Fairy B', 600)

        self.set_stats_display(True)
        self.set_cursor_state(True)

        self.set_cust_var('Activate', 0)


class Phase2Start(MapActionEvent):

    def __init__(self):

        triggers = [

                    TeamTurnTrigger(2),
                    UnitAliveTrigger('Marisa?', False),
                    UnitAliveTrigger('Youmu?', False),
                    UnitAliveTrigger('Fairy A', False),
                    UnitAliveTrigger('Fairy B', False),
                    UnitAliveTrigger('Fairy C', False),
                    UnitAliveTrigger('Fairy D', False),
                    UnitAliveTrigger('Wind Weasel A', False),
                    UnitAliveTrigger('Wind Weasel B', False),
                    UnitAliveTrigger('Wind Weasel C', False),
                    UnitAliveTrigger('Healer Fairy A', False),
                    UnitAliveTrigger('Healer Fairy B', False),

                    ]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        phase2_units = [('Lord Fuzzy?',(22, 10)),
                        ('Fuzzball A',(20, 12)),
                        ('Fuzzball B',(24, 12)),
                        ('Fuzzball C',(19, 11)),
                        ('Fuzzball D',(25, 11)),

                        ('Ayaka?',(12, 13)),
                        ('Cursed Tree A',(11, 14)),
                        ('Cursed Tree B',(13, 14)),

                        ('Misaki?',(32, 13)),
                        ('Walking Tree A',(31, 14)),
                        ('Walking Tree B',(33, 14)),



                            ]

        self.center_on('Asa')


        self.say("Oh. Perhaps these replicas will perform better.",
                 'Asa',
                 'Asa')

        self.map.all_units_by_name['Asa'].render_hp_change(700, 450)
        self.set_hp('Asa', 450)

        for new_unit, coord in phase2_units:

            unit_name = self.map.check_occupancy(coord)

            if unit_name:
                self.center_on_coords(coord)
                self.play_sfx('shimmer')
                self.show_animation('magic_cast', coord)
                self.random_teleport(unit_name, (18, 26, 9, 3))
                self.center_on(unit_name)
                self.emote(unit_name, 'questionmark')


            # Deploy the enemy units
            self.center_on_coords(coord)
            self.play_sfx('shimmer')
            self.show_animation('magic_cast', coord)
            self.deploy_unit(new_unit, coord)

        self.set_spirit_charge('Ayaka?', 600)


class Phase3Start(MapActionEvent):


    def __init__(self):

        triggers = [
                     UnitAliveTrigger('Lord Fuzzy?', False),
                     UnitAliveTrigger('Fuzzball A', False),
                     UnitAliveTrigger('Fuzzball B', False),
                     UnitAliveTrigger('Fuzzball C', False),
                     UnitAliveTrigger('Fuzzball D', False),
                     UnitAliveTrigger('Ayaka?', False),
                     UnitAliveTrigger('Cursed Tree A', False),
                     UnitAliveTrigger('Cursed Tree B', False),
                     UnitAliveTrigger('Misaki?', False),
                     UnitAliveTrigger('Walking Tree A', False),
                     UnitAliveTrigger('Walking Tree B', False),

                            ]

        MapActionEvent.__init__(self,triggers)

    def execute(self):


        self.center_on('Asa')
        self.map.all_units_by_name['Asa'].render_hp_change(450, 250)
        self.set_hp('Asa', 250)
        self.set_invincibility_state('Asa', False)

        self.say("Barrier down. Alas. I can rely only upon my magic now.",
                 'Asa',
                 'Asa')


class InitAsaAttack(MapActionEvent):

    def __init__(self):
        triggers = [TeamTurnTrigger(2), CustVarTrigger('Activate', 0)]
        MapActionEvent.__init__(self, triggers, repeat=True)


    def execute(self):

        # Asa attack cycle
        # Enemy Turn 1: Charging Spells
        # Turn 2: Fire Spell Card - Go back to Turn 1
        # Turn 3: Fire AOE


        self.center_on('Asa')
        self.show_animation('sealing_spell', (22,15))

        self.say("Preparing spell.",
            'Asa',
            'Asa')

        self.set_cust_var('Activate', 1)


class TagTarget(MapActionEvent):

    def __init__(self):
        triggers = [TeamTurnTrigger(1), CustVarTrigger('Activate', 1), UnitAliveTrigger('Asa', True)]
        MapActionEvent.__init__(self, triggers, repeat = True)


    def render_grid(self, target):

        target_location = target.location_tile
        nearest_neighbors = [target.location_tile+Vector2(0, 1),
                             target.location_tile+Vector2(0, -1),
                             target.location_tile+Vector2(1, 0),
                             target.location_tile+Vector2(-1, 0)]
        next_nearest_neighbors = [target.location_tile+Vector2(0, 2),
                                  target.location_tile+Vector2(2, 0),
                                  target.location_tile+Vector2(-2, 0),
                                  target.location_tile+Vector2(0, -2),
                                  target.location_tile+Vector2(1, 1),
                                  target.location_tile+Vector2(-1, 1),
                                  target.location_tile+Vector2(1, -1),
                                  target.location_tile+Vector2(-1, -1),

                                  ]

        # Draw a target zone moving outward from target.
        self.add_highlight(target_location)
        self.render_update()
        self.pause(0.1)
        for location in nearest_neighbors:
            self.add_highlight(location)
        self.render_update()
        self.pause(0.1)
        for location in next_nearest_neighbors:
            self.add_highlight(location)

        self.render_update()
        self.pause(1)

        # Remove all highlights
        self.remove_highlight(target_location)
        all_neighbor_locations = next_nearest_neighbors+nearest_neighbors
        for location in all_neighbor_locations:
            self.remove_highlight(location)


    def render_update(self):

        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.render_menu_panel()

        # Draws emoticon frame
        pygame.display.flip()

    def execute(self):
        """
        Targets the unit with highest density of neighbors
        """

        # Determine the unit with highest density of neighbors

        prioritized_units = []

        for unit in self.map.team1:

            score = 0

            for neighbor in self.map.team1:

                neighbor_distance = abs(unit.location_tile.x - neighbor.location_tile.x) + abs(unit.location_tile.y - neighbor.location_tile.y)

                if neighbor_distance == 0:
                    pass
                elif neighbor_distance == 1:
                    score += 2
                elif neighbor_distance == 2:
                    score += 1

            prioritized_units.append([score, unit.name, unit])

        prioritized_units.sort()
        prioritized_units.reverse()

        target = prioritized_units[0][2]

        self.center_on(target.name)
        self.say("Acquiring target.",
            'Asa',
            'Asa')


        self.set_status_effect(target.name, "Target")
        self.render_grid(target)
        self.set_cust_var('Activate', 2)


class AsaAoE(MapActionEvent):

    def __init__(self):
        triggers = [TeamTurnTrigger(2), UnitAliveTrigger('Asa', True), CustVarTrigger('Activate', 2)]
        MapActionEvent.__init__(self, triggers, repeat = True)
        self.user = 'Asa'

    def animate_action(self, target):

        self.play_sfx('beam2')
        self.show_animation('asa_light_spell', target.location_tile+Vector2(0,-0.5))

    def render_effect(self, target, damage_value):


        text_name = self.map.engine.bfont.render("Reflected Cascade", True, (0, 0, 0))
        half_width = text_name.get_width()/2


        effect_text = self.map.engine.render_outlined_text(str(damage_value), self.map.engine.cfont, (255, 0, 0), (255, 255, 255))

        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
        self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
        self.map.engine.surface.blit(text_name, (420-half_width, 25))
        target.plot_stats()
        self.map.engine.surface.blit(effect_text, ((target.location_pixel.x+18-effect_text.get_width()/2, target.location_pixel.y-25)-self.map.screen_shift*self.map.engine.tilesize))

        pygame.display.flip()
        self.map.engine.clock.tick(60)
        self.map.engine.pause(1)

    def execute_damage(self, target):

        # Damage values
        target_HP_fraction = 0.30
        nearest_neighbor_HP_fraction = 0.25
        nnn_HP_fraction = 0.20

        damage = int(target.maxHP*target_HP_fraction)
        start_HP = target.HP
        target.HP -= damage

        if target.HP < 0:
            target.HP = 0

        self.center_on(target.name)

        self.play_sfx('shimmer')
        self.show_animation('light_spell', target.location_tile)
        self.play_sfx('crit')
        self.render_effect(target, damage)
        target.render_hp_change(start_HP, target.HP)

        if target.HP == 0:
            target.alive = False
            if not target.ressurected and (target.has_trait_property('Revive Lv.1') or target.has_trait_property('Revive Lv.2') or target.has_trait_property('Revive Lv.3')):
                self.map.check_map_event_revive(target)
            else:
                self.map.kill(target, render_fadeout=True)


        for neighbor in self.map.all_units_by_name.values():
            # Drop affects all units except for lord fuzzy
            if neighbor.name != self.user:
                # find distance

                neighbor_distance = abs(target.location_tile.x - neighbor.location_tile.x) + abs(target.location_tile.y - neighbor.location_tile.y)

                # Damage to nearest neighbors
                if neighbor_distance == 1:

                    damage = int(neighbor.maxHP*nearest_neighbor_HP_fraction)

                # Damage to NNN
                elif neighbor_distance == 2:

                    damage = int(neighbor.maxHP*nnn_HP_fraction)

                # Target out of range, skip
                else:
                    continue

                start_HP = neighbor.HP
                neighbor.HP -= damage

                if neighbor.HP < 0:
                    neighbor.HP = 0


                self.play_sfx('shimmer')
                self.show_animation('light_spell', neighbor.location_tile)

                self.play_sfx('hit')
                self.render_effect(neighbor, damage)
                neighbor.render_hp_change(start_HP, neighbor.HP)

                if neighbor.HP == 0:
                    neighbor.alive = False


                    if not neighbor.ressurected and (neighbor.has_trait_property('Revive Lv.1') or neighbor.has_trait_property('Revive Lv.2') or neighbor.has_trait_property('Revive Lv.3')):
                        self.map.check_map_event_revive(neighbor)
                    else:
                        self.map.kill(neighbor, render_fadeout=True)




    def execute(self):
        # Find targetted units

        if "Stun" not in self.map.all_units_by_name['Asa'].status.keys():
            for unit in self.map.team1:

                if "Target" in unit.status.keys():



                    self.say('Fully charged!',
                         'Asa',
                         'Asa')

                    self.say('Mirror Sign: Reflected Cascade!',
                         'Asa',
                         'Asa')

            for unit in self.map.team1:
                if "Target" in unit.status.keys():

                    self.center_on(unit.name)

                    # Shows the first spell animation
                    self.animate_action(unit)

                    # Hits the targetted unit.
                    self.execute_damage(unit)

        for unit in self.map.team1:
            if "Target" in unit.status.keys():
                unit.remove_status('Target')

        # Asa does no further actions this turn
        self.set_cust_var('Activate', 3)

class AsaRestStage(MapActionEvent):

    def __init__(self):

        triggers = [CustVarTrigger('Activate', 3), TeamTurnTrigger(1)]

        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):
        # Activates Asa for a recharge next turn

        self.set_cust_var('Activate', 0)


class PostMissionMAE(MapActionEvent):
    def __init__(self):
        # Triggers on turn 2
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):
        self.remove_all_enemies()
        self.stop_music()

        positions = {
                             'Youmu':(22, 16),
                             'Yuyuko':(23, 16),
                             'Eirin':(21, 16),

                             'Aya':(20, 18),
                             'Chen':(20, 19),
                             'Yukari':(21, 18),
                             'Ran':(21, 19),
                             'Reimu':(22, 18),
                             'Marisa':(22, 19),
                             'Mokou':(23, 18),
                             'Keine':(23, 19),
                             'Kaguya':(24,18),
                             'Reisen':(24, 19),

                             'Asa':(22, 14),
                             'Miu':(22, 15)
                             }

        for unit, coord in positions.items():

            self.set_unit_pos(unit, coord)

    def execute(self):

        self.play_music('event01')
        self.center_on('Youmu')

        if 'mirror_fragment' in self.map.engine.player.treasures.keys():
            self.map.engine.player.remove_treasure('mirror_fragment')

        self.say('My sincerest apologies. I allowed my instincts to take over after many centuries of disuse.',
             'Asa',
             'Asa')
        self.say('That was unbecoming of a servant of the royal court.',
             'Asa',
             'Asa')

        self.say("It's fine. That's in the past now. Asa, who was it that you served?",
             'Youmu',
             'Youmu')

        self.say('My sister and I were crafted by a magician to open a route of communication between two persons of royal blood.',
             'Asa',
             'Asa')

        self.say('If I were to hazard a guess, maybe one of my people from before we severed our ties to Earth?',
             'Eirin',
             'Eirin')


        self.say('How you speak of them is curious. I gather I am no longer needed in this era. Unfortunate.',
             'Asa',
             'Asa')
        self.say("I have another question if you don't mind. Can you still speak with your sister?",
             'Youmu',
             'Youmu')
        self.say("Yes. Hm. I can sense her within the archives of an occult society school in the old capital of Kyoto.",
             'Asa',
             'Asa')

        self.say('R-really? Then I would like to send a message...if you would be so kind.',
             'Miu',
             'Miu')
        self.say("Of course. I am happy to continue to serve my purpose. Now, place your hand upon the mirror and speak your thoughts.",
             'Asa',
             'Asa')
        self.say("I deliver a message on behalf of the Kodama Lord of the Northern Forests to the guardians of the old capital's trees.",
             'Miu',
             'Miu')



        self.say("\"My dearest mother and father, I hope that you are well. It has been centuries since I left to follow Lady Fuyuhana into battle...\"",
             'Miu',
             'Miu')
        self.fade_to_color('black', 1.0)
        self.fade_from_color('black', 1.0)
        self.say("\"... and so I am determined to create a future where we Kodama may work alongside those of Gensokyo rather than rule over them.\"",
             'Miu',
             'Miu')
        self.say("\"I pray that this message has reached you while you are still capable of receiving it.\"",
             'Miu',
             'Miu')
        self.say("My sister says that the sealing club she is held by investigates paranormal events. She will do her best to ensure that your message reaches its destination.",
             'Asa',
             'Asa')
        self.say("Please take me with you so that I may relay any response.",
             'Asa',
             'Asa')

        self.say("Be hopeful but realistic. With how much things have changed outside, it may be years before we'll hear a reply of any sort.",
             'Yukari',
             'Yukari')
        self.say("We've waited for centures. A few more years is nothing.",
             'Miu',
             'Miu')

        self.say("Oh, by the way. The reason that Haruna didn't come here is because she's gathering her trees and the Kodama to convince them that this pointless conflict needs to end. I'll join her there soon.",
             'Miu',
             'Miu')
        self.say("There's just one last challenge left, Youmu. Defeat Fuyuhana and bring this crisis to its conclusion! And...thank you for your help today.",
             'Miu',
             'Miu')


        self.say("Yes. Thank you, Miu. I am glad we now fight on the same side.",
             'Youmu',
             'Youmu')

        self.say("Phew! That's two less Kodama to deal with. I say we've done pretty good for ourselves, even if we're still reeling from that fight with Asa.",
             'Reimu',
             'Reimu')

        self.say("Ah. One more thing. Please, take these, our spells. I am certain a little bit of Kodama magic will help you during your last battle. And please, take care.",
             'Miu',
             'Miu')

