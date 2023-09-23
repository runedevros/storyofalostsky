from lostsky.worldmap.event import BattleEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent, ArrivalTrigger, TeamTurnTrigger, UnitAliveTrigger, CustVarTrigger, TurnNumTrigger
from lostsky.core.linalg import Vector2
import pygame
from random import choice

class Mission(BattleEvent):

    def __init__(self):
        # Event Data
        name = 'To Youkai Mountain (Abridged)'
        location = 'Southern Village Path'
        id_string = 'Katsudemo'
        prereqs = ['Do not spawn']
        show_rewards = False
        desc = "Katsucon Test Mission"

        BattleEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'katsudemo.txt'
        mission_type = 'battle'
        objective = {'type':'Defeat All',
                      'desc': 'Defeat all enemies!'}

        deploy_data = {'enable':True,
                       'max_units':4,
                       'preset_units':{},
                       'boxes':[[3, 9, 3, 3]],
                       'default_locations':{'Marisa':(4, 10),
                                            'Youmu':(5, 10),
                                            'Chen':(4, 11),
                                            'Ran':(5, 11),
                                            'Mokou':(5, 9)
                                            },
                       }

        reward_list = []

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
                           {'template_name': 'Firefly',
                                'unit_name': 'Firefly A',
                                    'level': 9},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy A',
                                    'level': 8},
                           {'template_name': 'Fairy',
                                'unit_name': 'Fairy B',
                                    'level': 8},
                          ]

        initial_spells = {'Lord Fuzzy':['Fuzzball Swarm'],
                          'Fuzzball A':['Holy Amulet'],
                          'Fuzzball B':['Holy Amulet'],
                          'Firefly A':['Poison Dust'],
                          'Fairy A':['Dagger Throw'],
                          'Fairy B':['Dagger Throw'],
                          }
        initial_traits = {'Lord Fuzzy':['Regen Lv.1'],
                         }
        initial_ai_states = {'Lord Fuzzy':'Defend',
                             'Fuzzball A':'Attack',
                             'Fuzzball B':'Attack',
                             'Firefly A':'Attack',
                             'Fairy A':'Defend',
                             'Fairy B':'Defend',
                             }
        initial_locations = {'Youmu':(5, 10),
                             'Marisa':(4, 11),
                             'Chen':(4, 10),
                             'Ran':(4, 9),
                             'Mokou':(3, 10),


                             #bottom half of map
                             'Lord Fuzzy':(18, 12),

                             'Fuzzball A':(6, 7),
                             'Fuzzball B':(10, 8),
                             'Firefly A':(10, 4),

                             'Fairy A':(16, 11),
                             'Fairy B':(20, 8),

                             }
        reserve_units = []#[list of unit names to deploy later in mission]
        all_landmarks = []

        required_starters = ['Youmu', 'Chen', 'Ran', 'Marisa', 'Mokou']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = [InitFuzzyAttack(), TagTarget(), FuzzyDrop()]
        required_survivors = ['Youmu', 'Mokou', 'Marisa', 'Ran', 'Chen',]
        post_mission_MAE = PostMissionMAE()

        self.map_data = MapData(map_name, mission_type, objective,
                                deploy_data, reward_list, enemy_unit_data,
                                initial_spells, initial_traits, initial_ai_states,
                                initial_locations, reserve_units, all_landmarks,
                                required_starters, pre_mission_MAE, mid_mission_MAE_list,
                                required_survivors, post_mission_MAE)


class InitFuzzyAttack(MapActionEvent):

    def __init__(self):
        triggers = [TurnNumTrigger(2)]
        MapActionEvent.__init__(self, triggers)

    def execute(self):

        self.center_on('Lord Fuzzy')

        self.say("That's it! You guys are going down!",
            'Lord Fuzzy',
            'Lord Fuzzy')

        self.say("Uh oh! The boss is really ticked off!",
            'Fuzzball',
            'Fuzzball')

        self.say("Does that mean he'll be using THAT attack?",
            'Fuzzball',
            'Fuzzball')

        self.say("I hear he can crush a bunch of walking trees by his size alone!",
            'Fuzzball',
            'Fuzzball')



        self.set_cust_var('Activate', True)


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
        self.play_music('event03')

        self.center_on('Youmu')

        self.say("Just a little further to the mountain...",
                'Youmu',
                'Youmu')
        self.say("Looks like the Fuzzballs have set up a little blockade up ahead. That's pretty bold of them.",
                'Ran',
                'Ran')


        self.startle('Fuzzball A')
        self.say("Boss, more travelers!",
                'Fuzzball',
                'Fuzzball')

        self.center_on('Lord Fuzzy')
        self.startle('Lord Fuzzy')
        self.say("Well, turn them back!",
                'Lord Fuzzy',
                'Lord Fuzzy')


        self.say("Hey, you guys! This is our road! Nobody gets past here!",
                'Fuzzball',
                'Fuzzball')
        self.say("Not humans, not youkai, not even those monster walking trees!",
                'Fuzzball',
                'Fuzzball')

        self.say("Youkai Mountain's our only lead on the location of our masters. We have no choice but to fight our way through!",
                'Youmu',
                'Youmu')

        self.stop_music()

        self.say("I like the sound of that plan!",
                'Marisa',
                'Marisa')


        self.play_music('battle03')


        self.set_cursor_state(True)
        self.set_stats_display(True)


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

        self.center_on(target.name)

        possible_lines = ["Got you right where I want ya!",
                          'Right there! A perfect target!',
                          'Going to pound you to dust!'
                                  ]

        line = choice(possible_lines)


        self.say(line,
            'Lord Fuzzy',
            'Lord Fuzzy')
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

        damage = int(target.maxHP*target_HP_fraction)
        start_HP = target.HP
        target.HP -= damage

        if target.HP < 0:
            target.HP = 0


        self.play_sfx('crit')
        self.render_effect(target, damage)
        target.render_hp_change(start_HP, target.HP)

        if target.HP == 0:
            self.map.kill(target)

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
                    self.map.kill(neighbor)




    def execute(self):
        # Find targetted units

        possible_lines = ['Here I come!',
                          'No escape from the King of Fuzzballs!',
                          'I\'ll crush you to bits!',
                          'Destruction from above!',
                          'Secret technique: Fuzzy Crusher!'
                                  ]

        line = choice(possible_lines)

        if "Stun" not in self.map.all_units_by_name['Lord Fuzzy'].status.keys():

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

                    unit.remove_status('Target')


class PostMissionMAE(MapActionEvent):
    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def pre_exec(self):

        self.set_cursor_state(False)
        self.set_stats_display(False)
        self.remove_all_enemies()
        self.set_unit_pos('Youmu', (21, 11))
        self.set_unit_pos('Ran', (20, 10))
        self.set_unit_pos('Chen', (20, 11))
        self.set_unit_pos('Marisa', (20, 12))
        self.set_unit_pos('Mokou', (19, 11))

    def execute(self):


        # # Shows that not all youkai are aligned with Fuyuhana
        self.center_on('Youmu')
        self.say("No time to waste! Let's go!",
             'Youmu',
             'Youmu')
        self.move_unit('Youmu', (30, 11))
        self.move_unit('Chen', (30, 11))
        self.move_unit('Ran', (20, 11))
        self.move_unit('Ran', (30, 11))
        self.move_unit('Marisa', (20, 11))
        self.move_unit('Marisa', (30, 11))
        self.move_unit('Mokou', (30, 11))
