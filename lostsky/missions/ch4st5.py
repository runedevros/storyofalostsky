from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, UnitAliveTrigger, TeamTurnTrigger, ArrivalTrigger
from lostsky.battle.mapobj import SpiritSourcePoint
from random import choice
import pygame
import os

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'Loyalty and Devotion'
        location = 'Southern Thicket'
        id_string = 'CH4ST5'
        prereqs = ['CH4ST4']
        show_rewards = True
        desc = "The final battle for dominion over the Bamboo Forest awaits. With mystical lantern in hand and thoughts of her mistress's safety in mind, Youmu heads toward a dangerous confrontation with Ayaka and Fuyuhana."

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch4st5.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat All',
                     'desc':'Defeat Ayaka and all her allies!'}

        deploy_data = {'enable':True,
                       'max_units':18,
                       'preset_units':{},
                       'default_locations':{'Youmu':(12, 5),
                                            'Ran':(10, 5),
                                            'Chen':(10, 6),
                                            'Aya':(10, 7),
                                            'Reimu':(11, 5),
                                            'Marisa':(13, 5),
                                            'Keine':(11, 6),
                                            'Kaguya':(14,5),
                                            'Mokou':(14 ,6),
                                            'Reisen':(14, 7),
                                            'Eirin':(13,6),
                                            'Yukari':(12,6),
                                            'Alice':(12, 7),

                                               },
                       'boxes':[(10, 4, 5, 4), ]
                       }


        reward_list = [('treasure', '023_essenseofspring')
                   ]


        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Ayaka45',
                                'unit_name': 'Ayaka',
                                    'level': 28},
                           {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama A',
                                    'level': 22},

                           {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama B',
                                    'level': 22},

                           {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama C',
                                    'level': 22},

                           {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama D',
                                    'level': 22},


                           {'template_name': 'Fuyuhana',
                                'unit_name': 'Fuyuhana',
                                    'level': 50},

                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 22},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 22},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 22},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree D',
                                    'level': 22},
                           {'template_name': 'Yuyuko',
                                'unit_name': 'Yuyuko',
                                    'level': 22},
                           {'template_name': 'Yuyuko',
                                'unit_name': 'Yuyuko2',
                                    'level': 22},


                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree A',
                                    'level': 22},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree F',
                                    'level': 22},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree G',
                                    'level': 22},
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree B',
                                    'level': 22},


                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree C',
                                    'level': 22},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree J',
                                    'level': 22},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree K',
                                    'level': 22},
                           {'template_name': 'Cursed Tree',
                                'unit_name': 'Cursed Tree D',
                                    'level': 22},


                           {'template_name': 'Kodama Lord',
                                'unit_name': 'KL 1',
                                    'level': 22},

                           {'template_name': 'Kodama Lord',
                                'unit_name': 'KL 2',
                                    'level': 22},



                            ]

        initial_spells = {'Ayaka':['Pale Mist Spear', 'Jubokko\'s Touch', 'Leaf Crystal'],
                          'Hitodama A':['Fireball'],
                          'Hitodama B':['Leaf Crystal'],
                          'Hitodama C':['Dagger Throw'],
                          'Hitodama D':['Holy Amulet'],
                          'Cursed Tree A':['Poison Dust'],
                          'Cursed Tree B':['Poison Dust'],
                          'Cursed Tree C':['Poison Dust'],
                          'Cursed Tree D':['Poison Dust'],

                            }

        initial_traits = {}
        initial_ai_states = {'Ayaka':'Pursuit',
                             'Hitodama A':'Defend',
                             'Hitodama B':'Defend',
                             'Hitodama C':'Defend',
                             'Hitodama D':'Defend',
                             'Cursed Tree A':'Attack',
                             'Cursed Tree B':'Attack',
                             'Cursed Tree C':'Attack',
                             'Cursed Tree D':'Attack',

                            }
        initial_locations = {'Fuyuhana':(12, 1),
                             'Ayaka':(13, 1),
                             'Yuyuko':(12, 5),

                             'Walking Tree A':(9, 5),

                             'Walking Tree B':(10, 6),

                             'Walking Tree C':(14, 6),

                             'Walking Tree D':(15, 5),

                             'Cursed Tree A':(6, 5),
                             'Walking Tree F':(7, 6),
                             'KL 1':(7, 7),
                             'Walking Tree G':(7, 8),
                             'Cursed Tree B':(6, 9),


                             'Cursed Tree C':(18, 5),
                             'Walking Tree J':(17, 6),
                             'KL 2':(17, 7),
                             'Walking Tree K':(17, 8),
                             'Cursed Tree D':(18, 9),


                             'Youmu':(-1,10),
                             'Ran':(-1,10),
                             'Chen':(-1,10),
                             'Marisa':(-1,10),
                             'Reimu':(-1,10),
                             'Keine':(-1,10),
                             'Mokou':(-1,10),
                             'Aya':(-1,10),
                             'Kaguya':(-1,10),
                             'Reisen':(-1,10),
                             'Eirin':(-1,10),

                             }
        reserve_units = ['Yuyuko2','Hitodama A', 'Hitodama B', 'Hitodama C', 'Hitodama D']#[list of unit names to deploy later in mission]
        all_landmarks = [
                         {'name':'torii_NW',
                          'id_string':'small_torii',
                          'location':(4, 3)},
                         {'name':'cb_tree_SW',
                          'id_string':'cherryblossom_tree',
                          'location':(4, 12)},
                         {'name':'cb_tree_NE',
                          'id_string':'cherryblossom_tree',
                          'location':(20, 2)},
                         {'name':'torii_SE',
                          'id_string':'small_torii',
                          'location':(20, 11)},
        ]

        required_starters = ['Youmu', 'Ran', 'Chen', 'Marisa', 'Reimu', 'Keine', 'Mokou', 'Aya', 'Kaguya', 'Reisen', 'Eirin' ]
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [Ayaka_Autodamage(), Ayaka_AOE(), SSPAutodamage(), SWTreasureFoundMAE(), NETreasureFoundMAE()]
        required_survivors = ['Youmu', 'Ran', 'Chen', 'Marisa', 'Reimu', 'Keine', 'Mokou', 'Aya', 'Kaguya', 'Reisen', 'Eirin', 'Yukari', 'Yuyuko', 'Ayaka']
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

        self.set_bg_overlay('Sunset')

        self.play_music('battle01')

        self.set_stats_display(False)
        self.set_cursor_state(False)

        self.center_on('Yuyuko')


        self.say('My, my. Is it daybreak already? Do you have anything more, Fuyuhana?',
                 'Yuyuko',
                 'Yuyuko')

        self.say("You. Why do you intend to fight us? All those years ago, it was you who released spring and awakened the Kodama!",
                 'Fuyuhana',
                 'Fuyuhana')

        self.say("Ah, that. True, but your revival was never my intention.",
                 'Yuyuko',
                 'Yuyuko')
        self.say("As such, this is why...I am here. This mistake is mine alone, and mine alone to undo.",
                 'Yuyuko',
                 'Yuyuko')

        self.say("Haha. You may be death incarnate, but you're as frightening as a corpse. What strength do you have left?",
                 'Ayaka',
                 'Ayaka')
        self.say("I no longer care to humor you. This is your penance, Yuyuko. This will end everything!",
                 'Fuyuhana',
                 'Fuyuhana')
        self.stop_music()

        self.emote('Yuyuko', 'musicnote')
        self.say("Say... Fuyuhana?",
                 'Yuyuko',
                 'Yuyuko')
        self.say("Take a look. Isn't the dawn...beautiful?",
                 'Yuyuko',
                 'Yuyuko')



        for unit_name in ('Walking Tree A', 'Walking Tree B', 'Walking Tree C', 'Walking Tree D'):

            tree_unit = self.map.all_units_by_name[unit_name]
            delta = self.map.all_units_by_name['Yuyuko'].location_tile - tree_unit.location_tile
            self.play_sfx('shoot2')
            tree_unit.render_walk([delta])
            self.set_unit_pos(unit_name, (12,5))

        self.fade_to_color('white', 1.5)


        self.add_to_party('Yukari')
        self.assign_spell('Yukari', 'Holy Amulet')
        self.assign_spell('Yukari', 'Barrier Buster')
        self.assign_spell('Yukari', 'Weakening Amulet')
        self.assign_spell('Yukari', 'Ran and Chen')
        # Assign Yukari's SC here


        self.set_unit_pos('Reimu', (11, 5))
        self.set_unit_pos('Walking Tree A', (10, 5))

        self.set_unit_pos('Marisa', (13, 5))
        self.set_unit_pos('Walking Tree B', (14, 5))

        self.set_unit_pos('Yukari', (12, 6))
        self.set_unit_pos('Walking Tree C', (12, 7))

        self.set_unit_pos('Youmu', (12, 4))
        self.set_unit_pos('Walking Tree D', (12, 3))

        self.set_unit_pos('Ran', (8, 7))
        self.set_unit_pos('Chen', (8, 6))
        self.set_unit_pos('Aya', (8, 8))

        self.set_unit_pos('Mokou', (16, 7))
        self.set_unit_pos('Kaguya', (16, 6))
        self.set_unit_pos('Reisen', (16, 8))

        self.set_unit_pos('Keine', (9, 7))
        self.set_unit_pos('Eirin', (15, 7))

        self.fade_from_color('white', 1.5)

        self.play_music('battle04')
        self.startle('Youmu')
        self.say("Madam Yuyuko!",
                 'Youmu',
                 'Youmu')
        self.say("Impeccable timing, my darling Youmu.",
                 'Yuyuko',
                 'Yuyuko')
        self.say("Tch! You owe us one, Yuyuko.",
                 'Marisa',
                 'Marisa')

        self.emote('Reimu', 'scribble')
        self.say("Oh, shut it. Let's just give these guys a thrashing and get this over with!",
                 'Reimu',
                 'Reimu')

        self.play_sfx('crit')

        self.fade_to_color((90,90,255), 0.25)
        self.kill_unit('Walking Tree A')
        self.kill_unit('Walking Tree B')
        self.kill_unit('Walking Tree C')
        self.kill_unit('Walking Tree D')
        self.fade_from_color((90,90,255), 0.25)

        self.startle('Ran')
        self.say("Let's go, Chen! Lady Yuyuko is counting on us!",
                 'Ran',
                 'Ran')

        self.play_sfx('crit')

        self.fade_to_color((90,90,255), 0.25)
        self.kill_unit('KL 1')
        self.kill_unit('Walking Tree F')
        self.kill_unit('Walking Tree G')
        self.fade_from_color((90,90,255), 0.25)

        self.emote('Mokou', 'exclamation')
        self.say("This makes 132!",
                 'Mokou',
                 'Mokou')
        self.emote('Kaguya', 'musicnote')
        self.say("132? I'd say I'm impressed, however I'm at 154 trees and counting. Do try and keep up, sloth.",
                 'Kaguya',
                 'Kaguya')

        self.play_sfx('crit')
        self.fade_to_color((90,90,255), 0.25)
        self.kill_unit('KL 2')
        self.kill_unit('Walking Tree J')
        self.kill_unit('Walking Tree K')
        self.fade_from_color((90,90,255), 0.25)


        self.say('Come on! Use the lantern, Youmu!',
                 'Marisa',
                 'Marisa')

        self.say('I know! Here goes! Oh, Lantern of Souls, hear me! Banish Fuyuhana from this material plane!',
                 'Youmu',
                 'Youmu')

        self.play_sfx('shimmer')
        self.show_animation('light_spell', (12, 1))

        self.fade_to_color('white', 0.5)
        self.kill_unit('Fuyuhana')
        self.fade_from_color('white', 0.5)

        self.startle('Ayaka')
        self.say('No! NO! What have you done?',
                 'Ayaka',
                 'Ayaka')
        self.say("Nothing special, really. The lantern's spell has simply laid Fuyuhana to rest in her original tree. Just forever this time.",
                 'Yukari',
                 'Yukari')
        self.say("Oh and by the way, with her gone, so is her grasp over the clouds. In other words? We win!",
                 'Yukari',
                 'Yukari')

        self.stop_music()
        self.say('You heard her. So, your next move, Ayaka?',
                 'Youmu',
                 'Youmu')


        self.play_music('battle05')
        self.say('Youmu, you...! One day you will understand my unwavering devotion! My loyalty! I will protect my mistress to the end!',
                 'Ayaka',
                 'Ayaka')
        self.move_unit('Ayaka', (12, 2))
        self.play_sfx('shoot5')

        self.set_bg_overlay('Night')

        self.show_animation('magic_cast', (12,2))
        ssp_list = [SpiritSourcePoint('NorthWest', (4, 2), 2), SpiritSourcePoint('SouthWest', (9, 9), 2),
                    SpiritSourcePoint('NorthEast', (15, 5), 2), SpiritSourcePoint('SouthEast', (20, 12), 2)]

        for index, ssp in enumerate(ssp_list):
            self.map.add_ssp(ssp)

            self.show_animation('magic_cast', ssp.location)
            self.deploy_unit('Hitodama '+'ABCD'[index], ssp.location)


        self.say("She wouldn't! She can't possibly be releasing the final curse of a Kodama Lord!",
                 'Ran',
                 'Ran')
        self.say("In the ancient legends, the final curse of a Kodama Lord brought plagues and disasters upon the land. If Ayaka is willing to sacrifice herself to protect Fuyuhana's spirit, then...!",
                 'Keine',
                 'Keine')

        self.emote('Reisen', 'exclamation')
        self.say("But that'll wreck the whole Bamboo Forest! And Eientei!",
                 'Reisen',
                 'Reisen')
        self.say("For my mistress's dream! For the sake of forest's survival, I will not stop! I will never stop fighting!",
                 'Ayaka',
                 'Ayaka')
        self.say("There's no time to waste. Can we contain the curse, maybe redirect it so it doesn't affect the Bamboo Forest... Ah! Reimu, you're good at barriers, right?",
                 'Youmu',
                 'Youmu')
        self.say("Good thinking. Reimu, I want you to put up the most powerful barrier you can muster. Of course, I'll do the same. Let's seal the entire curse within this area!",
                 'Yukari',
                 'Yukari')
        self.say("Eirin, Marisa, Ran! Anyone with any experience with incantations or magic wands, I'll be requesting your contribution!",
                 'Yukari',
                 'Yukari')
        self.say("Boy, oh boy. I know you normally have crazy ideas, but this is lunacy! That kind of barrier will... It'll create a super powered Kodama Lord!",
                 'Reimu',
                 'Reimu')

        self.say("Reimu, I understand your concern, but this is a risk we must take. We'll pull through this. I guarantee it.",
                 'Youmu',
                 'Youmu')
        self.say("Remember, you've overcome every challenge that has confronted you. I've got written proof!",
                 'Aya',
                 'Aya')
        self.say("You beat Misaki, the legendary Kodama of Youkai Mountain.",
                 'Mokou',
                 'Mokou')
        self.say("And you've defeated the Kodama time and again, from Eientei to here.",
                 'Kaguya',
                 'Kaguya')
        self.say("This is simply another victory waiting to be added to your story. I have faith in you.",
                 'Yuyuko',
                 'Yuyuko')

        self.say("Ok! Ready, Reimu?",
                 'Yukari',
                 'Yukari')
        self.say("Who do you take me for? Here I go! Fantasy Seal!",
                 'Reimu',
                 'Reimu')
        self.say("Quadruple Barrier!",
                 'Yukari',
                 'Yukari')


        for ssp in ssp_list:
            self.play_sfx('support3')
            self.show_animation('sealing_spell', ssp.location)

        self.fade_to_color('white', 0.5)
        self.set_bg_overlay('Sunset')
        self.fade_to_color('white', 0.5)


        self.say("Madam Yuyuko, you've done enough. Leave the rest of the battle to us!",
                 'Youmu',
                 'Youmu')
        self.move_unit('Yuyuko', (12,4))
        self.kill_unit('Yuyuko')

        self.say("Youmu, let this be a spectacular battle between two noble knights and their tragic, blind devotion!",
                 'Ayaka',
                 'Ayaka')

        self.center_on('Youmu')
        self.set_spirit_charge('Ayaka', 900)

        self.set_stats_display(True)
        self.set_cursor_state(True)


class SWTreasureFoundMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((4, 12, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Player has discovered treasure under cherry blossom tree
        """

        self.say("Buried at the foot of the cherry tree is a small rusted box.",
                None,
                None)
        self.say("Acquired Treasure Item: Mirror of Truth!",
                None,
                None)
        self.add_item('treasure', '022_mirroroftruth', 1)



class NETreasureFoundMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((20, 2, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Player has discovered treasure under cherry blossom tree
        """

        self.say("Buried at the foot of the cherry tree is a small rusted box.",
                None,
                None)
        self.say("Acquired Treasure Item: Angel Feather!",
                None,
                None)
        self.add_item('treasure', '020_angelfeather', 1)

class SSPAutodamage(MapActionEvent):

    def __init__(self):

        triggers = [TeamTurnTrigger(1), UnitAliveTrigger('Ayaka', True)]
        MapActionEvent.__init__(self, triggers, repeat = True)

    def execute(self):

        # Does damage to any units currently occupying an SSP
        for location in self.map.all_ssps.keys():
            occupied = self.map.check_occupancy(location)
            if occupied and self.map.all_units_by_name[occupied].team == 1:
                unit = self.map.all_units_by_name[occupied]

                damage_factor = 0.34

                damage = int(unit.maxHP * damage_factor)

                starting_HP = unit.HP
                unit.HP -= damage
                if unit.HP <= 0:
                    unit.HP = 0

                self.center_on(unit.name)

                text_status_effect = self.map.engine.section_font.render('Cursed Field', True, (0, 0, 0))

                text_effect = self.map.engine.render_outlined_text(str(damage), self.map.engine.cfont, (255, 0, 0), (255, 255, 255))

                self.map.render_background()
                self.map.render_all_units()
                self.map.render_cursor()
                self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
                self.map.engine.surface.blit(text_status_effect, (420-text_status_effect.get_width()/2, 20))
                self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
                unit.plot_stats()
                self.map.engine.surface.blit(text_effect, ((unit.location_pixel.x+18-text_effect.get_width()/2, unit.location_pixel.y-25)-self.map.screen_shift*self.map.engine.tilesize))
                self.map.engine.pause(1)

                unit.render_hp_change(starting_HP, unit.HP)

                if unit.HP == 0:
                    if unit.deathquote:
                        self.say(unit.deathquote[0]['line'], unit.name, unit.deathquote[0]['portrait'])
                    self.map.kill(unit, render_fadeout=True)


class Ayaka_Autodamage(MapActionEvent):

    def __init__(self):

        triggers = [TeamTurnTrigger(2), UnitAliveTrigger('Ayaka', True)]
        MapActionEvent.__init__(self, triggers, repeat = True)

    def execute(self):

        # counts how many spirit source points are occupied
        ssps_occupied = 0
        damage_factor = 0
        for location in self.map.all_ssps.keys():
            occupied = self.map.check_occupancy(location)
            if occupied and self.map.all_units_by_name[occupied].team == 1:
                ssps_occupied += 1

        # Every turn, Ayaka takes residual damage
        if ssps_occupied == 0:
            damage_factor = 0.05
            self.say("This pain is a small price to pay for the overwhelming power of the final curse..!",
                 'Ayaka',
                 'Ayaka')

        elif ssps_occupied == 1:
            damage_factor = 0.07
            self.say("Gh! This is nothing! I can take this. For Fuyuhana!",
                 'Ayaka',
                 'Ayaka')

        elif ssps_occupied == 2:
            damage_factor = 0.10
            self.say("I must admit this pain is annoying. But I chose to sacrifice my strength to those sources!",
                 'Ayaka',
                 'Ayaka')


        elif ssps_occupied == 3:
            damage_factor = 0.12
            self.say("I may be losing a lot of energy, but surely they cannot survive long in those curse fields. I can endure this!",
                 'Ayaka',
                 'Ayaka')

        elif ssps_occupied == 4:
            damage_factor = 0.15
            self.say("Curses! I will not last long if this continues... No, but they are suffering, too. I...I must be strong!",
                 'Ayaka',
                 'Ayaka')

        damage = int( self.map.all_units_by_name['Ayaka'].maxHP * damage_factor)



        starting_HP = self.map.all_units_by_name['Ayaka'].HP
        self.map.all_units_by_name['Ayaka'].HP -= damage
        if self.map.all_units_by_name['Ayaka'].HP <= 0:
            self.map.all_units_by_name['Ayaka'].HP = 0


        self.center_on('Ayaka')

        text_status_effect = self.map.engine.section_font.render("Kodama's Last Curse", True, (0, 0, 0))

        text_effect = self.map.engine.render_outlined_text(str(damage), self.map.engine.cfont, (255, 0, 0), (255, 255, 255))

        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
        self.map.engine.surface.blit(text_status_effect, (420-text_status_effect.get_width()/2, 20))
        self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
        self.map.all_units_by_name['Ayaka'].plot_stats()
        self.map.engine.surface.blit(text_effect, ((self.map.all_units_by_name['Ayaka'].location_pixel.x+18-text_effect.get_width()/2, self.map.all_units_by_name['Ayaka'].location_pixel.y-25)-self.map.screen_shift*self.map.engine.tilesize))
        self.map.engine.pause(1)

        self.map.all_units_by_name['Ayaka'].render_hp_change(starting_HP, self.map.all_units_by_name['Ayaka'].HP)

        if self.map.all_units_by_name['Ayaka'].HP == 0:




            self.say("Ha...haha. I see... So this is the end. A mere servant to the end and nothing more. I was a fool.",
                 'Ayaka',
                 'Ayaka')

            self.show_animation('magic_cast',self.map.all_units_by_name['Ayaka'].location_tile)
            self.play_sfx('shoot5')
            self.fade_to_color('white', 0.5)
            self.remove_all_enemies()
            self.kill_unit('Ayaka')
            self.map.all_ssps = {}
            del self.map.all_landmarks['NorthWest']
            del self.map.all_landmarks['NorthEast']
            del self.map.all_landmarks['SouthWest']
            del self.map.all_landmarks['SouthEast']
            self.fade_from_color('white', 0.5)



class Ayaka_AOE(MapActionEvent):

    def __init__(self):
        """
        Ayaka gets an AOE attack that damages units around her within a 2 tile radius.
        """

        triggers = [TeamTurnTrigger(2), UnitAliveTrigger('Ayaka', True)]
        MapActionEvent.__init__(self, triggers, repeat = True)
        spear_image = pygame.image.load(os.path.join('images', 'bullets', 'spear_red.png')).convert_alpha()
        self.spear_image = pygame.transform.rotate(spear_image, 90)

        self.maxrange = 3

    def execute(self):
        self.center_on('Ayaka')

        targets = self.get_targets()
        if targets:
            possible_quotes = ( "Your error was coming too close.",
                                "You shall not reach my mistress.",
                                "Even at the expense of my life, I will pay the price.",
                                "Take the anger of these ancient roots infused with our forest's strength!"
                                    )

            self.say(choice(possible_quotes),
                     'Ayaka',
                     'Ayaka')

            self.execute_damage(targets)


    def get_targets(self):

        """
        Function name: check_range
        Purpose: get a list of all units in attack range of Ayaka's AOE attack.
        Output: returns a list of targets
        """

        targets = []

        user = self.map.all_units_by_name['Ayaka']

        for unit in self.map.team1:
            neighbor_distance = abs(user.location_tile.x - unit.location_tile.x) + abs(user.location_tile.y - unit.location_tile.y)

            if neighbor_distance < self.maxrange:
                targets.append((unit, neighbor_distance))

        return targets


    def render_spear(self, target):
        """
        Name: render_spear
        Draws a spear coming out of the ground for the given target
        """
        frame_count = 25

        text_name = self.map.engine.bfont.render("Barbed Roots", True, (0, 0, 0))
        half_width = text_name.get_width()/2

        for frame in xrange(0, frame_count):

            spear_y = (frame*float(self.spear_image.get_height())/frame_count)

            partial_spear = self.spear_image.subsurface((0,0,self.spear_image.get_width(), spear_y))

            self.map.render_background()
            self.map.render_all_units()
            self.map.render_cursor()
            self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
            self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
            self.map.engine.surface.blit(text_name, (420-half_width, 25))
            target.plot_stats()
            self.map.engine.surface.blit(partial_spear, ((target.location_pixel.x+18-self.spear_image.get_width()/2, target.location_pixel.y+30-spear_y)-self.map.screen_shift*self.map.engine.tilesize))

            pygame.display.flip()
            self.map.engine.clock.tick(60)


    def render_effect(self, target, damage_value):
        """
        Function name: render_effect

        Handles the drawing of the attack effect for Ayaka's AOE move
        """

        # Draws the spear attack
        self.play_sfx('shoot2')
        self.render_spear(target)

        self.play_sfx('hit')

        # Draws the battle damage
        text_name = self.map.engine.bfont.render("Barbed Roots", True, (0, 0, 0))
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

    def execute_damage(self, targets):
        """
        function name: execute_damage
        purpose: for every target in Ayaka's range, do a certain amount of damage to them.
        """


        # Fraction of current HP target takes
        n1_HP_fraction = 0.55
        n2_HP_fraction = 0.35

        for unit, neighbor_distance in targets:

            if neighbor_distance < self.maxrange:

                # Damage to nearest neighbors
                if neighbor_distance == 1:

                    damage = int(unit.HP*n1_HP_fraction)

                # Damage to NNN
                elif neighbor_distance == 2:

                    damage = int(unit.HP*n2_HP_fraction)

                start_HP = unit.HP
                unit.HP -= damage

                if unit.HP < 0:
                    unit.HP = 0

                self.render_effect(unit, damage)
                unit.render_hp_change(start_HP, unit.HP)

                if unit.HP == 0:


                    if not unit.ressurected and (unit.has_trait_property('Revive Lv.1') or unit.has_trait_property('Revive Lv.2') or unit.has_trait_property('Revive Lv.3')):
                        self.map.check_map_event_revive(unit)
                    else:
                        self.map.kill(unit, render_fadeout=True)



class PostMissionMAE(MapActionEvent):
    def __init__(self):
        # Triggers on turn 2
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):
        self.remove_all_enemies()
        self.stop_music()


        self.set_unit_pos('Ayaka', (12, 2))

        self.set_unit_pos('Reimu', (11, 5))
        self.set_unit_pos('Marisa', (13, 5))

        self.set_unit_pos('Yukari', (11, 4))
        self.set_unit_pos('Youmu', (12, 4))
        self.set_unit_pos('Yuyuko', (13, 4))
        self.set_unit_pos('Ran', (9, 6))
        self.set_unit_pos('Chen', (8, 6))
        self.set_unit_pos('Aya', (10, 6))
        self.set_unit_pos('Keine', (9, 7))

        self.set_unit_pos('Mokou', (14, 6))
        self.set_unit_pos('Kaguya', (15, 6))
        self.set_unit_pos('Reisen', (16, 6))
        self.set_unit_pos('Eirin', (15, 7))


    def execute(self):

        self.play_music('event01')


        self.center_on('Youmu')

        self.say("Do you see? We are the same, Youmu. Loyal to our mistresses to the bitter end.",
                 'Ayaka',
                 'Ayaka')
        self.say("You should have set your blade down, Ayaka.",
                 'Youmu',
                 'Youmu')
        self.say("Tell me. How long have you served your mistress, Youmu?",
                 'Ayaka',
                 'Ayaka')
        self.say("...I have served Madam Yuyuko for many decades.",
                 'Youmu',
                 'Youmu')

        self.say("Too short. That is not nearly long enough for you to understand that this devotion is not a blessing, but a curse!",
                 'Ayaka',
                 'Ayaka')
        self.say("I know of no other life than to fight for my mistress in the name of her dream of protecting our forest! And I will never know anything more!",
                 'Ayaka',
                 'Ayaka')
        self.say("I can do nothing else to stop you. You have bested me, even armed with my final curse. I have seen my mistake to the end.",
                 'Ayaka',
                 'Ayaka')
        self.say("There is nothing left for me but to fade from this mortal world. Perhaps then I will find peace.",
                 'Ayaka',
                 'Ayaka')
        self.say("Still, I cannot help but smile. I was bested by a worthy, honorable foe. It is a better end than I deserve.",
                 'Ayaka',
                 'Ayaka')

