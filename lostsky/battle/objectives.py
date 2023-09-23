# Battle Objectives

class Objective(object):

    """
    # Map Objective Class (generic)
    """

    def __init__(self, desc):
        """
        # Function name: __init__
        # Purpose: Initializes the objective
        # Inputs:  desc - objective description
        """
        self.desc = desc

    def check(self, map):
        """
        # Function name: check
        # Purpose: Checks if a victory condition has been met
        # Inputs: Map - the map to check within
        """

        pass

    def report(self, map):

        """
        # Function name: check
        # Purpose: Reports the progress of the player and enemy
        # Inputs: Map - the map to check within
        # Outputs: player_status, enemy_status
        """
        pass

class Rout(Objective):
    """
    # Rout Objective Class (generic)
    """

    def __init__(self, desc):
        """
        # Function name: __init__
        # Purpose: Initializes the objective
        # Inputs:  desc - objective description
        """
        Objective.__init__(self, desc)
        self.goal = "Defeat all enemies!"
        self.enemy_goal = "All player units defeated!"

    def check(self, map):

        """
        # Function name: check
        # Purpose: Checks if a victory condition has been met
        # Inputs: Map - the map to check within
        #
        #   Conditions for Player Victory - Defeat all enemies
        #   Condition for Enemy Victory - Defeat all allies
        """

        if map.team1 == []:
            return 'team2victory'
        elif map.team2 == []:
            return 'team1victory'
        else:
            return False


    def report(self, map):

        """
        # Function name: report
        # Purpose: Reports the progress of the player and enemy
        # Inputs: Map - the map to check within
        # Outputs: player_status, enemy_status - strings describing the progress the player and enemy have made
        """

        player_status = "Enemies Remaining: "+str(len(map.team2))
        enemy_status = "Player Units Remaining: "+str(len(map.team1))
        return player_status, enemy_status

class Headhunt(Objective):
    """
    # Headhunt Objective Class (Targetted)
    """

    def __init__(self, target, desc):
        """
        # Function name: __init__
        # Purpose: Initializes the objective
        # Inputs:    target - target that must be destroyed
        #            desc - objective description
        """
        Objective.__init__(self, desc)
        self.goal = "Defeat "+target.name+"!"
        self.enemy_goal = "All player units defeated and " +target.name+" protected!"
        self.target = target

    def check(self, map):

        """
        # Function name: check
        # Purpose: Checks if a victory condition has been met
        # Inputs: Map - the map to check within
        #
        #   Conditions for Player Victory - Defeat target
        #   Condition for Enemy Victory - Defeat all allies
        """

        if map.team1 == []:
            return 'team2victory'
        elif self.target.alive == False:
            return 'team1victory'
        else:
            return False

    def report(self, map):
        """
        # Function name: report
        # Purpose: Reports the progress of the player and enemy
        # Inputs: Map - the map to check within
        # Outputs: player_status, enemy_status - strings describing the progress the player and enemy have made
        """

        player_status = self.target.name+" HP: "+str(self.target.HP)+"/"+str(self.target.maxHP)
        enemy_status = "Enemies Remaining: "+str(len(map.team1))
        return player_status, enemy_status

class Protect(Objective):

    """
    # Protect and Destroy Objective Class (Targetted)
    """

    def __init__(self, target, desc):
        """
        # Function name: __init__
        # Purpose: Initializes the objective
        # Inputs:    target - target that player must protect
        #            desc - objective description
        """
        Objective.__init__(self, desc)
        self.goal = "Defeat all enemies and protect " +target.name+"!"
        self.enemy_goal = target.name+" defeated!"
        self.target = target

    def check(self, map):

        """
        # Function name: check
        # Purpose: Checks if a victory condition has been met
        # Inputs: Map - the map to check within
        #
        #   Conditions for Player Victory - Defeat all enemies
        #   Condition for Enemy Victory - Defeat target
        """
        if self.target.alive == False:
            return 'team2victory'
        elif map.team2 == []:
            return 'team1victory'
        else:
            return False

    def report(self, map):

        """
        # Function name: report
        # Purpose: Reports the progress of the player and enemy
        # Inputs: Map - the map to check within
        # Outputs: player_status, enemy_status - strings describing the progress the player and enemy have made
        """

        player_status = "Enemies Remaining: "+str(len(map.team2))
        enemy_status = self.target.name+" HP: "+str(self.target.HP)+"/"+str(self.target.maxHP)
        return player_status, enemy_status

class Survive(Objective):
    """
    # Survive Objective
    """

    def __init__(self, count, desc):
        """
        # Function name: __init__
        # Purpose: Initializes the objective
        # Inputs:    count - number of turns that player must survive
        #            desc - objective description
        """
        Objective.__init__(self, desc)
        self.goal = "Survive for " +str(count)+" turns or defeat all enemies!"
        self.enemy_goal = "All player units defeated in "+str(count)+" turns!"
        self.count = count

    def check(self, map):

        """
        # Function name: check
        # Purpose: Checks if a victory condition has been met
        # Inputs: Map - the map to check within
        #
        #   Conditions for Player Victory - Survive X complete turns. All enemies defeated.
        #   Condition for Enemy Victory - Defeat player team by the end of X turns.
        """

        if map.team1 == []:
            return 'team2victory'
        elif map.turn_count == self.count+1 or map.team2 == []:
            return 'team1victory'
        else:
            return False


    def report(self, map):
        """
        # Function name: report
        # Purpose: Reports the progress of the player and enemy
        # Inputs: Map - the map to check within
        # Outputs: player_status, enemy_status - strings describing the progress the player and enemy have made
        """
        player_status = "Turns Remaining: "+str(self.count+1-map.turn_count+1)
        enemy_status = "Player Units Remaining: "+str(len(map.team1))
        return player_status, enemy_status

class Escape(Objective):

    def __init__(self, turns, location_box, location_name, desc):
        """
        # Function name: __init__
        # Purpose: Initializes the objective
        # Inputs:
        #            turns - number of turns that the mission must be completed by
        #            location_box - (X, Y, dX, dY) for required arrival location
        #            location_name - name of the place player needs to arrive at
        #            desc - objective description
        """
        Objective.__init__(self, desc)
        self.goal = "Arrive at %s by %s turns!" % (location_name, turns)
        self.enemy_goal = "All player units defeated!"
        self.turns = turns

        # Set up the valid arrival tiles
        x1, y1, x2, y2 = location_box
        self.arrival_locations = []
        self.location_name = location_name
        [self.arrival_locations.append((x1+delta_x, y1+delta_y)) for delta_x in xrange(0, x2) for delta_y in xrange(0, y2)]

        self.arrived = False

    def check(self, map):
        """
        # Function name: check
        # Purpose: Checks if a victory condition has been met
        # Inputs: Map - the map to check within
        #
        #   Conditions for Player Victory - Any player unit has arrived at the location
        #   Condition for Enemy Victory - Defeat player team or turns have run out
        """

        # Checks if any party member has arrived
        if self.arrived == False:
            for unit in map.team1:
                if tuple(unit.location_tile) in self.arrival_locations:
                    self.arrived = True
                    map.say(unit.name+" has arrived at "+self.location_name+"!")
                    break

        if self.arrived == True:
            return 'team1victory'
        elif map.team1 == [] or map.turn_count >= self.turns+1:
            return 'team2victory'
        else:
            return False

    def report(self, map):
        """
        # Function name: report
        # Purpose: Reports the progress of the player and enemy
        # Inputs: Map - the map to check within
        # Outputs: player_status, enemy_status - strings describing the progress the player and enemy have made
        """

        player_status = "Turns remaining: %s" % str(self.turns - map.turn_count)
        enemy_status = "Player Units Remaining: %d" % len(map.team1)
        return player_status, enemy_status


class DefeatAndArrive(Objective):

    def __init__(self, target, location_box, location_name, desc):
        """
        # Function name: __init__
        # Purpose: Initializes the objective
        # Inputs:
        #            target - target that must be defeated
        #            location_box - (X, Y, dX, dY) for required arrival location
        #            location_name - name of the place player needs to arrive at
        #            desc - objective description
        """
        Objective.__init__(self, desc)
        self.goal = "Arrive at "+location_name+" and defeat "+target.name+"!"
        self.enemy_goal = "All player units defeated!"

        # Set up the boss target
        self.target = target

        # Set up the valid arrival tiles
        x1, y1, x2, y2 = location_box
        self.arrival_locations = []
        self.location_name = location_name
        [self.arrival_locations.append((x1+delta_x, y1+delta_y)) for delta_x in xrange(0, x2) for delta_y in xrange(0, y2)]

        self.arrived = False

    def check(self, map):
        """
        # Function name: check
        # Purpose: Checks if a victory condition has been met
        # Inputs: Map - the map to check within
        #
        #   Conditions for Player Victory - Any player unit has arrived at the location and the target enemy has been beaten
        #   Condition for Enemy Victory - Defeat player team
        """

        # Checks if any party member has arrived
        if self.arrived == False:
            for unit in map.team1:
                if tuple(unit.location_tile) in self.arrival_locations:
                    self.arrived = True
                    map.say(unit.name+" has arrived at "+self.location_name+"!")
                    break

        if self.target.alive == False and self.arrived == True:
            return 'team1victory'
        elif map.team1 == []:
            return 'team2victory'
        else:
            return False

    def report(self, map):
        """
        # Function name: report
        # Purpose: Reports the progress of the player and enemy
        # Inputs: Map - the map to check within
        # Outputs: player_status, enemy_status - strings describing the progress the player and enemy have made
        """

        if self.arrived:
            player_status = "Arrived: Yes ; "
        else:
            player_status = "Arrived: No ; "

        if self.target.alive:
            player_status += self.target.name+" HP: "+str(self.target.HP)+"/"+str(self.target.maxHP)
        else:
            player_status += self.target.name+" defeated!"

        enemy_status = "Player Units Remaining: "+str(len(map.team1))
        return player_status, enemy_status

class CaptureSpiritSource(Objective):

    def __init__(self, ssp_count, desc):
        """
        # Function name: __init__
        # Purpose: Creates a capture magic sources objective
        # Inputs:
        #            ssp_count - Number of spirit source points that need to be captured
        #            desc - objective description
        """

        Objective.__init__(self, desc)
        self.ssp_count = ssp_count
        self.goal = "Capture "+str(self.ssp_count)+" Spirit Source Points!"
        self.enemy_goal = "All player units defeated!"

    def check(self, map):
        """
        # Function name: check
        # Purpose: Checks if a victory condition has been met
        # Inputs: Map - the map to check within
        #
        #   Conditions for Player Victory - X number of SSPs are under player control
        #   Condition for Enemy Victory - Defeat player team
        """
        counter = 0

        # Checks the number of points that have been captured
        for ssp in map.all_ssps.values():
            if ssp.capture_state == 1:
                counter += 1

        # Checks if the number of ssps capture is >= minimum count to win
        if counter >= self.ssp_count:
            return 'team1victory'
        elif map.team1 == []:
            return 'team2victory'
        else:
            return False

    def report(self, map):

        """
        # Function name: report
        # Purpose: Reports the progress of the player and enemy
        # Inputs: Map - the map to check within
        # Outputs: player_status, enemy_status - strings describing the progress the player and enemy have made
        """

        counter = 0

        # Checks the number of points that have been captured
        for ssp in map.all_ssps.values():
            if ssp.capture_state == 1:
                counter += 1

        player_status = "Spirit Source Points: "+str(counter)+"/"+str(self.ssp_count)
        enemy_status = "Player Units Remaining: "+str(len(map.team1))

        return player_status, enemy_status

class TerritoryDefenseBoss(Objective):

    def __init__(self, target, location_box, location_name, desc):
        """
        # Function name: __init__
        # Purpose: Initializes the objective
        # Inputs:
        #            target - target that must be defeated
        #            location_box - (X, Y, dX, dY) where enemy is not allowed to enter
        #            location_name - name of the place player needs to arrive at
        #            desc - objective description
        """
        Objective.__init__(self, desc)
        self.goal = "Defend "+location_name+" and defeat "+target.name+"!"
        self.enemy_goal = "All player units defeated!"

        # Set up the boss target
        self.target = target

        # Set up the valid arrival tiles
        x1, y1, x2, y2 = location_box
        self.arrival_locations = [(x1+delta_x, y1+delta_y) for delta_x in xrange(0, x2)
                                   for delta_y in xrange(0, y2)]

        self.location_name = location_name

        self.arrived = False

    def check(self, map):
        """
        # Function name: check
        # Purpose: Checks if a victory condition has been met
        # Inputs: Map - the map to check within
        #
        #   Conditions for Player Victory - Enemy boss chara is defeated
        #   Condition for Enemy Victory - Either defeat all player units or any enemy unit must arrive at
        #                                the destination location
        """

        # Checks if any party member has arrived
        for unit in map.team2:
            if tuple(unit.location_tile) in self.arrival_locations:
                self.arrived = True

        if not self.target.alive:
            return 'team1victory'
        elif not map.team1 or self.arrived:
            return 'team2victory'
        else:
            return False

    def report(self, map):
        """
        # Function name: report
        # Purpose: Reports the progress of the player and enemy
        # Inputs: Map - the map to check within
        # Outputs: player_status, enemy_status - strings describing the progress the player and enemy have made
        """

        player_status = self.target.name+" HP: "+str(self.target.HP)+"/"+str(self.target.maxHP)

        enemy_status = "Advance to "+self.location_name+"; Player Units Remaining: "+str(len(map.team1))

        return player_status, enemy_status

class TerritoryDefenseRout(Objective):

    def __init__(self, location_box, location_name, desc):
        """
        # Function name: __init__
        # Purpose: Initializes the objective
        # Inputs:
        #            target - target that must be defeated
        #            location_box - (X, Y, dX, dY) where enemy is not allowed to enter
        #            location_name - name of the place player needs to arrive at
        #            desc - objective description
        """
        Objective.__init__(self, desc)
        self.goal = "Defend "+location_name+" and defeat all enemies!"
        self.enemy_goal = "All player units defeated!"

        # Set up the valid arrival tiles
        x1, y1, x2, y2 = location_box
        self.arrival_locations = [(x1+delta_x, y1+delta_y) for delta_x in xrange(0, x2)
                                   for delta_y in xrange(0, y2)]

        self.location_name = location_name

        self.arrived = False

    def check(self, map):
        """
        # Function name: check
        # Purpose: Checks if a victory condition has been met
        # Inputs: Map - the map to check within
        #
        #   Conditions for Player Victory - Enemy boss chara is defeated
        #   Condition for Enemy Victory - Either defeat all player units or any enemy unit must arrive at
        #                                the destination location
        """

        # Checks if any party member has arrived
        for unit in map.team2:
            if tuple(unit.location_tile) in self.arrival_locations:
                self.arrived = True

        if not map.team2:
            return 'team1victory'
        elif not map.team1 or self.arrived:
            return 'team2victory'
        else:
            return False

    def report(self, map):
        """
        # Function name: report
        # Purpose: Reports the progress of the player and enemy
        # Inputs: Map - the map to check within
        # Outputs: player_status, enemy_status - strings describing the progress the player and enemy have made
        """

        player_status = self.target.name+" HP: "+str(self.target.HP)+"/"+str(self.target.maxHP)

        enemy_status = "Advance to "+self.location_name+"; Player Units Remaining: "+str(len(map.team1))

        return player_status, enemy_status


class TurnCapture(Objective):

    def __init__(self, turn_limit, ssp_count, desc):
        """
        # Function name: __init__
        # Purpose: Creates a capture magic sources objective
        # Inputs:
        #            ssp_count - Number of spirit source points that need to be captured
        #            desc - objective description
        """

        Objective.__init__(self, desc)
        self.turn_limit = turn_limit
        self.ssp_count = ssp_count
        self.goal = "Capture "+str(self.ssp_count)+" Spirit Source Points!"
        self.enemy_goal = "All player units defeated!"

    def check(self, map):
        """
        # Function name: check
        # Purpose: Checks if a victory condition has been met
        # Inputs: Map - the map to check within
        #
        #   Conditions for Player Victory - X number of SSPs are under player control
        #   Condition for Enemy Victory - Defeat player team
        """

        map.update_ssps()
        counter = 0

        # Checks the number of points that have been captured
        for ssp in map.all_ssps.values():
            if ssp.capture_state == 1:
                counter += 1

        # Checks if the number of ssps capture is >= minimum count to win
        if counter >= self.ssp_count:
            return 'team1victory'
        elif map.team1 == [] or  map.turn_count == self.turn_limit+1:
            return 'team2victory'
        else:
            return False

    def report(self, map):

        """
        # Function name: report
        # Purpose: Reports the progress of the player and enemy
        # Inputs: Map - the map to check within
        # Outputs: player_status, enemy_status - strings describing the progress the player and enemy have made
        """

        counter = 0

        # Checks the number of points that have been captured
        for ssp in map.all_ssps.values():
            if ssp.capture_state == 1:
                counter += 1

        player_status = "Spirit Source Points: "+str(counter)+"/"+str(self.ssp_count)
        enemy_status = "Player Units Remaining: "+str(len(map.team1))

        return player_status, enemy_status
