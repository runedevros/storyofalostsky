from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Prologue'
        location = 'Netherworld Gardens'
        id_string = 'Prologue'
        prereqs = []
        show_rewards = True
        desc = 'The prologue to the story.'

        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'prologue.txt'
        mission_type = 'conversation'
        objective = None
        deploy_data = {}
        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = [ {'template_name': 'Yuyuko',
                                'unit_name': 'Yuyuko',
                                    'level': 10
                                },

                            {'template_name': 'Yukari',
                            'unit_name': 'Yukari',
                                'level': 16
                            }
                          ]

        initial_spells = {}
        initial_traits = {}
        initial_ai_states = {}
        initial_locations = {'Ran':(-1, 7),
                             'Chen':(-1, 6),
                             'Youmu':(5, 5),
                             'Yukari':(6, 7),
                             'Yuyuko':(5, 15)
                             }
        reserve_units = []
        all_landmarks = [{'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(2, 12)},
                          {'name':'CB2',
                          'id_string':'cherryblossom_tree',
                          'location':(6, 10)},
                          {'name':'CB3',
                          'id_string':'cherryblossom_tree',
                          'location':(3, 8)},
                          {'name':'CB4',
                          'id_string':'cherryblossom_tree',
                          'location':(8, 8)},
                          {'name':'CB5',
                          'id_string':'cherryblossom_tree',
                          'location':(3, 4)},
                          {'name':'CB6',
                          'id_string':'cherryblossom_tree',
                          'location':(4, 7)},
                          {'name':'CB7',
                          'id_string':'cherryblossom_tree',
                          'location':(8, 7)},
                          {'name':'CB8',
                          'id_string':'cherryblossom_tree',
                          'location':(12, 1)},
                          {'name':'CB9',
                          'id_string':'cherryblossom_tree',
                          'location':(14, 4)},
                          {'name':'CB10',
                          'id_string':'cherryblossom_tree',
                          'location':(10, 7)},

                          {'name':'CB11',
                          'id_string':'cherryblossom_tree',
                          'location':(16, 0)},
                          {'name':'CB12',
                          'id_string':'cherryblossom_tree',
                          'location':(17, 3)},
                          {'name':'CB13',
                          'id_string':'cherryblossom_tree',
                          'location':(18, 1)},
                          {'name':'CB14',
                          'id_string':'cherryblossom_tree',
                          'location':(19, 4)},
                          {'name':'CB15',
                          'id_string':'cherryblossom_tree',
                          'location':(22, 3)},

                         ]

        required_starters = ['Chen', 'Ran', 'Youmu']
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
        self.set_bg_overlay('Night')
        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.play_music('event01')

        # Introduction sequence
        self.say("Our world is known as Gensokyo. Long ago, we were separated from the world you know by a great magic barrier, and our world has remained isolated and untarnished since.",
                 None, None)
        self.say("It is home to both humans and youkai: mystical beings among which you would find playful fairies, energetic spirits, whimsical ghosts, among many others. What the other world refers to as fantasy and myth is, to us, reality.",
                 None, None)
        self.say("Gensokyo itself contains two distinct realms for the living and the dead respectively. The spirits of the Netherworld are managed by the master of Hakugyokurou, the ghost princess Yuyuko Saigyouji.",
                 None, None)
        self.say("The phantoms of Hakugyokurou revel in its majestic garden, which is carefully maintained by the dutiful Youmu Konpaku, Saigyouji's half-ghost retainer.",
                 None, None)
        self.say("Talented in the arts of swordplay, Youmu Konpaku serves also as the vigilant protector of the realm. It is from this realm of the dead that our story begins. She speaks with Yukari Yakumo, the youkai of boundaries...",
                 None, None)

        # Conversation between Yukari, Yuyuko, and Youmu
        self.say("Oh, Youmu! Has Yuyuko returned yet?",
                 'Yukari', 'Yukari')
        self.say('Returned? Did Madam leave?',
                 'Youmu', 'Youmu')
        self.move_unit('Yuyuko', (5, 7))
        self.say('Tsk, tsk. How irresponsible of you to not notice, Youmu.',
                 'Yuyuko', 'Yuyuko')
        self.say("I'm terribly sorry, Madam. I promise to keep more constant watch over you.",
                 'Youmu', 'Youmu')
        self.say('Oh, my! That might be a little troublesome...',
                 'Yuyuko', 'Yuyuko')
        self.say("Well! To think that our sweet, little Youmu would grow up a voyeur!",
                 'Yukari', 'Yukari')
        self.emote('Youmu', 'exclamation')
        self.startle('Youmu')
        self.say("I--",
                 'Youmu', 'Youmu')
        self.say("Anyway, we can talk about that another time. Now, Yuyuko, I've been wanting to ask. Did you find it?",
                 'Yukari', 'Yukari')
        self.say("Oh, yes! It was recovered just recently. I'm so glad! I don't know what I'd do if it was lost again.",
                 'Yuyuko', 'Yuyuko')
        self.say("Madam Yuyuko, what was it that you lost?",
                 'Youmu', 'Youmu')
        self.say("My favorite kimono, of course! See? Don't you think it looks lovely in this light?",
                 'Yuyuko', 'Yuyuko')
        self.say("Pardon me, but I think it looks strikingly similar to all your other kimono",
                 "Youmu", "Youmu")
        self.say("No, no! Look closer. See all the pretty light shades of color and how beautifully they blend together? This one's much more special.",
                 "Yukari", "Yukari")
        self.say("I do not. All that strikes me is the paper lantern Madam is holding--oh. Wait, I recognize that lantern. Isn't that the Lantern of Souls?",
                 "Youmu", "Youmu")
        self.say("And see how it brings out the colors of my kimono?",
                 "Yuyuko", "Yuyuko")
        self.say("...As you say, Madam.",
                 "Youmu", "Youmu")
        self.say("Hahaha! Well, we'd best get moving. The night doesn't last forever, you know.",
                 "Yukari", "Yukari")
        self.say("You're leaving so soon? Then please allow me to--",
                 "Youmu", "Youmu")
        self.say("Nope! Just stay put and be good a good girl, okay, little Youmu?",
                 "Yukari", "Yukari")
        self.say("Please, don't fret so much. We'll be back before long, all right? Toodles!",
                 "Yuyuko", "Yuyuko")
        self.say("Now! One portal for two, please!",
                 "Yukari", "Yukari")

        # Fade to white, remove Yukari and Yuyuko from the map, fade back
        self.fade_to_color('white', 0.1)
        self.kill_unit('Yuyuko')
        self.kill_unit('Yukari')
        self.fade_from_color('white', 0.1)

        self.emote('Youmu', 'dotdotdot')
        self.say("...How abrupt.",
                 "Youmu", "Youmu")

        # Next scene, the moring after with Youmu, Ran, and Chen
        self.fade_to_color('black', 1.0)
        self.set_bg_overlay(None)
        self.set_unit_pos('Youmu', (5, 10))
        self.fade_from_color('black', 1.0)

        self.say("The next morning...", None, None)

        self.move_unit('Youmu', (7, 10))
        self.say("They've been gone far too long. I ought to have accompanied them...",
                 "Youmu", "Youmu")
        self.move_unit('Youmu', (5, 10))
        self.say("But that moment has already passed. I had best go out and search for them.",
                 "Youmu", "Youmu")


        self.move_unit('Ran', (7, 7))
        self.move_unit('Chen', (6, 6))
        self.say("Excuse us, Youmu.",
                 "Ran", "Ran")
        self.move_unit('Youmu', (7, 8))
        self.set_cursor_state(True)
        self.center_on('Youmu')
        self.say("Good morning, Ran and Chen. Pardon me for asking, but would you happen to know Madam Yuyuko's whereabouts?",
                 "Youmu", "Youmu")
        self.set_cursor_state(False)
        self.say("Oh, no. Is your mistress not with you either?",
                 "Ran", "Ran")
        self.say("Madam Yukari told us that she was heading to Hakugyokurou the other day, but...we haven't seen her since.",
                 "Ran", "Ran")
        self.say("How odd. Your mistress was here just last night before she left with Madam Yuyuko. I thought, perhaps, they would be with you.",
                 "Youmu", "Youmu")
        self.say("Say, if Madam Yukari needed someone to go with her, why did she go all the way here to ask Madam Yuyuko to go without bringing us along, too?",
                 "Chen", "Chen")
        self.say("I'm unaware of their intentions, but I heard they were leaving for the Forest of Magic to find a ghost.",
                 "Youmu", "Youmu")
        self.say("Oh, yes! And they took the Lantern of Souls along with them. Did you hear something similar from Madam Yukari?",
                 "Youmu", "Youmu")
        self.say("I dunno, but there's a looot of crazy stuff happening in the forest right now. The youkai there have gone nuts!",
                 "Chen", "Chen")
        self.say("Really? Do you know what's happened?",
                 "Youmu", "Youmu")
        self.say("I'm afraid we don't have a clue! But I'm certain it's connected to our mistresses somehow.",
                 "Ran", "Ran")
        self.say("As do I. I think it's best that we all go investigate. I'm concerned about Madam.",
                 "Youmu", "Youmu")
        self.say("Honestly, I bet this is all just a part of one of Madam Yukari's schemes... Regardless, we should get going as soon as we're ready!",
                 "Ran", "Ran")
        self.say("And so the three set off in search of their missing mistresses, not knowing this would be the first step in a long, long journey.",
                 None, None)

        self.set_cursor_state(True)
        self.set_stats_display(True)
