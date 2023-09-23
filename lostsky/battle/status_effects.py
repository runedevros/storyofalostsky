# Status Effects
from random import randint
import pygame
import os

def get_effects_catalog():

    return {'High Spirit': HighSpirit(),
 'Low Spirit': LowSpirit(),
 'Poison': Poison(),
 'Stun': Stun(),
 'Spirit Drain': SpiritDrain(),
 'Immobilize': Immobilize(),
 'Dizzy': Dizzy(),
 'Movement Down': MovementDown(),
 'Binding Seal': BindingSeal(),
 'STR Down': StrDown(),
 'DEF Down': DefDown(),
 'MAG Down': MagDown(),
 'MDEF Down': MdefDown(),
 'Illusion Veil': IllusionVeil(),
 'Tracking Shot': TrackingShot(),
 'Life Bless': LifeBless(),
 'STR Up': StrUp(),
 'MAG Up': MagUp(),
 'DEF Up': DefUp(),
 'MDEF Up': MdefUp(),
 'Spirit Recharge': SpiritRecharge(),
 'Magic Fortress': MagicFortress(),
 'Mega Offense': MegaOffense(),
 'Target': Target(),
 'Fog Veil': FogVeil(),
 'Invisible': Invisible(),
 }

# Base class for status effects
class StatusEffect(object):

    def __init__(self, name):
        self.name = name
        self.positive_status = False # Defaults to negative status effect

        # [STR, DEF, MAG, MDEF, ACC, AGL]
        self.statmods = [0, 0, 0, 0, 0, 0]

        # Bonus to unit's hit%
        self.hitmod = 0

        # Bonus to unit's crit%
        self.critmod = 0

        # Penalty against attacking unit's hit%
        self.evamod = 0

        # Bonus/Penalty to movement
        self.movemod = 0

        self.icon_position = (0,0)

        # Icon image is assigned when the engine initializes this set of status effects
        self.icon = None

    def execute_effect(self, unit):
        pass

    def check_recovery(self, unit):
        pass


class HighSpirit(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "High Spirit")

        self.type = 'Other'
        self.positive_status = True
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (7, 1)

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        # Outputs: Returns false always
        """
        return False

class LowSpirit(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "Low Spirit")

        self.type = 'Other'
        self.positive_status = False
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (7, 2)

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        # Outputs: Returns false always
        """
        return False


# Poison status effect
class Poison(StatusEffect):

    def __init__(self):

        """
        # Function Name: __init__
        # Purpose: Creates the Poison Status effect
        """

        StatusEffect.__init__(self, "Poison")
        self.type = 'Physical'
        self.show_change = True
        self.HP_change = True
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (0, 0)

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        turns = unit.status[self.name]
        roll = randint(0, 100)

        # Probability of healing: 30+10*N% where N is number of turns that have passed
        if roll <= (30+10*turns) and turns > 0:
            print "%s is naturally cured of %s" % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

    def execute_effect(self, unit):
        """
        # Function Name: Execute Effect
        # Purpose: Performs the effect of the status on a unit
        # Inputs: Unit - target unit to enact status on
        """
        # Decreases unit's HP by 15% of max HP
        # Caps damage at 50 HP / turn for high HP enemies
        hp_change = -min(50, int(unit.maxHP*0.15))
        unit.HP += hp_change

        print "%s takes %s damage from the poison" % (unit.name, str(hp_change))
        if unit.HP <= 0:
            unit.HP = 0
            unit.alive = False
        return hp_change

class Stun(StatusEffect):

    def __init__(self):
        """
        # Function Name: __init__
        # Purpose: Creates the Stun Status effect
        """
        StatusEffect.__init__(self, "Stun")
        self.type = 'Physical'
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (1, 0)

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        # Effect only lasts for 1 turn
        turns = unit.status[self.name]
        if turns > 0:
            print "%s is naturally cured of %s" % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

    def execute_effect(self, unit):
        """
        # Function Name: Execute Effect
        # Purpose: Performs the effect of the status on a unit
        # Inputs: Unit - target unit to enact status on
        """

        unit.turnend = True

class SpiritDrain(StatusEffect):

    def __init__(self):
        """
        # Function Name: __init__
        # Purpose: Creates the Stun Drain effect
        """

        StatusEffect.__init__(self, "Spirit Drain")
        self.type = 'Magical'
        self.show_change = True
        self.HP_change = False
        self.SC_change = True
        # Icon position in status effects icon image
        self.icon_location = (2, 0)


    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        turns = unit.status[self.name]
        roll = randint(0, 100)

        # Probability of healing: 30+10*N% where N is number of turns that have passed
        if roll <= (20+10*turns) and turns > 0:
            print "%s is naturally cured of %s" % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

    def execute_effect(self, unit):
        """
        # Function Name: Execute Effect
        # Purpose: Performs the effect of the status on a unit
        # Inputs: Unit - target unit to enact status on
        """
        # Decreases unit's HP by 50 each turn to a min of 100
        before = unit.spirit
        unit.spirit -= 50
        if unit.spirit <= 100:
            unit.spirit = 100

        unit.check_spirit_range()
        difference = unit.spirit - before
        print "%s takes %s SC damage from the spirit drain" % (unit.name, str(-difference))
        return difference



class SpiritRecharge(StatusEffect):

    def __init__(self):
        """
        # Function Name: __init__
        # Purpose: Creates the Stun Drain effect
        """

        StatusEffect.__init__(self, "Spirit Recharge")
        self.type = 'Magical'
        self.show_change = True
        self.HP_change = False
        self.SC_change = True
        # Icon position in status effects icon image
        self.icon_location = (0, 3)
        self.max_turns = 4

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """

        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

    def execute_effect(self, unit):
        """
        # Function Name: Execute Effect
        # Purpose: Performs the effect of the status on a unit
        # Inputs: Unit - target unit to enact status on
        """
        # Decreases unit's HP by 50 each turn to a min of 100
        before = unit.spirit
        unit.spirit += 50

        unit.check_spirit_range()
        difference = unit.spirit - before
        print "%s gains %s SC from spirit recharge" % (unit.name, str(difference))
        return difference


class Immobilize(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "Immobilize")
        self.type = 'Physical'
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        self.max_turns = 1
        # Icon position in status effects icon image
        self.icon_location = (4, 0)

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """

        # Immobilize lasts one turn
        turns = unit.status[self.name]
        if turns >= self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

class BindingSeal(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "Binding Seal")
        self.type = 'Magical'
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (5, 0)

        self.movemod = -1
        self.evamod = -20

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        turns = unit.status[self.name]
        roll = randint(0, 100)

        # Probability of healing: 30+10*N% where N is number of turns that have passed
        if roll <= (30+10*turns)  and turns > 0:
            print "%s is naturally cured of %s" % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False


class Dizzy(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "Dizzy")
        self.type = 'Physical'
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (6, 0)

        self.hitmod = -30

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        turns = unit.status[self.name]
        roll = randint(0, 100)

        # Probability of healing: 30+10*N% where N is number of turns that have passed
        if roll <= (30+10*turns)  and turns > 0:
            print "%s is naturally cured of %s" % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

class MovementDown(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "Movement Down")
        self.type = 'Physical'
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (5, 0)

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        turns = unit.status[self.name]
        roll = randint(0, 100)

        # Probability of healing: 30+10*N% where N is number of turns that have passed
        if roll <= (30+10*turns)  and turns > 0:
            print "%s is naturally cured of %s" % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False



class StrDown(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "STR Down")
        self.type = 'Magical'
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (0, 2)

        # Decreases STR 15%
        self.statmods = [-0.15, 0, 0, 0, 0, 0]

        self.max_turns = 3


    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """

        # Effect only lasts for 4 turn
        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

class DefDown(StatusEffect):

    def __init__(self):

        """
        Decreases damage taken from magic attacks by 10%. Applied after base dmg calculation.
        """


        StatusEffect.__init__(self, "DEF Down")
        self.type = 'Magical'
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (1, 2)

        self.statmods = [0, 0, 0, 0, 0, 0]

        self.max_turns = 3

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """

        # Effect only lasts for 4 turn
        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

class MagDown(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "MAG Down")
        self.type = 'Magical'
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (2, 2)

        # Decreases MAG by 15%
        self.statmods = [0, 0, -0.15, 0, 0, 0]

        self.max_turns = 3

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """

        # Effect only lasts for 4 turn
        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

class MdefDown(StatusEffect):

    def __init__(self):
        """
        Decreases damage taken from magic attacks by 10%. Applied after base dmg calculation.
        """

        StatusEffect.__init__(self, "MDEF Down")
        self.type = 'Magical'
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (3, 2)

        self.statmods = [0, 0, 0, 0, 0, 0]


        self.max_turns = 3

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """

        # Effect only lasts for 4 turn
        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False


####################################
# Support Status Effects
####################################

class LifeBless(StatusEffect):

    def __init__(self):

        """
        # Function Name: __init__
        # Purpose: Creates the Health Bless Status effect
        """

        StatusEffect.__init__(self, "Life Bless")
        self.type = 'Magical'
        self.positive_status = True
        self.show_change = True
        self.HP_change = True
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (7, 0)

        self.max_turns = 3

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        # Effect only lasts for 4 turn
        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

    def execute_effect(self, unit):
        """
        # Function Name: Execute Effect
        # Purpose: Performs the effect of the status on a unit
        # Inputs: Unit - target unit to enact status on
        """
        if unit.HP < unit.maxHP:
            # Restores unit's HP by 15% of max HP
            hp_change = +int(unit.maxHP*0.15)
            unit.HP += hp_change

            print "%s recovers %s from Life Bless" % (unit.name, str(hp_change))
            if unit.HP >= unit.maxHP:
                unit.HP = unit.maxHP
            return hp_change
        else:
            print "%s already at full HP. Life Bless has no effect this turn." % (unit.name)
            return 0

class IllusionVeil(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "Illusion Veil")
        self.type = 'Magical'
        self.positive_status = True
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (5, 1)

        # Increase evasion by 20%
        self.evamod = 20

        self.max_turns = 3

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        # Effect only lasts for 4 turn
        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

class TrackingShot(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "Tracking Shot")
        self.type = 'Magical'
        self.positive_status = True
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (4, 1)

        # Increase hit by 20%
        self.hitmod = 20

        self.max_turns = 3

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        # Effect only lasts for 4 turn
        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

class StrUp(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "STR Up")
        self.type = 'Physical'
        self.positive_status = True
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (0, 1)

        # Increase STR by 15%
        self.statmods = [0.15, 0, 0, 0, 0, 0]

        self.max_turns = 3

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        # Effect only lasts for 4 turn
        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

class DefUp(StatusEffect):

    def __init__(self):

        """
        Decreases damage taken from physical attacks by 10%. Applied after base dmg calculation.
        """

        StatusEffect.__init__(self, "DEF Up")
        self.type = 'Physical'
        self.positive_status = True
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (1, 1)

        self.statmods = [0, 0, 0, 0, 0, 0]

        self.max_turns = 3

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        # Effect only lasts for 4 turn
        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

class MagUp(StatusEffect):

    def __init__(self):


        StatusEffect.__init__(self, "MAG Up")
        self.type = 'Magical'
        self.positive_status = True
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (2, 1)

        # Increase MAG by 15%
        self.statmods = [0, 0, 0.15, 0, 0, 0]

        self.max_turns = 3

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        # Effect only lasts for 4 turn
        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

class MdefUp(StatusEffect):

    def __init__(self):
        """
        Decreases damage taken from magic attacks by 10%. Applied after base dmg calculation.
        """

        StatusEffect.__init__(self, "MDEF Up")
        self.type = 'Magical'
        self.positive_status = True
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (3, 1)

        self.statmods = [0, 0, 0, 0, 0, 0]

        self.max_turns = 3

    def check_recovery(self, unit):
        """
        # Function Name: Check Recovery
        # Purpose: Checks if a unit has recovered from this status effect
        # Inputs: Unit - target unit to check
        """
        # Effect only lasts for 4 turn
        turns = unit.status[self.name]
        if turns > self.max_turns:
            print "%s's %s has worn off." % (unit.name, self.name)
            return True
        else:
            unit.status[self.name] += 1
            return False

class MagicFortress(StatusEffect):

    def __init__(self):
        """
        25% damage reduction in total attack damage applied after final calculation
        Grants a 25% increase to unit's magic attack stat
        """

        StatusEffect.__init__(self, 'Magic Fortress')
        self.type = 'Magical'
        self.positive_status = True
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (1, 3)

        # Increase magic attack by 25%
        self.statmods = [0, 0, 0.25, 0, 0, 0]

        self.max_turns = 1

    def check_recovery(self, unit):
        # Status effect neutralizes at the start of next turn.
        return True

class MegaOffense(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, 'Mega Offense')
        self.type = 'Magical'
        self.positive_status = True
        self.show_change = False
        self.HP_change = False
        self.SC_change = False
        # Icon position in status effects icon image
        self.icon_location = (5, 3)

        # Increase DEF/MDEF by 25%, Magic Attack by 15%
        self.statmods = [0, 0, 2, 0, 0, 0]

        self.max_turns = 1

    def check_recovery(self, unit):
        # Status effect neutralizes at the start of next turn.
        return True

class Target(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "Target")
        self.type = 'Other'
        self.positive_status = "Negative"
        self.show_change = False
        self.HP_change = False
        self.SC_change = False

        self.icon_location = (2, 3)


class FogVeil(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "Fog Veil")
        self.type = 'Other'
        self.positive_status = "Positive"
        self.show_change = False
        self.HP_change = False
        self.SC_change = False

        self.icon_location = (3, 3)


class Invisible(StatusEffect):

    def __init__(self):
        StatusEffect.__init__(self, "Invisible")
        self.type = 'Other'
        self.positive_status = "Positive"
        self.show_change = False
        self.HP_change = False
        self.SC_change = False

        self.icon_location = (4, 3)

    def check_recovery(self, unit):
        # Status effect neutralizes at the start of next turn.
        return True