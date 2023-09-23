from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, TurnNumTrigger, UnitAliveTrigger
from lostsky.battle.mapobj import SpiritSourcePoint

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        """

        """
        name = 'The Tengu Trial'
        location = 'Nine Heavens Waterfall'
        id_string = 'CH3ST3'
        prereqs = ['CH3ST2']
        show_rewards = True
        desc = "In a shocking turn of events, Lord Tenma has presented a challenge to Youmu and her friends to undergo the Trial of the Red Feathers. \"It\'s just for show. Youmu doesn't stand a chance. We'll never let outsiders set foot in our sacred sanctuary,\" Momiji said as her Wolf Tengu carefully prepared for this momentous event."

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        ssp_list = [SpiritSourcePoint('Nitori 1', (1, 30), 0),
                    SpiritSourcePoint('Nitori 2', (26, 30), 0),
                    SpiritSourcePoint('Aya 1', (2, 24), 0),
                    SpiritSourcePoint('Aya 2', (6, 18), 0),
                    SpiritSourcePoint('Momiji 1', (27, 21), 0),
                    SpiritSourcePoint('Momiji 2', (18, 14), 0)
                    ]

        # Map Data
        map_name = 'ch3st3.txt'
        mission_type = 'battle'
        objective = {'type':'Capture Spirit Sources',
                     'ssps': ssp_list,
                     'number': 6,
                     'desc':'Capture all Spirit Source Points!'
                     }

        deploy_data = {'enable':True,
                       'max_units':9,
                       'preset_units':{},
                       'boxes':[(12, 24, 3, 3)],
                       'default_locations':{'Youmu':(13,24),
                                            'Ran':(13,26),   
                                            'Chen':(14,26),
                                            'Reimu':(12,25),
                                            'Keine':(14,25),
                                            'Marisa':(12,26),
                                            'Mokou':(14,24),
                                            'Alice':(12,24),
                                            },
                       }
        reward_list = [('treasure', 'tengu_feather')
                   ]

        # Enemy Unit Data
        enemy_unit_data = [  {'template_name': 'Momiji',
                                'unit_name': 'Momiji',
                                    'level': 11},
                            {'template_name': 'Wolf Tengu',
                                'unit_name': 'Wolf Tengu A',
                                'level': 10},
                            {'template_name': 'Wolf Tengu',
                                'unit_name': 'Wolf Tengu B',
                                'level': 10},
                            {'template_name': 'Wolf Tengu',
                                'unit_name': 'Wolf Tengu C',
                                'level': 10},
                            {'template_name': 'Wolf Tengu',
                                'unit_name': 'Wolf Tengu D',
                                'level': 10},
                            {'template_name': 'Wolf Tengu',
                             'unit_name': 'Wolf Tengu E',
                             'level': 10},


                             {'template_name': 'Nitori',
                                    'unit_name': 'Nitori',
                                        'level': 11},

                            {'template_name': 'Kappa',
                                'unit_name': 'Kappa A',
                                'level': 10},
                            {'template_name': 'Kappa',
                                'unit_name': 'Kappa B',
                                'level': 10},
                            {'template_name': 'Kappa',
                                'unit_name': 'Kappa C',
                                'level': 10},
                            {'template_name': 'Kappa',
                                'unit_name': 'Kappa D',
                                'level': 10},

                            {'template_name': 'Aya',
                                'unit_name': 'Aya',
                                'level': 11},
                            {'template_name': 'Crow Tengu',
                                'unit_name': 'Reporter A',
                                'level': 11},
                            {'template_name': 'Crow Tengu',
                                'unit_name': 'Reporter B',
                                'level': 11},
                            {'template_name': 'Crow Tengu',
                                'unit_name': 'Reporter C',
                                'level': 11},


                             {'template_name': 'Tsubaki',
                                    'unit_name': 'Tsubaki',
                                        'level': 15},
                            {'template_name': 'Crow Tengu',
                                'unit_name': 'Red Feather A',
                                'level': 13},
                            {'template_name': 'Crow Tengu',
                                'unit_name': 'Red Feather B',
                                'level': 13},
                            {'template_name': 'Crow Tengu',
                                'unit_name': 'Red Feather C',
                                'level': 13},
                            {'template_name': 'Crow Tengu',
                                'unit_name': 'Red Feather D',
                                'level': 13},
                            {'template_name': 'Crow Tengu',
                                'unit_name': 'Red Feather E',
                                'level': 13},
#
#

                            ]

        initial_spells = {'Momiji':['Dagger Throw'],
                          'Wolf Tengu A':['Dagger Throw'],
                          'Wolf Tengu B':['Dagger Throw'],
                          'Wolf Tengu C':['Dagger Throw'],
                          'Wolf Tengu D':['Dagger Throw'],

                          'Nitori':['Tanabata Festival'],
                          'Kappa A':['Illusion Veil', 'Fireball'],
                          'Kappa B':['Tanabata Festival'],
                          'Kappa C':['Fireball'],
                          'Kappa D':['Tanabata Festival'],

                          'Aya':['Holy Amulet'],
                          'Reporter A':['Shimmering Stars'],
                          'Reporter B':['Feather Pin'],
                          'Reporter C':['Spirit Break'],

                          'Tsubaki':['Red Feather Gale'],
                          'Red Feather A':['Spirit Break'],
                          'Red Feather B':['Fireball'],
                          'Red Feather C':['Spirit Break'],
                          'Red Feather D':['Fireball'],
                          'Red Feather E':['Spirit Break'],

                            }
        initial_traits = {'Aya':['Flight', 'Mirage'],
                          'Reporter A':['Flight'],
                          'Reporter B':['Flight'],
                          'Reporter C':['Flight'],
                          'Nitori':['Danmaku Sniper', 'Swimming'],
                          'Kappa A':['Swimming'],
                          'Kappa B':['Swimming'],
                          'Kappa C':['Swimming'],
                          'Kappa D':['Swimming'],
                          'Tsubaki':['Flight'],
                          'Red Feather A':['Flight'],
                          'Red Feather B':['Flight'],
                          'Red Feather C':['Flight'],
                          'Red Feather D':['Flight'],
                          'Red Feather E':['Flight'],


                          }
        initial_ai_states = {'Momiji':'Defend',
                             'Wolf Tengu A':'Defend',
                             'Wolf Tengu B':'Defend',
                             'Wolf Tengu C':'Defend',
                             'Wolf Tengu D':'Defend',

                             'Nitori':'Defend',
                             'Kappa A':'Support',
                             'Kappa B':'Attack',
                             'Kappa C':'Attack',
                             'Kappa D':'Attack',

                             'Aya':'Pursuit',
                             'Reporter A':'Pursuit',
                             'Reporter B':'Pursuit',
                             'Reporter C':'Pursuit',


                             'Tsubaki':'Defend',
                             'Red Feather A':'Defend',
                             'Red Feather B':'Defend',
                             'Red Feather C':'Defend',
                             'Red Feather D':'Defend',
                             'Red Feather E':'Defend',


                            }
        initial_locations = {

                             'Youmu': (13, 22),
                             'Marisa': (11, 23),
                             'Reimu': (11, 24),
                             'Ran': (15, 23),
                             'Chen': (15, 24),
                             'Keine': (12, 25),
                             'Mokou': (14, 25),


                             'Momiji': (19, 15),
                             'Wolf Tengu A': (20, 14),
                             'Wolf Tengu B': (18, 16),
                             'Wolf Tengu C': (26, 21),
                             'Wolf Tengu D': (28, 21),

                             'Nitori':(26, 30),

                             'Kappa A': (4, 28),
                             'Kappa B': (6, 33),
                             'Kappa C': (22, 27),
                             'Kappa D': (20, 30),

                             'Aya': (13, 19),
                             'Reporter A': (8, 18),
                             'Reporter B': (7, 20),
                             'Reporter C': (5, 22),

                             'Tsubaki': (25, 4),
                             'Red Feather A':(2, 6),
                             'Red Feather B':(9, 3),
                             'Red Feather C':(19, 4),
                             'Red Feather D':(24, 8),
                             'Red Feather E':(32, 10),
                             }
        reserve_units = ['Wolf Tengu E']
        all_landmarks = [{'name':'Tengu Shrine 1',
                          'id_string':'minishrine',
                          'location':(18, 13)
                          },
                        {'name':'Tengu Shrine 2',
                          'id_string':'minishrine',
                          'location':(27, 20)
                          },
                        {'name':'Tengu Shrine 3',
                          'id_string':'minishrine',
                          'location':(6, 17)
                          },
                        {'name':'Tengu Shrine 4',
                          'id_string':'minishrine',
                          'location':(2, 23)
                          },
                        {'name':'Tengu Shrine 5',
                          'id_string':'minishrine',
                          'location':(1, 29)
                          },
                        {'name':'Tengu Shrine 6',
                          'id_string':'minishrine',
                          'location':(26, 29)
                          },
                        {'name':'Tengu Outpost',
                          'id_string':'shrine',
                          'location':(25, 3)
                          },
                        {'name':'Tengu House 1',
                          'id_string':'house_2',
                          'location':(26, 3)
                          },
                        {'name':'Tengu House 2',
                          'id_string':'house_2',
                          'location':(24, 3)
                          },


        ]

        required_starters = ['Youmu', 'Marisa', 'Reimu', 'Chen', 'Ran', 'Keine', 'Mokou']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [ActivateRedFeathers()]
        required_survivors = ['Aya', 'Tsubaki', 'Momiji', 'Youmu', 'Marisa', 'Reimu', 'Chen', 'Ran', 'Keine', 'Mokou', 'Nitori']
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

        self.center_on('Aya')
        self.say('Welcome to the Trial of the Red Feathers!',
                 'Aya',
                 'Aya')

        # Aya flies around taking photos
        self.startle('Aya')
        self.play_sfx('camera')
        self.fade_to_color('white', 0.2)
        self.fade_from_color('white', 0.2)


        self.say('Lady Tsubaki will explain the rules. So take it away!',
                 'Aya',
                 'Aya')

        self.center_on('Tsubaki')

        self.say('We stand at the top of the Waterfall of Nine Heavens. Seek out the six shrines scattered across the region and claim their spiritual energy as your own.',
                 'Tsubaki',
                 'Tsubaki')

        self.center_on('Aya')

        self.say('Oh. That sounds fairly simple, actually.',
                 'Youmu',
                 'Youmu')
        self.say("Don't be silly, we're going to try to stop you, of course, and some of them are going to be super difficult to reach. No being lazy, ok? Lady Tsubaki, we can deactivate the shrines too, right?",
                 'Aya',
                 'Aya')
        self.say("Yes.",
                 'Tsubaki',
                 'Tsubaki')
        self.say('The Kappa and I are ready! Your Reporter friends better be up to the task, Aya!',
                 'Momiji',
                 'Momiji')
        self.say("Ooh, Kappa, too? Oh, boy, I can't wait! This will be so much fun!",
                 'Aya',
                 'Aya')

        # One last photo
        self.move_unit('Aya', (18, 15))
        self.startle('Aya')
        self.play_sfx('camera')
        self.fade_to_color('white', 0.2)
        self.fade_from_color('white', 0.2)

        # Tsubaki gets annoyed
        self.center_on('Tsubaki')
        self.emote('Tsubaki', 'scribble')
        self.say("This is a serious trial, Miss Shameimaru. Mind you do more than snap those pictures of yours.",
                 'Tsubaki',
                 'Tsubaki')

        # All enemy units report their readiness
        self.center_on('Aya')
        self.move_unit('Aya', (6, 20))
        self.center_on('Aya')
        self.say("Yeah, yeah, I know, I know. That aside. Ready, everyone?",
                  'Aya',
                  'Aya')
        self.center_on('Reporter A')
        self.say("We're ready and raring to go!",
                  'Reporter A',
                  'Crow Tengu')

        self.center_on('Nitori')
        self.say("Me, too! Me, too! I'll blow 'em to smithereens!",
                  'Nitori',
                  'Nitori')

        self.center_on('Momiji')
        self.say("Wolf Tengu, we'll show those crows that we're the best warriors on this mountain! So give it your all!",
                  'Momiji',
                  'Momiji')

        self.center_on('Youmu')
        self.say("We'll give it our best, too!",
                  'Youmu',
                  'Youmu')

        self.set_cursor_state(True)
        self.set_stats_display(True)


class ActivateRedFeathers(MapActionEvent):

    def __init__(self):
        triggers = [TurnNumTrigger(10),
                    UnitAliveTrigger('Tsubaki', True)]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        # Higher level Tengu change AI state into pursuit mode
        self.center_on('Tsubaki')
        self.say('How about you give it a shot, Red Feathers?', 'Tsubaki', 'Tsubaki')

        switch_list = ['Red Feather A', 'Red Feather B', 'Red Feather C', 'Red Feather D',
                       'Red Feather E']
        for unit in self.map.team2:
            if unit.name in switch_list:
                self.set_ai_state(unit.name, "Pursuit")

class PostMissionMAE(MapActionEvent):
    def __init__(self):
        # Triggers on turn 2
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):
        self.remove_all_enemies()

        # Move the party, Tsubaki, Aya, Momiji, and Nitori together
        self.set_unit_pos('Tsubaki', (13, 27))
        self.set_unit_pos('Aya', (12, 28))
        self.set_unit_pos('Nitori', (13, 28))
        self.set_unit_pos('Momiji', (14, 28))
        self.set_unit_pos('Youmu', (13, 24))
        self.set_unit_pos('Marisa', (11, 23))
        self.set_unit_pos('Reimu', (11, 24))
        self.set_unit_pos('Ran', (15, 23))
        self.set_unit_pos('Chen', (15, 24))
        self.set_unit_pos('Keine', (12, 25))
        self.set_unit_pos('Mokou', (14, 25))

    def execute(self):

        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.stop_music()
        self.center_on('Youmu')

        self.say("You've done it. Congratulations, Youmu.",
            'Tsubaki',
            "Tsubaki")

        # Aya takes a picture
        self.startle('Aya')
        self.play_sfx('camera')
        self.fade_to_color('white', 0.2)
        self.fade_from_color('white', 0.2)

        self.say("Sheesh, that was tough. Maybe even the toughest. Oof, I'm going to feel this tomorrow.",
            'Marisa',
            "Marisa")

        self.say("Youmu, step forward.",
            'Tsubaki',
            "Tsubaki")

        # Youmu moves closer to Tsubaki
        self.move_unit('Youmu', (13, 25))
        self.move_unit('Tsubaki', (13, 26))

        self.say('From this day forward, we acknowledge you as a member of the Order of the Red Feathers.',
            'Tsubaki',
            "Tsubaki")
        self.say("Formalities aside, we can actually go to the summit without getting beat up for it now, right?",
            'Reimu',
            'Reimu')
        self.say("Yes, just as we had agreed. Aya, escort them to the top of the mountain.",
            'Tsubaki',
            "Tsubaki")
        self.say("Youmu, this red feather amulet will act as your permit.",
            'Tsubaki',
            "Tsubaki")
        self.say("Heck, yeah! Just what I wanted to hear! This journalist is going right into the middle of the action, and my pen ain't gonna stop!",
            'Aya',
            "Aya")

        self.deploy_unit('Wolf Tengu E', (25, 23))
        self.move_unit('Wolf Tengu E', (20, 23))
        self.say("Momiji! Momiji!",
            'Wolf Tengu',
            "Wolf Tengu")
        self.startle('Momiji')
        self.move_unit('Momiji', (14, 26) )
        self.move_unit('Momiji', (15, 26) )
        self.move_unit('Momiji', (15, 25) )
        self.move_unit('Momiji', (16, 24) )
        self.move_unit('Momiji', (16, 23) )
        self.move_unit('Momiji', (18, 23) )

        self.startle('Momiji')
        self.say("What is it? What happened?",
            'Momiji',
            'Momiji')

        self.say("The outpost on the mountain path is under attack by a Kodama Lord! We need your help! Please!",
            'Wolf Tengu',
            "Wolf Tengu")

        self.emote('Momiji', 'exclamation')
        self.say("Lady Tsubaki, I have to go.",
            'Momiji',
            'Momiji')
        self.move_unit('Wolf Tengu E', (26, 23))
        self.move_unit('Momiji', (26, 23))

        self.say("Momiji? Momiji, wait!",
            'Youmu',
            'Youmu')

        self.set_cursor_state(False)
        self.set_stats_display(False)
