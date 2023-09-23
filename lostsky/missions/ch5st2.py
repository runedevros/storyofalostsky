from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, TeamTurnTrigger, TurnNumTrigger, SSPStateTrigger, UnitAliveTrigger, UnitHPBelowTrigger, CustVarTrigger
from lostsky.battle.mapobj import SpiritSourcePoint, LightSource
from lostsky.core.linalg import Vector2
import pygame
import os
from random import choice, randint
from math import sin, cos, radians, degrees, pi

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'End of the Lost Sky'
        location = 'Central Forest'
        id_string = 'CH5ST2'
        prereqs = ['CH5ST1']
        show_rewards = True
        desc = "Youmu's party braved the rugged terrain of Youkai Mountain and drove the Kodama out from the endless maze of the Bamboo Forest. Now it's time for the final confrontation! Fuyuhana still has her final curse up her sleeve, and as the Kodama's powers have proven, this will be a much bigger challenge to contain than Ayaka's!"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch5st2.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat Boss',
                     'target':'Fuyuhana',
                     'desc':'Capture all spirit sources before 8 turns, and then defeat Fuyuhana!'
                     }

        deploy_data = {'enable':True,
                       'max_units':18,
                       'preset_units':{},
                       'default_locations':{
                                               },
                       'boxes':[(12, 22, 5, 3)]
                       }


        reward_list = []


        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'FinalFuyuhana',
                                'unit_name': 'Fuyuhana',
                                    'level': 38},
                           {'template_name': 'Kodama Lord',
                                'unit_name': 'Kodama Lord A',
                                    'level': 30},
                           {'template_name': 'Kodama Lord',
                                'unit_name': 'Kodama Lord B',
                                    'level': 30},
                           {'template_name': 'Kodama Lord',
                                'unit_name': 'Kodama Lord C',
                                    'level': 30},
                           {'template_name': 'Kodama Lord',
                                'unit_name': 'Kodama Lord D',
                                    'level': 30},


                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree A',
                                    'level': 30},
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree B',
                                    'level': 30},
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree C',
                                    'level': 30},
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree D',
                                    'level': 30},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 28},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 28},


                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 30},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 30},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 30},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy D',
                                    'level': 30},

                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy A',
                                    'level': 32},
                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy B',
                                    'level': 32},
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

                           # Second Wave
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy Captain A',
                                    'level': 34},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy Captain B',
                                    'level': 34},
                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy C',
                                    'level': 32},
                           {'template_name': 'Healer Fairy',
                                'unit_name': 'Healer Fairy D',
                                    'level': 32},
                           {'template_name': 'Kodama Lord',
                                'unit_name': 'Elite Kodama A',
                                    'level': 36},
                           {'template_name': 'Kodama Lord',
                                'unit_name': 'Elite Kodama B',
                                    'level': 36},


                            {'template_name': 'Ayaka',
                                'unit_name': 'Ayaka',
                                    'level': 30},
                            {'template_name': 'Haruna',
                                'unit_name': 'Haruna',
                                    'level': 30},
                            {'template_name': 'Miu',
                                'unit_name': 'Miu',
                                    'level': 30},
                            {'template_name': 'Kotone',
                                'unit_name': 'Kotone',
                                    'level': 30},


                            ]

        initial_spells = {'Fuyuhana':['Clouds and Sun'],
                          'Kodama Lord A':["Leaf Crystal"],
                          'Kodama Lord B':["Leaf Crystal"],
                          'Kodama Lord C':['Mystic Barrier', "Holy Amulet"],
                          'Kodama Lord D':['Mystic Barrier', "Holy Amulet"],
                          'Cursed Tree A':['Spirit Break'],
                          'Cursed Tree B':['Spirit Break'],
                          'Cursed Tree C':['Poison Dust'],
                          'Cursed Tree D':['Poison Dust'],
                          'Walking Tree A':['Leaf Crystal'],
                          'Walking Tree B':['Leaf Crystal'],

                          'Fairy A':['Encourage', 'Fireball'],
                          'Fairy B':['Encourage', 'Fireball'],
                          'Fairy C':['Illusion Veil', 'Fireball'],
                          'Fairy D':['Illusion Veil', 'Fireball'],
                          'Healer Fairy A':['Healing Drop'],
                          'Healer Fairy B':['Healing Drop'],

                          'Wind Weasel A':['Dagger Throw'],
                          'Wind Weasel B':['Dagger Throw'],
                          'Wind Weasel C':['Dagger Throw'],
                          'Wind Weasel D':['Dagger Throw'],

                          'Fairy Captain A':['Barrier Buster'],
                          'Fairy Captain B':['Weakening Amulet'],
                          'Elite Kodama A':['Pollenating Butterfly'],
                          'Elite Kodama B':['Chestnut Meteor'],
                          'Healer Fairy C':['Evergreen Branch'],
                          'Healer Fairy D':['Evergreen Branch'],



                            }
        initial_traits = {'Fuyuhana':['Magic+ Lv.2', 'Teleport', 'Holy Tree Charm'],
                          'Cursed Tree A':['Fog Veil'],
                          'Cursed Tree B':['Fog Veil'],
                          'Cursed Tree C':['Fog Veil'],
                          'Cursed Tree D':['Fog Veil'],

                          'Fairy Captain A':['Danmaku Sniper', 'Flight', 'Magic+ Lv.3'],
                          'Fairy Captain B':['Close Combat', 'Move+ Lv.2', 'Sneak', 'Magic+ Lv.3'],
                          'Elite Kodama A':['Magic+ Lv.3', 'Regen Lv.2', 'Move+ Lv.2'],
                          'Elite Kodama B':['Magic+ Lv.3', 'Regen Lv.2', 'Move+ Lv.2'],
                          'Healer Fairy C':['Flight'],
                          'Healer Fairy D':['Flight'],


                          }
        initial_ai_states = {'Fuyuhana':'Defend',
                             'Kodama Lord A':'Defend',
                             'Kodama Lord B':'Defend',
                             'Kodama Lord C':'Defend',
                             'Kodama Lord D':'Defend',

                             'Cursed Tree A':'Attack',
                             'Cursed Tree B':'Attack',
                             'Cursed Tree C':'Attack',
                             'Cursed Tree D':'Attack',
                             'Walking Tree A':'Attack',
                             'Walking Tree B':'Attack',

                             'Fairy A':'Attack',
                             'Fairy B':'Attack',
                             'Fairy C':'Attack',
                             'Fairy D':'Attack',

                             'Healer Fairy A':'HealerStandby',
                             'Healer Fairy B':'HealerStandby',

                             'Wind Weasel A':'Attack',
                             'Wind Weasel B':'Attack',
                             'Wind Weasel C':'Attack',
                             'Wind Weasel D':'Attack',

                             'Fairy Captain A':'Pursuit',
                             'Fairy Captain B':'Pursuit',
                             'Elite Kodama A':'Pursuit',
                             'Elite Kodama B':'Pursuit',
                             'Healer Fairy C':'HealerStandby',
                             'Healer Fairy D':'HealerStandby',


                            }
        initial_locations = {

                             'Fuyuhana':(14, 13),


                             'Kodama Lord A':(5, 5),
                             'Cursed Tree A':(4, 6),
                             'Cursed Tree C':(6, 6),
                             'Healer Fairy A':(5, 6),


                             'Kodama Lord B':(23, 5),
                             'Cursed Tree B':(24, 6),
                             'Cursed Tree D':(22, 6),
                             'Healer Fairy B':(23, 6),

                             'Kodama Lord C':(2, 13),
                             'Kodama Lord D':(26, 13),
                             'Fairy A':(1, 14),
                             'Fairy C':(3, 14),
                             'Fairy B':(27, 14),
                             'Fairy D':(25, 14),


                             'Walking Tree A':(5, 22),
                             'Walking Tree B':(23, 22),
                             'Wind Weasel A':(4, 23),
                             'Wind Weasel B':(6, 23),
                             'Wind Weasel C':(22, 23),
                             'Wind Weasel D':(24, 23),

                             'Reimu':(13, 16),
                             'Youmu':(14, 16),
                             'Yuyuko':(15, 16),

                             'Chen':(13, 17),
                             'Yukari':(14, 17),
                             'Ran':(15, 17),

                             'Marisa':(11, 17),
                             'Aya':(11, 18),

                             'Eirin':(13, 18),
                             'Kaguya':(14, 18),
                             'Reisen':(15, 18),

                             'Keine':(17, 17),
                             'Mokou':(17, 18)





                             }
        reserve_units = ['Fairy Captain A', 'Fairy Captain B', 'Elite Kodama A', 'Elite Kodama B', 'Healer Fairy C', 'Healer Fairy D', 'Ayaka', 'Kotone', 'Miu', 'Haruna']
        all_landmarks = [
                          {'name':'sw_gate',
                          'id_string':'small_torii',
                          'location':(5, 23)},
                          {'name':'se_gate',
                          'id_string':'small_torii',
                          'location':(23, 23)},

                          {'name':'w_gate',
                          'id_string':'small_torii',
                          'location':(2, 14)},
                          {'name':'e_gate',
                          'id_string':'small_torii',
                          'location':(26, 14)},

                          {'name':'nw_gate',
                          'id_string':'small_torii',
                          'location':(5, 6)},
                          {'name':'ne_gate',
                          'id_string':'small_torii',
                          'location':(23, 6)},


        ]

        required_starters = ['Youmu', 'Yuyuko', 'Ran', 'Chen', 'Reimu', 'Marisa', 'Yukari', 'Keine', 'Mokou', 'Aya', 'Eirin', 'Kaguya', 'Reisen']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [SE_LampSwitchOn(), SE_LampSwitchOff(), SW_LampSwitchOff(), SW_LampSwitchOn(), W_LampSwitchOff(),
                                 W_LampSwitchOn(), E_LampSwitchOff(), E_LampSwitchOn(), Phase1Countdown(), FuyuhanaPhase1Curse(),
                                 Phase2Start(), Phase3Start(), TagTarget(), FuyuhanaAoE(), Phase4Start() ]
        required_survivors = ['Youmu', 'Yuyuko', 'Ran', 'Chen', 'Reimu', 'Marisa', 'Yukari', 'Keine', 'Mokou', 'Aya', 'Eirin', 'Kaguya', 'Reisen', 'Fuyuhana']
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
        self.set_stats_display(False)
        self.set_cursor_state(False)


        ssp_list = [SpiritSourcePoint('NorthWest', (5, 5), 2), SpiritSourcePoint('SouthWest', (5, 22), 2),
                    SpiritSourcePoint('NorthEast', (23, 5), 2), SpiritSourcePoint('SouthEast', (23, 22), 2),
                    SpiritSourcePoint('East', (26, 13), 2), SpiritSourcePoint('West', (2, 13), 2),


                    ]
        for index, ssp in enumerate(ssp_list):
            self.map.add_ssp(ssp)


        self.map.add_light_source(LightSource('LightNorthEast', (25, 8), False, 5))
        self.map.add_light_source(LightSource('LightNorthWest', (3, 8), False, 5))
        self.map.add_light_source(LightSource('LightSouthEast', (26, 18), False, 5))
        self.map.add_light_source(LightSource('LightSouthWest', (2, 18), False, 5))

        self.center_on('Fuyuhana')

        self.play_music('event03')

        self.say("We're finally here. There she is.",
                 'Youmu',
                 'Youmu')
        self.say("I see. So Ayaka, Haruna, Miu, and Kotone have all been defeated. I must face you with the remaining strength of the Kodama forces.",
                 'Fuyuhana',
                 'Fuyuhana')
        self.say("It is sorrowful, but there is no time for tears. It was inevitable.",
                 'Fuyuhana',
                 'Fuyuhana')

        self.say("Can we negotiate with you instead? Like before, all those years ago?",
                 'Youmu',
                 'Youmu')

        self.say("Negotiate? Surely you jest! I bowed down and was slain before I could utter my final curse! I could not guarantee their promise was kept, that the forest would be protected!",
                 'Fuyuhana',
                 'Fuyuhana')
        self.say("For centuries, I drifted between life and death, burdened by the failure of the Kodama to ensure the forest's well being.",
                 'Fuyuhana',
                 'Fuyuhana')
        # Referring to the events of Perfect Cherry Blossom
        self.say("No, I refuse to repeat my mistakes again here. That wave of spring from all those years ago extended to me a chance to right my wrongs.",
                 'Fuyuhana',
                 'Fuyuhana')
        self.say("No, that history will never repeat again! To my dying breath, I swear to avenge those Kodama who have fallen for my cause! I will bring ruin upon your people and your lands!",
                 'Fuyuhana',
                 'Fuyuhana')


        self.say("Ok, it's our turn, Reimu. This time, we'll definitely be ready to seal up this cocky Kodama's final curse.",
                 'Yukari',
                 'Yukari')

        self.startle('Reimu')
        self.say("Fantasy Seal!",
                 'Reimu',
                 'Reimu')
        self.startle('Yukari')
        self.say("Quadruple Barrier!",
                 'Yukari',
                 'Yukari')

        self.play_sfx("support3")
        self.show_animation('sealing_spell', (14, 13))
        self.play_sfx("support1")
        self.show_animation('barrier_spell', (14, 13))

        self.play_sfx("beam2")
        self.fade_to_color('white', 2.0)
        self.set_bg_overlay('Night')
        self.set_fog_state(True)


        self.fade_from_color('white', 2.0)


        self.say("Tell me you're not surprised. I taught Ayaka her mist gathering spell when she was younger.  Remember, cloud gathering is my specialty.",
                 'Fuyuhana',
                 'Fuyuhana')
        self.say("Ayaka's curse may have been repelled by such petty tricks, but your magic cannot hope to contain mine.",
                 'Fuyuhana',
                 'Fuyuhana')
        self.say("Now, I curse all Gensokyo's flowers who dare bloom outside the protection of this forest to become naught but ash!",
                 'Fuyuhana',
                 'Fuyuhana')

        self.say("No! Ran, why didn't it work? Do you sense anything different about her magical powers?",
                 'Yukari',
                 'Yukari')

        self.say("Your barrier is up, and I know my magic can't pierce it, and neither would Fuyuhana's if it were her alone.",
                 'Ran',
                 'Ran')
        self.say("An impenetrable barrier, summoning a deadly curse, and this seemingly unnatural amount of strength...!",
                 'Ran',
                 'Ran')
        self.emote('Ran', 'lightbulb')
        self.say("Of course! We've seen similar magic before. Misaki drew power from the volcanic fires deep inside in Youkai Mountain. Similarly, Fuyuhana must be drawing magical energy from the entire forest!",
                 'Ran',
                 'Ran')



        self.say("N-no more flowers? N-no! I want to go flower viewing with Ran and Madam Yukari again in the spring! Don't take them away!",
                 'Chen',
                 'Chen')
        self.emote('Reimu', 'annoyed')
        self.say("Yeah, I had hoped for a nice gathering at my shrine under the cherry blossoms next year, too. You know, since it boosts donations.",
                 'Reimu',
                 'Reimu')
        self.emote('Marisa', 'exclamation')
        self.say("Oh, please! Forget the curse! I've been itching to give her a taste of my Master Spark. It's time to get even for what she did to my precious house!",
                 'Marisa',
                 'Marisa')
        self.say("As if causing a drought in Gensokyo was bad enough, her curse will sign the death warrant for the entire Human Village. I shall not allow that to happen!",
                 'Keine',
                 'Keine')
        self.say("Same here! We Tengu will never allow you to destroy us like this! We all depend on Gensokyo's flora for survival.",
                 'Aya',
                 'Aya')
        self.startle('Kaguya')
        self.say("Though we did not originate from this world, we now claim Gensokyo as our home, and as such, we will risk our lives to protect it!",
                 'Kaguya',
                 'Kaguya')
        self.say("Princess, I've got your back. And so does the rest of our fine team. Udonge, we're counting on you for support!",
                 'Eirin',
                 'Eirin')
        self.startle('Reisen')
        self.say("Naturally, Lady Yagokoro. I'll make sure they know how I became known as Eientei's finest illusionist and sniper!",
                 'Reisen',
                 'Reisen')
        self.emote('Mokou', 'exclamation')
        self.say("Hey, you're not getting all the glory, Kaguya! I'll make sure I take down twice as many trees as you!",
                 'Mokou',
                 'Mokou')

        self.stop_music()
        self.say("Ran, I'm sure you already have a battle plan formed.",
                 'Yukari',
                 'Yukari')


        self.play_music('battle06')

        self.show_chapter_title(5)
        self.say("Of course, Madam.",
                 'Ran',
                 'Ran')

        self.set_cursor_state(True)
        self.center_on_coords((5, 5))
        self.startle('Kodama Lord A')
        self.emote('Kodama Lord A', 'exclamation')
        self.center_on_coords((23, 5))
        self.startle('Kodama Lord B')
        self.emote('Kodama Lord B', 'exclamation')

        self.say("Those Spirit Source Points are funneling in energy from every tree in the forest to Fuyuhana.",
                 'Ran',
                 'Ran')


        self.center_on_coords((2, 13))
        self.startle('Kodama Lord C')
        self.emote('Kodama Lord C', 'exclamation')
        self.center_on_coords((26, 13))
        self.startle('Kodama Lord D')
        self.emote('Kodama Lord C', 'musicnote')


        self.say("Fuyuhana's spell will take some time to prepare. We will seal these six spirit source points to deny her access to that magical energy before it's ready.",
                 'Ran',
                 'Ran')


        self.center_on_coords((5, 22))
        self.startle('Walking Tree A')
        self.emote('Walking Tree A', 'annoyed')
        self.center_on_coords((23, 22))
        self.startle('Walking Tree B')
        self.emote('Walking Tree B', 'questionmark')


        self.say("I'm certain that should reduce the curse's power to something we can manage. We will then take care of her barrier and fog field as well.",
                 'Ran',
                 'Ran')

        self.center_on('Fuyuhana')
        self.say("Be sure to stay clear of Fuyuhana for now. She has some dangerous magic at her disposal with all the energy she has from the forest. Am I clear?",
                 'Ran',
                 'Ran')

        self.set_cursor_state(False)
        self.center_on('Youmu')
        self.say("Very good, Ran. So, are you ready, Youmu?",
                 'Yukari',
                 'Yukari')


        self.say("It's unfortunate that we weren't able to settle this without fighting, but I'm more than happy to bring this crisis to a close!",
                 'Youmu',
                 'Youmu')
        self.say("That's it, Youmu! Now, let's make sure this grand adventure of yours has the best happy ending ever!",
                 'Yuyuko',
                 'Yuyuko')

        self.set_invincibility_state('Fuyuhana', True)
        self.set_cust_var('Phase', 1)

        # Fuyuhana charges a spell. After 8 player turns
        self.say('Ran calculates that Fuyuhana will require 8 turns to fully prepare her spell.', None, None)
        self.set_cust_var('Countdown', 9)

        self.set_cursor_state(True)
        self.set_stats_display(True)

        self.set_status_effect('Cursed Tree A', 'Fog Veil')
        self.set_status_effect('Cursed Tree B', 'Fog Veil')
        self.set_status_effect('Cursed Tree C', 'Fog Veil')
        self.set_status_effect('Cursed Tree D', 'Fog Veil')

class Phase1Countdown(MapActionEvent):

    def __init__(self):

        triggers = [TeamTurnTrigger(1), CustVarTrigger('Phase', 1)]
        MapActionEvent.__init__(self, triggers, repeat=True)


    def execute(self):




        if self.map.cust_var['Countdown'] > 0:

            self.map.cust_var['Countdown'] -= 1
            self.say("Fuyuhana continues to build power. Turns left: %d"%self.map.cust_var['Countdown'], None, None)

            if self.map.cust_var['Countdown'] == 4 and 'Ran' in self.map.all_units_by_name.keys():

                self.say('The curse is about halfway complete! We have to hurry!',
                         'Ran',
                         'Ran')

            if self.map.cust_var['Countdown'] == 2 and 'Ran' in self.map.all_units_by_name.keys():

                self.say("Fuyuhana is three-quarters of the way there. We haven't got much time!",
                         'Ran',
                         'Ran')

            if self.map.cust_var['Countdown'] == 0:

                if 'Ran' in self.map.all_units_by_name.keys():
                    self.say("Oh, no! We're out of time! We have to secure those spirit source points immediately!",
                             'Ran',
                             'Ran')

                else:
                    self.say("Fuyuhana's curse is ready to deploy!", None, None)




class FuyuhanaPhase1Curse(MapActionEvent):

    def __init__(self):

        triggers = [TeamTurnTrigger(2), CustVarTrigger('Phase', 1), CustVarTrigger('Countdown', 0)]
        self.bullet_images = [ pygame.image.load(os.path.join('images', 'bullets', 'medorb_white.png')).convert_alpha(),
                               pygame.image.load(os.path.join('images', 'bullets', 'amulet_red.png')).convert_alpha(),
                               pygame.image.load(os.path.join('images', 'bullets', 'bigorb_orange.png')).convert_alpha(),
                               pygame.image.load(os.path.join('images', 'bullets', 'smallorb_red.png')).convert_alpha(),


                       ]

        MapActionEvent.__init__(self, triggers, repeat = True)


    def execute(self):


        self.center_on('Fuyuhana')
        self.say("Final curse of a Kodama Lord: Blossoms of Ash!",
                 "Fuyuhana",
                 "Fuyuhana")

        self.animation(self.map.all_units_by_name['Fuyuhana'])

        for target in list(self.map.team1):

            self.set_status_effect(target.name, 'Poison')
            self.set_status_effect(target.name, 'Dizzy')
            self.set_status_effect(target.name, 'Movement Down')

            damage_factor = 0.66

            damage = int(target.maxHP*damage_factor)
            start_HP = target.HP
            target.HP -= damage

            if target.HP < 0:
                target.HP = 0

            self.center_on(target.name)

            self.play_sfx('crit')
            self.render_effect(target, damage)
            target.render_hp_change(start_HP, target.HP)


            if target.HP == 0:
                target.alive = False


                if not target.ressurected and (target.has_trait_property('Revive Lv.1') or target.has_trait_property('Revive Lv.2') or target.has_trait_property('Revive Lv.3')):
                    self.map.check_map_event_revive(target)
                else:
                    self.map.kill(target, render_fadeout=True)

    def render_effect(self, target, damage_value):


        text_name = self.map.engine.bfont.render("Blossoms of Ash", True, (0, 0, 0))
        half_width = text_name.get_width()/2


        effect_text = self.map.engine.render_outlined_text(str(damage_value), self.map.engine.cfont, (255, 0, 0), (255, 255, 255))

        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
        self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
        self.map.engine.surface.blit(text_name, (420-half_width, 25))
        target.plot_stats()
        self.map.engine.surface.blit(effect_text, ((target.location_pixel.x+18-effect_text.get_width()/2, target.location_pixel.y-25)-self.map.screen_shift*self.map.engine.tilesize))

        pygame.display.flip()
        self.map.engine.clock.tick(60)
        self.map.engine.pause(1)

    def animation(self, unit):
        """
        function name: animation


        purpose: Draws burst of bullets going everywhere
        """

        curse_bullets_group = pygame.sprite.RenderUpdates()

        # First burst: Circular pattern of white bullets
        first_stage = 20
        for i in xrange(0,first_stage):
            start_coord = unit.location_pixel + Vector2(17,0) - 35* unit.map.screen_shift
            # Stars emtited from a 90 degree angle above target.

            # Generates a uniform distribution of angles for a circle
            angle = i*360.0/19

            speed = 5
            velocity = speed*Vector2(cos(radians(angle)), sin(radians(angle)))

            curse_bullets_group.add(BulletSprite(pygame.transform.rotate(self.bullet_images[0], -angle), start_coord, velocity))

        # Sets up the first frame

        unit.map.render_background()
        unit.map.render_all_units()
        unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
        unit.plot_stats()

        bg_surface = unit.map.engine.surface.copy()

        curse_bullets_group.clear(unit.map.engine.surface, bg_surface)
        curse_bullets_group.draw(unit.map.engine.surface)

        pygame.display.flip()
        unit.map.engine.clock.tick(60)

        # Animates rest of action
        self.play_sfx('fire')
        for tick in xrange(0,60):

            curse_bullets_group.clear(unit.map.engine.surface, bg_surface)
            curse_bullets_group.update()

            rects = curse_bullets_group.draw(unit.map.engine.surface)

            pygame.display.update(rects)
            unit.map.engine.clock.tick(60)

        # Second wave: Blast of random bullets in all directions

        second_stage_bullets = 100
        for i in xrange(0,second_stage_bullets):
            start_coord = unit.location_pixel + Vector2(17,0) - 35* unit.map.screen_shift
            # Stars emtited from a 90 degree angle above target.
            angle = randint(0,359)
            speed = randint(3,8)
            velocity = speed*Vector2(cos(radians(angle)), sin(radians(angle)))

            curse_bullets_group.add(BulletSprite(pygame.transform.rotate(choice(self.bullet_images), -angle), start_coord, velocity))

        # First Frame

        unit.map.render_background()
        unit.map.render_all_units()
        unit.map.engine.surface.blit(unit.map.engine.menu_board, (0, 490))
        unit.plot_stats()

        bg_surface = unit.map.engine.surface.copy()

        curse_bullets_group.clear(unit.map.engine.surface, bg_surface)
        curse_bullets_group.draw(unit.map.engine.surface)

        pygame.display.flip()
        unit.map.engine.clock.tick(60)

        self.play_sfx('beam1')
        for tick in xrange(0,240):

            curse_bullets_group.clear(unit.map.engine.surface, bg_surface)
            curse_bullets_group.update()

            rects = curse_bullets_group.draw(unit.map.engine.surface)

            pygame.display.update(rects)
            unit.map.engine.clock.tick(60)

class BulletSprite(pygame.sprite.Sprite):

    def __init__(self, image, position, velocity):
        """
        Sprite for star images used in Dizzy Attack's animation
        """

        self.velocity = velocity
        self.image = image
        self.floor = 490
        self.rect = self.image.get_rect()
        self.float_position = position
        self.rect.center = (int(self.float_position.x),int(self.float_position.y))

        pygame.sprite.Sprite.__init__(self)

    def update(self):

        """
        Does an Euler's method update on position based on acceleration / velocity every time function is called.
        """

        self.float_position += self.velocity

        self.rect.center = (int(self.float_position.x),int(self.float_position.y))

        if self.rect.bottom > self.floor:
            self.kill()

class SE_LampSwitchOn(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('SouthEast', 1)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if not self.map.all_landmarks['LightSouthEast'].lit:
            self.map.all_landmarks['LightSouthEast'].switch_state(True)

class SE_LampSwitchOff(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('SouthEast', 2)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):
        if self.map.all_landmarks['LightSouthEast'].lit:
            self.map.all_landmarks['LightSouthEast'].switch_state(False)


class SW_LampSwitchOn(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('SouthWest', 1)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if not self.map.all_landmarks['LightSouthWest'].lit:
            self.map.all_landmarks['LightSouthWest'].switch_state(True)

class SW_LampSwitchOff(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('SouthWest', 2)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):
        if self.map.all_landmarks['LightSouthWest'].lit:
            self.map.all_landmarks['LightSouthWest'].switch_state(False)


class W_LampSwitchOn(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('West', 1)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if not self.map.all_landmarks['LightNorthWest'].lit:
            self.map.all_landmarks['LightNorthWest'].switch_state(True)

class W_LampSwitchOff(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('West', 2)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):
        if self.map.all_landmarks['LightNorthWest'].lit:
            self.map.all_landmarks['LightNorthWest'].switch_state(False)



class E_LampSwitchOn(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('East', 1)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        if not self.map.all_landmarks['LightNorthEast'].lit:
            self.map.all_landmarks['LightNorthEast'].switch_state(True)

class E_LampSwitchOff(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger('East', 2)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):
        if self.map.all_landmarks['LightNorthEast'].lit:
            self.map.all_landmarks['LightNorthEast'].switch_state(False)


class Phase2Start(MapActionEvent):

    def __init__(self):

        triggers = [SSPStateTrigger(name, 1) for name in ('NorthWest', 'NorthEast', 'SouthEast', 'SouthWest', 'West', 'East')]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        self.say("The curse! Though my defeat appears inevitable, I will not fall without a fight!",
                 'Fuyuhana',
                 'Fuyuhana')

        # Different lines depending on if Reimu and Yukari are alive
        if "Reimu" in self.map.all_units_by_name.keys():
            name = "Reimu"
            line = "That annoying barrier around her collapsed! We can get through now!"

        elif "Yukari" in self.map.all_units_by_name.keys():
            name = "Yukari"
            line = "Well done! With her spell disrupted, let us directly attack Fuyuhana!"

        else:
            name = None
            line = "Fuyuhana's barrier has broken and she is open to attack!"
        self.say(line, name, name)

        self.set_cust_var('Phase', 2)

        for ssp_name in ("NorthWest", "NorthEast", "SouthWest", "SouthEast", "East", "West"):

            self.center_on_coords(self.map.all_landmarks[ssp_name].location)
            self.play_sfx("support3")
            self.show_animation("light_spell", self.map.all_landmarks[ssp_name].location)

            self.map.all_landmarks[ssp_name].map = None
            del self.map.all_ssps[tuple(self.map.all_landmarks[ssp_name].location)]
            del self.map.all_landmarks[ssp_name]

        self.center_on('Fuyuhana')
        self.play_sfx("support3")
        self.show_animation("light_spell", (14, 13))

        self.set_invincibility_state('Fuyuhana', False)
        self.map.all_units_by_name['Fuyuhana'].moves = 5
        self.map.all_units_by_name['Fuyuhana'].spell_actions = list((None, None, None, None, None))
        self.assign_spell('Fuyuhana', 'Great Mother Tree')
        self.set_ai_state('Fuyuhana', 'Pursuit')
        self.map.all_units_by_name['Fuyuhana'].get_moves_path()

        # Deploy second round of enemies
        self.fade_to_color('white', 1.0)
        self.set_fog_state(False)
        self.set_bg_overlay('Sunset')
        self.fade_from_color('white', 1.0)


class Phase3Start(MapActionEvent):

    def __init__(self):

        triggers = [UnitAliveTrigger('Fuyuhana', True), UnitHPBelowTrigger('Fuyuhana', 500)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):

        self.set_cust_var('Phase', 3)
        self.set_cust_var('Activate_AOE', True)
        self.set_cust_var('Target Started', False)
        # Teleport Fuyuhana back to her starting position
        unit_name = self.map.check_occupancy((14,13))

        if unit_name and unit_name != "Fuyuhana":
            self.center_on_coords((14,13))
            self.play_sfx('shimmer')
            self.show_animation('magic_cast', (14,13))
            self.random_teleport(unit_name, (12, 22, 5, 3))
            self.center_on(unit_name)
            self.emote(unit_name, 'questionmark')

        if tuple(self.map.all_units_by_name['Fuyuhana'].location_tile) != (14, 13):
            self.center_on('Fuyuhana')
            self.play_sfx('shimmer')
            self.show_animation('magic_cast', self.map.all_units_by_name['Fuyuhana'].location_tile)
            self.set_unit_pos('Fuyuhana', (14, 13))

        self.center_on('Fuyuhana')

        third_phase_units = (('Elite Kodama A',(7, 16)),
                             ('Elite Kodama B',(21, 16)),
                             ('Healer Fairy C',(7, 10)),
                             ('Healer Fairy D',(21, 10)),
                             ('Fairy Captain A',(11, 6)),
                             ('Fairy Captain B',(17, 6)),

                            )

        for new_unit, coord in third_phase_units:

            unit_name = self.map.check_occupancy(coord)

            if unit_name:
                self.center_on_coords(coord)
                self.play_sfx('shimmer')
                self.show_animation('magic_cast', coord)
                self.random_teleport(unit_name, (12, 22, 5, 3))
                self.center_on(unit_name)
                self.emote(unit_name, 'questionmark')
                self.center_on_coords((14,13))


            # Deploy the enemy units
            self.play_sfx('shimmer')
            self.show_animation('magic_cast', coord)
            self.deploy_unit(new_unit, coord)

            self.set_spirit_charge(new_unit, 600)


class TagTarget(MapActionEvent):

    def __init__(self):
        triggers = [TeamTurnTrigger(1), CustVarTrigger('Activate_AOE', True)]
        MapActionEvent.__init__(self, triggers, repeat = True)


    def render_grid(self, target):

        target_location = target.location_tile
        nearest_neighbors = [target.location_tile+Vector2(0, 1),
                             target.location_tile+Vector2(0, -1),
                             target.location_tile+Vector2(1, 0),
                             target.location_tile+Vector2(-1, 0)]
        next_nearest_neighbors = [target.location_tile+Vector2(0, 2),
                                  target.location_tile+Vector2(2, 0),
                                  target.location_tile+Vector2(-2, 0),
                                  target.location_tile+Vector2(0, -2),
                                  target.location_tile+Vector2(1, 1),
                                  target.location_tile+Vector2(-1, 1),
                                  target.location_tile+Vector2(1, -1),
                                  target.location_tile+Vector2(-1, -1),

                                  ]

        # Draw a target zone moving outward from target.
        self.add_highlight(target_location)
        self.render_update()
        self.pause(0.1)
        for location in nearest_neighbors:
            self.add_highlight(location)
        self.render_update()
        self.pause(0.1)
        for location in next_nearest_neighbors:
            self.add_highlight(location)

        self.render_update()
        self.pause(1)

        # Remove all highlights
        self.remove_highlight(target_location)
        all_neighbor_locations = next_nearest_neighbors+nearest_neighbors
        for location in all_neighbor_locations:
            self.remove_highlight(location)


    def render_update(self):

        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.render_menu_panel()

        # Draws emoticon frame
        pygame.display.flip()

    def execute(self):
        """
        Targets the unit with highest density of neighbors
        """

        # Determine the unit with highest density of neighbors

        prioritized_units = []

        for unit in self.map.team1:

            score = 0

            for neighbor in self.map.team1:

                neighbor_distance = abs(unit.location_tile.x - neighbor.location_tile.x) + abs(unit.location_tile.y - neighbor.location_tile.y)

                if neighbor_distance == 0:
                    pass
                elif neighbor_distance == 1:
                    score += 2
                elif neighbor_distance == 2:
                    score += 1

            prioritized_units.append([score, unit.name, unit])

        prioritized_units.sort()
        prioritized_units.reverse()

        target1 = prioritized_units[0][2]

        possible_lines = ["Fools! You're so easy to destroy clustered together like that.",
                          "Scatter! Like fallen leaves to the wind!",
                          "Take this! Now fall before me."
                          ]

        self.say(choice(possible_lines),
            'Fuyuhana',
            'Fuyuhana')

        self.center_on(target1.name)
        self.set_status_effect(target1.name, "Target")
        self.render_grid(target1)

        if len(prioritized_units) > 1:
            target2 = prioritized_units[1][2]

            self.center_on(target2.name)
            self.set_status_effect(target2.name, "Target")
            self.render_grid(target2)

        self.set_cust_var('Target Started', True)


class FuyuhanaAoE(MapActionEvent):

    def __init__(self):
        triggers = [TeamTurnTrigger(2), CustVarTrigger('Target Started', True)]

        MapActionEvent.__init__(self, triggers, repeat = True)
        self.user = 'Fuyuhana'


        self.bullet_images = [ pygame.image.load(os.path.join('images', 'bullets', 'medorb_white.png')).convert_alpha(),
                               pygame.image.load(os.path.join('images', 'bullets', 'smallorb_red.png')).convert_alpha(),
                               pygame.image.load(os.path.join('images', 'bullets', 'crystal_orange.png')).convert_alpha(),


                       ]

    def animate_action(self, target):



        self.play_sfx('fire')

        # Calculates the origin for a circular animation of bullets around the target
        x_o = (target.location_pixel.x)
        y_o = (target.location_pixel.y)
        r_o = Vector2(x_o, y_o)

        # Calculates the offsets associated with the bullets
        offset_vectors = [Vector2(35.0/2 - image.get_width()/2, 35.0/2 - image.get_height()/2) for image in self.bullet_images]


        for i in xrange(0, 60):


            self.map.render_background()
            self.map.render_all_units()
            self.map.render_cursor()
            self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
            self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
            target.plot_stats()

            x = 60*sin(i*pi/30)
            y = 60*cos(i*pi/30)

            angle = degrees(i*pi/30)

            self.map.engine.surface.blit(self.bullet_images[0], (r_o+offset_vectors[0]+Vector2(x, y)-self.map.screen_shift*self.map.engine.tilesize))
            self.map.engine.surface.blit(self.bullet_images[0], (r_o+offset_vectors[0]+Vector2(-x, -y)-self.map.screen_shift*self.map.engine.tilesize))
            self.map.engine.surface.blit(self.bullet_images[1], (r_o+offset_vectors[1]+Vector2(0.66*x, -0.66*y)-self.map.screen_shift*self.map.engine.tilesize))
            self.map.engine.surface.blit(self.bullet_images[1], (r_o+offset_vectors[1]+Vector2(-0.66*x, 0.66*y)-self.map.screen_shift*self.map.engine.tilesize))

            self.map.engine.surface.blit(pygame.transform.rotate(self.bullet_images[2], angle), (r_o+offset_vectors[2]+Vector2(0.33*x, 0.33*y)-self.map.screen_shift*self.map.engine.tilesize))
            self.map.engine.surface.blit(pygame.transform.rotate(self.bullet_images[2], angle+90), (r_o+offset_vectors[2]+Vector2(-0.33*x, 0.33*y)-self.map.screen_shift*self.map.engine.tilesize))
            self.map.engine.surface.blit(pygame.transform.rotate(self.bullet_images[2], angle+180), (r_o+offset_vectors[2]+Vector2(-0.33*x, -0.33*y)-self.map.screen_shift*self.map.engine.tilesize))
            self.map.engine.surface.blit(pygame.transform.rotate(self.bullet_images[2], angle+270),(r_o+offset_vectors[2]+Vector2(0.33*x, -0.33*y)-self.map.screen_shift*self.map.engine.tilesize))


            pygame.display.flip()
            self.map.engine.clock.tick(60)

    def render_effect(self, target, damage_value):


        text_name = self.map.engine.bfont.render("Holy Tree's Ward", True, (0, 0, 0))
        half_width = text_name.get_width()/2

        effect_text = self.map.engine.render_outlined_text(str(damage_value), self.map.engine.cfont, (255, 0, 0), (255, 255, 255))

        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
        self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
        self.map.engine.surface.blit(text_name, (420-half_width, 25))
        target.plot_stats()
        self.map.engine.surface.blit(effect_text, ((target.location_pixel.x+18-effect_text.get_width()/2, target.location_pixel.y-25)-self.map.screen_shift*self.map.engine.tilesize))

        pygame.display.flip()
        self.map.engine.clock.tick(60)
        self.map.engine.pause(1)

    def execute_damage(self, target):

        # Damage values
        target_HP_fraction = 0.45
        nearest_neighbor_HP_fraction = 0.35
        nnn_HP_fraction = 0.25

        damage = int(target.maxHP*target_HP_fraction)
        start_HP = target.HP
        target.HP -= damage

        if target.HP < 0:
            target.HP = 0

        self.center_on(target.name)

        self.play_sfx('crit')
        self.render_effect(target, damage)
        target.render_hp_change(start_HP, target.HP)

        if target.HP == 0:
            target.alive = False

            if not target.ressurected and (target.has_trait_property('Revive Lv.1') or target.has_trait_property('Revive Lv.2') or target.has_trait_property('Revive Lv.3')):
                self.map.check_map_event_revive(target)
            else:
                self.map.kill(target, render_fadeout=True)

        for neighbor in self.map.all_units_by_name.values():
            # Drop affects all units except for lord fuzzy
            if neighbor.name != self.user:
                # find distance

                neighbor_distance = abs(target.location_tile.x - neighbor.location_tile.x) + abs(target.location_tile.y - neighbor.location_tile.y)

                # Damage to nearest neighbors
                if neighbor_distance == 1:

                    damage = int(neighbor.maxHP*nearest_neighbor_HP_fraction)

                # Damage to NNN
                elif neighbor_distance == 2:

                    damage = int(neighbor.maxHP*nnn_HP_fraction)

                # Target out of range, skip
                else:
                    continue

                start_HP = neighbor.HP
                neighbor.HP -= damage

                if neighbor.HP < 0:
                    neighbor.HP = 0

                self.play_sfx('hit')
                self.render_effect(neighbor, damage)
                neighbor.render_hp_change(start_HP, neighbor.HP)

                if neighbor.HP == 0:
                    neighbor.alive = False


                    if not neighbor.ressurected and (neighbor.has_trait_property('Revive Lv.1') or neighbor.has_trait_property('Revive Lv.2') or neighbor.has_trait_property('Revive Lv.3')):
                        self.map.check_map_event_revive(neighbor)
                    else:
                        self.map.kill(neighbor, render_fadeout=True)




    def execute(self):
        # Find targetted units

        target_found = False
        for unit in self.map.team1:

            if "Target" in unit.status.keys():

                target_found = True
                break

        if target_found and "Stun" not in self.map.all_units_by_name['Fuyuhana'].status.keys():

            possible_lines = ["Kodama's Shield: Holy Tree's Ward",
                              "Bleed!",
                              "For the forest eternal!"
                              ]

            self.say(choice(possible_lines),
                'Fuyuhana',
                'Fuyuhana')

            for unit in self.map.team1:
                if "Target" in unit.status.keys():

                    self.center_on(unit.name)

                    # Shows the first spell animation
                    self.animate_action(unit)

                    # Hits the targetted unit.
                    self.execute_damage(unit)

            for unit in self.map.team1:
                if "Target" in unit.status.keys():
                    unit.remove_status('Target')



class Phase4Start(MapActionEvent):

    def __init__(self):

        triggers = [UnitAliveTrigger('Fuyuhana', True), UnitHPBelowTrigger('Fuyuhana', 300)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):


        self.set_cust_var('Phase', 4)

        self.center_on('Fuyuhana')
        self.say("The end is nigh. The last of my strength will ensure the Kodama that follow in my footsteps will never know your kind nor their descendants!",
            'Fuyuhana',
            'Fuyuhana')
        self.fade_to_color('white', 1.0)
        self.set_bg_overlay(None)
        self.fade_from_color('white', 1.0)
        self.say("At last, the final clouds have departed from this forest. I shall cast my final spell. Hear me, My Last Words. Ashes of Iwanaga!",
            'Fuyuhana',
            'Fuyuhana')

        # Clears all status effects
        self.map.all_units_by_name['Fuyuhana'].status = {}

        self.map.all_units_by_name['Fuyuhana'].spell_actions = list((None, None, None, None, None))
        self.assign_spell('Fuyuhana', 'Ashes of Iwanaga')


class PostMissionMAE(MapActionEvent):
    def __init__(self):
        # Triggers on turn 2

        triggers = []
        MapActionEvent.__init__(self, triggers)


        self.bullet_images = [ pygame.image.load(os.path.join('images', 'bullets', 'medorb_white.png')).convert_alpha(),
                               pygame.image.load(os.path.join('images', 'bullets', 'amulet_red.png')).convert_alpha(),
                               pygame.image.load(os.path.join('images', 'bullets', 'amulet_white.png')).convert_alpha(),
                               pygame.image.load(os.path.join('images', 'bullets', 'bigorb_orange.png')).convert_alpha(),
                               pygame.image.load(os.path.join('images', 'bullets', 'smallorb_red.png')).convert_alpha(),



                       ]

    def pre_exec(self):

        self.remove_all_enemies()
        self.stop_music()

        self.set_bg_overlay('Night')
        self.set_fog_state(False)

        new_positions = {   'Fuyuhana':(14, 16),


                            'Reimu':(13, 18),
                            'Youmu':(14, 18),
                            'Yuyuko':(15, 18),


                            'Marisa':(11, 17),
                            'Aya':(11, 18),
                            'Chen':(12, 17),
                            'Yukari':(12, 18),
                            'Ran':(12, 19),

                            'Eirin':(16, 17),
                            'Kaguya':(16, 18),
                            'Reisen':(16, 19),

                            'Keine':(17, 17),
                            'Mokou':(17, 18)

        }

        for name, coord in new_positions.items():
            self.set_unit_pos(name, coord)


    def animate_sealing(self, target):

        # For a given number of bullets, calculate the phase offsets to distribute them evenly around a circle
        num_bullets = 20
        phase_offsets = [bullet_counter*2*pi/num_bullets for bullet_counter in xrange(0, num_bullets)]

        # Calculates the origin for a circular animation of bullets around the target
        x_o = target.location_pixel.x
        y_o = target.location_pixel.y
        r_o = Vector2(x_o, y_o)

        # Calculates the offsets associated with the bullets
        offset_vectors = [Vector2(35.0/2 - image.get_width()/2, 35.0/2 - image.get_height()/2) for image in self.bullet_images]

        self.play_sfx('beam1')
        for frame_counter in xrange(0, 360):


            self.map.render_background()
            self.map.render_all_units()
            self.map.render_cursor()
            self.map.engine.surface.blit(self.map.engine.text_board, (0, 490))


            if frame_counter == 60 or frame_counter == 120:
                self.play_sfx('shoot6')

            # Calculate parametric equation for series of rotating bullets
            for bullet_counter in xrange(0, num_bullets):

                angle = frame_counter*pi/60+phase_offsets[bullet_counter]


                # Fold in first wave of bullets after 60 frames
                if frame_counter > 60 and bullet_counter%2 == 0:
                    x = (200-((frame_counter-60)*200/60))*sin(angle)
                    y = (200-((frame_counter-60)*200/60))*cos(angle)

                # Fold in remaining bullets after 120 frames
                elif frame_counter > 120 and bullet_counter%2 != 0:
                    x = (200-((frame_counter-120)*200/60))*sin(angle)
                    y = (200-((frame_counter-120)*200/60))*cos(angle)

                else:

                    x = 200*sin(angle)
                    y = 200*cos(angle)

                # Clips out any bullets that fall outside the draw region
                if y_o+y+self.bullet_images[1+bullet_counter%2].get_height()-35*self.map.screen_shift.y < 490:

                    self.map.engine.surface.blit(self.bullet_images[1+bullet_counter%2], (r_o+offset_vectors[0]+Vector2(x, y)-self.map.screen_shift*self.map.engine.tilesize))


            pygame.display.flip()
            self.map.engine.clock.tick(60)


    def animate_fuyuhanacurse(self, unit):
        """
        function name: animation


        purpose: Draws burst of bullets going everywhere
        """

        curse_bullets_group = pygame.sprite.RenderUpdates()

        # Second wave: Blast of random bullets in all directions

        second_stage_bullets = 50
        for i in xrange(0,second_stage_bullets):
            start_coord = unit.location_pixel + Vector2(17,0) - 35* unit.map.screen_shift
            # Stars emtited from a 90 degree angle above target.
            angle = randint(0,359)
            speed = randint(4,9)
            velocity = speed*Vector2(cos(radians(angle)), sin(radians(angle)))

            curse_bullets_group.add(BulletSprite(pygame.transform.rotate(choice(self.bullet_images), -angle), start_coord, velocity))

        # First Frame

        unit.map.render_background()
        unit.map.render_all_units()
        unit.map.engine.surface.blit(unit.map.engine.text_board, (0, 490))

        bg_surface = unit.map.engine.surface.copy()

        curse_bullets_group.clear(unit.map.engine.surface, bg_surface)
        curse_bullets_group.draw(unit.map.engine.surface)

        pygame.display.flip()
        unit.map.engine.clock.tick(60)

        self.play_sfx('beam1')
        for tick in xrange(0,180):

            curse_bullets_group.clear(unit.map.engine.surface, bg_surface)
            curse_bullets_group.update()

            rects = curse_bullets_group.draw(unit.map.engine.surface)

            pygame.display.update(rects)
            unit.map.engine.clock.tick(60)

    def execute(self):

        self.play_music('battle04')
        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.center_on('Fuyuhana')
        self.say("No! I can still fight! I will carry this burden until I cease to exist!",
            'Fuyuhana',
            'Fuyuhana')


        self.deploy_unit('Haruna', (14, 25))
        self.deploy_unit('Miu', (13, 25))
        self.deploy_unit('Kotone', (15, 25))
        self.move_unit('Haruna', (14, 20))
        self.move_unit('Miu', (13, 21))
        self.move_unit('Kotone', (15, 21))

        self.say("Amazing... Getting past that barrier was no easy feat.",
            'Miu',
            'Miu')
        self.say("Thankfully all their power was concentrated on keeping the magic inside the barrier rather than the other way around.",
            'Kotone',
            'Kotone')
        self.say("Yes. It appears we've arrived here on time. Now then. Let us help finally bring this madness to an end.",
            'Haruna',
            'Haruna')

        self.say("Ahh. My beloved disciples...please. I ask you to carry on my fight, my burden.",
            'Fuyuhana',
            'Fuyuhana')

        self.animate_fuyuhanacurse(self.map.all_units_by_name['Fuyuhana'])

        self.move_unit('Reimu', (14, 17))
        self.say("There! She's weakened enough that I can put a permanent seal on her!",
            'Reimu',
            'Reimu')
        self.say("Well, don't just stand there! What are you waiting for? Seal it! This curse is a huge pain the neck!",
            'Marisa',
            'Marisa')

        self.say("So this...is how my story ends...",
            'Fuyuhana',
            'Fuyuhana')
        self.move_unit('Fuyuhana', (14, 14))


        self.emote('Youmu', 'dotdotdot')


        self.emote('Reimu', 'exclamation')
        self.move_unit('Reimu', (14, 16))
        self.say("Divine Arts! Omnidirectional Sealing Circle!",
            'Reimu',
            'Reimu')
        self.say("I command thee! Be banished from our world forever!",
            'Reimu',
            'Reimu')

        self.center_on('Fuyuhana')
        self.animate_sealing(self.map.all_units_by_name['Fuyuhana'])


        self.startle('Youmu')

        self.play_sfx('shoot4')
        self.fade_to_color('white', 1.0)
        self.set_unit_pos('Youmu', (14, 16))
        self.set_unit_pos('Reimu', (15, 16))
        self.set_unit_pos('Fuyuhana', (14, 13))
        self.set_bg_overlay(None)
        self.fade_from_color('white', 1.0)

        self.play_music('title')
        self.emote('Reimu', 'annoyed')
        self.say("What the?! Youmu! You'd better have a good reason for interrupting me. I was this close to sealing her for good!",
            'Reimu',
            'Reimu')

        self.center_on('Youmu')

        self.say("Tell me! Can Fuyuhana put an end to her own curse?",
            'Youmu',
            'Youmu')

        self.say("It doesn't matter. While it was an incomplete seal, your shrine maiden's damage has been done. I can no longer exert my powers upon this world.",
            'Fuyuhana',
            'Fuyuhana')


        self.say("Oh. Thank goodness then.",
            'Youmu',
            'Youmu')
        self.say("Maybe you're right. If you leave this forest to us, one day we'll forget our agreement, and it will fade from our hearts with time and this crisis will begin again. Even we ghosts do not have perfect memories.",
            'Youmu',
            'Youmu')
        self.say("All we believed was that we should either submit to the will of the Kodama or exterminate them. However, I think there is a third option.",
            'Youmu',
            'Youmu')
        self.say("Fuyuhana, I would like to offer an olive branch. In Gensokyo, we are interconnected, and in times of danger, even mortal enemies may fight alongside each other.",
            'Youmu',
            'Youmu')
        self.say("Look at us! Humans, tengu, ghosts, youkai, lunarians... The Kodama are more than welcome to join us! We all care about this world, and that includes this forest.",
            'Youmu',
            'Youmu')


        self.say("In all our years, it has always been the Kodama against the humans and youkai. Never have we considered working alongside them. The very idea sounds revolting!",
            'Fuyuhana',
            'Fuyuhana')
        self.emote('Fuyuhana', 'dotdotdot')
        self.say("However... Perhaps I must place such prejudices aside. The world has changed without me. It is a decision for the next generation, not mine. What do you say, Miu and Kotone?",
            'Fuyuhana',
            'Fuyuhana')

        self.center_on('Haruna')

        self.startle('Miu')
        self.say("I'm the youngest of all of us, and I finally got to see all the people and youkai of Gensokyo during our trip. I think...that maybe we can go forward as friends instead.",
            'Miu',
            'Miu')
        if self.map.engine.check_event_completion(['CH5SQ3']):
            self.say("If we were able to fight side by side against the out of control mirror youkai Asa. I think... No, I'm certain we can do it again!",
                'Miu',
                'Miu')

        self.startle('Kotone')
        self.say("I've fought and fought, trained and trained, but I have nothing to show for it but a long history of black eyes.",
            'Kotone',
            'Kotone')
        self.say("I'm sorry, but I'm tired of playing the bully. I want to become strong enough to be a dependable protector of the forest. Without wanton destruction.",
            'Kotone',
            'Kotone')
        if self.map.engine.check_event_completion(['CH5SQ1']):
            self.say("Alongside Wriggle and her squad, we'll be the greatest heroes that this forest has known! I swear it.",
                'Kotone',
                'Kotone')

        self.say("Ok, then. Looks like Reimu and I are going to have some serious competition resolving incidents in those woods!",
            'Marisa',
            'Marisa')
        self.say("Look, I still don't trust them, but if it brings this war to a close, sure, I'll take it. I'm keeping an eye on all of you! So you better watch your back!",
            'Reimu',
            'Reimu')


        self.say("Haruna, you are the last of the elder Kodama. Ayaka and I shall soon exit this stage. May I entrust you to guide them toward a better future?",
            'Fuyuhana',
            'Fuyuhana')
        self.say("Of course. I will gladly take this honorable burden upon my shoulders.",
            'Haruna',
            'Haruna')
        self.move_unit('Haruna', (14, 19))
        self.pause(0.2)
        self.move_unit('Youmu', (14, 18))
        self.emote('Youmu', 'musicnote')
        self.say("Then, Youmu, let us together write a new era. Not as bitter foes but as fellow protectors of this forest, of all of Gensokyo!",
            'Haruna',
            'Haruna')

        self.center_on('Youmu')
        self.say("Yes! We all will!",
            'Youmu',
            'Youmu')

        self.say("My dearest Kodama Lords, I thank you from the bottom of my heart for your centuries of service. I shall now disappear from this world, rest assured that the forest is in good hands.",
            'Fuyuhana',
            'Fuyuhana')


        self.play_sfx('shimmer')
        self.fade_to_color('white', 2.0)
        self.kill_unit('Fuyuhana')
        self.fade_from_color('white', 0.5)

        self.say("We will ensure its continued protection. You have my word! All of us, together! We all swear it!",
            'Youmu',
            'Youmu')

        self.stop_music()
        self.fade_to_color('black', 5.0)