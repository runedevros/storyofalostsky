# trait class

class Trait(object):

    def __init__(self, name, variation, desc):

        """
        # Function Name: __init__
        # Purpose: Creates a trait class
        # Inputs: Name = Trait's name (e.g. "Magic Attack +", "Flight"
        #         Variation = "Support", "Trait Skill", "Proximity"
        #         Desc = Short description of the Trait
        #
        #       Base Class for all traits
        """

        # Define description variables
        self.name = name
        self.variation = variation
        self.desc = desc

        # Initializes dummy modifiers for base trait class
        self.statmods = [0, 0, 0, 0, 0, 0]

        # Modify directly the hit and evade percentages
        self.hit_bonus = 0
        self.evade_bonus = 0

        # Movement modifiers (Addition and subtraction are mutually exclusive)
        self.movemod_add = 0
        self.movemod_mult = 0

        # EXPmod is multiplicative
        self.expmod = 0

        # Spirit Mod is multiplicative of total received at the end of the battle
        self.spiritmod = 0

        # Additional properties of the trait
        self.properties = []

    def turn_execute(self, user):
        """
        Things that happen once a turn. Nothing for base class.
        """
        pass

    def turn_check(self, user):
        """
        Checks whether class needs to do turn execute, if not, pass.
        """
        return False

class SupportTrait(Trait):

    def __init__(self, name, desc, statmods, hit_bonus, evade_bonus, movemod_add, movemod_mult, expmod, spiritmod, properties):

        """
        # Function Name: __init__
        # Purpose: Creates a  support trait class
        # Inputs: Name = Trait's name (e.g. "Magic Attack +", "Flight"
        #         Desc = Short description of the traitibute
        #         Statmods = A list containing 6 numbers for STR, DEF, MAG, MDEF, ACC, AGL percent bonuses
        #         Movemod_add = A modifier that adds to a units movement points. Must be a non-negative integer
        #         Movemod_mult = A multiplier modifier to a units allowed movement spots. Must be a non-negative integer
        #         Flight = If True, it grants the unit flight
        #         Expmod = A positive rational number that multiplies experience gains in battle.
        #         Spiritmod = A positive rational number that multiplies spirit gains (and losses) in battle.
        """

        Trait.__init__(self, name, 'Support', desc)

        # Base stat modifiers
        self.statmods = statmods

        # Movement modifiers (Addition and subtraction are mutually exclusive)
        self.movemod_add = movemod_add
        self.movemod_mult = movemod_mult

        self.hit_bonus = hit_bonus
        self.evade_bonus = evade_bonus

        # EXPmod is multiplicative
        self.expmod = expmod

        # Spirit Mod is multiplicative of total received at the end of the battle
        self.spiritmod = spiritmod

        # Additional properties of the trait
        self.properties = properties


    def turn_execute(self, user):

        """
        # Function Name: turn_execute
        # Purpose: Does whatever the trait is designed to do at the beginning of the turn
        # Inputs: user - The person who is using this trait
        """

        # Regeneration HP
        if ('Regen Lv.1' in self.properties or 'Regen Lv.2' in self.properties or 'Regen Lv.3' in self.properties):
            # Regen Lv.1 - 10% max HP
            if 'Regen Lv.1' in self.properties:
                recovery = int(user.maxHP*0.10)

            # Regen Lv.2 - 15% max HP
            elif 'Regen Lv.2' in self.properties:
                recovery = int(user.maxHP*0.15)

            # Regen Lv.3 - 20% max HP
            elif 'Regen Lv.3' in self.properties:
                recovery = int(user.maxHP*0.20)

            user.map_heal(user, self.name, recovery, 'orb2')
            print user.name + " regen: " + str(recovery)
        if ('Spirit Regen' in self.properties):
            user.sc_regen(self.name, 25, 600)

        # Assignment of fog veil trait
        if 'Fog Veil' in self.properties:
            print "Assigning status Fog Veil"
            if "Fog Veil" not in user.status:
                user.give_status('Fog Veil')

    def turn_check(self, user):

        """
        # Function Name: turn_execute
        # Purpose: Checks if the trait is needed to be executed on this turn
        # Inputs: user - The person who is using this trait
        # Outputs: True if trait needs to be executed, False if trait does not need to be executed
        """

        if ('Regen Lv.1' in self.properties
            or 'Regen Lv.2' in self.properties
            or 'Regen Lv.3' in self.properties) and user.HP < user.maxHP:

            return True
        elif ('Spirit Regen' in self.properties) and user.spirit < 600:
            return True
        elif 'Fog Veil' in self.properties and 'Fog Veil' not in user.status.keys():
            return True
        else:
            return False



class TraitSkill(Trait):

    def __init__(self, name, desc):
        """
        Initializes a Trait Skill

        Trait skills have a matching skill defined in trait_skills.py to the trait name
        """

        Trait.__init__(self, name, 'Trait Skill', desc)

class ProximityTrait(Trait):

    def __init__(self, name, desc, team, range, emit_mods, emit_hit_bonus, emit_evade_bonus, emit_targets,
                 receive_mods, receive_hit_bonus, receive_evade_bonus, receive_sources):

        """
        Initializes a Proximity Trait

        # Inputs: name = Trait's name (e.g. "Magic Attack +", "Flight"
        #         desc = Short description of the trait
        #         team = "ally" or "enemy"
        #         range = range of effectiveness for proximity trait
        #         emit_mods = stats to modify other units with
        #         emit_targets = list of targets this trait affects. Empty list to affect entire allied team
        #         receive_mods = stats to modify self with
        #         receive_sources = List of targets this trait receives from. Leave empty to receive traits near any
        #               allied or enemy unit.
        """
        Trait.__init__(self, name, "Proximity", desc)

        self.team = team
        self.range = range
        self.emit_mods = emit_mods
        self.emit_hit_bonus = emit_hit_bonus
        self.emit_evade_bonus = emit_evade_bonus

        self.receive_mods = receive_mods
        self.receive_hit_bonus = receive_hit_bonus
        self.receive_evade_bonus = receive_evade_bonus

        self.emit_targets = emit_targets
        self.receive_sources = receive_sources
