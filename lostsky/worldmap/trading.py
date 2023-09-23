
# Trading system
import os
import pygame
from pygame.locals import *
from lostsky.core.utils import split_lines, get_ui_panel, padlib_rounded_rect, draw_aligned_text
from lostsky.core.colors import border_color, selected_color, panel_color, scroll_bar_color, disabled_color
from sys import exit

class TradingSystem(object):
    """
    # Top Level Trading System Manager
    # Handles:
    #       - Manages and keeps up to date all trading information
    #       - Allows viewing of trade items
    #       - Displays Misc Messages from the shop owner
    """

    def __init__(self, engine):
        """
        # Function name: __init__
        # Purpose: Creates trading system object
        # Inputs: engine - top level engine
        """

        # link with engine
        self.engine = engine
        # Load shopkeeper image
        self.rinnosuke = pygame.image.load(os.path.join("images", "rinnosuke_shop.png")).convert_alpha()
        # A list of available trades
        self.available_trades = []
        self.available_specials = []

    def update_available_trades(self):
        """
        # Function name: update available trades
        # Purpose: Updates the current list of available trades
        """
        trade_list = []

        for trade in self.engine.trading_catalog.trading_list.values():
            # trade_available =  self.engine.check_event_completion(trade.prereqs)

            trade_available = True
            if trade_available and trade.id_string not in self.engine.player.trading_data['non_repeatable']:



                trade_list.append((trade.id_string,trade))
                trade_list.sort()

        if trade_list:
            _, self.available_trades = zip(*trade_list)
        else:
            self.available_trades = []

        # Find the next available milestone
        num_recovered = len(self.engine.player.trading_data['found_treasures'])
        for index, goals in enumerate(self.engine.trading_catalog.milestones):
            if goals > num_recovered:
                self.engine.player.trading_data['next_milestone'] = index
                break

        else:
            self.engine.player.trading_data['next_milestone'] = None



    def verify_trade(self, trade):
        """
        # Function name: verify_trade
        # Purpose: Verifies that a trade can be performed
        # Inputs: treasure_inventory: Player's treasure inventory
        # Outputs: can_trade = True if player can perform this trade, false otherwise
        """

        can_trade = True
        for item_wanted in trade.wanted:

            # Case: Player either does not have the treasure or player does not have the item in sufficient quantities
            if item_wanted['id_string'] not in self.engine.player.treasures.keys() or (item_wanted['id_string'] in self.engine.player.treasures.keys() and item_wanted['quantity'] > self.engine.player.treasures[item_wanted['id_string']]):
                can_trade = False

            # Case: Player has item in sufficient quantities
            elif item_wanted['quantity'] < self.engine.player.treasures[item_wanted['id_string']]:

                can_trade = True

        return can_trade


    def execute_trade(self, trade):

        """
        # Function name: execute trade
        # Purpose: Performs the trade
        # Inputs: trade - trade to be performed
        """

        # Removes wanted items
        [self.engine.player.remove_treasure(item_wanted['id_string'], item_wanted['quantity']) for item_wanted in trade.wanted]
        [self.engine.player.trading_data['found_treasures'].append(item_wanted['id_string']) for item_wanted in trade.wanted
        if self.engine.treasure_catalog[item_wanted['id_string']].type == "Generic" and
        item_wanted['id_string'] not in self.engine.player.trading_data['found_treasures']]

        # Adds offered items
        for item_offered in trade.offered:
            if item_offered['item_type'] == 'treasure':
                self.engine.player.add_treasure(item_offered['item_id'], item_offered['quantity'])
            else:
                [self.engine.player.add_item(self.engine.spell_catalog[item_offered['item_id']].construct_spell()) for counter in xrange(0, item_offered['quantity'])]


        if self.engine.player.trading_data['next_milestone'] != None:
            current_milestone = self.engine.trading_catalog.milestones[self.engine.player.trading_data['next_milestone']]

        # Checks if the next treasure collection milestone has been reached
        if self.engine.player.trading_data['next_milestone'] != None and len(self.engine.player.trading_data['found_treasures']) == current_milestone:
            current_reward = self.engine.trading_catalog.rewards[self.engine.player.trading_data['next_milestone']]

            self.say("Congratulations, you've reached another milestone!")
            self.say(current_reward['desc'])

            for reward in current_reward['items_given']:
                # Gives a treasure
                if reward['item_type'] == 'treasure':
                    self.engine.player.add_treasure(reward['item_id'], reward['quantity'])
                    self.say("I'll give you this item as a reward: %s x%s"%(self.engine.treasure_catalog[reward['item_id']].name,
                                                 str(reward['quantity'])))

                # Gives a spell item
                else:
                    for counter in xrange(0, reward['quantity']):
                        spell_reward = self.engine.spell_catalog[reward['item_id']].construct_spell()
                        self.engine.player.add_item(spell_reward)
                    self.say("I'll give you this item as a reward: %s x%s"%(spell_reward.name,
                             str(reward['quantity'])))
            # Goes to next treasure
            self.engine.player.trading_data['next_milestone'] += 1
            # All rewards have been given
            if self.engine.player.trading_data['next_milestone'] >= len(self.engine.trading_catalog.rewards):
                self.engine.player.trading_data['next_milestone'] = None

        if not trade.repeatable:
            self.engine.player.trading_data['non_repeatable'].append(trade.id_string)

    def render_shop_menu(self):
        """
        # Function name: render_shop_menu
        # Purpose: Draws the main menu for the shop
        """

        text_menu_header = self.engine.speaker_font.render("Kourindou Shop", True, (0, 0, 0))

        text_options = [self.engine.section_font.render("View Trades", True, (0, 0, 0)),
                   self.engine.section_font.render("Recovered Items", True, (0, 0, 0)),
                   self.engine.section_font.render("Cancel", True, (0, 0, 0))]

        header_panel = get_ui_panel((300, 40), border_color, panel_color)
        option_panel = get_ui_panel((250, 40), border_color, panel_color)

        # Background image
        self.engine.surface.blit(self.engine.shop_bg, (0, 0))
        self.engine.surface.blit(self.rinnosuke, (70, 280))
        self.engine.surface.blit(self.engine.text_board, (0, 490))

        # Renders the options
        self.engine.surface.blit(header_panel, (210 - header_panel.get_width()/2, 45) )
        self.engine.surface.blit(text_menu_header, (210  - text_menu_header.get_width()/2,
                                                    45 + header_panel.get_height()/2 - text_menu_header.get_height()/2))

        for index, text_option in enumerate(text_options):
            self.engine.surface.blit(option_panel, (210 - option_panel.get_width()/2, 95 + index*50) )
            self.engine.surface.blit(text_option, (212  - text_option.get_width()/2,
                                                    97 + index*50 + option_panel.get_height()/2 - text_option.get_height()/2))



    def say(self, lines):

        """
        # Function name: say
        # Purpose: Displays a line of text and awaits for the player to press Z to continue
        # Inputs: lines = The string of text to be displayed
        """

        menu_flag = True
        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_z or event.key == K_RETURN:
                        menu_flag = False
            if menu_flag:
                self.render_shop_menu()

                # Draws the message
                self.engine.draw_conversation_message(lines, "Rinnosuke")
                pygame.display.flip()
                self.engine.clock.tick(60)

    def draw_treasure_data(self, treasure_key):

        """
        # Function name: draw_treasure_data
        # Purpose: draws information about a single treasure
        """


        small_icon_panel = get_ui_panel((41, 41), border_color, panel_color)
        item_panel = get_ui_panel((260, 41), border_color, panel_color)
        desc_panel = get_ui_panel((320, 180), border_color, panel_color)

        treasure_data = self.get_single_treasure_data(treasure_key)


        self.engine.surface.blit(small_icon_panel, (470, 100))
        self.engine.surface.blit(self.engine.icons[treasure_data[0]], (470 + small_icon_panel.get_width()/2 - self.engine.icons[treasure_data[0]].get_width()/2,
                                                           100 + small_icon_panel.get_height()/2 - self.engine.icons[treasure_data[0]].get_height()/2))

        self.engine.surface.blit(item_panel, (530, 100))
        self.engine.surface.blit(treasure_data[1], (530 + item_panel.get_width()/2 - treasure_data[1].get_width()/2,
                                                     102 + item_panel.get_height()/2 - treasure_data[1].get_height()/2))

        self.engine.surface.blit(desc_panel, (470, 150))
        draw_aligned_text(self.engine.surface, treasure_data[2], self.engine.message_font, (0, 0, 0), (480, 160), 300 )

        # text_treasure = self.engine.bfont.render("Treasure", True, (0, 0, 0))
        # text_desc = self.engine.bfont.render("Description", True, (0, 0, 0))
        # # Renders currently selected treasure data
        # self.engine.surface.blit(text_single_treasure_data[0], (470, 50))
        # self.engine.surface.blit(text_treasure, (470, 70))
        # self.engine.surface.blit(text_desc, (480, 110))
        # [self.engine.surface.blit(line, (490, 130+index*20)) for index, line in enumerate(text_single_treasure_data[1])]

    def get_single_treasure_data(self, treasure_key):

        """
        # Function Name: get_single_treassure_data
        # Purpose: Generates the text objects of the currently selected treasure in the inventory
        # Inputs: treasure_key - relevant treasure key
        """

        treasure_data = []
        # Format (Text objects)
            # [big_name, description]
        treasure_data.append(self.engine.treasure_catalog[treasure_key].icon)
        treasure_data.append(self.engine.section_font.render(self.engine.treasure_catalog[treasure_key].name, True, (0, 0, 0)))
        treasure_data.append(self.engine.treasure_catalog[treasure_key].desc)
        return treasure_data

    def trading_menu(self):

        """
        # Function name: trading_menu
        # Purpose: Top level trading menu
        """

        self.update_available_trades()

        menu_flag = True
        update = True
        menu_pos = 0

        self.intro()

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
                            menu_pos = 2

                        update = True
                    if ( event.key == K_DOWN or event.key == K_RIGHT ):
                        if menu_pos < 2:
                            menu_pos += 1
                        elif menu_pos == 2:
                            menu_pos = 0

                        update = True
                    if event.key == K_z or event.key == K_RETURN:

                        # Ordinary trades
                        if menu_pos == 0:
                            self.select_trade_menu()
                            update = True

                        # Treasure Collection
                        elif menu_pos == 1:
                            self.treasure_collection()
                            update = True

                        # Exit
                        elif menu_pos == 2:
                            return

                    if event.key == K_x:
                        return
            if update:
                update = False
                self.render_shop_menu()

                # Draws the cursor
                padlib_rounded_rect(self.engine.surface, selected_color, (83, 93+50*menu_pos, 254, 44), 6, 5)

                pygame.display.flip()
            self.engine.clock.tick(60)

    def intro(self):

        """
        # Function name: intro
        # Purpose: rinnosuke's introductory speech
        """

        if self.engine.player.trading_data['first_time']:
            self.say("Welcome to Kourindou!")
            self.say("Here you can trade treasures that you've found for useful items.")
            self.say("As the number of treasures returned increases, I have some special rewards for you.")
            self.engine.player.trading_data['first_time'] = False
        else:
            self.say("Welcome to Kourindou!")
            self.say("I have some great deals on trades.")

    def select_trade_menu(self):

        """
        # Function name: select_trade_menu
        # Purpose: allows the player to view all the available trades
        """

        update = True
        menu_flag = True
        menu_pos = 0
        offset = 0
        max_slots = 7

        self.update_available_trades()

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if ( event.key == K_UP or event.key == K_LEFT ) and self.available_trades:

                        update = True

                        # Top of the list, jump to the bottom
                        if menu_pos == 0:
                            menu_pos = len(self.available_trades)-1
                            offset = max(0, len(self.available_trades) - max_slots)

                        # Top of the itnerval, shift offset up
                        elif menu_pos == offset:
                            menu_pos -= 1
                            offset -= 1

                        # within interval, move cursor without changing shift
                        elif menu_pos > 0:
                            menu_pos -= 1

                    if ( event.key == K_DOWN or event.key == K_RIGHT ) and self.available_trades:

                        update = True

                        # Bottom of the list of slots: Jumps to the top
                        if menu_pos == len(self.available_trades) - 1:
                            menu_pos = 0
                            offset = 0

                        # Bottom of the interval, advance the offset by 1
                        elif menu_pos == offset + max_slots - 1:
                            offset += 1
                            menu_pos += 1

                        # intermediate interval: move the cursor only down by 1
                        elif menu_pos < len(self.available_trades) - 1:
                            menu_pos += 1

                    if event.key == K_z and self.available_trades:
                        self.confirmation_menu(menu_pos, offset)
                        self.update_available_trades()
                        if menu_pos >= len(self.available_trades) - 1:
                            menu_pos = len(self.available_trades) - 1


                        update = True

                    if event.key == K_x:
                        menu_flag = False

            if update:
                update = False

                self.engine.surface.blit(self.engine.stats_bg, (0, 0))
                self.draw_trade_list(offset)
                self.draw_trade_scrollbar(offset)
                if self.available_trades:
                    self.draw_trade_information(self.available_trades[menu_pos])
                    # Draws the cursor for the selected trade
                    padlib_rounded_rect(self.engine.surface, selected_color, (208 - 150, 98 + 60*(menu_pos - offset), 304, 44), 6, 5)

                pygame.display.flip()
            self.engine.clock.tick(60)

    def draw_trade_list(self, offset):
        """

        function name: draw_trade_list

        purpose: draws the entries for the trades list within the viewing window

        input: offset - current window offset for the trade list

        """

        option_panel = get_ui_panel((300, 40), border_color, panel_color)
        top_panel = get_ui_panel((340, 40), border_color, panel_color)
        text_header = self.engine.speaker_font.render("Available Trades", True, (0, 0, 0))

        max_slots = 7

        # draws the header
        self.engine.surface.blit(top_panel, (210 - top_panel.get_width()/2, 45))
        self.engine.surface.blit(text_header, (210 - text_header.get_width()/2,
                                               45 + top_panel.get_height()/2 - text_header.get_height()/2))

        # Draws all the trades within the viewing window
        for index, trade in enumerate(self.available_trades[offset:min(offset+max_slots, len(self.available_trades))]):

            text_trade = self.engine.section_font.render(trade.name, True, (0, 0, 0))

            self.engine.surface.blit(option_panel, (210 - option_panel.get_width()/2, 100 + 60*index))
            self.engine.surface.blit(text_trade, (212 - text_trade.get_width()/2,
                                                  102 + option_panel.get_height()/2 - text_trade.get_height()/2 + 60*index))


    def draw_trade_scrollbar(self, offset):
        """
        function name: draw_trade_scrollbar

        purpose: draws the scrollbar for the trades list

        input: offset - current window offset for the trade list
        """

        max_slots = 7

        # Only draws scrollbar if list is too long
        if len(self.available_trades) <= max_slots:
            return

        scroll_bar_total = 60 * max_slots - 20

        scroll_bar = get_ui_panel((20, scroll_bar_total), border_color, panel_color)

        # Calculates the length of the scroll bar section and how far the spacing is
        scroll_length = scroll_bar_total*max_slots/(len(self.available_trades))
        scroll_delta = (scroll_bar_total - scroll_length) / (len(self.available_trades) - max_slots)

        scroll_bar_section = get_ui_panel((20, scroll_length), border_color, scroll_bar_color)

        self.engine.surface.blit(scroll_bar, (410, 100))

        # Special case to clamp the scroll bar at the bottom of the screen to correct for round off
        if offset == len(self.available_trades) - max_slots:
            self.engine.surface.blit(scroll_bar_section, (410, 100 + scroll_bar_total - scroll_bar_section.get_height()))
        else:
            self.engine.surface.blit(scroll_bar_section, (410, 100 + scroll_delta * offset))

    def draw_trade_information(self, trade):
        """
        function name: draw_trade_information

        purpose: draws the data (description, items wanted, items offered) for this trade

        inputs: trade - the trade object to draw

        """


        section_panel = get_ui_panel((330, 40), border_color, panel_color)
        desc_panel = get_ui_panel((330, 160), border_color, panel_color)
        item_panel = get_ui_panel((220, 41), border_color, panel_color)
        disabled_item_panel = get_ui_panel((220, 41), border_color, disabled_color)
        small_icon_panel = get_ui_panel((41, 41), border_color, panel_color)
        text_title = self.engine.speaker_font.render(trade.name, True, (0, 0, 0))
        text_wanted = self.engine.section_font.render("Items Wanted", True, (0, 0, 0))
        text_rewards = self.engine.section_font.render("Rewards", True, (0, 0, 0))

        # Draws the trade's name at the top
        self.engine.surface.blit(section_panel, (630 - section_panel.get_width()/2, 45))
        self.engine.surface.blit(text_title, (630 - text_title.get_width()/2,
                                              45 + section_panel.get_height()/2 - text_title.get_height()/2))

        # Draws the description of the trade
        self.engine.surface.blit(desc_panel, (630 - desc_panel.get_width()/2, 100))
        draw_aligned_text(self.engine.surface, trade.desc, self.engine.sfont, (0, 0, 0), (640 - desc_panel.get_width()/2, 110), desc_panel.get_width() - 20)

        # Draws the list of items wanted, their icon, and the number of items wanted
        wanted_items_y_position = 320
        index = 0
        self.engine.surface.blit(section_panel, (630 - section_panel.get_width()/2, wanted_items_y_position - 50))
        self.engine.surface.blit(text_wanted, (630 - text_wanted.get_width()/2,
                                              wanted_items_y_position - 50 + section_panel.get_height()/2 - text_wanted.get_height()/2))
        for index, wanted_item in enumerate(trade.wanted):
            item_object = self.engine.treasure_catalog[wanted_item['id_string']]
            item_icon = self.engine.icons[item_object.icon]
            text_quantiy = self.engine.data_font.render("%d"%wanted_item['quantity'], True, (0, 0, 0))
            text_name = self.engine.message_font.render(item_object.name, True, (0, 0, 0))

            self.engine.surface.blit(small_icon_panel, (470, wanted_items_y_position + index*50))
            self.engine.surface.blit(item_icon, (470 + small_icon_panel.get_width()/2 - item_icon.get_width()/2,
                                                 wanted_items_y_position + small_icon_panel.get_height()/2 - item_icon.get_height()/2 + index*50))

            if wanted_item['id_string'] in self.engine.player.treasures.keys() and self.engine.player.treasures[wanted_item['id_string']] >= wanted_item['quantity']:
                self.engine.surface.blit(item_panel, (520, wanted_items_y_position + index*50))
            else:
                self.engine.surface.blit(disabled_item_panel, (520, wanted_items_y_position + index*50))


            self.engine.surface.blit(text_name, (520 + item_panel.get_width()/2 - text_name.get_width()/2,
                                                 wanted_items_y_position + item_panel.get_height()/2 - text_name.get_height()/2 + index*50))
            self.engine.surface.blit(small_icon_panel, (750, wanted_items_y_position + index*50))
            self.engine.surface.blit(text_quantiy, (750 + small_icon_panel.get_width()/2 - text_quantiy.get_width()/2,
                                                 wanted_items_y_position + small_icon_panel.get_height()/2 - text_quantiy.get_height()/2 + index*50))

        # Determines the position of the offered items list based off of the number of items that are drawn in the previous section
        reward_list_y_offset = wanted_items_y_position + (index+1)*50 + 60

        # Draws the items that are offered, their icon, and the number of items offered
        self.engine.surface.blit(section_panel, (630 - section_panel.get_width()/2, reward_list_y_offset - 50))
        self.engine.surface.blit(text_rewards, (630 - text_rewards.get_width()/2,
                                              reward_list_y_offset - 50 + section_panel.get_height()/2 - text_rewards.get_height()/2))

        for index, reward_item in enumerate(trade.offered):

            # generates appropriate images for treasures and spell actions
            if reward_item['item_type'] == 'treasure':
                item_object = self.engine.treasure_catalog[reward_item['item_id']]
                item_icon = self.engine.icons[item_object.icon]
                text_quantiy = self.engine.data_font.render("%d"%reward_item['quantity'], True, (0, 0, 0))
                text_name = self.engine.message_font.render(item_object.name, True, (0, 0, 0))
            else:
                temp_spell = self.engine.spell_catalog[reward_item['item_id']].construct_spell()

                if temp_spell.type in ('healing', 'support'):
                    item_icon = self.engine.spell_type_icons['Healing']
                elif temp_spell.type == "healingitem":
                    item_icon = self.engine.spell_type_icons['Item']
                else:
                    item_icon = self.engine.spell_type_icons[temp_spell.affinity]

                text_quantiy = self.engine.data_font.render("%d"%reward_item['quantity'], True, (0, 0, 0))
                text_name = self.engine.message_font.render(reward_item['item_id'], True, (0, 0, 0))


            self.engine.surface.blit(small_icon_panel, (470, reward_list_y_offset + index*50))
            self.engine.surface.blit(item_icon, (470 + small_icon_panel.get_width()/2 - item_icon.get_width()/2,
                                                 reward_list_y_offset + small_icon_panel.get_height()/2 - item_icon.get_height()/2 + index*50))
            self.engine.surface.blit(item_panel, (520, reward_list_y_offset + index*50))
            self.engine.surface.blit(text_name, (520 + item_panel.get_width()/2 - text_name.get_width()/2,
                                                 reward_list_y_offset + item_panel.get_height()/2 - text_name.get_height()/2 + index*50))
            self.engine.surface.blit(small_icon_panel, (750, reward_list_y_offset + index*50))
            self.engine.surface.blit(text_quantiy, (750 + small_icon_panel.get_width()/2 - text_quantiy.get_width()/2,
                                                 reward_list_y_offset + small_icon_panel.get_height()/2 - text_quantiy.get_height()/2 + index*50))


    def confirmation_menu(self, list_pos, offset):
        """
        function name: confirmation_menu

        purpose: allows player to confirm they want to go forward with the trade

        inputs: list_pos - position of the selected trade in the list self.available_trades
                offset - current window offset for the trade list

        """

        update = True

        menu_pos = 0
        menu_flag = True

        confirm_panel = get_ui_panel((150, 120), border_color,  (220, 220, 70) )
        option_panel = get_ui_panel((130, 40), border_color,  panel_color )
        disabled_option_panel = get_ui_panel((130, 40), border_color,  disabled_color)
        text_confirm = self.engine.section_font.render("Confirm", True, (0, 0, 0))
        text_cancel = self.engine.section_font.render("Cancel", True, (0, 0, 0))

        while menu_flag:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                        if menu_pos == 1:
                            menu_pos = 0
                        else:
                            menu_pos = 1
                        update = True

                    if event.key == K_z:

                        if menu_pos == 0:

                            if self.verify_trade(self.available_trades[list_pos]):
                                self.engine.sfx_system.sound_catalog['levelup'].play()
                                self.execute_trade(self.available_trades[list_pos])

                                return

                        else:
                            return

                    if event.key == K_x:
                        return



            if update:
                update = False

                # All the information from the trade select screen is redrawn
                self.engine.surface.blit(self.engine.stats_bg, (0, 0))
                self.draw_trade_list(offset)
                self.draw_trade_scrollbar(offset)
                self.draw_trade_information(self.available_trades[list_pos])
                padlib_rounded_rect(self.engine.surface, selected_color, (208 - 150, 98 + 60*(list_pos - offset), 304, 44), 6, 5)

                # Draws a confirmation panel
                self.engine.surface.blit(confirm_panel, (295, 150+60*(list_pos - offset)))
                # Confirmation option: this is grayed out if trade cannot be executed
                if self.verify_trade(self.available_trades[list_pos]):
                    self.engine.surface.blit(option_panel, (305, 160+60*(list_pos - offset)))
                else:
                    self.engine.surface.blit(disabled_option_panel, (305, 160+60*(list_pos - offset)))
                self.engine.surface.blit(text_confirm, (305 + option_panel.get_width()/2 - text_confirm.get_width()/2,
                                                        162 + option_panel.get_height()/2 - text_confirm.get_height()/2 + 60*(list_pos - offset)))
                # Cancel option: always drawn
                self.engine.surface.blit(option_panel, (305, 220+60*(list_pos - offset)))
                self.engine.surface.blit(text_cancel, (305 + option_panel.get_width()/2 - text_cancel.get_width()/2,
                                                        222 + option_panel.get_height()/2 - text_cancel.get_height()/2 + 60*(list_pos - offset)))

                # Draws the cursor for the confirmation panel
                if menu_pos == 0:
                    padlib_rounded_rect(self.engine.surface, selected_color, (303, 158 + 60*(list_pos - offset), option_panel.get_width() + 4, option_panel.get_height()+4), 6, 5)
                else:
                    padlib_rounded_rect(self.engine.surface, selected_color, (303, 218 + 60*(list_pos - offset), option_panel.get_width() + 4, option_panel.get_height()+4), 6, 5)


                pygame.display.flip()
            self.engine.clock.tick(60)



    def treasure_collection(self):
        """
        function name: treasure_collection
        purpose: Display and examine a collection of returned treasures
        """

        text_menu_header = self.engine.section_font.render("Treasure Collection", True, (0, 0, 0))
        text_recovered = self.engine.section_font.render("Recovered", True, (0, 0, 0))
        text_bonus = self.engine.section_font.render("Next Milestone", True, (0, 0, 0))

        spacing = 50
        grid_size = spacing*4-(spacing - self.engine.unit_tile.get_width())
        item_grid_panel = get_ui_panel((grid_size + 40, grid_size*3/4 + 40), border_color, panel_color)
        title_panel = get_ui_panel((330, 40), border_color, panel_color)
        description_panel = get_ui_panel((250, 40), border_color, panel_color)
        data_panel = get_ui_panel((60, 40), border_color, panel_color)

        # Assembles list of treasures
        treasure_list = [treasure.id_string for treasure in self.engine.treasure_catalog.values()
                         if treasure.type == "Generic"]
        treasure_list.sort()

        # Calculates number of treasures found and the next milestone
        text_num_treasures = self.engine.data_font.render(str(len(self.engine.player.trading_data['found_treasures'])), True, (0, 0, 0))
        if self.engine.player.trading_data['next_milestone'] != None:
            text_next_milestone = self.engine.data_font.render(str(self.engine.trading_catalog.milestones[self.engine.player.trading_data['next_milestone']]), True, (0, 0, 0))
        else:
            text_next_milestone = self.engine.data_font.render("N/A", True, (0, 0, 0))
        menu_flag = True
        menu_pos = [0, 0]

        while menu_flag:
            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:

                    if event.key == K_UP:
                        if menu_pos[1] > 0:
                            menu_pos[1] -= 1
                        else:
                            menu_pos[1] = 2

                    if event.key == K_LEFT:
                        if menu_pos[0] > 0:
                            menu_pos[0] -= 1
                        else:
                            menu_pos[0] = 3

                    if event.key == K_DOWN:
                        if menu_pos[1] < 2:
                            menu_pos[1] += 1
                        else:
                            menu_pos[1] = 0

                    if event.key == K_RIGHT:
                        if menu_pos[0] < 3:
                            menu_pos[0] += 1
                        else:
                            menu_pos[0] = 0

                    if event.key == K_x:
                        menu_flag = False

            if menu_flag:

                # Background image
                self.engine.surface.blit(self.engine.stats_bg, (0, 0))

                # Header
                self.engine.surface.blit(title_panel, (210 - title_panel.get_width()/2, 45))
                self.engine.surface.blit(text_menu_header, (210 - text_menu_header.get_width()/2,
                                                            47 + title_panel.get_height()/2 - text_menu_header.get_height()/2))

                # Sets the x-position so that the 5x5 box is centered
                x0 = 210-grid_size/2
                y0 = 120

                # Treasures displayed as a 5x5 grid
                self.engine.surface.blit(item_grid_panel, (x0 - 20, y0 - 20))

                for y in xrange(0, 3):
                    for x in xrange(0, 4):
                        self.engine.surface.blit(self.engine.unit_tile, (x0+50*x, y0+50*y))

                        treasure_id = treasure_list[4*y+x]

                        if treasure_id in self.engine.player.trading_data['found_treasures']:
                            item_icon = self.engine.icons[self.engine.treasure_catalog[treasure_id].icon]
                            self.engine.surface.blit(item_icon,(x0 + self.engine.unit_tile.get_width()/2 - item_icon.get_width()/2 +spacing*x,
                                                                y0 + self.engine.unit_tile.get_height()/2 - item_icon.get_height()/2 +spacing*y))

                # Draws all the treasures
                if treasure_list[4*menu_pos[1]+menu_pos[0]] in self.engine.player.trading_data['found_treasures']:
                    self.draw_treasure_data(treasure_list[4*menu_pos[1]+menu_pos[0]])

                # Calculates the position of the number of treasures / milestone panels so they line up with the top panel
                description_x = 210 - title_panel.get_width()/2
                data_x = 210 + title_panel.get_width()/2 - data_panel.get_width()

                # Draws the two descriptions at the bottom of the screen
                self.engine.surface.blit(description_panel, (description_x, 350))
                self.engine.surface.blit(text_recovered, (description_x + description_panel.get_width()/2 - text_recovered.get_width()/2,
                                                              352 + description_panel.get_height()/2 - text_recovered.get_height()/2))
                self.engine.surface.blit(description_panel, (description_x, 410))
                self.engine.surface.blit(text_bonus, (description_x + description_panel.get_width()/2 - text_bonus.get_width()/2,
                                                              412 + description_panel.get_height()/2 - text_bonus.get_height()/2))

                # Draws the values for number of treasures and milestone
                self.engine.surface.blit(data_panel, (data_x, 350))
                self.engine.surface.blit(text_num_treasures, (data_x + data_panel.get_width()/2 - text_num_treasures.get_width()/2,
                                                              350 + data_panel.get_height()/2 - text_num_treasures.get_height()/2))

                self.engine.surface.blit(data_panel, (data_x, 410))
                self.engine.surface.blit(text_next_milestone, (data_x + data_panel.get_width()/2 - text_next_milestone.get_width()/2,
                                                              410 + data_panel.get_height()/2 - text_next_milestone.get_height()/2))


                # Draws cursor
                self.engine.surface.blit(self.engine.cursor_img, (x0+spacing*menu_pos[0], y0+50*menu_pos[1]))

                pygame.display.flip()
                self.engine.clock.tick(60)



class Trade(object):

    def __init__(self, name, id_string, desc, repeatable, prereqs, wanted, offered, ):


        """
        # Function name: __init__
        # Purpose: Creates a trade object
        # Inputs:
        #           name - the displayed name for the trade
        #           id_string - the key in the trade catalog
        #           desc - a description of the trade
        #           repeatable - T/F. if trade can only be done once
        #           prereqs - after what mission does this trade appear
        #           wanted - a list of items to be traded
        #           offered - a list of items that the player receives
        """

        self.name = name
        self.id_string = id_string
        self.desc = desc
        self.repeatable = repeatable
        self.prereqs = prereqs
        self.wanted = wanted
        self.offered = offered

