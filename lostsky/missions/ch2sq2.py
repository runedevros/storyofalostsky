from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, TurnNumTrigger, UnitAliveTrigger

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'To the Aid of Alice'
        location = "Alice's House"
        id_string = 'CH2SQ2'
        prereqs = ['CH2SQ1']
        show_rewards = False
        desc = "The Kodama Lord Kotone marches towards Alice's house in the Forest of Magic. Oh, no! Will our heroes be able to stop her in time?"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch2sq2.txt'
        mission_type = 'battle'
        objective = {'type':'Defend and Defeat Boss',
                     'target':'Kotone',
                     'location_box': [21, 13, 3, 2],
                     'location_name': 'Alice\'s House',
                     'desc':'Defeat Kotone and keep enemies from the area near Alice\'s house.'
                     }

        deploy_data = {'enable':True,
                       'max_units':9,
                       'preset_units':{'Alice':(22, 13),
                                       'Marisa':(22, 14)},
                       'boxes':[(17, 15, 3, 3), (25, 15, 3, 3)],
                       'default_locations':{'Youmu':(26, 16),
                                            'Chen':(25, 16),
                                            'Ran':(26, 15),
                                            'Reimu':(18, 16),
                                            'Keine':(19, 16),
                                            'Mokou':(18, 15),
                                            'Aya':(19, 15),
                       }

                       }
        reward_list = [('spell_action', 'Feather Pin'),
                       ('treasure', '007_spellbook')
                      ]

        # Enemy Unit Data
        enemy_unit_data = [

                            # Initial enemy group
                            {'template_name': 'Kotone',
                                'unit_name': 'Kotone',
                                    'level': 9
                                },
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 6
                                },

                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 6
                                },

                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 6
                                },

                            # Three Dolls for the intro scene
                            {'template_name': 'Doll',
                                'unit_name': 'Doll A',
                                    'level': 6
                            },
                            {'template_name': 'Doll',
                                'unit_name': 'Doll B',
                                    'level': 6
                            },
                            {'template_name': 'Doll',
                                'unit_name': 'Doll C',
                                    'level': 6
                            },


                            # Squad 1 - Close units approaching from the east
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 5
                            },
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 5
                            },
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 6
                                },

                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy D',
                                    'level': 6
                                },
                            {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy A',
                                    'level': 6
                                },

                            # Squad 2 - Close units approaching from the west.
                            {'template_name': 'Fairy',
                                'unit_name': 'Sealing Fairy',
                                    'level': 6
                                },
                            {'template_name': 'Fairy',
                                'unit_name': 'Dazzling Fairy',
                                    'level': 6
                                },
                            {'template_name': 'Fairy',
                                'unit_name': 'Ninja Fairy',
                                    'level': 6
                                },
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy Captain',
                                    'level': 8
                                },

                            # Squad 3 - Firefly unit from the northwest

                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly A',
                                    'level': 7
                                },
                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly B',
                                    'level': 7
                                },
                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly C',
                                    'level': 7
                                },
                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly D',
                                    'level': 7
                                },

                            # Kotone's Squad

                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree D',
                                    'level': 7
                            },
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree E',
                                    'level': 7
                            },
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree F',
                                    'level': 7
                            },
                            {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy B',
                                    'level': 6
                                },

                            ]

        initial_spells = {'Fairy A':['Fireball'],
                          'Fairy B':['Fireball'],
                          'Fairy C':['Holy Amulet'],
                          'Fairy D':['Holy Amulet'],
                          'Dazzling Fairy':['Shimmering Stars'],
                          'Sealing Fairy':['Spirit Break'],
                          'Ninja Fairy':['Feather Pin'],
                          'Fairy Captain':['Holy Amulet'],

                          'Walking Tree A':['Leaf Crystal'],
                          'Walking Tree B':['Leaf Crystal'],
                          'Walking Tree C':['Leaf Crystal'],
                          'Walking Tree D':['Leaf Crystal'],
                          'Walking Tree E':['Leaf Crystal'],
                          'Walking Tree F':['Leaf Crystal'],
                          'Healer Fairy A':['Healing Drop'],
                          'Healer Fairy B':['Healing Drop'],

                          'Kotone':['Fireball'],

                          'Firefly A':['Poison Dust'],
                          'Firefly B':['Poison Dust'],
                          'Firefly C':['Poison Dust'],
                          'Firefly D':['Poison Dust'],


                            }
        initial_traits = {'Healer Fairy A':['Move+ Lv.1', 'Flight'],
                          'Healer Fairy B':['Move+ Lv.1', 'Flight'],
                          'Firefly A':['Flight'],
                          'Firefly B':['Flight'],
                          'Firefly C':['Flight'],
                          'Firefly D':['Flight'], }
        initial_ai_states = {'Kotone':'Attack',
                             'Fairy A':'Attack',
                             'Fairy B':'Attack',
                             'Fairy C':'Attack',
                             'Fairy D':'Attack',
                             'Walking Tree A':'Attack',
                             'Walking Tree B':'Attack',
                             'Walking Tree C':'Attack',
                             'Walking Tree D':'Attack',
                             'Walking Tree E':'Attack',
                             'Walking Tree F':'Attack',

                             'Ninja Fairy': 'Pursuit',
                             'Sealing Fairy': 'Pursuit',
                             'Dazzling Fairy': 'Pursuit',
                             'Fairy Captain': 'Pursuit',

                             'Firefly A': 'Pursuit',
                             'Firefly B': 'Pursuit',
                             'Firefly C': 'Pursuit',
                             'Firefly D': 'Pursuit',

                             'Healer Fairy A': 'HealerStandby',
                             'Healer Fairy B': 'HealerStandby'



                            }
        initial_locations = {'Fairy A':(21, 16),
                             'Fairy B':(23, 16),
                             'Walking Tree A':(22, 16),
                             'Kotone':(22, 15),

                             'Youmu': (13, 27),
                             'Marisa': (15, 25),
                             'Ran': (12, 28),
                             'Chen': (13, 28),
                             'Reimu': (14, 27),
                             'Keine': (14, 28),

                             }
        reserve_units = ['Doll A', 'Doll B', 'Doll C',
                         'Fairy C',
                         'Fairy D',
                         'Walking Tree B',
                         'Walking Tree C',
                         'Healer Fairy A',

                         'Fairy Captain',
                         'Sealing Fairy',
                         'Ninja Fairy',
                         'Dazzling Fairy',

                         'Walking Tree D',
                         'Walking Tree E',
                         'Walking Tree F',
                         'Healer Fairy B',

                         'Firefly A',
                         'Firefly B',
                         'Firefly C',
                         'Firefly D',


                         ]#[list of unit names to deploy later in mission]
        all_landmarks = [{'name':'Alice\'s House',
                          'id_string':'house_2',
                          'location':(22, 13)},
                         ]

        required_starters = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Reimu', 'Keine']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [SummonFireflies(), KotonePursuit()]
        required_survivors = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Reimu', 'Keine', 'Kotone', 'Alice']
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

        # Kotone proposes an alliance with Alice

        self.center_on('Kotone')

        self.move_unit('Kotone', (22, 14))
        self.say("...and as a representative of Fuyuhana Touji, Kodama Lord of the Forest of Magic, I humbly ask you to join our cause.",
                'Kotone',
                'Kotone')
        self.emote('Kotone', 'dotdotdot')
        self.say("Um. Hey. We did check that someone's actually home, right?",
                'Fairy A',
                'Fairy')
        self.say("Uh. Well--a-aha! Something moved in that window over there! Someone's definitely home. I know you're in there, Alice! Would you please just come out and give us a reply already?",
                'Kotone',
                'Kotone')
        self.emote('Kotone', 'scribble')
        self.say("You can't run away! There's no way out! We have your house surrounded!",
                'Kotone',
                'Kotone')
        self.say("Tch, fine. Guess we'll have to show her we mean business. Walking Tree! Break in through that window!",
                'Kotone',
                'Kotone')

        self.play_music('battle01')

        # Marisa charges into battle

        self.center_on('Marisa')
        self.say("Yes! Looks like we got here in time!",
                'Marisa',
                'Marisa')
        self.move_unit('Marisa', (19, 18))
        self.center_on('Marisa')
        self.say("Wait! Marisa!",
                'Ran',
                'Ran')
        self.move_unit('Marisa', (19, 14))
        self.startle('Marisa')
        self.play_sfx('miss')
        self.move_unit('Marisa', (22, 14))
        self.play_sfx('crit')

        # Marisa knocks Kotone aside
        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)
        self.move_unit('Kotone', (26, 14))

        self.emote('Kotone', 'annoyed')
        self.say("What?! No! Not you guys again!",
                'Kotone',
                'Kotone')

        self.say("Thought you could go around and bully my friend and get away with it, could you?! Well think again!",
                'Marisa',
                'Marisa')
        self.emote('Marisa', 'questionmark')
        self.say("Uh... Say do you guys hear something?",
                'Marisa',
                'Marisa')

        # Three dolls deploy around Marisa
        self.say("Something's ticking. A clock perhaps.",
                'Fairy A',
                'Fairy')
        self.emote('Marisa', 'exclamation')
        self.deploy_unit('Doll A', (22, 13))
        self.move_unit('Doll A', (21, 14))
        self.deploy_unit('Doll B', (22, 13))
        self.move_unit('Doll B', (23, 14))
        self.deploy_unit('Doll C', (22, 13))


        self.center_on('Doll A')
        self.say("3...",
                'Doll A',
                'Doll')

        self.say("Oh no. Oh no. Oh nononononono--this is really, really bad!",
                'Marisa',
                'Marisa')


        self.center_on('Doll B')
        self.say("2...",
                'Doll B',
                'Doll')


        self.center_on('Doll C')
        self.say("1...",
                'Doll C',
                'Doll')

        # Alice makes her appearance
        self.add_to_party('Alice')
        self.assign_spell('Alice', 'Fireball')
        self.assign_spell('Alice', 'Artful Sacrifice')
        self.set_unit_pos('Alice', (23, 23))

        self.center_on('Alice')

        self.say("Marisa, you idiot!",
                'Alice',
                'Alice')

        self.center_on('Marisa')

        # Dolls explode, taking themselves and a few nearby units out. Marisa is thrown aside.
        self.play_sfx('explode')
        self.fade_to_color('white', 1.5)
        self.set_hp('Marisa', 1)
        self.kill_unit('Doll A')
        self.kill_unit('Doll B')
        self.kill_unit('Doll C')

        self.kill_unit('Fairy A')
        self.kill_unit('Fairy B')
        self.kill_unit('Walking Tree A')

        self.fade_from_color('white', 0.5)
        self.move_unit('Marisa', (22, 21))

        self.center_on('Marisa')

        self.emote('Marisa', 'scribble')
        self.move_unit('Alice', (21, 22))
        self.emote('Marisa', 'scribble')
        self.startle('Alice')

        # Alice drags Marisa towards the rest of the party
        self.move_unit('Alice', (21, 23))
        self.move_unit('Marisa', (21, 22))

        self.move_unit('Alice', (20, 23))
        self.move_unit('Marisa', (21, 23))

        self.emote('Marisa', 'scribble')
        self.startle('Alice')

        self.move_unit('Alice', (19, 23))
        self.move_unit('Marisa', (20, 23))


        self.startle('Alice')
        self.say("Ah...ugh... Help! We're over here!",
                'Alice',
                'Alice')

        self.center_on('Keine')

        self.emote('Keine', 'exclamation')
        self.say("Youmu, let's go. I heard someone call for help that way!",
                'Keine',
                'Keine')

        # Player party regroups
        self.move_unit('Keine', (20, 24))

        self.move_unit('Youmu', (20, 26))
        self.move_unit('Ran', (19, 26))
        self.move_unit('Chen', (21, 26))
        self.move_unit('Reimu', (20, 27))

        self.center_on('Keine')

        self.startle('Marisa')
        self.say("Marisa! Marisa, are you okay?!",
                'Youmu',
                'Youmu')
        self.say("Owowowowowowowowow! Ow! Quit it!",
                'Marisa',
                'Marisa')
        self.say("Hold still, Marisa! You were thrown a long distance by that blast, and rather violently at that, so please let me get to work.",
                'Keine',
                'Keine')
        self.set_hp('Marisa', 10)
        self.emote('Marisa', 'scribble')
        self.say("There. That should get you back on your feet.",
                'Keine',
                'Keine')
        self.say("How like you to charge in so recklessly. I had those exploding dolls set up as a trap for that Kodama Lord, not for you! Idiot!",
                'Alice',
                'Alice')
        self.emote('Marisa', 'annoyed')
        self.say("Hey, don't blame me! We came to help you! I thought you were in trouble!",
                'Marisa',
                'Marisa')
        self.say("And why would I need your help? Don't you dare look down on me. I could have taken Kotone on my own, easily.",
                'Alice',
                'Alice')
        self.say("See? I told you Alice could fend for herself.",
                'Reimu',
                'Reimu')
        self.say("Heehee! Come on, let's all just be friends and fight together! And...y'know, not with each other.",
                'Chen',
                'Chen')


        self.say("Why are all of you here anyway? It's unusual to see all of you gathered in one place",
                'Alice',
                'Alice')
        self.say("Long story, not worth the time. Now will you at least let us help you get on outta here?",
                'Marisa',
                'Marisa')
        self.startle('Alice')
        self.say("No, idiot! We can't leave now! My doll making materials are still inside!",
                'Alice',
                'Alice')

        self.move_unit('Ran', (21, 24))
        self.say("Kotone is pulling her trees back to the forest's edge. Let's take this chance to position ourselves to defend Alice's house while she gathers her things.",
                'Ran',
                'Ran')
        self.say("Agreed!",
                'Youmu',
                'Youmu')

        # Party gathers at Alice's house
        self.fade_to_color('black', 1.0)

        self.set_unit_pos('Alice', (22, 13))
        self.set_unit_pos('Marisa', (21, 13))
        self.set_unit_pos('Youmu', (22, 14))

        self.set_unit_pos('Reimu', (21, 14))
        self.set_unit_pos('Keine', (23, 13))
        self.set_unit_pos('Ran', (23, 14))
        self.set_unit_pos('Chen', (23, 15))

        # Deploy all enemy units

        # Eastern Squad
        self.deploy_unit('Walking Tree B', (28, 18))
        self.deploy_unit('Walking Tree C', (28, 14))
        self.deploy_unit('Fairy C', (30, 14))
        self.deploy_unit('Fairy D', (30, 17))
        self.deploy_unit('Healer Fairy A', (31, 17))

        # Western Squad
        self.deploy_unit('Fairy Captain', (3, 15))
        self.deploy_unit('Ninja Fairy', (3, 12))
        self.deploy_unit('Dazzling Fairy', (3, 17))
        self.deploy_unit('Sealing Fairy', (1, 15))

        # Kotone's Squad
        self.set_unit_pos('Kotone', (33, 2))
        self.deploy_unit('Walking Tree D', (32, 2))
        self.deploy_unit('Walking Tree E', (32, 3))
        self.deploy_unit('Walking Tree F', (33, 3))
        self.deploy_unit('Healer Fairy B', (34, 1))

        self.fade_from_color('black', 1.0)

        self.center_on('Alice')

        self.say("If they so much as walk past my house, I'll kill them all.",
                'Alice',
                'Alice')

        self.center_on('Kotone')
        self.say("Listen up! We have a strategy today. Charge!!!",
                'Kotone',
                'Kotone')

        self.center_on('Fairy Captain')
        self.say("Kotone! Sorry we're late! Most of our group was wiped out by--by them right there!",
                'Fairy Captain',
                'Fairy')

        self.center_on('Marisa')
        self.say("Heh! We smashed your pathetic reinforcements before we got here. Hope you don't mind.",
                'Marisa',
                'Marisa')

        self.center_on('Kotone')
        self.emote('Kotone', 'scribble')
        self.say("Argh! Inexcusable! Unacceptable!!!",
                'Kotone',
                'Kotone')
        self.say("Never mind! Press onward with the attack! There is no change in strategy!",
                'Kotone',
                'Kotone')
        self.say("We are the guardians of this forest! Regardless of the odds, we will never back down! So charge!",
                'Kotone',
                'Kotone')

        self.center_on('Alice')

        self.set_cursor_state(True)
        self.set_stats_display(True)

class SummonFireflies(MapActionEvent):

    def __init__(self):
        trigger_list = [
            TurnNumTrigger(5),
            UnitAliveTrigger('Kotone', True),
        ]
        MapActionEvent.__init__(self, trigger_list)

    def execute(self):
        self.center_on('Kotone')
        self.emote('Kotone', 'exclamation')
        self.deploy_unit('Firefly A', (2, 4))
        self.deploy_unit('Firefly B', (5, 5))
        self.deploy_unit('Firefly C', (7, 4))
        self.deploy_unit('Firefly D', (11, 4))
        self.center_on_coords((6, 4))
        self.say("Good! The fireflies are here! They'll never see this coming.",
                 'Kotone',
                 'Kotone')
        self.center_on_coords((22, 13))


class KotonePursuit(MapActionEvent):

    def __init__(self):
        trigger_list = [
            TurnNumTrigger(8),
            UnitAliveTrigger('Kotone', True),
        ]
        MapActionEvent.__init__(self, trigger_list)

    def execute(self):
        self.center_on('Kotone')
        self.emote('Kotone', 'scribble')
        self.say("The battle's not progressing as planned at all. ...I have no choice. We're going in!",
                 'Kotone',
                 'Kotone')
        self.set_ai_state('Kotone', 'Pursuit')
        self.set_ai_state('Walking Tree D', 'Pursuit')
        self.set_ai_state('Walking Tree E', 'Pursuit')
        self.set_ai_state('Walking Tree F', 'Pursuit')

        self.center_on_coords((22, 13))

class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):
        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.remove_all_enemies()

        self.set_unit_pos('Kotone', (33, 2))

        self.set_unit_pos('Alice', (22, 13))
        self.set_unit_pos('Marisa', (21, 13))
        self.set_unit_pos('Youmu', (22, 15))
        self.set_unit_pos('Reimu', (21, 15))
        self.set_unit_pos('Keine', (20, 14))
        self.set_unit_pos('Ran', (23, 15))
        self.set_unit_pos('Chen', (24, 14))


    def execute(self):
        self.center_on('Kotone')

        self.say("Geez! I barely made it out of there in one piece. Ayaka is not going to take this well at all!",
                'Kotone',
                'Kotone')
        self.move_unit('Kotone', (33, -1))
        self.center_on('Alice')

        self.say("I see. Yuyuko is missing, and you believe that her disappearance is related to the recent crisis.",
                'Alice',
                'Alice')

        self.say("The circumstances under which our mistresses disappeared make it seem so.",
                'Ran',
                'Ran')

        self.say("Alice. Have you heard anything about them?",
                'Youmu',
                'Youmu')

        self.say("I have, but nothing you don't already know, I'm certain.",
                'Alice',
                'Alice')
        self.say("It seems that I am among the few remaining of the inhabitants of this forest. All others have either fled or joined forces with the Kodama Lords.",
                'Alice',
                'Alice')

        self.say("So what're you gonna do now, Miss Alice? Are you gonna come with us?",
                'Chen',
                'Chen')

        self.emote('Alice', 'questionmark')

        self.say("We'd love to have you with us.",
                'Marisa',
                'Marisa')

        self.say("I'm not sure yet. Solving Gensokyo's crises? Not really what I do every day.",
                'Alice',
                'Alice')

        self.say("Come on! Remember all the fun we had together last time?",
                'Marisa',
                'Marisa')

        self.emote('Alice', 'dotdotdot')

        self.say("Th-that's... F-fine. I am indebted to you all, I suppose--and, well, yes, I've developed an incipient need for vengeance against the Kodama Lords. Yes, that's it.",
                'Alice',
                'Alice')

        self.say("Great! Welcome aboard!",
                'Marisa',
                'Marisa')

        self.say("It will aid us greatly to have you fight alongside us, Alice.",
                'Youmu',
                'Youmu')


        self.say("I must clarify an important point first. I-I'm absolutely not doing this because I enjoy your company at all, Marisa!",
                'Alice',
                'Alice')

        self.center_on('Reimu')
        self.move_unit('Reimu', (21, 16))
        self.move_unit('Youmu', (21, 15))
        self.say("Ugh. Hey, Youmu.",
                'Reimu',
                'Reimu')

        self.say("Look at them, off in their own little world arguing with each other like an old married couple. It's kinda irritating, don't you think?",
                'Reimu',
                'Reimu')

        self.say("Ah, well, at the very least, they'll ensure this journey will be a lively one.",
                'Youmu',
                'Youmu')

