from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, UnitHPBelowTrigger, UnitAliveTrigger, SSPStateTrigger, CustVarTrigger
from lostsky.battle.mapobj import SpiritSourcePoint

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'The Guardian Misaki'
        location = 'Summit'
        id_string = 'CH3ST5'
        prereqs = ['CH3ST4']
        show_rewards = True
        desc = "The Guardian Misaki awaits at the top of Youkai Mountain. With the balance of Gensokyo at stake, will Youmu's team be able to convince her to help them stop Fuyuhana?"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch3st5.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat Boss',
                     'target':'Misaki',
                     'desc':'Defeat Misaki!'
                     }

        deploy_data = {'enable':True,
                       'max_units':9,
                       'preset_units':{},
                       'boxes':[(10, 19, 5, 3)],
                       'default_locations':{'Youmu':(13,19),
                                            'Ran':(10,19),
                                            'Keine':(14,19),
                                            'Marisa':(12,19),
                                            'Aya':(11,19),
                                            'Mokou':(14,20),
                                            'Chen':(10,20),
                                            'Reimu':(12,20),
                                            'Alice':(12,21),
                                            }
                       }
        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Misaki',
                                'unit_name': 'Misaki',
                                    'level': 15
                                },
                          {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama A',
                                    'level': 10
                                },
                          {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama B',
                                    'level': 10
                                },
                          {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama C',
                                    'level': 10
                                },
                          {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama D',
                                    'level': 10
                                },
                          {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama E',
                                    'level': 12
                                },
                          {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama F',
                                    'level': 12
                                },
                          {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama G',
                                    'level': 12
                                },
                          {'template_name': 'Hitodama',
                                'unit_name': 'Hitodama H',
                                    'level': 12
                                },

                          {'template_name': 'Kodama Lord',
                                'unit_name': 'Kodama Lord',
                                'level': 9},

                          {'template_name': 'Yuyuko',
                             'unit_name': 'Yuyuko',
                             'level': 10
                          },

                          {'template_name': 'Yukari',
                             'unit_name': 'Yukari',
                             'level': 16
                          }

                            ]

        initial_spells = {'Misaki':["Iwanaga's Flames", "Withering Fall"],
                          'Hitodama A':['Fireball'],
                          'Hitodama B':['Holy Amulet'],
                          'Hitodama C':['Leaf Crystal'],
                          'Hitodama D':['Dagger Throw'],


                          'Hitodama E':['Fireball'],
                          'Hitodama F':['Holy Amulet'],
                          'Hitodama G':['Leaf Crystal'],
                          'Hitodama H':['Dagger Throw'],

                          'Kodama Lord':['Leaf Crystal']

                            }
        initial_traits = {'Misaki':['Holy Tree Charm']}
        initial_ai_states = {'Misaki':'Attack',
                             'Hitodama A':'Defend',
                             'Hitodama B':'Defend',
                             'Hitodama C':'Defend',
                             'Hitodama D':'Defend',
                             'Hitodama E':'Defend',
                             'Hitodama F':'Defend',
                             'Hitodama G':'Defend',
                             'Hitodama H':'Defend', }

        initial_locations = {'Misaki':(12, 13),
                              'Kodama Lord':(12, 15),

                              'Youmu': (12, 18),
                              'Aya': (11, 18),
                              'Ran': (11, 19),
                              'Chen': (11, 20),
                              'Reimu': (12, 19),
                              'Marisa': (12, 20),
                              'Keine': (13, 19),
                              'Mokou': (13, 20),

                              }
        reserve_units = ['Hitodama %s' % letter for letter in 'ABCDEFGH'] #[list of unit names to deploy later in mission]
        reserve_units.append('Yuyuko')
        reserve_units.append('Yukari')
        all_landmarks = [
                            {'name':'Torii',
                             'id_string':'small_torii',
                             'location':(12, 8)
                        },
                            {'name':'Tree',
                             'id_string':'cherryblossom_tree',
                             'location':(12, 7)
                        },

        ]

        required_starters = ['Youmu', 'Marisa', 'Reimu', 'Ran', 'Chen', 'Mokou', 'Keine', 'Aya']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [Misaki1(), Misaki2(), Misaki3(), Misaki4(), Misaki5()]
        required_survivors = ['Misaki', 'Youmu', 'Marisa', 'Reimu', 'Ran', 'Chen', 'Mokou', 'Keine', 'Aya']
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

        # Initialize spirit source points
        ssp_list = [SpiritSourcePoint('NorthWest', (3, 7), 2), SpiritSourcePoint('SouthWest', (3, 16), 2),
                    SpiritSourcePoint('NorthEast', (21, 7), 2), SpiritSourcePoint('SouthEast', (21, 16), 2)]

        map(self.map.add_ssp, ssp_list)
        self.set_invincibility_state('Misaki', True)
        self.set_spell_lock('Misaki', True)

        # Disables Misaki going after SSPs
        self.map.all_units_by_name['Misaki'].ai.current_state.pursue_ssp = False
        self.set_cursor_state(False)
        self.set_stats_display(False)

        # Hero party confronts a Kodama Lord already fighting Misaki
        self.play_music('battle04')
        self.center_on('Youmu')
        self.say("We're here at last!",
                    'Youmu',
                    'Youmu')
        self.say('Yeah, but someone beat us to it.',
                    'Mokou',
                    'Mokou')
        self.say("Ha, what rotten luck. All the fairies have already scattered. So be it. I'll just have to take you on myself, Misaki.",
                'Kodama Lord',
                'Kodama')
        self.say('Oh...',
            'Misaki',
            'Misaki')

        # Kodama lord fights Misaki. Gets beaten pretty badly
        self.script_battle('Kodama Lord',
                           'Misaki',
                            {'lhs_equip':0,
                             'rhs_equip':0,
                             'lhs_hit':False,
                             'lhs_crit':False,
                             'rhs_hit':True,
                             'rhs_crit':True})
        self.startle('Kodama Lord')

        self.say("Gah! Hngh! This can't...be! I... I...",
            'Kodama Lord',
            'Kodama')

        # Kodama Lord attempts to escape but is blocked by the party
        self.move_unit('Kodama Lord', (13, 17))

        self.say("She's too strong! Augh...ha... Re...retreat! All of you!",
            'Kodama Lord',
            'Kodama')
        self.emote('Kodama Lord', 'exclamation')
        self.say("...Haha, it's you...hngh...fools. Not even you stand a chance...against Misaki.",
            'Kodama Lord',
            'Kodama')
        self.say("Get out of here...if you want to live to see...another day.",
            'Kodama Lord',
            'Kodama')

        # Party lets her retreat
        self.move_unit('Keine', (14, 19))
        self.move_unit('Mokou', (14, 20))
        self.move_unit('Kodama Lord', (13, 30))
        self.kill_unit('Kodama Lord')
        self.move_unit('Keine', (13, 19))
        self.move_unit('Mokou', (13, 20))

        # Misaki confronts party
        self.emote('Misaki', 'scribble')
        self.say("Those Kodama sought the goddess Iwanaga's gift of immortality that lies deep in our mountain. Though you seem different, I presume your desires are the very same.",
            'Misaki',
            'Misaki')
        self.say("Lady Misaki, we mean you nor this sacred ground any harm.",
            'Youmu',
            'Youmu')
        self.say("Iwanaga's gift of immortality? No one should have that gift.",
            'Mokou',
            'Mokou')
        self.say("You say that only because her flames already rest within you. The gift is already yours. Indeed, it is much more a curse than a gift, is it not?",
            'Misaki',
            'Misaki')
        self.startle('Mokou')
        self.say("A curse? Sure. But it doesn't matter. I've learned to accept my place.",
            'Mokou',
            'Mokou')
        self.say("I've met all of my wonderful friends thanks to this curse. They may come and go, but they all live on in me. So I'm fine.",
            'Mokou',
            'Mokou')
        self.say("Anyway, that's enough about me. We're here to stop your daughter.",
            'Mokou',
            'Mokou')
        self.say("Fuyuhana's actions threaten to break the delicate balance of Gensokyo, endangering all those who call it home. We humbly request that you help us stop her. In the name of our wonderful world!",
            'Youmu',
            'Youmu')
        self.say("Very well, I'll humor you. What is needed to stop Fuyuhana will only be bestowed upon those with sufficient strength and will. I ask you now... Prove to me your worth by defeating me in battle!",
            'Misaki',
            'Misaki')

        # Show a barrier animation around Misaki. Reimu senses its nature
        self.play_sfx('miss')
        self.show_animation('barrier_spell', (12, 13))
        self.startle('Reimu')
        self.say("Ugh!",
            'Reimu',
            'Reimu')
        self.say("What's wrong, Reimu?",
            'Marisa',
            'Marisa')
        self.say("Something felt off when we watched that Kodama Lord fight her. Now I see what it was.",
            'Reimu',
            'Reimu')
        self.say("Misaki's is completely surrounded by a powerful barrier. Its sheer strength sends shivers down my spine.",
            'Reimu',
            'Reimu')
        self.say("You mean it's so powerful that even Marisa's Master Spark won't break it?",
            'Chen',
            'Chen')
        self.say("Master Spark? I'd be surprised if that could even dent it! I doubt that even Yukari could break this thing!",
            'Reimu',
            'Reimu')
        self.say("I feel the same as Reimu. I don't know anyone capable of breaking that barrier!",
            'Ran',
            'Ran')

        # Center camera on one of the four spirit source points in the map
        self.set_cursor_state(True)
        self.center_on_coords((3, 7))
        self.say("But... Look over there at those spirit source points! Misaki must be drawing her power from the mountain itself. Do you see where I'm going, Youmu?",
            'Ran',
            'Ran')
        self.say("Yes! If we seal them, Misaki's barrier should falter! We can't give up yet.",
            'Youmu',
            'Youmu')

        self.set_cursor_state(False)

        # Go back to the party for one last line before the battle starts.
        self.stop_music()
        self.center_on('Youmu')
        self.play_music('battle05')
        self.say("Then what are we waiting for? Let's seal 'em up fast before Misaki pulverizes us!",
            'Marisa',
            'Marisa')



        self.set_cursor_state(True)
        self.set_stats_display(True)

class Misaki1(MapActionEvent):
    def __init__(self):
        # Triggers on all SSPs captured
        triggers = [SSPStateTrigger('NorthWest', 1),
                    SSPStateTrigger('NorthEast', 1),
                    SSPStateTrigger('SouthEast', 1),
                    SSPStateTrigger('SouthWest', 1),
                    ]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        # Misaki is impressed that the party discovered how to break her barrier.
        self.center_on('Misaki')
        self.say("Thinking clearly under pressure... Impressive. A marked improvement over those Kodama who did nothing but attack my barrier.",
            'Misaki',
            'Misaki')

        # Reimu senses barrier is down. If she's not in the party a generic line is said.
        if 'Reimu' in self.map.all_units_by_name.keys() and self.map.all_units_by_name['Reimu'].alive:
            self.center_on('Reimu')
            self.emote('Reimu', 'exclamation')
            self.say("There! Misaki's barrier is broken! Now's our chance!",
                'Reimu',
                'Reimu')
        else:
            self.say("Misaki's barrier is down. She is now vulnerable to attack.",
                    None,
                    None)

        self.set_invincibility_state('Misaki', False)
        self.set_equip('Misaki', 'Withering Fall')

class Misaki2(MapActionEvent):
    def __init__(self):
        # Triggers on turn 2

        triggers = [UnitHPBelowTrigger('Misaki', 300), UnitAliveTrigger('Misaki', True)]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        # Misaki summons guardian orbs
        self.center_on('Misaki')
        self.say("Guardians of Iwanaga's fires, arise!",
                "Misaki",
                "Misaki")

        self.set_invincibility_state('Misaki', True)

        # Equip Misaki with her more powerful spell
        self.set_equip('Misaki', "Iwanaga's Flames")

        # Switch the SSP state of all SSPs
        self.set_ssp_state('NorthWest', 2)
        self.set_ssp_state('NorthEast', 2)
        self.set_ssp_state('SouthWest', 2)
        self.set_ssp_state('SouthEast', 2)

        ssp_coords = ((3, 7), (3, 16), (21, 7), (21, 16))

        # if a unit is currently standing on the SSP while it switches states, teleport them to the middle of the map
        deploy_set = 'ABCD'

        for index, coord in enumerate(ssp_coords):

            unit_name = self.map.check_occupancy(coord)

            if unit_name:
                self.center_on_coords(coord)
                self.play_sfx('fire2')
                self.show_animation('fire_spell', coord)
                self.random_teleport(unit_name, (6, 7, 8, 11))
                self.center_on(unit_name)
                self.emote(unit_name, 'questionmark')

            # Deploy the Hitodama
            self.center_on_coords(coord)
            letter = deploy_set[index]
            self.deploy_unit('Hitodama %s'%letter, coord)
            self.pause(0.5)

        # Show barrier animation to indicate that Misaki is invincible again.
        self.center_on('Misaki')
        self.play_sfx('miss')
        self.show_animation('barrier_spell', tuple(self.map.all_units_by_name['Misaki'].location_tile))
        self.set_cust_var('Phase 2', True)


class Misaki3(MapActionEvent):
    def __init__(self):
        # Triggers on all SSPs captured
        triggers = [SSPStateTrigger('NorthWest', 1),
                    SSPStateTrigger('NorthEast', 1),
                    SSPStateTrigger('SouthEast', 1),
                    SSPStateTrigger('SouthWest', 1),
                    CustVarTrigger('Phase 2', True)
                    ]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        # Same thing as last time barrier goes down, but with Marisa
        if 'Marisa' in self.map.all_units_by_name.keys() and self.map.all_units_by_name['Marisa'].alive:
            self.center_on('Marisa')
            self.emote('Marisa', 'exclamation')
            self.say("Whoa! Hey, her barrier collapsed! And now her magic is getting sucked right into the mountain!",
                'Marisa',
                'Marisa')
        else:
            self.say("Misaki's barrier is down. She is now vulnerable to attack.",
                None,
                None)

        self.set_equip('Misaki', 'Withering Fall')
        self.set_invincibility_state('Misaki', False)

class Misaki4(MapActionEvent):
    def __init__(self):
        # Triggers on turn 2

        triggers = [UnitHPBelowTrigger('Misaki', 150), UnitAliveTrigger('Misaki', True)]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        self.center_on('Misaki')
        self.say("Let's see you fare against these guardians!",
            "Misaki",
            "Misaki")

        self.set_invincibility_state('Misaki', True)

        # Equip Misaki with her more powerful spell
        self.set_equip('Misaki', "Iwanaga's Flames")

        # Switch the SSP state of all SSPs
        self.set_ssp_state('NorthWest', 2)
        self.set_ssp_state('NorthEast', 2)
        self.set_ssp_state('SouthWest', 2)
        self.set_ssp_state('SouthEast', 2)

        ssp_coords = ((3, 7), (3, 16), (21, 7), (21, 16))

        # if a unit is currently standing on the SSP while it switches states, teleport them to the middle of the map
        deploy_set = 'EFGH'

        for index, coord in enumerate(ssp_coords):

            unit_name = self.map.check_occupancy(coord)

            if unit_name:
                self.center_on_coords(coord)
                self.play_sfx('fire2')
                self.show_animation('fire_spell', coord)
                self.random_teleport(unit_name, (6, 7, 8, 11))
                self.center_on(unit_name)
                self.emote(unit_name, 'questionmark')

            # Deploy the Hitodama
            self.center_on_coords(coord)
            letter = deploy_set[index]
            self.deploy_unit('Hitodama %s'%letter, coord)
            self.pause(0.5)

        self.center_on('Misaki')
        self.play_sfx('miss')
        self.show_animation('barrier_spell', tuple(self.map.all_units_by_name['Misaki'].location_tile))
        self.set_cust_var('Phase 3', True)

class Misaki5(MapActionEvent):
    def __init__(self):
        # Triggers on all SSPs captured
        triggers = [SSPStateTrigger('NorthWest', 1),
                    SSPStateTrigger('NorthEast', 1),
                    SSPStateTrigger('SouthEast', 1),
                    SSPStateTrigger('SouthWest', 1),
                    CustVarTrigger('Phase 3', True)
                    ]

        MapActionEvent.__init__(self, triggers)

    def execute(self):

        # Final time Misaki's barrier goes down
        if 'Ran' in self.map.all_units_by_name.keys() and self.map.all_units_by_name['Ran'].alive:
            self.center_on('Ran')
            self.emote('Ran', 'exclamation')
            self.say("She's on her last legs! I don't think she'll be able to raise her barrier again! Let's take her down once and for all!",
                'Ran',
                'Ran')
        else:
            self.say("Misaki's barrier is down. She is now vulnerable to attack.",
                None,
                None)


        self.set_equip('Misaki', "Withering Fall")
        self.set_invincibility_state('Misaki', False)


class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.set_unit_pos('Misaki', (12, 13))

        self.set_unit_pos('Youmu', (12, 15))
        self.set_unit_pos('Ran', (9, 16))
        self.set_unit_pos('Chen', (10, 17))
        self.set_unit_pos('Mokou', (11, 17))
        self.set_unit_pos('Aya', (12, 17))
        self.set_unit_pos('Keine', (13, 17))
        self.set_unit_pos('Marisa', (14, 17))
        self.set_unit_pos('Reimu', (15, 16))


    def execute(self):

        self.stop_music()
        self.play_music('event02')

        # End of battle conversation with Misaki
        self.center_on('Youmu')
        self.say("Wonderfully executed. I concede. Your strong devotion to the presevation of our world's balance is clear.",
            'Misaki',
            'Misaki')
        self.say("Look, we almost died there. Now can you do something about that kid of yours and her hissy fit that's gonna destroy Gensokyo as we know it? Sheesh! I swear...",
            'Marisa',
            'Marisa')
        self.say("We are protectors, not conquerors. I understand her motivations. However, it is not our place to impose our desires upon this world.",
            'Misaki',
            'Misaki')
        self.say("She is punishing Gensokyo for its treatment of the forest, but she is destroying Gensokyo in the process. So yes. I will assist you as promised.",
            'Misaki',
            'Misaki')
        self.say("How can we stop her?",
            'Youmu',
            'Youmu')
        self.say("She is an incredibly powerful Kodama Lord, as you know. However, upon her demise, her powers will increase considerably.",
            'Misaki',
            'Misaki')
        self.say("The fires of Iwanaga preserved her ghost in a limbo between life and death. To this day, she still holds onto that final curse.",
            'Misaki',
            'Misaki')
        self.say("If she is defeated, the destruction she will cause then will be unimaginable. Every crisis thus far will pale in comparison.",
            'Misaki',
            'Misaki')
        self.say("But Gensokyo will dry up and wilt if she's allowed to continue.",
            'Mokou',
            'Mokou')
        self.say("Fuyuhana's power is to gather clouds; however, clouds will only gather around Fuyuhana in her corporeal form.",
            'Misaki',
            'Misaki')
        self.say("So we need to take her physical body away from her without killing her. That holy branch is her anchor to the world of the living.",
            'Reimu',
            'Reimu')
        self.say("Then... The Lantern of Souls! It attracts ghosts, so if we can separate her spirit from her body...",
            'Youmu',
            'Youmu')

        self.emote('Misaki', 'heart')
        self.say("Well done, Youmu. Take this, a drop of sap from the tree that I've kept constant vigil over.",
            'Misaki',
            'Misaki')
        self.say("If you burn it as the lantern's oil, you'll be able to separate Fuyuhana's spirit from the holy branch. She cannot resist the call of Iwanaga's flame.",
            'Misaki',
            'Misaki')
        self.say("Alas, I cannot abandon this mountain, no matter what my heart desires. This is all I can do to assist you.",
            'Misaki',
            'Misaki')
        self.say("Know that my prayers are with you. Please help my daughter.",
            'Misaki',
            'Misaki')
        self.say("I understand. Farewell, Misaki. Thank you for everything.",
            'Youmu',
            'Youmu')

        # Misaki vanishes
        self.show_animation('fire_spell', (12, 13))
        self.kill_unit('Misaki')

        self.say("All right, that was great and all, but your lantern is broken, Youmu. We'll have to fix it. How old is this beat up thing anyway?",
            'Reimu',
            'Reimu')
        self.say("Quite old, I imagine. It's been in my mistress's care since before I was born.",
            'Youmu',
            'Youmu')

        # Yuyuko and Yukari make an appearance at last
        self.fade_to_color('white', 1.0)
        self.deploy_unit('Yuyuko', (11, 20))
        self.deploy_unit('Yukari', (13, 20))
        self.play_music('event01')
        self.fade_from_color('white', 1.0)

        self.say("Ohohoho! At long last, it's my time to shine!",
            'Yuyuko',
            'Yuyuko')
        self.say("So are we late? Yuyuko wanted to stop for snacks at a Tengu city on our way here. Not a vacation she says, huh...",
            'Yukari',
            'Yukari')

        # Youmu runs up to Yuyuko
        self.startle('Youmu')
        self.emote('Youmu', 'exclamation')
        self.move_unit('Aya', (12, 18))
        self.move_unit('Aya', (11, 18))
        self.move_unit('Youmu', (12, 19))
        self.move_unit('Youmu', (11, 19))

        self.say("Madam Yuyuko!",
            'Youmu',
            'Youmu')
        self.emote('Chen', 'musicnote')
        self.say("Madam Yukari! Hello!",
            'Chen',
            'Chen')
        self.say("About time you two showed your faces. What have you two been up to anyway? Going on an extended date?",
            'Reimu',
            'Reimu')
        self.say("Hey! We've been busy, too.",
            'Yukari',
            'Yukari')
        self.say("Madam Yuyuko, why didn't you tell me where you were going?",
            'Youmu',
            'Youmu')
        self.say("Oh, um. You see, Yukari showed up that night and dragged me off to a lovely picnic in the forest. We were going to meet this ghost who had been appearing in the forest recently.",
            'Yuyuko',
            'Yuyuko')
        self.emote('Youmu', 'dotdotdot')
        self.say("I'm so sorry, Youmu, sweetie! Yukari insisted that we keep this a secret. So I did! I didn't mean to worry you.",
            'Yuyuko',
            'Yuyuko')
        self.say("You can probably guess that things didn't go exactly as planned.",
            'Yukari',
            'Yukari')
        self.say("What? You guys got beaten up by Fuyuhana? You're kidding, right? You'd better be kidding.",
            'Marisa',
            'Marisa')
        self.say("Nope, no joking around here. Then she ran away as soon as one of her lieutenants managed to knock the lantern out of Yuyuko's hand.",
            'Yukari',
            'Yukari')
        self.say("Oh yeah, she's getting steadily more powerful, too. She's almost at the point where she's at the same level as when she reigned over the Forest of Magic centuries ago.",
            'Yukari',
            'Yukari')
        self.say("Her underlings, especially Ayaka, are nothing to sneeze at either. So pardon us for joining you late.",
            'Yukari',
            'Yukari')
        self.say("If you say so. Where to next, madam?",
            'Ran',
            'Ran')
        self.say("Let's regroup at a place that's more comfortable! The outdoors are nice, but I don't feel like it right now. Oh, and I could go for some tea.",
            'Yukari',
            'Yukari')
        self.say("A splendid idea, Yukari! Tea sounds wonderful right now! Let's throw a tea party while we're at it!",
            'Yuyuko',
            'Yuyuko')
        self.say("My article's moving along quite nicely! Oh, but I'm sure the Tsubaki would want to hear from us, too. Y'know, before my newspaper's out.",
            'Aya',
            'Aya')
        self.say("I agree. Everyone, let's return to the outpost. I want to make sure Nitori and Momiji are well before we continue onward.",
            'Youmu',
            'Youmu')





