'''
Created on May 19, 2010

@author: Fawkes
'''
import animations
import pygame
from pygame.locals import *
from random import randint
from lostsky.bullet_scripts import catalog
from sys import exit
from lostsky.core.utils import get_ui_panel
from lostsky.core.colors import panel_color, border_color, dmg_color, healing_color

class BattleEventSystem(object):
    '''
    Battle System - Main class to handle battle event logic between two units.
    '''

    def __init__(self, engine):
        '''
        Function name: __init__
        Purpose: Sets up the battle system
        '''
        self.engine = engine
        self.bg_surface = pygame.Surface(engine.surface.get_size())
        self.spell_anim_catalog = catalog.get_catalog()
        self.revive_anim = self.spell_anim_catalog['special_revive'](self.engine.surface, self.bg_surface)
        self.barrier_anim = self.spell_anim_catalog['special_barrier'](self.engine.surface, self.bg_surface)

        self.meter_panel = get_ui_panel((40, 35), border_color, panel_color)

        self.damage_color = (250, 40, 40)
        self.heal_color = (40, 250, 40)
        self.empty_color = (100, 100, 50)

    def battle_event(self, lhs_unit, rhs_unit, script=None, double_attack=False):
        '''
        function name: Battle Event:
        Purpose:    Runs a single battle event between the LHS_unit and the RHS_unit.
                    If a script is provided, follows the pre-scripted battle event
        Inputs: lhs_unit, rhs_unit - participants in the battle
                script - a dictionary of the form {lhs_hit:T/F ,
                                                   lhs_crit:T/F,
                                                    rhs_hit: T/F,
                                                     rhs_crit:T/F}
        Outputs: lhs_effect, rhs_effect - HP change caused by unit actions
                 lhs_crit, rhs_crit - Critical hit event T/F

        '''

        # initializes a fresh sprite group
        self.chara_sprites = pygame.sprite.RenderUpdates()

        # Initialize the animation system
        if self.engine.options.battle_anim:

            if lhs_unit.animation_enable:
                lhs_anim = animations.CharaAnimData(lhs_unit.anim_frames, rhs=False)
            else:
                lhs_anim = animations.CharaAnimPlaceholder(lhs_unit, rhs=False)
            self.chara_sprites.add(lhs_anim)

            if rhs_unit.animation_enable:
                rhs_anim = animations.CharaAnimData(rhs_unit.anim_frames, rhs=True)
            else:
                rhs_anim = animations.CharaAnimPlaceholder(rhs_unit, rhs=True)
            self.chara_sprites.add(rhs_anim)
        else:
            lhs_anim = None
            rhs_anim = None

        if rhs_unit.spell_actions[rhs_unit.equipped] and hasattr(rhs_unit.spell_actions[rhs_unit.equipped], 'animation'):
            anim_name = rhs_unit.spell_actions[rhs_unit.equipped].animation
            if anim_name not in self.spell_anim_catalog:
                #default to fireball animation
                rhs_spell_anim = self.spell_anim_catalog['all_fireball'](self.engine.surface, self.bg_surface)
            else:
                rhs_spell_anim = self.spell_anim_catalog[anim_name](self.engine.surface, self.bg_surface)
        else:
            rhs_spell_anim = None

        if lhs_unit.spell_actions[lhs_unit.equipped] and hasattr(lhs_unit.spell_actions[lhs_unit.equipped], 'animation'):
            anim_name = lhs_unit.spell_actions[lhs_unit.equipped].animation
            if anim_name not in self.spell_anim_catalog:
                #default to fireball animation
                lhs_spell_anim = self.spell_anim_catalog['all_fireball'](self.engine.surface, self.bg_surface)
            else:
                lhs_spell_anim = self.spell_anim_catalog[anim_name](self.engine.surface, self.bg_surface)
        else:
            lhs_spell_anim = None

        text_first_strike = self.engine.render_outlined_text("First Strike!", self.engine.cfont, (255, 0, 0), (255, 255, 255))



        # RHS first strike case:
        if rhs_unit.has_trait_property('First Strike') and lhs_unit.spell_actions[lhs_unit.equipped].type == "attack":

            # If a unit has the trait property "First Strike" it initiates action when attacked
            rhs_action, rhs_effect, rhs_crit, sc_cost_rhs = self.rhs_action_phase(lhs_unit, rhs_unit, script, lhs_anim, rhs_anim, rhs_spell_anim)

            # If LHS unit can still act, proceed with unit's action
            if lhs_unit.can_counterattack(rhs_unit):
                lhs_action = True
                lhs_effect, lhs_crit, sc_cost_lhs = self.lhs_action_phase(lhs_unit, rhs_unit, script, lhs_anim, lhs_spell_anim, rhs_anim)
            else:
                lhs_action = False
                lhs_effect = 0
                lhs_crit = 0
                sc_cost_lhs = 0

        else:
            lhs_action = True
            lhs_effect, lhs_crit, sc_cost_lhs = self.lhs_action_phase(lhs_unit, rhs_unit, script, lhs_anim, lhs_spell_anim, rhs_anim)
            rhs_action, rhs_effect, rhs_crit, sc_cost_rhs = self.rhs_action_phase(lhs_unit, rhs_unit, script, lhs_anim, rhs_anim, rhs_spell_anim)

        self.post_battle_event(lhs_unit, rhs_unit, lhs_action, rhs_action)

        # Return battle results
        return lhs_effect, rhs_effect, lhs_crit, rhs_crit, sc_cost_lhs, sc_cost_rhs

    def lhs_action_phase(self, lhs_unit, rhs_unit, script, lhs_anim, lhs_spell_anim, rhs_anim):

        # Calculate LHS effect
        if script:
            lhs_effect, lhs_crit = self.get_battle_effects(lhs_unit, rhs_unit, True, script['lhs_hit'], script['lhs_crit'])
        else:
            lhs_effect, lhs_crit = self.get_battle_effects(lhs_unit, rhs_unit, False)

        print lhs_unit.name, ' uses ', lhs_unit.spell_actions[lhs_unit.equipped].name, ' on ', rhs_unit.name

        text_lhs_effect = self.get_text_effect(lhs_unit, lhs_effect)

        # Draw LHS's action
        if self.engine.options.battle_anim:
            self.draw_idle_delay(lhs_unit, rhs_unit, lhs_anim, rhs_anim)
            self.draw_lhs_action(lhs_unit, rhs_unit, lhs_anim, rhs_anim)
            self.draw_lhs_spell(lhs_unit, rhs_unit, lhs_anim, rhs_anim, lhs_spell_anim)
            if lhs_effect != 'miss' and lhs_unit.spell_actions[lhs_unit.equipped].type == 'attack':
                if lhs_crit:
                    self.engine.sfx_system.sound_catalog['crit'].play()
                else:
                    self.engine.sfx_system.sound_catalog['hit'].play()
            elif (lhs_unit.spell_actions[lhs_unit.equipped].type == 'healing' or
                  lhs_unit.spell_actions[lhs_unit.equipped].type == 'support'):
                self.engine.sfx_system.sound_catalog['heal'].play()
            else:
                self.engine.sfx_system.sound_catalog['miss'].play()
        else:
            self.draw_map_delay(lhs_unit, rhs_unit)

        # Apply battle effects
        rhs_hp_before = rhs_unit.HP
        revive_anim = self.apply_battle_effects(lhs_unit, rhs_unit, lhs_effect, lhs_crit)

        rhs_hp_after = rhs_unit.HP

        # Draw effect of LHS's action
        if self.engine.options.battle_anim:

            if not revive_anim:
                # standard attack or healing actions
                if lhs_effect != 0:
                    self.draw_lhs_effect(lhs_unit, rhs_unit, lhs_anim, rhs_anim, text_lhs_effect, rhs_hp_before, rhs_hp_after)

                # Case of healing spells that don't cure HP or for support spells
                else:

                    pass

            else:
                # A revive action has been triggered.
                rhs_unit.HP = 0
                # Draw the HP meter going down to zero
                self.draw_lhs_effect(lhs_unit, rhs_unit, lhs_anim, rhs_anim, text_lhs_effect, rhs_hp_before, 0)
                # Nifty animation for revival
                self.draw_revive_effect(lhs_unit, rhs_unit, lhs_anim, rhs_anim, 'rhs')
                # Draw the HP meter going back up to the recovered HP
                rhs_revive_effect = self.engine.render_outlined_text(str(rhs_hp_after), self.engine.battle_effect_font, healing_color, (255, 255, 255), thickness=1.1)
                rhs_unit.HP = rhs_hp_after
                self.draw_lhs_effect(lhs_unit, rhs_unit, lhs_anim, rhs_anim, rhs_revive_effect, 0, rhs_hp_after)


        else:

            if lhs_effect != 'miss' and lhs_unit.spell_actions[lhs_unit.equipped].type == 'attack':
                if lhs_crit:
                    self.engine.sfx_system.sound_catalog['crit'].play()
                else:
                    self.engine.sfx_system.sound_catalog['hit'].play()
            elif (lhs_unit.spell_actions[lhs_unit.equipped].type == 'healing' or
                  lhs_unit.spell_actions[lhs_unit.equipped].type == 'support'):
                self.engine.sfx_system.sound_catalog['heal'].play()
            else:
                self.engine.sfx_system.sound_catalog['miss'].play()

            if lhs_effect != 0:
                self.draw_map_lhs_effect(lhs_unit, rhs_unit, text_lhs_effect)
            if revive_anim:
                rhs_unit.render_hp_change(rhs_hp_before, 0)
                self.draw_map_revive_effect(lhs_unit, rhs_unit, 'rhs')
            if lhs_effect != 0:

                if revive_anim:
                    rhs_hp_before = 0

                rhs_unit.render_hp_change(rhs_hp_before, rhs_hp_after)

       # Wrap up the battle
        sc_cost_lhs =  lhs_unit.spell_actions[lhs_unit.equipped].sc_cost

        return lhs_effect, lhs_crit, sc_cost_lhs

    def rhs_action_phase(self, lhs_unit, rhs_unit, script, lhs_anim, rhs_anim, rhs_spell_anim):
        """
        Function name: RHS action
        Purpose: RHS unit's action phase. Typically counterattack action

        Inputs: lhs_unit, rhs_unit - participants in the battle
                script - a dictionary of the form {lhs_hit:T/F ,
                                                   lhs_crit:T/F,
                                                    rhs_hit: T/F,
                                                     rhs_crit:T/F}

                lhs_anim, rhs_anim - animation data for participants

        """

        # Case: RHS unit counterattacks
        if lhs_unit.spell_actions[lhs_unit.equipped].type == "attack" and rhs_unit.can_counterattack(lhs_unit):

            rhs_action = True

            # Calculate RHS effect
            if script:
                rhs_effect, rhs_crit = self.get_battle_effects(rhs_unit, lhs_unit, True, script['rhs_hit'], script['rhs_crit'])
            else:
                rhs_effect, rhs_crit = self.get_battle_effects(rhs_unit, lhs_unit, False)

            print rhs_unit.name, ' uses ', rhs_unit.spell_actions[rhs_unit.equipped].name, ' on ', lhs_unit.name

            text_rhs_effect = self.get_text_effect(rhs_unit, rhs_effect)

            # Draw RHS's action
            if self.engine.options.battle_anim:
                self.draw_idle_delay(lhs_unit, rhs_unit, lhs_anim, rhs_anim)
                self.draw_rhs_action(lhs_unit, rhs_unit, lhs_anim, rhs_anim)
                self.draw_rhs_spell(lhs_unit, rhs_unit, lhs_anim, rhs_anim, rhs_spell_anim)
                if rhs_effect != 'miss' and rhs_unit.spell_actions[rhs_unit.equipped].type == 'attack':
                    if rhs_crit:
                        self.engine.sfx_system.sound_catalog['crit'].play()
                    else:
                        self.engine.sfx_system.sound_catalog['hit'].play()
                elif (rhs_unit.spell_actions[rhs_unit.equipped].type == 'healing' or
                      rhs_unit.spell_actions[rhs_unit.equipped].type == 'support'):
                    self.engine.sfx_system.sound_catalog['heal'].play()
                else:
                    self.engine.sfx_system.sound_catalog['miss'].play()
            else:
                self.draw_map_delay(lhs_unit, rhs_unit)

            # Apply RHS unit's battle effects to LHS unit
            lhs_hp_before = lhs_unit.HP

            revive_anim = self.apply_battle_effects(rhs_unit, lhs_unit, rhs_effect, rhs_crit)

            lhs_hp_after = lhs_unit.HP

            # Draw the resulting effect
            if self.engine.options.battle_anim:


                if not revive_anim:
                    self.draw_rhs_effect(lhs_unit, rhs_unit, lhs_anim, rhs_anim, text_rhs_effect, lhs_hp_before, lhs_hp_after)

                else:
                    # A revive action has been triggered.
                    lhs_unit.HP = 0
                    self.draw_rhs_effect(lhs_unit, rhs_unit, lhs_anim, rhs_anim, text_rhs_effect, lhs_hp_before, 0)

                    # Nifty animation for revival
                    self.draw_revive_effect(lhs_unit, rhs_unit, lhs_anim, rhs_anim, 'lhs')
                    lhs_unit.HP = lhs_hp_after
                    # Draw the HP meter going back up to the recovered HP
                    lhs_revive_effect = self.engine.render_outlined_text(str(lhs_hp_after), self.engine.battle_effect_font,  healing_color, (255, 255, 255), thickness=1.1)
                    self.draw_rhs_effect(lhs_unit, rhs_unit, lhs_anim, rhs_anim, lhs_revive_effect, 0, lhs_hp_after)

                    self.engine.pause(0.25)


            else:

                if rhs_effect != 'miss' and rhs_unit.spell_actions[rhs_unit.equipped].type == 'attack':
                    if rhs_crit:
                        self.engine.sfx_system.sound_catalog['crit'].play()
                    else:
                        self.engine.sfx_system.sound_catalog['hit'].play()
                elif (rhs_unit.spell_actions[rhs_unit.equipped].type == 'healing' or
                      rhs_unit.spell_actions[rhs_unit.equipped].type == 'support'):
                    self.engine.sfx_system.sound_catalog['heal'].play()
                else:
                    self.engine.sfx_system.sound_catalog['miss'].play()

                if rhs_effect != 0:
                    self.draw_map_rhs_effect(lhs_unit, rhs_unit, text_rhs_effect)
                if revive_anim:
                    lhs_unit.render_hp_change(lhs_hp_before, 0)
                    self.draw_map_revive_effect(lhs_unit, rhs_unit, 'lhs')
                if rhs_effect != 0:
                    if revive_anim:
                        lhs_hp_before = 0
                    lhs_unit.render_hp_change(lhs_hp_before, lhs_hp_after)

            sc_cost_rhs = rhs_unit.spell_actions[rhs_unit.equipped].sc_cost

        else:
            rhs_action = False
            rhs_crit = False
            rhs_effect = 'n/a'
            sc_cost_rhs = 0

        return rhs_action,  rhs_effect, rhs_crit, sc_cost_rhs

    def get_battle_effects(self, acting_unit, target, scripted, hit=None, crit=None):

        """
        # Fuction name: get_battle_effects
        # Purpose: Computes the damage stats of the battle of the battle
        # Inputs: lhs_unit, rhs_unit
        #         script - scripted events dictionary corresponding to {lhs_hit:T/F , lhs_crit:T/F, rhs_hit: T/F, rhs_crit:T/F}
        # Outputs:
        #   effect - Damage inflicted or HP healed
        #   critical - True if a critical hit is inflicted
        #   side - RHS/LHS for attacker and defender
        """

        if acting_unit.spell_actions[acting_unit.equipped].type == 'attack':

            # Case for scripted actions (only affects offensive actions / counterattacks)
            if scripted and hit:
                effect = acting_unit.compute_damage(target)
                if crit:
                    critical = True
                    effect = int(effect*1.5)
                else:
                    critical = False
            elif scripted and not hit:
                effect, critical = ['miss', False]
            else:
                effect, critical = acting_unit.spell_actions[acting_unit.equipped].get_effect(acting_unit, target)

        elif acting_unit.spell_actions[acting_unit.equipped].type in ('healing', 'support'):
            effect = acting_unit.spell_actions[acting_unit.equipped].get_effect(acting_unit, target)
            critical = False
        return effect, critical

    def get_text_effect(self, acting_unit, effect):
        """
        # Fuction name: get_text_effect
        # Purpose: Generates the pygame surface for a given effect value
        # Inputs: acting unit - The participant taking action
        #         effect - effect to render
        # Output: text_effect - pygame surface of the damage text
        """


        # Case for Offensive Combat Interactions
        if acting_unit.spell_actions[acting_unit.equipped].type == 'attack':

            if self.engine.options.battle_anim:
                if effect == 'miss':
                    text_effect = self.engine.render_outlined_text("MISS!", self.engine.battle_effect_font, dmg_color, (255, 255, 255), thickness = 1.1)
                else:
                    text_effect = self.engine.render_outlined_text(str(effect),  self.engine.battle_effect_font, dmg_color, (255, 255, 255), thickness = 1.1)
            else:
                if effect == 'miss':
                    text_effect = self.engine.render_outlined_text("MISS!", self.engine.cfont, dmg_color, (255, 255, 255))
                else:
                    text_effect = self.engine.render_outlined_text(str(effect), self.engine.cfont, dmg_color, (255, 255, 255))

        # Case for Healing Combat interactions
        elif acting_unit.spell_actions[acting_unit.equipped].type in ('healing', 'support'):
            if self.engine.options.battle_anim:
                text_effect =  self.engine.render_outlined_text(str(effect),  self.engine.battle_effect_font, healing_color, (255, 255, 255), thickness = 1.1)
            else:
                text_effect = self.engine.render_outlined_text(str(effect), self.engine.cfont,  healing_color, (255, 255, 255))

        return text_effect

    def apply_battle_effects(self, acting_unit, target, effect, critical):

        """
        # Fuction name: apply_battle_effects
        # Purpose: Applies the battle effects to the target
        # Inputs: acting unit, target - The participants in the battle
        #         effect - effect to apply to the target
        #         critical - critical hit if applicable
        # Output: revive_anim - T/F if revive animation needs to be shown
        """
        revive_anim = False

        if acting_unit.spell_actions[acting_unit.equipped].type == 'attack' and effect != "miss":
            target.HP -= effect

            # If the defender is dead, sets HP to 0 and sets their alive flag to False
            if target.HP <= 0:
                target.HP = 0
                target.alive = False

                # Try this first
                # 10% chance of surviving a killing blow at high spirits
                #   If it works, the target survives with 1HP.
                #   The target has their spirit reduced by 5.0
                if target.spirit_stats == "high":
                    print 'High Spirits Death Save'
                    x = randint(1, 10)
                    if x == 10:
                        target.alive = True
                        target.HP = 1
                        target.spirit -= 500

                # If high spirits save is not available or fails, go to revive traits.
                if not target.alive and target.ressurected == False:

                    if (target.has_trait_property('Revive Lv.1')
                        or target.has_trait_property('Revive Lv.2')
                        or target.has_trait_property('Revive Lv.3')):

                        # Revives the target and returns a flag to show the barrier animation
                        revive_anim = self.revive(target)

            # Status Effects Processed here
            elif target.HP > 0 and acting_unit.spell_actions[acting_unit.equipped].status_effects:
                acting_unit.spell_actions[acting_unit.equipped].give_status_effect(acting_unit, target)

        elif acting_unit.spell_actions[acting_unit.equipped].type in ('healing', 'support'):
            target.HP += effect
            if target.HP > target.maxHP:
                target.HP = target.maxHP

        return revive_anim

    def post_battle_event(self, lhs_unit, rhs_unit, lhs_action, rhs_action):
        '''
        # Function Name: Post-battle Event
        # Purpose: Processes post battle stats updates like lowering spell use counts
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         rhs_action - whether the RHS unit took action (counter) during this event
        '''

        # Modifiers for spirit saver and spirit booster
        SAVER_MOD = 0.8
        BOOSTER_MOD = 1.2

        if lhs_action:
            # Lowers life of the spell action by 1
            lhs_unit.spell_actions[lhs_unit.equipped].livesleft -= 1

            # Takes off SC cost of the spell action
            if lhs_unit.spell_actions[lhs_unit.equipped].sc_cost > 0:


                if lhs_unit.has_trait_property('Spirit Saver'):
                    spirit_delta = int(lhs_unit.spell_actions[lhs_unit.equipped].sc_cost*SAVER_MOD)
                elif lhs_unit.has_trait_property('Spirit Booster'):
                    spirit_delta = int(lhs_unit.spell_actions[lhs_unit.equipped].sc_cost*BOOSTER_MOD)
                else:
                    spirit_delta = lhs_unit.spell_actions[lhs_unit.equipped].sc_cost

                lhs_unit.spirit -= spirit_delta

                if lhs_unit.spirit < 0:
                    lhs_unit.spirit = 0

            # If lives left are 0, replaces the equipped slot with empty
            if lhs_unit.spell_actions[lhs_unit.equipped].livesleft == 0:
                lhs_unit.map.display_alert('Spell Action Used Up!',
                                           "%s's %s has run out of uses!"%(lhs_unit.name,
                                                                           lhs_unit.spell_actions[lhs_unit.equipped].namesuffix))

                if lhs_unit.spell_actions[lhs_unit.equipped].consumable == True:
                    lhs_unit.spell_actions[lhs_unit.equipped] = None


        # Checks the opponent if they have an equipped spell and if it was used in a counterattack
        if rhs_action:
            # Lowers life of the spell action by 1
            rhs_unit.spell_actions[rhs_unit.equipped].livesleft -= 1

            # Takes off SC cost of the spell action
            if rhs_unit.spell_actions[rhs_unit.equipped].sc_cost > 0:
                if rhs_unit.has_trait_property('Spirit Saver'):
                    spirit_delta = int(rhs_unit.spell_actions[rhs_unit.equipped].sc_cost*SAVER_MOD)
                elif rhs_unit.has_trait_property('Spirit Booster'):
                    spirit_delta = int(rhs_unit.spell_actions[rhs_unit.equipped].sc_cost*BOOSTER_MOD)
                else:
                    spirit_delta = rhs_unit.spell_actions[rhs_unit.equipped].sc_cost

                rhs_unit.spirit -= spirit_delta

                if rhs_unit.spirit < 0:
                    rhs_unit.spirit = 0

            # If lives left are 0, replaces the equipped slot with empty
            if rhs_unit.spell_actions[rhs_unit.equipped].livesleft == 0:
                rhs_unit.map.display_alert('Spell Action Used Up!',
                                           "%s's %s has run out of uses!"%(rhs_unit.name,
                                                                           rhs_unit.spell_actions[rhs_unit.equipped].namesuffix))
                if rhs_unit.spell_actions[rhs_unit.equipped].consumable == True:
                    rhs_unit.spell_actions[rhs_unit.equipped] = None


    def draw_idle_delay(self, lhs_unit, rhs_unit, lhs_anim, rhs_anim):
        '''
        # Function Name: draw_idle_delay
        # Purpose: Half second idle delay
        #         LHS Unit Animation: Idle
        #         RHS Unit Animation: Idle
        #
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         lhs_anim, rhs_anim - animation data for units in battle
        '''

        if lhs_unit.animation_enable:
            lhs_anim.set_mode('idle')
        if rhs_unit.animation_enable:
            rhs_anim.set_mode('idle')

        max_frames = 30

        for frame_num in xrange(0, max_frames):
            # Prevents lockup of the system during animation
            self.check_exit()
            self.render_background(lhs_unit, rhs_unit)
            self.render_combat_gui()
            self.render_combat_data(lhs_unit, rhs_unit)

            self.chara_sprites.update()
            self.chara_sprites.draw(self.engine.surface)

            # Defaults to map sized sprite if no animation available
            #if lhs_unit.animation_enable:
            #    lhs_anim.render(self.engine.surface)
            #else:
            #    self.engine.surface.blit(lhs_unit.image, (210, 280), (175, 0, 35, 35))
            #if rhs_unit.animation_enable:
            #    rhs_anim.render(self.engine.surface)
            #else:
            #    self.engine.surface.blit(rhs_unit.image, (595, 280), (280, 0, 35, 35))

            pygame.display.flip()
            self.engine.clock.tick(60)

    def draw_lhs_action(self, lhs_unit, rhs_unit, lhs_anim, rhs_anim):
        '''
        # Function Name: draw_lhs_action
        # Purpose: Draw the LHS unit activating the spell
        #         LHS Unit Animation: Physical/Magical Spell Activation
        #         RHS Unit Animation: Idle
        #
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         lhs_anim, rhs_anim - animation data for units in battle
        '''
        if lhs_unit.animation_enable:
            lhs_anim.set_mode(lhs_unit.spell_actions[lhs_unit.equipped].attacktype)
            max_frames = lhs_anim.FRAME_REPEAT*len(lhs_anim.anim_dict[lhs_anim.mode]['frames'])
        else:
            max_frames = 1
        # if rhs_unit.animation_enable:
        #     rhs_anim.set_mode('idle')


        # Draws first frame
        self.render_background(lhs_unit, rhs_unit, self.bg_surface)
        self.render_combat_gui(self.bg_surface)
        self.render_combat_data(lhs_unit, rhs_unit, self.bg_surface)

        self.engine.surface.blit(self.bg_surface, (0, 0))
        self.chara_sprites.update()
        self.chara_sprites.draw(self.engine.surface)
        pygame.display.flip()
        self.engine.clock.tick(60)

        # Runs once through the LHS unit's activation animation
        for frame_num in xrange(1, max_frames):
            self.check_exit()

            self.chara_sprites.clear(self.engine.surface, self.bg_surface)
            self.chara_sprites.update()
            rects = self.chara_sprites.draw(self.engine.surface)

            pygame.display.update(rects)
            self.engine.clock.tick(60)

    def draw_lhs_spell(self, lhs_unit, rhs_unit, lhs_anim, rhs_anim, lhs_spell_anim):
        '''
        # Function Name: draw_lhs_spell
        # Purpose: Draw the LHS unit casting the spell and spell bullets
        #         LHS Unit Animation: Physical/Magical Spell Casting
        #         RHS Unit Animation: Idle
        #
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         lhs_anim, rhs_anim - animation data for units in battle
        '''

        if lhs_unit.animation_enable:
            lhs_anim.set_mode("cast_"+lhs_unit.spell_actions[lhs_unit.equipped].attacktype)
        # if rhs_unit.animation_enable:
        #     rhs_anim.set_mode('idle')

        self.render_background(lhs_unit, rhs_unit, self.bg_surface)
        self.render_combat_gui(self.bg_surface)
        self.render_combat_data(lhs_unit, rhs_unit, self.bg_surface)

        self.engine.surface.blit(self.bg_surface, (0, 0))
        self.chara_sprites.update()
        self.chara_sprites.draw(self.engine.surface)
        pygame.display.flip()
        self.engine.clock.tick(60)

        num_sfx = len(lhs_spell_anim.sfx_timings)

        #Initialize sound effects
        if lhs_spell_anim.sfx_timings:
            current_timing, current_effect = lhs_spell_anim.sfx_timings[0]
            sfx_index = 0
        else:
            current_timing = None
            current_effect = None
            sfx_index = 0

        t0 = pygame.time.get_ticks()

        for frame_counter in xrange(0, lhs_spell_anim.max_frames):
            self.check_exit()

            rhs_mode = False

            # Play a sound effect if the current sound effect is triggered on this frame
            if current_effect and frame_counter >= current_timing:
                self.engine.sfx_system.sound_catalog[current_effect].play()
                sfx_index += 1
                if sfx_index < num_sfx:
                    current_timing, current_effect = lhs_spell_anim.sfx_timings[sfx_index]
                else:
                    current_timing = None
                    current_effect = None


            self.chara_sprites.clear(self.engine.surface, self.bg_surface)
            lhs_spell_anim.clear()
            self.chara_sprites.update()
            rects = self.chara_sprites.draw(self.engine.surface)
            rects += lhs_spell_anim.update(t0, rhs_mode)

            pygame.display.update(rects)
            t0 = pygame.time.get_ticks()
            self.engine.clock.tick(60)

    def draw_lhs_effect(self, lhs_unit, rhs_unit, lhs_anim, rhs_anim, text_lhs_effect, rhs_hp_before, rhs_hp_after):
        '''
        # Function Name: draw_lhs_effect_text
        # Purpose: Draw the effect the LHS unit had on the RHS unit for 1 s
        #         LHS Unit Animation: Idle
        #         RHS Unit Animation: Idle
        #
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         lhs_anim, rhs_anim - animation data for units in battle
        #         text_lhs_effect - effect of LHS's action on RHS unit
        '''
        frame_num = 0
        if lhs_unit.animation_enable:
            lhs_anim.set_mode('idle')

        max_frames = 60

        # Calculate the size of the box to show
        effect_box_before = self.engine.big_hp_meter.get_width() - int(self.engine.big_hp_meter.get_width()*float(rhs_hp_before)/rhs_unit.maxHP)
        effect_box_after = self.engine.big_hp_meter.get_width() - int(self.engine.big_hp_meter.get_width()*float(rhs_hp_after)/rhs_unit.maxHP)
        effect_box_delta = effect_box_after - effect_box_before

        if rhs_unit.invincible and lhs_unit.spell_actions[lhs_unit.equipped].type == 'attack':
            self.barrier_animation(lhs_unit, rhs_unit, False)

        for frame_num in xrange(0, max_frames):
            # Prevents lockup of the system during animation
            self.check_exit()
            self.render_background(lhs_unit, rhs_unit)
            self.render_combat_gui()
            self.render_combat_data(lhs_unit, rhs_unit)

            # Case for damage taken
            if rhs_hp_before > rhs_hp_after:
                pygame.draw.rect(self.engine.surface, self.damage_color, (457 + effect_box_before, 22, effect_box_delta, 21 ))

            # Case for healing
            elif rhs_hp_before < rhs_hp_after:
                pygame.draw.rect(self.engine.surface, self.heal_color, (457 + effect_box_before, 22, effect_box_delta, 21 ))

            # Case for no HP change
            else:
                pass

            self.chara_sprites.update()
            self.chara_sprites.draw(self.engine.surface)

            # Draws damage caused by LHS unit
            self.engine.surface.blit(text_lhs_effect, (560 + self.engine.battle_panel.get_width()/2 - text_lhs_effect.get_width()/2, 120))

            pygame.display.flip()
            self.engine.clock.tick(60)

        if rhs_hp_after != rhs_hp_before:
            smoothstep = lambda v: (v*v*(3-2*v))

            max_frames = 30

            for frame_num in xrange(0, max_frames):

                v = float(frame_num)/float(max_frames)
                v = smoothstep(v)
                intermediate_step = int(v*effect_box_delta)

                current_x = effect_box_before + intermediate_step
                current_delta = effect_box_delta - intermediate_step

                # Prevents lockup of the system during animation
                self.check_exit()
                self.render_background(lhs_unit, rhs_unit)
                self.render_combat_gui()
                self.render_combat_data(lhs_unit, rhs_unit)


                if rhs_hp_before > rhs_hp_after:
                    pygame.draw.rect(self.engine.surface, self.damage_color, (457 + current_x, 22, current_delta, 21 ))
                else:
                    pygame.draw.rect(self.engine.surface, self.heal_color, (457 + current_x, 22, current_delta, 21 ))

                self.chara_sprites.update()
                self.chara_sprites.draw(self.engine.surface)

                # Draws damage caused by LHS unit
                self.engine.surface.blit(text_lhs_effect, (560 + self.engine.battle_panel.get_width()/2 -text_lhs_effect.get_width()/2, 120))

                pygame.display.flip()
                self.engine.clock.tick(60)

    def draw_rhs_action(self, lhs_unit, rhs_unit, lhs_anim, rhs_anim):
        '''
        # Function Name: draw_rhs_action
        # Purpose: Draw the RHS unit activating the spell
        #         LHS Unit Animation: Idle
        #         RHS Unit Animation: Physical/Magical Spell Activation
        #
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         lhs_anim, rhs_anim - animation data for units in battle
        '''

        if rhs_unit.animation_enable:
            rhs_anim.set_mode(rhs_unit.spell_actions[rhs_unit.equipped].attacktype)
            max_frames = rhs_anim.FRAME_REPEAT*len(rhs_anim.anim_dict[rhs_anim.mode]['frames'])
        else:
            max_frames = 1


        # Draws first frame
        self.render_background(lhs_unit, rhs_unit, self.bg_surface)
        self.render_combat_gui(self.bg_surface)
        self.render_combat_data(lhs_unit, rhs_unit, self.bg_surface)

        self.engine.surface.blit(self.bg_surface, (0, 0))
        self.chara_sprites.update()
        self.chara_sprites.draw(self.engine.surface)
        pygame.display.flip()
        self.engine.clock.tick(60)

        # Runs once through the RHS unit's activation animation
        for frame_num in xrange(0, max_frames):
            self.check_exit()

            self.chara_sprites.clear(self.engine.surface, self.bg_surface)
            self.chara_sprites.update()
            rects = self.chara_sprites.draw(self.engine.surface)

            pygame.display.update(rects)
            self.engine.clock.tick(60)

    def draw_rhs_spell(self, lhs_unit, rhs_unit, lhs_anim, rhs_anim, rhs_spell_anim):
        '''
        # Function Name: draw_rhs_spell
        # Purpose: Draw the RHS unit casting the spell and spell bullets
        #         LHS Unit Animation: Idle
        #         RHS Unit Animation: Physical/Magical Spell Casting
        #
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         lhs_anim, rhs_anim - animation data for units in battle
        '''

        if rhs_unit.animation_enable:
            rhs_anim.set_mode('cast_'+rhs_unit.spell_actions[rhs_unit.equipped].attacktype)

        self.render_background(lhs_unit, rhs_unit, self.bg_surface)
        self.render_combat_gui(self.bg_surface)
        self.render_combat_data(lhs_unit, rhs_unit, self.bg_surface)

        self.engine.surface.blit(self.bg_surface, (0, 0))
        self.chara_sprites.update()
        self.chara_sprites.draw(self.engine.surface)
        pygame.display.flip()
        self.engine.clock.tick(60)


        # Initialize Sound Effects
        num_sfx = len(rhs_spell_anim.sfx_timings)

        if rhs_spell_anim.sfx_timings:
            current_timing, current_effect = rhs_spell_anim.sfx_timings[0]
            sfx_index = 0
        else:
            current_timing = None
            current_effect = None
            sfx_index = 0

        t0 = pygame.time.get_ticks()

        for frame_counter in xrange(0, rhs_spell_anim.max_frames):
            self.check_exit()

            rhs_mode = True

            # Play a sound effect if the current sound effect is triggered on this frame
            if current_effect and frame_counter >= current_timing:
                self.engine.sfx_system.sound_catalog[current_effect].play()
                sfx_index += 1
                if sfx_index < num_sfx:
                    current_timing, current_effect = rhs_spell_anim.sfx_timings[sfx_index]
                else:
                    current_timing = None
                    current_effect = None

            self.chara_sprites.clear(self.engine.surface, self.bg_surface)
            rhs_spell_anim.clear()
            self.chara_sprites.update()
            rects = self.chara_sprites.draw(self.engine.surface)
            rects += rhs_spell_anim.update(t0, rhs_mode)

            pygame.display.update(rects)
            t0 = pygame.time.get_ticks()
            self.engine.clock.tick(60)

    def draw_rhs_effect(self, lhs_unit, rhs_unit, lhs_anim, rhs_anim, text_rhs_effect, lhs_hp_before, lhs_hp_after):
        '''
        # Function Name: draw_rhs_effect_text
        # Purpose: Draw the effect the RHS unit had on the LHS unit for 1 s
        #         LHS Unit Animation: Idle
        #         RHS Unit Animation: Idle
        #
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         lhs_anim, rhs_anim - animation data for units in battle
        #         text_rhs_effect - effect of RHS's action on LHS unit
        '''

        # Calculate the size of the box to show
        effect_box_before = int(self.engine.big_hp_meter.get_width()*float(lhs_hp_before)/lhs_unit.maxHP)
        effect_box_after = int(self.engine.big_hp_meter.get_width()*float(lhs_hp_after)/lhs_unit.maxHP)
        effect_box_delta = effect_box_before - effect_box_after

        frame_num = 0
        if rhs_unit.animation_enable:
            rhs_anim.set_mode('idle')

        max_frames = 60

        if lhs_unit.invincible and rhs_unit.spell_actions[rhs_unit.equipped].type == 'attack':
            self.barrier_animation(lhs_unit, rhs_unit, True)

        for frame_num in xrange(0, max_frames):
            # Prevents lockup of the system during animation
            self.check_exit()
            self.render_background(lhs_unit, rhs_unit)
            self.render_combat_gui()
            self.render_combat_data(lhs_unit, rhs_unit)


            if lhs_hp_before > lhs_hp_after:
                pygame.draw.rect(self.engine.surface, self.damage_color, (87 + effect_box_after, 22, effect_box_delta, 21 ))
            elif lhs_hp_before < lhs_hp_after:
                pygame.draw.rect(self.engine.surface, self.heal_color, (87 + effect_box_after, 22, effect_box_delta, 21 ))
            else:
                pass

            self.chara_sprites.update()
            self.chara_sprites.draw(self.engine.surface)

            # Draws damage caused by LHS unit
            self.engine.surface.blit(text_rhs_effect, (175+self.engine.battle_panel.get_width()/2-text_rhs_effect.get_width()/2, 120))

            pygame.display.flip()
            self.engine.clock.tick(60)

        if lhs_hp_after != lhs_hp_before:
            smoothstep = lambda v: (v*v*(3-2*v))

            max_frames = 30

            for frame_num in xrange(0, max_frames):

                v = float(frame_num)/float(max_frames)
                v = smoothstep(v)
                intermediate_step = int(v*effect_box_delta)

                current_delta = effect_box_delta - intermediate_step

                # Prevents lockup of the system during animation
                self.check_exit()
                self.render_background(lhs_unit, rhs_unit)
                self.render_combat_gui()
                self.render_combat_data(lhs_unit, rhs_unit)


                if lhs_hp_before > lhs_hp_after:
                    pygame.draw.rect(self.engine.surface, self.damage_color, (87 + effect_box_after, 22, current_delta, 21 ))
                else:
                    pygame.draw.rect(self.engine.surface, self.heal_color, (87 + effect_box_after, 22, current_delta, 21 ))

                self.chara_sprites.update()
                self.chara_sprites.draw(self.engine.surface)

                # Draws damage caused by LHS unit
                self.engine.surface.blit(text_rhs_effect, (175+self.engine.battle_panel.get_width()/2-text_rhs_effect.get_width()/2, 120))

                pygame.display.flip()
                self.engine.clock.tick(60)

    def draw_revive_effect(self, lhs_unit, rhs_unit, lhs_anim, rhs_anim, revive):
        '''
        # Function Name: draw_rhs_spell
        # Purpose: Draw an animation indicating that a character has
        #          executed a revive trait (counterbomb)
        #         LHS Unit Animation: Idle
        #         RHS Unit Animation: Idle
        #
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         lhs_anim, rhs_anim - animation data for units in battle
        #         revive - 'lhs' or 'rhs'
        '''

        if lhs_unit.animation_enable:
            lhs_anim.set_mode('idle')
        if rhs_unit.animation_enable:
            rhs_anim.set_mode('idle')


        if revive == 'lhs':

            # Highest revive trait overrides lower revive traits
            if lhs_unit.has_trait_property('Revive Lv.3'):
                trait_name = self.engine.render_outlined_text("Revive Lv.3!", self.engine.cfont, (255, 0, 0), (255, 255, 255))
            elif lhs_unit.has_trait_property('Revive Lv.2'):
                trait_name = self.engine.render_outlined_text("Revive Lv.2!", self.engine.cfont, (255, 0, 0), (255, 255, 255))
            elif lhs_unit.has_trait_property('Revive Lv.1'):
                trait_name = self.engine.render_outlined_text("Revive Lv.1!", self.engine.cfont, (255, 0, 0), (255, 255, 255))

            # Draw as if spell anim cast by RHS unit
            rhs_mode = True

        else:

            # Highest revive trait overrides lower revive traits
            if rhs_unit.has_trait_property('Revive Lv.3'):
                trait_name = self.engine.render_outlined_text("Revive Lv.3!", self.engine.cfont, (255, 0, 0), (255, 255, 255))
            elif rhs_unit.has_trait_property('Revive Lv.2'):
                trait_name = self.engine.render_outlined_text("Revive Lv.2!", self.engine.cfont, (255, 0, 0), (255, 255, 255))
            elif rhs_unit.has_trait_property('Revive Lv.1'):
                trait_name = self.engine.render_outlined_text("Revive Lv.1!", self.engine.cfont, (255, 0, 0), (255, 255, 255))

            # Draw as if spell anim cast by LHS unit
            rhs_mode = False

        self.render_background(lhs_unit, rhs_unit, self.bg_surface)
        self.render_combat_gui(self.bg_surface)
        self.render_combat_data(lhs_unit, rhs_unit, self.bg_surface)
        if revive == 'lhs':
            self.bg_surface.blit(trait_name, (225-trait_name.get_width()/2, 145))

        else:
            self.bg_surface.blit(trait_name, (610-trait_name.get_width()/2, 145))

        self.engine.surface.blit(self.bg_surface, (0, 0))
        self.chara_sprites.update()
        self.chara_sprites.draw(self.engine.surface)
        self.revive_animation(lhs_unit, rhs_unit, rhs_mode)

    def revive_animation(self, lhs_unit, rhs_unit, rhs_mode):

        """
        function name: draws the revive animation
        inputs: rhs_mode - True if the animation is played while the RHS unit is taking its action
        """

        self.render_background(lhs_unit, rhs_unit, self.bg_surface)
        self.render_combat_gui(self.bg_surface)
        self.render_combat_data(lhs_unit, rhs_unit, self.bg_surface)

        self.engine.surface.blit(self.bg_surface, (0, 0))
        self.chara_sprites.update()
        self.chara_sprites.draw(self.engine.surface)

        pygame.display.flip()
        self.engine.clock.tick(60)


        t0 = pygame.time.get_ticks()

        for frame_counter in xrange(0, self.revive_anim.max_frames):
            self.check_exit()

            self.chara_sprites.clear(self.engine.surface, self.bg_surface)
            self.revive_anim.clear()
            self.chara_sprites.update()
            rects = self.chara_sprites.draw(self.engine.surface)
            rects += self.revive_anim.update(t0, rhs_mode)

            pygame.display.update(rects)
            t0 = pygame.time.get_ticks()
            self.engine.clock.tick(60)


        # Resets revive animation for next time
        self.revive_anim.anim_sprite.current_frame = 0


    def barrier_animation(self, lhs_unit, rhs_unit, rhs_mode):

        """
        function name: draws the barrier animation
        inputs: rhs_mode - True if the animation is played while the RHS unit is taking its action
        """

        self.render_background(lhs_unit, rhs_unit, self.bg_surface)
        self.render_combat_gui(self.bg_surface)
        self.render_combat_data(lhs_unit, rhs_unit, self.bg_surface)

        self.engine.surface.blit(self.bg_surface, (0, 0))
        self.chara_sprites.update()
        self.chara_sprites.draw(self.engine.surface)

        pygame.display.flip()
        self.engine.clock.tick(60)


        t0 = pygame.time.get_ticks()

        for frame_counter in xrange(0, self.barrier_anim.max_frames):
            self.check_exit()

            self.chara_sprites.clear(self.engine.surface, self.bg_surface)
            self.barrier_anim.clear()
            self.chara_sprites.update()
            rects = self.chara_sprites.draw(self.engine.surface)
            rects += self.barrier_anim.update(t0, rhs_mode)

            pygame.display.update(rects)
            t0 = pygame.time.get_ticks()
            self.engine.clock.tick(60)


        # Resets revive animation for next time
        self.barrier_anim.anim_sprite.current_frame = 0

    def check_exit(self):
        """
        # Function Name: check_exit
        # Purpose: Checks if the user has exited in the middle of a battle (prevents
        # game from freezing up)
        """
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                exit()

    def revive(self, user):
        """
        # Function Name: revive_execute
        # Purpose: Does whatever the trait is designed to do before the battle
        # Inputs: user - The person who is using this trait
        """

        print "Revive attempted for "+user.name
        if user.has_trait_property('Revive Lv.1'):
            # HP to revive to (multiply to Max HP)
            HP_ressurect = 0.05
            # SC pentalty
            SC_penalty = 300

        if user.has_trait_property('Revive Lv.2'):
            HP_ressurect = 0.50
            SC_penalty = 600

        if user.has_trait_property('Revive Lv.3'):
            HP_ressurect = 1
            SC_penalty = 900

        print user.name +" revived!"
        user.alive = True
        user.ressurected = True
        user.spirit -= SC_penalty
        recovery = int(HP_ressurect*user.maxHP)
        user.HP = recovery

        if user.spirit < 0:
            user.spirit = 0

        return True

    def render_background(self, lhs_unit, rhs_unit, target_surface = None):
        '''
        # Function Name: draw_background
        # Purpose: Draws the background corresponding to the terrain that each unit is standing on.
        '''
        if not target_surface:
            target_surface = self.engine.surface

        target_surface.blit(self.engine.battle_bg, (0, 0))

        #self.engine.surface.blit(lhs_unit.map.terrainmap[tuple(lhs_unit.location_tile)][0].bg_img, (0, 0))
        #self.engine.surface.blit(rhs_unit.map.terrainmap[tuple(rhs_unit.location_tile)][0].bg_img, (420, 0))

    def render_unit_stats(self, unit, rhs, target_surface = None):
        """
        # Function Name: plot_battle_lhs
        # Purpose: Plots the unit's portrait, name, HP, four stats, active spell, and active spell's mods to the
        # left side of the display panel
        """
        if rhs:
            offset = 420
        else:
            offset = 0

        if not target_surface:
            target_surface = self.engine.surface


        text_name = self.engine.bfont.render(unit.name, True, (0, 0, 0))
        text_line1 = self.engine.sfont.render("HP: %3.0f/%3.0f"%(unit.HP, unit.maxHP), True, (0, 0, 0))
        text_line2 = self.engine.sfont.render("LV: %2.0f    EXP: %3.0f/100"%(unit.level, unit.exp), True, (0, 0, 0))

        # Trait lines
#        if unit.traits[0][0]:
#            text_line3_str = "Action Trait: "+ unit.traits[0][0].name
#        else:
#            text_line3_str = "Action Trait: None"
#
#        if unit.traits[1][0]:
#            text_line4_str = 'Support Trait: '+unit.traits[1][0].name
#        else:
#            text_line4_str = 'Support Trait: None'

#        text_line3 = self.engine.sfont.render(text_line3_str, True, (0, 0, 0))
#        text_line4 = self.engine.sfont.render(text_line4_str, True, (0, 0, 0))

        text_line5 = self.engine.sfont.render("Spirit Charge: %3.0f"%(unit.spirit), True, (0, 0, 0))

        if unit.spell_actions[unit.equipped]:
            # Attack type
            target_surface.blit(self.engine.spell_icons_big, (150+offset, 552), unit.spell_actions[unit.equipped].a_type_big)
            # Damage type
            target_surface.blit(self.engine.spell_icons_big, (175+offset, 552), unit.spell_actions[unit.equipped].d_type_big)
            # Spell Type
            target_surface.blit(self.engine.spell_icons_big, (200+offset, 552), unit.spell_actions[unit.equipped].al_type_big)
            # Counterattack
            target_surface.blit(self.engine.spell_icons_big, (225+offset, 552), unit.spell_actions[unit.equipped].c_type_big)

        target_surface.blit(unit.av, (10+offset, 500))
        target_surface.blit(text_name, (150+offset, 500))
        target_surface.blit(text_line1, (150+offset, 520))
        target_surface.blit(text_line2, (150+offset, 535))
        #target_surface.blit(text_line3, (150+offset, 575))
        #target_surface.blit(text_line4, (150+offset, 590))
        target_surface.blit(text_line5, (150+offset, 605))



    def render_combat_gui(self, target_surface = None):
        """
        # Function Name: render combat gui
        # Purpose: renders the background objects
        """

        if not target_surface:
            target_surface = self.engine.surface

        # Displays the two battle panels

        target_surface.blit(self.engine.battle_panel, (175, 290))
        target_surface.blit(self.engine.battle_panel, (560, 290))

    def render_health_meters(self, lhs_unit, rhs_unit, target_surface):
        """
        Draws the health meters of both units

        inputs: lhs_unit, rhs_unit -  participants in the battle
                target_surface - Target to draw to
        """

        # Calculates the portion of the HP meter to draw
        lhs_fraction = float(lhs_unit.HP) / lhs_unit.maxHP
        rhs_fraction = float(rhs_unit.HP) / rhs_unit.maxHP
        lhs_hp_width = int(lhs_fraction*self.engine.big_hp_meter.get_width())
        rhs_hp_width = int(rhs_fraction*self.engine.big_hp_meter.get_width())
        lhs_empty = self.engine.big_hp_meter.get_width() - lhs_hp_width
        rhs_empty = self.engine.big_hp_meter.get_width() - rhs_hp_width

        target_surface.blit(self.engine.meter_outline, (85, 20))
        target_surface.blit(self.engine.big_hp_meter, (87, 22))
        if lhs_empty:
            pygame.draw.rect(target_surface, self.empty_color, (87 + lhs_hp_width, 22, lhs_empty, 21))

        target_surface.blit(self.engine.meter_outline, (455, 20))
        target_surface.blit(self.engine.big_hp_meter, (457, 22))
        if rhs_empty:
            pygame.draw.rect(target_surface, self.empty_color, (457, 22, rhs_empty, 21))

    def render_sc_meters(self, lhs_unit, rhs_unit, target_surface):
        """
        Draws the health meters of both units

        inputs: lhs_unit, rhs_unit -  participants in the battle
                target_surface - Target to draw to
        """

        # Calculates the portion of the HP meter to draw
        lhs_fraction = float(lhs_unit.spirit) / 900
        rhs_fraction = float(rhs_unit.spirit) / 900
        lhs_sc_width = int(lhs_fraction*self.engine.big_hp_meter.get_width())
        rhs_sc_width = int(rhs_fraction*self.engine.big_hp_meter.get_width())
        lhs_empty = self.engine.big_hp_meter.get_width() - lhs_sc_width
        rhs_empty = self.engine.big_hp_meter.get_width() - rhs_sc_width

        target_surface.blit(self.engine.meter_outline, (50, 55))
        target_surface.blit(self.engine.big_sc_meter, (52, 57))
        if lhs_empty:
            pygame.draw.rect(target_surface, self.empty_color, (52 + lhs_sc_width, 57, lhs_empty, 21))

        target_surface.blit(self.engine.meter_outline, (490, 55))
        target_surface.blit(self.engine.big_sc_meter, (492, 57))
        if rhs_empty:
            pygame.draw.rect(target_surface, self.empty_color, (492, 57, rhs_empty, 21))

    def render_combat_data(self, lhs_unit, rhs_unit, target_surface = None):
        """
        # Function Name: render combat
        # Purpose: Renders the menu boards, the two battle panels, and data
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        """
        if not target_surface:
            target_surface = self.engine.surface

        text_HP = self.engine.speaker_font.render("HP", True, (0, 0, 0))
        text_SC = self.engine.speaker_font.render("SC", True, (0, 0, 0))
        target_surface.blit(self.engine.battle_top, (0, 0))
        target_surface.blit(self.meter_panel, (5, 50))
        target_surface.blit(text_SC, (6 + self.meter_panel.get_width()/2 - text_SC.get_width()/2,
                                        51 + self.meter_panel.get_height()/2 - text_SC.get_height()/2))

        target_surface.blit(self.meter_panel, (795, 50))
        target_surface.blit(text_SC, (796 + self.meter_panel.get_width()/2 - text_SC.get_width()/2,
                                        51 + self.meter_panel.get_height()/2 - text_SC.get_height()/2))

        target_surface.blit(self.meter_panel, (40, 15))
        target_surface.blit(text_HP, (41 + self.meter_panel.get_width()/2 - text_HP.get_width()/2,
                                        16 + self.meter_panel.get_height()/2 - text_HP.get_height()/2))

        target_surface.blit(self.meter_panel, (760, 15))
        target_surface.blit(text_HP, (761 + self.meter_panel.get_width()/2 - text_HP.get_width()/2,
                                        16 + self.meter_panel.get_height()/2 - text_HP.get_height()/2))


        self.render_health_meters(lhs_unit, rhs_unit, target_surface)
        self.render_sc_meters(lhs_unit, rhs_unit, target_surface)

        # Plots stats in bottom right
        self.engine.surface.blit(self.engine.battle_board, (0, 490))
        lhs_unit.plot_stats()
        rhs_unit.plot_stats(rhs = True)

        if target_surface != self.engine.surface:
            bottom_panel = self.engine.surface.subsurface(0, 490, 840, 630-490)
            target_surface.blit(bottom_panel, (0, 490))

    # Methods for when battle animations are turned off go here
    def draw_map_delay(self, lhs_unit, rhs_unit):
        """
        # Function Name: draw_map_delay
        # Purpose: Draws a half second delay on the battle map, rendering the data
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        """

        # Half a second pause
        for i in xrange(0, 30):
            lhs_unit.map.render_background()
            lhs_unit.map.render_all_units()
            lhs_unit.map.render_cursor()
            self.render_combat_data(lhs_unit, rhs_unit)
            pygame.display.flip()
            self.engine.clock.tick(60)

    def draw_map_lhs_effect(self, lhs_unit, rhs_unit, text_lhs_effect):
        """
        # Function Name: draw_map_lhs_effect
        # Purpose: Draws the effect of the lhs unit's action on the battle map
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         lhs_effect_text - effect of lhs unit's action on rhs_unit
        """

        # Draw damage for 1 second
        effect_image_width = text_lhs_effect.get_width()/2
        for i in xrange(0, 60):
            lhs_unit.map.render_background()
            lhs_unit.map.render_all_units()
            lhs_unit.map.render_cursor()
            self.render_combat_data(lhs_unit, rhs_unit)

            self.engine.surface.blit(text_lhs_effect,
                                         (rhs_unit.location_pixel.x+18-effect_image_width-35*rhs_unit.map.screen_shift.x,
                                          rhs_unit.location_pixel.y-25-35*rhs_unit.map.screen_shift.y))
            pygame.display.flip()
            self.engine.clock.tick(60)


    def draw_map_rhs_effect(self, lhs_unit, rhs_unit, text_rhs_effect):
        """
        # Function Name: draw_map_rhs_effect
        # Purpose: Draws the effect of the rhs unit's action on the battle map
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         text_rhs_effect - effect of rhs unit's action on lhs_unit
        """

        # Draw damage for 1 second
        effect_image_width = text_rhs_effect.get_width()/2
        for i in xrange(0, 60):
            lhs_unit.map.render_background()
            lhs_unit.map.render_all_units()
            lhs_unit.map.render_cursor()
            self.render_combat_data(lhs_unit, rhs_unit)

            self.engine.surface.blit(text_rhs_effect,
                                         (lhs_unit.location_pixel.x+18-effect_image_width-35*rhs_unit.map.screen_shift.x,
                                          lhs_unit.location_pixel.y-25-35*rhs_unit.map.screen_shift.y))
            pygame.display.flip()
            self.engine.clock.tick(60)

    def draw_map_revive_effect(self, lhs_unit, rhs_unit, revive):
        """
        # Function Name: draw_map_lhs_effect
        # Purpose: Draws the effect of the lhs unit's action on the battle map
        # Inputs: lhs_unit, rhs_unit -  participants in the battle
        #         revive - unit to revive
        """

        # Draw trait name for 1 second
        if revive == 'lhs':

            # Highest revive trait overrides lower revive traits
            if lhs_unit.has_trait_property('Revive Lv.3'):
                trait_name = self.engine.render_outlined_text("Revive Lv.3!", self.engine.cfont, (255, 0, 0), (255, 255, 255))
            elif lhs_unit.has_trait_property('Revive Lv.2'):
                trait_name = self.engine.render_outlined_text("Revive Lv.2!", self.engine.cfont, (255, 0, 0), (255, 255, 255))
            elif lhs_unit.has_trait_property('Revive Lv.1'):
                trait_name = self.engine.render_outlined_text("Revive Lv.1!", self.engine.cfont, (255, 0, 0), (255, 255, 255))

        else:
            # Highest revive trait overrides lower revive traits
            if rhs_unit.has_trait_property('Revive Lv.3'):
                trait_name = self.engine.render_outlined_text("Revive Lv.3!", self.engine.cfont, (255, 0, 0), (255, 255, 255))
            elif rhs_unit.has_trait_property('Revive Lv.2'):
                trait_name = self.engine.render_outlined_text("Revive Lv.2!", self.engine.cfont, (255, 0, 0), (255, 255, 255))
            elif rhs_unit.has_trait_property('Revive Lv.1'):
                trait_name = self.engine.render_outlined_text("Revive Lv.1!", self.engine.cfont, (255, 0, 0), (255, 255, 255))


        for i in xrange(0, 60):
            lhs_unit.map.render_background()
            lhs_unit.map.render_all_units()
            lhs_unit.map.render_cursor()
            self.render_combat_data(lhs_unit, rhs_unit)


            if revive == 'lhs':
                self.engine.surface.blit(trait_name,
                                         (lhs_unit.location_pixel.x+18-trait_name.get_width()/2-35*rhs_unit.map.screen_shift.x,
                                          lhs_unit.location_pixel.y-25-35*rhs_unit.map.screen_shift.y))



            else:
                self.engine.surface.blit(trait_name,
                                         (rhs_unit.location_pixel.x+18-trait_name.get_width()/2-35*rhs_unit.map.screen_shift.x,
                                          rhs_unit.location_pixel.y-25-35*rhs_unit.map.screen_shift.y))


            pygame.display.flip()
            self.engine.clock.tick(60)

