from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, TurnNumTrigger, ArrivalTrigger, UnitAliveTrigger

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'Lost Sky Crisis'
        location = 'Graveyard'
        id_string = 'CH2ST3'
        prereqs = ['CH2ST2']
        show_rewards = False
        desc = "Lately, there have been sightings of a wayward Kodama at the village graveyard. There are rumors in the village that the Kodama are looking for a relic hidden away there."
        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch2st3v3.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat Boss',
                     'target':'Miu',
                     'desc':'Defeat Miu to escape!'
                     }

        deploy_data = {'enable':True,
                       'max_units':8,
                       'preset_units':{},
                       'boxes':[(10, 9, 5, 2)],
                       'default_locations':{'Youmu':(14,10),
                                            'Ran':(14,9),
                                            'Chen':(13,10),
                                            'Reimu':(10,9),
                                            'Keine':(11,10),
                                            'Marisa':(12,9),
                                            'Mokou':(10,10),
                                            'Alice':(12,10)
                                            },
                       }
        reward_list = [('spell_action', 'Rice Cake'),
                       ('treasure', 'synth_fire'),
                       ('treasure', 'synth_water'),
                       ('treasure', 'synth_earth')
                       ]

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Fuyuhana',
                                'unit_name': 'Fuyuhana',
                                    'level': 30},
                           # Kodama Lord Kotone's group
                           {'template_name': 'Kotone',
                                'unit_name': 'Kotone',
                                    'level': 8},
                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy A',
                                    'level': 5},
                           {'template_name': 'Firefly',
                            'unit_name': 'Firefly A',
                            'level': 6},
                           {'template_name': 'Firefly',
                            'unit_name': 'Firefly B',
                            'level': 6},

                           {'template_name': 'Firefly',
                            'unit_name': 'Firefly C',
                            'level': 6},
                           {'template_name': 'Firefly',
                            'unit_name': 'Firefly D',
                            'level': 6},

                           # Kodama Lord Ayaka's group
                           {'template_name': 'Ayaka',
                                'unit_name': 'Ayaka',
                                    'level': 13},
                           {'template_name': 'Cursed Tree',
                            'unit_name': 'Cursed Tree A',
                            'level': 12},
                           {'template_name': 'Cursed Tree',
                            'unit_name': 'Cursed Tree B',
                            'level': 12},
                           {'template_name': 'Cursed Tree',
                            'unit_name': 'Cursed Tree C',
                            'level': 12},
                           {'template_name': 'Cursed Tree',
                            'unit_name': 'Cursed Tree D',
                            'level': 12},
                           {'template_name': 'Cursed Tree',
                            'unit_name': 'Cursed Tree E',
                            'level': 12},



                           # Kodama Lord Haruna's Group
                           {'template_name': 'Haruna',
                                'unit_name': 'Haruna',
                                    'level': 8},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 5},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 5},

                           # Central Island Group
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 5},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 5},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 5},

                           # Kodama Lord Miu's exit guard group
                           {'template_name': 'Miu',
                                'unit_name': 'Miu',
                                    'level': 8},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree D',
                                    'level': 6},
                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy B',
                                    'level': 6},

                           # Reinforcement group
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 6},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy D',
                                    'level': 6},

                          ]

        initial_spells = {'Fuyuhana':['Leaf Crystal'],
                          'Kotone':['Fireball'],
                          'Ayaka':['Dagger Throw'],
                          'Haruna':['Holy Amulet'],
                          'Miu':['Holy Amulet'],

                          'Walking Tree A':['Leaf Crystal'],
                          'Walking Tree B':['Leaf Crystal'],
                          'Walking Tree C':['Leaf Crystal'],
                          'Walking Tree D':['Leaf Crystal'],


                          'Fairy A':['Fireball'],
                          'Fairy B':['Fireball'],
                          'Cursed Tree A':['Poison Dust'],
                          'Cursed Tree B':['Poison Dust'],
                          'Cursed Tree C':['Poison Dust'],
                          'Cursed Tree D':['Leaf Crystal'],
                          'Cursed Tree E':['Leaf Crystal'],

                          'Fairy C':['Dagger Throw'],
                          'Fairy D':['Dagger Throw'],

                          'Healer Fairy A':['Healing Drop'],
                          'Healer Fairy B':['Healing Drop'],

                          'Firefly A':['Fireball'],
                          'Firefly B':['Poison Dust'],
                          'Firefly C':['Poison Dust'],
                          'Firefly D':['Fireball']

                          }
        initial_traits = {'Healer Fairy A':['Move+ Lv.1', 'Flight'],
                          'Healer Fairy B':['Move+ Lv.1', 'Flight'],
                          'Firefly A':['Flight'],
                          'Firefly B':['Flight'],
                          'Firefly C':['Flight'],
                          'Firefly D':['Flight'],
                          'Cursed Tree A':['Move+ Lv.2', 'Mirage'],
                          'Cursed Tree B':['Move+ Lv.2', 'Mirage'],
                          'Cursed Tree C':['Move+ Lv.2', 'Mirage'],
                          'Cursed Tree D':['Move+ Lv.2', 'Mirage'],
                          'Cursed Tree E':['Move+ Lv.2', 'Mirage'],


                          'Ayaka':['Mirage','Mist Field'],
                          'Haruna':['Danmaku Sniper', 'Tactician'],
                          'Miu':['Flight']
                          }
        initial_ai_states = {'Kotone':'Defend',
                             'Ayaka':'Pursuit',
                             'Haruna':'Defend',
                             'Miu':'Defend',

                             'Walking Tree A':'Defend',
                             'Walking Tree B':'Defend',
                             'Walking Tree C':'Attack',
                             'Walking Tree D':'Attack',

                             'Fairy A':'Defend',
                             'Fairy B':'Defend',
                             'Cursed Tree A':'Pursuit',
                             'Cursed Tree B':'Pursuit',
                             'Cursed Tree C':'Pursuit',
                             'Cursed Tree D':'Pursuit',
                             'Cursed Tree E':'Pursuit',
                             'Fairy C':'Attack',
                             'Fairy D':'Attack',

                             'Firefly A':'Defend',
                             'Firefly B':'Defend',
                             'Firefly C':'Defend',
                             'Firefly D':'Defend',

                             'Healer Fairy A':'HealerStandby',
                             'Healer Fairy B':'HealerStandby'

                             }
        initial_locations = {'Keine':(-1, -1),
                             'Youmu':(-1, -1),
                             'Ran':(-1, -1),
                             'Chen':(-1, -1),
                             'Reimu':(-1, -1),
                             'Marisa':(-1, -1),
                             'Ayaka':(12, 5)

                             }
        reserve_units = ['Fuyuhana',
                         'Kotone',
                         'Haruna',
                         'Miu',
                         'Cursed Tree D',
                         'Cursed Tree E',
                         'Walking Tree A',
                         'Walking Tree B',
                         'Walking Tree C',
                         'Walking Tree D',
                         'Fairy A',
                         'Fairy B',
                         'Cursed Tree A',
                         'Cursed Tree B',
                         'Cursed Tree C',
                         'Fairy C',
                         'Fairy D',
                         'Firefly A',
                         'Firefly B',
                         'Firefly C',
                         'Firefly D',
                         'Healer Fairy A',
                         'Healer Fairy B',
                         ]


        all_landmarks = [{'name':'GS1',
                          'id_string':'tombstone',
                          'location':(4, 10)},
                          {'name':'GS2',
                          'id_string':'tombstone',
                          'location':(6, 10)},
                          {'name':'GS3',
                          'id_string':'tombstone',
                          'location':(6, 8)},
                          {'name':'GS4',
                          'id_string':'tombstone',
                          'location':(4, 8)},
                          {'name':'GS5',
                          'id_string':'tombstone',
                          'location':(4, 6)},
                          {'name':'GS6',
                          'id_string':'tombstone',
                          'location':(6, 6)},
                          {'name':'GS7',
                          'id_string':'tombstone',
                          'location':(11, 6)},
                          {'name':'GS8',
                          'id_string':'tombstone',
                          'location':(13, 6)},
                          {'name':'GS9',
                          'id_string':'tombstone',
                          'location':(11, 8)},
                          {'name':'GS10',
                          'id_string':'tombstone',
                          'location':(13, 8)},
                          {'name':'GS11',
                          'id_string':'tombstone',
                          'location':(11, 10)},
                          {'name':'GS12',
                          'id_string':'tombstone',
                          'location':(13, 10)},
                          {'name':'GS13',
                          'id_string':'tombstone',
                          'location':(18, 6)},
                          {'name':'GS14',
                          'id_string':'tombstone',
                          'location':(20, 6)},
                          {'name':'GS15',
                          'id_string':'tombstone',
                          'location':(18, 8)},
                          {'name':'GS16',
                          'id_string':'tombstone',
                          'location':(20, 8)},
                          {'name':'GS17',
                          'id_string':'tombstone',
                          'location':(18, 10)},
                          {'name':'GS18',
                          'id_string':'tombstone',
                          'location':(20, 10)},

                          {'name':'Mini Shrine',
                          'id_string':'minishrine',
                          'location':(12, 3)},
                          {'name':'CB0',
                          'id_string':'cherryblossom_tree',
                          'location':(11, 3)},
                          {'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(13, 3)},

                          {'name':'CB2',
                          'id_string':'cherryblossom_tree',
                          'location':(9, 25)},
                          {'name':'CB3',
                          'id_string':'cherryblossom_tree',
                          'location':(14, 25)},

                          {'name':'Torii',
                          'id_string':'small_torii',
                          'location':(12, 11)},
                         ]

        required_starters = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Reimu', 'Keine']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [WestTreasureMAE(), EastTreasureMAE(), MiuReinforceMAE(),
                                AyakaHarunaMAE()]
        required_survivors = ['Youmu', 'Ran', 'Chen', 'Marisa', 'Reimu', 'Keine',
                              'Mokou', 'Kotone', 'Miu', 'Haruna', 'Ayaka']
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
        Big encounter with Fuyuhana
        """
        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.play_music('battle04')

        self.add_to_party('Mokou')
        self.assign_spell('Mokou', 'Dagger Throw')
        self.assign_spell('Mokou', 'Flying Phoenix')
        self.assign_spell('Mokou', 'Rice Cake')
        self.set_unit_pos('Mokou', (12, 9))

        self.center_on('Mokou')

        self.say("Kodama Lords? There haven't been Kodama Lords in Gensokyo for generations. What's the meaning of this?",
            'Mokou',
            'Mokou')
        self.say("Haha, what indeed? Now that we've awakened, let us remind you how dangerous we are.",
            'Ayaka',
            'Ayaka')
        self.say("Fujiwara no Mokou, you are no ordinary human. Ah... I see. The same flame that tints my leaves a brilliant red burns brightly within you. ...Fascinating.",
            'Voice',
            None)
        self.say("Now. We will bind you to the sacred branch enshrined here!",
            'Ayaka',
            'Ayaka')
        self.say("The summer sun shall herald our return! The return of the Kodama Lords!",
            'Voice',
            None)

        self.fade_to_color('white', 1)
        self.deploy_unit('Fuyuhana', (12, 4))
        self.fade_from_color('white', 1)

        self.say("My lady, it has been too long. Your loyal servant, Ayaka of the Pale Mist, is ready to serve you once more!",
            'Ayaka',
            'Ayaka')
        self.say("Indeed it has. Living as a phantom was uncomfortably restricting. Now then, Ayaka. Keep her busy while I cast the cloud gathering spell.",
            'Fuyuhana',
            'Fuyuhana')
        self.say("Ha! I don't know what you're after, but right now I don't care. I have a dear friend in that village, and I'm not gonna let you near her without a fight.",
            'Mokou',
            'Mokou')

        self.move_unit('Mokou', (12, 5))
        self.fade_to_color('white', 0.2)
        self.play_sfx('miss')
        self.set_unit_pos('Ayaka', (12, 10))
        self.fade_from_color('white', 0.2)

        self.emote('Mokou', 'questionmark')

        self.move_unit('Mokou', (12, 10))
        self.fade_to_color('white', 0.2)
        self.play_sfx('miss')
        self.set_unit_pos('Ayaka', (12, 8))
        self.fade_from_color('white', 0.2)

        self.emote('Mokou', 'scribble')

        self.say("Ugh! What's with my aim today? I can't seem to hit her!",
            'Mokou',
            'Mokou')
        self.say("Hmm...",
            'Ayaka',
            'Ayaka')

        self.set_unit_pos('Youmu', (15, 16))
        self.set_unit_pos('Ran', (15, 16))
        self.set_unit_pos('Chen', (15, 16))

        self.set_unit_pos('Marisa', (9, 16))
        self.set_unit_pos('Reimu', (9, 16))
        self.set_unit_pos('Keine', (9, 16))

        self.move_unit('Youmu', (15, 11))
        self.move_unit('Ran', (14, 12))
        self.move_unit('Chen', (16, 12))

        self.move_unit('Marisa', (9, 11))
        self.move_unit('Reimu', (8, 12))
        self.move_unit('Keine', (10, 12))


        self.say("Mokou!",
            'Keine',
            'Keine')
        self.say("So you're here. I heard about the commotion in the village and came to investigate.",
            'Mokou',
            'Mokou')
        self.say("I see. And they're the perpetrators behind this crisis!",
            'Youmu',
            'Youmu')

        self.set_invincibility_state('Ayaka', True)
        self.move_unit('Youmu', (13, 8))

        temp_spell_action = self.map.all_units_by_name['Youmu'].spell_actions[0]

        self.map.all_units_by_name['Youmu'].spell_actions[0]  = None
        self.assign_spell('Youmu', "Dagger Throw")
        self.script_battle('Youmu', 'Ayaka', {'rhs_equip':0, 'lhs_equip':0, 'lhs_hit':False, 'rhs_hit':True, 'lhs_crit':False, 'rhs_crit':False})
        self.map.all_units_by_name['Youmu'].spell_actions[0]  =  temp_spell_action

        self.emote('Youmu', 'scribble')


        self.say("Having trouble? Lemme give it a shot!",
            'Marisa',
            'Marisa')

        self.move_unit('Marisa', (9, 8))

        temp_spell_action = self.map.all_units_by_name['Marisa'].spell_actions[0]

        self.set_spirit_charge('Marisa', 500)
        self.map.all_units_by_name['Marisa'].spell_actions[0]  = None
        self.assign_spell('Marisa', "Master Spark")
        self.script_battle('Marisa', 'Ayaka', {'rhs_equip':0, 'lhs_equip':0, 'lhs_hit':False, 'rhs_hit':False, 'lhs_crit':False, 'rhs_crit':False})
        self.map.all_units_by_name['Marisa'].spell_actions[0]  =  temp_spell_action

        self.emote('Marisa', 'questionmark')


        self.say("Huh? No way! Even Master Spark missed!",
            'Marisa',
            'Marisa')
        self.say("She dodged it so effortlessly.",
            'Youmu',
            'Youmu')
        self.say("Thank you. You've provided me sufficient time, Ayaka. The spell is ready.",
            'Fuyuhana',
            'Fuyuhana')

        self.fade_to_color('white', 0.5)
        self.show_image('clouds001', 'sky001.jpg', (0, 0))
        self.fade_from_color('white', 0.5)


        self.say("Ah! Look! The sky is--!",
            'Chen',
            'Chen')

        # Show image of sky with clouds -> sky without clouds
        self.fade_to_color('white', 0.5)
        self.hide_image('clouds001')
        self.show_image('clouds002', 'sky002.jpg', (0, 0))
        self.fade_from_color('white', 0.5)

        self.say("How... The clouds... They've vanished!",
            'Keine',
            'Keine')

        self.fade_to_color('white', 0.5)
        self.hide_image('clouds002')
        self.fade_from_color('white', 0.5)

        self.say("What is she planning? Does she intend to steal away Gensokyo's rain?",
            'Ran',
            'Ran')
        self.say("We Kodama Lords have long been protectors of the forest, but after centuries of our absence, it's clear that this land, or rather, the entirety of Gensokyo, requires our leadership. We shall rule Gensokyo!",
            'Fuyuhana',
            'Fuyuhana')
        self.say("Haha, oh, please. We don't need or want you high and mighty types bossing us around!",
            'Marisa',
            'Marisa')
        self.say("I am returning to the sanctuary. Ayaka, I expect to find these nuisances utterly destroyed before we meet again.",
            'Fuyuhana',
            'Fuyuhana')
        self.say("Yes. Your wish is my command...my lady.",
            'Ayaka',
            'Ayaka')




        # Ayaka's Party Deploys
        self.move_unit('Ayaka', (12, 3))

        self.fade_to_color('white', 0.5)
        self.kill_unit('Fuyuhana')
        self.deploy_unit('Cursed Tree A', (12, 1))
        self.deploy_unit('Cursed Tree B', (10, 1))
        self.deploy_unit('Cursed Tree C', (14, 1))
        self.deploy_unit('Cursed Tree D', (11, 2))
        self.deploy_unit('Cursed Tree E', (13, 2))
        self.fade_from_color('white', 0.5)


        self.center_on('Ayaka')

        # Haruna's Party Deploys
        self.fade_to_color('white', 0.5)
        self.deploy_unit('Haruna', (5, 22))
        self.deploy_unit('Fairy A', (6, 23))
        self.deploy_unit('Fairy B', (4, 23))
        self.deploy_unit('Walking Tree A', (3, 21))
        self.deploy_unit('Walking Tree B', (7, 21))
        self.fade_from_color('white', 0.5)

        self.center_on('Haruna')
        self.emote('Haruna', 'zzz')
        self.say("Haruna!",
            'Ayaka',
            'Ayaka')
        self.say("Nnnghh...huh? Did we really have to return so early?",
            'Haruna',
            'Haruna')

        # Kotone's Group
        self.fade_to_color('white', 0.5)
        self.deploy_unit('Kotone', (18, 24))
        self.deploy_unit('Healer Fairy A', (17, 24))
        self.deploy_unit('Firefly A', (20, 19))
        self.deploy_unit('Firefly B', (15, 19))
        self.deploy_unit('Firefly C', (19, 25))
        self.deploy_unit('Firefly D', (16, 25))
        self.fade_from_color('white', 0.5)
        self.center_on('Kotone')
        self.startle('Kotone')
        self.say("Ayaka. I, Kodama Sorceress Kotone, am ready for battle! And I see Lady Ayaka has brought her prized Cursed Trees.",
            'Kotone',
            'Kotone')


        # Miu's Group
        self.fade_to_color('white', 0.5)
        self.deploy_unit('Miu', (13, 32))
        self.deploy_unit('Healer Fairy B', (13, 33))
        self.deploy_unit('Walking Tree C', (10, 33))
        self.deploy_unit('Walking Tree D', (16, 33))
        self.fade_from_color('white', 0.5)

        self.center_on('Miu')
        self.say("I'm here too! Ah...right. Ready to receive orders!",
            'Miu',
            'Miu')

        self.center_on('Youmu')

        self.say("What, just four of them? We'll gladly send them packing.",
            'Marisa',
            'Marisa')
        self.say("I've analyzed Ayaka's spiritual energy. She's protected by a magical mist barrier. Any spells we shoot at it will pass right through to the other side without harming her.",
            'Ran',
            'Ran')
        self.emote('Marisa', 'annoyed')
        self.say("Hey! That's cheating!",
            'Marisa',
            'Marisa')
        self.say("Yeah, well, I have a feeling these Kodama Lords won't play along with the one-on-one duels that we've gotten so used to having.",
            'Reimu',
            'Reimu')
        self.say("Ran! Can you tell if the others are protected, too?",
            'Mokou',
            'Mokou')
        self.say("I don't sense the same magic around them. They should be vulnerable to our usual attacks.",
            'Ran',
            'Ran')
        self.say("The one farthest away seems to be the least confident of herself, and one of them is half-asleep.",
            'Reimu',
            'Reimu')
        self.say("Let's...retreat to the human village for now.",
            'Youmu',
            'Youmu')
        self.emote('Marisa', 'scribble')
        self.say("Say what! We're going to turn tail and run?",
            'Marisa',
            'Marisa')
        self.say("Oh, get over it, Marisa. You can wait. The battle's not gonna run away from us.",
            'Reimu',
            'Reimu')
        self.say("A wise decision. We may be unable to win against Ayaka at the moment, but Akyu should be able to shed some light on our predicament.",
            'Keine',
            'Keine')
        self.say("After all, in our history exist records of the Kodama Lords' previous defeat.",
            'Keine',
            'Keine')




        self.set_cursor_state(True)
        self.set_stats_display(True)


class WestTreasureMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((9, 25, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        self.say("Buried at the foot of the cherry tree is a small rusted box.",
                None,
                None)
        self.say("Acquired Treasure Item: Lava Rock!",
                None,
                None)
        self.add_item('treasure', 'synth_fire', 1)


class EastTreasureMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((14, 25, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        self.say("Sitting at the side of the cherry tree is a cardboard box.",
                None,
                None)
        self.say("Acquired Treasure Item: Cell Phone!",
                None,
                None)
        self.add_item('treasure', '002_cellphone', 1)


class MiuReinforceMAE(MapActionEvent):

    def __init__(self):
        triggers = [TurnNumTrigger(3),
                    # Ayaka must be still alive
                    UnitAliveTrigger('Ayaka', True)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Ayaka sends reinforcements to back up Miu
        """
        self.set_stats_display(False)
        self.center_on('Ayaka')

        self.say("Miu, they're coming your way. Get ready!",
                'Ayaka',
                'Ayaka')

        self.center_on('Miu')
        self.say("Got it!",
                'Miu',
                'Miu')
        self.center_on('Ayaka')
        self.say("I'm sending some of our fairies to assist you. They may be fast, but that's a non-issue. We'll catch up to them in no time.",
                'Ayaka',
                'Ayaka')

        self.center_on('Miu')
        self.deploy_unit('Fairy D', (13, 34))
        self.move_unit('Fairy D', (11, 33))
        self.deploy_unit('Fairy C', (13, 34))
        self.move_unit('Fairy C', (15, 33))

        self.say("We'll not fail you, Lady Ayaka!",
                'Fairy',
                'Fairy')


        self.say("Well, I have to hand it to them. They're way more organized than the other morons we've recently encountered.",
                'Reimu',
                'Reimu')

        self.set_stats_display(True)


class AyakaHarunaMAE(MapActionEvent):

    def __init__(self):
        triggers = [TurnNumTrigger(5),
                    UnitAliveTrigger('Ayaka', True),
                    UnitAliveTrigger('Haruna', True)
                    ]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Ayaka + Haruna converse about old times
        """
        self.set_stats_display(False)
        self.center_on('Ayaka')
        self.say("Are you okay, Ayaka?",
                'Haruna',
                'Haruna')
        self.say("As well as can be expected. They're tough, but we have strength in numbers.",
                'Ayaka',
                'Ayaka')
        self.center_on('Haruna')
        self.say("It's been so long since we've last seen battle. It's incredible...so much has changed in this world.",
                'Haruna',
                'Haruna')
        self.center_on('Ayaka')
        self.say("It must be so strange to Miu and Kotone. Our world is almost unrecognizable from the world we saw before we went to sleep. Many new youkai have appeared as well.",
                'Ayaka',
                'Ayaka')
        self.center_on('Haruna')
        self.say("Yes... We've been estranged from the outside world for so long. I cannot help but wonder if our companions of old are even around anymore.",
                'Haruna',
                'Haruna')
        self.set_stats_display(True)


class AyakaYoumuMAE(MapActionEvent):

    def __init__(self):
        triggers = [TurnNumTrigger(7),
                    UnitAliveTrigger('Ayaka', True),
                    UnitAliveTrigger('Youmu', True),
                    UnitAliveTrigger('Chen', True)
                    ]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Ayaka talks with Youmu during their fight
        """
        self.set_stats_display(False)
        self.center_on('Ayaka')
        self.say("There you are!",
                'Ayaka',
                'Ayaka')
        self.center_on('Chen')
        self.say("Aah! Yikes! These guys are really tough!",
                'Chen',
                'Chen')
        self.center_on('Youmu')
        self.say("Don't falter! We must keep moving!",
                'Youmu',
                'Youmu')
        self.set_stats_display(True)

class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.remove_all_enemies()
        self.set_unit_pos('Youmu', (13, 34))
        self.set_unit_pos('Ran', (12, 33))
        self.set_unit_pos('Chen', (12, 32))
        self.set_unit_pos('Reimu', (13, 33))
        self.set_unit_pos('Marisa', (13, 32))
        self.set_unit_pos('Mokou', (14, 33))
        self.set_unit_pos('Keine', (14, 32))


        self.set_unit_pos('Ayaka', (15, 8))
        self.set_unit_pos('Haruna', (9, 8))
        self.set_unit_pos('Miu', (12, 10))
        self.set_unit_pos('Kotone', (12, 6))

    def execute(self):

        # Heroes escape from the scene
        self.center_on('Youmu')
        self.say("We made it!",
                'Youmu',
                'Youmu')
        self.say("Is everyone all right?",
                'Keine',
                'Keine')
        self.say("A few bruises but otherwise fine.",
                'Mokou',
                'Mokou')
        self.say("Good to hear! Let's hurry and bust out of here then.",
                'Marisa',
                'Marisa')

        self.move_unit('Youmu', (13, 36))
        self.move_unit('Ran', (13, 36))
        self.move_unit('Chen', (13, 36))
        self.move_unit('Marisa', (13, 36))
        self.move_unit('Reimu', (13, 36))
        self.move_unit('Mokou', (13, 36))
        self.move_unit('Keine', (13, 36))

        # Kodana Lords talk about their defeat
        self.center_on('Haruna')

        self.say("My apologies, Ayaka! We let them escape.",
                'Haruna',
                'Haruna')
        self.say("No. The fault is mine alone. I failed to fulfill my duty to the forest.",
                'Miu',
                'Miu')
        self.say("Miu, don't shoulder the blame yourself. We should have supported you more in that battle. If only we had more time to train you...",
                'Kotone',
                'Kotone')
        self.emote('Kotone', 'annoyed')
        self.move_unit('Haruna', (12, 8))
        self.say("Enough! You both fought hard and bravely. We cannot expect to have everything go according to plan. Feeling sorry for ourselves will get us nowhere.",
                'Haruna',
                'Haruna')
        self.startle('Kotone')
        self.say("Let me go after them!",
            'Kotone',
            'Kotone')
        self.say("No. You're exhausted, Kotone. What good will charging into their stronghold alone do?",
            'Haruna',
            'Haruna')
        self.say("Haruna is correct. We have only just awakened, and we are currently at our weakest. I propose this instead. Return to the forest and ensure that the cloud gathering is a success.",
            'Ayaka',
            'Ayaka')
        self.say("Until Fuyuhana completes the rain ceremony to strengthen the forest, we cannot guarantee its safety while we are so far away from it. I hope this is acceptable.",
            'Haruna',
            'Haruna')

        self.emote('Kotone', 'exclamation')
        self.emote('Miu', 'exclamation')
        self.say("At once!",
                'Miu and Kotone',
                None)

        self.move_unit('Kotone', (12, -1))
        self.move_unit('Haruna', (13, 8))
        self.move_unit('Miu', (12, -1))
        self.kill_unit('Kotone')
        self.kill_unit('Miu')

        self.say("Well, now. I can see that working with these new Kodama Lords will prove difficult.",
                'Ayaka',
                'Ayaka')
        self.say("As your mentor of many years, all I can offer is that you place your trust in them. We were so much like them once, so you understand, I hope.",
                'Haruna',
                'Haruna')
        self.say("Yes. I suppose you're right. You often are.",
                'Ayaka',
                'Ayaka')
        self.say("Haruna, I have an assignment for you. You are the most capable of persuading the trees to fight alongside us.",
                'Ayaka',
                'Ayaka')
        self.emote('Haruna', 'questionmark')
        self.say("Fuyuhana wants to make sure that the sacred sanctuary on Youkai Mountain is safe. Don't let the Tengu--or those heroes--anywhere near it. Will you do this for me?",
                'Ayaka',
                'Ayaka')
        self.say("I see. Very well. I'll set out with a some of our fairies immediately.",
                'Haruna',
                'Haruna')
        self.say("Thank you. I wish you the best of luck, Haruna.",
                'Ayaka',
                'Ayaka')

        self.stop_music()
        self.set_stats_display(True)
        self.set_cursor_state(False)
