from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Emissary of the Tengu'
        location = "Wind God's Lake"
        id_string = 'CH3ST2'
        prereqs = ['CH3ST1']
        show_rewards = False
        desc = "Following the unexpected arrival of Youmu and company at the basin of Youkai Mountain, Emissary of Lord Tenma Tsubaki Akahane has agreed to meet with their group. There have been rumors that the higher ranking Tengu that they may be able to settle upon an agreement, but the majority of the Tengu leaders are still strongly opposed to involving themselves with the outside world. Tensions remain strong."

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
                        {'template_name': 'Aya',
                            'unit_name': 'Aya',
                            'level': 10},
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
                            }

        ]

        initial_spells = {}

        initial_traits = {}

        initial_ai_states = {}

        initial_locations = {'Ran':(4, 13),
                             'Chen':(5, 13),
                             'Youmu':(6, 14),
                             'Marisa':(4, 14),
                             'Reimu':(5, 14),
                             'Mokou':(4, 15),
                             'Keine':(5, 15),

                             'Nitori':(8, 12),
                             'Aya':(8, 13),
                             'Momiji':(8, 14),


                             'Tsubaki':(18, 17)
                             }

        reserve_units = ['Yukari', 'Yuyuko']#[list of unit names to deploy later in mission]

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

        required_starters = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Reimu', 'Keine', 'Mokou']
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

        # Aya motions for party to approach the tengu outpost
        self.center_on('Aya')
        self.say('No getting lost along the way, ok? Follow me!', 'Aya', 'Aya')


        # Set everyone in front of Tsubaki
        self.fade_to_color('black', 0.5)


        self.set_unit_pos('Aya', (17, 18))
        self.set_unit_pos('Momiji', (19, 18))
        self.set_unit_pos('Youmu', (18, 19))
        self.set_unit_pos('Keine', (19, 19))
        self.set_unit_pos('Mokou', (16, 19))
        self.set_unit_pos('Ran', (16, 20))
        self.set_unit_pos('Chen', (17, 20))

        self.set_unit_pos('Nitori', (20, 19))
        self.set_unit_pos('Marisa', (20, 20))
        self.set_unit_pos('Reimu', (19, 20))

        self.fade_from_color('black', 0.5)

        # Conference with the Tengu leader
        self.center_on('Aya')

        self.say("Yoohoo! Tsubaki! I've brought them just as you asked. Ah, I can just see my newspapers selling like crazy! This is gonna be the best morning special report!",
                 'Aya',
                 'Aya')

        self.move_unit('Aya', (17, 17))
        self.move_unit('Momiji', (19, 17))

        self.say("A shame we couldn't meet under less pressing circumstances.",
                 'Tsubaki',
                 'Tsubaki')
        self.say("Ah, yes. Would...it inappropriate for me to speak honestly?",
                 'Youmu',
                 'Youmu')
        self.say("Please allow me, Youmu. Trust me, I've had fair my share of experiences dealing with youkai.",
                 'Keine',
                 'Keine')
        self.say("Nuh-uh, no can do. Tsubaki specifically requested to speak with Youmu. Besides, she's your leader, right? Maybe you should let her act more like one.",
                 'Aya',
                 'Aya')
        self.say("I shall introduce myself. My name is Tsubaki Akahane, representative of Lord Tenma and emissary of the Order of the Red Feathers.",
                 'Tsubaki',
                 'Tsubaki')
        self.say("Mm. And I am Youmu Konpaku, retainer and servant of Madam Yuyuko Saigyouji.",
                 'Youmu',
                 'Youmu')


        self.say("Tell me why you've come to this mountain. Depending on your answer, I will react accordingly. You are still intruders, after all.",
                 'Tsubaki',
                 'Tsubaki')
        self.say("Very well.",
                 'Youmu',
                 'Youmu')

        self.fade_to_color('black', 1)
        self.fade_from_color('black', 1)

        self.say("...That is all. I hope that was satisfactory. We humbly request that you allow us passage to the tree guardian's sanctuary located at the mountain's peak.",
                 'Youmu',
                 'Youmu')
        self.say("Tell me you're joking. That's sacred ground! Only the Great Tengu priests and the Order of the Red Feathers are allowed there.",
                 'Momiji',
                 'Momiji')
        self.say("Not even I'm allowed to step foot in there. Absolutely preposterous!",
                 'Momiji',
                 'Momiji')

        self.emote('Tsubaki', 'dotdotdot')


        self.say("Momiji's right on point. We don't let outsiders into Misaki's Sanctuary.",
                 'Tsubaki',
                 'Tsubaki')
        self.say("Even if I wanted to help, convincing Lord Tenma and the rest of the Order would be impossible. Thus, my answer is this. The outside world hardly concerns us, so kindly leave us out of your problems.",
                 'Tsubaki',
                 'Tsubaki')
        self.say("You heard her. Now leave!",
                 'Momiji',
                 'Momiji')

        self.say("No... No! Please hear us out! I cannot simply leave like this. This crisis affects you as well! You require water just as we do. Without clouds, without rains... You will not survive this crisis. No one will.",
                 'Youmu',
                 'Youmu')
        self.emote('Marisa', 'lightbulb')
        self.say("Speaking of which, hey, Nitori. Roundabouts, how much water does Youkai Mountain have left?",
                 'Marisa',
                 'Marisa')
        self.say("For everyone living here? Let's see, there's about that many people and that much water used at that rate... It's--oh, wait, plus plants, um. Aha! I'm guesstimating about a month's worth!",
                 'Nitori',
                 'Nitori')

        self.say("Pah, it's not like we're unfamiliar with droughts. We shall persevere without your assistance.",
                 'Tsubaki',
                 'Tsubaki')
        self.say("Oh, yeah, sure. So all the clouds are gone because of totally natural, normal circumstances, huh? No rain ever again? Yeah, of course you'll be fine. ...Yeah, right. You'll be fine my foot!",
                 'Marisa',
                 'Marisa')
        self.say("Hold your tongue! You've no right to speak to Lady Akahane that way!",
                 'Momiji',
                 'Momiji')

        self.play_music('battle01')

        # Marisa pushes her way to the front
        self.move_unit('Marisa', (20, 21))
        self.move_unit('Marisa', (18, 21))
        self.move_unit('Marisa', (18, 20))
        self.startle('Marisa')
        self.emote('Youmu', 'exclamation')
        self.move_unit('Youmu', (17, 19))
        self.move_unit('Marisa', (18, 19))
        self.emote('Marisa', 'annoyed')

        self.say("You know what? I've heard enough out of you chickens! You think constantly turning away the outside world is magically gonna fix all of your problems?",
                 'Marisa',
                 'Marisa')
        self.say("Oh, please! No one can save the world by staying put!",
                 'Marisa',
                 'Marisa')
        self.say("Marisa, please. Stop. I don't think antagonizing her will help any of us.",
                 'Youmu',
                 'Youmu')
        self.say("I guess all those legends about the oh-so-amazing Tengu was just a load of garbage! Who knew they solved their problems by casually ignoring them! Ha! I'm absolutely disgusted!",
                 'Marisa',
                 'Marisa')
        self.say("You crows rule the skies! You wolves rule the earth! Aren't you supposed to protect this world? If you're anything at all like the legends, then come on! Help us resolve this crisis!",
                 'Marisa',
                 'Marisa')
        self.say("Marisa, wait!",
                 'Youmu',
                 'Youmu')
        self.say("I'm seriously fed up with this. Come on, Youmu. Reimu. We're forcing our way in there whether these Tengu like it or not. I've lost all of my respect for them.",
                 'Marisa',
                 'Marisa')
        self.say("Then at least pretend to show some respect, Marisa! You're not helping us at all!",
                 'Keine',
                 'Keine')
        self.play_music('event01')
        self.say("Don't.",
                 'Tsubaki',
                 'Tsubaki')
        self.say("What she said is perfectly acceptable.",
                 'Tsubaki',
                 'Tsubaki')


        self.say("What?",
                 'Keine',
                 'Keine')
        self.say("It's true. We're too scared to involve ourselves with the outside world to address this crisis. But, tell me, how do you fight against this fear?",
                 'Tsubaki',
                 'Tsubaki')
        self.say("Excuse me! I have a suggestion if it's ok.",
                 'Chen',
                 'Chen')
        self.say("Chen, no. Let your elders figure this out.",
                 'Ran',
                 'Ran')
        self.say("It's fine. Go ahead, Chen.",
                 'Tsubaki',
                 'Tsubaki')
        self.say("Thanks! So. Only the Great Tengu priests and your Order of Red Feathers can enter the holy sanctuary, right?",
                 'Chen',
                 'Chen')
        self.say("Yup! That's correct.",
                 'Aya',
                 'Aya')
        self.say("Then I have another question! How do we join the Order of the Red Feathers?",
                 'Chen',
                 'Chen')
        self.emote('Marisa', 'exclamation')
        self.say("Wait. Wait, what?! Am I hearing things or did you just ask what I think you did? Because...",
                 'Marisa',
                 'Marisa')
        self.say("...Aya, a word?",
                 'Tsubaki',
                 'Tsubaki')

        # Tsubaki and Aya move aside to have a private chat
        self.move_unit('Tsubaki', (15, 17))
        self.move_unit('Aya', (14, 17))
        self.emote('Aya', 'questionmark')
        self.emote('Tsubaki', 'heart')
        self.emote('Aya', 'exclamation')
        self.emote('Tsubaki', 'dotdotdot')
        self.emote('Tsubaki', 'lightbulb')
        self.emote('Aya', 'heart')

        self.say("You're kidding. Are they seriously considering Chen's suggestion?",
                 'Reimu',
                 'Reimu')

        # Tsubaki and Aya return to the party
        self.move_unit('Tsubaki', (18, 17))
        self.move_unit('Aya', (17, 17))


        self.say("I agree. We can't afford to devote our warriors to anything but protecting the mountain from Fuyuhana's and her lot.",
                 'Tsubaki',
                 'Tsubaki')
        self.say("Also? They're not going to leave this mountain without trying. We might as well let them have a crack at it. So how about it?",
                 'Aya',
                 'Aya')
        self.say("Ha, I often forget how wise children can be. Very good, Chen. Excuse me. I must meet with the Order of the Red Feathers and Lord Tenma.",
                 'Tsubaki',
                 'Tsubaki')
        self.say("Please, wait! Don't forget that the trial has never been given to outsiders before! Are you absolutely certain you want to do this?",
                 'Momiji',
                 'Momiji')
        self.say("Personally, I think that helps their case. I mean, it shows that we care enough to change at least a wee bit to help resolve this lost sky crisis! We won't take this without a fight kinda thing! You know?",
                 'Aya',
                 'Aya')
        self.say("Everyone, spend the night here. I'll return in the morning with word from Lord Tenma, so be patient. Momiji, you're with me. We need to report on the battle at the river by tonight so I need a hand.",
                 'Tsubaki',
                 'Tsubaki')

        self.say("Roger! You don't even need to tell me! I'll look after these kids and make sure they get all their arrangements to stay here in order. See you in the morning!",
                 'Aya',
                 'Aya')

        self.say("Thank you very much. We look forward to your return, Miss Tsubaki.",
                 'Youmu',
                 'Youmu')

        # Tsubaki and Momiji withdraw
        self.move_unit('Tsubaki', (10, 17))
        self.move_unit('Momiji', (11, 17))
        self.move_unit('Tsubaki', (10, 13))
        self.move_unit('Momiji', (11, 13))
        self.move_unit('Tsubaki', (-1, 13))
        self.move_unit('Momiji', (-1, 13))


        self.say("Well. Color me impressed, Chen. We owe this turn of fate all to you.",
                 'Mokou',
                 'Mokou')
        self.say("Hey. Don't celebrate yet. We haven't even been given the ok yet, much less learned anything about the trial. Ugh, honestly, I don't wanna think about it.",
                 'Reimu',
                 'Reimu')
        self.say("Oh, oh! I've got some tasty tidbits on that! So. One out of every hundred are able to pass. Ooh, I can see the fear in your eyes. As for me, I'm totally stoked!",
                 'Aya',
                 'Aya')

        # Switch to nighttime scene with Yukari and Yuyuko
        self.fade_to_color('black', 1)
        self.set_unit_pos('Youmu', (-1, -1))
        self.set_unit_pos('Reimu', (-1, -1))
        self.set_unit_pos('Marisa', (-1, -1))
        self.set_unit_pos('Ran', (-1, -1))
        self.set_unit_pos('Chen', (-1, -1))
        self.set_unit_pos('Mokou', (-1, -1))
        self.set_unit_pos('Keine', (-1, -1))
        self.set_unit_pos('Aya', (-1, -1))
        self.set_unit_pos('Tsubaki', (-1, -1))
        self.set_unit_pos('Momiji', (-1, -1))
        self.set_unit_pos('Nitori', (-1, -1))
        self.set_bg_overlay('Night')
        self.fade_from_color('black', 1)

        # Yuyuko and Yukari make an appearance
        self.play_music('event02')
        self.center_on_coords((7, 10))
        self.deploy_unit('Yuyuko', (7, 9))
        self.move_unit('Yuyuko', (7, 10))
        self.deploy_unit('Yukari', (7, 9))
        self.move_unit('Yukari', (8, 10))

        self.say("Whoop. Well! There goes the last light in their camp. It's pitch black now.",
                'Yukari',
                'Yukari')
        self.say("Hmm, I do wonder if Youmu has been getting enough rest. You know how she is, after all.",
                'Yuyuko',
                'Yuyuko')
        self.say("I'm sure she's fine. I mean, have you seen her little party there? Impressive line up, especially for little Youmu, wouldn't you say?",
                'Yukari',
                'Yukari')

        # Ran discovers the two of them
        self.set_unit_pos('Ran', (9, 8))
        self.emote('Ran', 'exclamation')
        self.move_unit('Ran', (9, 10))

        self.say("Oh, my! If it isn't Ran! I do believe we've been discovered.",
                'Yuyuko',
                'Yuyuko')
        self.say("I thought it was your spiritual energy that I sensed. I see I was right.",
                'Ran',
                'Ran')
        self.say("Well, well, well. I guess there's no hiding from my own shikigami.",
                'Yukari',
                'Yukari')
        self.say("Oh, Ran! I must say, your shikigami Chen is growing up so well! My heart practically melted listening to her say all that.",
                'Yuyuko',
                'Yuyuko')
        self.say("It was impressive of her to speak up to the emissary like that. I was afraid I'd have to baby you all so things would go your way, but thanks to Chen, I didn't have to lift a finger. Nice going.",
                'Yukari',
                'Yukari')
        self.say("I am grateful to Chen, as well, but that aside... Madam Yukari, tell me. Is this simply another one of your tests?",
                'Ran',
                'Ran')
        self.emote('Yukari', 'dotdotdot')

        self.say("I'm leaning toward yes. But don't try to ask me too much right now. I won't lay my cards down just yet.",
                'Yukari',
                'Yukari')
        self.say("Maybe you've noticed, but we've been pulling some strings behind the scenes. I certainly wish we were vacationing right, now, but trust me, that's the last thing on our minds.",
                'Yukari',
                'Yukari')
        self.say("I see. If you won't tell me any more, I'll leave it at that.",
                'Ran',
                'Ran')
        self.say("Oh, one more thing, Ran. It goes without saying, but let's keep our meeting a secret, hm?",
                'Yukari',
                'Yukari')
        self.say("Understood, madam.",
                'Ran',
                'Ran')
        self.say("And now it's time to say bye-bye. Good luck tomorrow! Toodles!",
                'Yuyuko',
                'Yuyuko')

        # Remove Yuyuko and Yukari, set scene to daytime
        self.fade_to_color('black', 1)
        self.kill_unit('Yuyuko')
        self.kill_unit('Yukari')
        self.set_unit_pos('Ran', (-1, -1))
        self.set_unit_pos('Tsubaki', (14, 20))
        self.set_unit_pos('Aya', (14, 19))
        self.set_bg_overlay(None)
        self.fade_from_color('black', 1)
        self.play_music('event01')
        self.center_on('Aya')

        self.say("Good morning!",
                'Aya',
                'Aya')

        # Move Youmu out from the house
        self.set_unit_pos('Youmu', (16, 17))
        self.move_unit('Youmu', (16, 18))

        self.emote('Youmu', 'exclamation')

        # Aya snaps a photo
        self.play_sfx('camera')
        self.fade_to_color('white', 0.2)
        self.fade_from_color('white', 0.2)

        self.say("Youmu! Have I got a special delivery for you!",
                'Aya',
                'Aya')

        # Rest of the party moves out of the house
        self.set_unit_pos('Reimu', (16, 17))
        self.move_unit('Reimu', (17, 17))
        self.set_unit_pos('Marisa', (16, 17))
        self.move_unit('Marisa', (17, 18))
        self.set_unit_pos('Mokou', (20, 18))
        self.move_unit('Mokou', (17, 19))
        self.set_unit_pos('Keine', (20, 18))
        self.move_unit('Keine', (18, 19))
        self.set_unit_pos('Ran', (20, 18))
        self.move_unit('Ran', (18, 17))
        self.set_unit_pos('Chen', (20, 18))
        self.move_unit('Chen', (18, 18))

        self.emote('Youmu', 'questionmark')

        self.say("'Lord Tenma to Youmu and friends: The First Ever Trial of the Red Feathers for Outsiders'...",
                'Youmu',
                'Youmu')

        # Aya snaps another photo
        self.play_sfx('camera')
        self.fade_to_color('white', 0.2)
        self.fade_from_color('white', 0.2)


        self.say("Tenma and the Order of the Red Feathers accept your proposal.",
                'Tsubaki',
                'Tsubaki')
        self.say("I'll be running this trial. Aya and Momiji will be assisting me. Upon success, you'll gain access to the sanctuary.",
                'Tsubaki',
                'Tsubaki')
        self.say("Are you able to tell us what to expect?",
                'Youmu',
                'Youmu')
        self.say("No. Come to the Nine Heavens Waterfall and you'll see for yourself. I hope you're prepared for this.",
                'Tsubaki',
                'Tsubaki')
        self.say("What a suspenseful morning to begin today with! Oooh, this is bound to be a great front page article on the evening edition! I sure hope my pen can keep up!",
                'Aya',
                'Aya')

        self.set_cursor_state(True)
        self.set_stats_display(True)
        self.done = True