from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, TurnNumTrigger, ArrivalTrigger, UnitAliveTrigger
# from lostsky.battle.mapobj import SpiritSourcePoint

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        """

        """
        name = 'Road to the Sanctuary'
        location = 'Upper Youkai Mountain'
        id_string = 'CH3ST4'
        prereqs = ['CH3ST3']
        show_rewards = True
        desc = "Breaking news! An urgent call for help was received from the upper path leading to the summit of the guardian Misaki. This reporter will be on the frontlines in Youmu's team up close and personal with the action!"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch3st4.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat Boss',
                     'target':'Haruna',
                     'desc':'Defeat Haruna'
                     }

        deploy_data = {'enable':True,
                       'max_units':10,
                       'preset_units':{'Momiji': (28, 17)},
                       'boxes':[(2, 31, 3, 3)],
                       'default_locations':{'Youmu':(4,33),
                                            'Ran':(3,33),
                                            'Chen':(2,33),
                                            'Reimu':(4,32),
                                            'Keine':(2,32),
                                            'Alice':(2,31),
                                            'Marisa':(4,31),
                                            'Mokou':(3,32),
                                            'Aya':(3,31),
                                            },
                       }
        reward_list = [('treasure', 'synth_earth'),
            ('treasure', 'synth_fire'),
            ('treasure', 'synth_water'),

                   ]

        # Enemy Unit Data
        enemy_unit_data = [


                            # Tengu Unit
                            {'template_name': 'Wolf Tengu',
                             'unit_name': 'Wolf Tengu A',
                             'level': 8},
                            {'template_name': 'Wolf Tengu',
                             'unit_name': 'Wolf Tengu B',
                             'level': 8},



                            # Group 1
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 9},
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 9},
                            {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy A',
                                    'level': 9},
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 9},
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 9},

                            # Group 2
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 10},
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy D',
                                    'level': 10},
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy E',
                                    'level': 10},

                            # Group 3
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 12},
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree D',
                                    'level': 12},

                            # Group 4
                            {'template_name': 'Haruna',
                                'unit_name': 'Haruna',
                                    'level': 14},
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy F',
                                    'level': 10},
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy G',
                                    'level': 10},
                            {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy B',
                                    'level': 12},
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree E',
                                    'level': 12},
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree F',
                                    'level': 12},
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree G',
                                    'level': 12},
                            #Group 5
                            {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel A',
                                    'level': 11},
                            {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel B',
                                    'level': 11},
                            {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel C',
                                    'level': 11},

                            # End scene units

                            {'template_name': 'Ayaka',
                             'unit_name': 'Ayaka',
                             'level': 15},
                            {'template_name': 'Miu',
                             'unit_name': 'Miu',
                             'level': 15},
                            {'template_name': 'Kotone',
                             'unit_name': 'Kotone',
                             'level': 15},
                            {'template_name': 'Tsubaki',
                             'unit_name': 'Tsubaki',
                             'level': 15},
                            {'template_name': 'Nitori',
                             'unit_name': 'Nitori',
                             'level': 15},


                            ]

        initial_spells = {'Haruna':['Holy Amulet'],
                          'Fairy A':['Encourage', 'Fireball'],
                          'Fairy B':['Encourage', 'Fireball'],
                          'Fairy C':['Spirit Break'],
                          'Fairy D':['Holy Amulet'],
                          'Fairy E':['Holy Amulet'],
                          'Fairy F':['Holy Amulet'],
                          'Fairy G':['Holy Amulet'],
                          'Healer Fairy A':['Healing Drop'],
                          'Healer Fairy B':['Healing Drop'],
                          'Walking Tree A':['Leaf Crystal'],
                          'Walking Tree B':['Leaf Crystal'],
                          'Walking Tree C':['Leaf Crystal'],
                          'Walking Tree D':['Leaf Crystal'],
                          'Walking Tree E':['Leaf Crystal'],
                          'Walking Tree F':['Leaf Crystal'],
                          'Walking Tree G':['Leaf Crystal'],
                          'Wind Weasel A':['Dagger Throw'],
                          'Wind Weasel B':['Dagger Throw'],
                          'Wind Weasel C':['Dagger Throw'],
                          'Wolf Tengu A':['Dagger Throw'],
                          'Wolf Tengu B':['Dagger Throw'],
                            }
        initial_traits = {'Haruna':['Focused Movement', 'Defense+ Lv.3'],
                          'Healer Fairy B':['Healing+ Lv.1'],
                          'Walking Tree E':['Regen Lv.2'],
                          'Walking Tree F':['Regen Lv.2'],
                          'Walking Tree G':['Regen Lv.2'],
                          }
        initial_ai_states = {'Haruna':'Defend',
                             'Fairy A':'Support',
                             'Fairy B':'Support',
                             'Fairy C':'Attack',
                             'Fairy D':'Attack',
                             'Fairy E':'Attack',
                             'Fairy F':'Defend',
                             'Fairy G':'Defend',
                             'Healer Fairy A':'HealerStandby',
                             'Healer Fairy B':'HealerStandby',
                             'Walking Tree A':'Attack',
                             'Walking Tree B':'Attack',
                             'Walking Tree C':'Attack',
                             'Walking Tree D':'Attack',
                             'Walking Tree E':'Defend',
                             'Walking Tree F':'Defend',
                             'Walking Tree G':'Defend',
                             'Wind Weasel A':'Defend',
                             'Wind Weasel B':'Defend',
                             'Wind Weasel C':'Defend',
                            }
        initial_locations = {
                             'Fairy A':(10, 26),
                             'Fairy B':(10, 29),
                             'Healer Fairy A':(13, 28),
                             'Walking Tree A':(8, 26),
                             'Walking Tree B':(9, 28),

                             'Fairy C':(21, 17),
                             'Fairy D':(20, 16),
                             'Fairy E':(20, 18),

                             'Walking Tree C':(17, 14),
                             'Walking Tree D':(11, 14),

                             'Haruna':(14, 3),
                             'Fairy F':(13, 5),
                             'Fairy G':(15, 5),
                             'Healer Fairy B':(14, 5),
                             'Walking Tree E':(14, 6),
                             'Walking Tree F':(13, 7),
                             'Walking Tree G':(15, 7),

                             'Wolf Tengu A':(14, 4),
                             'Wolf Tengu B':(30, 13),


                             'Wind Weasel A':(5, 15),
                             'Wind Weasel B':(6, 16),
                             'Wind Weasel C':(5, 17),

                             # Player party
                             'Youmu':(3, 32),
                             'Ran':(2, 33),
                             'Chen':(3, 33),
                             'Marisa':(4, 33),
                             'Keine':(2, 34),
                             'Mokou':(3, 34),
                             'Reimu':(4, 34),
                             }
        reserve_units = ['Ayaka', 'Miu', 'Kotone', 'Tsubaki', 'Nitori']#[list of unit names     to deploy later in mission]
        all_landmarks = [{'name':'Torii 1',
                          'id_string':'small_torii',
                          'location':(14, 8)
                          },
                        {'name':'Torii 2',
                          'id_string':'small_torii',
                          'location':(14, 9)
                          },
                        {'name':'Torii 3',
                          'id_string':'small_torii',
                          'location':(14, 10)
                          },
                        {'name':'Torii 4',
                          'id_string':'small_torii',
                          'location':(14, 11)
                          },
                        {'name':'Torii 5',
                          'id_string':'small_torii',
                          'location':(14, 12)
                          },
                        {'name':'Torii 6',
                          'id_string':'small_torii',
                          'location':(14, 13)
                          },
                        {'name':'Shrine 1',
                          'id_string':'shrine',
                          'location':(14, 1)
                          },
                        {'name':'House 1',
                          'id_string':'house_2',
                          'location':(30, 13)
                          },
                        {'name':'House 2',
                          'id_string':'house_2',
                          'location':(5, 16)
                          },


        ]

        required_starters = ['Youmu', 'Ran', 'Chen', 'Marisa', 'Reimu', 'Keine', 'Mokou']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [TreasureInfoMAE(), TreasureFoundMAE()]
        required_survivors = ['Youmu', 'Ran', 'Chen', 'Marisa', 'Reimu', 'Keine', 'Mokou', 'Aya', 'Momiji', 'Haruna']
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

        self.play_music('battle02')

        # Adds Aya to the party
        self.add_to_party('Aya')

        self.set_unit_pos('Aya', (3, 30))
        self.assign_spell('Aya', 'Leaf Crystal')
        self.assign_spell('Aya', 'Holy Amulet')
        self.assign_spell('Aya', 'Tengu Wind Path')


        # Add Momiji to map
        self.add_temporary_ally('Momiji')
        self.assign_spell('Momiji', 'Dagger Throw')
        self.assign_spell('Momiji', 'Rice Cake')
        self.assign_trait('Momiji', 'Attack+ Lv.1')
        self.set_unit_pos('Momiji', (30, 14))
        self.set_hp('Momiji', 15)
        self.set_spell_uses('Momiji', 'Rice Cake', 3)

        self.center_on('Wolf Tengu A')
        self.say('Argh!', 'Wolf Tengu A', 'Wolf Tengu')
        self.set_hp('Wolf Tengu A', 12)
        self.script_battle('Haruna', 'Wolf Tengu A',
                            {'lhs_equip':0,
                             'rhs_equip':0,

                             'rhs_hit':False,
                             'lhs_hit':True,
                             'lhs_crit':True,
                             'rhs_crit':True,
                             })
        self.center_on('Momiji')
        self.say("This is bad. I told them to retreat, but they didn't listen, and now this...",
            "Momiji",
            "Momiji")
        self.say("My deepest apologies, Momiji. I would do anything to right my wrongs, but right now I can't even move.",
            "Wolf Tengu",
            "Wolf Tengu")
        self.say("What's done is done. Just stay here in this outpost. In this condition, all I want you to do is recover.",
            "Momiji",
            "Momiji")
        self.say("I understand. Take care, Momiji.",
            "Wolf Tengu",
            "Wolf Tengu")
        self.kill_unit('Wolf Tengu B')
        self.emote('Momiji', 'dotdotdot')
        self.say("Youmu's group should be coming up from the rear soon.",
            "Momiji",
            "Momiji")

        self.center_on('Haruna')
        self.startle('Fairy F')
        self.say("Hmph. Just one left.",
                    "Fairy",
                    "Fairy")
        self.center_on('Fairy C')
        self.say("And our fairies are in hot pursuit of that last Wolf Tengu. They didn't stand a chance!",
                    "Fairy",
                    "Fairy")
        self.center_on('Haruna')
        self.say("Well done, everyone. Once we have disposed of Momiji, we'll have this segment of the mountain under our complete control.",
                    "Haruna",
                    'Haruna')
        self.say("We're very fortunate that you were able to sway this many of the mountain's trees to our side.",
                    "Fairy",
                    "Fairy")
        self.say("Fortunate indeed. It was quite difficult. Most trees here are loyal to either the Tengu who tended to them well or to Misaki herself.",
                    "Haruna",
                    'Haruna')
        self.say("I have one more thing to report, Miss Haruna. Based on hearsay from the wild youkai, the Otherworldly Mirror you're looking for may be in the river basin.",
                    "Fairy",
                    "Fairy")
        self.say("It's not conclusive, but it is a step forward in the right direction. We'll continue our search.",
                    "Fairy",
                    "Fairy")
        self.say("Thank you. Please, remember to be careful. The river basin is heavily guarded by the Tengu, and I'd rather you return alive.",
                    "Haruna",
                    'Haruna')

        self.center_on('Aya')
        self.say("Momiji!",
            'Aya',
            'Aya')
        self.center_on('Momiji')
        self.move_unit('Momiji', (28, 17))
        self.startle('Momiji')
        self.say("Aya!",
            'Momiji',
            'Momiji')
        self.say("Hang on, Momiji! We're coming to help!",
            'Aya',
            'Aya')
        self.center_on('Youmu')
        self.say("Those enemies in the way will make reaching her difficult.",
            'Youmu',
            'Youmu')
        self.say("For you, maybe. Aya! Let's fly around these bozos and get to Momiji asap!",
            'Marisa',
            'Marisa')
        self.say("You got it, Marisa! Don't fall behind or I'll leave you in the dust!",
            'Aya',
            'Aya')

        self.set_cursor_state(True)
        self.set_stats_display(True)



class TreasureInfoMAE(MapActionEvent):

    def __init__(self):
        triggers = [TurnNumTrigger(2),
                    UnitAliveTrigger('Haruna', True)
        ]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Haruna gives information on the nature of the western house and how only Momiji can enter it.
        """
        self.set_stats_display(False)
        self.center_on('Haruna')
        self.say("Miss Haruna!",
            "Fairy",
            "Fairy")
        self.center_on_coords((5, 16))
        self.say("The Wind Weasel team we sent out has found a house that's protected by a barrier.",
            "Fairy",
            "Fairy")
        self.say("Further, it seems only a Wolf Tengu like that Momiji is able to pass through it.",
            "Fairy",
            "Fairy")
        self.center_on('Haruna')
        self.say("I see. Leave it be for now. We'll deal with it later. It is most likely holding treasure, but that is not among our current objectives.",
            'Haruna',
            'Haruna')
        self.say("Remember, we're not conquerers. We've no reason to plunder and raid. Still, it might contain more than mere treasure, so do guard it.",
            'Haruna',
            'Haruna')
        self.say("Aye.",
            "Fairy",
            "Fairy")
        self.set_stats_display(True)



class TreasureFoundMAE(MapActionEvent):

    def __init__(self):

        triggers = [ArrivalTrigger((5, 16, 1, 1), 1, unit='Momiji')]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Player has discovered treasure at house
        """
        self.emote('Momiji', 'exclamation')

        self.say("The sentry barrier is still up. Good.",
            'Momiji',
            'Momiji')
        self.say("This is the spirit recharger device that the Kappa have been working on lately. It'll give anyone a refreshing boost of spiritual energy.",
            'Momiji',
            'Momiji')
        self.say("Obtained Kappa's secret invention!",
            None,
            None)

        # One copy goes to Momiji
        self.assign_spell('Momiji', 'Spirit Recharge')
        # One copy goes the player inventory
        self.add_item('spell_action', 'Spirit Recharge', 1)

class PostMissionMAE(MapActionEvent):
    def __init__(self):
        # Triggers on turn 2
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):
        self.remove_all_enemies()
        self.set_unit_pos('Haruna', (14, 5))
        self.set_unit_pos('Momiji', (14, 4))
        self.set_unit_pos('Youmu', (14, 2))
        self.set_unit_pos('Aya', (14, 1))
        self.set_unit_pos('Keine', (13, 2))
        self.set_unit_pos('Mokou', (13, 1))
        self.set_unit_pos('Marisa', (13, 0))

        self.set_unit_pos('Ran', (15, 2))
        self.set_unit_pos('Chen', (15, 1))
        self.set_unit_pos('Reimu', (15, 0))

    def execute(self):

        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.center_on('Youmu')
        self.say("I hadn't expected the Tengu reinforcements to arrive so soon.",
            'Haruna',
            'Haruna')

        self.deploy_unit('Ayaka', (14, 15))
        self.deploy_unit('Miu', (13, 15))
        self.deploy_unit('Kotone', (15, 15))

        self.move_unit('Ayaka', (14, 8))
        self.move_unit('Miu', (13, 9))
        self.move_unit('Kotone', (15, 9))

        self.startle('Ayaka')
        self.say("Step aside, Haruna, we'll handle this.",
            'Ayaka',
            'Ayaka')
        self.move_unit('Haruna', (14, 9))
        self.say("Momiji Inubarashi, the White Wolf of Youkai Mountain. How I looked forward to this battle.",
            'Ayaka',
            'Ayaka')
        self.say("Oh? So you've heard of me, have you?",
            'Momiji',
            'Momiji')
        self.say("Mind you don't praise yourself too much. Your clan simply has had a long history dating back to the time of Fuyuhana's reign.",
            'Ayaka',
            'Ayaka')
        self.say("Good grief. She's as stuffy sounding as she was in that play. How does anyone talk like that normally?",
            'Reimu',
            'Reimu')
        self.say("Youmu, the area above is holy ground to us Kodama. We care not what you and the Tengu have agreed upon. We will stop you here and now.",
            'Haruna',
            'Haruna')
        self.say("Regardless, that sanctuary holds the key to ending this crisis. We won't back down without a fight!",
            'Youmu',
            'Youmu')
        self.say("Geez! How did that place earn so many holy points from everyone anyway? Look, one trial was already way too much, so just get the heck out of our way! ",
            'Marisa',
            'Marisa')

        self.startle('Momiji')

        self.say("Go on ahead, Youmu! I'll hold Ayaka and her allies here.",
            'Momiji',
            'Momiji')
        self.say("I can't! It'll be you against the most powerful of Kodama Lords! Don't be rash!",
            'Youmu',
            'Youmu')
        self.emote('Momiji', 'annoyed')
        self.say("Just go! We're counting on you to succeed, so you can count on us to succeed, too!",
            'Momiji',
            'Momiji')
        self.move_unit('Youmu', (14, 3))
        self.emote('Youmu', 'dotdotdot')
        self.say("Are you certain you'll be okay?",
            'Youmu',
            'Youmu')
        self.startle('Marisa')
        self.move_unit('Marisa', (14, 2))
        self.say("Trust her. We didn't come all this way up here just to turn back. Now get those legs running! Go!",
            'Marisa',
            'Marisa')
        self.say("Momiji... Thank you.",
            'Youmu',
            'Youmu')
        self.move_unit('Youmu', (14, -1))
        self.move_unit('Marisa', (14, -1))
        self.move_unit('Reimu', (14, -1))
        self.move_unit('Aya', (14, -1))
        self.move_unit('Mokou', (14, -1))
        self.move_unit('Ran', (14, -1))
        self.move_unit('Keine', (14, -1))
        self.move_unit('Chen', (14, -1))


        self.say("Oh? So you are quite skilled. It's an honor to do battle with you, Momiji.",
            'Ayaka',
            'Ayaka')
        self.emote('Momiji', 'dotdotdot')
        self.say("Your skill isn't one to balk at either.",
            'Momiji',
            'Momiji')


        self.move_unit('Ayaka', (14, 7))
        self.move_unit('Miu', (13, 8))
        self.move_unit('Kotone', (15, 8))

        self.emote('Momiji', 'annoyed')
        self.move_unit('Momiji', (14, 5))

        self.play_music('battle01')
        self.say("It appears to be a one-sided battle. I think she's mocking you, Momiji",
            'Tsubaki',
            'Tsubaki')
        self.deploy_unit('Tsubaki', (15, 15))
        self.move_unit('Tsubaki', (15, 11))
        self.deploy_unit('Nitori', (13, 15))
        self.move_unit('Nitori', (13, 11))

        self.say("Well. It has been a while since I have gotten my hands dirty. Nitori and I will help, Momiji. ",
            'Tsubaki',
            'Tsubaki')
        self.say("Lady Akahane!",
            'Momiji',
            'Momiji')
        self.say("Kodama Lords, your presence on the Youkai Mountain is an affront to our people. Show some respect or we'll force you to bow down to us.",
            'Tsubaki',
            'Tsubaki')
        self.say("An affront? Open your eyes! Our will is that of the natural world! Tengu or human, we'll annihilate all who dare oppose the will of the forest. En garde.",
            'Ayaka',
            'Ayaka')



        self.set_cursor_state(True)
        self.set_stats_display(True)
