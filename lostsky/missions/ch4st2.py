__author__ = 'Fawkes'

from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, SSPStateTrigger, TurnNumTrigger
from lostsky.battle.mapobj import LightSource, SpiritSourcePoint
from lostsky.core.linalg import Vector2

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'In Defense of Eientei'
        location = 'Eientei'
        id_string = 'CH4ST2'
        prereqs = ['CH4ST1']
        show_rewards = True
        desc = "Eientei is under seige! Will Youmu and her friends arrive in time before those helpless bunnies are trampled underneath the vicious, heavy roots of the Kodamas' Walking Trees?"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch4st2.txt'
        mission_type = 'battle'
        objective = {'type':'Defend and Defeat All',
                     'desc':'Protect Eientei and defeat all enemies!',
                     'location_box': [20, 16, 3, 3],
                     'location_name': 'Eientei',

                     }

        deploy_data = {'enable':True,
                       'max_units':18,
                       'preset_units':{},
                       'default_locations':{'Youmu':(11,18),
                                            'Ran':(10,18),
                                            'Chen':(12,18),
                                            'Reimu':(10,16),
                                            'Aya':(11,16),
                                            'Marisa':(12,16),
                                            'Keine':(9,17),
                                            'Mokou':(13,17),
                                            'Alice':(11,17),
                                            'Eirin':(21, 17),
                                            'Reisen':(21, 18)
                                               },
                       'boxes':[(9, 16, 5, 3), (20,16, 3, 3)]
                       }


        reward_list = [('spell_action', 'Rice Cake'),
                       ('treasure', 'synth_wood'),
                       ('treasure', 'synth_water'),

                   ]


        # Enemy Unit Data
        enemy_unit_data = [ {'template_name': 'NPCKaguya',
                                'unit_name': 'Kaguya',
                                    'level': 16
                                },


                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 16
                                },
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 16
                                },
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 16
                                },
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree D',
                                    'level': 16
                                },
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree E',
                                    'level': 16
                                },

                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly A',
                                    'level': 17
                                },
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly B',
                                    'level': 17
                                },
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly C',
                                    'level': 17
                                },
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly D',
                                    'level': 17
                                },
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly E',
                                    'level': 17
                                },


                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 17
                                },
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 16
                                },
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 17
                                },
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel A',
                                    'level': 17
                                },
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel B',
                                    'level': 17
                                },


                            # Reinforcement Wave
                           {'template_name': 'Kodama Lord',
                                'unit_name': 'Kodama Lord',
                                    'level': 22
                                },
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree A',
                                    'level': 18
                                },
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree B',
                                    'level': 18
                                },
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree C',
                                    'level': 18
                                },
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy D',
                                    'level': 18
                                },
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy E',
                                    'level': 18
                                },
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy F',
                                    'level': 18
                                },
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy G',
                                    'level': 18
                                },


                            ]

        initial_spells = {'Walking Tree A':['Leaf Crystal'],
                          'Walking Tree B':['Leaf Crystal'],
                          'Walking Tree C':['Leaf Crystal'],
                          'Walking Tree D':['Leaf Crystal'],
                          'Walking Tree E':['Leaf Crystal'],
                          'Firefly A':['Fireball'],
                          'Firefly B':['Poison Dust'],
                          'Firefly C':['Fireball'],
                          'Firefly D':['Poison Dust'],
                          'Firefly E':['Fireball'],

                          'Fairy A':['Holy Amulet'],
                          'Fairy B':['Holy Amulet'],
                          'Fairy C':['Holy Amulet'],
                          'Fairy D':['Holy Amulet'],
                          'Fairy E':['Holy Amulet'],
                          'Fairy F':['Holy Amulet'],
                          'Fairy G':['Holy Amulet'],

                          'Wind Weasel A':['Dagger Throw'],
                          'Wind Weasel B':['Dagger Throw'],


                          'Cursed Tree A':['Spirit Break'],
                          'Cursed Tree B':['Poison Dust'],
                          'Cursed Tree C':['Poison Dust'],
                          'Cursed Tree D':['Spirit Break'],

                          'Kodama Lord':['Leaf Crystal']

                            }
        initial_traits = {'Firefly A':['Flight'],
                          'Firefly B':['Flight'],
                          'Firefly C':['Flight'],
                          'Firefly D':['Flight'],
                          'Firefly E':['Flight'],
                          'Cursed Tree A':['Fog Veil'],
                          'Cursed Tree B':['Fog Veil'],
                          'Cursed Tree C':['Fog Veil'],
                          'Cursed Tree D':['Fog Veil'],
                          }
        initial_ai_states = {'Walking Tree A':'Pursuit',
                             'Walking Tree B':'Pursuit',
                             'Walking Tree C':'Pursuit',
                             'Walking Tree D':'Pursuit',
                             'Walking Tree E':'Pursuit',
                             'Firefly A':'Attack',
                             'Firefly B':'Attack',
                             'Firefly C':'Attack',
                             'Firefly D':'Attack',
                             'Firefly E':'Attack',
                             'Fairy A':'Pursuit',
                             'Fairy B':'Pursuit',
                             'Fairy C':'Pursuit',
                             'Fairy D':'Pursuit',
                             'Fairy E':'Pursuit',
                             'Fairy F':'Pursuit',
                             'Fairy G':'Pursuit',
                             'Wind Weasel A':'Pursuit',
                             'Wind Weasel B':'Pursuit',
                             'Kodama Lord':'Pursuit',
                             'Cursed Tree A':'Pursuit',
                             'Cursed Tree B':'Pursuit',
                             'Cursed Tree C':'Pursuit',


                            }
        initial_locations = {'Walking Tree A':(13, 6),
                             'Walking Tree B':(7, 8),
                             'Walking Tree C':(26, 8),
                             'Walking Tree D':(28, 10),
                             'Walking Tree E':(4, 11),

                             'Firefly A':(-1, 15),
                             'Firefly B':(-1, 15),
                             'Firefly C':(-1, 15),
                             'Firefly D':(-1, 15),
                             'Firefly E':(-1, 15),


                             'Fairy A':(5, 11),
                             'Fairy B':(8, 8),
                             'Fairy C':(14, 6),

                             'Wind Weasel A':(26, 10),
                             'Wind Weasel B':(29, 12),


                             'Kaguya':(21, 17),
                             'Aya':(-1, -1),
                             'Marisa':(-1, -1),
                             'Youmu':(-1, -1),
                             'Ran':(-1, -1),
                             'Chen':(-1, -1),
                             'Reimu':(-1, -1),
                             'Keine':(-1, -1),
                             'Mokou':(-1, -1),

                             }
        reserve_units = ['Kodama Lord', 'Cursed Tree A', 'Cursed Tree B', 'Cursed Tree C', 'Fairy D', 'Fairy E', 'Fairy F', 'Fairy G',
                         ]
        all_landmarks = [{'name':'Eientei',
                          'id_string':'eientei',
                          'location':(20, 16)
                         },
                         {'name':'Torii',
                          'id_string':'small_torii',
                          'location':(11, 10)
                         },

                         ]

        required_starters = ['Aya', 'Marisa', 'Youmu', 'Keine', 'Ran', 'Chen', 'Reimu', 'Mokou',]
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [LampSwitchOn(), LampSwitchOff(), DeploySecondWave()]
        required_survivors = ['Aya', 'Marisa', 'Youmu', 'Keine', 'Ran', 'Chen', 'Reimu', 'Mokou', 'Eirin', 'Reisen']
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

        self.map.add_light_source(LightSource('North Lantern', (9,11), False, 5))
        self.map.add_ssp(SpiritSourcePoint('North SSP', (11, 11), 2))

        self.map.add_light_source(LightSource('Eientei 1', (19,17), True, 3))
        self.map.add_light_source(LightSource('Eientei 2', (23,17), True, 3))



        self.play_music('event03')

        # Adds Eientei Crew
        self.add_to_party('Eirin')
        self.add_to_party('Reisen')


        self.assign_spell('Reisen', 'Dagger Throw')
        self.assign_spell('Reisen', 'Invisible Full Moon')
        self.assign_spell('Eirin', 'Healing Drop')
        self.assign_spell('Eirin', 'Medicinal Drop')
        self.assign_spell('Eirin', 'Astral Entombing')
        self.set_unit_pos('Eirin', (21, 19))
        self.set_unit_pos('Reisen', (13, 15))

        self.center_on('Eirin')
        self.say("Stay inside where you're safe, Princess. Reisen and I will handle this.",
                 'Eirin',
                 'Eirin')
        self.say("Are you certain it was wise to have sent the other rabbits away? Would they not have helped as well?",
                 'Kaguya',
                 'Kaguya')
        self.say("The rabbits may be good pranksters, but they're no warriors. Don't worry about them though. Tewi will lead them into the bamboo forest where they can hide.",
                 'Eirin',
                 'Eirin')
        self.say("(I miss them already though. My precious test subjects...)",
                 'Eirin',
                 'Eirin')
        self.move_unit('Kaguya', (21,16))
        self.kill_unit('Kaguya')
        self.move_unit('Eirin', (21,17))
        self.center_on('Eirin')
        self.say("Udonge, your hearing's sharp. What do you sense out there?",
                 'Eirin',
                 'Eirin')
        self.center_on('Reisen')
        self.say("I hear two groups approaching Eientei, Madam Eirin. One big group in the northwest and a smaller one from the northeast.",
                 'Reisen',
                 'Reisen')
        self.move_unit('Reisen', (13, 13))
        self.say("I'll split the fog open with this moonstone arrow. Try and get your long range shot through when I do.",
                 'Eirin',
                 'Eirin')
        self.map.engine.trait_actions_catalog['Moonstone Arrow'].execute_action(self.map.all_units_by_name['Eirin'], Vector2(11, 8))
        self.say("All right, Udonge. Ready? We're following our plan to the T. Hug the edge of the fog and shoot any enemies I expose.",
                 'Eirin',
                 'Eirin')

        self.center_on("Walking Tree A")
        self.emote('Walking Tree A', 'scribble')
        self.say("Huh? What happened to the fog?",
                 'Fairy',
                 'Fairy')

        self.center_on('Reisen')
        self.emote('Reisen', 'exclamation')
        self.say("I hear something. Someone's coming.",
                 'Reisen',
                 'Reisen')
        self.center_on_coords((5, 15))

        self.say("Didn't you say it was just past the brook?",
                 'Marisa',
                 'Marisa')
        self.set_unit_pos('Mokou', (-1,15))
        self.set_unit_pos('Marisa', (-1,15))
        self.set_unit_pos('Youmu', (-1,15))
        self.set_unit_pos('Aya', (-1,15))

        self.move_unit('Youmu', (2, 15))
        self.move_unit('Mokou', (1,15))
        self.move_unit('Marisa', (1, 14))
        self.move_unit('Aya', (1, 16))

        self.say("I've walked this route a million times. Without fog.",
                 'Mokou',
                 'Mokou')

        self.move_unit('Firefly A', (8, 15))
        self.move_unit('Firefly B', (7, 14))
        self.move_unit('Firefly C', (7, 16))
        self.move_unit('Firefly D', (6, 13))
        self.move_unit('Firefly E', (6, 17))

        self.say("Uh-huh. Well, those fireflies there seem to be going where they need to be, and fast.",
                 'Marisa',
                 'Marisa')
        self.say("Let's have faith in Mokou then. We must be heading in the right direction.",
                 'Youmu',
                 'Youmu')

        self.center_on('Reisen')


        self.move_unit('Firefly A', (15, 13))
        self.move_unit('Firefly B', (14, 14))
        self.move_unit('Firefly C', (13, 15))
        self.move_unit('Firefly D', (12, 14))
        self.move_unit('Firefly E', (11, 13))

        self.startle('Reisen')
        self.emote('Youmu', 'exclamation')


        self.say("After them!",
                 'Youmu',
                 'Youmu')

        self.move_unit('Marisa', (11, 14))
        self.move_unit('Mokou', (12, 15))
        self.move_unit('Youmu', (13, 16))
        self.move_unit('Aya', (11, 16))

        self.center_on('Youmu')
        self.emote('Reisen', 'questionmark')


        self.move_unit('Firefly A', (15, -1))
        self.move_unit('Firefly B', (14, -1))
        self.move_unit('Firefly C', (13, -1))
        self.move_unit('Firefly D', (12, -1))
        self.move_unit('Firefly E', (11, -1))

        self.set_unit_pos('Firefly A', (1, 5))
        self.set_unit_pos('Firefly B', (4, 6))
        self.set_unit_pos('Firefly C', (6, 4))
        self.set_unit_pos('Firefly D', (9, 5))
        self.set_unit_pos('Firefly E', (13, 3))

        self.say("Reisen! Eientei must be pretty close if she's hear.",
                 'Aya',
                 'Aya')
        self.say("What do you want? Can't you see we're fighting a battle here?",
                 'Reisen',
                 'Reisen')
        self.say("I can tell you we're not with the Kodama. Let us first help you fend off this attack, and then we'll explain ourselves.",
                 'Youmu',
                 'Youmu')
        self.say("It's not just us either. Everyone else should be here soon, and together we'll make this battle a lot easier. Promise.",
                 'Marisa',
                 'Marisa')
        self.fade_to_color('black', 1)


        self.set_unit_pos('Reimu', (12, 15))
        self.set_unit_pos('Youmu', (13, 15))
        self.set_unit_pos('Marisa', (14, 15))
        self.set_unit_pos('Ran', (11, 16))
        self.set_unit_pos('Chen', (12, 16))
        self.set_unit_pos('Aya', (13, 16))
        self.set_unit_pos('Keine', (14, 16))
        self.set_unit_pos('Mokou', (14, 17))
        self.set_unit_pos('Eirin', (12, 13))

        self.fade_from_color('black', 1)

        self.say("Oh, brother. Mokou is with them.",
                 'Reisen',
                 'Reisen')
        self.say("Well, we're about to be attacked by the Kodama, so Mokou or not, help sounds good to me.",
                 'Eirin',
                 'Eirin')
        self.say("We'll accept your offer for now, but afterwards, I'll make sure you're...treated properly depending on your reasons. How's that?",
                 'Eirin',
                 'Eirin')
        self.emote('Ran', 'musicnote')
        self.say("Your magic is pretty impressive for being able to clear this fog like that. None of our spells could manage that!",
                 'Ran',
                 'Ran')
        self.say("Why, thank you. Some lunar secrets are beyond the wisdom of these old tree folks. Unfortunately, there's a drawback.",
                 'Eirin',
                 'Eirin')
        self.center_on('Walking Tree A')

        self.pause(0.25)
        self.map.remove_temporary_light_sources()
        self.pause(0.25)
        self.emote('Walking Tree A', 'musicnote')

        self.center_on('Eirin')

        self.say("Against Ayaka's fog spell, it'll only keep it clear for a short time. And that's why I have plenty of moonstone arrows on hand.",
                 'Eirin',
                 'Eirin')

        self.center_on_coords((21, 17))


        self.say("All right, I think we've chatted enough. We can't let any of their units reach Eientei!",
                 'Reisen',
                 'Reisen')
        
        self.say("They have two groups trying to enter Eientei at the moment. Let's split up to deal with the groups in the east and west at the same time.",
                 'Keine',
                 'Keine')

        self.say("Understood! That's a simple task for us!",
                 'Youmu',
                 'Youmu')

        self.play_music('battle01')

        self.set_cursor_state(True)
        self.set_stats_display(True)


class LampSwitchOn(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('North SSP', 1)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if not self.map.all_landmarks['North Lantern'].lit:
            self.map.all_landmarks['North Lantern'].switch_state(True)

class LampSwitchOff(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('North SSP', 2)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):
        if self.map.all_landmarks['North Lantern'].lit:
            self.map.all_landmarks['North Lantern'].switch_state(False)

class DeploySecondWave(MapActionEvent):

    def __init__(self):

        triggers = [TurnNumTrigger(5)]
        MapActionEvent.__init__(self, triggers, repeat=False)

    def execute(self):
        self.center_on_coords((18, 34))

        # Deploy Kodama Lord
        self.deploy_unit('Kodama Lord', (18, 34))
        self.move_unit('Kodama Lord', (18, 30))

        self.deploy_unit('Cursed Tree A', (18, 34))
        self.set_status_effect('Cursed Tree A', 'Fog Veil')
        self.move_unit('Cursed Tree A', (16, 32))

        self.deploy_unit('Cursed Tree B', (18, 34))
        self.set_status_effect('Cursed Tree B', 'Fog Veil')
        self.move_unit('Cursed Tree B', (20, 32))

        self.deploy_unit('Cursed Tree C', (18, 34))
        self.set_status_effect('Cursed Tree C', 'Fog Veil')
        self.move_unit('Cursed Tree C', (18, 32))

        self.deploy_unit('Fairy D', (18, 34))
        self.move_unit('Fairy D', (17, 28))
        self.deploy_unit('Fairy E', (18, 34))
        self.move_unit('Fairy E', (19, 28))
        self.deploy_unit('Fairy F', (18, 34))
        self.move_unit('Fairy F', (17, 33))
        self.deploy_unit('Fairy G', (18, 34))
        self.move_unit('Fairy G', (19, 33))


        self.center_on_coords((18, 30))

        self.say('All right! We have a clear path to Eientei. All troops, go forth!',
                 'Kodama Lord',
                 'Kodama'

                 )

        self.center_on_coords((21, 17))


class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.remove_all_enemies()
        self.set_unit_pos('Eirin', (21,17))
        self.set_unit_pos('Reisen', (22,17))

        self.set_unit_pos('Reimu', (20, 19))
        self.set_unit_pos('Youmu', (21, 19))
        self.set_unit_pos('Marisa', (22, 19))
        self.set_unit_pos('Ran', (19, 19))
        self.set_unit_pos('Chen', (20, 20))
        self.set_unit_pos('Aya', (21, 20))
        self.set_unit_pos('Keine', (22, 20))
        self.set_unit_pos('Mokou', (23, 20))

    def execute(self):

        self.center_on('Youmu')

        self.say("That was just a minor Kodama Lord leading them, but they were still incredibly strong! Thank goodness it's over.",
                 'Youmu',
                 'Youmu')

        self.say("We should expect no less from Ayaka's troops. There will still be more to come.",
                 'Ran',
                 'Ran')

        self.say("With that out of the way, let's talk business. What are your reasons for heading to Eientei?",
                 'Eirin',
                 'Eirin')