from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, ArrivalTrigger

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'River Basin Rumble'
        location = 'River Basin'
        id_string = 'CH3ST1'
        prereqs = ['CH2ST5']
        show_rewards = True
        desc = "Youkai Mountain's Wolf Tengu defense force is on high alert this morning. A recent attack by the Kodama Lords was successfully repelled by Momiji, captain of the Wolf Tengu guards. Her wolves along with their volant Crow Tengu allies have scattered the razed remains of fallen trees in their wake. This has given the elder Tengu great cause for concern regarding these conflicts just beyond the mountain."

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch3st1.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat Boss',
                     'target':'Momiji',
                     'desc':'Defeat Momiji the Wolf Tengu!'
                     }

        deploy_data = {'enable':True,
                       'max_units':8,
                       'preset_units':{},
                       'boxes':[(6, 35, 2, 2), (14, 35, 2, 2)],
                       'default_locations':{'Youmu':(7,35),
                                            'Alice':(7,36),
                                            'Mokou':(6,35),
                                            'Keine':(6,36),
                                            'Ran':(14,35),
                                            'Chen':(14,36),
                                            'Reimu':(15,36),
                                            'Marisa':(15,35),
                                            },
                       }

        reward_list = [('treasure', 'synth_metal'),
                       ('treasure', 'synth_wood'),
                      ]

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Momiji',
                                'unit_name': 'Momiji',
                                    'level': 10},
                         {'template_name': 'Nitori',
                                'unit_name': 'Nitori',
                                    'level': 10},

                         {'template_name': 'Kappa',
                                'unit_name': 'Kappa A',
                                'level':9},
                        {'template_name': 'Kappa',
                                   'unit_name': 'Kappa B',
                                   'level':9},
                        {'template_name': 'Kappa',
                                   'unit_name': 'Kappa C',
                                   'level':9},

                        {'template_name': 'Kappa',
                             'unit_name': 'Kappa Medic',
                                 'level': 9},


                         {'template_name': 'Crow Tengu',
                                'unit_name': 'Crow Tengu A',
                                    'level': 8},
                         {'template_name': 'Crow Tengu',
                                'unit_name': 'Crow Tengu B',
                                    'level': 8},
                         {'template_name': 'Crow Tengu',
                                'unit_name': 'Crow Tengu C',
                                    'level': 8},

                        {'template_name': 'Wolf Tengu',
                            'unit_name': 'Wolf Tengu A',
                            'level': 8},
                        {'template_name': 'Wolf Tengu',
                            'unit_name': 'Wolf Tengu B',
                            'level': 8},
                        {'template_name': 'Wolf Tengu',
                            'unit_name': 'Wolf Tengu C',
                            'level': 8},
                        {'template_name': 'Wolf Tengu',
                            'unit_name': 'Wolf Tengu D',
                            'level': 8},
                        {'template_name': 'Wolf Tengu',
                            'unit_name': 'Wolf Tengu E',
                            'level': 8},
                        {'template_name': 'Wolf Tengu',
                            'unit_name': 'Wolf Tengu F',
                            'level': 8},
                        {'template_name': 'Wolf Tengu',
                            'unit_name': 'Wolf Tengu G',
                            'level': 8},
                        {'template_name': 'Aya',
                            'unit_name': 'Aya',
                            'level': 10},

                        {'template_name': 'Crow Tengu',
                            'unit_name': 'Crow Tengu E',
                                'level': 8},
                        {'template_name': 'Crow Tengu',
                            'unit_name': 'Crow Tengu F',
                                'level': 8},


                          ]

        initial_spells = {'Momiji':['Dagger Throw'],
                          'Nitori':['Tanabata Festival'],
                          'Crow Tengu A':['Weakening Amulet'],
                          'Crow Tengu B':['Barrier Buster'],
                          'Crow Tengu C':['Weakening Amulet'],
                          'Kappa A':['Illusion Veil', 'Fireball'],
                          'Kappa B':['Encourage', 'Fireball'],
                          'Kappa C':['Life Bless', 'Fireball'],
                          'Wolf Tengu A':['Dagger Throw'],
                          'Wolf Tengu B':['Dagger Throw'],
                          'Wolf Tengu C':['Dagger Throw'],
                          'Wolf Tengu D':['Dagger Throw'],
                          'Wolf Tengu E':['Dagger Throw'],
                          'Wolf Tengu F':['Dagger Throw'],
                          'Wolf Tengu G':['Dagger Throw'],

                          'Kappa Medic':['Healing Drop'],
        }

        initial_traits = {'Momiji':['Attack+ Lv.1'],
                          'Crow Tengu A':['Flight'],
                          'Crow Tengu B':['Flight'],
                          'Crow Tengu C':['Flight'],
                          'Kappa A':['Swimming'],
                          'Kappa B':['Swimming'],
                          'Kappa C':['Swimming'],
                          'Kappa Medic':['Mirage', 'Swimming'],
                          'Nitori':['Danmaku Sniper', 'Swimming']
        }
        initial_ai_states = {'Momiji':'Attack',
                             'Nitori':'Attack',
                             'Crow Tengu A':'Pursuit',
                             'Crow Tengu B':'Pursuit',
                             'Crow Tengu C':'Pursuit',
                             'Kappa A':'Support',
                             'Kappa B':'Support',
                             'Kappa C':'Support',
                             'Wolf Tengu A':'Attack',
                             'Wolf Tengu B':'Attack',
                             'Wolf Tengu C':'Attack',
                             'Wolf Tengu D':'Attack',
                             'Wolf Tengu E':'Attack',
                             'Wolf Tengu F':'Attack',
                             'Wolf Tengu G':'Attack',
                             'Kappa Medic':'HealerStandby',

                             }

        initial_locations = {
                             # Tengu Lookout


                             'Youmu':(6, 35),
                             'Keine':(5, 36),
                             'Mokou':(7, 36),

                             'Ran':(12, 36),
                             'Chen':(12, 37),
                             'Marisa':(13, 36),
                             'Reimu':(13, 37),


                             # Forward scout party
                             'Wolf Tengu F':(9, 25),
                             'Wolf Tengu G':(8, 24),
                             'Crow Tengu C':(6, 23),
                             'Kappa A':(7, 24),
                             'Kappa B':(14, 9),
                             'Kappa C':(15, 9),


                             'Wolf Tengu A':(20, 9),
                             'Wolf Tengu B':(19, 9),
                             'Wolf Tengu C':(23, 10),
                             'Wolf Tengu D':(20, 11),
                             'Wolf Tengu E':(21, 11),

                             'Crow Tengu A':(20, 14),
                             'Crow Tengu B':(21, 14),

                             'Kappa Medic':(18, 9)

                             }
        reserve_units = ['Momiji', 'Nitori', 'Aya', 'Crow Tengu E', 'Crow Tengu F']#[list of unit names to deploy later in mission]
        all_landmarks = [
                         {'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(22, 31)},

                         # Rocks
                        {'name':'SR1',
                         'id_string':'small_rock',
                         'location':(8, 16)},
                        {'name':'SR2',
                         'id_string':'small_rock',
                         'location':(19, 19)},
                        {'name':'SR3',
                         'id_string':'small_rock',
                         'location':(23, 15)},
                        {'name':'BR1',
                         'id_string':'big_rock',
                         'location':(22, 14)},
                        {'name':'BR2',
                         'id_string':'big_rock',
                         'location':(13, 11)},
                        {'name':'SR4',
                         'id_string':'small_rock',
                         'location':(14, 12)},

                         #Houses
                        {'name':'Island House',
                         'id_string':'house_1',
                         'location':(13, 12)},
                        {'name':'East House',
                         'id_string':'house_1',
                         'location':(22, 15)},


                         #Lilypads
                         {'name':'LP1',
                          'id_string':'lilypad',
                          'location':(4, 12)},
                         {'name':'LP2',
                          'id_string':'lilypad',
                          'location':(8, 20)},
                         {'name':'LP3',
                          'id_string':'lilypad',
                          'location':(10, 7)},
                         {'name':'LP4',
                          'id_string':'lilypad',
                          'location':(12, 21)},


                         ]

        required_starters = ['Youmu', 'Chen', 'Ran', 'Reimu', 'Marisa', 'Keine', 'Mokou']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [TreasureFoundMAE()
                                ]
        post_mission_MAE = PostMissionMAE()
        required_survivors = ['Youmu', 'Chen', 'Ran', 'Reimu', 'Marisa', 'Keine', 'Mokou', 'Nitori', 'Momiji', 'Wolf Tengu A']

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
        Mission Prologue: Momiji
        """
        self.set_stats_display(False)
        self.set_cursor_state(False)

        self.play_music('event03')
        # Party approaches the river from the south
        self.center_on('Marisa')
        self.say("There are so many Tengu out right now, I couldn't even begin to count 'em! Sheesh!",
                 'Marisa',
                 'Marisa')
        self.say("Right? There were a lot less the last time we were here, and they were still a royal pain in the rear! With this many... You know what, I don't even want to think about it.",
                 'Reimu',
                 'Reimu')
        self.say("Don't let your guards down. I see someone coming down the mountain towards us.",
                 'Youmu',
                 'Youmu')
        self.show_chapter_title(3)

        # Wolf tengu discussing their recent encounters, but the Crow Tengu aren't impressed
        self.center_on('Wolf Tengu A')

        self.startle('Wolf Tengu A')
        self.say("Ugh. When is Momiji going to get here?",
                 'Wolf Tengu A',
                 'Wolf Tengu')

        self.emote('Wolf Tengu B', 'exclamation')
        self.say("Wait, wait, wait. You mean THE Momiji? I heard she can bring down one of Fuyuhana's trees in a single strike!",
                 'Wolf Tengu B',
                 'Wolf Tengu')
        self.say("She even singlehandedly drove them off and stopped them in their tracks before they managed to reach this mountain. She's coming HERE?",
                 'Wolf Tengu B',
                 'Wolf Tengu')

        self.move_unit('Crow Tengu A', (19, 13))
        self.emote('Crow Tengu A', 'scribble')
        self.say("You don't even know what your own leader is up to? Please. You wolves are all brawn and no brains.",
                 'Crow Tengu A',
                 'Crow Tengu')
        self.say("All I need to do is cast this Weakening Amulet curse, and you'd be as vulnerable as a newborn puppy.",
                 'Crow Tengu A',
                 'Crow Tengu')

        self.emote('Wolf Tengu A', 'annoyed')
        self.say("What did you just say? How dare you look down on us! You crows can't even face anything head-on! You're all a bunch of pompous, feathered cowards!",
                 'Wolf Tengu A',
                 'Wolf Tengu')

        self.emote('Crow Tengu A', 'scribble')

        self.say("Ha! Unlike you lot, we Crow Tengu rule the skies. Our library of curses makes us invincible.",
                 'Crow Tengu A',
                 'Crow Tengu')
        self.say("With it, we can stop any enemy dead in their tracks. My dear little puppies, please, leave Fuyuhana's pathetic trees to us.",
                 'Crow Tengu A',
                 'Crow Tengu')

        self.startle('Crow Tengu B')
        self.say("Indeed, if Lord Tenma hadn't ordered us to \"assist\" you, we could easily protect this mountain on our own. So just stay out of our way, am I understood?",
                 'Crow Tengu A',
                 'Crow Tengu')

        self.startle('Wolf Tengu B')
        self.say("Hmph. Like we'd let you steal all the glory.",
                 'Wolf Tengu B',
                 'Wolf Tengu')

        # Momiji and Nitori arrive, they seem to be talking about something
        self.deploy_unit('Momiji', (15, -1))
        self.deploy_unit('Nitori', (15, -1))

        self.move_unit('Momiji', (13, 5))
        self.move_unit('Nitori', (13, 4))
        self.emote('Nitori', 'heart')
        self.emote('Momiji', 'questionmark')

        self.move_unit('Momiji', (15, 7))
        self.move_unit('Nitori', (14, 7))
        self.emote('Nitori', 'lightbulb')
        self.startle('Momiji')

        self.move_unit('Momiji', (17, 8))
        self.move_unit('Nitori', (16, 8))
        self.emote('Momiji', 'annoyed')

        self.say("Enough bickering, all of you! Wolf Tengu. Crow Tengu. Form up!",
                 'Momiji',
                 'Momiji')

        self.say("You heard her! Form up!",
                 'Wolf Tengu C',
                 'Wolf Tengu')

        # Tengu units form up
        self.move_unit('Wolf Tengu C', (21, 9))
        self.move_unit('Wolf Tengu D', (20, 10))
        self.move_unit('Crow Tengu A', (20, 11))
        self.startle('Crow Tengu A')
        self.move_unit('Wolf Tengu D', (19, 10))
        self.move_unit('Crow Tengu A', (20, 10))
        self.move_unit('Wolf Tengu E', (21, 10))
        self.move_unit('Crow Tengu B', (21, 11))
        self.move_unit('Kappa Medic', (19, 11))

        self.say("Listen up! We're here to protect the Kappa's water facilities from those pesky intruders. Any and all who trespass this mountain is our enemy, so show them no mercy! Got it?",
                 'Momiji',
                 'Momiji')

        self.center_on('Crow Tengu C')
        self.emote('Crow Tengu C', 'exclamation')
        self.say("Reporting! Momiji, a number of humans are approaching from downstream. We need to move immediately!",
                 'Crow Tengu C',
                 'Crow Tengu')

        self.play_music('battle02')

        self.center_on('Wolf Tengu A')
        self.say("Hmph, here already? Speak of the devil.",
                 'Wolf Tengu C',
                 'Wolf Tengu')

        self.emote('Momiji', 'exclamation')
        self.say("You came just in time. Well done. All right, everyone in position! Line up on both sides of the river! We'll stop them in their tracks!",
                 'Momiji',
                 'Momiji')

        self.fade_to_color('black', 0.5)

        # Forward two groups
        self.set_unit_pos('Crow Tengu A', (6, 23))
        self.set_unit_pos('Crow Tengu B', (16, 23))
        self.set_unit_pos('Crow Tengu C', (17, 23))
        self.set_unit_pos('Wolf Tengu A', (9, 25))
        self.set_unit_pos('Wolf Tengu B', (8, 24))
        self.set_unit_pos('Wolf Tengu C', (20, 25))

        # Nitori's Group
        self.set_unit_pos('Nitori', (11, 14))
        self.set_unit_pos('Kappa B', (10, 15))
        self.set_unit_pos('Kappa C', (12, 15))
        self.set_unit_pos('Wolf Tengu D', (10, 14))
        self.set_unit_pos('Wolf Tengu E', (12, 14))

        # Momiji's group
        self.set_unit_pos('Momiji', (20 , 8))
        self.set_unit_pos('Wolf Tengu F', (19, 7))
        self.set_unit_pos('Wolf Tengu G', (21, 9))
        self.set_unit_pos('Kappa Medic', (19, 9))

        self.fade_from_color('black', 0.5)

        self.center_on('Mokou')
        self.say("They're coming.",
                 'Mokou',
                 'Mokou')

        self.emote('Reimu', 'lightbulb')
        self.say("Crows and wolves, huh. There's no way they'd work together without a good leader...and just as I expected, there's good ol' Momiji. Shall we beat her up?",
                 'Reimu',
                 'Reimu')

        self.set_stats_display(True)
        self.set_cursor_state(True)

class TreasureFoundMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((22, 31, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Player has discovered treasure under cherry blossom tree
        """

        self.say("Buried at the foot of the cherry tree is a small rusted box.",
                None,
                None)
        self.say("Acquired Treasure Item: Gondolier's Glove!",
                None,
                None)
        self.add_item('treasure', '005_gondglove', 1)

class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):
        self.remove_all_enemies()
        self.stop_music()
        self.set_unit_pos('Momiji', (16, 6))
        self.set_unit_pos('Nitori', (17, 5))
        self.set_unit_pos('Wolf Tengu A', (17, 6))

        self.set_unit_pos('Ran', (17, 8))
        self.set_unit_pos('Youmu', (18, 8))
        self.set_unit_pos('Keine', (19, 8))

        self.set_unit_pos('Marisa', (16, 9))
        self.set_unit_pos('Chen', (17, 10))
        self.set_unit_pos('Mokou', (19, 10))
        self.set_unit_pos('Reimu', (20, 9))

    def execute(self):
        """
        Victory Scene
        """
        self.set_stats_display(False)
        self.set_cursor_state(False)

        # Hero group confronts Momiji
        self.center_on('Momiji')
        self.say("Not another step forward, any of you!",
                'Momiji',
                'Momiji')
        self.say("Please calm down, Momiji! We're not with Fuyuhana nor her trees.",
                 'Keine',
                 'Keine')

        self.say("Well, you certainly acted the part well enough, decimating my forces and all. I'll be needing more proof than that!",
                 'Momiji',
                 'Momiji')

        self.emote('Marisa', 'annoyed')
        self.say("Oh, please! You attacked us first! What did you want us to do? Just sit there and take it?",
                 'Marisa',
                 'Marisa')

        self.say("You trespassers shouldn't have set foot onto this mountain to begin with! The fault lies with you!",
                 'Momiji',
                 'Momiji')

        self.emote('Youmu', 'annoyed')
        self.emote('Momiji', 'annoyed')

        # Aya arrives with more Crow Tengu
        self.deploy_unit('Aya', (23, -1))

        self.deploy_unit('Crow Tengu E', (19, -1))
        self.deploy_unit('Crow Tengu F', (20, -1))

        self.move_unit('Aya', (21, 2))
        self.center_on('Aya')
        self.startle('Aya')
        self.play_sfx('camera')
        self.fade_to_color('white', 0.2)
        self.fade_from_color('white', 0.2)

        self.say("Ok. Ok. So how about this for a cool headline: \"Sudden change of heart! Heroes cruelly invade Tengu Homeland!\" Nice, huh? I'm so jotting that down.",
                 'Aya',
                 'Aya')

        self.move_unit('Crow Tengu E', (19, 6))
        self.move_unit('Crow Tengu F', (20, 7))

        # Aya circles around and takes pictures
        self.move_unit('Aya', (21, 12))
        self.startle('Aya')
        self.play_sfx('camera')
        self.fade_to_color('white', 0.2)
        self.fade_from_color('white', 0.2)

        self.move_unit('Aya', (15, 12))
        self.startle('Aya')
        self.play_sfx('camera')
        self.fade_to_color('white', 0.2)
        self.fade_from_color('white', 0.2)

        self.move_unit('Aya', (15, 6))
        self.startle('Aya')
        self.play_sfx('camera')
        self.fade_to_color('white', 0.2)
        self.fade_from_color('white', 0.2)

        self.say("I was wondering when that nosy reporter was gonna show up.",
                 'Reimu',
                 'Reimu')

        self.say("Have you come...with reinforcements?",
                 'Youmu',
                 'Youmu')

        self.say("Nah! Actually I'm here on official business from the Great Tengu today, so feel free to relax already! You've earned it! Well, kinda.",
                 'Aya',
                 'Aya')

        self.emote('Wolf Tengu A', 'scribble')
        self.say("Ugh. I already know what's coming. Those snooty higher ups are going to turn our efforts on their heads like it's nothing, aren't they.",
                 'Wolf Tengu A',
                 'Wolf Tengu')

        self.say("Aya... You! Don't tell me you're just going to let these humans waltz their way their way into the mountain!",
                 'Momiji',
                 'Momiji')
        self.say("Tsk-tsk, Momiji! So sorry, but the command comes straight from Lord Tenma himself! We've been asked to meet an emissary at the foot of Moriya Shrine. So no disobeying, okie-doke?",
                 'Aya',
                 'Aya')

        self.say("Hmm. Moriya Shrine, huh? So are they getting dragged into this, too, or what?",
                 'Marisa',
                 'Marisa')
        self.say("Amazing reporter as I am, I...can't say yet! But, hey! It's pretty much the only neutral-ish territory here on the mountain, so.",
                 'Aya',
                 'Aya')
        self.say("Very well, then it's worth looking into. Everyone, let's go and hear what the Tengu have to say.",
                 'Youmu',
                 'Youmu')

        self.fade_to_color('black', 0.5)

        self.set_unit_pos('Youmu', (-1, -1))
        self.set_unit_pos('Reimu', (-1, -1))
        self.set_unit_pos('Mokou', (-1, -1))
        self.set_unit_pos('Ran', (-1, -1))
        self.set_unit_pos('Chen', (-1, -1))
        self.set_unit_pos('Keine', (-1, -1))

        self.kill_unit('Momiji')
        self.kill_unit('Aya')
        self.kill_unit('Crow Tengu E')
        self.kill_unit('Crow Tengu F')
        self.kill_unit('Wolf Tengu A')

        # Nitori and Marisa have a chat alone
        self.set_unit_pos('Marisa', (15, 6))
        self.set_unit_pos('Nitori', (16, 6))
        self.fade_from_color('black', 0.5)

        self.emote('Nitori', 'musicnote')
        self.say("Oh, hey, Marisa! I gotta say, I was super impressed by that fight just now!",
                 'Nitori',
                 'Nitori')
        self.say("Witnessing your woosh-shazam-ness of your Master Spark hits me in the heart right there, you know? Ohh, if only my rockets could compare!",
                 'Nitori',
                 'Nitori')

        self.say("Thanks! But come on, I can't take all the credit. I mean, you and your rockets? I gotta say, you were pretty darn cool! Awesomest battle I've seen in awhile!",
                 'Marisa',
                 'Marisa')

        self.say("Ohmigosh, hearing you say that makes me super duper happy like whoa! Um, um, so. It's just a prototype, but if you like it, I'm totally ok with handing it over!",
                 'Nitori',
                 'Nitori')

        self.emote('Marisa', 'exclamation')
        self.say("H-huh? Just like that? You're really ok with just giving it to me?",
                 'Marisa',
                 'Marisa')

        self.say("Heck yeah! I mean, I've heard about what's going on and what you're up to and stuff.",
                 'Nitori',
                 'Nitori')
        self.say("Us kappa are gonna do our part to protect this mountain, but I wanna do more, you know? So take this as a token of my helpfulness!",
                 'Nitori',
                 'Nitori')


        self.say("Acquired Nitori's latest invention: Tanabata Festival",
                None,
                None)
        self.add_item('spell_action', 'Tanabata Festival', 1)

        self.set_stats_display(True)
        self.set_cursor_state(True)
