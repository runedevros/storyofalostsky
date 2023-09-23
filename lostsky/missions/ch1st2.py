from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, ArrivalTrigger, CustVarTrigger

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'Marisa\'s Arrival'
        location = 'Central Forest'
        id_string = 'CH1ST2'
        prereqs = ['CH1ST1']
        show_rewards = True
        desc = "Early this morning, I spoke with Marisa Kirisame. She was minding her business, peacefully hunting for mushrooms, when suddenly, trees began to storm violently past! And there she stood, confused, desolate and alone, anxious to return home. What did the trees want? What were they after? Stay tuned! You can bet this here reporter will do all she can to find out!"
        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch1st2b.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat Boss',
                     'target':'Kodama Lord',
                     'desc':'Defeat the Kodama Lord!'
                     }

        deploy_data = {'enable':False,
                       'max_units':None,
                       'preset_units':None,
                       'boxes':[]
                       }

        reward_list = [('spell_action', 'Rice Cake'),
                       ('treasure', 'synth_fire'),
                      ]

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 4},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree C',
                                    'level': 4},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree D',
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
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy F',
                                    'level': 4},
                           {'template_name': 'Kodama Lord',
                                'unit_name': 'Kodama Lord',
                                    'level': 5},

                           #intro scene enemies
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 2},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball A',
                                    'level': 1},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball B',
                                    'level': 1},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball C',
                                    'level': 1},
                          ]

        initial_spells = {'Walking Tree A':['Leaf Crystal'],
                          'Walking Tree B':['Leaf Crystal'],
                          'Walking Tree C':['Leaf Crystal'],
                          'Walking Tree D':['Leaf Crystal'],
                          'Fairy A':['Holy Amulet'],
                          'Fairy B':['Holy Amulet'],
                          'Fairy C':['Fireball'],
                          'Fairy D':['Fireball'],
                          'Fairy E':['Fireball'],
                          'Fairy F':['Holy Amulet'],
                          'Kodama Lord':['Leaf Crystal'],
                          'Fuzzball A':['Dagger Throw'],
                          'Fuzzball B':['Holy Amulet'],
                          'Fuzzball C':['Holy Amulet']}

        initial_traits = {}
        initial_ai_states = {'Walking Tree A':'Attack',
                          'Walking Tree B':'Attack',
                          'Walking Tree C':'Attack',
                          'Walking Tree D':'Attack',
                          'Fairy A':'Defend',
                          'Fairy B':'Defend',
                          'Fairy C':'Defend',
                          'Fairy D':'Defend',
                          'Fairy E':'Defend',
                          'Fairy F':'Defend',
                          'Kodama Lord':'Attack',
                          'Fuzzball A':'Attack',
                          'Fuzzball B':'Attack',
                          'Fuzzball C':'Attack'}

        initial_locations = {'Ran':(0, 22),
                             'Chen':(0, 24),
                             'Youmu':(1, 23),

                             'Walking Tree B':(40, 20),
                             'Fuzzball A':(40, 20),
                             'Fuzzball B':(40, 20),
                             'Fuzzball C':(40, 20),

                             'Walking Tree A':(24, 23),
                             'Walking Tree C':(28, 26),
                             'Walking Tree D':(27, 12),

                             'Fairy A':(12, 12),
                             'Fairy B':(10, 9),
                             'Fairy C':(16, 11),
                             'Fairy D':(19, 9),
                             'Fairy E':(12, 8),
                             'Fairy F':(14, 10),
                             'Kodama Lord':(18, 9),

                             }
        reserve_units = []#[list of unit names to deploy later in mission]
        all_landmarks = [{'name':'M1',
                          'id_string':'mushroom',
                          'location':(10, 11)},
                         {'name':'M2',
                          'id_string':'mushroom',
                          'location':(8, 8)},
                         {'name':'M3',
                          'id_string':'mushroom',
                          'location':(23, 8)},
                         {'name':'M4',
                          'id_string':'mushroom',
                          'location':(18, 10)},
                         {'name':'M5',
                          'id_string':'mushroom',
                          'location':(24, 21)},
                         {'name':'M6',
                          'id_string':'mushroom',
                          'location':(11, 18)},
                         {'name':'M7',
                          'id_string':'mushroom',
                          'location':(14, 22)},
                         {'name':'M8',
                          'id_string':'mushroom',
                          'location':(13, 27)},
                         {'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(27, 23)},
                         ]

        required_starters = ['Youmu', 'Chen', 'Ran']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [DirectPathMAE(),
                                AlternatePathMAE(),
                                TreasureAlertMAE(),
                                TreasureFoundMAE(),
                                ]
        post_mission_MAE = PostMissionMAE()
        required_survivors = ['Youmu', 'Chen', 'Ran', 'Marisa']

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
        Marisa arrives, tutorial part 2
        """

        self.set_cursor_state(False)
        self.set_stats_display(False)

        # Set up Marisa
        self.add_to_party('Marisa')
        self.assign_spell('Marisa', 'Fireball')
        self.assign_spell('Marisa', 'Master Spark')
        self.set_spell_uses('Marisa', 'Master Spark', 2)
        self.set_spirit_charge('Marisa', 505)
        self.set_unit_pos('Marisa', (30, 22))

        # Heroes arrive on the scene
        self.center_on('Youmu')
        self.move_unit('Youmu', (3, 23))
        self.move_unit('Ran', (2, 22))
        self.move_unit('Chen', (2, 24))


        self.say("Are you sure we're going the right way?",
                'Chen',
                'Chen')
        self.say("We must be! We haven't the time to be lost!",
                'Youmu',
                'Youmu')
        self.say("Shh! Wait. Something's coming.",
                'Ran',
                'Ran')

        # Setup intro scene
        self.set_unit_pos('Fuzzball A', (13, 6))
        self.set_unit_pos('Fuzzball B', (13, 6))
        self.set_unit_pos('Fuzzball C', (13, 6))
        self.set_unit_pos('Walking Tree B', (13, 6))

        # Three Fuzzballs move in.
        # One of them tries to go towards Youmu, but she blocks the way
        # All Fuzzballs retreat
        self.move_unit('Fuzzball A', (13, 23))
        self.move_unit('Fuzzball B', (13, 22))
        self.move_unit('Fuzzball C', (13, 21))
        self.move_unit('Walking Tree B', (13, 18))
        self.move_unit('Fuzzball A', (7, 23))
        self.move_unit('Walking Tree B', (13, 20))
        self.move_unit('Fuzzball B', (13, 31))
        self.move_unit('Fuzzball C', (13, 31))
        self.move_unit('Fuzzball A', (5, 23))
        self.move_unit('Youmu', (4, 23))
        self.startle('Youmu')
        self.move_unit('Fuzzball A', (13, 23))
        self.move_unit('Fuzzball A', (13, 31))
        self.move_unit('Walking Tree B', (13, 22))


        # Remove the three fuzzballs in the intro scene
        self.kill_unit('Fuzzball A')
        self.kill_unit('Fuzzball B')
        self.kill_unit('Fuzzball C')

        # Marisa's entrance
        self.play_music('battle01')
        self.say("Outta my way!!!",
                'Marisa',
                'Marisa')
        self.move_unit('Marisa', (17, 22))

        # Marisa uses MS on Tree
        self.script_battle('Marisa',
                           'Walking Tree B',
                           {'lhs_hit':True,
                            'lhs_crit':True,
                            'lhs_equip':1,
                            'rhs_hit':True,
                            'rhs_crit':False,
                            'rhs_equip':0
                            }
                           )
        self.say("Isn't that...",
                'Youmu',
                'Youmu')

        self.move_unit('Marisa', (15, 22))

        # Hero group moves up
        self.move_unit('Youmu', (6, 23))
        self.move_unit('Ran', (5, 22))
        self.move_unit('Chen', (5, 24))
        self.say("Marisa?",
                'Youmu',
                'Youmu')
        self.move_unit('Youmu', (11, 23))
        self.move_unit('Ran', (11, 22))
        self.move_unit('Chen', (11, 24))
        self.center_on('Youmu')

        self.say("Hm? You looking for trouble?",
                'Marisa',
                'Marisa')
        self.say("If by trouble you mean those fuzzballs, then we've already found it.",
                'Ran',
                'Ran')
        self.say("Yeah! And what's more, our mistresses are gone! They went into the forest last night, and now, poof! They're gone!",
                'Chen',
                'Chen')
        self.say("That so? So those two big troublemakers disappear and then the forest goes nuts the morning after? Ha! 'Course it would.",
                'Marisa',
                'Marisa')
        self.say("It's as if you suggest that they are behind all of this.",
                'Youmu',
                'Youmu')
        self.say("You saying they aren't?",
                'Marisa',
                'Marisa')
        self.emote('Youmu', 'dotdotdot')
        self.emote('Marisa', 'dotdotdot')
        self.say("... Um, hey. Weren't we in a hurry?",
                'Chen',
                'Chen')
        self.say("Got important places to be, do you? Well! How 'bout I tag along and help you out?",
                'Marisa',
                'Marisa')
        self.say("...There has to be a catch. What do you want in return?",
                'Ran',
                'Ran')
        self.say("Heh, well! Those jerks caught me while I was gathering mushrooms for my spells, and now they've completely cut me off from my house!",
                'Marisa',
                'Marisa')
        self.say("I've only got enough fuel for one--super awesome--Master Spark spell!",
                'Marisa',
                'Marisa')
        self.say("That's my story. My place is just up ahead. In short, you kids are gonna help me get my stuff back, and I get to come with and lend you me plus my awesome magic! 'Kay? 'Kay!",
                'Marisa',
                'Marisa')
        self.say("That sounds reasonable. Very well, let us head for Marisa's house.",
                'Youmu',
                'Youmu')
        self.say("Ah... Hush, everyone! The voices are coming closer!",
                'Ran',
                'Ran')

        # Spying on the actions of the Kodama Lord and her servants
        self.move_unit('Ran', (10, 20))
        self.center_on('Ran')
        self.pause(1.0)
        self.center_on('Kodama Lord')
        self.set_cursor_state(True)
        self.pause(0.5)

        self.move_unit('Fairy F', (17, 9))
        self.startle('Fairy F')

        self.say("I see, I see. Let's keep the pressure up then. We need to control every last inch of this forest.",
                '???',
                'Kodama')
        self.startle('Fairy F')
        self.move_unit('Fairy F', (14, 10))
        self.say("Ugh, what a pain. These forest residents are way more stubborn than we expected.",
                '???',
                'Kodama')
        self.say("But all that pain's paid off! This setup is absolutely perfect! That dumb magician can't possibly make it past this trap! Ehehehe!",
                '???',
                'Kodama')

        # Heroes plan their next actions
        self.set_cursor_state(False)
        self.center_on('Ran')
        self.move_unit('Ran', (11, 22))
        self.center_on('Ran')
        self.say("That's a Kodama. They're the protectors and leaders of the tree youkai. Things make a lot more sense now, if they're the ones in charge of this mess.",
                'Ran',
                'Ran')
        self.center_on('Marisa')
        self.say("They sure talk a lot over setting up a trap of all things. We've heard plenty. Let's just blast our way through!",
                'Marisa',
                'Marisa')
        self.say("Hang on! You only have one Spark spell left, right? Let's just avoid the trap, and keep moving. What we want is their leader.",
                'Ran',
                'Ran')
        self.say("Since she's the brains behind all this, once she's gone, her lackeys will become confused and scatter, giving us a path through.",
                'Ran',
                'Ran')
        self.set_cursor_state(True)
        self.center_on('Walking Tree A')
        self.pause(1.0)
        self.say("Oh. Well, there's a a small path that circles around this place just nearby. We can use it to reach that blabbermouth.",
                'Marisa',
                'Marisa')
        self.center_on('Walking Tree D')
        self.pause(1.0)
        self.center_on('Marisa')
        self.set_cursor_state(False)
        self.say("The longest road is the shortest path... Nevermind--we're trusting you.",
                'Ran',
                'Ran')
        self.say("Marisa joins the party!",
                None,
                None)
        self.say("I'm a witch, so I may not be able to take many hits, but I sure can cover a lot of ground--and fast!",
                'Marisa',
                'Marisa')
        self.set_cursor_state(True)
        self.set_stats_display(True)

        tutorial_selection = self.choice('Would you like to see a tutorial on Elemental Relations and Traits?', ['Yes', 'No'])
        if tutorial_selection == 'Yes':

            self.set_stats_display(False)
            self.say("We have several enemies in this forest, many much stronger than the ones we've faced before. It's going to be difficult, so we need to strategize. What can we use to our advantage in battle?",
                    'Youmu',
                    'Youmu')
            self.say("Oh, I know! Youmu, since you're not a sorcerer, you probably don't know this. Marisa, are you familiar with the concept of Magic Flow?",
                    'Ran',
                    'Ran')
            self.say("'Course I am! Every magician knows about that! Guess this means explanation time for the rest of you though.",
                    'Marisa',
                    'Marisa')

            # Tutorial part 1 - Spell Relations
            self.show_image('tutorial_spell_type', 'tutorial_spell_type.png', (170, 70))
            self.say("Spell actions are divided up into four different schools that are linked in a cycle representing the natural flow of magic in the world.",
                    'Marisa',
                    'Marisa')
            self.say("It goes: Nature to Elemental to Spiritual to Force, and Force goes back around to Nature, completing the cycle.",
                    'Marisa',
                    'Marisa')
            self.say("If you move with the flow of magic, your attacks will be stronger.",
                    'Ran',
                    'Ran')
            self.say("For instance, Youmu's Dagger Throw spell, a Force type spell, will work more effectively on an enemy equipped with Leaf Crystal, a Nature type spell.",
                    'Ran',
                    'Ran')
            self.emote('Chen', 'lightbulb')
            self.say("Oh, I get it! So that means my Leaf Crystal spell won't be effective against any enemies that are using the Spiritual type Holy Amulet spell, right?",
                    'Chen',
                    'Chen')
            self.say("Right! How about you, Youmu? Did you get all that?",
                    'Ran',
                    'Ran')
            self.say("I believe so. I need to follow the flow of magic and visualize it as a cycle: Nature to Elemental to Spiritual to Force, and then back to Nature again.",
                    'Youmu',
                    'Youmu')
            self.say("By doing so, we can strengthen our spells by exploiting our foes' weaknesses!",
                    'Youmu',
                    'Youmu')
            self.hide_image('tutorial_spell_type')

            # Tutorial Part 2 - Traits
            self.say("Very good, Youmu. Let's move on to Traits then. These come in two flavors: Support and Action. Support traits are more focused on stat improvement while Action traits are more battle focused.",
                    'Ran',
                    'Ran')
            self.show_image('tutorial_flight', 'tutorial_traits_flight.png', (490, 210))
            self.show_image('tutorial_noflight', 'tutorial_traits_noflight.png', (210, 210))
            self.say("Take for instance my Action trait Flight, which allows me to travel easily over any terrain. It's super convenient for travelling over some of the rougher regions of Gensokyo.",
                    'Marisa',
                    'Marisa')
            self.hide_image('tutorial_flight')
            self.hide_image('tutorial_noflight')
            self.say("Take also my Shikigami: Chen gains combat bonuses whenever I'm nearby. I can also use my Magic Fortress trait skill to set up a barrier around myself.",
                'Ran',
                'Ran')
            self.say("We'll learn new traits as we gain more experience, so you should check up on them periodically.",
                'Ran',
                'Ran')
        # Custom mission flag to see if player has chosen a strategy
        self.set_cust_var('player_path_chosen', False)

class DirectPathMAE(MapActionEvent):

    def __init__(self):
        triggers = [# Triggers if any unit from the player team moves into a set of coordinates
                    ArrivalTrigger((8, 6, 11, 15), 1),

                    # Verifies that the player has not already shosen a path
                    CustVarTrigger('player_path_chosen', False)

                    ]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Triggers if player chooses a direct attack up the middle of the forest
        """

        self.set_stats_display(False)
        self.center_on('Kodama Lord')
        self.emote('Kodama Lord', 'exclamation')
        self.say("Aha! Just as I predicted!",
                'Kodama Lord',
                'Kodama')
        self.say("Attack!!!",
                'Kodama Lord',
                'Kodama')
        self.center_on_coords((27, 14))

        # Makes sure the alternate path event is not triggered
        self.set_cust_var('player_path_chosen', True)


        self.set_ai_state('Kodama Lord', 'Pursuit')
        for fairy_suffix in ('A', 'B', 'C', 'D', 'E', 'F'):
            self.set_ai_state('Fairy %s'%fairy_suffix, 'Pursuit')
        self.set_stats_display(True)


class AlternatePathMAE(MapActionEvent):

    def __init__(self):
        triggers = [# Triggers if any unit from the player team moves into a set of coordinates
                    ArrivalTrigger((19, 8, 11, 9), 1),

                    # Verifies that the player has not already shosen a path
                    CustVarTrigger('player_path_chosen', False)
                    ]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Case if player decides to go for a sneak attack
        """
        self.set_stats_display(False)
        self.center_on('Kodama Lord')
        self.emote('Kodama Lord', 'questionmark')
        self.startle('Kodama Lord')
        self.say("What?! No! How did you get over there?!",
                'Kodama Lord',
                'Kodama')
        self.center_on_coords((27, 14))

        # Makes sure the alternate path event is not triggered
        self.set_cust_var('player_path_chosen', True)

        self.set_ai_state('Kodama Lord', 'Pursuit')
        self.set_stats_display(True)

class TreasureAlertMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((18, 20, 7, 4), 1)]

        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Alerts player to presence of treasure under the tree
        """
        self.center_on_coords((27, 23))
        self.say("There seems to be something shiny sitting under the cherry blossom tree.",
                None,
                None)
        self.center_on_coords((18, 22))

class TreasureFoundMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger((27, 23, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Player has discovered treasure under cherry blossom tree
        """

        self.say("Buried at the foot of the cherry tree is a small rusted box.",
                None,
                None)
        self.say("Acquired Treasure Item: Wooden Statue!",
                None,
                None)
        self.add_item('treasure', '000_statue', 1)

class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):
        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.remove_all_enemies()
        self.stop_music()
        self.set_unit_pos('Youmu', (14, 3))
        self.set_unit_pos('Ran', (13, 3))
        self.set_unit_pos('Chen', (16, 4))
        self.set_unit_pos('Marisa', (15, 3))

    def execute(self):
        """
        Victory Scene
        """

        self.center_on('Marisa')
        self.say("Yikes, these kids aren't very loyal for an army, huh? They all flew as soon as the Kodama Lord went down.",
                'Marisa',
                'Marisa')
        self.say("Hey--hey, you guys! What's this? One of those fairies left it behind.",
                'Chen',
                'Chen')

        self.show_image('fire_crystal',
                        'fire_crystal.png',
                        (350, 210))

        self.say("Oh, my! What a find! This is definitely a magical item.",
                'Ran',
                'Ran')
        self.say("Hey, sweet! I bet if we take it to Kourin, he could easily tell us what it is! Well, that is, if the trees haven't trashed his place yet... Hoo boy.",
                'Marisa',
                'Marisa')

        self.hide_image('fire_crystal')
        self.say("I can't wait to find out! And look, the coast is all clear! Lead the way, Marisa!",
                'Chen',
                'Chen')
        self.say("Next stop, my place. All aboard!",
                'Marisa',
                'Marisa')
        self.say("We'll follow your lead then, Marisa.",
                'Youmu',
                'Youmu')
        self.say("Homeward! I swear, if they've so much as touched my place, I'm gonna cut these tree youkai down to size and light 'em up!",
                'Marisa',
                'Marisa')
        self.set_cursor_state(True)
        self.set_stats_display(True)
