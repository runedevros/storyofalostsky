from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, TurnNumTrigger, UnitAliveTrigger

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'To the Aid of Alice'
        location = "Alice's House"
        id_string = 'touhoucon_demo'
        prereqs = []
        show_rewards = False
        desc = "The Kodama Lord Kodama Lord marches towards Alice's house in the Forest of Magic. Oh, no! Will our heroes be able to stop her in time?"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'touhoucon_demo.txt'
        mission_type = 'battle'
        objective = {'type':'Defend and Defeat Boss',
                     'target':'Kodama Lord',
                     'location_box': [14, 13, 3, 2],
                     'location_name': 'Alice\'s House',
                     'desc':'Defeat the Kodama Lord and keep enemies from Alice\'s house.'
                     }

        deploy_data = {'enable':True,
                       'max_units':9,
                       'preset_units':{'Alice':(15, 14),},
                       'boxes':[(14, 15, 3, 3),],
                       'default_locations':{'Youmu':(16, 16),
                                            'Chen':(15, 15),
                                            'Ran':(15, 16),
                                            'Marisa':(15, 17),
                                            'Mokou':(14, 16),
                                            'Alice':(15, 14),
                       }

                       }
        reward_list = [('spell_action', 'Feather Pin'),
                       ('treasure', '007_spellbook')
                      ]

        # Enemy Unit Data
        enemy_unit_data = [

                            # Initial enemy group
                            {'template_name': 'Kodama Lord',
                                'unit_name': 'Kodama Lord',
                                    'level': 12
                                },
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 12
                                },
                            {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 12
                                },

                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 12},

                            # Units close to alice's house

                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 12},
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 12},
                            {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy A',
                                    'level': 12
                                },
                            {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree D',
                                    'level': 12},


                            # Squad 3 - Firefly unit from the northwest

                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly A',
                                    'level': 12
                                },
                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly B',
                                    'level': 12
                                },
                            {'template_name': 'Firefly',
                                'unit_name': 'Firefly C',
                                    'level': 12
                                },

                            # Alice's Dolls
                            {'template_name': 'Doll',
                                'unit_name': 'Doll A',
                                    'level': 12},
                            {'template_name': 'Doll',
                                'unit_name': 'Doll B',
                                    'level': 12},
                            {'template_name': 'Doll',
                                'unit_name': 'Doll C',
                                    'level': 12},

                                
                            ]

        initial_spells = {'Fairy A':['Fireball'],
                          'Fairy B':['Fireball'],

                          'Walking Tree A':['Leaf Crystal'],
                          'Walking Tree B':['Leaf Crystal'],
                          'Walking Tree C':['Leaf Crystal'],
                          'Walking Tree D':['Leaf Crystal'],
                          'Healer Fairy A':['Healing Drop'],

                          'Kodama Lord':['Fireball'],

                          'Firefly A':['Fireball'],
                          'Firefly B':['Poison Dust'],
                          'Firefly C':['Fireball'],


                            }
        initial_traits = {'Healer Fairy A':['Move+ Lv.1', 'Flight'],
                          'Firefly A':['Flight'],
                          'Firefly B':['Flight'],
                          'Firefly C':['Flight'], }
        initial_ai_states = {'Kodama Lord':'Attack',
                             'Fairy A':'Attack',
                             'Fairy B':'Attack',
                             'Walking Tree A':'Attack',
                             'Walking Tree B':'Attack',
                             'Walking Tree C':'Attack',
                             'Walking Tree D':'Attack',

                             'Firefly A': 'Pursuit',
                             'Firefly B': 'Pursuit',
                             'Firefly C': 'Pursuit',

                             'Healer Fairy A': 'HealerStandby',

                            }
        initial_locations = {'Fairy A':(14, 15),
                             'Fairy B':(27, 3),
                             'Walking Tree A':(28, 2),
                             'Kodama Lord':(15, 15),

                             'Walking Tree B':(14, 17),
                             'Walking Tree C':(15, 17),
                             'Walking Tree D':(16, 17),
                             'Healer Fairy A':(-1,-1),


                             'Youmu': (15, 25),
                             'Alice':(-1,-1),
                             'Marisa': (15, 21),
                             'Ran': (15, 25),
                             'Chen': (15, 25),
                             'Mokou': (15, 25),

                             }
        reserve_units = ['Firefly A', 'Firefly B', 'Firefly C', 'Doll A', 'Doll B', 'Doll C']#[list of unit names to deploy later in mission]
        all_landmarks = [{'name':'Alice\'s House',
                          'id_string':'house_2',
                          'location':(15, 13)},

                         {'name':'banner1',
                          'id_string':'treebanner',
                          'location':(27, 2)},
                         {'name':'banner2',
                          'id_string':'treebanner',
                          'location':(29, 2)},
                         {'name':'banner3',
                          'id_string':'treebanner',
                          'location':(27, 4)},
                         {'name':'banner4',
                          'id_string':'treebanner',
                          'location':(29, 4)},
                         ]

        required_starters = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Mokou', 'Alice']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [SummonFireflies(), KodamaLordPursuit()]
        required_survivors = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Mokou', 'Alice', 'Kodama Lord']
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

        self.play_music('event03')
        self.center_on('Kodama Lord')

        self.say("Um. Hey. We did check that someone's actually home, right?",
                'Fairy',
                'Fairy')
        self.say("Uh. Well--a-aha! Something moved in that window over there! Someone's definitely home. I know you're in there, Alice! Would you please just come out and give us a reply already?",
                'Kodama Lord',
                'Kodama')
        self.emote('Kodama Lord', 'scribble')
        self.say("You can't run away! There's no way out! We have your house surrounded!",
                'Kodama Lord',
                'Kodama')
        self.center_on('Kodama Lord')
        self.say("Tch, fine. Guess we'll have to show her we mean business. Walking Tree! Break in through that window!",
                'Kodama Lord',
                'Kodama')
        #
        self.say("Yes! Looks like we got here in time!",
                'Marisa',
                'Marisa')
                
        self.say("Wait! Marisa!",
                'Ran',
                'Ran')

        self.play_sfx('shoot2')
        self.move_unit('Marisa', (15, 14))
        self.play_sfx('hit')
        self.move_unit('Kodama Lord', (17, 15))


        
        self.say("Thought you could go around and bully my friend and get away with it, could you?! Well think again!",
                'Marisa',
                'Marisa')
        self.emote('Marisa', 'questionmark')
        self.say("Uh... Say do you guys hear something?",
                'Marisa',
                'Marisa')
        
        # # Three dolls deploy around Marisa
        self.say("Something's ticking. A clock perhaps.",
                'Fairy A',
                'Fairy')
        self.emote('Marisa', 'exclamation')
        
        self.deploy_unit('Doll A', (15, 13))
        self.move_unit('Doll A', (14, 14))
        self.deploy_unit('Doll B', (15, 13))
        self.move_unit('Doll B', (16, 14))
        self.deploy_unit('Doll C', (15, 13))
        
        self.say("Oh no. Oh no. Oh nononononono--this is really, really bad!",
                'Marisa',
                'Marisa')
        
        
        self.play_music('battle04')



        self.set_unit_pos('Alice', (15, 10))
        
        self.center_on('Alice')
        
        self.say("Marisa, you idiot!",
                'Alice',
                'Alice')


                
        self.center_on('Marisa')
        
        # Dolls explode, taking themselves and a few nearby units out. Marisa is thrown aside.
        self.play_sfx('explode')
        self.fade_to_color('white', 1.5)
        self.kill_unit('Doll A')
        self.kill_unit('Doll B')
        self.kill_unit('Doll C')


        self.set_unit_pos('Marisa', (13, 14))


        south_team_locations = {

                             'Fairy A':(1, 30),
                             'Kodama Lord':(1, 30),
                             'Walking Tree B':(1, 30),
                             'Walking Tree C':(1, 30),
                             'Walking Tree D':(1, 30),
                             'Healer Fairy A':(1, 30),
                            }

        for unit_name in south_team_locations.keys():
            self.set_unit_pos(unit_name, south_team_locations[unit_name])


        self.fade_from_color('white', 1.5)

        self.move_unit('Alice', (14, 13))



        self.move_unit('Youmu', (15, 15))
        self.move_unit('Ran', (16, 15))
        self.move_unit('Chen', (15, 16))
        self.move_unit('Mokou', (16, 16))

        self.center_on('Marisa')

        self.startle('Marisa')
        self.say("Marisa! Marisa, are you okay?!",
                'Youmu',
                'Youmu')
        self.say("Owowowowowowowowow! Ow! Quit it!",
                'Marisa',
                'Marisa')
        self.say("Hold still, Marisa! You were thrown a long distance by that blast, and rather violently at that, so please let me get to work.",
                'Ran',
                'Ran')

        self.move_unit('Ran', (14, 15))
        self.emote('Marisa', 'scribble')
        self.say("There. That should get you back on your feet.",
                'Ran',
                'Ran')

        self.say("How like you to charge in so recklessly. I had those exploding dolls set up as a trap for that Kodama Lord, not for you! Idiot!",
                'Alice',
                'Alice')
        self.emote('Marisa', 'annoyed')
        self.say("Hey, don't blame me! We came to help you! I thought you were in trouble!",
                'Marisa',
                'Marisa')
        self.say("And why would I need your help? Don't you dare look down on me. I could have taken Kodama Lord on my own, easily.",
                'Alice',
                'Alice')
        self.say("See? I told you Alice could fend for herself.",
                'Mokou',
                'Mokou')

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

        south_team_locations = {

                             'Fairy A':(29, 3),
                             'Kodama Lord':(28,3),
                             'Walking Tree B':(26, 15),
                             'Walking Tree C':(26, 15),
                             'Walking Tree D':(26, 15),
                             'Healer Fairy A':(26, 15),
                            }

        for unit_name in south_team_locations.keys():
            self.set_unit_pos(unit_name, south_team_locations[unit_name])


        south_team_locations = {

                             'Walking Tree B':(21, 14),
                             'Walking Tree C':(22, 17),
                             'Walking Tree D':(18, 16),
                             'Healer Fairy A':(20,16),
                            }


        self.say("Let's take this chance to position ourselves to defend Alice's house while she gathers her things.",
                'Ran',
                'Ran')

        for unit_name in south_team_locations.keys():
            self.move_unit(unit_name, south_team_locations[unit_name])

        self.say("Agreed!",
                'Youmu',
                'Youmu')

        self.center_on('Kodama Lord')
        self.say("Our scouting team was taken out!",
                'Fairy',
                'Fairy')
        self.say("Argh! Inexcusable! Unacceptable!!!",
                'Kodama Lord',
                'Kodama')
        self.say("Never mind! Press onward with the attack! There is no change in strategy!",
                'Kodama Lord',
                'Kodama')
        self.say("We are the guardians of this forest! Regardless of the odds, we will never back down! So charge!",
                'Kodama Lord',
                'Kodama')

        self.center_on('Youmu')

        self.set_cursor_state(True)
        self.set_stats_display(True)

class SummonFireflies(MapActionEvent):

    def __init__(self):
        trigger_list = [
            TurnNumTrigger(3),
            UnitAliveTrigger('Kodama Lord', True),
        ]
        MapActionEvent.__init__(self, trigger_list)

    def execute(self):
        self.center_on('Kodama Lord')
        self.emote('Kodama Lord', 'exclamation')

        self.deploy_unit('Firefly A', (2, 5))
        self.deploy_unit('Firefly B', (7, 3))
        self.deploy_unit('Firefly C', (11, 3))
        self.center_on_coords((6, 4))
        self.say("Good! The fireflies are here! They'll never see this coming.",
                 'Kodama Lord',
                 'Kodama')
        self.center_on_coords((22, 13))


class KodamaLordPursuit(MapActionEvent):

    def __init__(self):
        trigger_list = [
            TurnNumTrigger(6),
            UnitAliveTrigger('Kodama Lord', True),
        ]
        MapActionEvent.__init__(self, trigger_list)

    def execute(self):
        self.center_on('Kodama Lord')
        self.emote('Kodama Lord', 'scribble')
        self.say("The battle's not progressing as planned at all. ...I have no choice. We're going in!",
                 'Kodama Lord',
                 'Kodama')
        self.set_ai_state('Kodama Lord', 'Pursuit')
        self.set_ai_state('Walking Tree A', 'Pursuit')
        self.set_ai_state('Fairy A', 'Pursuit')
        self.set_ai_state('Fairy B', 'Pursuit')

        self.center_on_coords((22, 13))

class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):
        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.remove_all_enemies()

        self.set_unit_pos('Kodama Lord', (28, 3))

        self.set_unit_pos('Alice', (15, 14))
        self.set_unit_pos('Marisa', (15, 17))
        self.set_unit_pos('Youmu', (16, 16))
        self.set_unit_pos('Ran', (15, 16))
        self.set_unit_pos('Chen', (15, 15))
        self.set_unit_pos('Mokou', (14, 16))


    def execute(self):
        self.center_on('Kodama Lord')

        self.say("Geez! I barely made it out of there in one piece. The others are not going to take this well at all!",
                'Kodama Lord',
                'Kodama')
        self.move_unit('Kodama Lord', (28, -1))
