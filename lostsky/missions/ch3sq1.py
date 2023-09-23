from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, UnitHPBelowTrigger, UnitAliveTrigger, TeamTurnTrigger
from lostsky.battle.mapobj import SpiritSourcePoint

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'Treasure Hunter Sakuya'
        location = 'Genbu Ravine'
        id_string = 'CH3SQ1'
        prereqs = ['CH3ST6']
        show_rewards = True
        desc = "The Genbu Ravine is downstream from Youkai Mountain at the edge of the Forest of Magic. A few Kodama from Haruna's group also showed up looking for something important and so did the maid of the Scarlet Devil Mansion, Sakuya Izayoi."

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch3sq1.txt'
        mission_type = 'battle'
        objective = {'type': 'Defeat All',
                     'desc': 'Defeat all enemies!'
                     }

        deploy_data = {'enable': True,
                       'max_units': 18,
                       'preset_units': {'Sakuya':(12,24)},
                       'default_locations': {
        'Youmu': (23, 25),
        'Ran': (24, 24),
        'Reimu': (24, 25),
        'Keine': (24, 26),
        'Marisa': (25, 24),
        'Chen': (25, 25),
        'Mokou': (25, 26),
        'Aya': (26, 25),
                                             },
                       'boxes': [(23, 23, 4, 4)]
                       }

        reward_list = [('spell_action', 'Rice Cake')
                       ]

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Kodama Lord',
                            'unit_name': 'Kodama Lord A',
                            'level': 15},
                           {'template_name': 'Kodama Lord',
                            'unit_name': 'Kodama Lord B',
                            'level': 15},

                           {'template_name': 'Walking Tree',
                            'unit_name': 'Walking Tree A',
                            'level': 12},
                           {'template_name': 'Walking Tree',
                            'unit_name': 'Walking Tree B',
                            'level': 12},
                           {'template_name': 'Walking Tree',
                            'unit_name': 'Walking Tree C',
                            'level': 12},
                           {'template_name': 'Walking Tree',
                            'unit_name': 'Walking Tree D',
                            'level': 12},
                           {'template_name': 'Walking Tree',
                            'unit_name': 'Walking Tree E',
                            'level': 12},
                           {'template_name': 'Walking Tree',
                            'unit_name': 'Walking Tree F',
                            'level': 12},

                           {'template_name': 'Fairy',
                            'unit_name': 'Fairy A',
                            'level': 13},
                           {'template_name': 'Fairy',
                            'unit_name': 'Fairy B',
                            'level': 13},
                           {'template_name': 'Fairy',
                            'unit_name': 'Fairy C',
                            'level': 13},
                           {'template_name': 'Fairy',
                            'unit_name': 'Fairy D',
                            'level': 13},
                           {'template_name': 'Fairy',
                            'unit_name': 'Fairy E',
                            'level': 13},

                           {'template_name': 'Healer Fairy',
                            'unit_name': 'Healer Fairy A',
                            'level': 14},

                           {'template_name': 'Healer Fairy',
                            'unit_name': 'Healer Fairy B',
                            'level': 14},
                           {'template_name': 'Wind Weasel',
                            'unit_name': 'Wind Weasel A',
                            'level': 12
                            },
                           {'template_name': 'Wind Weasel',
                            'unit_name': 'Wind Weasel B',
                            'level': 12
                            },
                           {'template_name': 'Wind Weasel',
                            'unit_name': 'Wind Weasel C',
                            'level': 12
                            },
                           {'template_name': 'Wind Weasel',
                            'unit_name': 'Wind Weasel D',
                            'level': 12
                            },
                           {'template_name': 'Wind Weasel',
                            'unit_name': 'Wind Weasel E',
                            'level': 12
                            },
                           {'template_name': 'Wind Weasel',
                            'unit_name': 'Wind Weasel F',
                            'level': 12
                            },

                           ]

        initial_spells = {  'Kodama Lord A':['Leaf Crystal'],
                            'Kodama Lord B':['Leaf Crystal'],
                            'Fairy A': ['Dagger Throw'],
                            'Fairy B': ['Holy Amulet'],
                            'Fairy C': ['Fireball'],
                            'Fairy D': ['Fireball'],
                            'Fairy E': ['Dagger Throw'],
                            'Walking Tree A': ['Leaf Crystal'],
                            'Walking Tree B': ['Leaf Crystal'],
                            'Walking Tree C': ['Leaf Crystal'],
                            'Walking Tree D': ['Leaf Crystal'],
                            'Walking Tree E': ['Leaf Crystal'],
                            'Walking Tree F': ['Leaf Crystal'],

                            'Wind Weasel A':['Dagger Throw'],
                            'Wind Weasel B':['Dagger Throw'],
                            'Wind Weasel C':['Dagger Throw'],
                            'Wind Weasel D':['Dagger Throw'],
                            'Wind Weasel E':['Dagger Throw'],
                            'Wind Weasel F':['Dagger Throw'],

                            'Healer Fairy A':['Healing Drop'],
                            'Healer Fairy B':['Healing Drop'],

                          }
        initial_traits = {'Fairy A': []}
        initial_ai_states = { 'Kodama Lord A': 'Attack',
                              'Kodama Lord B': 'Attack',

                              'Fairy A':'Attack',
                              'Fairy B':'Attack',
                              'Fairy C':'Attack',
                              'Fairy D':'Attack',
                              'Fairy E':'Attack',
                              'Walking Tree A':'Attack',
                              'Walking Tree B':'Attack',
                              'Walking Tree C':'Attack',
                              'Walking Tree D':'Attack',
                              'Walking Tree E':'Attack',
                              'Walking Tree F':'Attack',
                              'Wind Weasel A':'Pursuit',
                              'Wind Weasel B':'Pursuit',
                              'Wind Weasel C':'Pursuit',
                              'Wind Weasel D':'Pursuit',
                              'Wind Weasel E':'Pursuit',
                              'Wind Weasel F':'Pursuit',


                             'Healer Fairy A': 'HealerStandby',
                             'Healer Fairy B': 'HealerStandby',

                             }
        initial_locations = {   'Kodama Lord A':(6, 18),
                                'Kodama Lord B': (21, 10),

                                'Walking Tree A': (18, 11),
                                'Walking Tree B': (24, 11),
                                'Walking Tree C': (10, 25),
                                'Walking Tree D': (14, 21),
                                'Walking Tree E': (9, 10),
                                'Walking Tree F': (14, 10),

                                'Fairy A': (19, 13),
                                'Fairy B': (23, 13),
                                'Fairy C': (9, 13),
                                'Fairy D': (14, 13),
                                'Fairy E': (5, 20),

                                'Healer Fairy A': (12, 10),
                                'Healer Fairy B': (12, 23),

                                'Wind Weasel A':(17, 25),
                                'Wind Weasel B':(7, 21),
                                'Wind Weasel C':(8, 11),
                                'Wind Weasel D':(9, 11),
                                'Wind Weasel E':(14, 11),
                                'Wind Weasel F':(15, 11),

                             }
        reserve_units = []  # [list of unit names to deploy later in mission]
        all_landmarks = []

        required_starters = ['Youmu', 'Aya', 'Marisa', 'Chen', 'Keine', 'Reimu', 'Sakuya', 'Ran', 'Mokou']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [RecoveryMAE()]
        required_survivors = ['Youmu', 'Aya', 'Marisa', 'Chen', 'Keine', 'Reimu', 'Sakuya', 'Ran', 'Mokou']
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

        self.play_music('battle02')

        self.set_unit_pos('Youmu', (31, 25))
        self.set_unit_pos('Ran', (31, 25))
        self.set_unit_pos('Chen', (31, 25))
        self.set_unit_pos('Reimu', (31, 25))
        self.set_unit_pos('Marisa', (31, 25))
        self.set_unit_pos('Keine', (31, 25))
        self.set_unit_pos('Mokou', (31, 25))
        self.set_unit_pos('Aya', (31, 25))

        self.add_temporary_ally('Sakuya')

        self.assign_spell('Sakuya', 'Dagger Throw')
        self.assign_spell('Sakuya', 'Killing Doll')

        self.assign_trait('Sakuya', 'Critical+ Lv.2')
        self.assign_trait('Sakuya', 'Teleport')
        self.assign_trait('Sakuya', 'Double Action')

        self.set_unit_pos('Sakuya', (9, 20))
        self.center_on('Sakuya')

        self.say("We found this maid lurking in this ravine while doing our search for the artifact that Kodama Lord Haruna wanted.",
                 'Wind Weasel', 'Wind Weasel')

        self.center_on('Kodama Lord A')

        self.say("You're the vampire's maid, Sakuya Izayoi, aren't you? This is a long way from your mansion.",
                 'Kodama Lord A', 'Kodama')

        self.say("If you're here that must mean that she's planning on interfering with our plans.",
                 'Kodama Lord A', 'Kodama')

        self.say("Pardon me? Like I was explaining to your fairies, I don't know anything about this magic mirror of yours.",
                 'Sakuya', 'Sakuya')

        self.say("(Ah.... I got the treasure scroll for Miss Remilia, but I have to hurry and get out of here.)",
                 'Sakuya', 'Sakuya')

        self.center_on('Walking Tree C')
        self.move_unit('Sakuya', (9, 25))


        self.center_on('Sakuya')

        self.say("She's got something in her hand! Don't let her get away!",
                 'Kodama Lord B', 'Kodama')

        # Battle Scene
        self.script_battle("Sakuya", "Walking Tree C",
                           {'lhs_equip':0,
                            'rhs_equip':0,
                            'lhs_hit':True,
                            'rhs_hit':False,
                            'lhs_crit':True,
                            'rhs_crit':False}
                           )

        self.move_unit('Sakuya', (9, 24))
        self.move_unit('Sakuya', (12, 24))

        self.center_on_coords((23,23))

        self.move_unit('Youmu', (23, 25))
        self.move_unit('Ran', (24, 24))
        self.move_unit('Reimu', (24, 25))
        self.move_unit('Keine', (24, 26))
        self.move_unit('Marisa', (25, 24))
        self.move_unit('Chen', (25, 25))
        self.move_unit('Mokou', (25, 26))
        self.move_unit('Aya', (26, 25))

        self.center_on('Youmu')

        self.say("Thank goodness we made it in time!",
                 'Youmu', 'Youmu')

        self.say("Miss Sakuya, let us lend a hand.",
                 'Youmu', 'Youmu')

        self.say("We can't stay long. The Genbu Ravine is at the edge of the Forest of Magic. I expect they'll call for help soon.",
                'Ran', 'Ran')

        self.center_on('Sakuya')
        self.emote('Sakuya', 'musicnote')
        self.say("Miss Konpaku, I had no idea you were here too!",
                 'Sakuya', 'Sakuya')

        # Walking Tree recovers
        self.center_on('Walking Tree C')
        wt_initial_HP = self.map.all_units_by_name['Walking Tree C'].HP
        wt_max_HP = self.map.all_units_by_name['Walking Tree C'].maxHP

        self.say("Hey! Look at that tree that Sakuya just attacked.",
                 'Mokou', 'Mokou')

        self.pause(0.5)
        self.map.all_units_by_name['Walking Tree C'].render_hp_change(wt_initial_HP, wt_max_HP)
        self.emote('Walking Tree C', 'musicnote')
        self.pause(0.5)
        self.set_hp('Walking Tree C', wt_max_HP)


        self.center_on('Youmu')
        self.emote("Chen", "exclamation")

        self.say("Wow! How can they recover so fast?",
                 'Chen', 'Chen')

        self.center_on('Kodama Lord B')
        self.say("Our walking trees are fortified with our magic fertilizer. So long as we stand, our trees will instantly heal.",
                 'Kodama Lord B', 'Kodama')

        self.center_on('Marisa')
        self.say("Magicians aren't supposed to reveal their secrets, you know. You two just marked yourselves with huge bullseyes. Let's go get 'em.",
                'Marisa', 'Marisa')

        self.say("Thank you, Miss Konpaku! I'll be sure to reward you after this battle ends.",
                 'Sakuya', 'Sakuya')

        self.center_on('Sakuya')

        self.set_cursor_state(True)
        self.set_stats_display(True)


class RecoveryMAE(MapActionEvent):

    def __init__(self):
        triggers = [TeamTurnTrigger(2)]
        MapActionEvent.__init__(self, triggers, repeat=True)

    def execute(self):

        kodama_alive = 0
        if self.map.all_units_total['Kodama Lord A'].alive:
            kodama_alive += 1
        if self.map.all_units_total['Kodama Lord B'].alive:
            kodama_alive += 1

        unit_names = ['Walking Tree A', 'Walking Tree B', 'Walking Tree C', 'Walking Tree D',
                      'Walking Tree E', 'Walking Tree F']

        if kodama_alive:

            for unit in [self.map.all_units_by_name[unit_name] for unit_name in unit_names
                         if unit_name in self.map.all_units_by_name.keys()]:
                if unit.alive and unit.HP < unit.maxHP:

                    delta_HP = unit.maxHP - unit.HP

                    if kodama_alive == 1:
                        change = 0.33
                    elif kodama_alive == 2:
                        change = 0.66
                    else:
                        change = 0

                    hp_recover = min(delta_HP, int(change*unit.maxHP))

                    unit.render_hp_change(unit.HP, unit.HP+hp_recover)
                    unit.HP += hp_recover



class PostMissionMAE(MapActionEvent):
    def __init__(self):
        # Triggers on turn 2


        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.remove_all_enemies()

        self.set_unit_pos('Sakuya', (12,24))
        self.set_unit_pos('Youmu', (12,25))
        self.set_unit_pos('Ran', (12,26))
        self.set_unit_pos('Chen', (12,27))
        self.set_unit_pos('Reimu', (11,26))
        self.set_unit_pos('Marisa', (11,27))
        self.set_unit_pos('Keine', (13,26))
        self.set_unit_pos('Mokou', (13,27))
        self.set_unit_pos('Aya', (10,26))


    def execute(self):

        self.center_on('Sakuya')
        self.set_stats_display(False)
        self.set_cursor_state(False)
        self.play_music('event01')

        self.say("I owe you a debt of gratitude.",
                 'Sakuya', 'Sakuya')
        self.say("This is the first we heard from Remilia since this crisis started.",
                 'Reimu', 'Reimu')
        self.say( "Is she up to no good again?",
            'Reimu', 'Reimu')

        self.say("I assure you that my Mistress has no intention of getting involved in the affairs of the Kodama. I'm actually on a mission for Miss Patchouli Knowledge today.",
                 'Sakuya', 'Sakuya')

        self.say("This scroll. See?",
                 'Sakuya', 'Sakuya')

        self.say("What does Miss Patchouli want with that scroll?",
                 'Youmu', 'Youmu')

        self.say("She wouldn't say, and as a maid, I don't ask too many details. Besides, I lack the ability to read it.",
            'Sakuya', 'Sakuya')

        self.move_unit('Aya', (11, 24))
        self.say("Ah! That's written in an old Tengu script. Can I have a look?",
                 'Aya', 'Aya')

        self.emote('Aya', 'dotdotdot')
        self.emote('Aya', 'lightbulb')

        self.say("I translated what I could on it. Patchouli will have to fill in the blanks. It describes an archaic form of alchemy to change other elements to water.",
                 'Aya', 'Aya')

        self.say("Well that's one way of outlasting our current drought crisis. I doubt we could use it for all of Gensokyo because of how rare some of these ingredients you need for the magic.",
                 'Ran', 'Ran')

        self.say("It would probably be enough to meet the water needs of Scarlet Devil Mansion though. Unfortunately for them, the water from the lake isn't suitable for drinking.",
            'Keine', 'Keine')

        self.say("Still, it says here it needs something called a Water God's Stone. It's not an ingredient I've ever used in my magic recipes.",
                 'Marisa', 'Marisa')

        self.say("I would bet that Miss Patchouli would be able to figure out how to make it or knows where to find it.",
                 'Youmu', 'Youmu')

        self.say("As promised, your reward Miss Youmu. It's a set of recipes Miss Patchouli has been experimenting with!",
            'Sakuya', 'Sakuya')

        self.say("Received the recipes to create Barrier Buster and Weakening Amulet!", None, None)

        self.add_recipe('Barrier Buster')
        self.add_recipe('Weakening Amulet')

        self.say("Thank you Miss Sakuya. This'll help us a lot on your journey. Safe travels!",
                 'Youmu', 'Youmu')
