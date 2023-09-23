import pygame
from random import random
from lostsky.core.linalg import Vector2
from math import fabs

class UnitAI(object):

    """
    # Class Name: UnitAI
    # Purpose: A Finite State Machine implementation of unit AI
    """

    def __init__(self, unit, starting_state):

        """
        # Function Name: __init__
        # Purpose: Constructs the Unit AI class
        # Input:   Unit - Unit to assign AI to
        #          Starting_state - State that the unit's AI starts with
        """
        self.all_states = {'Attack': Attack(unit),
                           'AttackRetreat': AttackRetreat(unit),
                           'HealerStandby': HealerStandby(unit),
                           'HealerSOS': HealerSOS(unit),
                           'Pursuit': Pursuit(unit),
                           'PursuitRetreat': PursuitRetreat(unit),
                           'Defend': Defend(unit),
                           'DefendRetreat': DefendRetreat(unit),
                           'Support': Support(unit)}

        self.current_state = self.all_states[starting_state]

        # SOS list for healers
        self.sos_list = []

        # Self
        self.target_notifications = []

        # Spell lock - Locks a unit in to their currently assigned spell
        self.spell_lock = False


    def update_state(self):
        """
        # Function Name: __init__
        # Purpose: Checks if a unit needs a change in state and updates as necessary
        """
        # Flush the target notifications inbox
        self.target_notifications = []

        new_state = self.current_state.check_conditions()
        if new_state:

            self.current_state = self.all_states[new_state]

    def execute_turn(self):
        """
        # Function Name: execute turn
        # Purpose: Updates a unit's state and carries out the unit's turn
        """

        self.current_state.think()

        return self.current_state.act()

class AIState(object):

    def __init__(self, unit):
        """
        # Function Name: __init__
        # Purpose: Constructs the Generic AI State class
        # Input:   Unit - Unit to assign AI State to
        """
        self.unit = unit

        # This refers to a unit that is being marked as this AI's target
        self.target_unit = None

        # Alternately, a unit can be assigned to go to a destination, or decide not to pursue a unit
        # for instance to go after a spirit source point.
        self.assigned_destination = None

        # Pathfinder's data
        self.open_by_coord = {}
        self.open_list = []
        self.closed_by_coord = {}
        self.current_path = []

    def think(self):
        """
        # Function Name: think
        # Purpose: Processes that select target before actions are taken
        """
        pass

    def act(self):
        """
        # Function Name: act
        # Purpose: Acts out the unit's turn
        """
        pass

    def check_conditions(self):
        """
        # Function Name: check_conditions
        # Purpose: Placeholder
        """
        pass

    ########################
    # Misc Common Functions
    ########################

    def check_spell_actions(self):
        """
        # Spell Action switching:
        # Purpose: If unit is out of spells go down or cannot use the equipped spell due to SC restrictions,
        # go down the list until you find the first equippable spell
        """

        print "Using Main AI spell scanning algorithm"
        if not self.unit.spell_actions[self.unit.equipped] or self.unit.spell_actions[self.unit.equipped].unlock > self.unit.spirit:

            for index, spell_action in enumerate(self.unit.spell_actions):

                # checks whether spell exists and whether user meets the usability criteria
                # if so, switch to that spell
                if spell_action and spell_action.livesleft and spell_action.unlock <= self.unit.spirit:
                    self.unit.equipped = index
                    print "Switching action to new usable spell action: "+spell_action.namesuffix
                    break

            else:

                print "No available spells!"

    def closest_ally(self):
        """
        # Function Name: closest ally
        # Purpose: locates the closest ally
        # Output: ally - ally with the closest distance from unit
        """
        ally_list = []
        [ally_list.append([(self.unit.location_tile - unit.location_tile).get_magnitude(), unit.name, unit]) for unit in self.unit.map.team2 if unit != self.unit]
        if ally_list:
            # Selects the closest
            return min(ally_list)[2]
        # Nobody else is around
        else:
            return None

    def healer_available(self):
        """
        # Function Name: healer_available
        # Purpose: Checks if there is a healer on the map and in range (20 tiles)
        # Output: T/F if a healer is available
        """
        for unit in self.unit.map.team2:
            if unit.ai.current_state.name in ("HealerStandby", "HealerSOS") and (self.unit.location_tile - unit.location_tile).get_magnitude() < 20:
                return True
        return False

    def select_highest_priority_target(self, priority_list):
        """
        Function Name: select_highest_priority_target
        Purpose: Given a priority_list of target candidates, filter out all unreachable candidates and return
                the top scoring reachable candidates
        """


        priority_list.sort(reverse = True)
        selected_target = None

        # If target is non-flying, filter out targets it can't reach.
        if self.unit.has_trait_property('Flight'):
            selected_target = priority_list[0][2]
            print "%s's move - Target Selected: %s" % (self.unit.name, selected_target.name)

            # Picks off highest priority unit
            return selected_target

        else:
            for _, _, candidate_target in priority_list:

                candidate_destinations = [candidate_target.location_tile + Vector2(displacement) for
                               displacement in self.unit.spell_actions[self.unit.equipped].validattacks
                                ]

                for destination in candidate_destinations:

                    # Checks if any of the tiles that this unit can attack from are reachable.
                    if self.check_tile_passable(destination):
                        selected_target = candidate_target
                        print "%s's move - Target Selected: %s" % (self.unit.name, selected_target.name)
                        break

                # if target can be reached, go after it. Otherwise, go after next reachable target.
                if selected_target:
                    return selected_target

            else:
                return None


    def select_movement(self):

        target_destination = self.select_destination()

        # If target destination can be reached in this turn, skip additional pathfinding
        if target_destination and target_destination != self.unit.location_tile:
            displacement = tuple(target_destination - self.unit.location_tile)

            if displacement in self.unit.validmoves.keys():
                self.path = self.unit.get_path(displacement)
                self.final_pos = target_destination

            # If unit is flying, pathfinding is irrelevant and move to the closest available position
            elif self.unit.has_trait_property('Flight'):
                candidate_move_list = []
                for move in self.unit.validmoves.keys():
                    distance_to_destination = (target_destination - (self.unit.location_tile + Vector2(move))).get_magnitude()
                    candidate_move_list.append((distance_to_destination, move))

                selected_move = min(candidate_move_list)[1]

                self.path = self.unit.get_path(selected_move)
                self.final_pos = self.unit.location_tile + Vector2(selected_move)


            else:
                # Resort to pathfinding as a last option if destination is out of range
                self.path, self.final_pos = self.pathfind(target_destination)

                # Fall back on closest distance if no path is found.
                if not self.path:
                    print "%s has found no valid path to target destination. Falling back to minimum distance" % self.unit.name
                    candidate_move_list = []
                    for move in self.unit.validmoves.keys():
                        distance_to_destination = (target_destination - (self.unit.location_tile + Vector2(move))).get_magnitude()
                        candidate_move_list.append((distance_to_destination, move))

                    selected_move = min(candidate_move_list)[1]

                    self.path = self.unit.get_path(selected_move)
                    self.final_pos = self.unit.location_tile + Vector2(selected_move)

        else:
            self.final_pos = self.unit.location_tile
            self.path = []


    def select_destination(self):
        """
        select_destination
        purpose: After a target has been found, select the destination
        """
        candidate_destinations = self.generate_candidate_destinations()

        if candidate_destinations:

            # If going to the assigned destination is a valid option, set it as your final destination
            if (self.assigned_destination and self.check_tile_passable(self.assigned_destination) and
                self.check_ally_position(self.assigned_destination)):
                return self.assigned_destination

            else:

                prioritized_destinations = []

                for destination in candidate_destinations:
                    # Verifies that the destination can be entered and nobody is occupying it.
                    if self.check_tile_passable(destination) and self.check_ally_position(destination):
                        prioritized_destinations.append([self.prioritize_destinations(destination), destination])


                if prioritized_destinations:
                    target_destination = max(prioritized_destinations)
                    print "Final destination selected: %s" % target_destination
                    return target_destination[1]
                else:
                    print "No good destinations found. Staying put"
                    return None

        else:

            print "No good destinations found. Staying put"
            return None



    def generate_candidate_destinations(self):

        """
        # Purpose: Generate list of candidate destinations based on the spell range around a target.

        """

        # Case for pursuing target unit
        if self.target_unit:
            candidate_destinations = [self.target_unit.location_tile + Vector2(displacement) for
                               displacement in self.unit.spell_actions[self.unit.equipped].validattacks
                                ]
        # Case for going to assigned destination
        elif self.assigned_destination:
            candidate_destinations = [self.assigned_destination + Vector2(displacement) for
                               displacement in self.unit.spell_actions[self.unit.equipped].validattacks
                                ]
            candidate_destinations.append(self.assigned_destination)
        else:
            candidate_destinations = []


        return candidate_destinations


    def prioritize_destinations(self, destination):
        ######
        # Function Name: prioritize_inrange
        # Purpose: Prioritizes by balancing distance from enemy and distance from allies
        # Input: destination - destination tile (x, y)
        ######

        # Proximity term we want to select the best tile closest to us IF THE TARGET IS OUT OF RANGE
        distance_to_destination = (self.unit.location_tile-destination).get_magnitude()
        max_moves = max(self.unit.calculate_max_moves(), 1)
        if destination not in self.unit.validmoves.keys():
            distance_weight = 0.1
        else:
            distance_weight = 0

        # Want to keep away from enemy attack range
        enemies_in_range = 0.0
        for enemy in self.unit.map.team1:
            if enemy.spell_actions[enemy.equipped] and enemy.spell_actions[enemy.equipped].type == 'attack' and (destination in enemy.validmoves.keys() or destination in enemy.valid_spell_range):
                enemies_in_range += 1.0

        enemy_distance_term = ((len(self.unit.map.team1)-enemies_in_range)/len(self.unit.map.team1))
        enemy_distance_weight = 40

        # Want to stay close to allies while staying in range
        ally_distances = [(destination-ally.location_tile).get_magnitude() for ally in self.unit.map.team2 if (self.unit.location_tile - ally.location_tile).get_magnitude() <= self.pursdist and ally is not self.unit]
        if ally_distances:
            ally_distance_term = (max(ally_distances)-sum(ally_distances)/len(ally_distances))/max(ally_distances)
        else:
            ally_distance_term = 0
        ally_distance_weight = 40

        # Terrain Defense term
        tdef_term = -1*self.unit.map.terrainmap[tuple(destination)][0].damage_mod / 100.0
        tdef_weight = 20

        priority_numerator = (enemy_distance_term*enemy_distance_weight + ally_distance_term*ally_distance_weight + tdef_term*tdef_weight)
        priority_denominator = sum([enemy_distance_weight, ally_distance_weight, tdef_weight])


        base_priority = priority_numerator/priority_denominator - distance_weight*((distance_to_destination-max_moves)/max_moves)

        # Modifiers for priority
        if self.target_unit and self.unit.spell_actions[self.unit.equipped] and self.target_unit.spell_actions[self.target_unit.equipped]:
            target_displacement = destination - self.target_unit.location_tile

            # Additional priority is given to a certain tile if
            # - AI unit is in range
            # - Target is out of counterattack range
            if (tuple(target_displacement) in self.unit.spell_actions[self.unit.equipped].validattacks
                and tuple(-1*target_displacement) not in self.target_unit.spell_actions[self.target_unit.equipped].validattacks
                ):
                final_priority = base_priority*1.5
            else:
                final_priority = base_priority

        else:
            final_priority = base_priority

        return final_priority


    def pathfind(self, target):
        """
        Method name: pathfind
        Purpose: Given a set of coordinates (x, y), use A* Pathfinding to obtain a path to the target
        Input: target - destination
        Output: a list of displacement vectors to follow if a path is found, an empty list if a path does not exist
        """

        # convert target to a vector
        target = Vector2(target)

        # Clears out data
        self.open_by_coord = {}
        self.open_list = []
        self.closed_by_coord = {}
        self.current_path = []

        # Add the starting square to the open list

        starting_tile = PathfindingTile( self.unit.location_tile,
                                         None,
                                         None,
                                         self.unit.map.terrainmap[tuple(self.unit.location_tile)][0].cost,
                                        target)


        self.open_list.append(starting_tile)
        self.open_by_coord[tuple(self.unit.location_tile)] = starting_tile

        path_found = False

        # Vector Directions
        unit_vectors = [Vector2(0, 1),
                        Vector2(1, 0),
                        Vector2(-1, 0),
                        Vector2(0, -1)
                        ]


        # Checks if target can use swimming to get through water terrain
        swimming = self.unit.has_trait_property('Swimming')

        while not path_found:

            self.open_list.sort()

            # Remove the lowest scoring tile from the open list and set it to the current tile
            current_tile = self.open_list.pop(0)
            del self.open_by_coord[tuple(current_tile.position)]

            # Move the current tile to the closed list
            self.closed_by_coord[(tuple(current_tile.position))] = current_tile

            # Iterate through the four unit vectors (up, down, left, right)
            for unit_vector in unit_vectors:
                # Generate new tiles
                new_coords = current_tile.position + unit_vector
                new_coords_tuple = tuple(new_coords)

                # Initially checks if the new coordinates are valid or if it is already closed
                if self.check_tile_passable(new_coords) and new_coords_tuple not in self.closed_by_coord.keys():

                    # Case 1: not on the open list, add to open list and record the F costs
                    if new_coords_tuple not in self.open_by_coord.keys():

                        if swimming and (self.unit.map.terrainmap[new_coords_tuple][0].name == 'Deep Water'):
                            cost = 1
                        else:
                            cost = self.unit.map.terrainmap[new_coords_tuple][0].cost

                        new_tile = PathfindingTile( new_coords,
                                                    unit_vector,
                                                    current_tile,
                                                    cost,
                                                    target)

                        self.open_by_coord[new_coords_tuple] = new_tile
                        self.open_list.append(new_tile)

                    # Case 2: if target is already on the open list, check if the g_score
                    if new_coords_tuple in self.open_by_coord.keys():

                        # Determine if this path is better by recalculating G values
                        new_g_values = self.open_by_coord[new_coords_tuple].calculate_g_score(current_tile)
                        if new_g_values < self.open_by_coord[new_coords_tuple].g_score:
                            self.open_by_coord[new_coords_tuple].displacement_vector = unit_vector
                            self.open_by_coord[new_coords_tuple].parent = current_tile
                            (self.open_by_coord[new_coords_tuple].f_score,
                             self.open_by_coord[new_coords_tuple].g_score) = self.open_by_coord[new_coords_tuple].calculate_f_score(current_tile)

            # Success: return final coordinate path
            if current_tile.position == target:
                return self.construct_path(current_tile)

            if not self.open_list:
                print "No Valid Path Found"
                return [], self.unit.location_tile

    def construct_path(self, end_tile):
        """
        Method name: construct_path
        Purpose: given a pathfinding tile, walk through the parents back to the origin and return a list of displacement
        vectors to travel
        Inputs: end_tile - final tile obtained in A* Pathfinding
        Output: List of tuples containing coordiante and (dx, dy) unit displacement vectors
        """


        tile_list = []

        tile_list.append(end_tile)
        next_parent = end_tile.parent

        max_moves = self.unit.calculate_max_moves()


        start_appending = False
        # Walks backwards from the destination until the origin has been reached
        while next_parent:

            tile_list.append(next_parent)
            next_parent = next_parent.parent

        for index, tile in enumerate(tile_list):
            # Find the furthest tile that satisfies both conditions:
            # 1) Within movement range
            # 2) Another unit is not already occupying it
            if tile.g_score <= max_moves and self.check_ally_position(tile.position):
                break
            else:
                continue

        tile_list = tile_list[index:]
        tile_list.reverse()

        path = []

        final_coords = tile_list[0].position
        for index, tile in enumerate(tile_list):
            if tile.g_score <= max_moves:
                if tile.displacement_vector:
                    path.append(tuple(tile.displacement_vector))
                    final_coords = tile.position
            else:
                break

        return path, final_coords

    def check_tile_passable(self, new_coords):
        """
        Method name: check_ok
        Purpose: checks that new coordinates are actually in the map zone
        Inputs: New_coords - Vector2(x, y) of coordinates to check

        """

        swimming = self.unit.has_trait_property('Swimming')
        new_coords_tuple = tuple(new_coords)
        walk_prohibited = new_coords_tuple in self.unit.map.map_walk_prohibited
        fly_prohibited = new_coords_tuple in self.unit.map.map_fly_prohibited

        if new_coords.x > self.unit.map.map_x-1:
            return False
        if new_coords.y > self.unit.map.map_y-1:
            return False
        if new_coords.x < 0 or new_coords.y < 0:
            return False
        # Checks against enemy units
        for unit in self.unit.map.team1:
            if tuple(unit.location_tile) == tuple(new_coords):
                return False


        if walk_prohibited:

            if self.unit.has_trait_property('Flight') and not fly_prohibited:
                return True

            # If it is water and unit does not have swimming trait, prohibit entry
            if self.unit.map.terrainmap[new_coords_tuple][0].name == 'Deep Water' and not swimming:
                return False
            else:
                pass

            # If it is another type of non-walkable terrain, prohibit entry
            if not self.unit.map.terrainmap[new_coords_tuple][0].name == 'Deep Water':
                return False
            else:
                pass

        return True

    def check_ally_position(self, new_coords):
        """
        checks if any allied units occupy this tile to determine if it is a valid candidate for a final position
        """
        for unit in self.unit.map.team2:
            if tuple(unit.location_tile) == tuple(new_coords):
                return False
        return True



class PathfindingTile(object):

    def __init__(self, position, displacement_vector, parent, terrain_cost, target):
        """
        Method Name: __init__
        Purpose: Creates a pathfinding tile
        Inputs:
            position - Vector2(x, y) of this tile
            displacement vector - Unit vector telling the direction to get to this tile
            parent - this tile's parent
            terrain_cost - this tile's terrain cost
            target - destination the pathfinding algorithm is trying to reach

        """


        self.position = position
        self.displacement_vector = displacement_vector
        self.parent = parent
        self.terrain_cost = terrain_cost
        self.target = target
        self.f_score, self.g_score = self.calculate_f_score()

    def __cmp__(self, other):
        """
        Method name __cmp___
        Purpose: For sorting the list of tiles, returns a comparison of this object (self) and (other) by
        f - score. If the f-scores are equal, the two tiles are treated with the same cost in sorting
        """


        if self.f_score < other.f_score:
            return -1
        elif self.f_score > other.f_score:
            return 1
        else:
            return 0

    def calculate_f_score(self, other_parent = None):
        """
        Method name calculate_f_score

        Purpose: Calculates F score for A-star pathfinding for this tile

                F = G + H
                Where G: Cost to reach this tile
                      H: Heuristic distance to destination

        Inputs: other_parent: if another tile is supplied, calculate F based on other tile (optional)

        """

        # First, calculate G
        g_score = self.calculate_g_score()

        # Heuristic
        # Use Manhattan distance for heuristic
        h_score = fabs(self.position.x - self.target.x) + fabs(self.position.y - self.target.y)

        f_score = g_score + h_score

        return f_score, g_score

    def calculate_g_score(self, other_parent = None):
        """
        Calculate G score

        Purpose: Calculate the path distance for this tile
        Optional: other_parent (calculate this tile using other_parent instead of this one)

        """



        # Calculate score of current parent
        if other_parent:
            g_score = other_parent.g_score + self.terrain_cost
        elif not other_parent and self.parent:
            g_score = self.parent.g_score + self.terrain_cost
        # Starting tile case
        else:
            g_score = 0

        return g_score



class Attack(AIState):
    """
    # Class Name: Attack
    # Purpose: Range Limited offensive state
    #          Will seek out nearby enemies and attack, but does not actively pursue if out of range
    """
    def __init__(self, unit):
        """
        # Function Name: __init__
        # Purpose: Constructs the attack AI State class
        # Input:   Unit - Unit to assign AI State to
        """
        self.name = "Attack"
        self.pursdist = 10

        self.pursue_ssp = True

        AIState.__init__(self, unit)

    def think(self):
        """
        # Function Name: think
        # Purpose: Pre-action processing
        """

        if not self.unit.ai.spell_lock:
            self.check_spell_actions()
        self.unit.get_moves_path()

        # Unit is dormant if no spell equipped
        if self.unit.spell_actions[self.unit.equipped] and self.unit.spell_actions[self.unit.equipped].livesleft and  self.unit.spirit >= self.unit.spell_actions[self.unit.equipped].unlock:
            if self.unit.map.all_ssps:
                #
                unit_distances = [(unit.location_tile - self.unit.location_tile).get_magnitude() for unit in
                    self.unit.map.team1]

                avg_distance = sum(unit_distances)/len(unit_distances)

                ssp_candidates = []

                # Checks through all SSPs to see if there are any good ones.
                for ssp in self.unit.map.all_ssps.values():
                    # Case: SSP is unclaimed or belong sto team 1

                    if ssp.capture_state == 0 or ssp.capture_state == 1:
                        distance_to_ssp = (self.unit.location_tile - ssp.location).get_magnitude()

                        if distance_to_ssp < avg_distance and distance_to_ssp <= 0.5*self.pursdist:
                            ssp_candidates.append((distance_to_ssp, ssp.location))
                    # Case: SSP belongs to Enemy Team (Team 2)
                    else:
                        pass

                # Goes after the closest available SSP.
                if ssp_candidates and self.pursue_ssp:
                    self.assigned_destination = min(ssp_candidates)[1]

                else:
                    self.assigned_destination = None

            if self.unit.map.objective.__class__.__name__ in ('TerritoryDefenseBoss','TerritoryDefenseRout','TerritoryDefenseMultiBoss'):

#
                unit_distances = [(unit.location_tile - self.unit.location_tile).get_magnitude() for unit in
                    self.unit.map.team1]

                avg_distance = sum(unit_distances)/len(unit_distances)

                objective_candidates = []

                # Checks through all SSPs to see if there are any good ones.
                for objective_coord in self.unit.map.objective.arrival_locations:
                    # Case: SSP is unclaimed or belong sto team 1

                    objective_tile = Vector2(objective_coord)

                    distance_to_objective = (self.unit.location_tile - objective_tile).get_magnitude()

                    # If it is a territory defense objective,
                    if distance_to_objective < avg_distance and distance_to_objective <= self.pursdist:

                        # Prioritizes going for unoccupied tiles rather than contesting already occupied tiles.
                        if not self.unit.map.check_occupancy(objective_coord):
                            unoccupied_priority_multiplier = 0.25
                            objective_candidates.append((unoccupied_priority_multiplier*distance_to_objective, objective_tile))
                        else:
                            objective_candidates.append((distance_to_objective, objective_tile))


                # Goes after the closest available SSP.
                if objective_candidates:
                    self.assigned_destination = min(objective_candidates)[1]

                else:
                    self.assigned_destination = None


            # If unit does not have an assigned destination or
            if self.assigned_destination:

                # see if an enemy unit currently occupies the destination tile:
                for unit in self.unit.map.team1:
                    if unit.location_tile == self.assigned_destination:
                        self.target_unit = unit
                        break
                else:
                    self.target_unit = None
            else:
                self.target_unit = self.select_target()
                self.assigned_destination = None

        else:
            self.target_unit = None

        if self.target_unit or self.assigned_destination:
            self.select_movement()

        else:
            # If unit has no target, stay put
            self.final_pos = self.unit.location_tile
            self.path = []

    def compute_priority(self, target):
        """
        # Function Name: compute priority
        # Purpose: computes the priority using a weighted average of
        #             1. Target Distance
        #             2. Target Weakness
        #             3. Damage Effect
        #             4. Randomness factor
        #             5. Multiplicative weight factors
        """

        # Distance Term: How close is the target to you? (distance as fraction of max pursuit distance)
        #
        target_distance = (self.unit.location_tile - target.location_tile).get_magnitude()
        distance_term = (self.pursdist - target_distance)/self.pursdist
        distance_weight = 60

        # Weakness Term: How weak is the target? (fraction of total target HP depleted)
        #
        weakness_term = float(target.maxHP - target.HP)/float(target.maxHP)
        weakness_weight = 15

        # Damage Term: How much damage can you inflict on the target (fraction of total HP)?
        #
        if self.unit.spell_actions[self.unit.equipped]:
            raw_damage = self.unit.compute_damage(target)
        else:
            raw_damage = 0
        damage_term = min(float(raw_damage)/float(target.maxHP), 1.0)
        damage_weight = 20

        randomness_term = random()
        randomness_weight = 20

        weight_sum = weakness_weight + distance_weight + damage_weight + randomness_weight

        priority = (distance_term*distance_weight + weakness_term*weakness_weight + damage_term*damage_weight + randomness_term*randomness_weight)/weight_sum

        # Prioritize targets that aren't affected by status effects
        if self.unit.spell_actions[self.unit.equipped]:
            # 25% bonus if the target has yet to be afflicted by the status effect
            for status_effect in self.unit.spell_actions[self.unit.equipped].status_effects:
                if status_effect not in target.status:
                    priority *=  1.25

        # Prioritizes targets with healing spells
        if target.spell_actions[target.equipped] and target.spell_actions[target.equipped].type in ('support', 'healing', 'healingitem'):
            priority *= 1.2

        # Invisible targets are automatically prioritized last since AI has no chance of hitting them.
        if "Invisible" in target.status.keys():
            priority = 0

        return priority


    def select_target(self):
        """
        # Function Name: select_target
        # Purpose: Selects a target among the targets in range by sorting priorities
        """

        available_targets = [target for target in self.unit.map.team1 if ((self.unit.location_tile - target.location_tile).get_magnitude() <= self.pursdist
                or target.name in self.unit.ai.target_notifications)]


        # Only bothers to prioritize if there are enemy units within range
        if available_targets:


            # Assembles a list of all target units with their priority numbers
            priority_list = [[self.compute_priority(target), target.name, target] for target in available_targets]

            selected_target = self.select_highest_priority_target(priority_list)
            return selected_target

        else:

            # No targets in range
            return None

    def select_target_in_spellrange(self):
        available_targets = [target for target in self.unit.map.team1 if tuple(self.unit.location_tile - target.location_tile) in self.unit.spell_actions[self.unit.equipped].validattacks]

        # Only bothers to prioritize if there are enemy units within range
        if available_targets:


            # Assembles a list of all target units with their priority numbers
            priority_list = [[self.compute_priority(target), target.name, target] for target in available_targets]

            # Picks off highest priority unit
            target = max(priority_list)[2]
            print "%s's move - New target in spell range selected: %s" % (self.unit.name, target.name)

            return target

        else:

            # No targets in range
            return None


    def signal_nearby_allies(self):
        """
        # Purpose: Notifies nearby enemies that this unit is currently attacking someone.
        """
        max_signal_distance = 5

        for ally in self.unit.map.team2:

            if ((ally.location_tile - self.unit.location_tile).get_magnitude() < max_signal_distance and
                self.target_unit.name not in ally.ai.target_notifications):

                if ally.ai.current_state.name == 'Defend' and self.name =="Pursuit":
                    # Defending AI will only pursue targets at 2x it's pursuit range when signalled by pursuit AI
                    if (ally.location_tile - self.target_unit.location_tile).get_magnitude() < 2*ally.ai.current_state.pursdist:
                        ally.ai.target_notifications.append(self.target_unit.name)
                else:
                        ally.ai.target_notifications.append(self.target_unit.name)

    def act(self):
        """zz
        # Function Name: act
        # Purpose: Conducts the actions of a unit
        #           1. Move to a new location if target is in pursuit range
        #           2. Execute an attack
        """

        # Acts only if a unit has a target or an assigned destination
        if self.target_unit or self.assigned_destination:

            if self.target_unit and (self.target_unit.location_tile - self.unit.location_tile).get_magnitude() <= self.pursdist:
                self.signal_nearby_allies()

            # Center on unit
            self.unit.map.center_on(self.unit)

            # Forces update of map after unit moves
            self.unit.map.render_background()
            self.unit.map.render_all_units()
            self.unit.map.render_cursor()

            self.unit.map.engine.surface.blit(self.unit.map.engine.menu_board, (0, 490))
            self.unit.plot_stats()

            pygame.display.set_caption("Story of a Lost Sky - Current Pos(%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                               %(self.unit.map.cursor_pos.x, self.unit.map.cursor_pos.y, self.unit.map.screen_shift.x, self.unit.map.screen_shift.y))
            pygame.display.flip()

            self.unit.map.engine.pause(0.5)

            self.unit.map.cursor_pos = Vector2(tuple(self.final_pos))
            if self.unit.location_tile != self.final_pos and self.unit.map.engine.options.show_enemy_moves:
                self.unit.render_walk(self.path)

            #Update location and generate valid moves again.
            self.unit.update_location(self.final_pos.x, self.final_pos.y)

            # Center on Unit after action
            self.unit.map.center_on(self.unit)

            # Graphics rendering stuff (After move)
            self.unit.map.render_background()
            self.unit.map.render_all_units()
            self.unit.map.render_cursor()

            self.unit.map.engine.surface.blit(self.unit.map.engine.menu_board, (0, 490))
            self.unit.plot_stats()

            pygame.display.set_caption("Story of a Lost Sky - Current Pos(%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                               %(self.unit.map.cursor_pos.x, self.unit.map.cursor_pos.y, self.unit.map.screen_shift.x, self.unit.map.screen_shift.y))
            pygame.display.flip()
            self.unit.map.engine.clock.tick(60)

            # Delays time 1 second
            self.unit.map.engine.pause(1)

            pygame.display.flip()
            self.unit.map.engine.clock.tick(60)


            if self.target_unit:
                # Updates target location after movement phase.
                target_displacement = - self.target_unit.location_tile - self.unit.location_tile

                # Checks if the target is in range of the equipped attack
                if self.unit.spell_actions[self.unit.equipped] and target_displacement in self.unit.spell_actions[self.unit.equipped].validattacks:
                    self.unit.spell_actions[self.unit.equipped].action(self.unit, self.target_unit)
                    pygame.display.flip()
                    self.unit.map.engine.clock.tick(60)
                # Search for a new target you can hit
                elif self.unit.spell_actions[self.unit.equipped]:
                    self.target_unit = self.select_target_in_spellrange()
                    if self.target_unit:
                        self.unit.spell_actions[self.unit.equipped].action(self.unit, self.target_unit)
                        pygame.display.flip()
                        self.unit.map.engine.clock.tick(60)
            elif self.assigned_destination and self.unit.spell_actions[self.unit.equipped]:

                # If pusuing an assigned destination, check if you can make an attack
                self.target_unit = self.select_target_in_spellrange()
                if self.target_unit:
                    self.unit.spell_actions[self.unit.equipped].action(self.unit, self.target_unit)
                    pygame.display.flip()
                    self.unit.map.engine.clock.tick(60)



            pygame.display.flip()
            self.unit.map.engine.clock.tick(60)

            # Unit has taken an action
            return True

        else:

            # Unit has taken no action
            return False


    def find_nearest_healer(self):
        """
        # Function Name: find nearest healer
        # Purpose: Locates the nearest healer and return her unit
        # Output: healer - unit to signal for help
        """
        healer_list = []
        [healer_list.append([(self.unit.location_tile - unit.location_tile).get_magnitude(), unit.name, unit]) for unit in self.unit.map.team2 if unit.ai.current_state.name in ("HealerStandby", "HealerSOS")]

        # Selects the closest healer
        healer = min(healer_list)[2]
        return healer

    def check_conditions(self):
        """
        # Function Name: check_conditions
        # Purpose: Switches attack state to retreat or other states depending on conditions
        """

        targets_nearby = any([True for target in self.unit.map.team1 if
                            (self.unit.location_tile-target.location_tile).get_magnitude() < self.pursdist])


        support_spell_available, support_spell_index = self.unit.check_spell_type_availability('support')

        # If HP falls below 40%, signal a nearby healer
        if float(self.unit.HP)/self.unit.maxHP <= 0.40 and self.healer_available():

            # Locates healer
            healer = self.find_nearest_healer()

            # Signal SOS
            healer.ai.sos_list.append(self.unit.name)

            print "%s is low on HP! Sending an SOS message to %s and going to retreat mode!" % (self.unit.name, healer.name)
            return "AttackRetreat"

        elif support_spell_available and not targets_nearby:

            self.unit.equipped = support_spell_index

            print "No targets are nearby and a support spell is available. Switching to Support AI."

            return "Support"

        else:
            return None

    def check_spell_actions(self):
        """
        # Spell Action switching:
        # Purpose: If unit is out of spells go down or cannot use the equipped spell due to SC restrictions,
        # go down the list until you find the first equippable spell
        """

        # For the case of attack-type AI, if the spell action is optimized to the most powerful one that can be equipped
        self.unit.equipped = 0

        equippable_spells = sorted([(spell_action.effect, index) for index, spell_action in enumerate(self.unit.spell_actions)
                                if spell_action and spell_action.livesleft and spell_action.unlock <= self.unit.spirit and spell_action.type == 'attack'], reverse=True)

        # checks if any spells may be equipped, otherwise fall back to slot one
        if equippable_spells:
            print "%s: Switching to most powerful usable spell."%self.unit.name
            self.unit.equipped = equippable_spells[0][1]
        else:
            print "%s: Unable to find any usable spell"%self.unit.name
            self.unit.equipped = 0

class AttackRetreat(Attack):

    """
    # Class Name: AttackRetreat
    # Purpose: Retreat to nearest healer
    """
    def __init__(self, unit):
        """
        # Function Name: __init__
        # Purpose: Constructs the attack AI State class
        # Input:   Unit - Unit to assign AI State to
        """
        Attack.__init__(self, unit)
        self.name = "AttackRetreat"
        self.pursdist = 10
        self.target_unit = None

    def think(self):
        """
        # Function Name: think
        # Purpose: Pre-action processing
        """

        self.unit.get_moves_path()

        self.target_unit = None
        for unit in self.unit.map.team2:
            # Validates that healer unit has an equipped spell action and can be retreated to
            if self.unit.name in unit.ai.sos_list and unit.spell_actions[unit.equipped]:
                self.target_unit = unit
                break

        if self.target_unit:
            self.select_movement()

        else:
            # If unit has no target, stay put
            self.final_pos = self.unit.location_tile
            self.path = []

    def generate_candidate_destinations(self):

        """
        # Purpose: Generate list of candidate destinations based on the spell range around a target.

        """
        # Generate list of candidate destinations based on healing unit's spell range

        candidate_destinations = [self.target_unit.location_tile + Vector2(displacement) for
                               displacement in self.target_unit.spell_actions[self.target_unit.equipped].validattacks
                                ]
        return candidate_destinations

    def act(self):
        """
        # Function Name: act
        # Purpose: Conducts the actions of a unit
        #           1. Move to a new location if target is in pursuit range
        #           2. Execute an attack
        """

        # Checks if the closest target is within minimal range.
        if self.target_unit:

            # Center on unit
            self.unit.map.center_on(self.unit)
            self.unit.map.engine.pause(0.5)

            self.unit.map.cursor_pos = Vector2(tuple(self.final_pos))
            if self.unit.location_tile != self.final_pos and self.unit.map.engine.options.show_enemy_moves:
                self.unit.render_walk(self.path)

            #Update location and generate valid moves again.
            self.unit.update_location(self.final_pos.x, self.final_pos.y)

            self.unit.moved = True

            # Center on Unit after action
            self.unit.map.center_on(self.unit)

            # Graphics rendering stuff (After move)
            self.unit.map.render_background()
            self.unit.map.render_all_units()
            self.unit.map.render_cursor()

            self.unit.map.engine.surface.blit(self.unit.map.engine.menu_board, (0, 490))
            self.unit.plot_stats()

            pygame.display.set_caption("Story of a Lost Sky - Current Pos(%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                               %(self.unit.map.cursor_pos.x, self.unit.map.cursor_pos.y, self.unit.map.screen_shift.x, self.unit.map.screen_shift.y))

            pygame.display.flip()
            self.unit.map.engine.clock.tick(60)

            # Delays time 1 second
            self.unit.map.engine.pause(1)

            # No attack actions are performed in the retreat stage

            pygame.display.flip()
            self.unit.map.engine.clock.tick(60)

            return True

        else:

            return False

    def check_conditions(self):
        """
        # Function Name: check_conditions
        # Purpose: Switches attack state to attack if unit's HP is back up above 80%
        """


        def remove_from_sos_lists():
            """
            # Function Name: remove_from_sos_lists
            # Purpose: Remove unit from all SOS lists
            """
            for unit in self.unit.map.team2:
                if unit.ai.current_state.name in ("HealerStandby", "HealerSOS"):
                    if self.unit.name in unit.ai.sos_list:
                        del unit.ai.sos_list[unit.ai.sos_list.index(self.unit.name)]

        # If HP is above 60%, return to attack mode
        if float(self.unit.HP)/self.unit.maxHP >= 0.60:

            remove_from_sos_lists()
            print "%s is healthy again! Returning to attack mode!" % self.unit.name
            return "Attack"

        # No healers are available (All in range defeated) - Revert back to attack mode
        elif not self.healer_available():

            remove_from_sos_lists()
            print "%s is returning to attack mode since there are no healers left!" % self.unit.name
            remove_from_sos_lists()
            return "Attack"

        else:
            return None


class Pursuit(Attack):

    """
    # Class Name: Pursuit
    # Purpose: Extremely long range offensive state
    #          Will seek out nearby enemies and attack. Actively pursues enemies and captures SSPs
    """
    def __init__(self, unit):
        """
        # Function Name: __init__
        # Purpose: Constructs the attack AI State class
        # Input:   Unit - Unit to assign AI State to
        """
        Attack.__init__(self, unit)
        self.name = "Pursuit"
        self.pursdist = 30
        self.target_unit = None


    def select_target(self):
        """
        # Function Name: select_target
        # Purpose: Selects a target among the targets by sorting priorities
        """

        available_targets = []
        # No restrictions on range
        [available_targets.append(target) for target in self.unit.map.team1]

        def compute_priority(target):
            """
            # Function Name: compute priority
            # Purpose: computes the priority using a weighted average of
            #             1. Target Distance
            #             2. Target Weakness
            #             3. Damage Effect
            """

            # Distance Term: How close is the target to you? (distance as fraction of max pursuit distance)
            #
            target_distance = (self.unit.location_tile - target.location_tile).get_magnitude()
            distance_term = (self.pursdist - target_distance)/self.pursdist
            distance_weight = 60

            # Weakness Term: How weak is the target? (fraction of total target HP depleted)
            #
            weakness_term = float(target.maxHP - target.HP)/float(target.maxHP)
            weakness_weight = 15

            # Damage Term: How much damage can you inflict on the target (fraction of total HP)?
            #
            if self.unit.spell_actions[self.unit.equipped]:
                raw_damage = self.unit.compute_damage(target)
            else:
                raw_damage = 0
            damage_term = min(float(raw_damage)/float(target.maxHP), 1.0)
            damage_weight = 20

            priority = (distance_term*distance_weight + weakness_term*distance_weight + damage_term*damage_weight)/(distance_weight+weakness_weight+damage_weight)
            return priority

        # Only bothers to prioritize if there are enemy units within range
        if available_targets:

            priority_list = []

            # Assembles a list of all target units with their priority numbers
            [priority_list.append([compute_priority(target), target.name, target]) for target in available_targets]


            target = self.select_highest_priority_target(priority_list)

            return target

        else:

            # No targets in range
            return None

    def check_conditions(self):
        """
        # Function Name: check_conditions
        # Purpose: Switches attack state to retreat or other states depending on conditions
        """


        # If HP falls below 40%, signal a nearby healer
        if float(self.unit.HP)/self.unit.maxHP <= 0.40 and self.healer_available():

            # Locates healer
            healer = self.find_nearest_healer()

            # Signal SOS
            healer.ai.sos_list.append(self.unit.name)

            print "%s is low on HP! Sending an SOS message to %s and going to retreat mode!" % (self.unit.name, healer.name)
            return "PursuitRetreat"
        else:
            return None

class PursuitRetreat(AttackRetreat):

    def __init__(self, unit):
        """
        # Function Name: __init__
        # Purpose: Constructs the attack AI State class
        # Input:   Unit - Unit to assign AI State to
        """
        AttackRetreat.__init__(self, unit)
        self.name = "PursuitRetreat"

    def check_conditions(self):
        """
        # Function Name: check_conditions
        # Purpose: Switches attack state to attack if unit's HP is back up above 80%
        """

        def remove_from_sos_lists():
            """
            # Function Name: remove_from_sos_lists
            # Purpose: Remove unit from all SOS lists
            """
            for unit in self.unit.map.team2:
                if unit.ai.current_state.name in ("HealerStandby", "HealerSOS"):
                    if self.unit.name in unit.ai.sos_list:
                        del unit.ai.sos_list[unit.ai.sos_list.index(self.unit.name)]

        # If HP is above 60%, return to pursuit mode
        if float(self.unit.HP)/self.unit.maxHP >= 0.60:

            remove_from_sos_lists()
            print "%s is healthy again! Returning to attack mode!" % self.unit.name
            return "Pursuit"

        # No healers are available (All in range defeated) - Revert back to pursuit mode
        elif not self.healer_available():

            remove_from_sos_lists()
            print "%s is returning to attack mode since there are no healers left!" % self.unit.name
            remove_from_sos_lists()
            return "Pursuit"

        else:
            return None


class Defend(Attack):

    """
    # Class Name: Pursuit
    # Purpose: Extremely long range offensive state
    #          Will seek out nearby enemies and attack. Actively pursues enemies and captures SSPs
    """
    def __init__(self, unit):
        """
        # Function Name: __init__
        # Purpose: Constructs the attack AI State class
        # Input:   Unit - Unit to assign AI State to
        """
        Attack.__init__(self, unit)
        self.name = "Defend"
        self.pursdist = 5
        self.target_unit = None

    def check_conditions(self):
        """
        # Function Name: check_conditions
        # Purpose: Switches attack state to retreat or other states depending on conditions
        """


        # If HP falls below 40%, signal a nearby healer
        if float(self.unit.HP)/self.unit.maxHP <= 0.40 and self.healer_available():

            # Locates healer
            healer = self.find_nearest_healer()

            # Signal SOS
            healer.ai.sos_list.append(self.unit.name)

            print "%s is low on HP! Sending an SOS message to %s and going to retreat mode!" % (self.unit.name, healer.name)
            return "DefendRetreat"
        else:
            return None

class DefendRetreat(AttackRetreat):

    def __init__(self, unit):
        """
        # Function Name: __init__
        # Purpose: Constructs the attack AI State class
        # Input:   Unit - Unit to assign AI State to
        """
        AttackRetreat.__init__(self, unit)
        self.name = "DefendRetreat"

    def check_conditions(self):
        """
        # Function Name: check_conditions
        # Purpose: Switches attack state to attack if unit's HP is back up above 80%
        """

        def remove_from_sos_lists():
            """
            # Function Name: remove_from_sos_lists
            # Purpose: Remove unit from all SOS lists
            """
            for unit in self.unit.map.team2:
                if unit.ai.current_state.name in ("HealerStandby", "HealerSOS"):
                    if self.unit.name in unit.ai.sos_list:
                        del unit.ai.sos_list[unit.ai.sos_list.index(self.unit.name)]

        # If HP is above 60%, return to pursuit mode
        if float(self.unit.HP)/self.unit.maxHP >= 0.60:

            remove_from_sos_lists()
            print "%s is healthy again! Returning to attack mode!" % self.unit.name
            return "Defend"

        # No healers are available (All in range defeated) - Revert back to pursuit mode
        elif not self.healer_available():

            remove_from_sos_lists()
            print "%s is returning to attack mode since there are no healers left!" % self.unit.name
            remove_from_sos_lists()
            return "Defend"

        else:
            return None


class HealerStandby(AIState):

    """
    # Class Name: Healer Standby
    # Purpose: Range Limited healer state
    #          Will seek out nearby allies and heal them, but does not actively
    #          seek out units out of range
    """
    def __init__(self, unit):

        """
        # Function Name: __init__
        # Purpose: Constructs the  healer standby AI State class
        # Input:   Unit - Unit to assign AI State to
        """
        AIState.__init__(self, unit)
        self.name = "HealerStandby"
        self.pursdist = 10
        self.target_unit = None

    def think(self):
        """
        # Function Name: think
        # Purpose: Pre-action processing
        """

        self.check_spell_actions()
        self.unit.get_moves_path()

        # Acts only if unit has a spell equipped
        if self.unit.spell_actions[self.unit.equipped] and self.unit.spell_actions[self.unit.equipped].livesleft and self.unit.spirit >= self.unit.spell_actions[self.unit.equipped].unlock:
            self.target_unit = self.select_target()
        else:
            self.target_unit = None

        if self.target_unit:
            self.select_movement()

        else:
            # If unit has no target, stay put
            self.final_pos = self.unit.location_tile
            self.path = []

    def select_target(self):
        """
        # Function Name: select_target
        # Purpose: Selects a target among the targets in range by sorting priorities
        """

        available_targets = [target for target in self.unit.map.team2 if (self.unit.location_tile - target.location_tile).get_magnitude() <= self.pursdist and target.HP < target.maxHP]

        def compute_priority(target):
            """
            # Function Name: compute priority
            # Purpose: computes the priority using an equal average of
            #             1. Target Distance
            #             2. Target Weakness
            """

            # Distance Term: How close is the target to you? (distance as fraction of max pursuit distance)
            #
            target_distance = (self.unit.location_tile - target.location_tile).get_magnitude()
            distance_term = (self.pursdist - target_distance)/self.pursdist

            # Weakness Term: How weak is the target? (fraction of total target HP depleted)
            #
            weakness_term = float(target.maxHP - target.HP)/float(target.maxHP)

            priority = (distance_term + weakness_term)/2

            return priority

        # Only bothers to prioritize if there are enemy units within range
        if available_targets:

            priority_list = []

            # Assembles a list of all target units with their priority numbers
            [priority_list.append([compute_priority(target), target.name, target]) for target in available_targets]

            # Picks off highest priority unit
            target = self.select_highest_priority_target(priority_list)

            return target

        else:

            # No targets in range
            return None

    def act(self):

        """
        # Function Name: act
        # Purpose: Conducts the actions of a unit
        #           1. Move to a new location if target is in pursuit range
        #           2. Heals unit
        """

        # Check if unit has a target
        if self.target_unit:

            # Center on unit
            self.unit.map.center_on(self.unit)
            self.unit.map.engine.pause(0.5)

            self.unit.map.cursor_pos = Vector2(tuple(self.final_pos))
            if self.unit.location_tile != self.final_pos and self.unit.map.engine.options.show_enemy_moves:
                self.unit.render_walk(self.path)

            #Update location and generate valid moves again.
            self.unit.update_location(self.final_pos.x, self.final_pos.y)

            self.unit.moved = True

            # Center on Unit after action
            self.unit.map.center_on(self.unit)

            # Graphics rendering stuff (After move)
            self.unit.map.render_background()
            self.unit.map.render_all_units()
            self.unit.map.render_cursor()

            self.unit.map.engine.surface.blit(self.unit.map.engine.menu_board, (0, 490))
            self.unit.plot_stats()

            pygame.display.set_caption("Story of a Lost Sky - Current Pos(%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                               %(self.unit.map.cursor_pos.x, self.unit.map.cursor_pos.y, self.unit.map.screen_shift.x, self.unit.map.screen_shift.y))

            pygame.display.flip()
            self.unit.map.engine.clock.tick(60)

            # Delays time 1 second
            self.unit.map.engine.pause(1)

            pygame.display.flip()
            self.unit.map.engine.clock.tick(60)

            # Updates target location after movement phase.
            target_displacement = self.target_unit.location_tile - self.unit.location_tile

            # Checks if the target is in range of the equipped spell
            if self.unit.spell_actions[self.unit.equipped] and target_displacement in self.unit.spell_actions[self.unit.equipped].validattacks and self.target_unit.HP != self.target_unit.maxHP:
                self.unit.spell_actions[self.unit.equipped].action(self.unit, self.target_unit)
                pygame.display.flip()
                self.unit.map.engine.clock.tick(60)

            pygame.display.flip()
            self.unit.map.engine.clock.tick(60)

            return True

        else:

            return False

    def check_conditions(self):
        if self.unit.ai.sos_list:
            print "%s - Switching to priority healing mode." % self.unit.name
            return "HealerSOS"
        else:
            return None


    def check_spell_actions(self):
        """
        # Spell Action switching:
        # Purpose: If unit is out of spells go down or cannot use the equipped spell due to SC restrictions,
        # go down the list until you find the first equippable spell
        """

        # For the case of attack-type AI, if the spell action is optimized to the most powerful one that can be equipped
        self.unit.equipped = 0

        equippable_spells = sorted([(spell_action.effect, index) for index, spell_action in enumerate(self.unit.spell_actions)
                                if spell_action and spell_action.livesleft and spell_action.unlock <= self.unit.spirit and spell_action.type in ('healing', 'healingitem')], reverse=True)

        # checks if any spells may be equipped, otherwise fall back to slot one
        if equippable_spells:
            print "%s: Switching to most powerful usable spell."%self.unit.name
            self.unit.equipped = equippable_spells[0][1]
        else:
            print "%s: Unable to find any usable spell"%self.unit.name
            self.unit.equipped = 0


class Support(HealerStandby):
    def __init__(self, unit):
        HealerStandby.__init__(self, unit)
        self.name = "Support"
        self.pursdist = 10
        self.target_unit = None

    def select_target(self):
        """
        Identifies the nearest unit without a status effect and prioritizes that one.

        """
        if self.unit.spell_actions[self.unit.equipped].type == 'support':

            status_effect = set(self.unit.spell_actions[self.unit.equipped].status_effects)

            available_targets = [target for target in self.unit.map.team2
                                 if (self.unit.location_tile - target.location_tile).get_magnitude() <= self.pursdist
                                 and target != self.unit]

            prioritized_targets = []

            for target in available_targets:
                # Check if target has the status effect that this unit's support spell's status effects
                # using a set-intersection method

                target_status = set(target.status.keys())

                if not status_effect.intersection(target_status):
                    prioritized_targets.append(((self.unit.location_tile - target.location_tile).get_magnitude(),
                                                target))

            # Selects the closest target without the status effect and returns it
            if prioritized_targets:
                selected_target = min(prioritized_targets)[1]

                return selected_target
            else:
                return None

        else:
            return None


    def act(self):

        """
        # Function Name: act
        # Purpose: Conducts the actions of a unit
        #           1. Move to a new location if target is in pursuit range
        #           2. Applies positive status effect
        """

        # Check if unit has a target
        if self.target_unit:

            # Center on unit
            self.unit.map.center_on(self.unit)
            self.unit.map.engine.pause(0.5)

            self.unit.map.cursor_pos = Vector2(tuple(self.final_pos))
            if self.unit.location_tile != self.final_pos and self.unit.map.engine.options.show_enemy_moves:
                self.unit.render_walk(self.path)

            #Update location and generate valid moves again.
            self.unit.update_location(self.final_pos.x, self.final_pos.y)

            self.unit.moved = True

            # Center on Unit after action
            self.unit.map.center_on(self.unit)

            # Graphics rendering stuff (After move)
            self.unit.map.render_background()
            self.unit.map.render_all_units()
            self.unit.map.render_cursor()

            self.unit.map.engine.surface.blit(self.unit.map.engine.menu_board, (0, 490))
            self.unit.plot_stats()

            pygame.display.set_caption("Story of a Lost Sky - Current Pos(%1.0f, %1.0f) - Shift (%1.0f, %1.0f)"
                                               %(self.unit.map.cursor_pos.x, self.unit.map.cursor_pos.y, self.unit.map.screen_shift.x, self.unit.map.screen_shift.y))

            pygame.display.flip()
            self.unit.map.engine.clock.tick(60)

            # Delays time 1 second
            self.unit.map.engine.pause(1)

            pygame.display.flip()
            self.unit.map.engine.clock.tick(60)

            # Updates target location after movement phase.
            target_displacement = self.target_unit.location_tile - self.unit.location_tile

            # Checks if the target is in range of the equipped spell
            if self.unit.spell_actions[self.unit.equipped] and target_displacement in self.unit.spell_actions[self.unit.equipped].validattacks:
                self.unit.spell_actions[self.unit.equipped].action(self.unit, self.target_unit)
                pygame.display.flip()
                self.unit.map.engine.clock.tick(60)

            pygame.display.flip()
            self.unit.map.engine.clock.tick(60)

            return True

        else:

            return False


    def check_conditions(self):

        # Case if enemies are nearby and if attack spells are available
        switch_distance = 5
        attack_spell_available, attack_spell_index = self.unit.check_spell_type_availability('attack')

        if (any([True for enemy in self.unit.map.team1
                if (enemy.location_tile-self.unit.location_tile).get_magnitude() < switch_distance]) and
                attack_spell_available):
            # Switch to attack spell
            self.unit.equipped = attack_spell_index

            print "Enemies nearby and attack spell available. Switching to attack AI."

            return 'Attack'


    def check_spell_actions(self):
        """
        # Spell Action switching:
        # Purpose: If unit is out of spells go down or cannot use the equipped spell due to SC restrictions,
        # go down the list until you find the first equippable spell
        """

        if not self.unit.spell_actions[self.unit.equipped] or self.unit.spell_actions[self.unit.equipped].unlock > self.unit.spirit:

            for index, spell_action in enumerate(self.unit.spell_actions):

                # checks whether spell exists and whether user meets the usability criteria
                # also checks whether it's a support spell
                # if so, switch to that spell
                if spell_action and spell_action.livesleft and spell_action.unlock <= self.unit.spirit and spell_action.type == 'support':
                    self.unit.equipped = index
                    print "Switching action to new usable spell action: "+spell_action.namesuffix
                    break

            else:

                print "No available spells!"

class HealerSOS(HealerStandby):

    def __init__(self, unit):

        """
        # Function Name: __init__
        # Purpose: Constructs the  healer SOS AI State class
        # Input:   Unit - Unit to assign AI State to
        """
        HealerStandby.__init__(self, unit)
        self.name = "HealerSOS"
        self.pursdist = 20
        self.target_unit = None

    def think(self):
        """
        Function name: think
        Purpose: Select target and calculate movement path.
        """

        self.unit.get_moves_path()


        # Acts only if unit has a spell equipped
        if self.unit.spell_actions[self.unit.equipped]:
            self.target_unit = self.select_target()

        if self.target_unit:
            self.select_movement()

        else:
            # If unit has no target, stay put
            self.final_pos = self.unit.location_tile
            self.path = []

    def select_target(self):

        """
        # Function Name: select_target
        # Purpose: Selects a target among the targets in range by sorting priorities
        """

        available_targets = []
        [available_targets.append(target) for target in self.unit.map.team2 if (self.unit.location_tile - target.location_tile).get_magnitude() <= self.pursdist and target.name in self.unit.ai.sos_list]

        def compute_priority(target):
            """
            # Function Name: compute priority
            # Purpose: computes the priority using an equal average of
            #             1. Target Distance
            #             2. Target Weakness
            """

            # Distance Term: How close is the target to you? (distance as fraction of max pursuit distance)
            #
            target_distance = (self.unit.location_tile - target.location_tile).get_magnitude()
            distance_term = (self.pursdist - target_distance)/self.pursdist

            # Weakness Term: How weak is the target? (fraction of total target HP depleted)
            #
            weakness_term = float(target.maxHP - target.HP)/float(target.maxHP)

            priority = (distance_term + weakness_term)/2
            return priority

        # Only bothers to prioritize if there are enemy units within range
        if available_targets:

            priority_list = []

            # Assembles a list of all target units with their priority numbers
            [priority_list.append([compute_priority(target), target.name, target]) for target in available_targets]

            # Picks off highest priority unit
            target = self.select_highest_priority_target(priority_list)

            return target

        else:

            # No targets in range
            return None

    def refresh_sos_list(self):
        """
        # Function Name: refresh_sos_list
        # Purpose: Refreshes SOS list to clear out any units that have been defeated
        #    before the got healed
        """
        for name in self.unit.ai.sos_list:
            if not self.unit.map.all_units_total[name].alive:
                del self.unit.ai.sos_list[self.unit.ai.sos_list.index(name)]

    def check_conditions(self):
        """
        # Function Name: check_conditions
        # Purpose: Checks if SOS list is empty and jumps back to standby
        """

        # Updates SOS List
        self.refresh_sos_list()

        if not self.unit.ai.sos_list:
            print "%s - No units in need of help. Switching to range limited healing mode.." % (self.unit.name)
            return "HealerStandby"
        else:
            return None

