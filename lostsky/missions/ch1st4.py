from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Onward to the Village'
        location = 'Western Village Path'
        id_string = 'CH1ST4'
        prereqs = ['CH1ST3']
        show_rewards = False
        desc = "Just before sunset, I caught a glimpse of Reimu and Rinnosuke fleeing from the Forest of Magic. Rinnosuke's whole shop was completely trampled by those walking trees, so he salvaged what he could in a small wooden box. They looked to be heading for the human village."
        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch1st4.txt'
        mission_type = 'conversation'
        objective = None

        deploy_data = {'enable':False,
                       'max_units':None,
                       'preset_units':None,
                       'boxes':[]
                       }

        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Rinnosuke',
                                'unit_name': 'Rinnosuke',
                                    'level': 11},
                          ]

        initial_spells = {}

        initial_traits = {}

        initial_ai_states = {}

        initial_locations = {'Ran':(4, 18),
                             'Chen':(4, 20),
                             'Youmu':(5, 19),
                             'Marisa':(4, 19),

                             'Rinnosuke':(9, 19),
                             }

        reserve_units = []#[list of unit names to deploy later in mission]

        all_landmarks = []

        required_starters = ['Youmu', 'Chen', 'Ran', 'Marisa']
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

        # Use the sunset color overlay
        self.set_bg_overlay('Sunset')
        self.play_music('event01')
        self.add_to_party('Reimu')

        self.set_unit_pos('Reimu', (8, 19))
        self.assign_spell('Reimu', 'Holy Amulet')
        self.assign_spell('Reimu', 'Fantasy Seal')
        self.assign_spell('Reimu', 'Weakening Amulet')
        self.assign_spell('Reimu', 'Barrier Buster')
        self.center_on('Marisa')

        self.say("Well, well, well! If it isn't Reimu.",
                'Marisa',
                'Marisa')
        self.startle('Marisa')
        self.say("Aren't you late to the party?",
                'Marisa',
                'Marisa')
        self.say("I was busy making sure Rinnosuke got out of the forest safe and sound. I was over at his place when all this commotion started. So no, I'm not late.",
                'Reimu',
                'Reimu')
        self.say("Geez, so they kicked you out, too, huh?",
                'Marisa',
                'Marisa')
        self.center_on('Rinnosuke')
        self.say("Unfortunately. My antique shop's been reduced to a pile of rubble.",
                'Rinnosuke',
                'Rinnosuke')
        self.say("That's the short version of it at least. So? Why are those three with you, Marisa?",
                'Reimu',
                'Reimu')

        # Fade to black as they tell their story
        self.fade_to_color('black', 0.5)
        self.pause(0.5)
        self.fade_from_color('black', 0.5)

        self.center_on('Reimu')
        self.say("Hm. Knowing Yukari, I wouldn't be surprised if she knew exactly what was going on. Maybe she had a hand in this.",
                'Reimu',
                'Reimu')
        self.say("I doubt that. She isn't the type to stir up trouble and cause such widespread mayhem in the process.",
                'Ran',
                'Ran')
        self.say("Actually, I'm sure that's exactly the kind of thing she would do to keep herself entertained.",
                'Reimu',
                'Reimu')
        self.say("Oh, yeah. Hey, Kourin, we found this earlier today. What does it do?",
                'Marisa',
                'Marisa')

        self.show_image('fire_crystal', 'fire_crystal.png', (350, 210))
        self.say("Hm? Oh, this. It's called a Lava Rock, and it's used in the synthesis of spells. I'm sure with your knowledge of magic, you can figure out how to use it to craft your own spells.",
                'Rinnosuke',
                'Rinnosuke')
        self.hide_image('fire_crystal')
        self.say("Whoa, cool! Thanks, Mr. Morichika! ...And, also, Mr. Morichika? I'm really sorry your antique shop's gone. What do you plan to do now?",
                'Chen',
                'Chen')
        self.say("Hmm, well, hopefully, I can set up shop in the village. I'd be willing to trade any useful items for antiques that you might happen upon if you ever choose to drop by.",
                'Rinnosuke',
                'Rinnosuke')
        self.say("And I'll be willing to trade extra fine items if you find some of the artifacts from my old shop that are scattered, well, everywhere now. ...After recent events.",
                'Rinnosuke',
                'Rinnosuke')
        self.say("Well, best of luck with all that. Whew! Looks like we have quite the ragtag group here.",
                'Reimu',
                'Reimu')
        self.say("Hey, Reimu! You wanna join? You know you wanna. Just picture it: all those donations of gratitude you'll get if you help solve the Great Kodama Lord Mystery...",
                'Marisa',
                'Marisa')
        self.say("Ha! Well. When you put it that way... Done deal. I'm in.",
                'Reimu',
                'Reimu')
        self.say("Reimu joins the party!",
                None,
                None)
        self.say("Spell Synthesis is now available!",
                None,
                None)
        self.say("Be sure to check out the Spell Synthesis Tutorials if you don't know how it works.",
                None,
                None)
        self.say("We should consider using Spell Synthesis to replenish our spell supplies.",
                'Youmu',
                'Youmu')
        self.say("Fireball, Dagger Throw, Leaf Crystal, and Holy Amulet can now be synthesized!",
                None,
                None)
        self.add_recipe('Fireball')
        self.add_recipe('Dagger Throw')
        self.add_recipe('Leaf Crystal')
        self.add_recipe('Holy Amulet')
        self.say("Item Trading is now available!",
                None,
                None)
        self.say("Let's head for the human village, then.",
                'Reimu',
                'Reimu')


        # Hide all units except for Ran and Youmu
        self.fade_to_color('black', 0.5)
        self.set_unit_pos('Marisa', (-1, -1))
        self.set_unit_pos('Reimu', (-1, -1))
        self.set_unit_pos('Chen', (-1, -1))
        self.set_unit_pos('Rinnosuke', (-1, -1))
        self.fade_from_color('black', 0.5)

        # Youmu and Ran's private conversation
        self.move_unit('Youmu', (8, 19))
        self.move_unit('Ran', (7, 18))
        self.move_unit('Youmu', (9, 19))
        self.pause(1.0)
        self.move_unit('Youmu', (7, 19))
        self.center_on('Youmu')

        self.say("Pardon me, Ran...",
                'Youmu',
                'Youmu')
        self.say("What is it, Youmu?",
                'Ran',
                'Ran')
        self.say("Ran...I... Do you truly believe we can do this? I fear we won't be able to make it through this.",
                'Youmu',
                'Youmu')
        self.say("Oh, Youmu...",
                'Ran',
                'Ran')
        self.move_unit('Ran', (7, 18))
        self.say("So much has happened, and so quickly. A single day in fact! Madam Yuyuko's gone.",
                'Youmu',
                'Youmu')
        self.say("For Reimu and Marisa, this is yet another standard, routine day. But me? I'm a mere gardener! I'm unaccustomed to this! If it gets any worse, I...just don't see myself pulling through this.",
                'Youmu',
                'Youmu')
        self.say("Hmm. Well, this is the first chance we've had today to catch our breath, so let's just take it easy for now. No worries or anything of the sort!",
                'Ran',
                'Ran')
        self.say("I'm sorry, I can't. The consequences of our potential failure are too great. And that...frightens me. I can't just shake off that fear at a moment's notice.",
                'Youmu',
                'Youmu')
        self.say("Youmu. I'm not going to pretend the journey ahead is going to be easy. It'll likely be so incredibly difficult that there will be times you'll want to turn back, throw your hands into the air and give up.",
                'Ran',
                'Ran')
        self.say("But we won't. We have to have the courage and strength to go on. We're doing this not only for Madam Yuyuko and Madam Yukari, but also for all of Gensokyo.",
                'Ran',
                'Ran')
        self.say("But...what do you do when you want to give up? I don't know that I have the courage and strength you speak of.",
                'Youmu',
                'Youmu')
        self.say("Well... We've already started this journey, and we've already gotten this far.",
                'Ran',
                'Ran')
        self.say("We've found clues that'll help us figure this whole situation out. We've made some significant progress for the first day, wouldn't you say?",
                'Ran',
                'Ran')
        self.say("Strength is something you gain along the way, and all these little goals we've achieved just keep adding up.",
                'Ran',
                'Ran')
        self.say("And besides, what's the purpose of an adventure if it's nothing more than a serene outdoor picnic?",
                'Ran',
                'Ran')
        self.say("You're stronger than you give yourself credit for, Youmu, and you'll only grow stronger from this.",
                'Ran',
                'Ran')
        self.say("We will make it, Youmu. We'll be fine. You said it yourself, right? \"Come what may. We shall not surrender,\" or something like that...right?",
                'Ran',
                'Ran')
        self.say("...Thank you, Ran.",
                'Youmu',
                'Youmu')
        self.set_cursor_state(True)
        self.set_stats_display(True)
        self.done = True