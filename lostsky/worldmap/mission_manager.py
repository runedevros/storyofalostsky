#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from lostsky.core.utils import split_lines, draw_aligned_text, padlib_rounded_rect
from pygame.locals import *
from sys import exit
import os

class MissionManager(object):

    def __init__(self, engine):

        """
        # Function Name: __init__
        # Purpose: Initiates the mission manager object
        # Inputs: Engine - engine that the mission manager is associated with
        """
        self.engine = engine

    ####################################
    # Interaction Methods
    ####################################

    def index_menu(self):

        """
        # Function Name: index_menu
        # Purpose: Index Menu - Select from missions, rumors, archives, return to map
        # Inputs: None
        """

        current_story = self.engine.news_reports_list[0]
        for report in self.engine.news_reports_list[1:]:
            if self.engine.all_events_master[report['mission']].done == True:
                current_story = report

        menu_flag = True
        menu_pos = 0
        update = True

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
                            menu_pos = 4
                        update = True
                    if ( event.key == K_DOWN or event.key == K_RIGHT ):
                        if menu_pos < 4:
                            menu_pos += 1
                        elif menu_pos == 4:
                            menu_pos = 0
                        update = True
                    if event.key == K_z or event.key == K_RETURN:
                        # Current Missions Menu
                        if menu_pos == 0:
                            self.mission_display_menu(self.engine.all_events_sign_up, "Current Missions", current_story)
                        # Rumors Menu
                        elif menu_pos == 1:
                            self.hint_menu(current_story)
                        # Archives Menu
                        elif menu_pos == 2:
                            self.mission_display_menu(self.engine.all_events_completed, "Completed Missions", current_story)
                        elif menu_pos == 3:
                            self.profiles_menu(current_story)

                        else:
                            return
                        update = True

                    if event.key == K_x or ((event.key == K_z or event.key == K_RETURN) and menu_pos == 4):
                        menu_flag = False

            if update:
                update = False
                self.engine.surface.blit(self.engine.mission_bg, (0, 0))
                self.draw_newspaper_title("Bunbunmaru Newspaper")
                self.draw_front_lines()
                self.draw_author_and_date(current_story)
                self.draw_report(current_story)
                self.draw_front_options()

                pygame.draw.rect(self.engine.surface, (0, 0, 0), (10, 150 + menu_pos*80, 130, 60), 3)

                pygame.display.flip()
            self.engine.clock.tick(30)

    def mission_display_menu(self, mission_list, heading, report):
        """
        # Function Name: current missions menu
        # Purpose: Allows the player to view the a list of completed missions
        # Inputs: report - currently viewed front page article (used to set dates and author name)
        """

        menu_flag = True
        menu_pos = 0
        offset = 0
        max_slots = 8
        update = True

        # Sorts missions by event ID and omits the prologue sequence from the mission list
        unsorted_missions = [(event.event_id, event) for event in mission_list if event.event_id != "Prologue"]
        unsorted_missions.sort()
        if unsorted_missions:
            _, sorted_missions = zip(*unsorted_missions)
        else:
            sorted_missions = []

        while menu_flag:

             # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if ( event.key == K_UP or event.key == K_LEFT ) and sorted_missions:


                        update = True

                        # Top of the list, jump to the bottom
                        if menu_pos == 0:
                            menu_pos = len(sorted_missions)-1
                            offset = max(0, len(sorted_missions) - max_slots)

                        # Top of the itnerval, shift offset up
                        elif menu_pos == offset:
                            menu_pos -= 1
                            offset -= 1

                        # within interval, move cursor without changing shift
                        elif menu_pos > 0:
                            menu_pos -= 1


                    if ( event.key == K_DOWN or event.key == K_RIGHT ) and sorted_missions:

                        update = True

                        # Bottom of the list of slots: Jumps to the top
                        if menu_pos == len(sorted_missions) - 1:
                            menu_pos = 0
                            offset = 0

                        # Bottom of the interval, advance the offset by 1
                        elif menu_pos == offset + max_slots - 1:
                            offset += 1
                            menu_pos += 1

                        # intermediate interval: move the cursor only down by 1
                        elif menu_pos < len(sorted_missions) - 1:
                            menu_pos += 1

                    if event.key == K_x:
                        return

            if update:
                update = False

                # Draws background
                self.engine.surface.blit(self.engine.mission_bg, (0, 0))
                self.draw_newspaper_title(heading)
                self.draw_article_lines()
                self.draw_author_and_date(report)

                # Draws mission list
                self.draw_article_list(sorted_missions, offset)

                # If there are any missions, draw a list of them, the scroll bar and the currently selected mission
                if sorted_missions:
                    self.draw_scroll_bar(sorted_missions, offset)
                    self.draw_mission_data(sorted_missions[menu_pos])
                    pygame.draw.rect(self.engine.surface, (50, 50, 50), (10, 155 + 60*(menu_pos-offset), 250, 40), 3)

                pygame.display.flip()
            self.engine.clock.tick(30)

    def hint_menu(self, report):
        """
        # Function Name: hint_menu
        # Purpose: Allows the player to view helpful hints and rumors
        # Inputs: report - currently viewed front page article (used to set dates and author name)
        """

        # Filters out hints that have not been unlocked
        hint_list = [hint for hint in self.engine.hint_list if self.engine.check_event_completion(hint.prereqs)]

        menu_flag = True
        menu_pos = 0
        offset = 0
        max_slots = 8
        update = True

        while menu_flag:

             # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if ( event.key == K_UP or event.key == K_LEFT ) and hint_list:


                        update = True

                        # Top of the list, jump to the bottom
                        if menu_pos == 0:
                            menu_pos = len(hint_list)-1
                            offset = max(0, len(hint_list) - max_slots)

                        # Top of the itnerval, shift offset up
                        elif menu_pos == offset:
                            menu_pos -= 1
                            offset -= 1

                        # within interval, move cursor without changing shift
                        elif menu_pos > 0:
                            menu_pos -= 1


                    if ( event.key == K_DOWN or event.key == K_RIGHT ) and hint_list:

                        update = True

                        # Bottom of the list of slots: Jumps to the top
                        if menu_pos == len(hint_list) - 1:
                            menu_pos = 0
                            offset = 0

                        # Bottom of the interval, advance the offset by 1
                        elif menu_pos == offset + max_slots - 1:
                            offset += 1
                            menu_pos += 1

                        # intermediate interval: move the cursor only down by 1
                        elif menu_pos < len(hint_list) - 1:
                            menu_pos += 1

                    if event.key == K_x:
                        return

            if update:
                update = False

                # Draws the background
                self.engine.surface.blit(self.engine.mission_bg, (0, 0))
                self.draw_newspaper_title("Rumors and Hints")
                self.draw_article_lines()
                self.draw_author_and_date(report)

                # Draw list of hints
                self.draw_article_list(hint_list, offset)

                # Draws scroll bar and a selected hint
                if hint_list:
                    self.draw_scroll_bar(hint_list, offset)
                    self.draw_hint_data(hint_list[menu_pos])
                    pygame.draw.rect(self.engine.surface, (50, 50, 50), (10, 155 + 60*(menu_pos-offset), 250, 40), 3)

                pygame.display.flip()
            self.engine.clock.tick(30)


    def profiles_menu(self, report):
        """
        # Function Name: profiles_menu
        # Purpose: Allows the player to view bios of different characters we've encountered
        # Inputs: report - currently viewed front page article (used to set dates and author name)
        """

        # Filters out hints that have not been unlocked
        profile_list = [profile for profile in self.engine.profile_list if self.engine.check_event_completion([profile.prereqs])]
        character_portraits = [pygame.image.load(os.path.join('images', 'portrait', profile.image)).convert_alpha() for profile in profile_list]

        menu_flag = True
        menu_pos = 0
        offset = 0
        max_slots = 8
        update = True

        while menu_flag:

            # looks for event type data to select interaction
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    exit()
                if event.type == KEYDOWN:
                    if (event.key == K_UP or event.key == K_LEFT) and profile_list:

                        update = True

                        # Top of the list, jump to the bottom
                        if menu_pos == 0:
                            menu_pos = len(profile_list) - 1
                            offset = max(0, len(profile_list) - max_slots)

                        # Top of the itnerval, shift offset up
                        elif menu_pos == offset:
                            menu_pos -= 1
                            offset -= 1

                        # within interval, move cursor without changing shift
                        elif menu_pos > 0:
                            menu_pos -= 1

                    if (event.key == K_DOWN or event.key == K_RIGHT) and profile_list:

                        update = True

                        # Bottom of the list of slots: Jumps to the top
                        if menu_pos == len(profile_list) - 1:
                            menu_pos = 0
                            offset = 0

                        # Bottom of the interval, advance the offset by 1
                        elif menu_pos == offset + max_slots - 1:
                            offset += 1
                            menu_pos += 1

                        # intermediate interval: move the cursor only down by 1
                        elif menu_pos < len(profile_list) - 1:
                            menu_pos += 1

                    if event.key == K_x:
                        return

            if update:
                update = False

                # Draws the background
                self.engine.surface.blit(self.engine.mission_bg, (0, 0))
                self.draw_newspaper_title("Biographies")
                self.draw_article_lines()
                self.draw_author_and_date(report)

                # Draw list of hints
                self.draw_article_list(profile_list, offset)

                # Draws scroll bar and a selected hint
                if profile_list:
                    self.draw_scroll_bar(profile_list, offset)
                    self.draw_profile_data(profile_list[menu_pos], character_portraits[menu_pos] )
                    pygame.draw.rect(self.engine.surface, (50, 50, 50), (10, 155 + 60 * (menu_pos - offset), 250, 40),
                                     3)

                pygame.display.flip()
            self.engine.clock.tick(30)

    def draw_profile_data(self, profile, portrait):

        text_heading = self.engine.newspaper_mission_title_font.render(profile.name, True, (0, 0, 0))
        text_title = self.engine.newspaper_body_font.render("Title: %s"%profile.title, True, (0, 0, 0))
        text_specialty = self.engine.newspaper_body_font.render("Specialty: %s"%profile.specialty, True, (0, 0, 0))
        self.engine.surface.blit(portrait, (310, 155))
        self.engine.surface.blit(text_heading, (440, 155))
        self.engine.surface.blit(text_title, (440, 203))
        self.engine.surface.blit(text_specialty, (440, 225))

        draw_aligned_text(self.engine.surface, profile.desc,
                          self.engine.newspaper_body_font, (0, 0, 0), (310, 300), 510)

    def draw_newspaper_title(self, title_text):

        """
        function_name: draw_newspaper_title

        purpose: draws in big fancy letters the title of the newspaper section currently being viewed

        inputs - title_text : what text to display
        """

        text_title = self.engine.newspaper_top_font.render(title_text, True, (0, 0, 0))
        self.engine.surface.blit(text_title, (420 - text_title.get_width()/2, 15))

    def draw_front_options(self):

        """
        function name: draw_index_options

        purpose: draws the four options on the front page

        """

        text_options = [self.engine.newspaper_subtitle_font.render("Missions", True, (0, 0, 0)),
                        self.engine.newspaper_subtitle_font.render("Hints", True, (0, 0, 0)),
                        self.engine.newspaper_subtitle_font.render("Archives", True, (0, 0, 0)),
                        self.engine.newspaper_subtitle_font.render("Profiles", True, (0, 0, 0)),
                        self.engine.newspaper_subtitle_font.render("Cancel", True, (0, 0, 0))
                            ]

        background_panel = pygame.Surface((130, 60), pygame.SRCALPHA)
        background_panel.fill((100, 100, 100, 85))

        for index, option in enumerate(text_options):
            self.engine.surface.blit(background_panel, (10, 150 + index*80))
            self.engine.surface.blit(option, (75 - option.get_width()/2, 160 + index*80))

    def draw_front_lines(self):
        """
        function name: draw_front_lines

        purpose: draws the lines on the front page of the newspaper
        """


        pygame.draw.aaline(self.engine.surface, (50, 50, 50), (20, 95), (820, 95))
        pygame.draw.aaline(self.engine.surface, (50, 50, 50), (20, 135), (820, 135))

        pygame.draw.aaline(self.engine.surface, (50, 50, 50), (150, 150), (150, 620))

    def draw_report(self, report):
        """
        function name: draw_report

        purpose: draws the news report on the front page of the newspaper

        input: report - dictionary with keys for: name, subtitle, location, and the body
        """


        text_title = self.engine.newspaper_title_font.render(report['name'], True, (0, 0, 0))
        text_subtitle = self.engine.newspaper_subtitle_font.render(report['subtitle'], True, (80, 80, 80))

        self.engine.surface.blit(text_title, (160, 140))
        self.engine.surface.blit(text_subtitle, (160, 210))

        draw_aligned_text(self.engine.surface, report['location'].upper() + unichr(8212) + report['text'], self.engine.newspaper_body_font, (0, 0, 0), (160, 280), 660)

    def draw_author_and_date(self, report):
        """
        function name: draw_author_and_date

        purpose: Draws Aya's name and the date of the currently selected report

        input: report - dictionary with keys for: date
        """


        text_date = self.engine.newspaper_body_font.render(report['date'], True, (0, 0, 0))
        text_author = self.engine.newspaper_body_font.render("Aya Shameimaru", True, (0, 0, 0))

        self.engine.surface.blit(text_author, (30, 103))
        self.engine.surface.blit(text_date, (810 - text_date.get_width(), 100))

    def draw_article_list(self, article_list, offset):
        """
        function_name: draw_article_list

        purpose: draw the list of available articles to view

        input:  article_list - a list of articles (mission event objects or hints)
                offset - how far to offset the viewing window
        """
        max_slots = 8

        background_panel = pygame.Surface((250, 40), pygame.SRCALPHA)
        background_panel.fill((100, 100, 100, 85))

        for index, event in enumerate(article_list[offset:min(len(article_list), offset + max_slots)]):
            text_event = self.engine.newspaper_body_font.render(event.name, True, (0, 0, 0))

            self.engine.surface.blit(background_panel, (10, 155 + 60*index))
            self.engine.surface.blit(text_event, (10 + background_panel.get_width()/2 - text_event.get_width()/2,
                                                  155 + background_panel.get_height()/2 - text_event.get_height()/2 + 60*index))

    def draw_article_lines(self):
        """
        function name: draw_article_lines

        purpose: draws the lines on mission data and hints pages
        """

        pygame.draw.aaline(self.engine.surface, (50, 50, 50), (20, 95), (820, 95))
        pygame.draw.aaline(self.engine.surface, (50, 50, 50), (20, 135), (820, 135))

        pygame.draw.aaline(self.engine.surface, (50, 50, 50), (300, 150), (300, 620))
        pygame.draw.aaline(self.engine.surface, (50, 50, 50), (270, 150), (270, 620))

    def draw_mission_data(self, event):
        """
        function name: draw_mission_data

        purpose: draws the data for the selected mission

        input: event - mission event to draw data about
        """

        # Heading is the mission's name
        text_heading = self.engine.newspaper_mission_title_font.render(event.name, True, (0, 0, 0))
        self.engine.surface.blit(text_heading, (310, 155))

        # Include the location with the body of the description
        location_name = event.location_name + ", " + event.location.region.name
        draw_aligned_text(self.engine.surface, location_name.upper() + unichr(8212) + event.desc, self.engine.newspaper_body_font, (0, 0, 0), (310, 230), 510)


    def draw_hint_data(self, hint):
        """
        function name: draw_hint_data

        purpose: draws the data for the selected hint

        input: hint - hint to draw data about
        """


        text_heading = self.engine.newspaper_mission_title_font.render(hint.name, True, (0, 0, 0))
        text_author = self.engine.newspaper_body_font.render("(By: %s)"%hint.author, True, (0, 0, 0))
        self.engine.surface.blit(text_heading, (310, 155))
        self.engine.surface.blit(text_author, (310, 203))

        draw_aligned_text(self.engine.surface, hint.location.upper() + unichr(8212) + hint.text, self.engine.newspaper_body_font, (0, 0, 0), (310, 230), 510)

    def draw_scroll_bar(self, article_list, offset):
        """
        draw_scroll_bar

        purpose: draws a scroll bar

        inputs: article_list - a list of articles (missions or hints) that have been
                offset - current offset of the visible items window
                menu_pos - current position of selected recipe

        """
        max_slots = 8

        # Do not draw scrollbar if mission list is too short
        if len(article_list) <= max_slots:
            return

        scroll_bar_total = 60 * max_slots - 20
        scroll_bar = pygame.Surface((19, scroll_bar_total), pygame.SRCALPHA)
        scroll_bar.fill((150, 130, 140))
        pygame.draw.rect(scroll_bar, (50, 50, 50), (0, 0, 19, scroll_bar_total), 3)

        # Calculates the length of the scroll bar section and how far the spacing is
        #scroll_length = scroll_bar_total*max_slots/(len(all_recipe_data) - max_slots)
        scroll_length = scroll_bar_total*max_slots/(len(article_list))
        scroll_delta = (scroll_bar_total - scroll_length) / (len(article_list) - max_slots)

        scroll_bar_section = pygame.Surface((19, scroll_length), pygame.SRCALPHA)
        scroll_bar_section.fill((100, 100, 100))
        pygame.draw.rect(scroll_bar_section, (50, 50, 50), (0, 0, 19, scroll_length), 3)

        self.engine.surface.blit(scroll_bar, (276, 155))

        # Special case to clamp the scroll bar at the bottom of the screen to correct for round off
        if offset == len(article_list) - max_slots:
            self.engine.surface.blit(scroll_bar_section, (276, 155 + scroll_bar_total - scroll_bar_section.get_height()))
        else:
            self.engine.surface.blit(scroll_bar_section, (276, 155 + scroll_delta * offset))
