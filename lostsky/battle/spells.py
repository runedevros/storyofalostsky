# Spell class

from random import randint
from lostsky.battle.trait import Trait

class Spell(object):
    def __init__(self, nameprefix, namesuffix, attacktype, damagetype,
                 life, statmods, effect, shield, spellrange, affinity, spell_rank,
                 counterattack, unlock, sc_cost, minrange=1):

        """
        # Function Name: __init__
        # Purpose: Initializes a spell
        # Inputs: nameprefix = First part of a spell name "Love Sign"
        #         namesuffix = Second part of a spell name "Master Spark"
        #         attacktype = 'magical' or 'physical'
        #         life = how many times a spell can be used
        #         statmods = strength, defense, magic, magicdefense, agility, accuracy, critical modifiers
        #         damage = Base damage rate
        #         shield = Base shielding rate
        #         spellrange = how far the spell can be cast
        #         affinity = elemental, spiritual, nature, or force
        #         counterattack = True if the spell can be used to counter, False if it cannot
        """


        self.name = nameprefix + " - " + namesuffix    # E.G. "Hax Sign - Burn Everything"
        self.nameprefix = nameprefix
        self.namesuffix = namesuffix
        self.desc = ""                    # Description
        self.attacktype = attacktype     # Physical or Magical
        self.damagetype = damagetype     # Physical or Magical
        self.lives = life                # How many times a spell can be used
        self.livesleft = self.lives      # in one battle.

        # Stat mods
        self.strmod = statmods[0]
        self.defmod = statmods[1]
        self.magmod = statmods[2]
        self.mdefmod = statmods[3]
        self.aglmod = statmods[4]
        self.accmod = statmods[5]
        self.effect = effect
        self.shield = shield
        self.critmod = statmods[6]

        # Spell's range
        self.minrange = minrange
        self.spellrange = spellrange
        self.validattacks = []

        # Spell properties
        self.affinity = affinity
        self.spell_rank = spell_rank
        self.counterattack = counterattack

        # Stores the location of the spell's icon images
        # Attack Type
        if self.attacktype == 'physical':
            self.a_type_small = (15, 0, 15, 15)
            self.a_type_big = (20, 0, 20, 20)
        else:
            self.a_type_small = (30, 0, 15, 15)
            self.a_type_big = (40, 0, 20, 20)
        # Damage Type
        if self.type in ('healing', 'healingitem'):
            self.d_type_small = (180, 0, 15, 15)
            self.d_type_big = (240, 0, 20, 20)
        elif self.damagetype == 'physical':
            self.d_type_small = (150, 0, 15, 15)
            self.d_type_big = (200, 0, 20, 20)
        else:
            self.d_type_small = (165, 0, 15, 15)
            self.d_type_big = (220, 0, 20, 20)

        # SPELL TYPE
        if self.affinity == "Natural":
            self.al_type_small = (90, 0, 15, 15)
            self.al_type_big = (120, 0, 20, 20)
        elif self.affinity == "Elemental":
            self.al_type_small = (60, 0, 15, 15)
            self.al_type_big = (80, 0, 20, 20)
        elif self.affinity == "Spiritual":
            self.al_type_small = (45, 0, 15, 15)
            self.al_type_big = (60, 0, 20, 20)
        elif self.affinity == "Force":
            self.al_type_small = (75, 0, 15, 15)
            self.al_type_big = (100, 0, 20, 20)
        # Counterattack
        if self.counterattack == True:
            self.c_type_small = (0, 0, 15, 15)
            self.c_type_big = (0, 0, 20, 20)
        else:
            self.c_type_small = (120, 0, 15, 15)
            self.c_type_big = (160, 0, 20, 20)

        # Spell's Minimum Unlock Stat
        self.unlock = unlock

        # Spell's SC Cost
        self.sc_cost = sc_cost

        # Spell Restrictions
        self.restrictions = {'class': ['All'],
                            'character': ['All'],
                            'level': 0}

    def check_restrictions(self, unit):
        """
        # Function name: check restrictions
        # Purpose: Checks the unit against the spell's restrictions
        # Inputs: Unit - unit to check against
        # Output: True if unit can equip, False if not
        """

        can_equip = True

        # Check class restrictions
        if self.restrictions['class'] != ['All']:
            can_equip = can_equip and unit.unitclass in self.restrictions['class']

        # Check character restrictions
        if self.restrictions['character'] != ['All']:
            can_equip = can_equip and unit.name in self.restrictions['character']

        # Checks level restrictions
        can_equip = can_equip and unit.level >= self.restrictions['level']

        return can_equip


    def get_attack_range(self, unit):
        """
        # Function Name: get_attack_range
        # Purpose: generates the valid range of attack tiles for a spell
        """

        self.validattacks = []

        minimum_range = self.minrange
        maximum_range = self.spellrange

        # Checks if unit has range extending trait properties
        if unit.has_trait_property('Extend Min Range'):
            minimum_range += 1
        if unit.has_trait_property('Extend Max Range'):
            maximum_range += 1
        if unit.has_trait_property('Reduce Max Range'):
            maximum_range -= 1
            if maximum_range < 1:
                maximum_range = 1



        # generates the valid moveset for 1st quadrant
        # General Pattern:
        #
        #  X123
        #  123
        #  23
        #  3
        #

        for diagonal_row_num in xrange(minimum_range, maximum_range + 1):
            for index in xrange(0, diagonal_row_num + 1):
                self.validattacks.append((diagonal_row_num-index, index))

        # generates the valid moveset for 2nd, 3rd, 4th quadrants
        for coord in list(self.validattacks):

            self.validattacks.append((-coord[0], coord[1]))
            self.validattacks.append((-coord[0], -coord[1]))
            self.validattacks.append((coord[0], -coord[1]))

        # Removes duplicates
        self.validattacks = list(set(self.validattacks))



class AttackSpell(Spell):

    def __init__(self, nameprefix, namesuffix, attacktype, damagetype, life,
                  statmods, effect, shield, spellrange, affinity, spell_rank,
                  counterattack, unlock, sc_cost, minrange=1,
                  consumable = True, status_effects = None):

        """
        # Function Name: __init__
        # Purpose: Initializes a spell
        # Inputs: nameprefix = First part of a spell name "Love Sign"
        #         namesuffix = Second part of a spell name "Master Spark"
        #         attacktype = 'magical' or 'physical'
        #         life = how many times a spell can be used
        #         statmods = strength, defense, magic, magicdefense, agility, accuracy, critical modifiers
        #         damage = Base damage rate
        #         shield = Base shielding rate
        #         spellrange = how far the spell can be cast
        #         affinity = magical, spiritual, life, or none
        #         counterattack = True if the spell can be used to counter, False if it cannot
        #         unlocks = Minimum Spirit needed to use the spell
        #         minrange = minimum range
        #         consumable = True if spell does not recharge at end of battle, False if it does
        #         status_effects = list of status effects this spell inflict format: {'effect':% effective}
        """
        self.type = 'attack'
        self.consumable = consumable  # Consumable flag / Is a Spellcard if not consumable
        if status_effects:
            self.status_effects = status_effects
        else:
            self.status_effects = {}
        Spell.__init__(self, nameprefix, namesuffix, attacktype, damagetype, life,
                       statmods, effect, shield, spellrange, affinity, spell_rank,
                       counterattack, unlock, sc_cost, minrange)


    def action(self, attacker, defender):
        """
        # Function Name: action
        # Purpose: executes the actions of a spell
        # Inputs: attacker = person using this spell
        #         defender = target of attack
        """

        # Gets the battle event action
        effect, counterdamage, critical, countercrit, sc_cost_user, sc_cost_target = attacker.map.engine.battle_event_system.battle_event(attacker, defender)

        # Runs the attacker's EXP function
        attacker_exp_delta, attacker_level_up = attacker.experience(defender, effect)

        # Runs the attacker's Spirit function
        attacker_spirit_delta , defender_spirit_delta  = attacker.battle_spirit(defender, effect, critical)

        defender_exp_delta = 0
        defender_level_up = False
        if counterdamage != 'n/a':
            # Runs the defender's EXP function
            defender_exp_delta, defender_level_up = defender.experience(attacker, counterdamage)

            # Runs the defenders's Spirit function
            spirit_enemy_counter, spirit_self_counter = defender.battle_spirit(attacker, counterdamage, countercrit)
            attacker_spirit_delta += spirit_self_counter
            defender_spirit_delta += spirit_enemy_counter

        # If a unit is defeated, remove it from the map
        if attacker.alive == False:

            # Shows random one of unit's death quote if available
            if attacker.deathquote:
                rand_num = randint(0, len(attacker.deathquote)-1)
                attacker.map.say(attacker.deathquote[rand_num]['line'], attacker.name, attacker.deathquote[rand_num]['portrait'])

            attacker.map.kill(attacker, render_fadeout = True)
        if defender.alive == False:

            # Shows random one of unit's death quote if available
            if defender.deathquote:
                rand_num = randint(0, len(defender.deathquote)-1)
                defender.map.say(defender.deathquote[rand_num]['line'], defender.name, defender.deathquote[rand_num]['portrait'])

            attacker.map.kill(defender, render_fadeout = True)

        attacker.plot_results(defender, attacker_exp_delta, attacker_level_up, defender_exp_delta, defender_level_up, attacker_spirit_delta , defender_spirit_delta, sc_cost_user, sc_cost_target )

    def get_effect(self, user, target):
        """
        # Function Name: get_effect
        # Purpose: Executes an attack
        # Inputs: user = person using this spell
        #         target = target of attack
        """

        # Sums the trait bonuses for support and active
        user_trait_mods = user.compute_trait_stats_bonus()
        target_trait_mods = target.compute_trait_stats_bonus()

        # Gets the hit/miss threshold
        targetthreshold = user.compute_threshold(target)
        # Gets the crit threshold
        critthreshold = user.compute_crit_threshold(target)

        # Roll for attack: Generate random integer between 0, 100
        attackroll = randint(0, 100)

        # Rolls for critical hit
        critroll = randint(0, 100)

        # Initializes damage to be 0 and defaults critical to false
        damage = 0
        critical = False

        # If the attack roll is over the defender's threshold, it is considered a hit
        if attackroll >= targetthreshold:

            print user.name, ' hits', target.name

            # Gets the damage value
            damage = user.compute_damage(target)


            # Sets damage to 1 if damage is negative or 0
            if damage <= 0:
                damage = 1

            # If the attack roll is below the critical threshold, it is considered a critical hit and damage is multiplied 1.5
            if critroll <= critthreshold:
                print "Critical hit!"
                damage = int(damage*1.5)
                critical = True

            if critroll <= critthreshold and user.has_trait_property('Critical Conversion') and target.chartype != 'boss':
                print "Invitation!"
                damage = target.maxHP
                critical = True

            print user.name, 'does %4.0f damage!' % damage


        # If the damage done is 0, the attacker missed
        if damage == 0:
            print 'Miss!'
            damage = 'miss'

        return damage, critical

    def give_status_effect(self, user, target):
        """
        # Function Name: status_effect
        # Purpose: Executes an attack
        # Inputs: user = person using this spell
        #         target = target of attack
        """
        for status_effect_name in user.spell_actions[user.equipped].status_effects.keys():
            if status_effect_name not in target.status.keys():
                se_roll = randint(0, 100)

                status_effect_type = user.map.engine.status_effects_catalog[status_effect_name].type

                base_target = user.spell_actions[user.equipped].status_effects[status_effect_name]

                # Increased Resistance Trait
                if (target.has_trait_property('Resist Magical Status') and status_effect_type == "Magical" or
                    (target.has_trait_property('Resist Physical Status') and status_effect_type == "Physical")):
                    required_roll = base_target/4
                else:
                    required_roll = base_target

                if se_roll <= required_roll:
                    target.give_status(status_effect_name)
                    print "%s has given %s the status effect %s" % (user.name, target.name, status_effect_name)
            else:
                print "%s already has the status effect %s" % (target.name, status_effect_name)


    def get_attack_range(self, unit):
        """
        # Function Name: get_attack_range
        # Purpose: generates the valid range of attack tiles for a spell
        """

        self.validattacks = []

        minimum_range = self.minrange
        maximum_range = self.spellrange

        # Checks if unit has range extending trait properties
        if unit.has_trait_property('Extend Atk Min Range'):
            minimum_range += 1
        if unit.has_trait_property('Extend Atk Max Range'):
            maximum_range += 1
        if unit.has_trait_property('Reduce Atk Max Range'):
            maximum_range -= 1
            if maximum_range < 1:
                maximum_range = 1



        # generates the valid moveset for 1st quadrant
        # General Pattern:
        #
        #  X123
        #  123
        #  23
        #  3
        #

        for diagonal_row_num in xrange(minimum_range, maximum_range + 1):
            for index in xrange(0, diagonal_row_num + 1):
                self.validattacks.append((diagonal_row_num-index, index))

        # generates the valid moveset for 2nd, 3rd, 4th quadrants
        for coord in list(self.validattacks):

            self.validattacks.append((-coord[0], coord[1]))
            self.validattacks.append((-coord[0], -coord[1]))
            self.validattacks.append((coord[0], -coord[1]))

        # Removes duplicates
        self.validattacks = list(set(self.validattacks))

class HealingSpell(Spell):


    def __init__(self, nameprefix, namesuffix, attacktype, damagetype, life,
                 statmods, effect, shield, spellrange, affinity, spell_rank,
                 unlock , sc_cost, fullres=False, minrange=1, status_effects=None, consumable=True):

        """
        # Function Name: __init__
        # Purpose: Initializes a spell
        # Inputs: nameprefix = First part of a spell name "Love Sign"
        #         namesuffix = Second part of a spell name "Master Spark"
        #         attacktype = 'magical' or 'physical'
        #         life = how many times a spell can be used
        #         statmods = strength, defense, magic, magicdefense, agility, accuracy, critical modifiers
        #         effect = Base effect rate
        #         shield = Base shielding rate
        #         spellrange = how far the spell can be cast
        #         affinity = magical, spiritual, life, or none
        #         fullres = True if spell completely heals a target for higher level healing spells
        #         status_effects = List of status effects this spell heals
        """
        self.type = 'healing'
        self.consumable = consumable  # Consumable flag
        Spell.__init__(self,
                       nameprefix,
                       namesuffix,
                       attacktype,
                       damagetype,
                       life,
                       statmods,
                       effect,
                       shield,
                       spellrange,
                       affinity,
                       spell_rank,
                       False,
                       unlock,
                       sc_cost,
                       minrange)
        # If fullres is true, this spell is triggered to completely heal a target upon use.
        self.fullres = fullres
        if status_effects:
            self.status_effects = status_effects
        else:
            self.status_effects = []

    def action(self, user, target):
        """
        # Function Name: action
        # Purpose: executes the actions of a spell
        # Inputs: user = person using this spell
        #         target = target of spell
        """

        if target != user:
            # Gets the battle event action
            effect, counterdamage, critical, countercrit, sc_cost_user, sc_cost_target = user.map.engine.battle_event_system.battle_event(user, target)
        else:
            # If the target is herself, renders the animation (if enabled) on the map
            effect, sc_cost_user = user.map_heal(user, self.name)

        # Cures status effects
        #   Unit can cure the status effect
        #   Unit has a trait property that cures status effects with the use of a healing spell
        for status_effect in target.status.keys():
            if status_effect in self.status_effects or user.has_trait_property("Cure %s"%status_effect):
                target.remove_status(status_effect)
                print "%s has been cured of %s" % (target.name, status_effect)

        user_exp_delta, user_level_up = user.experience(target, effect)
        user_spirit_delta, target_spirit_delta = user.battle_spirit(target, effect, False)

        user.plot_results(target, user_exp_delta, user_level_up, 0, False, user_spirit_delta, 0, sc_cost_user, 0)


    def get_effect(self, user, target):
        """
        # Function Name: get_effect
        # Purpose: computes the effect of the spell
        # Inputs: target - the target of the spell
        """

        if self.fullres == True:
            recovery = target.maxHP
        else:
            # Recovery = (Users's MAG + Attacker's STRmod/MAGmod)*Attacker's spell's Base Effect
            recovery = (user.MAG + self.magmod)*self.effect

            if user.has_trait_property("Healing+ Lv.3"):
                recovery += recovery*0.30
            elif user.has_trait_property("Healing+ Lv.2"):
                recovery += recovery*0.20
            elif user.has_trait_property("Healing+ Lv.1"):
                recovery += recovery*0.10

        recovery = int(recovery)

        if target.HP + recovery > target.maxHP:
            recovery = target.maxHP - target.HP

        return recovery


    def get_attack_range(self, unit):
        """
        # Function Name: get_attack_range
        # Purpose: generates the valid range of attack tiles for a spell
        """

        self.validattacks = []

        minimum_range = self.minrange
        maximum_range = self.spellrange

        # Checks if unit has range extending trait properties
        if unit.has_trait_property('Extend Heal Min Range'):
            minimum_range += 1
        if unit.has_trait_property('Extend Heal Max Range'):
            maximum_range += 1
        if unit.has_trait_property('Reduce Heal Max Range'):
            maximum_range -= 1
            if maximum_range < 1:
                maximum_range = 1



        # generates the valid moveset for 1st quadrant
        # General Pattern:
        #
        #  X123
        #  123
        #  23
        #  3
        #

        for diagonal_row_num in xrange(minimum_range, maximum_range + 1):
            for index in xrange(0, diagonal_row_num + 1):
                self.validattacks.append((diagonal_row_num-index, index))

        # generates the valid moveset for 2nd, 3rd, 4th quadrants
        for coord in list(self.validattacks):

            self.validattacks.append((-coord[0], coord[1]))
            self.validattacks.append((-coord[0], -coord[1]))
            self.validattacks.append((coord[0], -coord[1]))

        # Removes duplicates
        self.validattacks = list(set(self.validattacks))


class SupportSpell(Spell):
    def __init__(self, nameprefix, namesuffix, attacktype, damagetype, life,
                 statmods, effect, shield, spellrange, affinity, spell_rank,
                 unlock , sc_cost, minrange=1, status_effects=None, consumable=True):

        """
        # Function Name: __init__
        # Purpose: Initializes a spell
        # Inputs: nameprefix = First part of a spell name "Love Sign"
        #         namesuffix = Second part of a spell name "Master Spark"
        #         attacktype = 'magical' or 'physical'
        #         life = how many times a spell can be used
        #         statmods = strength, defense, magic, magicdefense, agility, accuracy, critical modifiers
        #         effect = Base effect rate
        #         shield = Base shielding rate
        #         spellrange = how far the spell can be cast
        #         affinity = magical, spiritual, life, or none
        #         fullres = True if spell completely heals a target for higher level healing spells
        #         status_effects = List of status effects this spell heals
        """
        self.type = 'support'
        self.consumable = consumable  # Consumable flag
        Spell.__init__(self,
                       nameprefix,
                       namesuffix,
                       attacktype,
                       damagetype,
                       life,
                       statmods,
                       effect,
                       shield,
                       spellrange,
                       affinity,
                       spell_rank,
                       False,
                       unlock,
                       sc_cost,
                       minrange)

        if status_effects:
            self.status_effects = status_effects
        else:
            self.status_effects = []

    def action(self, user, target):
        """
        # Function Name: action
        # Purpose: executes the actions of a spell
        # Inputs: user = person using this spell
        #         target = target of spell
        """

        if target != user:
            # Gets the battle event action
            effect, counterdamage, critical, countercrit, sc_cost_user, sc_cost_target = user.map.engine.battle_event_system.battle_event(user, target)
        else:
            # If the target is herself, renders the animation (if enabled) on the map
            effect, sc_cost_user = user.map_heal(user, self.name)

        # Applies status effects
        for status_effect in self.status_effects:
            if status_effect not in target.status:
                target.give_status(status_effect)
                # If user has the trait support duration+, give an extra two turns to the target.
                if user.has_trait_property("Support Duration+"):
                    target.status[status_effect] = -2

        user_exp_delta, user_level_up = user.experience(target, effect)
        user_spirit_delta, target_spirit_delta = user.battle_spirit(target, effect, False)

        user.plot_results(target, user_exp_delta, user_level_up, 0, False, user_spirit_delta, 0, sc_cost_user, 0)

    def get_effect(self, user, target):
        """
        # Function Name: get_effect
        # Purpose: computes the effect of the spell
        # Inputs: target - the target of the spell
        """

        # Support spells do not have any healing effect
        return 0



    def get_attack_range(self, unit):
        """
        # Function Name: get_attack_range
        # Purpose: generates the valid range of attack tiles for a spell
        """

        self.validattacks = []

        minimum_range = self.minrange
        maximum_range = self.spellrange

        # Checks if unit has range extending trait properties
        if unit.has_trait_property('Extend Heal Min Range'):
            minimum_range += 1
        if unit.has_trait_property('Extend Heal Max Range'):
            maximum_range += 1
        if unit.has_trait_property('Reduce Heal Max Range'):
            maximum_range -= 1
            if maximum_range < 1:
                maximum_range = 1



        # generates the valid moveset for 1st quadrant
        # General Pattern:
        #
        #  X123
        #  123
        #  23
        #  3
        #

        for diagonal_row_num in xrange(minimum_range, maximum_range + 1):
            for index in xrange(0, diagonal_row_num + 1):
                self.validattacks.append((diagonal_row_num-index, index))

        # generates the valid moveset for 2nd, 3rd, 4th quadrants
        for coord in list(self.validattacks):

            self.validattacks.append((-coord[0], coord[1]))
            self.validattacks.append((-coord[0], -coord[1]))
            self.validattacks.append((coord[0], -coord[1]))

        # Removes duplicates
        self.validattacks = list(set(self.validattacks))




# Healing Item Class
class HealingItem(Spell):

    def __init__(self, name, life, effect_class, effect, max_range, min_range, affinity, status_effects=None):
        """
        # Function Name: __init__
        # Purpose: Initializes a spell
        # Inputs: name = Name of the spell ('peanut cheese bar')
        #         life = number of times the item can be used
        #         effect_class = 'percent' if the item recovers a certain percent of the target's max HP,
        #                       'constant' if the item recovers a constant HP value
        #         effect = effect (% HP or constant)
        #         range = how far away can the item be used
        #         affinity = item's magic system alignment
        #         bullet image = bullet image to use
        #         status_effects = status_effects to heal
        """

        self.type = 'healingitem'
        self.consumable = True # Consumable Flag
        self.effect_class = effect_class      # 'percent' for Percentage maxHP Healing / 'constant' Constant Value Healing
        if status_effects:
            self.status_effects = status_effects
        else:
            self.status_effects = []


        Spell.__init__(self, 'Item', name, 'physical', 'healing',
                       life, [0, 0, 0, 0, 0, 0, 0], effect, 1, max_range, affinity, 0, False, 0, 0, min_range)


    def action(self, user, target):
        """
        # Function Name: action
        # Purpose: executes the actions of an item
        # Inputs: user = person using this item
        #         target = target of item
        """

        # Adapt's healing spell's map-oriented healing animation
        effect, _ = user.map_heal(target, self.name)

        # Cures status effects
        for status_effect in self.status_effects:
            if status_effect in target.status:
                target.remove_status(status_effect)
                print "%s has been cured of %s" % (target.name, status_effect)

        user_exp_delta, user_level_up = user.experience(target, effect)

        # Using an item gives EXP but no spirit change
        user.plot_results(target, user_exp_delta, user_level_up, 0, False, 0, 0, 0, 0)


    def get_effect(self, user, target):

        """
        # Function Name: get_effect
        # Purpose: computes the effect of the spell
        # Inputs: target - the target of the spell
        """
        recovery = 0

        if self.effect_class == 'percent':
            recovery = int((self.effect/100)*target.maxHP)
        elif self.effect_class == 'constant':
            recovery = int(self.effect)


        # 20% increase in healing effectiveness if traits support it
        if user.has_trait_property('Healing User+'):
            recovery = int(1.2*recovery)
        if target.has_trait_property('Healing Receiver+'):
            recovery = int(1.2*recovery)

        return recovery



    def get_attack_range(self, unit):
        """
        # Function Name: get_attack_range
        # Purpose: generates the valid range of attack tiles for a spell
        """

        self.validattacks = []

        minimum_range = self.minrange
        maximum_range = self.spellrange

        # Checks if unit has range extending trait properties
        if unit.has_trait_property('Extend Heal Min Range'):
            minimum_range += 1
        if unit.has_trait_property('Extend Heal Max Range'):
            maximum_range += 1
        if unit.has_trait_property('Reduce Heal Max Range'):
            maximum_range -= 1
            if maximum_range < 1:
                maximum_range = 1



        # generates the valid moveset for 1st quadrant
        # General Pattern:
        #
        #  X123
        #  123
        #  23
        #  3
        #

        for diagonal_row_num in xrange(minimum_range, maximum_range + 1):
            for index in xrange(0, diagonal_row_num + 1):
                self.validattacks.append((diagonal_row_num-index, index))

        # generates the valid moveset for 2nd, 3rd, 4th quadrants
        for coord in list(self.validattacks):

            self.validattacks.append((-coord[0], coord[1]))
            self.validattacks.append((-coord[0], -coord[1]))
            self.validattacks.append((coord[0], -coord[1]))

        # Removes duplicates
        self.validattacks = list(set(self.validattacks))

