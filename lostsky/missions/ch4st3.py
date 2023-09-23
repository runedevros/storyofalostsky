__author__ = 'Fawkes'

from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapobj import LightSource, SpiritSourcePoint
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Alchemist of the Moon'
        location = 'Eientei'
        id_string = 'CH4ST3'
        prereqs = ['CH4ST2']
        show_rewards = True
        desc = "I'm reporting onsite from Eientei where Youmu has begun tense negotiations with Eirin Yagokoro and Kaguya Houraisan. Youmu hopes to offer them some of her team's fighting strength in exchange for help in producing oil for the Lantern of Souls...in the name of defeating Fuyuhana."

        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch4st2.txt'
        mission_type = 'conversation'
        objective = None

        deploy_data = {'enable':False,
                       'max_units':None,
                       'preset_units':None,
                       'boxes':[]
                       }

        reward_list = []


        # Enemy Unit Data
        enemy_unit_data = [ ]

        initial_spells = {}
        initial_traits = {}
        initial_ai_states = {}
        initial_locations = {'Eirin':(20,16),
                             'Reisen':(22,16),

                             'Youmu':(21, 18),
                             'Ran':(19, 19),
                             'Chen':(20,19),
                             'Aya':(21, 19),
                             'Marisa':(22, 19),
                             'Reimu':(23, 19),
                             'Mokou':(20, 20),
                             'Keine':(22, 20),
        }
        reserve_units = []
        all_landmarks = [{'name':'Eientei',
                          'id_string':'eientei',
                          'location':(20, 16)}]

        required_starters = ['Aya', 'Marisa', 'Youmu', 'Keine', 'Ran', 'Chen', 'Reimu', 'Mokou','Eirin','Reisen']
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
        self.set_fog_state(True)
        self.set_bg_overlay('Night')
        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.play_music('event02')

        self.map.add_light_source(LightSource('North Lantern', (9,11), True, 5))
        self.map.add_ssp(SpiritSourcePoint('North SSP', (11, 10), 1))

        self.map.add_light_source(LightSource('Eientei 1', (19,17), True, 3))
        self.map.add_light_source(LightSource('Eientei 2', (23,17), True, 3))



        # Adds Eientei Crew
        self.add_to_party('Kaguya')
        self.set_unit_pos('Kaguya', (21,16))
        self.assign_spell('Kaguya', 'Holy Amulet')
        self.assign_spell('Kaguya', 'Fireball')
        self.assign_spell('Kaguya', 'Mysterium')
        self.center_on('Kaguya')

        self.say("It's much quieter here than I remember.",
                 'Youmu',
                 'Youmu')
        self.say("We're the last of the inhabitants of the Bamboo Forest now that I've sent Tewi away with the other rabbits.",
                 'Eirin',
                 'Eirin')
        self.say("We'll be fine without their help anyway.",
                 'Reisen',
                 'Reisen')
        self.say("Youmu, you want to help us fight, you said. This isn't be a one-way deal, is it. What do you want in exchange?",
                 'Eirin',
                 'Eirin')
        self.say("Correct. Allow us to explain. The one who leads the Kodama is called Fuyuhana. She is a spirit bound to the physical world by using a branch from her old tree.",
                 'Youmu',
                 'Youmu')
        self.say("If we can sever that link, we eliminate her ability to influence this world.",
                 'Ran',
                 'Ran')
        self.say("We especially want to seal her ability to gather clouds, and therefore Gensokyo's rains, which she's currently using to nourish her trees.",
                 'Ran',
                 'Ran')
        self.say("This lantern, the Lantern of Souls, will be able to draw Fuyuhana away from her branch. But first, we need to make some oil for it to burn. Unfortunately, none of us have the skill to make it.",
                 'Youmu',
                 'Youmu')
        self.emote('Eirin', 'dotdotdot')
        self.say("Hmm.",
                 'Eirin',
                 'Eirin')
        self.say("Hey. Are you all really going to cooperate? How can we trust you?",
                 'Reisen',
                 'Reisen')
        self.say("My money isn't on you guys if it's a test of endurance. Just putting it out there! I mean, think about it. Two against an entire army of vicious trees? Wasn't the last battle super hard?",
                 'Aya',
                 'Aya')

        self.startle('Kaguya')
        self.say("Three.",
                 'Kaguya',
                 'Kaguya')
        self.move_unit('Kaguya', (21,17))
        self.say("Soon. Eleven.",
                 'Kaguya',
                 'Kaguya')
        self.say("Eirin, let us agree to this exchange. I tire of hiding. I tire of being sheltered and constantly protected. This time, I will join the fray.",
                 'Kaguya',
                 'Kaguya')
        self.say("Princess! You mustn't!",
                 'Eirin',
                 'Eirin')
        self.say("We have remained in Eientei for too long, and we have grown complacent. We may be from the moon, but if we are to live in Gensokyo, we cannot turn a blind eye to the world around us.",
                 'Kaguya',
                 'Kaguya')
        self.say("Even if it means working with Mokou? Seriously?",
                 'Reisen',
                 'Reisen')
        self.emote('Mokou', 'scribble')
        self.say("We fight to survive, do we not? If this is the path to survival, than we shall take it. Mokou, I expect much from you. Do not let me down.",
                 'Kaguya',
                 'Kaguya')
        self.say("I won't lose to you, Kaguya. This is just a temporary truce. We're still not friends.",
                 'Mokou',
                 'Mokou')
        self.say("Ok...so. What's the plan again?",
                 'Reimu',
                 'Reimu')

        self.startle('Youmu')
        self.say("Just like in the forest, if we can defeat their leader, their forces will fall into disarray.",
                 'Youmu',
                 'Youmu')
        self.say("We'll have to take on Ayaka of the Pale Mist. She's the one who has us cornered here in Eientei. She's a master tactician, all right. No doubt about it.",
                 'Eirin',
                 'Eirin')
        self.say("Oh? A more brilliant tactician than the great \"Brain of the Moon\"?",
                 'Ran',
                 'Ran')
        self.say("Miss Yakumo, Miss Kamishirasawa, Miss Yagokoro. The greatest minds of Gensokyo are standing here together. Have faith in yourselves. We have more than enough wits to outsmart Ayaka!",
                 'Youmu',
                 'Youmu')
        self.say("Well, when you put it that way... Of course, we can defeat her!",
                 'Eirin',
                 'Eirin')

        self.say("I know morale is great and all, but we're not done talking. Fighting in this fog is our enemies' biggest advantage. How do we get rid of it?",
                 'Reimu',
                 'Reimu')
        self.say("The fog covers anything outside a lantern light's reach. Even if we clear parts of it out, it'll become foggy again pretty soon after.",
                 'Marisa',
                 'Marisa')
        self.say("Is there a spell that allows us to clear up the fog all at once?",
                 'Youmu',
                 'Youmu')
        self.say("We can amplify the light from the moonstones into a field effect spell. That just might dispel all the fog in a single instant.",
                 'Eirin',
                 'Eirin')
        self.say("We wanted to try it out, but with just us around, it was impossible. But it's worth a shot.",
                 'Reisen',
                 'Reisen')
        self.say("This seals the agreement. You will assist us in battle against Ayaka and help clear the blanket of fog that covers this forest!",
                 'Kaguya',
                 'Kaguya')
        self.say("Do you know where the Bamboo Forest's Spirit Source Points are? We'll need to control those before we can set up that spell.",
                 'Reimu',
                 'Reimu')
        self.say("Sure, they're just east of here. As luck would have it, that's also where Ayaka is right now.",
                 'Eirin',
                 'Eirin')
        self.say("No problemo! We can kill two birds with one stone. First, clear the fog. Then, defeat Ayaka.",
                 'Aya',
                 'Aya')
        self.say("All right. We have ourselves a plan. Based on Aya's reports, Ayaka is preparing for their final attack right now.",
                 'Ran',
                 'Ran')
        self.say("Then we're running out of time. What are we waiting for? Let's go!",
                 'Reisen',
                 'Reisen')

        self.say("Princess, Udonge, please go on ahead. Now. If this lamp oil is as you describe it, then it must be a similar component to the one used in lunar medicine.",
                 'Eirin',
                 'Eirin')
        self.say("Hand me your ingredients along with a pinch of your trust. I'll have it ready in no time.",
                 'Eirin',
                 'Eirin')

