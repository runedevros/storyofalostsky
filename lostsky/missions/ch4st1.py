__author__ = 'Fawkes'
from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, SSPStateTrigger, ArrivalTrigger, TurnNumTrigger
from lostsky.battle.mapobj import LightSource, SpiritSourcePoint

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'Youkai in the Mist'
        location = 'Southern Thicket'
        id_string = 'CH4ST1'
        prereqs = ['CH3ST6']
        show_rewards = True
        desc = "We enter the Bamboo Forest within the veil of an impenetrable fog. The sound of the constant stomping of walking trees echoes in the distance, interspersed with cracking groans of frustration as their roots are caught in the clever rabbits' traps. Steadily, steadily, the Kodama forces advance deeper into the Bamboo Forest."

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch4st1.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat All',
                     'desc':'Defeat All Enemies'
                     }

        deploy_data = {'enable':True,
                       'max_units':18,
                       'preset_units':{},
                       'default_locations':{'Youmu':(16,14),
                                            'Ran':(15,15),
                                            'Chen':(16,15),
                                            'Aya':(17,15),
                                            'Reimu':(15,16),
                                            'Marisa':(17,16),
                                            'Keine':(15,17),
                                            'Mokou':(17,17),
                                            'Alice':(16,16),
                                               },
                       'boxes':[(15, 14, 3, 6)]
                       }


        reward_list = [('spell_action', 'Dagger Throw'),
                       ('treasure', 'synth_wood'),
                       ('treasure', 'synth_earth'),


                   ]


        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree A',
                                    'level': 16
                                },
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree B',
                                    'level': 16
                                },
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree C',
                                    'level': 16
                                },
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree D',
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
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 16
                                },
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 16
                                },
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 16
                                },
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy D',
                                    'level': 16
                                },
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly A',
                                    'level': 16
                                },
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly B',
                                    'level': 16
                                },
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly C',
                                    'level': 16
                                },
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly D',
                                    'level': 16
                                },


                           {'template_name': 'Kodama Lord',
                                'unit_name': 'Kodama Lord',
                                    'level': 16
                                },
                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Messenger Fairy',
                                    'level': 16
                                },




                            ]

        initial_spells = {'Cursed Tree A':['Poison Dust'],
                          'Cursed Tree B':['Spirit Break'],
                          'Cursed Tree C':['Poison Dust'],
                          'Cursed Tree D':['Spirit Break'],
                          'Walking Tree A':['Leaf Crystal'],
                          'Walking Tree B':['Leaf Crystal'],
                          'Walking Tree C':['Leaf Crystal'],
                          'Firefly A':['Fireball'],
                          'Firefly B':['Poison Dust'],
                          'Firefly C':['Poison Dust'],
                          'Firefly D':['Fireball'],
                          'Fairy A':['Holy Amulet'],
                          'Fairy B':['Holy Amulet'],
                          'Fairy C':['Holy Amulet'],
                          'Fairy D':['Holy Amulet'],

                            }
        initial_traits = {'Cursed Tree A':['Fog Veil', "Move+ Lv.2"],
                          'Cursed Tree B':['Fog Veil', "Move+ Lv.2"],
                          'Cursed Tree C':['Fog Veil', "Move+ Lv.2"],
                          'Cursed Tree D':['Fog Veil', "Move+ Lv.2"],
                          'Firefly A':['Flight'],
                          'Firefly B':['Flight'],
                          'Firefly C':['Flight'],
                          'Firefly D':['Flight'],
        }
        initial_ai_states = {'Cursed Tree A':'Defend',
                             'Cursed Tree B':'Attack',
                             'Cursed Tree C':'Attack',
                             'Cursed Tree D':'Attack',
                             'Walking Tree A':'Attack',
                             'Walking Tree B':'Attack',
                             'Walking Tree C':'Attack',
                             'Firefly A':'Attack',
                             'Firefly B':'Attack',
                             'Firefly C':'Attack',
                             'Firefly D':'Attack',
                             'Fairy A':'Defend',
                             'Fairy B':'Defend',
                             'Fairy C':'Defend',
                             'Fairy D':'Defend',
                             'Kodama Lord':'Attack',
                             'Messenger Fairy':'Defend',

#
                            }
        initial_locations = {'Cursed Tree A':(16, 5),

                             'Fairy A':(13, 2),
                             'Fairy B':(14, 5),
                             'Fairy C':(18, 5),
                             'Fairy D':(19, 2),

                             'Cursed Tree B':(30, 4),
                             'Cursed Tree C':(31, 5),
                             'Cursed Tree D':(32, 6),
                             'Walking Tree A':(28, 13),
                             'Walking Tree B':(29, 12),
                             'Walking Tree C':(30, 13),

                             'Firefly A':(2, 2),
                             'Firefly B':(2, 4),
                             'Firefly C':(4, 2),
                             'Firefly D':(4, 4),

                             'Kodama Lord':(16, 3),

                             'Aya':(2, 6),
                             'Marisa':(2, 7),

                            'Youmu':(16,14),
                            'Ran':(15,15),
                            'Chen':(16,15),
                            'Reimu':(15,16),
                            'Keine':(15,17),
                            'Mokou':(17,17),

                             }
        reserve_units = ['Messenger Fairy']
        all_landmarks = [
                         {'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(3, 3)},]

        required_starters = ['Aya', 'Marisa', 'Youmu', 'Keine', 'Ran', 'Chen', 'Reimu', 'Mokou',]
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [CenterLampSwitchOn(), CenterLampSwitchOff(), TreasureFoundMAE(), AwakenCursedTrees()]
        required_survivors = ['Aya', 'Marisa', 'Youmu', 'Keine', 'Ran', 'Chen', 'Reimu', 'Mokou',]
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
        self.set_bg_overlay('Night')
        self.set_stats_display(False)

        self.play_music('battle03')

        self.set_status_effect('Cursed Tree A', 'Fog Veil')
        self.set_status_effect('Cursed Tree B', 'Fog Veil')
        self.set_status_effect('Cursed Tree C', 'Fog Veil')
        self.set_status_effect('Cursed Tree D', 'Fog Veil')

        self.set_fog_state(True)
        self.map.add_light_source(LightSource('Lantern 1', (13,4), False, 5))
        self.map.add_light_source(LightSource('Lantern 2', (19,4), False, 5))
        self.map.add_light_source(LightSource('Lantern 3', (32,8), True, 3))
        self.map.add_ssp(SpiritSourcePoint('Center Lanterns', (16, 4), 2))

        self.center_on('Marisa')


        self.say('What the heck, Aya! How are you flying in this fog? I almost crashed three times trying.',
                 'Marisa',
                 'Marisa')
        self.say('I\'m a reporter, remember? When your job is flying around taking tricky pictures, a keen eye and quick reflexes comes in handy.',
                 'Aya',
                 'Aya')
        self.say("All right, I can barely make this out, but... Four fireflies here, a bunch of trees out east. Yikes. I think that's enough to say the Bamboo Forest seems to have already been overrun by the Kodummies.",
                 'Marisa',
                 'Marisa')
        self.say("You know it. Just getting to Eientei will be really hard. Well... On to the next area?",
                 'Aya',
                 'Aya')

        self.show_chapter_title(4)

        self.move_unit('Aya', (10, 8))
        self.move_unit('Marisa', (11, 9))

        self.center_on('Kodama Lord')


        # Kodama Lord struggles with controlling Ayaka's cursed trees.
        self.say('You there! Get with the other trees! I said the eastern part of this forest!',
                 'Kodama Lord',
                 'Kodama')

        self.emote('Cursed Tree A', 'annoyed')

        self.play_sfx('miss')
        self.move_unit('Cursed Tree A', (16, 3))
        self.play_sfx('hit')
        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)
        self.move_unit('Cursed Tree A', (16, 5))
        self.emote('Kodama Lord', 'scribble')
        self.say('Ayaka\'s cursed trees may be invulnerable in her fog, but they\'re absolutely impossible to control.',
                 'Kodama Lord',
                 'Kodama')
        self.emote('Kodama Lord', 'exclamation')
        self.say('She told us never to use these unless we needed to, but... Well! I do!',
                 'Kodama Lord',
                 'Kodama')

        self.emote('Kodama Lord', 'dotdotdot')


        self.move_unit('Kodama Lord', (16, 4))
        self.set_ssp_state('Center Lanterns', 1)
        self.set_lantern_state('Lantern 1', True)
        self.set_lantern_state('Lantern 2', True)

        self.say('That\'s more like it! No fog, no problem!',
                 'Kodama Lord',
                 'Kodama')

        self.play_sfx('miss')
        self.move_unit('Kodama Lord', (16, 5))
        self.move_unit('Kodama Lord', (16, 5))
        self.play_sfx('hit')
        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)
        self.move_unit('Kodama Lord', (16, 4))

        self.say('Now move!',
                 'Kodama Lord',
                 'Kodama')

        self.move_unit('Kodama Lord', (16, 3))
        self.set_ssp_state('Center Lanterns', 2)
        self.set_lantern_state('Lantern 1', False)
        self.set_lantern_state('Lantern 2', False)


        self.play_sfx('camera')
        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)

        self.say('Gotcha!',
                 'Aya',
                 'Aya')

        self.play_sfx('camera')
        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)

        self.say("That was a front page worthy shot, if I do say so myself! I knew Nitori's Fog-Vision camera would come in handy!",
                 'Aya',
                 'Aya')
        self.say("There we have it. That's the last of the Kodama forces in this region. Let's head back to Youmu.",
                 'Aya',
                 'Aya')

        self.center_on('Youmu')
        self.move_unit('Aya', (15, 13))
        self.move_unit('Marisa', (17, 13))

        self.say('Aya! Marisa!',
                 'Youmu',
                 'Youmu')
        self.say("What a pain in the neck. Next time, you're on scouting duty, Reimu.",
                 'Marisa',
                 'Marisa')
        self.say("Sorry, but espionage and recon ain't my thing. Suck it up, Marisa",
                 'Reimu',
                 'Reimu')
        self.say("She has a point. You and Aya have the best chance of escaping if you're caught, so you're our best candidates.",
                 'Ran',
                 'Ran')
        self.say("So? Did you find anything useful?",
                 'Ran',
                 'Ran')
        self.say("Kodama Lords have their usual forces around: walking trees, fireflies, fairies.",
                 'Aya',
                 'Aya')
        self.say("And as luck would have it, we spied a spirit source point that can drive away the fog!",
                 'Marisa',
                 'Marisa')
        self.say("Thanks for your work. That'll help a lot. Our aim is severely hampered by this fog.",
                 'Ran',
                 'Ran')
        self.say("I can still use my support spells luckily. Although for most skills, I suggest switching to homing for this battle.",
                 'Keine',
                 'Keine')
        self.say("By the way. There's too many of us to sneak around so don't bother.",
                 'Mokou',
                 'Mokou')
        self.say("Understood. Let's clear the area out.",
                 'Youmu',
                 'Youmu')

        self.center_on('Kodama Lord')

        self.deploy_unit('Messenger Fairy', (16, -1))
        self.move_unit('Messenger Fairy', (16, 2))

        self.startle('Messenger Fairy')
        self.say("Excuse me! Ayaka's summoning you.",
                 'Messenger Fairy',
                 'Healer Fairy')
        self.say("Any idea what it's about?",
                 'Kodama Lord',
                 'Kodama')
        self.say("We found Eientei. She's going to set up the plan.",
                 'Messenger Fairy',
                 'Healer Fairy')
        self.say("Oh? Well, I sure am looking forward to this battle!",
                 'Kodama Lord',
                 'Kodama')
        self.move_unit('Messenger Fairy', (16, -1))
        self.move_unit('Kodama Lord', (16, -1))

        self.kill_unit('Messenger Fairy')
        self.kill_unit('Kodama Lord')

        self.center_on('Youmu')

        self.set_cursor_state(True)
        self.set_stats_display(True)


class AwakenCursedTrees(MapActionEvent):

    def __init__(self):

        triggers = [TurnNumTrigger(4)]
        MapActionEvent.__init__(self, triggers, repeat=False)

    def execute(self):
        """
        Sets Eastern Cursed trees group to pursuit mode after 4 turns
        """
        for unit_name in ('Cursed Tree B', 'Cursed Tree C', 'Cursed Tree D'):
            if unit_name in self.map.all_units_by_name.keys():
                self.set_ai_state(unit_name, 'Pursuit')

class TreasureFoundMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((3, 3, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Player has discovered treasure under cherry blossom tree
        """

        self.say("Buried at the foot of the cherry tree is a small rusted box.",
                None,
                None)
        self.say("Acquired Treasure Item: Parasol!",
                None,
                None)
        self.add_item('treasure', '006_parasol', 1)

class CenterLampSwitchOn(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('Center Lanterns', 1)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if not self.map.all_landmarks['Lantern 1'].lit:
            self.map.all_landmarks['Lantern 1'].switch_state(True)
        if not self.map.all_landmarks['Lantern 2'].lit:
            self.map.all_landmarks['Lantern 2'].switch_state(True)


class CenterLampSwitchOff(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('Center Lanterns', 2)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if self.map.all_landmarks['Lantern 1'].lit:
            self.map.all_landmarks['Lantern 1'].switch_state(False)
        if self.map.all_landmarks['Lantern 2'].lit:
            self.map.all_landmarks['Lantern 2'].switch_state(False)


class PostMissionMAE(MapActionEvent):
    def __init__(self):
        # Triggers on turn 2
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.remove_all_enemies()
        self.set_unit_pos('Youmu', (16, 3))
        self.set_unit_pos('Ran', (13, 4))
        self.set_unit_pos('Chen', (13, 5))

        self.set_unit_pos('Reimu', (15, 4))
        self.set_unit_pos('Marisa', (16, 5))
        self.set_unit_pos('Aya', (17, 4))

        self.set_unit_pos('Keine', (19, 4))
        self.set_unit_pos('Mokou', (19, 5))

        self.set_ssp_state('Center Lanterns', 1)
        self.set_lantern_state('Lantern 1', True)
        self.set_lantern_state('Lantern 2', True)

    def execute(self):
        self.center_on('Youmu')
        self.say("Which way is it to Eientei?", 'Youmu', "Youmu")

        self.move_unit('Mokou', (19, 1))
        self.startle('Mokou')
        self.say("This way. I fight Kaguya there so often, I can find it in my sleep.", 'Mokou', "Mokou")
