from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, ArrivalTrigger
class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'Lost Lantern'
        location = 'Marisa\'s House'
        id_string = 'CH1ST3'
        prereqs = ['CH1ST2']
        show_rewards = False
        desc = "After joining up with Youmu and her party, Marisa leads them north towards her home.  With my great observation skills, I spotted one of the Kodama Lords at Marisa's place. She told me she had come to stop that \"--wretched tree wrecking witch who would blow up the whole forest if given the chance\" dead in her tracks. I've also heard rumors floating about that some of the bug youkai have allied themselves with these Kodama Lords. I'll definitely be keeping my eyes peeled!"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch1st3v2.txt'
        mission_type = 'battle'
        objective = {'type':'Arrive and Defeat Boss',
                     'target': 'Wriggle',
                     'location_name': 'Marisa\'s House',
                     'location_box': (19, 6, 3, 3),
                     'desc': "Defeat Wriggle and get any party member to Marisa's house (3x3 box)!"}

        deploy_data = {'enable':False,
                       'max_units':None,
                       'preset_units':None,
                       'boxes':[]
                       }

        reward_list = [('treasure', 'synth_wood'),
                       ('treasure', 'synth_metal'),
                      ]

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 4},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 4},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 4},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree D',
                                    'level': 4},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree E',
                                    'level': 4},

                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 4},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 4},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy C',
                                    'level': 4},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy D',
                                    'level': 4},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy E',
                                    'level': 4},

                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly A',
                                    'level': 5},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly B',
                                    'level': 5},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly C',
                                    'level': 5},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly D',
                                    'level': 5},
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly E',
                                    'level': 5},

                           {'template_name': 'Kotone',
                                'unit_name': 'Kodama Lord',
                                    'level': 8},

                           {'template_name': 'Wriggle',
                                'unit_name': 'Wriggle',
                                    'level': 6},
                          ]

        initial_spells = {'Walking Tree A':['Leaf Crystal'],
                          'Walking Tree B':['Leaf Crystal'],
                          'Walking Tree C':['Leaf Crystal'],
                          'Walking Tree D':['Leaf Crystal'],
                          'Walking Tree E':['Leaf Crystal'],
                          'Fairy A':['Holy Amulet'],
                          'Fairy B':['Fireball'],
                          'Fairy C':['Dagger Throw'],
                          'Fairy D':['Holy Amulet'],
                          'Fairy E':['Dagger Throw'],
                          'Firefly A':['Fireball'],
                          'Firefly B':['Fireball'],
                          'Firefly C':['Fireball'],
                          'Firefly D':['Fireball'],
                          'Firefly E':['Fireball'],
                          'Wriggle':['Fireball']}

        initial_traits = {'Firefly A':['Flight'],
                          'Firefly B':['Flight'],
                          'Firefly C':['Flight'],
                          'Firefly D':['Flight'],
                          'Firefly E':['Flight'],
                          'Wriggle':['Flight', 'Mirage']}

        initial_ai_states = {'Walking Tree A':'Attack',
                             'Walking Tree B':'Attack',
                             'Walking Tree C':'Attack',
                             'Walking Tree D':'Attack',
                             'Walking Tree E':'Attack',
                             'Fairy A':'Attack',
                             'Fairy B':'Attack',
                             'Fairy C':'Attack',
                             'Fairy D':'Attack',
                             'Fairy E':'Attack',
                             'Firefly A':'Attack',
                             'Firefly B':'Attack',
                             'Firefly C':'Attack',
                             'Firefly D':'Defend',
                             'Firefly E':'Defend',
                             'Wriggle':'Attack'}

        initial_locations = {'Ran':(15, 23),
                             'Chen':(16, 23),
                             'Youmu':(17, 23),
                             'Marisa':(16, 22),

                             'Walking Tree A':(4, 14),
                             'Walking Tree B':(10, 17),
                             'Walking Tree C':(1, 7),
                             'Walking Tree D':(10, 4),
                             'Walking Tree E':(9, 5),

                             'Fairy A':(6, 16),
                             'Fairy B':(3, 9),
                             'Fairy C':(4, 6),
                             'Fairy D':(19, 8),
                             'Fairy E':(21, 8),

                             'Firefly A':(17, 12),
                             'Firefly B':(21, 13),
                             'Firefly C':(15, 3),
                             'Firefly D':(13, 2),
                             'Firefly E':(17, 2),

                             'Kodama Lord':(14, 1),
                             'Wriggle':(15, 1),
                             }
        reserve_units = []#[list of unit names to deploy later in mission]
        all_landmarks = [{'name':'House1',
                          'id_string':'house_1',
                          'location':(20, 7)},
                         {'name':'LP 1',
                          'id_string':'lilypad',
                          'location':(22, 3)},
                         {'name':'CB 1',
                          'id_string':'cherryblossom_tree',
                          'location':(6, 6)},
                         {'name':'CB 2',
                          'id_string':'cherryblossom_tree',
                          'location':(15, 12)},
                         ]

        required_starters = ['Youmu', 'Chen', 'Ran', 'Marisa']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [MarisaHouseMAE(), NorthTreasureMAE(), SouthTreasureMAE()]
        required_survivors = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Wriggle']
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
        Arriving at Marisa's house, the heroes find an ambush set up by Kodama Lord
        and Wriggle.
        """
        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.center_on('Wriggle')
        self.say("So that tiny human is still making a racket?",
                'Wriggle',
                'Wriggle')
        self.say("And after we went through all that trouble to get her cornered, too...  Make sure she doesn't make it back, all right!",
                'Kodama Lord',
                'Kotone')
        self.say("Hm. But she's already here.",
                'Wriggle',
                'Wriggle')
        self.say("WHAT!?",
                'Kodama Lord',
                'Kotone')

        # Scene with hero party discussing what to do next
        self.center_on('Marisa')
        self.say("Just a bit farther!",
                'Marisa',
                'Marisa')
        self.say("I managed to cook up enough spell fuel for my Master Spark from the mushrooms I collected, but that's all I got.",
                'Marisa',
                'Marisa')
        self.say("Ohh! So that's what you were doing with those glass tubes along the way!",
                'Chen',
                'Chen')
        self.play_music('battle01')
        self.say("Everyone, be careful. I sense a powerful presence nearby.",
                'Ran',
                'Ran')
        self.say("We'll have to face it. Is everyone ready?",
                'Youmu',
                'Youmu')
        self.move_unit('Marisa', (16, 21))
        self.startle('Marisa')
        self.say("Just plow me a path to my house, and I'll cook whatever \"boss\" is loitering over there to a crisp!",
                'Marisa',
                'Marisa')
        self.say("I keep a fat magic fuel stash at home, so I'll easily make short work of 'em.",
                'Marisa',
                'Marisa')
        self.set_cursor_state(True)
        self.center_on_coords((20, 7))
        self.pause(0.5)
        self.say("If I can refuel my magic reactor to full power, nothing can stand in my way! Haha!",
                'Marisa',
                'Marisa')
        self.set_cursor_state(False)
        self.center_on('Wriggle')
        self.say("W-what are you waiting for?! S-stop them!",
                'Kodama Lord',
                'Kotone')
        self.say("Mm-hmm. So what exactly do you want us to do?",
                'Wriggle',
                'Wriggle')
        self.say("What do I--isn't it obvious? Defeat them! Or chase them out of the forest! Just get rid of them!!! Here, I'll even let you use these fairies and walking trees to get it done.",
                'Kodama Lord',
                'Kotone')
        self.say("Mm'kay. Just don't forget our promise. In exchange for our help, the other insects and me get to stay.",
                'Wriggle',
                'Wriggle')
        self.say("Don't take me for a fool. I know. I'll leave her to you. That witch isn't the only troublemaker in this forest, but I'm getting especially sick of her.",
                'Kodama Lord',
                'Kotone')
        self.move_unit('Kodama Lord', (14, 0))
        self.kill_unit('Kodama Lord')
        self.center_on('Youmu')

        self.set_cursor_state(True)
        self.set_stats_display(True)


class MarisaHouseMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((19, 6, 3, 3), 1, 'Marisa')]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        If Marisa arrives at her house, she gets a fully charged Master Spark and 900 SC
        """

        self.say("Yes! Woo-hoo! Made it!",
                'Marisa',
                'Marisa')
        self.say("All right! Now it's time to blaze right through with my signature move, Master Spark!!!",
                'Marisa',
                'Marisa')
        self.set_spirit_charge('Marisa', 900)
        self.say("Marisa's SC is maxed out!",
                None,
                None)
        self.say("Master Spark Spell Card fully charged!",
                None,
                None)
        self.set_spell_uses('Marisa', 'Master Spark', 5)


class NorthTreasureMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((15, 12, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        self.say("Buried at the foot of the cherry tree is a small rusted box.",
                None,
                None)
        self.say("Acquired Treasure Item: Rain Tear!",
                None,
                None)
        self.add_item('treasure', 'synth_water', 1)

class SouthTreasureMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((6, 6, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        self.say("Buried at the foot of the cherry tree is a small rusted box.",
                None,
                None)
        self.say("Acquired Treasure Item: Ancient Amber!",
                None,
                None)
        self.add_item('treasure', 'synth_wood', 1)

class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.remove_all_enemies()
        self.stop_music()
        self.set_unit_pos('Youmu', (18, 7))
        self.set_unit_pos('Ran', (19, 7))
        self.set_unit_pos('Chen', (19, 8))
        self.set_unit_pos('Marisa', (19, 6))
        self.set_unit_pos('Wriggle', (16, 7))

    def execute(self):

        # Conversation with Wriggle and hero party
        self.center_on('Wriggle')
        self.say("Okay! Okay! I surrender!",
                'Wriggle',
                'Wriggle')
        self.say("Music to my ears! So, mind telling us what you were doing with those things?",
                'Marisa',
                'Marisa')
        self.say("Sure, but I really don't know much. I do know that the youkai behind this is an ancient forest spirit that's suddenly become active again.",
                'Wriggle',
                'Wriggle')
        self.say("She's forcibly retaking the forest to protect it from those she thinks'll hurt it.",
                'Wriggle',
                'Wriggle')
        self.say("Ah. I see now. That explains why they were targeting Marisa.",
                'Youmu',
                'Youmu')
        self.say("Hey! I try my best not to blow up the forest... I mean. See? It's still here. Right?",
                'Marisa',
                'Marisa')
        self.say("She has a lot of support from the animal youkai here. Y'know, bugs like me and beasts and stuff. We're really fond of the forest, so yeah.",
                'Wriggle',
                'Wriggle')
        self.say("So in just a small amount of time, she's managed to organize a army that's got most of the youkai shaking in their boots! Even the most of the fuzzballs here have already fled.",
                'Wriggle',
                'Wriggle')
        self.say("And me, too. I'm leaving the forest too. The forest will still have its fair share of bugs, but it won't always need me. Eh, it should be ok.",
                'Wriggle',
                'Wriggle')
        self.say("Please, spare us a moment more. I have one more question. Have you heard anything of our mistresses?",
                'Youmu',
                'Youmu')
        self.say("Your mistresses?  Well...there were a lot of ghosts this morning, if that means anything to you.",
                'Wriggle',
                'Wriggle')
        self.say("Ghosts? Then--did you meet with Lady Yuyuko?",
                'Youmu',
                'Youmu')
        self.say("Nope! The only thing I found aside from all those pesky spirits would be this.",
                'Wriggle',
                'Wriggle')
        self.say("This--this is the Lantern of Souls!",
                'Youmu',
                'Youmu')

        self.add_item('treasure', 'broken_lantern', 1)
        self.say("Wow! A clue, a clue!",
                'Chen',
                'Chen')
        self.say("Hey, so where'd you find this anyway?",
                'Marisa',
                'Marisa')
        self.say("Um. Around here.",
                'Wriggle',
                'Wriggle')
        self.say("So that means we're on the right track! Right?",
                'Chen',
                'Chen')
        self.say("Not necessarily. They could've gone just about anywhere by now.",
                'Marisa',
                'Marisa')
        self.say("They're probably long gone by now. There was a big fight here last night, and this got knocked out from the scene, so I went ahead and picked it up. Curiosity, mostly.",
                'Wriggle',
                'Wriggle')
        self.say("Anyways, you four'd best get out of here. The tree youkai are more active at night, and the more aggressive ones'll definitely want a piece of you.",
                'Wriggle',
                'Wriggle')
        self.say("Wriggle's right. By sunset, they'll likely have us surrounded. Let's retreat for now.",
                'Ran',
                'Ran')
        self.say("And then what? We must know where our mistresses went after that fight.",
                'Youmu',
                'Youmu')
        self.say("So according to bugsy here, there's an ancient tree spirit causing this mess, right?",
                'Marisa',
                'Marisa')
        self.say("Let's see if we can find out more about her. Those two troublemakers you're all so worried about are prolly doing the same thing.",
                'Marisa',
                'Marisa')
        self.say("Now I don't know too much about the forest's past, but I bet those history buffs in the human village do. Maybe they can push you all in the right direction.",
                'Marisa',
                'Marisa')
        self.say("Before that, Marisa, you should probably grab whatever items you need from your house now. There's not going to be much left of this place once the other youkai arrive.",
                'Ran',
                'Ran')
        self.say("Right. ...Geez, my poor house.",
                'Marisa',
                'Marisa')

        # Marisa goes back to her house to get stuff
        self.move_unit('Marisa', (20, 7))
        self.startle('Marisa')
        self.move_unit('Marisa', (19, 6))

        self.say("Well, I'm going now. The rest of the gang is waiting for me.",
                'Wriggle',
                'Wriggle')

        self.move_unit('Wriggle', (16, 0))
        self.set_cursor_state(True)
        self.set_stats_display(True)