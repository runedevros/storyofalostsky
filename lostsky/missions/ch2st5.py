from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, ArrivalTrigger, TeamTurnTrigger, UnitAliveTrigger, CustVarTrigger, TurnNumTrigger
from lostsky.core.linalg import Vector2
import pygame
from random import choice

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'To Youkai Mountain'
        location = 'Southern Village Path'
        id_string = 'CH2ST5'
        prereqs = ['CH2ST4']
        show_rewards = False
        desc = "What's this about a secret weapon being prepared by the Fuzzball clans? After being chased out from the forest, the Fuzzballs have gathered at the southern road leading out of the human village. Could they be planning to strike back against Fuyuhana?"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch2st5v2.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat Boss',
                      'target': 'Lord Fuzzy',
                      'desc': 'Defeat Lord Fuzzy!'}

        deploy_data = {'enable':True,
                       'max_units':8,
                       'preset_units':{},
                       'boxes':[(12, 2, 4, 2)],
                       'default_locations':{'Youmu':(15,3),
                                            'Ran':(15,2),
                                            'Chen':(14,2),
                                            'Reimu':(12,3),
                                            'Keine':(14,3),
                                            'Marisa':(12,2),
                                            'Mokou':(13,3),
                                            'Alice':(13,2),
                                            },
                       }

        reward_list = [('treasure', '003_ibistapestry'),
                       ('treasure', 'synth_water'),
                      ]

        # Enemy Unit Data
        enemy_unit_data = [{'template_name': 'Lord Fuzzy',
                                'unit_name': 'Lord Fuzzy',
                                    'level': 12},

                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball A',
                                    'level': 9},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball B',
                                    'level': 9},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball C',
                                    'level': 9},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball D',
                                    'level': 8},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball E',
                                    'level': 8},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball F',
                                    'level': 8},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball G',
                                    'level': 7},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball H',
                                    'level': 7},
                           {'template_name': 'Fuzzball',
                                'unit_name': 'Fuzzball I',
                                    'level': 7},

                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel A',
                                    'level': 8},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel B',
                                    'level': 7},
                           {'template_name': 'Wind Weasel',
                                'unit_name': 'Wind Weasel C',
                                    'level': 7},
                          ]

        initial_spells = {'Lord Fuzzy':['Fuzzball Swarm'],
                          'Fuzzball A':['Stardust'],
                          'Fuzzball B':['Dagger Throw'],
                          'Fuzzball C':['Fireball'],
                          'Fuzzball D':['Stardust'],
                          'Fuzzball E':['Dagger Throw'],
                          'Fuzzball F':['Fireball'],
                          'Fuzzball G':['Stardust'],
                          'Fuzzball H':['Dagger Throw'],
                          'Fuzzball I':['Fireball'],
                          'Wind Weasel A':['Leaf Crystal'],
                          'Wind Weasel B':['Leaf Crystal'],
                          'Wind Weasel C':['Leaf Crystal'],
                          }
        initial_traits = {'Lord Fuzzy':['Regen Lv.1', 'Defense+ Lv.3'],
                         }
        initial_ai_states = {'Lord Fuzzy':'Attack',
                             'Fuzzball A':'Attack',
                             'Fuzzball B':'Attack',
                             'Fuzzball C':'Attack',
                             'Fuzzball D':'Attack',
                             'Fuzzball E':'Attack',
                             'Fuzzball F':'Attack',
                             'Fuzzball G':'Attack',
                             'Fuzzball H':'Attack',
                             'Fuzzball I':'Attack',
                             'Wind Weasel A':'Attack',
                             'Wind Weasel B':'Attack',
                             'Wind Weasel C':'Attack'
                             }
        initial_locations = {'Youmu':(15, 4),
                             'Reimu':(14, 3),
                             'Marisa':(14, 2),
                             'Chen':(15, 3),
                             'Ran':(15, 2),
                             'Keine':(16, 3),
                             'Mokou':(16, 2),

                             #top half of map

                             'Fuzzball G':(7, 6),
                             'Fuzzball H':(8, 5),
                             'Fuzzball I':(6, 7),

                             'Wind Weasel A':(3, 12),
                             'Wind Weasel B':(2, 11),
                             'Wind Weasel C':(4, 11),

                             #bottom half of map
                             'Fuzzball D':(20, 8),
                             'Lord Fuzzy':(18, 17),
                             'Fuzzball E':(21, 7),
                             'Fuzzball F':(19, 9),

                             'Fuzzball A':(17, 16),
                             'Fuzzball B':(16, 17),
                             'Fuzzball C':(18, 15),
                             }
        reserve_units = []#[list of unit names to deploy later in mission]
        all_landmarks = [{'name':'Mini Shrine',
                          'id_string':'minishrine',
                          'location':(3, 10)},
                         {'name':'CB 1',
                          'id_string':'cherryblossom_tree',
                          'location':(2, 10)},
                         {'name':'CB 2',
                          'id_string':'cherryblossom_tree',
                          'location':(4, 10)},
                         ]

        required_starters = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Reimu', 'Mokou', 'Keine']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [TreasureMAE(), InitFuzzyAttack(), TagTarget(), FuzzyDrop()]
        required_survivors = ['Lord Fuzzy', 'Youmu', 'Reimu', 'Marisa', 'Ran',
                              'Chen', 'Mokou', 'Keine']
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
        self.center_on('Lord Fuzzy')

        # Fuzzballs demonstrating their stun spell
        self.say("Hey, boss! Like. I got something to show you!",
                'Fuzzball A',
                'Fuzzball')
        self.emote('Fuzzball B', 'dotdotdot')
        self.say("Hmph! Fine. What is it?",
                'Lord Fuzzy',
                'Lord Fuzzy')
        self.say("The Master of the Forest's armies are, like, trees, right? If that's the case then like...this will be our secret weapon!",
                'Fuzzball A',
                'Fuzzball')
        self.say("So like. Hey, buddy, could you like stand over here for a moment?",
                'Fuzzball A',
                'Fuzzball')
        self.move_unit('Fuzzball B', (16, 16))
        self.emote('Fuzzball B', 'dotdotdot')

        self.say("Great, thanks! Here we go. Dazzling Light! Stardust!",
                'Fuzzball A',
                'Fuzzball')

        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)
        self.emote('Fuzzball B', 'scribble')
        self.say("Hey! Hey!!! Watch where you're firing that! H-huh?! Nooooo! I can't see! I can't move!",
                'Fuzzball B',
                'Fuzzball')

        self.emote('Fuzzball B', 'dotdotdot')
        self.say("Oh... I can move again.",
                'Fuzzball B',
                'Fuzzball')

        self.move_unit('Fuzzball B', (16, 17))
        self.startle('Fuzzball A')
        self.say("So like last night, I put together some element crystals to make these babies. This'll like totally stop those walking trees long enough that we can ambush them!",
                'Fuzzball A',
                'Fuzzball')
        self.say("Ohohohoho! Splendid! Yes, very well done.",
                'Lord Fuzzy',
                'Lord Fuzzy')


        self.center_on('Fuzzball G')
        self.play_music('battle02')
        self.say("Yo, boss, heads up! Humans coming our way!",
                'Fuzzball G',
                'Fuzzball')
        self.say("Oho? Battle formations, everyone! We can't lose twice in one day! Our pride won't take it!",
                'Lord Fuzzy',
                'Lord Fuzzy')

        # Player gets info on how best to deal with it
        self.center_on('Marisa')
        self.say("Oh, whoa, what?! Heeey! Those fuzzballs stole my trademark flashy spells!",
                'Marisa',
                'Marisa')
        self.say("Did you notice how that one fuzzball was stunned momentarily? They may not be bright, but that weapon still looks dangerous. Let's proceed carefully.",
                'Ran',
                'Ran')
        self.say("Although that is true, their weapon doesn't appear to have much range. As such, I believe attacking from a distance would be the best strategy.",
                'Keine',
                'Keine')
        self.say("Those numerous fuzzballs may be blocking our way, but defeating their leader should be enough to grant us passage. Let us fight accordingly.",
                'Youmu',
                'Youmu')

        self.set_cursor_state(True)
        self.set_stats_display(True)

class TreasureMAE(MapActionEvent):

    def __init__(self):
        triggers = [ArrivalTrigger( (3, 10, 1, 1), 1)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        self.say("A lone shrine is here that was guarded by youkai weasels.",
                None,
                None)
        self.say("They were protecting an odd treasure box. Inside was a rusted lamp.",
                None,
                None)
        self.say("Acquired Treasure Item: Magic Lamp!",
                None,
                None)
        self.add_item('treasure', '004_magiclamp', 1)

class InitFuzzyAttack(MapActionEvent):

    def __init__(self):
        triggers = [TurnNumTrigger(2)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):

        self.center_on('Lord Fuzzy')

        self.say("Ohhhh, that is it! You humans are going down! Way down! Face to the floor down!",
            'Lord Fuzzy',
            'Lord Fuzzy')

        self.say("Uh oh! The boss looks totally ticked off!",
            'Fuzzball',
            'Fuzzball')

        self.say("Does that mean he'll be using...that attack?",
            'Fuzzball',
            'Fuzzball')

        self.say("Oh, no... I hear he can crush a ton of walking trees by his sheer size alone! No one is safe!!!",
            'Fuzzball',
            'Fuzzball')


        self.set_cust_var('Activate', True)


class TagTarget(MapActionEvent):

    def __init__(self):
        triggers = [TeamTurnTrigger(1), CustVarTrigger('Activate', True), UnitAliveTrigger('Lord Fuzzy', True)]
        MapActionEvent.__init__(self, triggers, repeat = True)



    def render_grid(self, target):

        target_location = target.location_tile
        nearest_neighbors = [target.location_tile+Vector2(0, 1),
                             target.location_tile+Vector2(0, -1),
                             target.location_tile+Vector2(1, 0),
                             target.location_tile+Vector2(-1, 0)]
        next_nearest_neighbors = [target.location_tile+Vector2(0, 2),
                                  target.location_tile+Vector2(2, 0),
                                  target.location_tile+Vector2(-2, 0),
                                  target.location_tile+Vector2(0, -2),
                                  target.location_tile+Vector2(1, 1),
                                  target.location_tile+Vector2(-1, 1),
                                  target.location_tile+Vector2(1, -1),
                                  target.location_tile+Vector2(-1, -1),

                                  ]

        # Draw a target zone moving outward from target.
        self.add_highlight(target_location)
        self.render_update()
        self.pause(0.1)
        for location in nearest_neighbors:
            self.add_highlight(location)
        self.render_update()
        self.pause(0.1)
        for location in next_nearest_neighbors:
            self.add_highlight(location)

        self.render_update()
        self.pause(1)

        # Remove all highlights
        self.remove_highlight(target_location)
        all_neighbor_locations = next_nearest_neighbors+nearest_neighbors
        for location in all_neighbor_locations:
            self.remove_highlight(location)


    def render_update(self):

        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.render_menu_panel()

        # Draws emoticon frame
        pygame.display.flip()

    def execute(self):
        """



        """

        # Determine the unit with highest density of neighbors

        prioritized_units = []

        for unit in self.map.team1:

            score = 0

            for neighbor in self.map.team1:

                neighbor_distance = abs(unit.location_tile.x - neighbor.location_tile.x) + abs(unit.location_tile.y - neighbor.location_tile.y)

                if neighbor_distance == 0:
                    pass
                elif neighbor_distance == 1:
                    score += 2
                elif neighbor_distance == 2:
                    score += 1

            prioritized_units.append([score, unit.name, unit])

        prioritized_units.sort()
        prioritized_units.reverse()

        target = prioritized_units[0][2]

        possible_lines = ["Got you right where I want ya!",
                          'Right there! A perfect target!',
                          'Going to pound you to dust!'
                                  ]

        line = choice(possible_lines)


        self.say(line,
            'Lord Fuzzy',
            'Lord Fuzzy')
        self.center_on(target.name)
        self.set_status_effect(target.name, "Target")
        self.render_grid(target)

        pass

class FuzzyDrop(MapActionEvent):

    def __init__(self):
        triggers = [TeamTurnTrigger(2), UnitAliveTrigger('Lord Fuzzy', True), CustVarTrigger('Activate', True)]
        MapActionEvent.__init__(self, triggers, repeat = True)
        self.user = 'Lord Fuzzy'


    def animate_action(self, target):


        # Sprite groups for fuzzy animation
        self.fuzzy_sprite = pygame.sprite.Sprite()
        self.fuzzy_sprite.image = self.map.engine.giant_fuzzy
        self.fuzzy_sprite.rect = self.fuzzy_sprite.image.get_rect()

        self.big_fuzzy_group = pygame.sprite.RenderUpdates()
        self.big_fuzzy_group.add(self.fuzzy_sprite)

        # Records LF's current position
        old_position = self.map.all_units_by_name[self.user].location_tile.copy()

        # Shows LF jumping into the air
        self.center_on(self.user)
        self.move_unit(self.user, (old_position.x, old_position.y-15))

        # Hide LF in the corner of the map.
        self.set_unit_pos(self.user, (-1,-1))
        self.center_on(target.name)
        self.emote(target.name, 'exclamation')


        # Animates LF's descent as the huge fuzzy
        bg_surf = self.map.engine.surface.copy()

        destination_height = 35*(target.location_tile.y-self.map.screen_shift.y)+17

        x_position = 35*(target.location_tile.x-self.map.screen_shift.x)+17
        y_position = -1*self.fuzzy_sprite.image.get_height()


        self.play_sfx('falling')
        while self.fuzzy_sprite.rect.center[1] < destination_height and self.fuzzy_sprite.rect.bottom < 490:

            y_position += 10

            self.fuzzy_sprite.rect.center = (x_position, y_position)

            self.big_fuzzy_group.clear(self.map.engine.surface, bg_surf)
            self.big_fuzzy_group.update()
            rects = self.big_fuzzy_group.draw(self.map.engine.surface)

            pygame.display.update(rects)
            self.map.engine.clock.tick(60)

        # LF impact, fade out and restore LF to original position
        self.play_sfx('explode')
        self.pause(0.2)
        self.fade_to_color('white', 0.5)
        self.set_unit_pos(self.user, old_position)
        self.fade_from_color('white', 0.5)


    def render_effect(self, target, damage_value):


        text_name = self.map.engine.bfont.render("Fuzzy Drop!", True, (0, 0, 0))
        half_width = text_name.get_width()/2


        effect_text = self.map.engine.render_outlined_text(str(damage_value), self.map.engine.cfont, (255, 0, 0), (255, 255, 255))

        self.map.render_background()
        self.map.render_all_units()
        self.map.render_cursor()
        self.map.engine.surface.blit(self.map.engine.menu_board, (0, 490))
        self.map.engine.surface.blit(self.map.engine.map_spell_board, (175, 0))
        self.map.engine.surface.blit(text_name, (420-half_width, 25))
        target.plot_stats()
        self.map.engine.surface.blit(effect_text, ((target.location_pixel.x+18-effect_text.get_width()/2, target.location_pixel.y-25)-self.map.screen_shift*self.map.engine.tilesize))

        pygame.display.flip()
        self.map.engine.clock.tick(60)
        self.map.engine.pause(1)

    def execute_damage(self, target):

        # Damage values
        target_HP_fraction = 0.25
        nearest_neighbor_HP_fraction = 0.20
        nnn_HP_fraction = 0.15

        damage = int(target.HP*target_HP_fraction)
        start_HP = target.HP
        target.HP -= damage

        if target.HP < 0:
            target.HP = 0


        self.play_sfx('crit')
        self.render_effect(target, damage)
        target.render_hp_change(start_HP, target.HP)

        if target.HP == 0:
            target.alive = False



            if not target.ressurected and (target.has_trait_property('Revive Lv.1') or target.has_trait_property('Revive Lv.2') or target.has_trait_property('Revive Lv.3')):
                self.map.check_map_event_revive(target)
            else:
                self.map.kill(target, render_fadeout=True)


        for neighbor in self.map.all_units_by_name.values():
            # Drop affects all units except for lord fuzzy
            if neighbor.name != self.user:
                # find distance

                neighbor_distance = abs(target.location_tile.x - neighbor.location_tile.x) + abs(target.location_tile.y - neighbor.location_tile.y)

                # Damage to nearest neighbors
                if neighbor_distance == 1:

                    damage = int(neighbor.HP*nearest_neighbor_HP_fraction)

                # Damage to NNN
                elif neighbor_distance == 2:

                    damage = int(neighbor.HP*nnn_HP_fraction)

                # Target out of range, skip
                else:
                    continue

                start_HP = neighbor.HP
                neighbor.HP -= damage

                if neighbor.HP < 0:
                    neighbor.HP = 0

                self.play_sfx('hit')
                self.render_effect(neighbor, damage)
                neighbor.render_hp_change(start_HP, neighbor.HP)

                if neighbor.HP == 0:

                    target.alive = False

                    if not neighbor.ressurected and (neighbor.has_trait_property('Revive Lv.1') or neighbor.has_trait_property('Revive Lv.2') or neighbor.has_trait_property('Revive Lv.3')):
                        self.map.check_map_event_revive(neighbor)
                    else:
                        self.map.kill(neighbor, render_fadeout=True)




    def execute(self):
        # Find targetted units

        possible_lines = ['Here I come!',
                          'No escape from the King of Fuzzballs!',
                          'I\'ll crush you to bits!',
                          'Destruction from above!',
                          'Secret technique: Fuzzy Crusher!'
                                  ]

        if "Stun" not in self.map.all_units_by_name['Lord Fuzzy'].status.keys():

            line = choice(possible_lines)

            for unit in self.map.team1:
                if "Target" in unit.status.keys():

                    self.say(line,
                         'Lord Fuzzy',
                'Lord Fuzzy')

            for unit in self.map.team1:
                if "Target" in unit.status.keys():

                    # animate action
                    self.animate_action(unit)

                    # execute damage
                    self.execute_damage(unit)

        for unit in self.map.team1:
            if "Target" in unit.status.keys():
                unit.remove_status('Target')


class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.remove_all_enemies()
        self.stop_music()
        self.set_unit_pos('Youmu', (16, 15))
        self.set_unit_pos('Ran', (15, 14))
        self.set_unit_pos('Chen', (15, 13))
        self.set_unit_pos('Marisa', (16, 14))
        self.set_unit_pos('Reimu', (16, 13))
        self.set_unit_pos('Mokou', (17, 14))
        self.set_unit_pos('Keine', (17, 13))
        self.set_unit_pos('Lord Fuzzy', (16, 17))

    def execute(self):

        # Shows that not all youkai are aligned with Fuyuhana
        self.center_on('Youmu')
        self.say("Noooo...it happened...defeated twice in one day...",
                'Lord Fuzzy',
                'Lord Fuzzy')
        self.say("Twice, huh? Tch. So someone got to you pom-poms before us?",
                'Marisa',
                'Marisa')
        self.say("That's right...the Master of the Forest is already pushing well beyond the Forest of Magic. She's gathered the clouds all around the forest to nourish her trees with plenty of rain.",
                'Lord Fuzzy',
                'Lord Fuzzy')
        self.say("No. We were too slow. Tell me. Where are they headed to next?",
                'Youmu',
                'Youmu')
        self.say("The Master of the Forest's underlings are moving in this direction, but I hear from some of our northern cousins that they are advancing a super large group toward the bamboo forest. Oho....ho.",
                'Lord Fuzzy',
                'Lord Fuzzy')
        self.say("Fuyuhana's ambitious. They're covering a lot of ground, and fast. So let's go.",
                'Mokou',
                'Mokou')
