from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Reunion'
        location = "Wind God's Lake"
        id_string = 'CH3ST6'
        prereqs = ['CH3ST5']
        show_rewards = False
        desc = "The inhabitants of Youkai Mountain achieved a great victory today as the remainder of the Kodama Lords' forces were driven out of the mountain by the valiant efforts of the Tengu and Kappa. Now that Yuyuko and Youmu have reunited at last, Youmu and her companions have gathered together to figure out their next move."

        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch3st2.txt'
        mission_type = 'conversation'
        objective = None

        deploy_data = {'enable':False,
                       'max_units':None,
                       'preset_units':None,
                       'boxes':[]
                       }

        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Tsubaki',
                                'unit_name': 'Tsubaki',
                                    'level': 25},
                        {'template_name': 'Momiji',
                                'unit_name': 'Momiji',
                                    'level': 8},
                         {'template_name': 'Nitori',
                                'unit_name': 'Nitori',
                                    'level': 7},
                        {'template_name': 'Yuyuko',
                                'unit_name': 'Yuyuko',
                                    'level': 10
                                },

                            {'template_name': 'Yukari',
                            'unit_name': 'Yukari',
                                'level': 16
                            },

                            {'template_name': 'Wolf Tengu',
                            'unit_name': 'Wolf Tengu A',
                                'level': 10
                            },
                            {'template_name': 'Wolf Tengu',
                            'unit_name': 'Wolf Tengu B',
                                'level': 10
                            }

        ]

        reserve_units = []

        initial_spells = {}

        initial_traits = {}

        initial_ai_states = {}

        initial_locations = {

                             'Mokou':(16, 19),
                             'Yuyuko':(17, 19),
                             'Youmu':(18, 19),
                             'Keine':(19, 19),
                             'Marisa':(20, 19),


                             'Ran':(16, 20),
                             'Chen':(17, 20),
                             'Yukari':(18, 20),
                             'Reimu':(20, 20),


                             'Momiji':(14, 17),
                             'Wolf Tengu A':(12, 16),
                             'Wolf Tengu B':(13, 17),


                             'Aya':(19, 17),
                             'Tsubaki':(18, 17),
                             'Nitori':(17, 17),


                             }


        all_landmarks = [
                        {'name':'Main House',
                         'id_string':'house_2',
                         'location':(18, 16)},

                        {'name':'Cherry Tree 1',
                         'id_string':'cherryblossom_tree',
                         'location':(17, 16)},
                        {'name':'Cherry Tree 2',
                         'id_string':'cherryblossom_tree',
                         'location':(19, 16)},

                        {'name':'West House',
                         'id_string':'house_1',
                         'location':(20, 17)},
                        {'name':'East House',
                         'id_string':'house_1',
                         'location':(16, 17)},

        ]

        required_starters = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Reimu', 'Keine', 'Mokou', 'Aya']
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
        Prologue event
        """
        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.set_bg_overlay('Sunset')
        self.play_music('event01')

        # Momiji conversing with other Wolf Tengu guards
        self.center_on('Momiji')
        self.say("Momiji! We're dying to know. What was it like fighting that Kodama Lord?",
            'Wolf Tengu A',
            'Wolf Tengu')
        self.say("Well, Ayaka put up a difficult fight. Nitori's and Lady Tsubaki's presence was critical to our ultimate victory over her and her forces.",
            'Momiji',
            'Momiji')
        self.say("Pst, hey. Looks like the meeting's starting. You should go listen in. Don't worry, I'll take over the watch.",
            'Wolf Tengu B',
            'Wolf Tengu')

        # Planning what to do next
        self.center_on('Tsubaki')
        self.emote('Tsubaki', 'heart')
        self.say("Good news. The Kappa are building a structure to send water from our mountain to your village. It's a bit unusual for us to reach out like this, but it was necessary.",
            'Tsubaki',
            'Tsubaki')
        self.say("We are eternally grateful. If I might ask, have the Tengu's upper ranks complained about this at all?",
            'Keine',
            'Keine')
        self.say("Yuyuko and I persuaded them. I had to pull quite a few strings, but they've more or less shut up about it.",
            'Yukari',
            'Yukari')
        self.say("I suppose we owe you one then, Yukari.",
            'Keine',
            'Keine')
        self.say("Oh? Do you now? I'll be sure to remember that!",
            'Yukari',
            'Yukari')

        # Reimu knows that Yukari is a trickster. Pulls Marisa aside.
        self.move_unit('Reimu', (22, 20))
        self.move_unit('Marisa', (22, 19))
        self.center_on('Reimu')
        self.say("What kind of dirty trick did she pull this time...",
            'Reimu',
            'Reimu')
        self.say("Maybe she made all their prized silverware disappear or something.",
            'Marisa',
            'Marisa')
        self.say("Beautiful antique silverware and china, lost forever, zipped away within a one-way gap to oblivion. Classic Yukari.",
            'Reimu',
            'Reimu')
        # Reimu and Marisa return to the group
        self.move_unit('Reimu', (20, 20))
        self.move_unit('Marisa', (20, 19))

        self.center_on('Youmu')
        self.say("It's a time for unity. Some of the Tengu see that, though most are too stubborn to accept it. There'll be problems still, sure, but we'll address them as they come.",
            'Tsubaki',
            'Tsubaki')
        self.say("And while everyone starts getting all buddy-buddy with each other, Yuyuko and I will work on repairing the lantern.",
            'Yukari',
            'Yukari')
        self.say("We'll need to gather some pretty rare parts, so we'll leave getting the lantern oil to you.",
            'Yukari',
            'Yukari')
        self.say("About that. I...already tried synthesizing that oil stuff for the lantern. And...",
            'Marisa',
            'Marisa')
        self.say("Oh? How did it go?",
            'Youmu',
            'Youmu')
        self.emote('Nitori', 'scribble')
        self.say("It went all kablooey in my workshop! It's all burnt and still reeks of soot in there! Oh... My poor workshop...",
            'Nitori',
            'Nitori')
        self.say("...And I blew up my entire potion creation kit in the process. So, um, haha... I'll have to get a new one from Kourin.",
            'Marisa',
            'Marisa')
        self.say("But ok. Seriously. It'll take me months. At least. It's a super complicated process. I've never worked with anything like this stuff before, so I have to feel my way through trial and error.",
            'Marisa',
            'Marisa')
        self.emote('Yukari', 'lightbulb')
        self.say("Hm? One of my crows tells me that Fuyuhana has moved into the Bamboo Forest with Ayaka in tow, who's personally leading their trees.",
            'Yukari',
            'Yukari')
        self.say("This might actually be a good opportunity for us.",
            'Yukari',
            'Yukari')
        self.say("Oh, hey! You know, if there's anyone in Gensokyo who can make this lantern oil, I bet that Eirin of Eientei can.",
            'Marisa',
            'Marisa')
        self.say("Do you think she'll be willing to help us?",
            'Youmu',
            'Youmu')
        self.say("No dice. Don't even think that recluse Kaguya will help either.",
            'Mokou',
            'Mokou')
        self.say("But that's only under normal conditions, Mokou.",
            'Keine',
            'Keine')
        self.say("Madam Yukari, do we have information on how the battle is progressing?",
            'Ran',
            'Ran')
        self.say("Sure do! It's going poorly for Eientei. Ayaka is a calculating general and commands only the most experienced of the trees. Those cute fluffy bunnies don't stand a chance.",
            'Yukari',
            'Yukari')
        self.say("Unlike the Tengu, they don't have a well-trained army. They'll have to fend for themselves.",
            'Tsubaki',
            'Tsubaki')
        self.say("In that case, maybe they'll agree to help us in exchange for helping them drive the invaders out.",
            'Youmu',
            'Youmu')
        self.startle('Marisa')
        self.say("Music to my ears, Youmu. Sounds like we have a plan.",
            'Marisa',
            'Marisa')
        self.say("Then let's head out to the Bamboo Forest as soon as we're ready.",
            'Youmu',
            'Youmu')
        self.say("Oh, no! Too bad. I still have some business with the Tengu. You all go ahead, ok? We'll reunite at the human village. Ta-ta now!",
            'Yukari',
            'Yukari')

        # Remove everyone but Yuyuko and Youmu
        self.fade_to_color('black', 1.0)
        self.set_unit_pos('Reimu', (-1, -1))
        self.set_unit_pos('Marisa', (-1, -1))
        self.set_unit_pos('Ran', (-1, -1))
        self.set_unit_pos('Chen', (-1, -1))
        self.set_unit_pos('Mokou', (-1, -1))
        self.set_unit_pos('Keine', (-1, -1))
        self.set_unit_pos('Aya', (-1, -1))
        self.set_unit_pos('Tsubaki', (-1, -1))
        self.set_unit_pos('Nitori', (-1, -1))
        self.set_unit_pos('Momiji', (-1, -1))
        self.set_unit_pos('Yukari', (-1, -1))
        self.set_unit_pos('Wolf Tengu A', (-1, -1))
        self.set_unit_pos('Wolf Tengu B', (-1, -1))
        self.set_unit_pos('Youmu', (12, 15))
        self.set_unit_pos('Yuyuko', (13, 15))
        self.fade_from_color('black', 1.0)

        # Youmu and Yuyuko have a conversation together
        self.center_on('Youmu')
        self.say("Oh, wait. Youmu?",
            'Yuyuko',
            'Yuyuko')
        self.say("What is it, madam?",
            'Youmu',
            'Youmu')
        self.say("Youmu, I'm really proud of you, ok? You've led this group so far.",
            'Yuyuko',
            'Yuyuko')
        self.say("To be honest, I was scared when I had found out that you were gone. I thought that I had failed in my duty to protect you.",
            'Youmu',
            'Youmu')
        self.say("You've done well without me, Youmu. I couldn't be happier.",
            'Yuyuko',
            'Yuyuko')
        self.say("One more thing, Youmu. Yukari and I will be back in the village periodically, so don't worry about us too much. I think we've proven we can take care of ourselves. Now, off you go!",
            'Yuyuko',
            'Yuyuko')
        self.say("Madam Yuyuko, thank you. I won't let you down!",
            'Youmu',
            'Youmu')

        # Remove Youmu from map.
        self.fade_to_color('black', 1.0)
        self.set_unit_pos('Youmu', (-1, -1))
        self.fade_from_color('black', 1.0)

        # Yuyuko monologue
        self.say("Youki Konpaku, are you watching this crisis somewhere, all alone?",
            'Yuyuko',
            'Yuyuko')
        self.say("When you first brought Youmu to me, she was so frail and uncertain of herself, but now...",
            'Yuyuko',
            'Yuyuko')
        self.say("I am so fortunate to have watched her grow up all these years and so honored to have been able to serve as her mistress. My heart is overflowing with joy because of her... Thank you.",
            'Yuyuko',
            'Yuyuko')


        self.set_cursor_state(True)
        self.set_stats_display(True)
        self.done = True