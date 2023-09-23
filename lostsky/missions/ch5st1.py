from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'A Shining Horizon'
        location = 'Human Village'
        id_string = 'CH5ST1'
        prereqs = ['CH4ST5']
        show_rewards = False
        desc = "Victory! At the break of dawn today, the Kodama Lords and all their forces made a hasty retreat from the Bamboo Forest. Their leader Fuyuhana was permanently bound to the Forest of Magic, and Ayaka was defeated by Youmu and her party. As the dust settles in the Bamboo Forest, our heroes gather at the Human Village to plan their next moves."

        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch2st2.txt'
        mission_type = 'conversation'
        objective = None
        deploy_data = {}
        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Akyu',
                                 'unit_name': 'Akyu',
                                     'level': 5 },
                          {'template_name': 'Tsubaki',
                                 'unit_name': 'Tsubaki',
                                     'level': 5 },
                          ]

        initial_spells = {}
        initial_traits = {}
        initial_ai_states = {}
        initial_locations = {'Akyu':(14, 8),
                             'Keine':(15, 8),

                             'Youmu':(13, 6),
                             'Yukari':(11, 5),
                             'Ran':(11, 4),
                             'Chen':(10,5),

                             'Reimu':(13, 4),
                             'Marisa':(14, 4),

                             'Kaguya':(11, 7),
                             'Eirin':(10, 7),
                             'Reisen':(11, 8),
                             'Mokou':(12, 8),

                             'Aya':(29, 29),
                             }

        reserve_units = []
        all_landmarks = [{'name':'Akyu\'s House',
                          'id_string':'house_1',
                          'location':(14, 9)},

                          {'name':'House 2',
                          'id_string':'house_1',
                          'location':(10, 8)},
                          {'name':'House 3',
                          'id_string':'house_1',
                          'location':(14, 14)},
                          {'name':'House 4',
                          'id_string':'house_2',
                          'location':(10, 14)},
                          {'name':'House 5',
                          'id_string':'house_1',
                          'location':(5, 8)},
                          {'name':'House 6',
                          'id_string':'house_2',
                          'location':(18, 6)},
                          {'name':'House 7',
                          'id_string':'house_2',
                          'location':(24, 6)},
                          {'name':'House 8',
                          'id_string':'house_1',
                          'location':(25, 14)},
                          {'name':'House 9',
                          'id_string':'house_2',
                          'location':(5, 6)},

                          {'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(10, 9)},
                          {'name':'CB2',
                          'id_string':'cherryblossom_tree',
                          'location':(13, 8)},
                         ]

        required_starters = ['Chen', 'Ran', 'Youmu', 'Marisa', 'Reimu', 'Keine', 'Mokou', 'Aya', 'Kaguya', 'Reisen', 'Eirin', 'Yukari']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = []
        required_survivors = []
        post_mission_MAE = None

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
        Meeting with Akyu at her house
        """
        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.play_music('event03')
        self.center_on('Youmu')

        # Add YYK to the party
        self.add_to_party('Yuyuko')
        self.assign_spell('Yuyuko', 'Fireball')
        self.assign_spell('Yuyuko', 'Holy Amulet')
        self.assign_spell('Yuyuko', 'Resurrection Butterfly')
        self.set_unit_pos('Yuyuko', (14,6))

        self.say("It appears the curtains will finally fall on this latest crisis to befall Gensokyo! Well done.",
                'Akyu',
                'Akyu')

        self.emote('Chen', 'questionmark')

        self.say("Maybe, but... The sky is still bright blue. I don't see the clouds yet.",
                'Chen',
                'Chen')

        self.say("Indeed. However, my Crow Tengu scouts report that clouds are drifting away from the Forest of Magic.",
                 'Tsubaki',
                 'Tsubaki')

        self.set_unit_pos('Tsubaki', (12, 15))
        self.set_unit_pos('Aya', (11, 15))
        self.move_unit('Tsubaki', (12, 9))
        self.move_unit('Aya', (11, 9))


        self.play_sfx('camera')
        self.fade_to_color('white', 0.2)
        self.fade_from_color('white', 0.2)
        self.say("And snap! A perfect shot of the heroes that saved the day.",
                 'Aya',
                 'Aya')


        self.say("I believe that's a little premature, Aya.",
                 'Eirin',
                 'Eirin')
        self.say("What's the problem? All that's left is to put Fuyuhana to rest forever. That's the plan, right?",
                 'Marisa',
                 'Marisa')
        self.say("Oh, and get my house back. Those trees better not have stamped it down into a pile of rubble, or I'm gonna...",
                 'Marisa',
                 'Marisa')
        self.say("Tsubaki, do the Tengu know anything about the other Kodama Lords? We haven't heard from Haruna, Miu, or Kotone since we met them in the Bamboo Forest.",
                'Keine',
                'Keine')

        self.say("No. The minor Kodama have withdrawn to the Forest of Magic to regroup. Losing Ayaka dealt a heavy blow to their morale. They're on the defensive.",
                'Tsubaki',
                'Tsubaki')
        self.say("What? No way are we going to let the Kodama rebuild their tree armies! Let's just go in and blow them to pieces!",
                 'Reimu',
                 'Reimu')

        self.say("Oh, yeah. There are some rumors going around about the other Kodama Lords though.",
                'Aya',
                'Aya')
        self.say("So Haruna, the Kodama Lord that led the Youkai Mountain attack has been spotted in the river basin.",
                'Aya',
                'Aya')
        self.say("She's the least aggressive of the bunch, but some Kappa have reported that she and her fairies seem to be looking for some artifacts there.",
                'Aya',
                'Aya')


        self.say("Momiji mentioned after the Kodama Lord invasion that they sought something called an Otherworldly Mirror. Perhaps that?",
                'Tsubaki',
                'Tsubaki')
        self.startle('Marisa')
        self.say("Oh, brother. A secret weapon? I sure hope not.",
                 'Marisa',
                 'Marisa')

        self.say("As for Kotone, Wriggle told me that she was last seen taking refuge near Misty Lake.",
                'Aya',
                'Aya')
        self.say("And most mysteriously, Miu was was seen wandering near Gensokyo's border at the Hakurei Shrine.",
                'Aya',
                'Aya')
        self.say("Well, now! They're certainly worth further investigation if they're playing around at the border.",
                 'Yukari',
                 'Yukari')

        self.say("Then that leaves Fuyuhana. Youmu, the decision is yours. What will be our next course of action?",
                'Akyu',
                'Akyu')
        self.say("We could go for Fuyuhana right away, but I propose that we take care of these other Kodama Lords before they cause the people anymore trouble.",
                 'Youmu',
                 'Youmu')

        self.say("I see. Now, everyone. You have been traveling incessantly across Gensokyo, and I'm certain returning here from the Bamboo Forest must have been notoriously difficult.",
                'Akyu',
                'Akyu')
        self.say("We have ample time for now. Please, make yourselves comfortable and rest here this evening. You may resume your travels tomorrow.",
                'Akyu',
                'Akyu')
        self.say("An excellent proposal. I happen to have a bottle of our finest sake with me as well, so let us drink to our forthcoming victory!",
                'Tsubaki',
                'Tsubaki')

        self.fade_to_color('black', 1)

        self.set_unit_pos('Yuyuko', (12, 3))
        self.set_unit_pos('Yukari', (13, 3))
        self.set_unit_pos('Ran', (14, 3))
        self.set_unit_pos('Chen', (13, 2))
        self.set_unit_pos('Tsubaki', (11, 4))

        self.set_unit_pos('Kaguya', (9, 6))
        self.set_unit_pos('Mokou', (11, 6))
        self.set_unit_pos('Eirin', (8, 6))
        self.set_unit_pos('Reisen', (9, 5))

        self.set_unit_pos('Reimu', (15, 6))
        self.set_unit_pos('Youmu', (16, 6))
        self.set_unit_pos('Marisa', (17, 6))
        self.set_unit_pos('Keine', (15, 8))
        self.set_unit_pos('Akyu', (17, 8))
        self.set_unit_pos('Aya', (16, 7))

        self.set_bg_overlay('Night')
        self.fade_from_color('black', 1)


        self.center_on('Yukari')
        self.emote('Yukari', 'musicnote')
        self.emote('Tsubaki', 'dotdotdot')
        self.emote('Yuyuko', 'lightbulb')
        self.emote('Tsubaki', 'musicnote')
        self.startle('Ran')
        self.emote('Ran', 'dotdotdot')
        self.emote('Yukari', 'musicnote')


        self.center_on('Kaguya')
        self.emote('Kaguya', 'exclamation')
        self.startle('Mokou')
        self.emote('Mokou','scribble')
        self.move_unit('Mokou', (10,6))
        self.startle('Mokou')
        self.emote('Mokou','annoyed')

        self.center_on('Aya')
        self.emote('Aya', 'lightbulb')

        self.move_unit('Aya', (12, 7))
        self.center_on('Aya')

        self.play_sfx('camera')
        self.fade_to_color('white', 0.2)
        self.fade_from_color('white', 0.2)
        self.emote('Aya', 'musicnote')
        self.startle('Aya')

        self.emote('Kaguya', 'exclamation')
        self.emote('Eirin', 'musicnote')
        self.emote('Mokou', 'sweatdrop')
        self.emote('Mokou', 'musicnote')
        self.emote('Kaguya', 'musicnote')



        self.fade_to_color('black', 1)
        self.set_unit_pos('Eirin', (12, 4))
        self.set_unit_pos('Aya', (9, 5))
        self.set_unit_pos('Mokou', (-1, -1))


        self.set_unit_pos('Reimu', (11, 6))
        self.set_unit_pos('Marisa', (12, 6))
        self.set_unit_pos('Keine', (12, 7))
        self.set_unit_pos('Akyu', (11, 7))


        self.set_unit_pos('Youmu', (18, 12))

        self.fade_from_color('black', 1)
        self.play_music('event01')

        self.pause(0.2)

        self.set_unit_pos('Mokou', (14, 9))
        self.move_unit('Mokou', (14, 10))
        self.center_on('Youmu')
        self.move_unit('Mokou', (17, 12))


        self.say("I found you.",
                'Mokou',
                'Mokou')
        self.say("I apologize for leaving abruptly. I simply wanted some peace and quiet.",
                'Youmu',
                'Youmu')
        self.say("Youmu. You sure this is the way you want to end our journey?",
                'Mokou',
                'Mokou')
        self.say("Mokou, what do you mean?",
                'Youmu',
                'Youmu')

        self.say("So we beat the Kodama this time. Then in a few hundred years, they'll be back as the new Kodama grow up. We'll just repeat the cycle.",
                'Mokou',
                'Mokou')

        self.emote('Mokou', 'dotdotdot')
        self.say("Kaguya and I fought for centuries, and we still do. All over one insult to my family. Grudges linger, see.",
                'Mokou',
                'Mokou')
        self.say("Mm. Well, Mokou, do you know of another way to handle this situation?",
                'Youmu',
                'Youmu')

        self.say("Ha, I wish. I don't want Gensokyo to suffer a neverending cycle of revenge against the Kodama like Kaguya and me is all.",
                'Mokou',
                'Mokou')
        self.say("But you're the leader, so you decide. I just wanted to give my two cents is all.",
                'Mokou',
                'Mokou')

        self.startle('Marisa')
        self.center_on('Marisa')
        self.move_unit('Marisa', (16, 8))
        self.center_on('Marisa')


        self.say("Oh, hey! Youmu! Mokou! They're gonna start busting out the good stuff. You don't want to miss it, do you?",
                'Marisa',
                'Marisa')

        self.say("I'll be right there, Marisa! Thank you, Mokou. I'll keep your words in mind.",
                'Youmu',
                'Youmu')

        self.set_cursor_state(True)
        self.set_stats_display(True)
        self.done = True
