from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'Trees Can Walk?'
        location = 'Western Forest'
        id_string = 'CH1ST1'
        prereqs = []
        show_rewards = False
        desc = "In search of Yuyuko and Yukari, Youmu heads towards the Forest of Magic. Earlier today, a horde of tree youkai have uprooted themselves, wreaking chaos upon the forest. Witness the origins of Gensokyo's latest crisis!"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch1st1.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat All',
                     'desc':'Defeat all enemies!'
                     }

        deploy_data = {'enable':False,
                       'max_units':None,
                       'preset_units':None,
                       'boxes':[]
                       }
        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree A',
                                    'level': 3},
                           {'template_name': 'Walking Tree',
                                'unit_name': 'Walking Tree B',
                                    'level': 3},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball A',
                                    'level': 2},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball B',
                                    'level': 2},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball C',
                                    'level': 2},
                          ]

        initial_spells = {'Walking Tree A':['Leaf Crystal'],
                          'Walking Tree B':['Leaf Crystal'],
                          'Fuzzball A':['Dagger Throw'],
                          'Fuzzball B':['Holy Amulet'],
                          'Fuzzball C':['Holy Amulet']}

        initial_traits = {}
        initial_ai_states = {'Walking Tree A':'Attack',
                             'Walking Tree B':'Attack',
                             'Fuzzball A':'Attack',
                             'Fuzzball B':'Attack',
                             'Fuzzball C':'Attack',
                             }
        initial_locations = {'Ran':(0, 14),
                             'Chen':(0, 14),
                             'Youmu':(0, 14),
                             'Walking Tree A':(10, 0),
                             'Walking Tree B':(25, 15),
                             'Fuzzball A':(10, 0),
                             'Fuzzball B':(10, 0),
                             'Fuzzball C':(10, 0), }
        reserve_units = []#[list of unit names to deploy later in mission]
        all_landmarks = [{'name':'Mushroom 1',
                          'id_string':'mushroom',
                          'location':(7, 8)},
                         {'name':'Mushroom 2',
                          'id_string':'mushroom',
                          'location':(18, 8)},
                         {'name':'Mushroom 3',
                          'id_string':'mushroom',
                          'location':(9, 5)},
                         {'name':'Mushroom 4',
                          'id_string':'mushroom',
                          'location':(3, 12)},
                         ]

        required_starters = ['Youmu', 'Chen', 'Ran']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = []
        required_survivors = ['Youmu', 'Ran', 'Chen']
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
        Prologue event
        """
        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.play_music('battle03')

        # move enemy units into position
        self.move_unit('Fuzzball C', (10, 4))
        self.move_unit('Fuzzball C', (12, 4))
        self.move_unit('Fuzzball B', (10, 6))
        self.move_unit('Fuzzball B', (14, 6))
        self.move_unit('Fuzzball A', (10, 4))
        self.move_unit('Walking Tree A', (10, 3))
        self.move_unit('Walking Tree B', (21, 9))

        # Player units move into position
        self.move_unit('Youmu', (6, 10))
        self.move_unit('Ran', (6, 11))
        self.move_unit('Chen', (5, 11))
        self.center_on('Youmu')

        self.say("Wow, trees can walk? I didn't know they could do that!",
                 'Chen',
                 'Chen')
        self.say("They normally can't...unless they become youkai. They've either lived too long or someone's put them under a curse.",
                 'Ran',
                 'Ran')
        self.say("I'm a bit surprised myself. It's been several centuries since I last saw a tree out and about.",
                 'Ran',
                 'Ran')
        self.say("They appear to be chasing those Fuzzballs...",
                 'Youmu',
                 'Youmu')
        self.say("Aaaah!!! They're heading right for us!",
                 'Chen',
                 'Chen')


        # Fuzzballs retreat from walking trees
        self.move_unit('Fuzzball A', (11, 8))
        self.move_unit('Fuzzball A', (7, 9))
        self.move_unit('Fuzzball B', (15, 8))
        self.move_unit('Walking Tree B', (17, 8))
        self.move_unit('Fuzzball B', (11, 8))
        self.move_unit('Fuzzball C', (9, 8))

        self.say("No escape! We're trapped!",
                 'Fuzzball A',
                 'Fuzzball')
        self.say("What?! You think we're your enemies, too?",
                 'Chen',
                 'Chen')
        self.say("They intend to attack. We've no choice but to defend ourselves.",
                 'Youmu',
                 'Youmu')
        self.say("It might be a bit too late to mention this, but would you like to review the basics of combat?",
                 'Ran',
                 'Ran')

        tutorial_enable = self.choice("Do you wish to view the tutorial on battle mechanics?", ['Yes', 'No'])
        if tutorial_enable == 'Yes':
            self.set_cursor_state(True)
            self.say("It would be rash to enter battle without sufficient preparation.",
                     'Youmu',
                     'Youmu')
            self.say("Of course. Now pay attention. The trees here are slow movers, but they're pretty hard hitters, so be careful. The fuzzballs on the other hand are much faster, but they're also much weaker than the trees.",
                     'Ran',
                     'Ran')


            self.say("The two sides in a battle, the player and the enemy, take turns moving their units.",
                     'Tutorial',
                     None)
            self.say("During a player's unit's turn, the unit may move to another location within their movement range and attack an enemy unit.",
                     'Tutorial',
                     None)

            self.move_unit('Ran', (6, 9))
            self.pause(0.5)
            self.show_image('tutorial_attack', 'tutorial_attack.png', (350, 210))

            self.say("Attacking an enemy unit involves selecting the spell action, moving your map cursor over the enemy, and confirming the action.",
                    'Tutorial',
                    None)

            self.hide_image('tutorial_attack')
            self.show_image('tutorial_spell_key', 'tutorial_spell_key.png', (175, 70))

            self.say("There are symbols that will indicate the important properties of an equipped spell action.",
                    'Tutorial',
                    None)
            self.say("Attack types represent the strength of the user of the spell. For instance, Youmu has high STR, thus she is more suited to equip Physical Attack Type spell actions.",
                    'Tutorial',
                    None)
            self.say("Defense types represent the type of defense that the target uses to try and block attack damage. For instance, Ran, with her high MDEF, will take less damage from Magic Defense type spell actions than Youmu.",
                    'Tutorial',
                    None)
            self.say("Ideally, you want to equip a unit with a spell that will inflict heavy damage, then use it against an enemy unit with weak defense against that spell.",
                    'Tutorial',
                    None)
            self.say("Healing actions are also present in this game, and the amount of damage recovered is determined by the skills of the unit performing it.",
                    'Tutorial',
                    None)


            self.hide_image('tutorial_spell_key')


            self.say("Before making a selection, you may also press the 'C' key over any unit to see their attack and movement range.",
                'Tutorial',
                None)
            self.say("The 'A' and 'S' keys cycle through centering on friendly units, while the 'Q' and 'W' keys do the same for enemy units.",
                'Tutorial',
                None)

            self.show_image('tutorial_predictor', 'tutorial_predictor.png', (235, 70))

            self.say("During this stage, a prediction of the battle will be displayed. It includes the probability an action will hit, the damage of that action, as well as the chances of landing a critical hit. A critical hit inflicts 1.5x the damage of a normal attack.",
                'Tutorial',
                None)
            self.say("Using healing spells and items like Fried Tofu will work the same way.",
                'Tutorial',
                None)

            self.hide_image('tutorial_predictor')

            self.say("Here, I'll demonstrate!",
                     'Ran',
                     'Ran')

            self.center_on('Fuzzball A')
            self.startle('Fuzzball A')
            self.pause(0.5)

            self.script_battle('Ran',
                               'Fuzzball A',
                               {'lhs_hit':True,
                                'rhs_hit':True,
                                'lhs_equip':0,
                                'rhs_equip':0,
                                'lhs_crit':False,
                                'rhs_crit':False,
                                }, plot_results=True)

            self.say("Ran successfully attacked and gained Experience Points (EXP) and Spirit Charge (SC).",
                    'Tutorial',
                    None)
            self.say("Experience Points allow a character to level up and become stronger. A character gains a new level every 100 points. More EXP is awarded for fighting more powerful enemies and less for weaker enemies.",
                    'Tutorial',
                    None)
            self.say("Any unit that successfully attacks gains Spirit Charge (SC), which is magical energy that is needed to unlock powerful Spell Cards. Defeating an enemy will grant extra SC. ",
                    'Tutorial',
                    None)
            self.say("On the other hand, missing an attack and other special events can cause SC to drop. Each unit starts with 300 SC.",
                    'Tutorial',
                    None)
            self.say("An SC of 700 or higher puts a unit into High Spirits mode, granting them improved damage and critical hit rates. Likewise, an SC lower than 200 puts a unit into Low Spirits mode, lowering their damage and critical rate.",
                    'Tutorial',
                    None)
            self.say("After a unit completes an attack, the turn ends. Note that the character keeps the current spell action equipped, so be wary of spells that don't have a counterattack, those without a 'C' in the green box.",
                    'Tutorial',
                    None)
            self.say("Spell actions and healing items will eventually be used up and disappear, but special Spell Cards recharge after every battle.",
                    'Tutorial',
                    None)
            self.say("When all units have moved or you've finished your turn, select End Turn from the map menu. If you prefer, you can set the turn to automatically end after all your units have moved.",
                    'Tutorial',
                    None)
            self.say("That's it for this tutorial!",
                    'Tutorial',
                    None)
            self.center_on('Youmu')
            self.say("Our mistresses are somewhere in this forest. We cannot allow them to hinder us!",
                    'Youmu',
                    'Youmu')
        else:
            self.center_on('Youmu')
            self.say("We haven't the time. They're coming.",
                     'Youmu',
                     'Youmu')
            self.say("I understand.",
                     'Ran',
                     'Ran')
        self.show_chapter_title(1)
        self.set_cursor_state(True)
        self.set_stats_display(True)
        self.done = True

class PostMissionMAE(MapActionEvent):
    def __init__(self):
        # Triggers on turn 2
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):
        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.set_unit_pos('Youmu', (11, 7))
        self.set_unit_pos('Ran', (10, 6))
        self.set_unit_pos('Chen', (10, 8))

    def execute(self):
        self.center_on('Youmu')
        self.say("Yay! We did it!",
                'Chen',
                'Chen')
        self.say("That battle was unnecessarily difficult.",
                'Youmu',
                'Youmu')
        self.say("Mm, what we just fought were the younger youkai, too. If we're going to find our mistresses in this forest, we'll have to work doubly hard!",
                'Ran',
                'Ran')
        self.say("Come what may. We shall not surrender before we have secured our mistresses!",
                'Youmu',
                'Youmu')
        self.set_cursor_state(True)
        self.set_stats_display(True)
