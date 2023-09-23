from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'The Forest\'s Legend'
        location = 'Human Village'
        id_string = 'CH2ST4'
        prereqs = ['CH2ST3']
        show_rewards = False
        desc = "Legend has it that Fuyuhana Touji was a great Kodama Lord and former leader of the trees of the Forest of Magic. As today's special event, Akyu will hold a lecture concerning the Kodama Lords who have played a crucial role in the forest's past. That's really bad for me though. It sounds so boring. I usually sleep through these things. Anyway, on that note!"

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
                          ]

        initial_spells = {}
        initial_traits = {}
        initial_ai_states = {}
        initial_locations = {'Akyu':(15, 9),
                             'Keine':(15, 8),
                             'Mokou':(14, 8),

                             'Youmu':(17, 8),
                             'Ran':(18, 10),
                             'Chen':(18, 9),

                             'Reimu':(17, 9),
                             'Marisa':(17, 10),
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

        required_starters = ['Chen', 'Ran', 'Youmu', 'Marisa', 'Reimu', 'Keine', 'Mokou']
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
        Meeting with Akyu after the confrontation with the Kodama Lords
        """

        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.play_music('event01')
        self.center_on('Marisa')
        self.startle('Marisa')

        self.say("Geez!!! That was close!",
                'Marisa',
                'Marisa')
        self.say("Goodness, what a clamorous arrival. Are you all right?",
                'Akyu',
                'Akyu')
        self.say("It was an ambush! We had four Kodama Lords at our tail--we had no choice but to flee!",
                'Youmu',
                'Youmu')
        self.say("And let's not forget all the clouds vanishing.",
                'Mokou',
                'Mokou')
        self.say("Unfortunately, I'm not sure how long my barrier spell will hold! Our current sanctuary is sadly a temporary one.",
            'Keine',
            'Keine')
        self.say("So be it. We must quickly resolve this crisis!",
                'Youmu',
                'Youmu')
        self.say("Hey! That's the spirit, Youmu! You'll be a bona fide crisis resolver like Reimu and me in no time.",
                'Marisa',
                'Marisa')
        self.say("...I understand. Still, I made a promise, and there is much to talk about. Now is as good a moment as any.",
                'Akyu',
                'Akyu')
        self.say("Let me start at the very beginning, in ancient times, long before the foundation of Gensokyo itself has been established",
                'Akyu',
                'Akyu')
        self.play_music('event02')
        self.say("We begin with the birth of a single maple tree, spreading its roots over and within the Youkai Mountain, protecting it in a gentle yet firm embrace.",
                'Akyu',
                'Akyu')
        self.say("This tree lived proudly as the mountain's guardian, blessed by the grace of the goddess that lived in the mountain.",
                'Akyu',
                'Akyu')
        self.say("You refer to Princess Iwanaga, yes? She is the legendary goddess of immortality believed to reside upon Youkai Mountain.",
                'Keine',
                'Keine')
        self.say("Hmph, that's a name I'd rather not hear again. Is Fuyuhana immortal, too?",
                'Mokou',
                'Mokou')
        self.say("No, not quite. Because of the goddess, the trees who lived on Youkai Mountain were blessed with extraordinarily long lifetimes, but they did not share her immortality.",
                'Akyu',
                'Akyu')
        self.say("Moving along. Although the tree was born on the mountain, eventually, strong winds carried it to a vast plain. This was the beginning of the Forest of Magic.",
                'Akyu',
                'Akyu')
        self.say("As trees age, they gain a companion guardian spirit. These are the Kodama. Fuyuhana was the kodama that was bound to this first tree.",
                'Akyu',
                'Akyu')
        self.say("All the trees in the Forest of Magic originated from one tree?",
                'Chen',
                'Chen')
        self.say("That's mostly right. Some trees would eventually drift in, but Fuyuhana was also a particularly wise leader and strong protector of the forest.",
                'Akyu',
                'Akyu')
        self.say("Over the ages, she served as the leader of the Kodama and other flora and fauna in the Forest of Magic...",
                'Akyu',
                'Akyu')



        self.stop_music()

        # Scene with Reimu and Marisa dozing off at Akyu's explanation
        self.emote('Akyu', 'dotdotdot')
        self.pause(0.2)
        self.emote('Reimu', 'zzz')
        self.emote('Marisa', 'zzz')
        self.pause(0.2)

        self.emote('Keine', 'annoyed')
        self.move_unit('Keine', (16, 9))
        self.startle('Keine')

        self.say("All right, you two! Wake up! This is important! Don't make me treat you like a student who falls asleep in class!",
                'Keine',
                'Keine')
        self.say("Ah, Keine, I could use your assistance. I have an idea. You also: Reimu, Marisa, Youmu.",
                'Akyu',
                'Akyu')

        # Set everyone in position for the play
        # Reimu, Youmu, and Marisa are the actors
        self.fade_to_color('black', 1.0)
        self.set_unit_pos('Mokou', (10, 12))
        self.set_unit_pos('Akyu', (11, 11))
        self.set_unit_pos('Keine', (10, 10))
        self.set_unit_pos('Ran', (17, 10))
        self.set_unit_pos('Chen', (17, 12))

        self.set_unit_pos('Reimu', (17, 11))
        self.set_unit_pos('Youmu', (11, 10))
        self.set_unit_pos('Marisa', (14, 11))

        self.fade_from_color('black', 1.0)

        # Theater scene
        self.play_music('event01')
        self.emote('Reimu', 'scribble')
        self.say("So we just read these lines? Ugh...these look so wordy and formal. It's not anything like my usual way of talking.",
                'Reimu',
                'Reimu')
        self.say("Simply read it as it comes to you, Reimu. You will act as our great Kodama Lord, Fuyuhana Touji.",
                'Akyu',
                'Akyu')
        self.say("Youmu. You are her loyal retainer, Ayaka.",
                'Akyu',
                'Akyu')
        self.say("Marisa. You will be Hotaru, representative of the humans opposing Fuyuhana.",
                'Akyu',
                'Akyu')
        self.say("Oh. Oh! Ayaka? I think that was one of the Kodama Lords we fought.",
                'Chen',
                'Chen')
        self.say("Th-this is... I-I have never acted before!",
                'Youmu',
                'Youmu')
        self.say("Haha, same here. It could be fun though! At least it's way better than listening to Akyu's super long lecture.",
                'Marisa',
                'Marisa')
        self.say("Now that everyone has been assigned their roles, let us begin!",
                'Akyu',
                'Akyu')

        self.startle('Marisa')
        self.say("The Gensokyo Players present... Legend of the Forest of Magic by Hieda no Akyu!",
                'Marisa',
                'Marisa')
        self.startle('Marisa')
        self.say("Act 5, Scene 3. The End of the Kodama Lord's Reign! We will begin in the Forest of Magic from thousands of years ago.",
                'Marisa',
                'Marisa')
        self.say("We hope you enjoy this play!",
                'Marisa',
                'Marisa')

        # Fuyuhana and Ayaka talk about being cornered
        self.move_unit('Marisa', (12, 13))
        self.move_unit('Reimu', (14, 10))
        self.play_music('battle01')
        self.move_unit('Youmu', (13, 10))
        self.say("I have received the news. Haruna and the others have been defeated. Must your reign come to an end now? Will you not continue to fight?",
                'Ayaka (Youmu)',
                'Youmu')
        self.say("We may be blessed by by Iwanagi, but we are not immortal. It appears our continued expansion of our forest's boundaries is no longer to our benefit. It was only a matter of time.",
                'Fuyuhana (Reimu)',
                'Reimu')
        self.say("No! Please! We are still able to hold them back. They may have conquered the rest of the land, but I promise they will never reach the center of our forest.",
                'Ayaka (Youmu)',
                'Youmu')
        self.say("Fighting the humans and their youkai allies has taken a dreadful toll on our resources, morale, and our numbers.",
                'Fuyuhana (Reimu)',
                'Reimu')
        self.say("I have seen too many of our brothers and sisters, trees and Kodama alike, perish in this struggle. I tire of it.",
                'Fuyuhana (Reimu)',
                'Reimu')
        self.say("It is true that I have grossly underestimated their strength and their determination to defeat us. Regardless, I refuse to give up now! It is much too soon to do so.",
                'Ayaka (Youmu)',
                'Youmu')
        self.say("The humans fear the fulfillment of our retribution.",
                'Fuyuhana (Reimu)',
                'Reimu')
        self.say("After all, I am an elder Kodama Lord, and as such, the curse I release upon my death will unleash nature's wrath upon the village in the form of violent floods and incurable plagues.",
                'Fuyuhana (Reimu)',
                'Reimu')
        self.say("They will cower before they muster the courage to kill me.",
                'Fuyuhana (Reimu)',
                'Reimu')
        self.say("This may be our single hope of saving our precious forest.",
                'Fuyuhana (Reimu)',
                'Reimu')
        self.say("Ye gods! One of them comes this way!",
                'Ayaka (Youmu)',
                'Youmu')

        # Hotaru arrives to propose an end to the crisis
        self.move_unit('Marisa', (14, 12))
        self.say("You. Tell me why you dare step foot upon this sacred land.",
                'Ayaka (Youmu)',
                'Youmu')
        self.say("We care not. We have chosen to cut down your beloved tree.",
                'Hotaru (Marisa)',
                'Marisa')

        self.startle('Youmu')
        self.move_unit('Youmu', (14, 11))
        self.emote('Youmu', 'annoyed')
        self.say("You pompous--I shall see to it that you die now! I would sooner meet my own death before I so much as see you lay a finger upon my master!",
                'Ayaka (Youmu)',
                'Youmu')
        self.say("Be reasonable and listen! We do not wish to incur the forest's wrath. I would like for us to reach an agreement. A pact, if you will.",
                'Hotaru (Marisa)',
                'Marisa')
        self.say("Pah! What could you measly humans possibly offer us?",
                'Ayaka (Youmu)',
                'Youmu')
        self.say("Silence, Ayaka. Now. Speak, human. I will listen.",
                'Fuyuhana (Reimu)',
                'Reimu')

        self.move_unit('Youmu', (13, 10))
        self.say("What you cherish most is the protection of the forest.",
                'Hotaru (Marisa)',
                'Marisa')
        self.say("Upon your death, we will allow your spirit to remain and maintain vigil over the forest's well-being...for eternity. We further vow that we will bring harm upon the forest.",
                'Hotaru (Marisa)',
                'Marisa')
        self.say("The very proposal sickens me to the very depths of my being! We refuse your preposterous request!",
                'Ayaka (Youmu)',
                'Youmu')


        self.emote('Reimu', 'dotdotdot')

        self.say("Ayaka. Ayaka, do not forget. We owe everything to this forest. For the entirety of our being, we will be are bound to be its guardians.",
                'Fuyuhana (Reimu)',
                'Reimu')
        self.say("My death is but a small price to pay, if it means I may continue to be loyal to my duty. I pray you understand.",
                'Fuyuhana (Reimu)',
                'Reimu')
        self.say("No...",
                'Ayaka (Youmu)',
                'Youmu')
        self.say("Thank you, human. I will accept your terms.",
                'Fuyuhana (Reimu)',
                'Reimu')
        self.say("The pact is complete. I am sorry, Ayaka. Our selfishness allowed this forest to grow and spread far and wide, and yet even after committing that sin, we are still allowed to act as its protectors.",
                'Fuyuhana (Reimu)',
                'Reimu')
        self.say("I cannot possibly ask for more than this. You will understand one day, Ayaka. I am certain...",
                'Fuyuhana (Reimu)',
                'Reimu')

        # Move everyone to the center of the stage
        self.stop_music()
        self.play_music('event02')
        self.move_unit('Youmu', (13, 11))
        self.move_unit('Reimu', (14, 11))
        self.move_unit('Marisa', (15, 11))
        self.say("And so the spirit of Fuyuhana maintained vigil over the forest for the next several centuries.",
                'Youmu',
                'Youmu')
        self.say("Throughout the centuries, she was known as ghost who would banish enemies from the forest as well as guide those lost safely to the forest's edge.",
                'Marisa',
                'Marisa')
        self.say("What has become of her? Why has she initiated our current crisis? Alas, this I cannot answer...for they have yet to be recorded in the annals of history.",
                'Reimu',
                'Reimu')

        # chen is pleased
        self.emote('Chen', 'musicnote')
        self.say("*clap* *clap* *clap*",
                'Chen',
                'Chen')

        self.play_music('event01')
        # Restore character positions
        self.fade_to_color('black', (1.0))
        self.set_unit_pos('Akyu', (14, 8))
        self.set_unit_pos('Youmu', (16, 8))
        self.set_unit_pos('Mokou', (17, 7))
        self.set_unit_pos('Keine', (18, 7))
        self.set_unit_pos('Ran', (17, 8))
        self.set_unit_pos('Chen', (18, 8))
        self.set_unit_pos('Reimu', (17, 9))
        self.set_unit_pos('Marisa', (18, 9))
        self.fade_from_color('black', (1.0))

        self.say("I'm quite impressed. I'll have to try that in my classes next time.",
                'Keine',
                'Keine')

        self.emote('Youmu', 'lightbulb')
        self.say("I have an idea of our next destination. Let us pay a visit to Fuyuhana's birthplace on Youkai Mountain.",
                'Youmu',
                'Youmu')
        self.say("Ah, yes. There is a legend among the Tengu youkai that live upon that mountain. It tells of a Kodama and a tree even older than Fuyuhana that took root upon the mountain's peak.",
                'Akyu',
                'Akyu')
        self.say("What a smart decision! And since it's so smart, maybe our mistresses went there, too.",
                'Chen',
                'Chen')
        self.say("Smart or not, it's not going to be easy convincing the Tengu to let us up there.",
                'Reimu',
                'Reimu')
        self.say("Will it be hard to? I don't know much since I've never been to the Youkai Mountain before. What's it like?",
                'Chen',
                'Chen')
        self.say("It's a very dangerous area for outsiders like us since the Tengu youkai that live there are fiercely territorial. They are a very proud people.",
                'Ran',
                'Ran')
        self.say("So they would rather not involve themselves with matters that do not directly concern them. Including ours, probably. ",
                'Ran',
                'Ran')
        self.say("Then we'll just have to force our way in there.",
                'Marisa',
                'Marisa')
        self.say("Hang on! Breaking down the front gate will give us the opposite of the Tengus favor, and they'll have us running with our tails between our legs!",
                'Ran',
                'Ran')
        self.say("Whatever. Reimu and I got in last time that way. They sent Aya to fight us, but she was a total pushover.",
                'Marisa',
                'Marisa')
        self.say("The Tengu will be more on edge. If they've caught wind of the Kodama Lords' recent activities beyond the forest, the Tengu won't be allowing visitors in so readily.",
                'Mokou',
                'Mokou')
        self.say("Ah, but the crisis does relate to the Tengu people somewhat. With the clouds' disappearance, there won't be much rain until this crisis has been resolved, which surely they need...if not everyone in Gensokyo.",
                'Youmu',
                'Youmu')
        self.say("Areas that are lined with rivers like Youkai Mountain will be fine for the time being, but the human village and other areas won't be, especially with summer's imminent arrival.",
                'Keine',
                'Keine')
        self.say("Yikes. We gotta hurry and resolve it then.",
                'Marisa',
                'Marisa')
        self.say("Still, Youmu's right. They may be stubborn, but the looming threat of an eventual drought may force the Tengu to bend our way.",
                'Keine',
                'Keine')
        self.say("We may be able to successfully negotiate with them, allowing us entry into the mountain.",
                'Keine',
                'Keine')
        self.say("I don't intend on giving up at any rate, so we should prepare ourselves for a fairly rough climb to the top. This next segment of our journey will not be easy.",
                'Keine',
                'Keine')
        self.say("Yes. Let's head over right away!",
                'Youmu',
                'Youmu')
        self.say("Hmm, Youkai Mountain is to the south, right?",
                'Chen',
                'Chen')
        self.say("Yeah, there's a path from the village leading there.",
                'Reimu',
                'Reimu')
        self.say("Oh, yes! Please wait, everyone. Before I forget...",
                'Akyu',
                'Akyu')
        # Akyu goes into her house to pick up stuff
        self.move_unit('Akyu', (14, 9))
        self.emote('Akyu', 'questionmark')
        self.emote('Akyu', 'dotdotdot')
        self.emote('Akyu', 'exclamation')
        self.move_unit('Akyu', (14, 8))

        self.say("I managed to come upon this recipe for the spell Healing Drop while I was going through my archives.",
                'Akyu',
                'Akyu')
        self.say("I believe you will find it useful. And now you're free to go. I wish you all a safe and fulfilling journey.",
                'Akyu',
                'Akyu')
        self.add_recipe('Healing Drop')
        self.say("Healing Drop can now be synthesized!",
                None,
                None)
        self.set_stats_display(True)
        self.set_cursor_state(True)