'''
Created on Feb 26, 2011

@author: Fawkes
'''
from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, TurnNumTrigger, UnitAliveTrigger

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'Kotone\'s Schemes'
        location = 'Central Forest'
        id_string = 'CH2SQ1'
        prereqs = ['CH2ST2']
        show_rewards = True
        desc = "Some of my bug friends are stuck in the forest and want to leave, but I can't make the time to go back and help them. By the way, I've heard rumors that the Kodama Lord Kotone has been gathering a large group of fairies and tree youkai to bully the more stubborn forest residents into joining them. Kotone is a pretty rash and impatient Kodama Lord, so wrecking her plans should be a cinch. Please let my friends escape! In return, I promise to reward you with a few treasures that I found in the forest. Thanks in advance! --Wriggle Nightbug"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch1st2b.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat All',
                     'desc':'Defeat all enemies!'
                     }

        deploy_data = {'enable':True,
                       'max_units':8,
                       'preset_units':{},
                       'boxes':[(25, 21, 4, 4)],
                       'default_locations':{'Youmu':(25,22),
                                            'Ran':(25,23),
                                            'Chen':(26,23),
                                            'Reimu':(25,24),
                                            'Keine':(26,22),
                                            'Marisa':(25,21),
                                            'Mokou':(26,21),
                                            'Aya':(26,24),
                                            },
                       }

        reward_list = [('spell_action', 'Shimmering Stars'),
                       ('treasure', 'synth_fire'),
                       ('treasure', 'synth_metal'),
                       ('treasure', 'synth_earth'),
                      ]

        # Enemy Unit Data
        enemy_unit_data = [

                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 6},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 6},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 6},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree D',
                                    'level': 6},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree E',
                                    'level': 6},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree F',
                                    'level': 6},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree G',
                                    'level': 6},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree H',
                                    'level': 6},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree I',
                                    'level': 6},


                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy A',
                                    'level': 6},
                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy B',
                                    'level': 6},
                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy C',
                                    'level': 6},


                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy Captain',
                                    'level': 8},
                           {'template_name': 'Fairy',
                                'unit_name': 'Dazzling Fairy',
                                    'level': 6},
                           {'template_name': 'Fairy',
                                'unit_name': 'Cosmic Fairy',
                                    'level': 6},
                           {'template_name': 'Fairy',
                                'unit_name': 'Ninja Fairy',
                                    'level': 6},
                           {'template_name': 'Fairy',
                                'unit_name': 'Sealing Fairy',
                                    'level': 6},
                           {'template_name': 'Fairy',
                                'unit_name': 'Toxic Fairy',
                                    'level': 6},

                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel A',
                                    'level': 6},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel B',
                                    'level': 6},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel C',
                                    'level': 6},


                           {'template_name': 'Kotone',
                                'unit_name': 'Kotone',
                                    'level': 9},

                          ]

        initial_spells = {
                          'Fairy Captain':['Holy Amulet'],
                          'Kotone':['Leaf Crystal'],

                          'Dazzling Fairy':['Shimmering Stars'],
                          'Ninja Fairy':['Feather Pin'],
                          'Cosmic Fairy':['Stardust'],
                          'Toxic Fairy':['Poison Dust'],
                          'Sealing Fairy':['Spirit Break'],

                          'Wind Weasel A':['Dagger Throw'],
                          'Wind Weasel B':['Dagger Throw'],
                          'Wind Weasel C':['Dagger Throw'],

                          'Walking Tree D':['Leaf Crystal'],
                          'Walking Tree E':['Leaf Crystal'],
                          'Walking Tree F':['Leaf Crystal'],
                          'Walking Tree G':['Leaf Crystal'],
                          'Walking Tree H':['Leaf Crystal'],
                          'Walking Tree I':['Leaf Crystal'],

                          'Healer Fairy A':['Healing Drop'],
                          'Healer Fairy B':['Healing Drop'],
                          'Healer Fairy C':['Healing Drop'],

                          }

        initial_traits = {}

        initial_ai_states = {'Fairy Captain':'Attack',
                          'Kotone':'Attack',
                          'Walking Tree D':'Attack',
                          'Walking Tree E':'Attack',
                          'Walking Tree F':'Attack',
                          'Walking Tree G':'Attack',
                          'Walking Tree H':'Attack',
                          'Walking Tree I':'Attack',

                          'Wind Weasel A':'Attack',
                          'Wind Weasel B':'Attack',
                          'Wind Weasel C':'Attack',


                          'Cosmic Fairy':'Attack',
                          'Sealing Fairy':'Attack',
                          'Ninja Fairy':'Attack',
                          'Dazzling Fairy':'Attack',
                          'Toxic Fairy':'Attack',

                          'Healer Fairy A':'HealerStandby',
                          'Healer Fairy B':'HealerStandby',
                          'Healer Fairy C':'HealerStandby',

                          }

        initial_locations = {'Marisa':(26, 24),
                             'Reimu':(26, 25),
                             'Youmu':(27, 23),
                             'Ran':(28, 24),
                             'Chen':(28, 25),
                             'Keine':(27, 25),

                             'Fairy Captain':(11, 4),
                             'Kotone':(12, 4),
                             'Walking Tree A':(14, 3),
                             'Walking Tree B':(14, 4),
                             'Walking Tree C':(14, 5),


                             'Wind Weasel A':(23, 9),
                             'Wind Weasel B':(21, 8),
                             'Wind Weasel C':(25, 8),
                             'Healer Fairy A':(23, 8),

                             'Toxic Fairy':(9, 21),
                             'Dazzling Fairy':(11, 20),
                             'Healer Fairy B':(11, 22),


                             }
        reserve_units = ['Healer Fairy C',

                         'Walking Tree D',
                         'Walking Tree E',
                         'Walking Tree F',
                         'Walking Tree G',
                         'Walking Tree H',
                         'Walking Tree I',
                         'Sealing Fairy',
                         'Ninja Fairy',
                         'Cosmic Fairy',
                         ]
        all_landmarks = [{'name':'M1',
                          'id_string':'mushroom',
                          'location':(10, 11)},
                         {'name':'M2',
                          'id_string':'mushroom',
                          'location':(8, 8)},
                         {'name':'M3',
                          'id_string':'mushroom',
                          'location':(23, 8)},
                         {'name':'M4',
                          'id_string':'mushroom',
                          'location':(18, 10)},
                         {'name':'M5',
                          'id_string':'mushroom',
                          'location':(24, 21)},
                         {'name':'M6',
                          'id_string':'mushroom',
                          'location':(11, 18)},
                         {'name':'M7',
                          'id_string':'mushroom',
                          'location':(14, 22)},
                         {'name':'M8',
                          'id_string':'mushroom',
                          'location':(13, 27)},
                         {'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(27, 23)},
                         ]

        required_starters = ['Youmu', 'Chen', 'Ran', 'Reimu', 'Marisa', 'Keine']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [Turn2MAE(),
                                Turn6MAE(),
                                FiveFairiesDeadMAE()
                                ]
        post_mission_MAE = PostMissionMAE()
        required_survivors = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Reimu', 'Keine', 'Fairy Captain']

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
        Introductory Scene: Kotone gathers her forces
        """

        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.play_music('battle03')

        # Kotone and party prepares for battle
        self.center_on('Kotone')
        self.say("You there! Fairy Captain!",
                 "Kotone",
                 'Kotone')
        self.startle('Fairy Captain')
        self.say("Yes, Kotone!",
                 "Fairy Captain",
                 "Fairy")
        self.emote('Kotone', 'annoyed')
        self.say("Ugh. Tell me. Who has yet to arrive?",
                 "Kotone",
                'Kotone')
        self.say("Yes! Haruna's reinforcements for one. She's sending a few more trees from the swamp region our way.",
                 "Fairy Captain",
                 "Fairy")
        self.say("We're also waiting on some additional fairy reinforcements. We simply need to be patient for a few more hours before their arrival.",
                 "Fairy Captain",
                 "Fairy")
        self.center_on('Youmu')
        self.say("It's just as Wriggle said. This Kodama Lord has incredible support from the forest inhabitants. This could prove difficult.",
                 "Youmu",
                 "Youmu")
        self.say("Yes, potentially. Their tongues have proven to be fairly loose, so let's see if they'll let something useful slip.",
                 "Ran",
                 "Ran")
        self.say("Oh, hey. I wonder where they're headed.",
                 "Marisa",
                 "Marisa")
        self.center_on('Kotone')


        self.say("Annoyingly, Ayaka handed me this mission without telling me much about it. So fill me in. Tell me about this girl we're visiting.",
                 "Kotone",
                 'Kotone')
        self.say("Yes. The girl is a solitary sorceress named Alice Margatroid. She is well known for her mastery of puppetry and magic.",
                 "Fairy Captain",
                 "Fairy")
        self.say("Puppets? Ha! Let's not sell ourselves short. As if those could put up a fight.",
                 "Kotone",
                 'Kotone')
        self.say("I see. Then we intend to fight her.",
                 "Fairy Captain",
                 "Fairy")
        self.say("If memory serves right, you were originally under Haruna, Kodama Lord of the Northern Forests, weren't you?",
                 "Kotone",
                 'Kotone')
        self.say("Now I know Haruna prefers resolving conflicts peacefully but not me. With me, we settle our matters in battle, not mere words. Am I understood, Captain?",
                 "Kotone",
                 'Kotone')

        # Kotone gets impatient
        self.emote('Kotone', 'dotdotdot')
        self.say("(Ugh! This is ticking me off! Just how much longer do I have to wait? Can't we just go now!)",
                 "Kotone",
                 'Kotone')
        self.emote('Kotone', 'dotdotdot')


        self.say("Captain. You stay behind and gather our allies together. Come join me at the magician Alice's house when they've arrived.",
                 "Kotone",
                 'Kotone')
        self.say("You won't wait? It shouldn't be much longer.",
                 "Fairy Captain",
                 "Fairy")
        self.say("Hmph. I suppose I'll take a few of the trees that Haruna brought with me.",
                 "Kotone",
                 'Kotone')
        self.say("Don't worry, I've already sent a few ahead. By the time you guys reach us, we should have plenty of manpower to defeat that puny magician and her measly puppets.",
                 "Kotone",
                 'Kotone')
        self.say("By the time you guys get there, we should have enough to easily take on one puny magician.",
                 "Kotone",
                 'Kotone')
        self.say("Understood!",
                 "Fairy Captain",
                 "Fairy")

        # Kotone and a few walking trees withdraw from the battle map
        self.startle('Kotone')
        self.say("All right. Let's go!",
                 "Kotone",
                 'Kotone')
        self.move_unit('Kotone', (13, -1))
        self.move_unit('Walking Tree A', (14, -1))
        self.move_unit('Walking Tree B', (14, -1))
        self.move_unit('Walking Tree C', (14, -1))

        self.kill_unit('Kotone')
        self.kill_unit('Walking Tree A')
        self.kill_unit('Walking Tree B')
        self.kill_unit('Walking Tree C')

        # Party plans out what to do next
        self.center_on('Youmu')

        self.startle('Marisa')
        self.emote('Marisa', 'exclamation')
        self.say("Oh, geez! They're after Alice now! Come on, let's go, let's go! We've gotta follow her!",
                 "Marisa",
                 "Marisa")
        self.say("Hold on, Marisa. These trees are Kotone's reinforcements, right? She's severely underestimated Alice's strength if she's only taking a handful of trees.",
                 "Ran",
                 "Ran")
        self.say("Maybe, but...Alice has always been a loner. If it's just her up against Kotone and those trees, I'm not sure she'll come out okay at the end!",
                 "Marisa",
                 "Marisa")
        self.say("Please. Alice can take care of herself. She's as experienced as we are.",
                 "Reimu",
                 "Reimu")
        self.say("So, um. So what's the plan?",
                 "Chen",
                 "Chen")
        self.say("I suggest we defeat the reinforcements as soon as they've gathered here.",
                 "Ran",
                 "Ran")
        self.say("Even if they're just reinforcements, it's not going to be easy, so stay on guard. We'll have to time our attack carefully so we don't scare them off.",
                 "Ran",
                 "Ran")
        self.say("Then right at the last possible moment, we launch our attack.",
                 "Keine",
                 "Keine")
        self.say("Very well. Let's follow Ran's plan. We'll annihilate the reinforcements, and Kotone will have no backup to rely on when we finally fight her at Alice's house.",
                 "Youmu",
                 "Youmu")
        self.say("Seriously, Marisa. Quit worrying about Alice. She'll be fine. We'll be heading there immediately after anyway, and it's just a waste of energy.",
                 "Reimu",
                 "Reimu")
        self.emote('Marisa', 'dotdotdot')


        # Rest of the enemy team arrives
        self.fade_to_color('black', 1)
        self.deploy_unit('Cosmic Fairy', (13, 21))
        self.deploy_unit('Ninja Fairy', (10, 23))
        self.deploy_unit('Sealing Fairy', (12, 23))

        self.deploy_unit('Healer Fairy C', (14, 5))
        self.deploy_unit('Walking Tree D', (12, 5))
        self.deploy_unit('Walking Tree E', (12, 6))
        self.deploy_unit('Walking Tree F', (12, 7))
        self.deploy_unit('Walking Tree G', (16, 5))
        self.deploy_unit('Walking Tree H', (16, 6))
        self.deploy_unit('Walking Tree I', (16, 7))

        self.fade_from_color('black', 1)

        self.center_on('Fairy Captain')
        self.emote('Fairy Captain', 'annoyed')
        self.say("Finally, you're here! You certainly took your time, Healer.",
                 "Fairy Captain",
                 "Fairy")
        self.say("Don't blame me, Captain. Haruna took ages getting up out of hibernation, and then after that she had to wake all her trees up! Slowly, I might add.",
                 "Healer Fairy",
                 "Healer Fairy")
        self.say("Never mind. I don't have the patience to listen to your excuses.",
                 "Fairy Captain",
                 "Fairy")
        self.say("We're together now. We have your group, the Five Fantastic Forest Fairies, and the weasels. That's all that's important right now. Let's join up with Kotone as planned.",
                 "Fairy Captain",
                 "Fairy")

        # Fairy units introduce themselves: introduction of a bunch of status effects
        self.set_cursor_state(True)
        self.center_on('Cosmic Fairy')
        self.say("Oh! Finally, we get to do some fighting!",
                  'Cosmic Fairy', 'Fairy')
        self.center_on('Ninja Fairy')
        self.say("Everyone's confident in their abilities, I hope?",
                  'Ninja Fairy', 'Fairy')

        self.center_on('Dazzling Fairy')
        self.startle('Dazzling Fairy')
        self.emote('Dazzling Fairy', 'exclamation')
        self.say("Absolutely, boss! My magic will have them spinning! They'll never be able to aim properly again!",
                  'Dazzling Fairy', 'Fairy')

        self.center_on('Sealing Fairy')
        self.startle('Sealing Fairy')
        self.emote('Sealing Fairy', 'exclamation')
        self.say("I'll suck their spiritual power right out of them.",
                 'Sealing Fairy', 'Fairy')

        self.center_on('Toxic Fairy')
        self.startle('Toxic Fairy')
        self.emote('Toxic Fairy', 'exclamation')
        self.say("I've got my combination of potent poisonous potions at the ready.",
                 'Toxic Fairy', 'Fairy')

        self.center_on('Cosmic Fairy')
        self.startle('Cosmic Fairy')
        self.emote('Cosmic Fairy', 'exclamation')
        self.say("I've swiped a special spell that the Fuzzballs developed: a blast of light that'll leave anyone stunned for minutes.",
                  'Cosmic Fairy', 'Fairy')

        self.center_on('Ninja Fairy')
        self.startle('Ninja Fairy')
        self.emote('Ninja Fairy', 'exclamation')
        self.say("And I'm going to rain my daggers at their feet. That'll slow 'em to a crawl!",
                 'Ninja Fairy', 'Fairy')


        self.center_on('Youmu')
        self.set_cursor_state(False)
        self.say("Is it...Now?",
                 "Youmu",
                 "Youmu")
        self.say("Now! We'll hit them right as they're getting ready to move!",
                 "Ran",
                 "Ran")
        self.say("Understood! Everyone attack!",
                 "Youmu",
                 "Youmu")

        # Enemy units move into position in response
        self.center_on('Fairy Captain')
        self.say("No! We're under attack?! What rotten luck. Hey, you lot! I need some of the spell fairies up by the weasels! And you two walking trees! Go defend from the south! Am I clear?",
                 "Fairy Captain",
                 "Fairy")
        self.move_unit('Walking Tree F', (12, 10))
        self.move_unit('Walking Tree I', (16, 10))

        self.say("Come on! Move! All of you, move!",
                 "Fairy Captain",
                 "Fairy")

        self.move_unit('Walking Tree F', (12, 12))
        self.move_unit('Walking Tree I', (16, 12))

        self.say("Ugh, these idiots just won't listen! If only my status were equal to a Kodama's, then they'd finally listen!",
                 "Fairy Captain",
                 "Fairy")

        self.fade_to_color('black', 1)


        self.set_unit_pos('Walking Tree D', (10, 8))
        self.set_unit_pos('Walking Tree E', (11, 7))
        self.set_unit_pos('Fairy Captain', (12, 7))
        self.set_unit_pos('Healer Fairy C', (13, 7))
        self.set_unit_pos('Walking Tree G', (14, 7))
        self.set_unit_pos('Walking Tree H', (15, 8))


        self.set_unit_pos('Walking Tree F', (15, 25))
        self.set_unit_pos('Walking Tree I', (13, 27))
        self.set_unit_pos('Cosmic Fairy', (22, 9))
        self.set_unit_pos('Sealing Fairy', (24, 9))

        self.fade_from_color('black', 1)

        self.say("I sure hope we can hold up. I'd hate to have to face Kotone after losing all our reinforcements.",
                 "Fairy Captain",
                 "Fairy")
        self.center_on_coords((27, 23))


        self.set_cursor_state(True)
        self.set_stats_display(True)

class Turn2MAE(MapActionEvent):

    def __init__(self):
        trigger_list = [
            TurnNumTrigger(2),
            UnitAliveTrigger('Fairy Captain', True),
            UnitAliveTrigger('Healer Fairy C', True)
        ]
        MapActionEvent.__init__(self, trigger_list)

    def execute(self):

        # Fairy captain being confident in her units

        self.center_on('Fairy Captain')
        self.say("Ha! I worried for nothing, after all. They look weak.",
                 "Fairy Captain",
                 "Fairy")
        self.say("Um, I wouldn't be so sure. I've heard rumors of a sorcerer that can level an entire forest from halfway across Gensokyo! And guess what? She's with them!",
                 "Healer Fairy",
                 "Healer Fairy")
        self.emote('Fairy Captain', 'exclamation')
        self.say("What?! You've got to be joking! Someone like that couldn't possibly exist! Of all the rotten--",
                 "Fairy Captain",
                 "Fairy")


class Turn6MAE(MapActionEvent):

    def __init__(self):
        trigger_list = [
            TurnNumTrigger(6),
            UnitAliveTrigger('Fairy Captain', True),
            UnitAliveTrigger('Healer Fairy C', True)
        ]
        MapActionEvent.__init__(self, trigger_list)

    def execute(self):


        # Fairy captain commenting on how hard it is to run the show without a Kodama Lord

        self.center_on('Fairy Captain')
        self.say("Walking trees! Halt! No! Don't go there!",
                 "Fairy Captain",
                 "Fairy")
        self.emote('Fairy Captain', 'annoyed')
        self.say("Argh! What are you doing?! I said halt! Don't attack her yet!",
                 "Fairy Captain",
                 "Fairy")
        self.say("Haha, things would move so much more smoothly if we had a Kodama Lord leading us instead.",
                 "Healer Fairy",
                 "Healer Fairy")
        self.say("...I hate to admit it, but you're absolutely right. This is considerably more frustrating than I was expecting. Haha...Captain, am I?",
                 "Fairy Captain",
                 "Fairy")




class FiveFairiesDeadMAE(MapActionEvent):

    def __init__(self):
        trigger_list = [
            UnitAliveTrigger('Fairy Captain', True),
            UnitAliveTrigger('Ninja Fairy', False),
            UnitAliveTrigger('Cosmic Fairy', False),
            UnitAliveTrigger('Dazzling Fairy', False),
            UnitAliveTrigger('Toxic Fairy', False),
            UnitAliveTrigger('Sealing Fairy', False)
        ]
        MapActionEvent.__init__(self, trigger_list)

    def execute(self):

        # All five fairies are defeated. FC expresses her disbelief

        self.center_on('Fairy Captain')
        self.say("What? They defeated the five fairies? Curses! What now!",
                 "Fairy Captain",
                 "Fairy")


class PostMissionMAE(MapActionEvent):

    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.remove_all_enemies()
        self.stop_music()

        self.set_unit_pos('Youmu', (14, 6))

        self.set_unit_pos('Ran', (13, 8))
        self.set_unit_pos('Reimu', (14, 8))
        self.set_unit_pos('Marisa', (15, 8))
        self.set_unit_pos('Keine', (15, 9))
        self.set_unit_pos('Chen', (13, 9))

        self.set_unit_pos('Fairy Captain', (13, 2))

    def execute(self):

        # Fairy Captain withdraws from battle map ahead of hero party

        self.center_on('Fairy Captain')
        self.say("No way! They got all of us?! That's--no...I must warn Kotone!",
                'Fairy Captain',
                'Fairy')
        self.move_unit('Fairy Captain', (13, -1))
        self.kill_unit('Fairy Captain')

        self.center_on('Marisa')
        self.say("No time to lose! We're right behind ya!",
                'Marisa',
                'Marisa')
