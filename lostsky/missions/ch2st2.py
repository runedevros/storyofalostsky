from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'The Two Historians'
        location = 'Human Village'
        id_string = 'CH2ST2'
        prereqs = ['CH2ST1']
        show_rewards = False
        desc = 'The fight raged on outside, meanwhile, I met with Akyu on the porch of her house, watching the events intently. "Similar events occured here a long time ago," she told me. "The trees of the forest led by the Kodama Lords were also in conflict with the humans and youkai then. The Kodama have been dormant for many years now, deep in slumber, patiently awaiting the day they are needed again." She pauses. "And here we are now."'

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
        enemy_unit_data = [ {'template_name': 'Akyu',
                                 'unit_name': 'Akyu',
                                     'level': 5 },
                            {'template_name': 'Aya',
                                 'unit_name': 'Aya',
                                     'level': 7 },
                          ]

        initial_spells = {}
        initial_traits = {}
        initial_ai_states = {}
        initial_locations = {'Akyu':(15, 9),
                             'Keine':(15, 8),

                             'Youmu':(17, 9),
                             'Ran':(17, 10),
                             'Chen':(17, 8),

                             'Reimu':(18, 9),
                             'Marisa':(18, 11),
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

        required_starters = ['Chen', 'Ran', 'Youmu', 'Marisa', 'Reimu', 'Keine']
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
        self.set_bg_overlay('Night')
        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.play_music('event01')
        self.center_on('Akyu')

        self.say("Have some red tea, everyone. It's such a pleasant evening, so I thought we could meet out here in the garden.",
                'Akyu',
                'Akyu')

        # Akyu moves around serving tea to people
        self.move_unit('Akyu', (16, 10))
        self.pause(0.5)
        self.move_unit('Akyu', (16, 8))
        self.pause(0.5)
        self.move_unit('Akyu', (16, 9))
        self.move_unit('Akyu', (15, 9))

        self.say("Ah, yes. It isn't truly a visit until we've had a taste of your wonderful tea.",
                'Keine',
                'Keine')
        self.say("Youmu, you said you wanted to know more about the Kodama Lords and whomever else is behind the problems in the forest today, am I correct?",
                'Akyu',
                'Akyu')
        self.say("That is correct. We believe it will help us find Madam Yuyuko and Madam Yukari.",
                'Youmu',
                'Youmu')
        self.say("We're sure their disappearance is connected to this somehow.",
                'Ran',
                'Ran')
        self.say("The history of the forest is long and complex. A long time ago, a great youkai lord ruled over the forest's Kodama.",
                'Akyu',
                'Akyu')
        self.say("And so it may be connected to her. There is a plethora of information pertaining her, so I will need some time to organize it for you.",
                'Akyu',
                'Akyu')
        self.say("Thank you, Miss Hieda.",
                'Chen',
                'Chen')
        self.say("We greatly appreciate your helping us.",
                'Youmu',
                'Youmu')
        self.say("You are all free to stay here for the night. I'm sure I'll have everything ready by tomorrow morning.",
                'Akyu',
                'Akyu')
        self.say("Thank you for your help, Akyu. I'd best be heading home since this is much more Akyu's expertise than mine. I bid you all a pleasant night.",
                'Keine',
                'Keine')



        # Fade to black, remove everyone from the map
        self.fade_to_color('black', 1.0)
        self.set_bg_overlay(None)
        for unit_name in ['Akyu', 'Reimu', 'Youmu', 'Ran', 'Chen', 'Marisa', 'Keine']:
            self.set_unit_pos(unit_name, (29, 29))
        self.set_unit_pos('Aya', (10, 29))
        self.fade_from_color('black', 1.0)

        # Aya making her rounds
        self.say("Pick up your special early bird edition of the Bunbunmaru Newspaper right here!",
                'Aya',
                'Aya')

        self.move_unit('Aya', (13, 13))
        self.pause(0.5)
        self.startle('Aya')
        self.say("Read all about the latest crisis!",
                'Aya',
                'Aya')

        self.move_unit('Aya', (13, 10))
        self.pause(0.5)
        self.startle('Aya')
        self.say("Vengeful tree spirits take over the Forest of Magic!",
                'Aya',
                'Aya')

        self.move_unit('Aya', (9, 8))
        self.pause(0.5)
        self.startle('Aya')

        # Marisa and Reimu leave the house
        self.set_unit_pos('Marisa', (14, 9))
        self.move_unit('Marisa', (14, 11))
        self.set_unit_pos('Reimu', (14, 9))
        self.move_unit('Reimu', (14, 10))

        self.say("Geez, Aya! Did you have to come so early in the morning?",
                'Marisa',
                'Marisa')
        self.say("Typical. She always delivers her newspaper at the break of dawn. You could set your clock to her.",
                'Reimu',
                'Reimu')
        self.move_unit('Aya', (12, 11))
        self.say("Whaat? I have to beat all the other Tengu reporters and win over all their readers!",
                'Aya',
                'Aya')

        # Youmu, Ran, and Chen leave the house
        self.set_unit_pos('Youmu', (14, 9))
        self.move_unit('Youmu', (11, 9))
        self.set_unit_pos('Ran', (14, 9))
        self.move_unit('Ran', (12, 9))
        self.set_unit_pos('Chen', (14, 9))
        self.move_unit('Chen', (13, 9))

        self.say("What is the problem, everyone? Oh. Hello, Miss Shameimaru.",
                'Youmu',
                'Youmu')
        self.move_unit('Aya', (11, 10))
        self.say("Heya! I'm here to interview you about your adventures in this latest crisis! Could I get a few comments from you on what happened yesterday?",
                'Aya',
                'Aya')
        self.say("Um... I... What should I say?",
                'Youmu',
                'Youmu')
        self.say("Come oon! Work with me here. I need to get on the latest scoop. So tell me, how do you feel about the latest crisis?",
                'Aya',
                'Aya')
        self.say("You know you don't have to answer her if you don't have anything to say.",
                'Ran',
                'Ran')
        self.say("Well, I...I'm worried about what happened to Madam Yuyuko after she disappeared. I hope she's all right.",
                'Youmu',
                'Youmu')
        self.say("Ah! I see... Hmm...",
                'Aya',
                'Aya')
        self.say("Tee-hee! This is the perfect headline!",
                'Aya',
                'Aya')
        self.say('"Ghost Princess vanishes. The plot thickens! Is she the perpetrator of our latest crisis?"',
                'Aya',
                'Aya')
        self.say("Miss Shameimaru! I said nor implied any such thing!",
                'Youmu',
                'Youmu')
        self.say("Ouch, she really spun your words on that one.",
                'Reimu',
                'Reimu')
        self.say("Ehehehe, well... Oh! Look at the time. I've gotta go now to deliver the rest of my papers. Oh, and be sure to check out the latest section of my paper! It's sure to get your heart pumping!",
                'Aya',
                'Aya')
        self.say("One more thing. I started a section where people can post little jobs they need getting done. Who knows what'll be on there? Maybe you'll find something there that'll help you find Yuyuko.",
                'Aya',
                'Aya')
        self.move_unit('Aya', (12, 29))
        self.say("Be sure to regularly check the missions screen for new missions. They may lead you to new discoveries.",
                'Tutorial',
                None)

        # Keine and Akyu leave the house
        self.set_unit_pos('Keine', (12, 29))
        self.move_unit('Keine', (12, 11))
        self.startle('Keine')
        self.set_unit_pos('Akyu', (14, 9))
        self.move_unit('Akyu', (13, 10))

        self.say("You look kinda troubled there, Keine.",
                'Reimu',
                'Reimu')
        self.say("A villager spotted a Kodama Lord near the village cemetery, which is rather disconcerting to say the least.",
                'Keine',
                'Keine')
        self.say("Um, yeah, that's weird, right? Do Kodama lords usually go outside the forest?",
                'Chen',
                'Chen')
        self.say("No, not usually. They don't leave the forest unless it's something really important. Something's up.",
                'Ran',
                'Ran')
        self.say("That settles it then. You coming, Youmu?",
                'Marisa',
                'Marisa')
        self.say("I am. It is indeed unusual that one of the Kodama would leave the forest. I, too, fear something is amiss.",
                'Youmu',
                'Youmu')
        self.say("Oh, I'm so sorry. I'm still working on compiling the final pieces of information I've gathered. We can discuss it upon your return. I wish you the best of luck!",
                'Akyu',
                'Akyu')

        self.set_cursor_state(True)
        self.set_stats_display(True)
        self.done = True
