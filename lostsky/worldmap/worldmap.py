# World Map Class
# Map engine: "Gensokyo Navi"
import pygame
import os
from pygame.locals import *
from lostsky.core.linalg import Vector2
from lostsky.core.utils import draw_aligned_text, split_lines, padlib_rounded_rect, get_ui_panel
from lostsky.core.colors import border_color, panel_color, selected_color
from sys import exit

class Worldmap(object):

    def __init__(self, engine, region_list, region_path_list):
        """
        # Function Name: __init__
        # Purpose: Intializes world map
        # Inputs: Engine - Game system engine
        #         region_list - a list of regions in the world map
        """


        self.engine = engine
        engine.worldmap = self
        self.all_regions = {}
        self.all_regions_by_name = {}
        self.all_locations_by_name = {}
        self.conv_images = {}
        self.region_path_list = region_path_list
        self.background_surface = pygame.surface.Surface((840, 630))

        self.dot_positions = set()
        for region in region_list:
            self.all_regions[tuple(region.wm_coords)] = region
            self.all_regions_by_name[region.name] = region
            region.wm_parent = self
            for location in region.all_locations.values():
                self.all_locations_by_name[location.name] = location

        self.default_starting_pos = tuple(self.all_regions_by_name['Netherworld'].wm_coords)
        self.player_pos = Vector2(self.default_starting_pos)
        self.player_sprite_group = pygame.sprite.RenderUpdates()
        self.player_sprite = WorldmapSprite( 35*self.player_pos, self.engine.player_img)
        self.player_sprite_group.add(self.player_sprite)

        # Sets up connecting paths

        # List of all dots to not include a range around the region
        remove_pts = []
        for region in region_list:
            remove_pts.extend((tuple(region.wm_coords), tuple((region.wm_coords+Vector2(-1, 1))), tuple((region.wm_coords+Vector2(0, 1))), tuple((region.wm_coords+Vector2(0, 1)))))

        for path in region_path_list:

            # Each path has two connecting points along with the direction key to press to get to each location
            direction_to_1 = path.locations.keys()[0]
            region_1 = path.locations[direction_to_1]
            direction_to_2 = path.locations.keys()[1]
            region_2 = path.locations[direction_to_2]

            # We assign the starting point's path directions to this path so it can be called when the character needs to move
            self.all_regions_by_name[region_2].paths[direction_to_1] = path
            self.all_regions_by_name[region_1].paths[direction_to_2] = path

            # Constructs destination vectors
            delta_pos = self.all_regions_by_name[region_1].wm_coords - self.all_regions_by_name[region_2].wm_coords
            path.vectors[direction_to_1] = delta_pos
            path.vectors[direction_to_2] = -1*(delta_pos.copy())

            # # Decomposes delta vector into path dots for the map
            for i in xrange(min(1, int(delta_pos.y)), max(int(delta_pos.y), 0)):
                dot_vector = self.all_regions_by_name[region_2].wm_coords + Vector2(0, i)
                if tuple(dot_vector) not in remove_pts:
                    path.dot_positions.append(tuple(35*dot_vector))

            for j in xrange(min(1, int(delta_pos.x)), max(int(delta_pos.x), 0)):
                dot_vector = self.all_regions_by_name[region_2].wm_coords + Vector2(j, delta_pos.y)
                if tuple(dot_vector) not in remove_pts:
                    path.dot_positions.append(tuple(35*dot_vector))




        # Region connection paths
        self.unit_associate()

    ############################################
    # Computational Methods
    ############################################

    def unit_associate(self):

        """
        # Function Name: unit_associate
        # Purpose: Associates the unit's map attribute with the world map
        """

        for unit in self.engine.player_units:
            unit.map = self
            unit.in_battle = False

    def update_all_events(self):
        """
        # Function Name: unit_associate
        # Purpose: Associates the unit's map attribute with the world map
        # Outputs: new_mission = True/False if a new mission is available
        """

        # Clears out all location event data
        for location in self.all_locations_by_name.values():
            location.all_events = []

        # Clears out the available list
        self.engine.all_events_available = []
        self.engine.all_events_completed = []
        self.engine.all_events_sign_up = []

        # Updates all events
        for event in self.engine.all_events_master.values():

            # If event is done, add it to the list of completed events
            if event.done:
                event.available = False
                event.sign_up = False
                self.engine.all_events_completed.append(event)
                event.location = self.all_locations_by_name[event.location_name]
            else:

                # Updates availability of all events

                # Mission is added if no prerequisites are present or
                # all prerequisites are met
                if ((not event.prereq or self.engine.check_event_completion(event.prereq))
                    and not event.sign_up):

                    event.sign_up = True

                # if the event is signed up for add it to the world map
                if event.sign_up:
                    self.engine.all_events_sign_up.append(event)
                    self.all_locations_by_name[event.location_name].add_event(event)

            # Updates player data
            self.engine.player.all_event_data[event.event_id].update_from_event(event)
            self.update_all_paths()


    def update_all_paths(self):

        """
        # Function Name: update all paths
        # Purpose: Updates the unlocking of all the world map paths
        """

        for path in self.region_path_list:
            # A path is unlocked if there are no prerequisite missions or if all of these missions has been completed
            # The Engine's unlock_wm debug flag unlocks the whole map
            if self.engine.unlock_wm or not path.prereq or self.engine.check_event_completion(path.prereq):
                path.unlock = True
            else:
                path.unlock = False

        for region in self.all_regions.values():
            if self.engine.unlock_wm or not region.prereq or self.engine.check_event_completion(region.prereq):
                region.unlock = True
            else:
                region.unlock = False

            for path in region.location_path_list:
                # A path is unlocked if there are no prerequisite missions or if all of these missions has been completed
                # The Engine's unlock_wm debug flag unlocks the whole map
                if self.engine.unlock_wm or not path.prereq or self.engine.check_event_completion(path.prereq):
                    path.unlock = True
                else:
                    path.unlock = False
            for location in region.all_locations_by_name.values():
                if self.engine.unlock_wm or not location.prereq or self.engine.check_event_completion(location.prereq):
                    location.unlock = True
                else:
                    location.unlock = False



    def update_wm_player_data(self):

        """
        # Function Name: update wm player data
        # Purpose: Updates the location of the player
        """
        self.engine.player.wm_data['wm_coords'] = tuple(self.player_pos)
        self.engine.player.wm_data['in_region'] = False

    ############################################
    # Graphical Methods
    ############################################

    def render_background(self):

        """
        # Function Name: Render map to background surface
        # Purpose: Draws the background map and the locations
        """

        self.background_surface.blit(self.engine.wm_bg, (0, 0))
        self.background_surface.blit(self.engine.menu_board, (0, 490))

        for region in self.all_regions.values():
            draw_bubble = False
            # Checks if there is an event in the region
            for location in region.all_locations.values():
                if location.has_event():
                    draw_bubble = True
                    break

            if not region.unlock:
                self.background_surface.blit(self.engine.hidden_location_images[region.name], region.image_pos)

            elif region == self.all_regions[tuple(self.player_pos)]:
                self.background_surface.blit(self.engine.active_location_images[region.name], region.image_pos)
            else:
                self.background_surface.blit(self.engine.inactive_location_images[region.name], region.image_pos)

            if draw_bubble:
                self.background_surface.blit(self.engine.event_icon, (region.pix_coords+Vector2(25, -35)))


        name_panel = get_ui_panel((280, 45), border_color, panel_color)
        desc_panel = get_ui_panel((320, 60), border_color, panel_color)

        text_location_name = self.all_regions[tuple(self.player_pos)].name_big

        # Draws the description and name of the current region
        self.background_surface.blit(name_panel, (40, 505))
        self.background_surface.blit(text_location_name, (40 + name_panel.get_width()/2 - text_location_name.get_width()/2,
                                                          507 + name_panel.get_height()/2 - text_location_name.get_height()/2))

        self.background_surface.blit(desc_panel, (20, 555))

        self.draw_directions()

        draw_aligned_text(self.background_surface, self.all_regions[tuple(self.player_pos)].desc, self.engine.sfont,
                          (0, 0, 0), (30, 565), desc_panel.get_width()-20)


    def draw_directions(self):
        """
        function name: draw_directions

        Desc: Draw basic interaction directions on the world map
        """

        text_enter = self.engine.message_font.render("Z - Enter Region", True, (0, 0, 0))
        text_menu = self.engine.message_font.render("A - Main Menu", True, (0, 0, 0))

        panel = get_ui_panel((200, 35), border_color, panel_color)

        self.background_surface.blit(panel, (630 - panel.get_width()/2, 520))
        self.background_surface.blit(text_enter, (630 - text_enter.get_width()/2,
                                              520 + panel.get_height()/2 - text_enter.get_height()/2))

        self.background_surface.blit(panel, (630 - panel.get_width()/2, 565))
        self.background_surface.blit(text_menu, (630 - text_menu.get_width()/2 ,
                                              565 + panel.get_height()/2 - text_menu.get_height()/2))




    def render_arrows(self):

        """
        draw_arrows

        Draws the direction arrows for the unit on the main map screen.

        """

        # Draws arrows indicating where to move
        arrow_offset = {'up':Vector2(0, -35),
                     'down':Vector2(0, 35),
                     'left':Vector2(-35, 0),
                     'right':Vector2(35, 0)
                     }

        for direction in self.all_regions[tuple(self.player_pos)].paths.keys():
            if self.all_regions[tuple(self.player_pos)].paths[direction].unlock:

                arrow_coord = 35*self.player_pos + arrow_offset[direction]

                self.background_surface.blit(self.engine.direction_arrows[direction], arrow_coord)

    def render_updated_map(self, draw_arrows = True, fade_from = False):
        """
        Purpose: Updates the background surface and draws everything
        """
        self.render_background()
        if draw_arrows:
            self.render_arrows()

        self.engine.surface.blit(self.background_surface, (0, 0))
        self.player_sprite_group.update(self.player_pos*35)
        self.player_sprite_group.clear( self.engine.surface, self.background_surface)
        self.player_sprite_group.draw(self.engine.surface)

        if fade_from:

            self.engine.fade_from('black', 0.5)

        pygame.display.flip()
        self.engine.clock.tick(60)


    def move_to(self, direction_vector):
        """
        # Function Name: move to
        # Purpose: moves the player from point A to point B
        # Inputs: Destination - Where the player is going
        """

        # Smoothstep function
        # See: http://sol.gfxile.net/interpolation/
        smoothstep = lambda v: (v*v*(3-2*v))

        start_pos = 35*self.player_pos

        self.render_updated_map(draw_arrows = False)

        # Sets frame count proportional to the square root of the magnitude of the step vector
        frame_count = int(10*direction_vector.get_magnitude()**(1.0/2))

        for t in xrange(0, int(frame_count)+1):
            v = float(t)/float(frame_count)
            v = smoothstep(v)
            scale_term = int(35*v)
            intermediate_step = scale_term*direction_vector

            current_pos = start_pos + intermediate_step

            self.player_sprite_group.update(current_pos)
            self.player_sprite_group.clear( self.engine.surface, self.background_surface)
            rects = self.player_sprite_group.draw( self.engine.surface)

            pygame.display.update(rects)
            self.engine.clock.tick(60)

        self.player_pos += direction_vector

    ############################################
    # Interactive methods
    ############################################
    def say(self, line, speaker=""):

        """
        # Function name: say
        # Purpose: Displays a line of text and awaits for the player to press Z to continue
        # Inputs: string = The string of text to be displayed
        #         speaker = The name of the person saying it
        """

        text_speaker = self.engine.speaker_font.render(speaker, True, (0, 0, 0))

        menu_flag = True

        self.render_background()

        self.engine.surface.blit(self.background_surface, (0, 0))
        self.player_sprite_group.update(self.player_pos*35)
        self.player_sprite_group.clear( self.engine.surface, self.background_surface)
        self.player_sprite_group.draw(self.engine.surface)

        for conversation_image in self.conv_images.values():
            self.engine.surface.blit(conversation_image[0], conversation_image[1])

        self.engine.draw_conversation_message(line, speaker, None)

        pygame.display.flip()

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN and (event.key == K_z or event.key == K_RETURN):
                    menu_flag = False

            # Hold down C to skip through the dialog.
            keys = pygame.key.get_pressed()
            if keys[K_c]:
                menu_flag = False

            self.engine.clock.tick(60)

    def choice(self, query, responses):
        """
        # Function name: Choice
        # Purpose: Displays a question for the player to answer
        # Inputs: string = The string of text to be displayed (e.g. do you like pie?)
        #         responses = A list of (preferably less than 3) options given to the player
        # Output: the response selected from the given choices
        """

        menu_flag = True
        menu_pos = 0
        update = True


        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP or event.key == K_LEFT:
                        if menu_pos > 0:
                            menu_pos -= 1
                        elif menu_pos == 0:
                            menu_pos = len(responses)-1
                    if event.key == K_DOWN or event.key == K_RIGHT:
                        if menu_pos < len(responses)-1:
                            menu_pos += 1
                        elif menu_pos == len(responses)-1:
                            menu_pos = 0

                    if (event.key == K_z or event.key == K_RETURN):
                        menu_flag = False
                        return responses[menu_pos]

            if menu_flag:

                if update:
                    self.render_background()

                    self.engine.surface.blit(self.background_surface, (0, 0))
                    self.player_sprite_group.update(self.player_pos*35)
                    self.player_sprite_group.clear( self.engine.surface, self.background_surface)
                    self.player_sprite_group.draw(self.engine.surface)

                    self.engine.draw_choice_prompt(query, responses)
                    padlib_rounded_rect(self.engine.surface, selected_color, (138, 533 + menu_pos*45, 564, 39), 6, 5)

                    pygame.display.flip()

                self.engine.clock.tick(60)

    def user_input(self):
        """
        # Function Name: user input
        # Purpose: top level interaction. Checks if there is any input by the user
        #   and allows the user to move around the cursor with the arrow keys and select a unit
        #   if there is one under the mouse
        """

        arrowkeys = False
        directions = {K_LEFT:'left', K_RIGHT:'right', K_UP:'up', K_DOWN:'down'}
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                    # Checks if the player is allowed to move:
                    #   a. A path exists
                    #   b. The path is unlocked
                    if directions[event.key] in self.all_regions[tuple(self.player_pos)].paths.keys() and self.all_regions[tuple(self.player_pos)].paths[directions[event.key]].unlock:
                        self.move_to(self.all_regions[tuple(self.player_pos)].paths[directions[event.key]].vectors[directions[event.key]])
                        self.update_wm_player_data()
                        self.last_move = directions[event.key]

                        # Refreshes world map display

                        self.render_updated_map()

                        return
                if event.key == K_z or event.key == K_RETURN:

                    self.engine.fade_to('black', 0.5)
                    confirm_load = self.all_regions[tuple(self.player_pos)].navigate_loop(incoming_direction=self.last_move)

                    if not confirm_load and not self.engine.check_event_completion(['CH5ST2']):
                        self.render_updated_map(fade_from=True)

                    return confirm_load

                # World Map Menu
                if event.key == K_a:
                    self.engine.fade_to('black')
                    confirm_load = self.wm_menu()
                    self.engine.fade_to('black')
                    if not confirm_load:
                        self.render_updated_map(fade_from=True)
                    return confirm_load

    def navigate_loop(self, load_player=False):

        """
        # Function Name: Navigate Loop
        # Purpose: Player Interaction with the world map
        # Inputs: Load Player = True if player location data is to be loaded,
        #                       False if the map starts fresh
        """
        menu_flag = True


        self.engine.play_music('overworld')
        self.framenum = 0

        # Tracking for player's movement on the map
        self.last_move = None

        # Associates all player units with the world map
        self.unit_associate()

        if load_player:
            if self.engine.player.wm_data['wm_coords'] in self.all_regions.keys():
                self.player_pos = Vector2(self.engine.player.wm_data['wm_coords'])
                reset = False
            else:
                self.player_pos = Vector2(self.default_starting_pos)
                reset = True



            if self.engine.player.wm_data['in_region'] and not reset:


                if self.engine.player.wm_data['region_coords'] in self.all_regions[tuple(self.player_pos)].all_locations.keys():
                    confirm_load = self.all_regions[tuple(self.player_pos)].navigate_loop(self.engine.player.wm_data['region_coords'])
                else:
                    confirm_load = self.all_regions[tuple(self.player_pos)].navigate_loop()

                if confirm_load:
                    return

                # Checks if final mission is complete and goes to credits sequence
                if self.engine.check_event_completion(['CH5ST2']):
                    return


        self.update_wm_player_data()
        self.render_updated_map(fade_from=True)

        while menu_flag:

            if self.framenum == 9:
                self.framenum = 0
            self.framenum += 1

            confirm_load = self.user_input()
            if confirm_load:
                return


            # Checks if final mission is complete and goes to credits sequence
            if self.engine.check_event_completion(['CH5ST2']):
                return

            self.player_sprite_group.clear( self.engine.surface, self.background_surface)
            self.player_sprite_group.update(self.player_pos*35)
            self.player_sprite_group.clear( self.engine.surface, self.background_surface)
            rects = self.player_sprite_group.draw( self.engine.surface)

            pygame.display.update(rects)
            self.engine.clock.tick(60)

    def wm_menu(self):

        """
        # Function Name: World Map Menu
        # Purpose: Manages access to team management, save / load, options
        """

        menu_flag = True
        menu_pos = 0

        fade_flag = False

        options_panel = get_ui_panel((280, 60), border_color, panel_color)
        desc_panel = get_ui_panel((280, 140), border_color, panel_color)

        text_options = []
        icon_names = ['Party', 'Treasures']
        text_options.append(self.engine.section_font.render("Party Stats", True, (0, 0, 0)))
        text_options.append(self.engine.section_font.render("Treasures", True, (0, 0, 0)))

        description_list = [ "Manage the members of the party.",
                             "Displays the treasures that have been collected.",
                             "Create spell actions from elemental items.",
                             "Trade artifacts found for items to Kourindou.",
                             "Return to the world map.",
                             "Check the latest mission news in the Bunbunmaru Newspaper.",
                             "Save or load game data. Remember to save often!",
                             "Change game settings.",
                             "Ends the game.",
                                ]


        if self.engine.unlock_shops or self.engine.check_event_completion(['CH1ST4']):
            text_options.append(self.engine.section_font.render("Synthesis", True, (0, 0, 0)))
            text_options.append(self.engine.section_font.render("Trading", True, (0, 0, 0)))
            icon_names.append('Synthesis')
            icon_names.append('Trading')
        else:
            text_options.append(self.engine.section_font.render("Synthesis", True, (100, 100, 100)))
            text_options.append(self.engine.section_font.render("Trading", True, (100,100, 100)))
            icon_names.append('Disabled Synthesis')
            icon_names.append('Disabled Trading')

        icon_names.append('Cancel')
        icon_names.append('Missions')
        icon_names.append('Data')
        icon_names.append('Options')
        icon_names.append('Exit')

        text_options.append(self.engine.section_font.render("Cancel", True, (0, 0, 0)))

        text_options.append(self.engine.section_font.render("Newspaper", True, (0, 0, 0)))
        text_options.append(self.engine.section_font.render("Save/Load", True, (0, 0, 0)))
        text_options.append(self.engine.section_font.render("Options", True, (0, 0, 0)))
        text_options.append(self.engine.section_font.render("Exit Game", True, (0, 0, 0)))

        text_desc = self.engine.speaker_font.render('Description', True, (0, 0, 0))

        self.engine.play_music('shop_theme')

        update = True

        while menu_flag:

             # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    update = True
                    if (event.key == K_z or event.key == K_RETURN):

                        # COLUMN 1

                        # Selects Party Management Menu
                        if menu_pos == 0:
                            self.party_menu()

                        # Treasure Item menu
                        elif menu_pos == 1:
                            self.engine.treasure_menu()

                        # Spell Synthesis menu
                        elif menu_pos == 2 and (self.engine.unlock_shops or self.engine.check_event_completion(['CH1ST4'])):
                            self.engine.spell_synthesis_system.spell_synthesis_menu()

                        # Item Trading Menu
                        elif menu_pos == 3 and (self.engine.unlock_shops or self.engine.check_event_completion(['CH1ST4'])):
                            self.engine.trading_system.trading_menu()

                        # COLUMN 3

                        # Mission Management Menu
                        elif menu_pos == 5:

                            self.engine.mission_manager.index_menu()

                        # Selects Save / Load Menu
                        elif menu_pos == 6:
                            confirm_load = self.engine.save_menu()
                            if confirm_load == True:
                                return True

                        # Selects Options Menu
                        elif menu_pos == 7:
                            self.engine.options_menu()

                        # Exits program
                        elif menu_pos == 8:
                            exit()

                    if event.key == K_UP:

                        # Top of first column, go to bottom of first column
                        if menu_pos == 0:
                            menu_pos = 4
                        # Top of second column, go to bottom of second column
                        elif menu_pos == 5:
                            menu_pos = 8
                        else:
                            menu_pos -= 1
                    if event.key == K_DOWN:
                        # Bottom of first column, go to top of first  column
                        if menu_pos == 4:
                            menu_pos = 0

                        # Bottom of second column, go to top of second column
                        elif menu_pos == 8:
                            menu_pos = 5
                        else:
                            menu_pos += 1
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        if menu_pos < 5:
                            menu_pos += 5
                        else:
                            menu_pos -= 5

                    if menu_pos > 8:
                        menu_pos = 8


                    if ((event.key == K_z or event.key == K_RETURN) and menu_pos == 4) or event.key == K_x:
                        menu_flag = False
                        self.engine.play_music('overworld')


            if menu_flag:
                if update:
                    update = False
                    # Background image
                    self.engine.surface.blit(self.engine.stats_bg, (0, 0))
                    #self.engine.surface.blit(self.engine.menu_board, (0, 490))
                    # Header
                    # Renders the options
                    for index, option in enumerate(text_options):
                        if index < 5:
                            self.engine.surface.blit(options_panel, (70, 70 + 80*index))
                            self.engine.surface.blit(self.engine.wm_icons[icon_names[index]],
                                                     (90, 70 + options_panel.get_height()/2 - self.engine.wm_icons[icon_names[index]].get_height()/2 + 80*index))
                            self.engine.surface.blit(text_options[index], (90 + options_panel.get_width()/2 - text_options[index].get_width()/2,
                                                                           72 + options_panel.get_height()/2 - text_options[index].get_height()/2 + 80*index))

                        else:
                            self.engine.surface.blit(options_panel, (490, 70 + 80*(index-5)))
                            self.engine.surface.blit(self.engine.wm_icons[icon_names[index]],
                                                     (510, 70 + options_panel.get_height()/2 - self.engine.wm_icons[icon_names[index]].get_height()/2 + 80*(index-5)))
                            self.engine.surface.blit(text_options[index], (510 + options_panel.get_width()/2 - text_options[index].get_width()/2,
                                                                           72 + options_panel.get_height()/2 - text_options[index].get_height()/2 + 80*(index-5)))

                    if menu_pos < 5:
                        padlib_rounded_rect(self.engine.surface, selected_color,
                                            (68, 68 + 80*menu_pos, options_panel.get_width() + 4, options_panel.get_height()+4), 6, 5)
                    else:
                        padlib_rounded_rect(self.engine.surface, selected_color,
                                    (488, 68 + 80*(menu_pos-5), options_panel.get_width() + 4, options_panel.get_height()+4), 6, 5)

                    self.engine.surface.blit(desc_panel, (490,  390))
                    self.engine.surface.blit(text_desc, (490 + desc_panel.get_width()/2 - text_desc.get_width()/2,  400))
                    draw_aligned_text(self.engine.surface, description_list[menu_pos], self.engine.message_font, (0, 0, 0), (500, 430), 260)



                # Fade in once
                if fade_flag == False:
                    self.engine.fade_from('black')
                    fade_flag = True

                pygame.display.flip()
                self.engine.clock.tick(60)

    def party_menu(self):

        """
        # Party Management Menu
        # Purpose: Manages units in the party allowing management of
        #       traits and spells, etc
        """

        units = self.engine.player_units
        menu_flag = True
        menu_pos = [0, 0]
        unit_index = 0

        update = True

        while menu_flag:

             # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        update = True
                        if menu_pos[0] > 0:
                            menu_pos[0] -= 1
                        elif menu_pos[0] == 0:
                            menu_pos[0] = 3

                    if event.key == K_RIGHT:
                        update = True
                        if menu_pos[0] < 3:
                            menu_pos[0] += 1
                        elif menu_pos[0] == 3:
                            menu_pos[0] = 0

                    if event.key == K_UP:
                        update = True
                        if menu_pos[1] > 0:
                            menu_pos[1] -= 1
                        elif menu_pos[1] == 0:
                            menu_pos[1] = 3
                    if event.key == K_DOWN:
                        update = True
                        if menu_pos[1] < 3:
                            menu_pos[1] += 1
                        elif menu_pos[1] == 3:
                            menu_pos[1] = 0

                    # Computes the selected unit
                    unit_index = menu_pos[0] + 4*menu_pos[1]

                    # Calls up the options screen
                    if event.key == K_z or event.key == K_RETURN:
                        if unit_index < len(units):
                            self.unit_options(unit_index)
                        update = True

                    # Jumps straight to stats screen
                    if event.key == K_c:
                        if unit_index < len(units):
                            self.stats_interface(units[unit_index])
                        update = True

                    # Sort Units
                    if event.key == K_a:
                        update = True
                        self.engine.player_units = self.sort_units(units)
                        units = self.engine.player_units

                    if event.key == K_x:
                        return

            if update:
                update = False
                self.draw_units_screen(units)
                self.draw_party_directions()

                # Draw the cursor
                x_spacing = 150
                y_spacing = 100
                padlib_rounded_rect(self.engine.surface, selected_color,
                                    (178 - 35 + menu_pos[0]*x_spacing, 103 + menu_pos[1]*y_spacing, 109, 39), 6, 5)

                # If the selected position is in the range of the length of the units, draw the
                # stats of the unit
                if unit_index < len(units):
                    units[unit_index].plot_stats()

            pygame.display.flip()
            self.engine.clock.tick(60)




    def draw_party_directions(self):
        """
        function name: draw_party_directions

        Desc: Draw basic interaction directions on the world map
        """

        text_enter = self.engine.message_font.render("Z - Select Unit", True, (0, 0, 0))
        text_sort = self.engine.message_font.render("A - Sort Units", True, (0, 0, 0))
        text_stats = self.engine.message_font.render("C - Show Stats", True, (0, 0, 0))

        panel = get_ui_panel((180, 35), border_color, panel_color)
        big_panel = get_ui_panel((280, 35), border_color, panel_color)

        self.engine.surface.blit(panel, (630 - panel.get_width() - 5, 520))
        self.engine.surface.blit(text_enter, (630 - panel.get_width()/2 - text_enter.get_width()/2 - 5 ,
                                              520 + panel.get_height()/2 - text_enter.get_height()/2))

        self.engine.surface.blit(panel, (635, 520))
        self.engine.surface.blit(text_sort, (635 + panel.get_width()/2 - text_sort.get_width()/2 ,
                                              520 + panel.get_height()/2 - text_sort.get_height()/2))

        self.engine.surface.blit(big_panel, (630 - big_panel.get_width()/2, 565))
        self.engine.surface.blit(text_stats, (630 - text_stats.get_width()/2 ,
                                              565 + panel.get_height()/2 - text_stats.get_height()/2))


    def draw_units_screen(self, units):

        """
        Draw units screen

        Draws the interface background for the units screen

        Units - A list consisting of player character units

        """

        # Compiles a list of names
        name_panel = get_ui_panel((105, 35), border_color, panel_color)

        names = []
        for unit in units:
            text_name = self.engine.message_font.render(unit.name, True, (0, 0, 0))
            names.append(text_name)

        self.engine.surface.blit(self.engine.party_bg, (0, 0))
        self.engine.surface.blit(self.engine.menu_board, (0, 490))


        x_spacing = 150
        y_spacing = 100

        # Draw the panels
        for row in xrange(0, 4):
            for column in xrange(0, 4):
                self.engine.surface.blit(self.engine.unit_tile, (180+x_spacing*column, 62+y_spacing*row))
                self.engine.surface.blit(name_panel, (180-35+x_spacing*column, 105+y_spacing*row))

        # Draw the units
        for index, unit in enumerate(units):

            y_position = index/4
            x_position = index%4

            self.engine.surface.blit(unit.image, (180+x_spacing*x_position, 58+y_spacing*y_position), (0, 0, 35, 35))
            name = names[x_position+4*y_position]
            self.engine.surface.blit(name, (180 - 35 + name_panel.get_width()/2 + x_spacing*x_position - name.get_width()/2,
                                            105 + name_panel.get_height()/2 - name.get_height()/2 + y_spacing*y_position))


    def stats_interface(self, unit):


        # Records the unit's position in the team list
        index = self.engine.player_units.index(unit)

        menu_flag = True
        # page 0 (traits), page 1 (stats, default), page 2 (spells)
        page = 1
        while menu_flag:

            # Calls a unit's stats data loop in the requested page
            if page == 0:
                event = unit.traits_stats_loop()
            elif page == 1:
                event = unit.stats_loop()
            else:
                event = unit.spell_stats_loop()

            if event.key == K_x:
                menu_flag = False

            # Up and down keys traverse the list of units in a team
            elif event.key == K_DOWN:
                index += 1
                if index > len(self.engine.player_units)-1:
                    index = 0
                self.engine.fade_to('black', 0.25)
                unit = self.engine.player_units[index]
            elif event.key == K_UP:
                index -= 1
                if index < 0:
                    index = len(self.engine.player_units)- 1
                unit = self.engine.player_units[index]
                self.engine.fade_to('black', 0.25)
            elif event.key == K_LEFT:
                page -= 1
                if page < 0:
                    page = 2
                self.engine.fade_to('black', 0.25)
            elif event.key == K_RIGHT:
                page += 1
                if page > 2:
                    page = 0
                self.engine.fade_to('black', 0.25)

    def sort_units(self, units):
        """"
        # function name: sort_units
        # purpose: Allows player to sort units.
        """

        # Sorts units by a certain critieria
        def sort_units_by(criteria):
            sort_list = []
            # Compiles the criteria to be sorted for each unit (Name will be tiebreaker)
            for unit in self.engine.player_units:
                sort_criteria = {'Name':(unit.name, unit.name, unit),
                                 'Level':(unit.level, unit.name, unit),
                                 'HP':(unit.HP, unit.name, unit),
                                 'STR':(unit.STR, unit.name, unit),
                                 'MAG':(unit.MAG, unit.name, unit),
                                 'DEF':(unit.DEF, unit.name, unit),
                                 'MDEF':(unit.MDEF, unit.name, unit),
                                 'ACC':(unit.ACC, unit.name, unit),
                                 'AGL':(unit.AGL, unit.name, unit)}

                sort_list.append(sort_criteria[criteria])

            # Sorts units
            sort_list.sort()
            # Sorts Highest to Lowest for numerical criteria
            if criteria in ('Level', 'HP', 'STR', 'MAG', 'DEF', 'MDEF', 'ACC', 'AGL'):
                sort_list.reverse()

            units_list = [unit[2] for unit in sort_list]
            return units_list


        menu_flag = True
        menu_pos = [0, 0]
        criteria_list = ['Name', 'Level', 'HP', 'STR', 'DEF', 'MDEF', 'ACC', 'AGL']
        text_criteria_list = [self.engine.section_font.render(criteria, True, (0, 0, 0)) for criteria in criteria_list]
        update = True

        options_panel = get_ui_panel((80, 40), border_color, panel_color)

        while menu_flag:
             # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    # Handles left/right
                    if event.key == K_UP or event.key == K_DOWN:
                        if menu_pos[1] == 1:
                            menu_pos[1] = 0
                        else:
                            menu_pos[1] = 1

                        update = True

                    if event.key == K_LEFT:
                        if menu_pos[0] > 0:
                            menu_pos[0] -= 1
                        elif menu_pos[0] == 0:
                            menu_pos[0] = 3
                        update = True

                    if event.key == K_RIGHT:
                        if menu_pos[0] < 3:
                            menu_pos[0] += 1
                        elif menu_pos[0] == 3:
                            menu_pos[0] = 0
                        update = True

                    # Calls up the options screen
                    if event.key == K_z or event.key == K_RETURN:
                        units = sort_units_by(criteria_list[menu_pos[0]+4*menu_pos[1]])
                        update = True
                    if event.key == K_x:
                        return units

            if update:
                update = False
                self.draw_units_screen(units)

                # Draw the OPTIONS

                for index, text_criteria in enumerate(text_criteria_list):
                    if index < 4:
                        x_position = 455 + index*(options_panel.get_width()+10)
                        y_position = 510
                    else:
                        x_position = 455 + (index-4)*(options_panel.get_width()+10)
                        y_position = 570

                    self.engine.surface.blit(options_panel, (x_position, y_position))
                    self.engine.surface.blit(text_criteria, (x_position+options_panel.get_width()/2 - text_criteria.get_width()/2,
                                                             y_position+2+options_panel.get_height()/2 - text_criteria.get_height()/2))


                # Draw the cursor
                cursor_x = 453 + (options_panel.get_width()+10)*menu_pos[0]
                cursor_y = 508 + 60*menu_pos[1]
                padlib_rounded_rect(self.engine.surface, selected_color, (cursor_x, cursor_y, options_panel.get_width()+4, options_panel.get_height()+4), 6, 5)

                pygame.display.flip()
            self.engine.clock.tick(60)


    def unit_options(self, selected):
        """
        # Name: Unit_options
        # Purpose: Allows selection of various managment options for an individual unit
        # Inputs: None
        """

        menu_pos = 0
        menu_flag = True

        text_spells = self.engine.section_font.render("Spell Actions", True, (0, 0, 0))
        text_traits = self.engine.section_font.render("Set Traits", True, (0, 0, 0))
        text_stats = self.engine.section_font.render("Stats", True, (0, 0, 0))
        text_cancel = self.engine.section_font.render("Cancel", True, (0, 0, 0))

        options_panel = get_ui_panel((180, 40), border_color, panel_color)

        units = self.engine.player_units
        selected_unit = self.engine.player_units[selected]

        update = True

        while menu_flag:

             # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP or event.key == K_DOWN:
                        # Sets the new position (up and down swap the current row)
                        menu_pos = [2, 3, 0, 1][menu_pos]
                        update = True
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        # sets the new position (left and right swap the current column)
                        menu_pos = [1, 0, 3, 2][menu_pos]
                        update = True

                    if event.key == K_z or event.key == K_RETURN:
                        update = True
                        # Spells
                        if menu_pos == 0:
                            selected_unit.spell_swap_menu()

                        # Swap Traits
                        elif menu_pos == 1:
                            selected_unit.trait_swap_menu()

                        # Stats
                        elif menu_pos == 2:
                            self.stats_interface(selected_unit)

                        # Cancel
                        elif menu_pos == 3:
                            return

                    if event.key == K_x:
                        return

            if menu_flag:

                if update:
                    update = False
                    self.draw_units_screen(units)

                    # Draw the cursor
                    x_spacing = 150
                    y_spacing = 100
                    unit_cursor_x = selected % 4
                    unit_cursor_y = selected / 4
                    padlib_rounded_rect(self.engine.surface, selected_color,
                                        (178 - 35 + unit_cursor_x*x_spacing, 103 + unit_cursor_y*y_spacing, 109, 39), 6, 5)

                    # draws the available options
                    option_positions = ((440, 510), (640, 510), (440, 570), (640, 570))
                    for position in option_positions:
                        self.engine.surface.blit(options_panel, position)

                    self.engine.surface.blit(text_spells, (440 + options_panel.get_width()/2 - text_spells.get_width()/2,
                                                           512 + options_panel.get_height()/2 - text_spells.get_height()/2))
                    self.engine.surface.blit(text_traits, (640 + options_panel.get_width()/2 - text_traits.get_width()/2,
                                                           512 + options_panel.get_height()/2 - text_traits.get_height()/2))
                    self.engine.surface.blit(text_stats, (440 + options_panel.get_width()/2 - text_stats.get_width()/2,
                                                           572 + options_panel.get_height()/2 - text_stats.get_height()/2))
                    self.engine.surface.blit(text_cancel, (640 + options_panel.get_width()/2 - text_cancel.get_width()/2,
                                                           572 + options_panel.get_height()/2 - text_cancel.get_height()/2))

                    # draws a box around current selection
                    menu_cursor_x, menu_cursor_y = option_positions[menu_pos]
                    padlib_rounded_rect(self.engine.surface, selected_color,
                                        (menu_cursor_x-2, menu_cursor_y-2, options_panel.get_width()+4, options_panel.get_height()+4), 6, 5)

                    # Draw the cursor
                    # If the selected position is in the range of the length of the units, draw the
                    # stats of the unit
                    selected_unit.plot_stats()




                    pygame.display.flip()
                self.engine.clock.tick(60)


class Region(object):

    def __init__(self, engine, name, wm_coords, prereq, image_pos, advanced_background):
        """
        # Function Name: __init__
        # Purpose: Intializes a region
        # Inputs:
        #         engine - main system engine
        #         name - Region Name
        #         wm_coords - World map coordinates
        #         prereq - when to unlock this location
        #         image_pos - location to draw this region on the worldmap
        #         advanced_background - flag to enable drawing of new map image system
                                        to be removed when all regions have new map system implemented.
        """

        self.engine = engine
        self.name = name
        self.wm_coords = wm_coords
        self.pix_coords = 35*wm_coords
        self.prereq = prereq
        self.image_pos = image_pos

        # World Map Display Name
        self.name_small = self.engine.sfont.render(self.name, True, (0, 0, 0))
        self.name_big = self.engine.section_font.render(self.name, True, (0, 0, 0))
        # Gets the size of the name to center it
        name_small_halfwidth = self.name_small.get_width()/2
        self.name_coords = 35*(wm_coords+Vector2(0, 1))+Vector2(17-name_small_halfwidth, 0)

        # Subregions and locations
        self.subregions = []
        self.all_locations = {}
        self.all_locations_by_name = {}

        # Connection dot points
        self.dot_positions = set()
        self.paths = {}
        # self.connection_paths = paths
        # self.vector_paths = {'up':Vector2(0, 0), 'down':Vector2(0, 0), 'left':Vector2(0, 0), 'right':Vector2(0, 0)}

        self.unlock = False

        default_position = Vector2(0, 0)
        self.player_pos = default_position
        self.player_sprite_group = pygame.sprite.RenderUpdates()
        self.player_sprite = WorldmapSprite( 35*self.player_pos, self.engine.player_img)
        self.player_sprite_group.add(self.player_sprite)
        self.background_surface = pygame.surface.Surface((840, 630))
        self.advanced_background = advanced_background

    def add_locations(self, locations):
        """
        # Function Name: add_locations
        # Purpose: Adds a set of locations
        # Inputs: locations - a list of location objects to be added to the
        """

        for location in locations:
            # Adds the location to the dictionary
            self.all_locations[tuple(location.wm_coords)] = location
            self.all_locations_by_name[location.name] = location

            # Associates a location with the region
            location.region = self
            location.get_graphical()

            # if the location is flagged as an entrance location, set it to the
            # # default entry way to the world map
            # if location.name == self.entrance:
                # location.entrance = True
                # self.entrance_coords = location.wm_coords
            if location.name in self.entrances.values():
                location.exit = True


    def initialize_paths(self, location_path_list):

        """
        # Function Name: initialize_paths
        # Purpose: Initializes the paths of each location
        # Input: Location path list - a list of the paths to be initialized
        """

        self.location_path_list = location_path_list

        # List of all dots to not include a range around the location
        remove_pts = []
        for location in self.all_locations.values():
            remove_pts.extend((tuple(location.wm_coords), tuple(location.wm_coords+Vector2(-1, 1))))

        for path in location_path_list:

            # Each path has two connecting points along with the direction key to press to get to each location
            direction_to_1 = path.locations.keys()[0]
            region_1 = path.locations[direction_to_1]
            direction_to_2 = path.locations.keys()[1]
            region_2 = path.locations[direction_to_2]

            # We assign the starting point's path directions to this path so it can be called when the character needs to move
            self.all_locations_by_name[region_2].paths[direction_to_1] = path
            self.all_locations_by_name[region_1].paths[direction_to_2] = path

            # Constructs destination vectors
            delta_pos = self.all_locations_by_name[region_1].wm_coords - self.all_locations_by_name[region_2].wm_coords
            path.vectors[direction_to_1] = delta_pos
            path.vectors[direction_to_2] = -1*(delta_pos.copy())

    def update_region_player_data(self):
        """
        # Function Name: update wm player data
        # Purpose: Updates the location of the player
        """

        self.engine.player.wm_data['in_region'] = True
        self.engine.player.wm_data['region_coords'] = tuple(self.player_pos)

    ############################################
    # Graphical Methods
    ############################################

    def render_background(self, draw_directions = True):

        """
        # Function Name: Render background to the background surface
        # Purpose: Draws the background map and the locations
        """

        if self.advanced_background:
            self.background_surface.blit(self.engine.region_backgrounds[self.name], (0, 0))
        else:
            self.background_surface.blit(self.engine.region_bg, (0, 0))

        self.background_surface.blit(self.engine.menu_board, (0, 490))

        # [self.background_surface.blit(self.engine.path_dot, dot_pos)  for path in self.location_path_list if path.unlock for dot_pos in path.dot_positions]

        # Location dots and path points
        for location in self.all_locations.values():
            if self.advanced_background:

                if not location.unlock:
                    self.background_surface.blit(self.engine.hidden_location_images[location.name], location.image_pos)

                elif location == self.all_locations[tuple(self.player_pos)]:
                    self.background_surface.blit(self.engine.active_location_images[location.name], location.image_pos)
                else:
                    self.background_surface.blit(self.engine.inactive_location_images[location.name], location.image_pos)

            else:
                if location.unlock:
                    self.background_surface.blit(location.name_small, location.name_coords)

            if location.unlock:
                self.background_surface.blit(self.engine.location_circle, location.pix_coords, (location.type*35, 0, 35, 35))


            if location.has_event() and location.unlock:
                if self.player_pos == location.wm_coords:
                    self.background_surface.blit(self.engine.event_icon, (location.pix_coords+Vector2(30, -25)))
                else:
                    self.background_surface.blit(self.engine.event_icon, (location.pix_coords+Vector2(10, -15)))

        # Location Description

        name_panel = get_ui_panel((280, 45), border_color, panel_color)
        desc_panel = get_ui_panel((320, 60), border_color, panel_color)

        text_location_name = self.all_locations[tuple(self.player_pos)].name_big

        self.background_surface.blit(name_panel, (40, 505))
        self.background_surface.blit(text_location_name, (40 + name_panel.get_width()/2 - text_location_name.get_width()/2,
                                                          507 + name_panel.get_height()/2 - text_location_name.get_height()/2))

        self.background_surface.blit(desc_panel, (20, 555))
        draw_aligned_text(self.background_surface, self.all_locations[tuple(self.player_pos)].desc, self.engine.sfont,
                          (0, 0, 0), (30, 565), desc_panel.get_width()-20)

        if draw_directions:
            self.draw_directions()


    def render_arrows(self):

        """
        draw_arrows

        Draws the direction arrows for the unit on the main map screen.

        """

        # Draws arrows indicating where to move
        arrow_offset = {'up':Vector2(0, -40),
                     'down':Vector2(0, 40),
                     'left':Vector2(-35, 15),
                     'right':Vector2(35, 15)
                     }

        for direction in self.all_locations[tuple(self.player_pos)].paths.keys():
            if self.all_locations[tuple(self.player_pos)].paths[direction].unlock:

                arrow_coord = 35*self.player_pos + arrow_offset[direction]

                self.background_surface.blit(self.engine.direction_arrows[direction], arrow_coord)

    def render_updated_map(self, draw_arrows = True, fade_from = False):

        """
        Purpose: Updates the background surface and draws everything

        input - draw_arrows - enable drawing of direction arrows
        """
        self.render_background()
        if draw_arrows:
            self.render_arrows()
        self.engine.surface.blit(self.background_surface, (0, 0))
        self.player_sprite_group.update(self.player_pos*35)
        self.player_sprite_group.clear( self.engine.surface, self.background_surface)
        self.player_sprite_group.draw(self.engine.surface)

        if fade_from:
            self.engine.fade_from('black', 0.5)

        pygame.display.flip()
        self.engine.clock.tick(60)



    def draw_directions(self):
        """
        function name: draw_directions

        Desc: Draw basic interaction directions on the world map
        """

        text_enter = self.engine.message_font.render("Z - Select Event", True, (0, 0, 0))
        text_menu = self.engine.message_font.render("A - Main Menu", True, (0, 0, 0))
        text_return = self.engine.message_font.render("X - Leave Region", True, (0, 0, 0))

        panel = get_ui_panel((180, 35), border_color, panel_color)
        big_panel = get_ui_panel((280, 35), border_color, panel_color)

        self.background_surface.blit(panel, (630 - panel.get_width() - 5, 520))
        self.background_surface.blit(text_enter, (630 - panel.get_width()/2 - text_enter.get_width()/2 - 5 ,
                                              520 + panel.get_height()/2 - text_enter.get_height()/2))

        self.background_surface.blit(panel, (635, 520))
        self.background_surface.blit(text_menu, (635 + panel.get_width()/2 - text_menu.get_width()/2 ,
                                              520 + panel.get_height()/2 - text_menu.get_height()/2))

        self.background_surface.blit(big_panel, (630 - big_panel.get_width()/2, 565))
        self.background_surface.blit(text_return, (630 - text_return.get_width()/2 ,
                                              565 + panel.get_height()/2 - text_return.get_height()/2))


    def move_to(self, direction_vector):
        """
        # Function Name: move_to
        # Purpose: Moves the player to a new direction
        # DIrection vector - Relative direction to move from curren tposition
        """

        # Smoothstep function
        # See: http://sol.gfxile.net/interpolation/
        smoothstep = lambda v: (v*v*(3-2*v))


        start_pos = 35*self.player_pos
        current_pos = 35*self.player_pos

        # Sets frame count proportional to the square root of the magnitude of the step vector
        frame_count = int(10*direction_vector.get_magnitude()**(1.0/2))


        self.render_updated_map(draw_arrows = False)

        for t in xrange(0, int(frame_count)+1):
            v = float(t)/float(frame_count)
            v = smoothstep(v)
            scale_term = int(35*v)
            intermediate_step = scale_term*direction_vector

            current_pos = start_pos + intermediate_step

            self.player_sprite_group.update(current_pos)
            self.player_sprite_group.clear( self.engine.surface, self.background_surface)
            rects = self.player_sprite_group.draw( self.engine.surface)

            pygame.display.update(rects)
            self.engine.clock.tick(60)

        start_pos = current_pos.copy()

        self.player_pos += direction_vector
        self.render_updated_map()


    ############################################
    # Interactive methods
    ############################################

    def user_input(self):
        """
        # Function Name: user input
        # Purpose: top level interaction. Checks if there is any input by the user
        #   and allows the user to move around the cursor with the arrow keys and select a unit
        #   if there is one under the mouse
        """

        directions = {K_LEFT:'left', K_RIGHT:'right', K_UP:'up', K_DOWN:'down'}

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                    # Checks if the player is allowed to move:
                    #   a. A path exists
                    #   b. The path is unlocked
                    if directions[event.key] in self.all_locations[tuple(self.player_pos)].paths.keys() and self.all_locations[tuple(self.player_pos)].paths[directions[event.key]].unlock:
                        self.move_to(self.all_locations[tuple(self.player_pos)].paths[directions[event.key]].vectors[directions[event.key]])
                        self.update_region_player_data()
                        return



                # Location menu only accessible if events are present
                if (event.key == K_z or event.key == K_RETURN) and self.all_locations[tuple(self.player_pos)].all_events:
                    exit_flag = self.all_locations[tuple(self.player_pos)].menu_loop()

                    # Checks if final mission is complete and returns to WM if so
                    if self.engine.check_event_completion(['CH5ST2']):
                        return 'jump2wm'
                    else:

                        return exit_flag

               # World Map Menu
                if event.key == K_a:
                    self.engine.fade_to('black')
                    confirm_load = self.wm_parent.wm_menu()
                    if confirm_load:
                        return 'load_player'
                    else:
                        self.engine.fade_to('black')
                        self.render_updated_map(fade_from=True)

                if event.key == K_x:
                    return 'jump2wm'

        self.render_updated_map()
        return False

    def navigate_loop(self, start_coords=None, incoming_direction=None):

        """
        # Function Name: Navigate Loop
        # Purpose: Player Interaction with the world map
        # Inputs: start_coords - Player starting coordinates
        #         incoming direction - Player's incoming direction if a location has two+ gates
        """

        menu_flag = True

        if start_coords:
            self.player_pos = Vector2(start_coords)
        else:
            # If a location only has one entrance or player is not coming from another location since they just started the game, jump them directly to that default/only entrance
            if len(self.entrances.values()) == 1 or not incoming_direction:
                self.player_pos = Vector2(tuple(self.all_locations_by_name[self.entrances['default']].wm_coords))
            else:
                self.player_pos = Vector2(tuple(self.all_locations_by_name[self.entrances[incoming_direction]].wm_coords))

        self.update_region_player_data()
        self.render_updated_map(fade_from=True)
        while menu_flag:

            input_flag = self.user_input()


            # If the location flag received, return to the world map
            if input_flag == 'jump2wm':
                menu_flag = False
                self.wm_parent.player_pos = Vector2(tuple(self.wm_coords))
                self.wm_parent.update_wm_player_data()
            # If load player flag received, load new map
            elif input_flag == 'load_player':
                return True

            if menu_flag:

                self.player_sprite_group.update(self.player_pos*35)
                self.player_sprite_group.clear( self.engine.surface, self.background_surface)
                self.player_sprite_group.draw(self.engine.surface)


                pygame.display.flip()

                self.engine.clock.tick(60)


# Connecting path object
class Path(object):

    def __init__(self, locations, prereq):

        """
        # Function Name; __init__
        # Purpose: Initializes a path object
        # Inputs:
        #           locations - where does this path connect to
        #           prereqs - events that must be completed for this path to open
        """

        self.locations = locations
        if prereq:
            self.prereq = prereq
            self.unlocked = False
        else:
            self.prereq = None
            self.unlocked = True
        self.vectors = {}
        self.dot_positions = []


    def __str__(self):
        """
        # function Name: __str__
        # Purpose: String representation of a path
        # Output: returns the two connections of the path, the prerequisites, and whether it is locked or not
        """

        return str([self.locations, self.prereqs, self.unlocked])


class Location(object):

    def __init__(self, name, desc, wm_coords, type, portrait, image_position, prereq):
        """
        # Function Name: __init__
        # Purpose: Intializes a location
        # Inputs:
        #         Region - Parent region
        #         Name - Location's name
        #         Wm_coords - World map coordinates
        #         type - An integer that corresponds to the following types of location
        #                   0 - Neutral
        #                   1 - Danger Zone (Likely location for monster attacks and missions)
        #                   2 - Safe Zone (Towns and villages)
        #                   3 - Region exit / entrance point
        #         portrait - portrait image ID
        """

        self.name = name
        self.desc = desc
        self.wm_coords = wm_coords
        self.pix_coords = 35*wm_coords + Vector2(0, 5)

        self.image_pos = image_position
        self.type = type
        self.portrait = portrait
        self.all_events = []
        self.entrance = False
        self.exit = False
        self.paths = {}
        self.prereq = prereq
        self.unlock = False
        self.region = None

    def add_event(self, event):
        """
        # Function Name: add_event
        # Purpose: Adds an event to the region's list
        """
        self.all_events.append(event)
        event.location = self

    def has_event(self):
        """
        # Function Name: has_event
        # Purpose: Checks if this location has an any events
        # Output: Return True if location has events
        """
        for event in self.all_events:
            if event:
                return True
        # no event, return False
        return False

    def get_graphical(self):

        """
        # Function Name: get_graphical
        # Purpose: Generates the graphical objects for a location (note: requires association with a region)
        """

        # World Map Display objects

        self.name_small = self.region.engine.sfont.render(self.name, True, (0, 0, 0))
        self.name_big = self.region.engine.section_font.render(self.name, True, (0, 0, 0))

        # Gets the size of the name to center it
        name_small_halfwidth = self.name_small.get_width()/2
        self.name_coords = 35*(self.wm_coords+Vector2(0, 1))+Vector2(17-name_small_halfwidth, 5)

    def get_text_all_events(self):
        """
        # Function Name: get_text_all_events
        # Purpose: Generates the text objects from a location's events
        """

        text_event = []
        for event in self.all_events:
            text_event.append(self.region.engine.section_font.render(event.name, True, (0, 0, 0)))
        return text_event

    def render_menu_options(self):
        """
        Purpose: Draws the locations event options to background surface
        """

        options_panel = get_ui_panel((360, 40), border_color, panel_color)

        # Generate text objects
        text_cancel = self.region.engine.section_font.render("Cancel", True, (0, 0, 0))

        text_event = self.get_text_all_events()
        menu_y = 515
        for index, event in enumerate(self.all_events):
            self.region.background_surface.blit(options_panel, (450, menu_y + 50*index))
            self.region.background_surface.blit(self.region.engine.wm_icons[event.type], (460, menu_y + 2 + 50*index))
            self.region.background_surface.blit(text_event[index], (450 + options_panel.get_width()/2 - text_event[index].get_width()/2,
                                                                    menu_y + 2 + options_panel.get_height()/2 - text_event[index].get_height()/2  - +50*index))

        self.region.background_surface.blit(options_panel, (450, menu_y + 50*(index+1)))
        self.region.background_surface.blit(text_cancel, (450 + options_panel.get_width()/2 - text_cancel.get_width()/2,
                                                          menu_y + 2 + options_panel.get_height()/2 - text_cancel.get_height()/2 + 50*(index+1)))


    def render_updated_map(self):
        """
        Renders a full frame of the map and options menu
        """

        self.region.render_background(draw_directions = False)
        self.render_menu_options()
        self.region.engine.surface.blit(self.region.background_surface, (0, 0))
        self.region.player_sprite_group.draw(self.region.engine.surface)

    def menu_loop(self):
        """
        # Function Name: menu_loop
        # Purpose: Location level menu loop that allows for the selection of an event in a location.
        # Inputs: None
        # Outputs: exit_flag
        """



        menu_flag = True
        menu_pos = 0

        menu_max = len(self.all_events)
        update = True
        while menu_flag:

            # User Input
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT or event.key == K_UP:
                        if menu_pos > 0:
                            menu_pos -= 1
                        else:
                            menu_pos = menu_max
                        update = True
                    elif event.key == K_RIGHT or event.key == K_DOWN:
                        if menu_pos < menu_max:
                            menu_pos += 1
                        else:
                            menu_pos = 0
                        update = True
                    if event.key == K_z or event.key == K_RETURN:

                        # Selects event if it is available
                        if menu_pos < menu_max:

                            # Auto-save after mission if enabled
                            if self.region.engine.options.auto_save:
                                self.region.engine.player.save('autosave')

                            self.all_events[menu_pos].execute()

                            # Checks if final mission is complete and returns to WM if so
                            if self.region.engine.check_event_completion(['CH5ST2']):
                                return

                            # Auto-save after mission if enabled
                            if self.region.engine.options.auto_save:
                                self.region.engine.player.save('autosave')

                            return
                        # Cancel
                        elif menu_pos == menu_max:
                            return

                    if event.key == K_x:
                        return

            if menu_flag:
                if update:
                    update = False
                    # Location menu

                    self.render_updated_map()
                    padlib_rounded_rect(self.region.engine.surface, selected_color,
                                        (448, 513 + 50*menu_pos, 364, 44), 6, 5)
                    pygame.display.flip()

                self.region.engine.clock.tick(60)


class WorldmapSprite(pygame.sprite.Sprite):

    def __init__(self, start_pos, image):
        """
        # Function: __init__
        # Purpose: Creates a sprite for the worldmap
        # Inputs:   map - worldmap object to associate with
        #           image - image to use in the worldmap sprite
        #
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = image.subsurface((0, 0, 35, 35))
        self.rect = self.image.get_rect()
        self.rect.topleft = tuple(start_pos)

    def update(self, new_position):
        """
        # Function: update
        # Purpose: Updates sprite to current location of the unit (pixel)
        """
        self.rect.topleft = tuple(new_position)
