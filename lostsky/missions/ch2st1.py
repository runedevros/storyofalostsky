from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, ArrivalTrigger
from lostsky.battle.mapobj import SpiritSourcePoint

class Mission(BattleEvent):

    def __init__(self):




        # Map Data
        name = "A Barrier of History"
        location = 'Human Village'
        id_string = 'CH2ST1'
        prereqs = ['CH1ST4']
        show_rewards = False
        desc = "A crisis befalls the human village! A swarm of youkai that fleeing from the Forest of Magic have arrived at the human village! Keine, the village teacher has been desperately trying to fend them off, alone! But as commendable as her deeds are, how will she fare?!"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        ssp_list = [SpiritSourcePoint('W Point', (9, 14), 1),
                    SpiritSourcePoint('SW Point', (14, 23), 0),
                    SpiritSourcePoint('NW Point', (14, 6), 0),
                    SpiritSourcePoint('SE Point', (20, 23), 0),
                    SpiritSourcePoint('NE Point', (20, 6), 0),
                    SpiritSourcePoint('E Point', (25, 14), 0)
                    ]


        map_name = 'ch2st1.txt'
        mission_type = 'battle'
        objective = {'type':'Capture Spirit Sources',
                     'number':6,
                     'ssps':ssp_list,
                     'desc':'Capture 6 Spirit Sources!'
                     }

        deploy_data = {'enable':True,
                       'max_units':6,
                       'preset_units':{},
                       'boxes':[(1, 15, 4, 2)],
                       'default_locations':{'Youmu':(4,16),
                                            'Ran':(2,16),
                                            'Chen':(3,16),
                                            'Reimu':(3,15),
                                            'Keine':(4,15),
                                            'Marisa':(2,15),
                                            },
                       }

        reward_list = [('treasure', 'synth_fire'),
                       ('treasure', 'synth_earth')

                       ]

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 6},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 6},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 6},

                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly A',
                                    'level': 4},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly B',
                                    'level': 4},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly C',
                                    'level': 5},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly D',
                                    'level': 5},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly E',
                                    'level': 7},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly F',
                                    'level': 7},

                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball A',
                                    'level': 6},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball B',
                                    'level': 6},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball C',
                                    'level': 6},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball D',
                                    'level': 6},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball E',
                                    'level': 6},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball F',
                                    'level': 6},

                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel A',
                                    'level': 6},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel B',
                                    'level': 6},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel C',
                                    'level': 6}
                          ]

        initial_spells = {'Firefly A':['Poison Dust'],
                          'Firefly B':['Poison Dust'],
                          'Firefly C':['Poison Dust'],
                          'Firefly D':['Poison Dust'],
                          'Firefly E':['Poison Dust'],
                          'Firefly F':['Poison Dust'],

                          'Fairy A':['Fireball'],
                          'Fairy B':['Leaf Crystal'],
                          'Fairy C':['Fireball'],

                          'Fuzzball A':['Dagger Throw'],
                          'Fuzzball B':['Holy Amulet'],
                          'Fuzzball C':['Dagger Throw'],
                          'Fuzzball D':['Fireball'],
                          'Fuzzball E':['Dagger Throw'],
                          'Fuzzball F':['Dagger Throw'],

                          'Wind Weasel A':['Leaf Crystal'],
                          'Wind Weasel B':['Leaf Crystal'],
                          'Wind Weasel C':['Dagger Throw'],
                          }
        initial_traits = {'Firefly A':['Flight'],
                          'Firefly B':['Flight'],
                          'Firefly C':['Flight'],
                          'Firefly D':['Flight'],
                          'Firefly E':['Flight'],
                          'Firefly F':['Flight'],
                          }
        initial_ai_states = {'Fuzzball A':'Attack',
                             'Fuzzball B':'Attack',
                             'Fuzzball C':'Attack',
                             'Fuzzball D':'Attack',
                             'Fuzzball E':'Attack',
                             'Fuzzball F':'Attack',
                             'Wind Weasel A':'Attack',
                             'Wind Weasel B':'Attack',
                             'Wind Weasel C':'Attack',
                             'Fairy A':'Attack',
                             'Fairy B':'Attack',
                             'Fairy C':'Attack',
                             'Firefly A':'Attack',
                             'Firefly B':'Attack',
                             'Firefly C':'Attack',
                             'Firefly D':'Attack',
                             'Firefly E':'Attack',
                             'Firefly F':'Attack',
                             }
        initial_locations = {'Ran':(2, 16),
                             'Chen':(3, 16),
                             'Reimu':(3, 18),
                             'Marisa':(2, 18),
                             'Youmu':(3, 17),

                             # Two Fireflies above western SSP
                             'Firefly A':(9, 9),
                             'Firefly B':(10, 9),

                             # Five Fuzzballs at NW SSP
                             'Fuzzball A':(10, 5),
                             'Fuzzball B':(11, 4),
                             'Fuzzball C':(12, 5),
                             'Fuzzball D':(13, 4),
                             'Fuzzball E':(14, 5),

                             # Three Fairies at SW SSP
                             'Fairy A':(14, 24),
                             'Fairy B':(15, 24),
                             'Fairy C':(15, 23),

                             # Two FIreflies between E and SE SSP
                             'Firefly C':(20, 20),
                             'Firefly D':(21, 22),

                             #Fuzzball and 2 Fireflies at NE SSP
                             'Firefly E':(23, 10),
                             'Fuzzball F':(24, 11),
                             'Firefly F':(25, 10),

                             # 3 Wind Weasels at E SSP
                             'Wind Weasel A':(24, 15),
                             'Wind Weasel B':(25, 16),
                             'Wind Weasel C':(26, 15),

                            }

        reserve_units = []
        all_landmarks = [{'name':'House 1',
                          'id_string':'house_1',
                          'location':(17, 14)},
                         {'name':'House 2',
                         'id_string':'house_1',
                          'location':(15, 16)},
                         {'name':'House 3',
                          'id_string':'house_1',
                          'location':(17, 12)},
                         {'name':'House 4',
                         'id_string':'house_1',
                          'location':(15, 13)},
                         {'name':'House 5',
                          'id_string':'house_2',
                          'location':(19, 14)},
                         {'name':'House 6',
                         'id_string':'house_2',
                          'location':(18, 16)},
                         {'name':'House 7',
                          'id_string':'house_2',
                          'location':(13, 15)},
                         {'name':'House 8',
                         'id_string':'house_2',
                          'location':(14, 12)},


                         {'name':'W marker 1',
                          'id_string':'big_rock',
                          'location':(8, 14)},
                         {'name':'W marker 2',
                          'id_string':'big_rock',
                          'location':(10, 14)},
                         {'name':'NW marker 1',
                          'id_string':'big_rock',
                          'location':(13, 6)},
                         {'name':'NW marker 2',
                          'id_string':'big_rock',
                          'location':(15, 6)},
                         {'name':'NE marker 1',
                          'id_string':'big_rock',
                          'location':(19, 6)},
                         {'name':'NE marker 2',
                          'id_string':'big_rock',
                          'location':(21, 6)},
                         {'name':'E marker 1',
                          'id_string':'big_rock',
                          'location':(24, 14)},
                         {'name':'E marker 2',
                          'id_string':'big_rock',
                          'location':(26, 14)},
                         {'name':'SE marker 1',
                          'id_string':'big_rock',
                          'location':(15, 23)},
                         {'name':'SW marker 1',
                          'id_string':'big_rock',
                          'location':(19, 23)},
                         {'name':'SW marker 2',
                          'id_string':'big_rock',
                          'location':(21, 23)},


                         {'name':'Mini Shrine',
                          'id_string':'minishrine',
                          'location':(25, 2)},
                         {'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(24, 2)},
                         {'name':'CB2',
                          'id_string':'cherryblossom_tree',
                          'location':(26, 2)},

                         {'name':'LP1',
                          'id_string':'lilypad',
                          'location':(10, 27)},
                         {'name':'LP2',
                          'id_string':'lilypad',
                          'location':(12, 29)},
                         {'name':'LP3',
                          'id_string':'lilypad',
                          'location':(8, 29)},

                         ]

        required_starters = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Reimu']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [ShrineTreasureMAE()]
        required_survivors = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Reimu', 'Keine']
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

        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.set_bg_overlay('Sunset')

        # Add Keine to party
        self.add_to_party('Keine')
        self.assign_spell('Keine', 'Healing Drop')
        self.assign_spell('Keine', 'Sunbeam Mirror')
        self.assign_spell('Keine', 'Medicinal Drop')
        self.assign_spell('Keine', 'Encourage')
        self.assign_spell('Keine', 'Tracking Shot')
        self.set_unit_pos('Keine', (9, 15))

        self.center_on('Marisa')
        self.play_music('battle02')
        self.say("No way! They're over here too?",
                'Marisa',
                'Marisa')
        self.say("They appear to be the same ones that escaped the forest. They're fleeing.",
                'Youmu',
                'Youmu')
        self.say("Pardon, Reimu. A question. How long it would it take a youkai to get here from the forest?",
                'Keine',
                'Keine')

        # Keine moves closer to player units
        self.move_unit('Keine', (4, 18))
        self.say("These monsters have been leaving from the Forest of Magic in frenzied droves. They're violent and unpredictable, and, I theorize, unusually fast as well.",
                'Keine',
                'Keine')
        self.say("And we only just managed to get out of there alive... so I guess they're pretty fast seeing as they beat us.",
                'Reimu',
                'Reimu')
        self.say("Things were pretty crazy back in the forest. I thought we could get away from that mess, but of course not.",
                'Reimu',
                'Reimu')
        self.say("Hey, hey. What are those glowing lights at the edges of the village?",
                'Chen',
                'Chen')
        self.say("Ah, yes. Those are Spirit Source Points.",
                'Ran',
                'Ran')
        self.say("Spirit Source Points, huh? So what kind of a spell are you trying to cook up here, Keine?",
                'Marisa',
                'Marisa')
        self.say("A splendid question. It is a spell that will hide the village from anyone beyond its borders.",
                'Keine',
                'Keine')
        self.say("Should they look in our direction, they will only see what is beyond, not within. An invisibility spell of sorts.",
                'Keine',
                'Keine')
        self.say("Sadly only this place has been tightly secured. The others are not so fortunate, and I must do what I can for them.",
                'Keine',
                'Keine')
        self.say("If you wouldn't mind, I would greatly appreciate any assistance you could offer.",
                'Keine',
                'Keine')
        self.say("Oh, yes, a word of warning. Those fireflies can spray venomous dust over a large area. But not to worry; I have with me some medicine, as a precaution.",
                'Keine',
                'Keine')
        self.say("Keine is a healer. Her Healing Drop spell recovers health and her Medicinal Drop item can be used to cure poison and other status effects.",
                'Tutorial',
                None)
        self.say("All right, already. Let's just go beat them up and get this over with.",
                'Reimu',
                'Reimu')
        self.show_chapter_title(2)
        self.say("Oh, that's not really necessary. We simply have to maintain control of the Spirit Source Points. How would you like a review lesson on how they work?",
                'Keine',
                'Keine')

        # Tutorial on spirit source points
        tutorial_selection = self.choice('Would you like to view the tutorial on Spirit Source Points?',
                                        ['Yes', 'No'])
        if tutorial_selection == 'Yes':
            self.say("Um. Well. I don't know much about them, so it would be really helpful.",
            'Chen',
            'Chen')
            self.say("Spirit Source Points guide the flow of magic around Gensokyo, channeling and amplifying it.",
                    'Keine',
                    'Keine')
            self.say("Any wide area spell needs them. Think of it like a humongous magnifying glass for spells!",
                    'Marisa',
                    'Marisa')
            self.say("The objective of this battle will be to capture the six Spirit Source Points (SSPs). Once a unit lands on a location with a SSP, it is captured for the unit's team.",
                    'Tutorial',
                    None)
            self.say("The unit is not required to stay on the tile, but if another team's unit lands on the SSP, control switches over to the new owner.",
                    'Tutorial',
                    None)
            self.say("At the start of each turn, any unit occupying an SSP will gain a small amount of spirit charge (Up to 500 SC).",
                    'Tutorial',
                    None)
            self.say("This all sounds rather complicated.",
                    'Youmu',
                    'Youmu')
            self.say("Heh, this simple thing? Just be glad that you all don't have to learn all the intricacies of spiritual arts. You'll be in over your head in seconds! Curious?",
                    'Reimu',
                    'Reimu')
        else:
            self.say("We can save the explanations for after we're done. Let's go capture those points quickly.",
                    'Youmu',
                    'Youmu')

        self.set_cursor_state(True)
        self.set_stats_display(True)

class ShrineTreasureMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((25, 2, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        self.say("A lone shrine sits tucked away in the thicket of trees.",
        None,
        None)
        self.say("Off to the side, there is a small, dusty box. Inside is a glistening talisman!",
                None,
                None)
        self.say("Acquired Treasure Item: Dusty Talisman!",
                None,
                None)
        self.add_item('treasure', '001_talisman', 1)


class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):
        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.remove_all_enemies()
        self.set_unit_pos('Keine', (9, 15))
        self.set_unit_pos('Youmu', (9, 16))
        self.set_unit_pos('Marisa', (8, 16))
        self.set_unit_pos('Reimu', (7, 15))
        self.set_unit_pos('Chen', (10, 16))
        self.set_unit_pos('Ran', (11, 15))

    def execute(self):
        self.center_on('Keine')

        self.say("I invoke the magic of history! Rid the image of this human village from all memory!",
                'Keine',
                'Keine')

        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)
        self.startle('Youmu')
        self.pause(0.5)

        # Youmu scurries around trying to see what happened
        self.move_unit('Youmu', (14, 16))
        self.say("What... But...",
                'Youmu',
                'Youmu')
        self.startle('Youmu')
        self.pause(0.5)
        self.move_unit('Youmu', (9, 16))

        self.say("Nothing has changed...",
                'Youmu',
                'Youmu')
        self.say("If you will recall, you are not among the affected. You and the everyone in the village are free to come and go, but outsiders, however, are none the wiser.",
                'Keine',
                'Keine')
        self.say("Oh, hey, by the way, Keine. These three were looking to have a word with you.",
                'Marisa',
                'Marisa')
        self.say("Yes. We were wondering if you or Miss Hieda knew anything about the Kodama Lords responsible for the mayhem in the forest. That's originally why we chose to come here.",
                'Youmu',
                'Youmu')
        self.say("If it's an explanation you wanted, you've come to the correct place. Let's head into the village, where you can make yourselves at home while I prepare the lesson.",
                'Keine',
                'Keine')
        self.set_cursor_state(True)
        self.set_stats_display(True)
