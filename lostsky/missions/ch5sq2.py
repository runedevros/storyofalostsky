__author__ = 'Fawkes'

from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, ArrivalTrigger, UnitAliveTrigger, UnitHPBelowTrigger

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'The Otherworldly Mirror'
        location = 'River Basin'
        id_string = 'CH5SQ2'
        prereqs = ['CH5ST1']
        show_rewards = True
        desc = "Nitori sends word that they've encountered a Kodama Lord in the River Basin. The Kappa have recently found treasure there, so they're requesting assistance in protecting it."

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch5sq2.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat All',
                     'desc':'Defeat All Enemies!'
                     }

        deploy_data = {'enable':True,
                       'max_units':18,
                       'preset_units':{'Nitori':(23,6)},
                       'default_locations':{ 


                             'Ran':(7,12),
                             'Yukari':(7,13),
                             'Chen':(7,14),

                             'Reimu':(9,12),
                             'Marisa':(9,13),
                             'Aya':(9,14),

                             'Yuyuko':(8,16),
                             'Youmu':(9,16),
                             'Keine':(8,17),
                             'Mokou':(8,15),

                             'Kaguya':(7,18),
                             'Reisen':(7,19),
                             'Eirin':(7,20),

                                               },
                       'boxes':[(7, 12, 3, 9)]
                       }


        reward_list = [('treasure', 'mirror_fragment'), ('spell_action', 'Barrier Buster')
                   ]


        # Enemy Unit Data
        enemy_unit_data = [
                            {'template_name': 'Haruna44',
                                'unit_name': 'Haruna',
                                    'level': 32
                                },


                           {'template_name': 'Fairy',
                                'unit_name': 'Air Fairy A',
                                    'level': 25},
                           {'template_name': 'Fairy',
                                'unit_name': 'Air Fairy B',
                                    'level': 25},
                           {'template_name': 'Fairy',
                                'unit_name': 'Air Fairy C',
                                    'level': 25},
                           {'template_name': 'Fairy',
                                'unit_name': 'Air Fairy D',
                                    'level': 25},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy Captain',
                                    'level': 28},


                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy A',
                                    'level': 28},

                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy B',
                                    'level': 28},


                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 26},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 26},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 26},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree D',
                                    'level': 26},


                           {'template_name': 'Walking Tree',
                                'unit_name': 'Sacred Tree A',
                                    'level': 28},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Sacred Tree B',
                                    'level': 28},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Sacred Tree C',
                                    'level': 28},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Sacred Tree D',
                                    'level': 28},


                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel A',
                                    'level': 27},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel B',
                                    'level': 27},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel C',
                                    'level': 27},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel D',
                                    'level': 27},


                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly A',
                                    'level': 25},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly B',
                                    'level': 25},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly C',
                                    'level': 25},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly D',
                                    'level': 25},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly E',
                                    'level': 27},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly F',
                                    'level': 27},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly G',
                                    'level': 27},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly H',
                                    'level': 27},


                            ]

        initial_spells = {   'Haruna':['Evergreen Branch', 'Withering Fall'],
                             'Walking Tree A':['Leaf Crystal'],
                             'Walking Tree B':['Leaf Crystal'],
                             'Walking Tree C':['Leaf Crystal'],
                             'Walking Tree D':['Leaf Crystal'],
                             'Sacred Tree A':['Holy Amulet'],
                             'Sacred Tree B':['Weakening Amulet'],
                             'Sacred Tree C':['Holy Amulet'],
                             'Sacred Tree D':['Weakening Amulet'],

                             'Healer Fairy A':['Evergreen Branch', 'Healing Drop'],
                             'Healer Fairy B':['Evergreen Branch', 'Healing Drop'],

                             'Air Fairy A':['Holy Amulet'],
                             'Air Fairy B':['Dagger Throw'],
                             'Air Fairy C':['Leaf Crystal'],
                             'Air Fairy D':['Fireball'],

                             'Fairy Captain':['Holy Amulet'],

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
                             'Firefly H':['Poison Dust'],




                            }
        initial_traits = {'Haruna':['Magic+ Lv.2'],
                          'Fairy Captain':['Danmaku Sniper', 'Move+ Lv.1'],

                          'Air Fairy A':['Flight', 'Danmaku Master'],
                          'Air Fairy B':['Flight', 'Danmaku Master'],
                          'Air Fairy C':['Flight', 'Danmaku Master'],
                          'Air Fairy D':['Flight', 'Danmaku Master'],

                          'Healer Fairy A':['Flight'],
                          'Healer Fairy B':['Flight'],

                          'Firefly A':['Flight'],
                          'Firefly B':['Flight'],
                          'Firefly C':['Flight'],
                          'Firefly D':['Flight'],
                          'Firefly E':['Flight'],
                          'Firefly F':['Flight'],
                          'Firefly G':['Flight'],
                          'Firefly H':['Flight'],
                          }
        initial_ai_states = { 'Haruna':'HealerStandby',
                              'Fairy Captain':'Defend',
                              'Healer Fairy A':'HealerStandby',
                              'Healer Fairy B':'HealerStandby',

                              'Air Fairy A':'Defend',
                              'Air Fairy B':'Defend',
                              'Air Fairy C':'Defend',
                              'Air Fairy D':'Defend',

                              'Firefly A':'Pursuit',
                              'Firefly B':'Pursuit',
                              'Firefly C':'Pursuit',
                              'Firefly D':'Pursuit',
                              'Firefly E':'Defend',
                              'Firefly F':'Defend',
                              'Firefly G':'Defend',
                              'Firefly H':'Defend',

                              'Wind Weasel A':'Attack',
                              'Wind Weasel B':'Attack',
                              'Wind Weasel C':'Attack',
                              'Wind Weasel D':'Attack',


                              'Sacred Tree A':'Attack',
                              'Sacred Tree B':'Attack',
                              'Sacred Tree C':'Attack',
                              'Sacred Tree D':'Attack',

                              'Walking Tree A':'Attack',
                              'Walking Tree B':'Attack',
                              'Walking Tree C':'Attack',
                              'Walking Tree D':'Attack',
                              'Walking Tree E':'Attack',
                              'Walking Tree F':'Attack',


                            }
        initial_locations = {
                             'Haruna':(35, 13),
                             'Air Fairy A':(23, 20),
                             'Air Fairy B':(26, 6),
                             'Air Fairy C':(21, 14),
                             'Air Fairy D':(29, 11),
                             'Fairy Captain':(36, 13),

                             'Healer Fairy A':(20, 21),
                             'Healer Fairy B':(30, 7),

                             'Walking Tree A':(12, 10),
                             'Walking Tree B':(14, 21),
                             'Walking Tree C':(20, 19),
                             'Walking Tree D':(18, 14),

                             'Sacred Tree A':(34, 12),
                             'Sacred Tree B':(36, 12),
                             'Sacred Tree C':(34, 14),
                             'Sacred Tree D':(36, 14),

                             'Wind Weasel A':(21, 23),
                             'Wind Weasel B':(18, 21),
                             'Wind Weasel C':(31, 13),
                             'Wind Weasel D':(21, 13),

                             'Firefly A':(28, 7),
                             'Firefly B':(29, 9),
                             'Firefly C':(31, 19),
                             'Firefly D':(32, 21),
                             'Firefly E':(31, 8),
                             'Firefly F':(32, 10),
                             'Firefly G':(34, 18),
                             'Firefly H':(33, 16),

                             'Aya':(9,11),

                             'Kaguya':(2,11),
                             'Reisen':(2,12),
                             'Eirin':(2,13),

                             'Keine':(3,11),
                             'Mokou':(3,12),
                             'Marisa':(3,13),

                             'Chen':(4,11),
                             'Ran':(4,12),
                             'Yukari':(4,13),

                             'Youmu':(5,11),
                             'Yuyuko':(5,12),
                             'Reimu':(5,13),


                             }
        reserve_units = []
        all_landmarks = [

                         {'name':'house1',
                         'id_string':'house_1',
                         'location':(15, 6)},
                        {'name':'house2',
                         'id_string':'house_1',
                         'location':(32, 19)},
                        {'name':'house3',
                         'id_string':'house_1',
                         'location':(17, 19)},
                        {'name':'house4',
                         'id_string':'house_1',
                         'location':(29, 10)},
                        {'name':'house5',
                         'id_string':'house_1',
                         'location':(17, 9)},

                         {'name':'banner1',
                         'id_string':'snowbanner',
                         'location':(33, 11)},
                         {'name':'banner2',
                         'id_string':'snowbanner',
                         'location':(37, 11)},
                         {'name':'banner11',
                         'id_string':'snowbanner',
                         'location':(33, 15)},
                         {'name':'banner12',
                         'id_string':'snowbanner',
                         'location':(37, 15)},


        ]


        required_starters = ['Aya', 'Marisa', 'Youmu', 'Keine', 'Ran', 'Chen', 'Reimu', 'Mokou','Eirin','Reisen','Kaguya', 'Yukari', 'Yuyuko', 'Nitori']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [NitoriSpellHouse(), NitoriFlightHouse(), NitoriScopeHouse(), NitoriDoubleActionHouse(), NitoriCloakHouse(), HarunaSwitchMode()]
        required_survivors = ['Aya', 'Marisa', 'Youmu', 'Keine', 'Ran', 'Chen', 'Reimu', 'Mokou', 'Eirin', 'Reisen','Kaguya', 'Yukari', 'Yuyuko', 'Nitori', "Haruna", 'Fairy Captain']
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
        # Add Wriggle to map
        self.add_temporary_ally('Nitori')
        self.assign_trait('Nitori', 'Swimming')
        self.set_spirit_charge('Haruna', 500)
        self.set_spirit_charge('Healer Fairy A', 500)
        self.set_spirit_charge('Healer Fairy B', 500)

        self.play_music('battle02')

        self.set_unit_pos('Nitori', (12,8))
        self.center_on("Nitori")

        self.set_stats_display(False)
        self.set_cursor_state(False)
        self.say('Nitori!',
                 'Aya',
                 'Aya')
        self.say("So like we found this mirror shard and then got overrun by these fairies and trees and stuff! They must have been hiding here waiting to ambush us the moment we found the artifact.",
                 'Nitori',
                 'Nitori')
        self.say("Then! I stayed behind to make sure the other Kappa got to safety upstream. And that! Brings us to our current time.",
                 'Nitori',
                 'Nitori')
        self.say("So... What did you find again?",
                 'Marisa',
                 'Marisa')

        self.say("Hm, well. Some of Haruna's elites are out there. If I were her, I wouldn't use my best forces unless it was something very valuable.",
                 'Eirin',
                 'Eirin')
        self.say("Um, so my sensors detected super intense spiritual energy emanating from it! Maybe it's a super weapon?",
                 'Nitori',
                 'Nitori')

        self.center_on('Aya')
        self.emote('Aya', 'annoyed')
        self.say("Tell me you're joking. This is exactly what the Wolf Tengu were supposed to be here for!",
                 'Aya',
                 'Aya')
        self.say("Where are they! They should have been guarding this place!",
                 'Aya',
                 'Aya')

        self.center_on('Haruna')
        self.say("Here it is! A fragment of the Otherworldly Mirror.",
                 'Fairy Captain',
                 'Fairy')
        self.say("We should deal with these enemies now. Quickly, before the Wolf Tengu realize Miu has set up a diversion behind the mountain!",
                 'Haruna',
                 'Haruna')
        self.say("Our elite flying fairy corps are here. Our healing units are also equipped with your Evergreen Branch spell. Don't worry about us!",
                 'Fairy Captain',
                 'Fairy')
        self.say("I appreciate the reassurance. I trust you'll be able to take the fragment to safety even if I'm defeated. Now. Bring it to Miu.",
                 'Haruna',
                 'Haruna')

        self.center_on('Nitori')
        self.say("Nuts! What do I do? What do I do! They totally caught us off guard! Oh, yeah, by the way my equipment and spells are in these workshops!",
                 'Nitori',
                 'Nitori')
        self.set_cursor_state(True)
        self.center_on_coords((15,6))
        self.emote('Nitori', 'lightbulb')
        self.say("Oh, and! There're some shiny experimental devices that we've been working on in there, too, so it should be super duper fun to try them out!",
                 'Nitori',
                 'Nitori')
        self.set_cursor_state(False)

        self.center_on("Youmu")
        self.say("Mm. Unfortunately, there's no telling what Haruna intends to do with the artifact. Regardless, we can't let her have it!",
                 'Youmu',
                 'Youmu')

        self.set_cursor_state(True)
        self.set_stats_display(True)



class HarunaSwitchMode(MapActionEvent):

    def __init__(self):
        triggers=[UnitAliveTrigger('Haruna', True), UnitHPBelowTrigger('Haruna', 120)]

        MapActionEvent.__init__(self, triggers)

    def execute(self):
        self.say("I must do all I can to protect the Otherworldly Mirror! It shall not fall into their hands!",
                 'Haruna',
                 'Haruna')
        self.map.all_units_by_name['Haruna'].spell_actions = [None, None, None, None, None]
        self.assign_spell('Haruna','Withering Fall')
        self.set_ai_state('Haruna', 'Attack')
        self.map.all_units_by_name['Haruna'].equipped = 0


class NitoriSpellHouse(MapActionEvent):

    def __init__(self):
        """
        Gives Nitori her spells
        """

        triggers = [ArrivalTrigger((15, 6, 1, 1), 1, unit='Nitori')]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        self.say("Ohmigosh! My Fireball and Tanabata Festival spells! Thank goodie goodness they're still here!",
                 'Nitori',
                 'Nitori')

        self.assign_spell('Nitori', 'Fireball')
        self.assign_spell('Nitori', 'Tanabata Festival')

class NitoriFlightHouse(MapActionEvent):

    def __init__(self):
        """
        Gives Nitori her spells
        """

        triggers = [ArrivalTrigger((17, 9, 1, 1), 1, unit='Nitori')]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        self.say("Oh, yeah. I kept this cute heli-pack here just in case. With this, I'll be able to take to the skies and fly high! Lift off!",
                 'Nitori',
                 'Nitori')

        # Replaces Nitori's first trait (swimming) with Flight
        self.map.all_units_by_name['Nitori'].traits[0] = self.map.engine.trait_catalog['Heli-pack']

class NitoriScopeHouse(MapActionEvent):

    def __init__(self):
        """
        Gives Nitori her spells
        """

        triggers = [ArrivalTrigger((32, 19, 1, 1), 1, unit='Nitori')]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        self.say("So uh, this Kappa Scope hasn't been tested yet, but whatevs. It should boost my range and accuracy!",
                 'Nitori',
                 'Nitori')

        self.assign_trait('Nitori', 'Kappa Scope')

class NitoriDoubleActionHouse(MapActionEvent):

    def __init__(self):
        """
        Gives Nitori her spells
        """

        triggers = [ArrivalTrigger((17, 19, 1, 1), 1, unit='Nitori')]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        self.say("This? The Moriya folks asked me to develop this totally awesome multi-lock radar. It'll let me track and attack multiple targets at once!",
                 'Nitori',
                 'Nitori')

        self.assign_trait('Nitori', 'Double Action')


class NitoriCloakHouse(MapActionEvent):

    def __init__(self):
        """
        Gives Nitori her spells
        """

        triggers = [ArrivalTrigger((29, 10, 1, 1), 1, unit='Nitori')]

        MapActionEvent.__init__(self, triggers)

    def execute(self):
        self.say("Ooh, my trusty camouflage cloak! With this I can go poof and stuff! They'll never hit me now, hehe.",
                 'Nitori',
                 'Nitori')

        self.assign_trait('Nitori', 'Optical Camo')

class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.remove_all_enemies()
        self.set_unit_pos('Haruna', (35, 13))
        self.set_unit_pos('Fairy Captain', (36, 13))
        self.set_unit_pos('Youmu', (35, 15))
        self.set_unit_pos('Nitori', (36, 15))
        self.set_unit_pos('Aya', (34, 15))

        self.set_unit_pos('Yuyuko', (35, 17))
        self.set_unit_pos('Yukari', (34, 17))

        self.set_unit_pos('Eirin', (33, 17))
        self.set_unit_pos('Ran', (34, 18))
        self.set_unit_pos('Chen', (32, 17))
        self.set_unit_pos('Keine', (36, 17))
        self.set_unit_pos('Reimu', (37, 17))
        self.set_unit_pos('Marisa', (37, 17))
        self.set_unit_pos('Kaguya', (35, 18))
        self.set_unit_pos('Mokou', (33, 18))
        self.set_unit_pos('Reisen', (36, 18))


    def execute(self):

        self.set_stats_display(False)
        self.set_cursor_state(False)



        self.play_music('event02')

        self.center_on('Haruna')
        self.say("Hand over that magical weapon, Haruna!",
                 'Youmu',
                 'Youmu')

        self.emote('Haruna', 'questionmark')
        self.say("Magical weapon? Is that what you think it is?",
                 'Haruna',
                 'Haruna')

        self.emote('Fairy Captain', 'lightbulb')
        self.say("I have an idea. *whisper* *whisper*",
                 'Fairy Captain',
                 'Fairy')
        self.say("An excellent plan. Now, Youmu. Would you like to help us find the other half of the artifact?",
                 'Haruna',
                 'Haruna')
        self.say("If we are agreed, you may keep this half, and we can both prevent it from falling into nefarious hands.",
                 'Haruna',
                 'Haruna')


        self.say("Say, uh. Look, I really don't want to write the headline \"Honorable Heroes Help Kodama Lord Assemble Superweapon.\"",
                 'Aya',
                 'Aya')
        self.say("False. It's no weapon. It's a means of sending a message to...someone important. Even across this border.",
                 'Haruna',
                 'Haruna')

        self.say("So then \"Brave Heroes Help Kodama Lord Summon Reinforcements from the Outside World\"? B-better?",
                 'Aya',
                 'Aya')
        self.say("Hmm. Do we have a reason not to trust her? Of all the Kodama, she's proven to be the most reasonable.",
                 'Youmu',
                 'Youmu')
        self.say("Additionally, you can have the Kappa study it to verify my assertion.",
                 'Haruna',
                 'Haruna')
        self.say("Furthermore, once this is over, you have my word that I will not interfere with your battle against Fuyuhana again.",
                 'Haruna',
                 'Haruna')
        self.say("This I swear on my honor as the Kodama Lord of the Northern Forests.",
                 'Haruna',
                 'Haruna')

        self.say("Very well. I'll trust you. We have a deal.",
                 'Youmu',
                 'Youmu')

        self.move_unit('Fairy Captain', (35, 14))
        self.startle('Fairy Captain')
        self.emote('Youmu', 'musicnote')

        self.say("Nitori?",
                 'Youmu',
                 'Youmu')
        self.say("Ohmisupergosh! It's a kind of energy we never, ever seen before! So like! Maybe it's a magic that has long fallen out of use! Retro style!",
                 'Nitori',
                 'Nitori')
        self.say("Um, um. I couldn't tell you a centimeter more without taking it to my workshop, so! I'm gonna pocket this one for a bit! Yeah!",
                 'Nitori',
                 'Nitori')


        self.say("So. You mentioned there was a second half...?",
                 'Aya',
                 'Aya')
        self.say("I did. You'll receive more information when we're somewhere safe, farther away from here.",
                 'Haruna',
                 'Haruna')
        self.say("Understood. Until we hear from you again then.",
                 'Youmu',
                 'Youmu')





