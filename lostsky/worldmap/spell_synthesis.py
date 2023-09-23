import pygame
from pygame.locals import *
from lostsky.core.utils import padlib_rounded_rect, get_ui_panel
from lostsky.core.colors import panel_color, border_color, selected_color, disabled_color, scroll_bar_color
from sys import exit

# spell creation system


class SpellSynthesisSystem(object):


    def __init__(self, engine):

        """
        # function name: __init__
        # purpose: creates the spell creation system object
        # inputs: engine - game system engine
        """

        self.engine = engine

    def spell_synthesis_menu(self):
        """
        # function name: spell creation menu
        # purpose: allows player to select among menu options within the spell creation menu
        """

        text_options = [self.engine.section_font.render("Spell Recipes", True, (0, 0, 0)),
                        self.engine.section_font.render("Treasures", True, (0, 0, 0)),
                        self.engine.section_font.render("Tutorial", True, (0, 0, 0)),
                        self.engine.section_font.render("Cancel", True, (0, 0, 0)) ]

        text_desc = ["Create spell items from elemental crystals. Discover new recipes to gain access to new spells.",
                     "View treasures in your possession.",
                     "Read how to use spell synthesis.",
                     "Exit the spell synthesis menu.",]

        options_panel = get_ui_panel((180, 40), border_color, panel_color)

        menu_flag = True
        menu_pos = 0

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if ( event.key == K_UP or event.key == K_LEFT ):
                        if menu_pos > 0:
                            menu_pos -= 1
                        elif menu_pos == 0:
                            menu_pos = 3
                    if ( event.key == K_DOWN or event.key == K_RIGHT ):
                        if menu_pos < 3:
                            menu_pos += 1
                        elif menu_pos == 3:
                            menu_pos = 0
                    if event.key == K_z or event.key == K_RETURN:

                        # Recipes
                        if menu_pos == 0:
                            self.recipe_menu()

                        # Treasures
                        elif menu_pos == 1:
                            self.engine.treasure_menu()

                        # Tutorial
                        elif menu_pos == 2:
                            self.tutorial_basic()

                        # Cancel
                        elif menu_pos == 3:
                            menu_flag = False

                    if event.key == K_x:
                        menu_flag = False

            if menu_flag:
                # Background image
                self.engine.surface.blit(self.engine.shop_bg, (0, 0))
                # Renders the options
                for index, option in enumerate(text_options):
                    self.engine.surface.blit(options_panel, (120, 50 + index*50))
                    self.engine.surface.blit(option, (120 + options_panel.get_width()/2 - option.get_width()/2,
                                                      50 + options_panel.get_height()/2 - option.get_height()/2 + index*50))

                # Draws the cursor
                padlib_rounded_rect(self.engine.surface, selected_color, (118, 48 + menu_pos*50, options_panel.get_width() + 4, options_panel.get_height() + 4), 6, 5)

                # Draw description
                self.engine.draw_conversation_message(text_desc[menu_pos])

                pygame.display.flip()
                self.engine.clock.tick(60)

    ############################################
    # Interactive methods
    ############################################
    def say(self, line, speaker=None, portrait=None):

        """
        # Function name: say
        # Purpose: Displays a line of text and awaits for the player to press Z to continue
        # Inputs: line = The string of text to be displayed
        #         speaker = The name of the person saying it
        #         portrait = portrait to display
        """
        menu_flag = True

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN and (event.key == K_z or event.key == K_RETURN):
                    menu_flag = False

            # Hold down C to skip through the game.
            keys = pygame.key.get_pressed()
            if keys[K_c]:
                menu_flag = False
            self.engine.surface.blit(self.engine.shop_bg, (0, 0))
            self.engine.draw_conversation_message(line, speaker, portrait)
            pygame.display.flip()
            self.engine.clock.tick(60)

    def recipe_menu(self):
        """
        # Function name: Recipe Menu
        # Purpose: Catalog of known spell recipes and direct access to created a wanted spell
        """

        all_recipe_data = self.get_all_recipe_data()
        all_spells = [self.engine.spell_catalog[recipe_data['spell_name']].construct_spell() for recipe_data in all_recipe_data]

        menu_flag = True
        menu_pos = 0
        offset = 0
        max_slots = 5

        update = True

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if ( event.key == K_UP or event.key == K_LEFT ):

                        update = True

                        # Top of the list, jump to the bottom
                        if menu_pos == 0:
                            menu_pos = len(all_recipe_data)-1
                            offset = max(0, len(all_recipe_data) - max_slots)

                        # Top of the itnerval, shift offset up
                        elif menu_pos == offset:
                            menu_pos -= 1
                            offset -= 1

                        # within interval, move cursor without changing shift
                        elif menu_pos > 0:
                            menu_pos -= 1

                    if ( event.key == K_DOWN or event.key == K_RIGHT ):

                        update = True

                        # Bottom of the list of slots: Jumps to the top
                        if menu_pos == len(all_recipe_data) - 1:
                            menu_pos = 0
                            offset = 0

                        # Bottom of the interval, advance the offset by 1
                        elif menu_pos == offset + max_slots - 1:
                            offset += 1
                            menu_pos += 1

                        # intermediate interval: move the cursor only down by 1
                        elif menu_pos < len(all_recipe_data) - 1:
                            menu_pos += 1

                    if (event.key == K_z or event.key == K_RETURN):

                        # Verifies if a recipe can be used
                        can_make = self.engine.spell_recipes_catalog[all_recipe_data[menu_pos]['spell_name']].check_ingredients(self.engine.player.treasures)

                        if can_make:
                            self.confirm_recipe_menu(all_recipe_data, all_spells, offset, menu_pos)
                            # Gets Updated Recipe Data
                            all_recipe_data = self.get_all_recipe_data()
                            update = True

                    if event.key == K_x:
                        menu_flag = False

            if menu_flag:

                if update:
                    update = False
                    # Background image
                    self.engine.surface.blit(self.engine.stats_bg, (0, 0))

                    # Draws recipes, required and available ingredients on the left
                    # and the currently selected spell on the right.
                    self.draw_recipe_inventory(all_recipe_data, offset, menu_pos)
                    self.draw_required_ingredients(all_recipe_data[menu_pos])
                    self.draw_ingredient_inventory()
                    if len(all_recipe_data) > max_slots:
                        self.draw_scroll_bar(all_recipe_data, offset)
                    self.engine.draw_spell_action_data(all_spells[menu_pos])

                    pygame.display.flip()
                self.engine.clock.tick(60)



    def confirm_recipe_menu(self, all_recipe_data, all_spells, offset, menu_pos):
        """
        # function name: recipe_create_menu
        # purpose: Player is given the option to confirm the creation of the spell from the recipe
        # Inputs: all_recipe_data, all_spells - data needed to draw the information on the menu
                  offset - current menu visible window offset
                  menu_pos - the position of the cursor for the previous screen

        """

        # Loads the recipe object
        recipe = self.engine.spell_recipes_catalog[all_recipe_data[menu_pos]['spell_name']]

        menu_flag = True # Only two positions, so we use True for Confirm and False for cancel
        confirm_action = True

        text_confirm = self.engine.section_font.render('Create', True, (0, 0, 0))
        text_cancel = self.engine.section_font.render('Cancel', True, (0, 0, 0))

        confirmation_panel = get_ui_panel((120, 105), border_color, panel_color)
        option_panel = get_ui_panel((95, 40), border_color, panel_color)

        update = True

        max_slots = 5

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    # Any arrow key press toggles between Confirm and Cancel
                    if ( event.key == K_UP or event.key == K_LEFT or event.key == K_DOWN or event.key == K_RIGHT ):
                        confirm_action = not confirm_action
                        update = True
                    if (event.key == K_z or event.key == K_RETURN) and confirm_action:
                        # Execute creation
                        self.engine.player.add_item(self.engine.spell_catalog[recipe.spell_action].construct_spell())
                        # Remove used items
                        [self.engine.player.remove_treasure(ingredient, recipe.required_ingredients[ingredient]) for ingredient in recipe.required_ingredients.keys()]

                        self.engine.sfx_system.sound_catalog['levelup'].play()
                        return

                    if event.key == K_x or ((event.key == K_z or event.key == K_RETURN) and not confirm_action):
                        menu_flag = False
                        return False


            if menu_flag:
                if update:
                    update = False

                    # Draws all the previous screen's data
                    self.engine.surface.blit(self.engine.stats_bg, (0, 0))
                    self.draw_ingredient_inventory()
                    if len(all_recipe_data) > max_slots:
                        self.draw_scroll_bar(all_recipe_data, offset)
                    self.draw_recipe_inventory(all_recipe_data, offset, menu_pos)
                    self.draw_required_ingredients(all_recipe_data[menu_pos])
                    self.engine.draw_spell_action_data(all_spells[menu_pos])

                    # Draws a confirmation window with Create / Cancel as options
                    self.engine.surface.blit(confirmation_panel, (405 - confirmation_panel.get_width()/2, 70 + 65*(menu_pos-offset)))
                    self.engine.surface.blit(option_panel, (405 - option_panel.get_width()/2, 80 + 65*(menu_pos-offset)))
                    self.engine.surface.blit(text_confirm, (405 - text_confirm.get_width()/2,
                                                            82 + option_panel.get_height()/2 - text_confirm.get_height()/2 + 65*(menu_pos-offset)))
                    self.engine.surface.blit(option_panel, (405 - option_panel.get_width()/2, 125 + 65*(menu_pos-offset)))
                    self.engine.surface.blit(text_cancel, (405 - text_cancel.get_width()/2,
                                                            127 + option_panel.get_height()/2 - text_cancel.get_height()/2 + 65*(menu_pos-offset)))

                    if confirm_action:
                        cursor_y = 78 + 65*(menu_pos-offset)
                    else:
                        cursor_y = 123 + 65*(menu_pos-offset)

                    # Draws teh cursor for the create / cancel window
                    padlib_rounded_rect(self.engine.surface, selected_color, (403 - option_panel.get_width()/2,
                                                                      cursor_y,
                                                                      option_panel.get_width() + 4,
                                                                      option_panel.get_height() + 4), 6, 5)
                    pygame.display.flip()
                self.engine.clock.tick(60)


    def draw_recipe_inventory(self, all_recipe_data, offset, menu_pos):

        """
        draw_recipe_inventory

        purpose: draws a list of available recipes

        inputs: all_recipe_data - a list of recipe names and ingredients to draw
                offset - current offset of the visible items window
                menu_pos - current position of selected recipe

        """


        max_slots = 5

        recipe_panel = get_ui_panel((300, 50), border_color, panel_color)
        # draws all the recipes within the visible window
        for index, all_recipe_data in enumerate(all_recipe_data[offset:offset+max_slots]):

            self.engine.surface.blit(recipe_panel, (210 - recipe_panel.get_width()/2, 50 + 65*index))
            self.engine.surface.blit(all_recipe_data['name'], (210 - all_recipe_data['name'].get_width()/2,
                                       50 + recipe_panel.get_height()/2 - all_recipe_data['name'].get_height()/2 +65*index))

        # Draws the cursor for the inventory

        padlib_rounded_rect(self.engine.surface, selected_color, (210 - recipe_panel.get_width()/2 - 2,
                                                                  50 + 65*(menu_pos - offset) - 2,
                                                                  recipe_panel.get_width() + 4,
                                                                  recipe_panel.get_height() + 4), 6, 5)

    def draw_scroll_bar(self, all_recipe_data, offset):


        """
        draw_scroll_bar

        purpose: draws a scroll bar

        inputs: all_recipe_data - a list of recipe names and ingredients to draw
                offset - current offset of the visible items window
                menu_pos - current position of selected recipe

        """
        max_slots = 5
        scroll_bar_total = 65 * max_slots - 15

        scroll_bar = get_ui_panel((20, scroll_bar_total), border_color, panel_color)

        # Calculates the length of the scroll bar section and how far the spacing is
        #scroll_length = scroll_bar_total*max_slots/(len(all_recipe_data) - max_slots)
        scroll_length = scroll_bar_total*max_slots/(len(all_recipe_data))
        scroll_delta = (scroll_bar_total - scroll_length) / (len(all_recipe_data) - max_slots)

        scroll_bar_section = get_ui_panel((20, scroll_length), border_color, scroll_bar_color)

        self.engine.surface.blit(scroll_bar, (410, 50))

        # Special case to clamp the scroll bar at the bottom of the screen to correct for round off
        if offset == len(all_recipe_data) - max_slots:
            self.engine.surface.blit(scroll_bar_section, (410, 50 + scroll_bar_total - scroll_bar_section.get_height()))
        else:
            self.engine.surface.blit(scroll_bar_section, (410, 50 + scroll_delta * offset))

    def draw_required_ingredients(self, selected_recipe_data):

        """
        draw_recipe_ingredients

        purpose: Draws the (at most 2) different types of ingredients that are needed for this recipe

        inputs: selected_recipe_data - recipe names and ingredients to draw for a selected recipe
        """

        items_required_panel = get_ui_panel((300, 55), border_color, panel_color)

        item_panel = get_ui_panel((80, 35), border_color, panel_color)
        disabled_item_panel = get_ui_panel((80, 35), border_color, disabled_color)

        text_uses = self.engine.speaker_font.render("Uses:", True, (0, 0, 0))

        self.engine.surface.blit(items_required_panel, (210 - items_required_panel.get_width()/2, 370))

        for ing_index, ingredient in enumerate(selected_recipe_data['ingredients']):
            ingredient_icon = self.engine.icons[ingredient[0]]

            # Diferent centering is used if 1 ingredient vs 2 ingredients.
            if len(selected_recipe_data['ingredients']) > 1:
                self.engine.surface.blit(text_uses, (245  - items_required_panel.get_width()/2, 370 + items_required_panel.get_height()/2 - text_uses.get_height()/2))
                ing_x = 210 + items_required_panel.get_width()/2 - 10 - (1+ing_index)*(item_panel.get_width()+10)
                ing_y = 380
            else:
                self.engine.surface.blit(text_uses, (280  - items_required_panel.get_width()/2, 370 + items_required_panel.get_height()/2 - text_uses.get_height()/2))
                ing_x = 220
                ing_y = 380

            # Checks if enough ingredients are available:
            if ingredient[2]:
                self.engine.surface.blit(item_panel, (ing_x, ing_y))
            else:
                self.engine.surface.blit(disabled_item_panel, (ing_x, ing_y))

            self.engine.surface.blit(ingredient_icon, (ing_x + item_panel.get_width()/3 - ingredient_icon.get_width()/2,
                                                       ing_y + item_panel.get_height()/2 - ingredient_icon.get_height()/2))
            self.engine.surface.blit(ingredient[1], (ing_x  + 5 + item_panel.get_width()*2/3 - ingredient[1].get_width()/2,
                                                       ing_y + item_panel.get_height()/2 - ingredient[1].get_height()/2))

    def draw_ingredient_inventory(self):
        """
        draw_ingredient_inventory

        Purpose: Draws the number of ingredients available at the bottom of the synth screen

        """

        treasure_list = ['synth_wood', 'synth_metal', 'synth_fire', 'synth_earth', 'synth_water']

        available_quantities = []

        # Generate quantity indicators
        for item in treasure_list:
            if item in self.engine.player.treasures.keys():

                available_quantities.append(self.engine.data_font.render("%d"%self.engine.player.treasures[item], True, (0, 0, 0)))
            else:
                available_quantities.append(self.engine.data_font.render("0", True, (0, 0, 0)))

        text_ingredients = self.engine.speaker_font.render("Synthesis Crystals", True, (0, 0, 0))

        inventory_panel = get_ui_panel((300, 140), border_color, panel_color)
        item_panel = get_ui_panel((80, 35), border_color, panel_color)

        self.engine.surface.blit(inventory_panel, (210-inventory_panel.get_width()/2, 440))
        self.engine.surface.blit(text_ingredients, (210-text_ingredients.get_width()/2, 445))

        # Distributes the item panel in 3 items on the top row, 2 items on the second row
        item_positions = [ (210 - item_panel.get_width()*3/2 - 10, 480),
            (210 - item_panel.get_width()/2, 480),
            (210 + item_panel.get_width()/2 + 10, 480),
            (210 - item_panel.get_width() - 10, 530),
            (210 + 10, 530)
        ]


        # Draws each of the inventory items
        for index, item in enumerate(treasure_list):

            item_x, item_y = item_positions[index]
            self.engine.surface.blit(item_panel, (item_x, item_y))
            icon = self.engine.icons[self.engine.treasure_catalog[item].icon]
            text_quantity = available_quantities[index]

            self.engine.surface.blit(icon, (item_x + item_panel.get_width()/3 - icon.get_width()/2,
                                            item_y + item_panel.get_height()/2 - icon.get_height()/2))
            self.engine.surface.blit(text_quantity, (item_x + 5 + item_panel.get_width()*2/3 - text_quantity.get_width()/2,
                                                     item_y + item_panel.get_height()/2 - text_quantity.get_height()/2))

    def add_recipe(self, spell_name):
        """
        # function name: add recipe
        # purpose: Adds a recipe to the list of known recipes
        """
        self.engine.player.known_recipes.append(spell_name)
        self.engine.player.known_recipes.sort()


    def tutorial_basic(self):
        """
        tutorial_basic

        Purpose: Shows the player some information about how to use spell synthesis
        """

        self.say("You wanted to learn about spell synthesis, right?", "Marisa", "Marisa")
        self.say("Yes, how does it work?", "Youmu", "Youmu")
        self.say("Youmu, have you ever done much cooking?", "Marisa", "Marisa")
        self.say("Of course. I prepare meals for Lady Yuyuko all the time.", "Youmu", "Youmu")
        self.say("Okay then, it should be a snap for you. First off, let's begin with the elemental crystals.", "Marisa", "Marisa")
        self.say("Elemental crystals are our basic ingredients to synthesize spells. They're like your meats, vegetables, and grains in cooking.", "Marisa", "Marisa")
        self.say("What are these elemental crystals anyway?", "Youmu", "Youmu")
        self.say("Elemental crystals contain large amounts of pure magical energy, each corresponding to one of the basic classes of magic.", "Ran", "Ran")
        self.say("There are also more rare crystals that contain special magical properties. They can't be used directly so we have to use them to form our basic spells. The way we do this is with a spell recipe.", "Ran", "Ran")
        self.say("Since creating a spell is a complicated process, we need to rely on a recipe to create them. This tells us what steps we need to take to combine the elemental crystals.", "Marisa", "Marisa")
        self.say("Some recipes will specify one ingredient like the very basic spells. More advanced spells will specify multiple crystal types you need, so keep an eye out for ways to obtain them.", "Marisa", "Marisa")
        self.say("Basic ones are common, but it'll be harder to find the rarer special crystals.", "Marisa", "Marisa")
        self.say("For instance to forge a Fireball spell we use the recipe for that spell to create an equippable spell item. Remember to equip the spell after use, and check any new recipes we may get on our travels.", "Ran", "Ran")
        self.say("That's all there is to it. Select the recipe, and the spell is instantly created for you. This concludes the basic spell creation tutorial.", "Tutorial")


    def get_all_recipe_data(self):
        """
        # function name: get recipe data
        # purpose: constructs the recipe data for all known recipes
        """

        if not self.engine.unlock_shops:
            all_recipe_data = [self.get_recipe_data(self.engine.spell_recipes_catalog[recipe_name])
                                for recipe_name in self.engine.player.known_recipes]
        else:
            all_recipe_data = [self.get_recipe_data(recipe) for recipe in
                               self.engine.spell_recipes_catalog.values()]
        return all_recipe_data

    def get_recipe_data(self, recipe):
        """
        # function name: get recipe data
        # purpose: constructs the recipe data for a single recipes
        """

        recipe_data = { 'spell_name':recipe.spell_action,
                        'name':self.engine.section_font.render(recipe.spell_action, True, (0, 0, 0)),
                        'ingredients':[],
                        }
        # How many of each ingredient is required, as well as how much is in the player's inventory
        for ingredient in recipe.required_ingredients.keys():

            # Required ingredients
            # Returns ingredient in black text if player has enough of that item, in red if they don't
            if ingredient in self.engine.player.treasures.keys() and self.engine.player.treasures[ingredient] >= recipe.required_ingredients[ingredient]:
                recipe_data['ingredients'].append(
                    [self.engine.treasure_catalog[ingredient].icon,
                    self.engine.data_font.render(str(recipe.required_ingredients[ingredient]), True, (0, 0, 0, )),
                    True])

            else:
                recipe_data['ingredients'].append(
                    [self.engine.treasure_catalog[ingredient].icon,
                    self.engine.data_font.render(str(recipe.required_ingredients[ingredient]), True, (0, 0, 0, )),
                    False])

        return recipe_data

class Recipe(object):

    def __init__(self, spell_action, required_ingredients):
        """
        # function name: __init__
        # purpose: creates a spell recipe
        # inputs:   spell_action - The spell produced from this recipe
        #           required_ingredients - the required ingredients for this spell
        """

        self.spell_action = spell_action
        # Format: {ingredient:quantity}
        self.required_ingredients = required_ingredients

    def check_ingredients(self, treasure_inventory):
        """
        # function name: check_ingredients
        # purpose: checks if player can create this item
        # inputs:  treasure_inventory - player treasure inventory
        # Outputs: True if recipe can be created
        #          False if recipe cannot be created
        """

        for ingredient in self.required_ingredients.keys():

            if ingredient not in treasure_inventory.keys() or treasure_inventory[ingredient] < self.required_ingredients[ingredient]:
                # At least one condition has not been satisfied to create the item, return False
                return False

        # Condition satisfied, return True
        return True
