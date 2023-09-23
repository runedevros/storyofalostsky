import pygame
from pygame.locals import *
import os
from lostsky.core.linalg import Vector2
from lostsky.core import xmlreader
from random import randint
from math import floor
from buttons import NewMap, SaveMap, LoadMap, Resize, SwapLayer
import string

class MapEditor(object):
    
    
    def __init__(self, screen):
        """
        # function: __init__
        # Purpose: creates Main Map Editor system
        """
        
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.sfont = pygame.font.Font(os.path.join('fonts',"DejaVuSans-Oblique.ttf"), 12)
        self.mfont = pygame.font.Font(os.path.join('fonts',"DejaVuSans-Oblique.ttf"), 16)
        self.bfont = pygame.font.Font(os.path.join('fonts',"VeraSeBd.ttf"), 14)
        self.cfont = pygame.font.Font(os.path.join('fonts',"VeraSeBd.ttf"), 24)
    
        # Menu_buttons
        self.buttons = [NewMap(self,
                               'New',
                               pygame.image.load(os.path.join('images','map_editor_images','map.png')).convert_alpha(),
                               Vector2(5,5)),
                        SaveMap(self,
                               'Save',
                               pygame.image.load(os.path.join('images','map_editor_images','disk.png')).convert_alpha(),
                               Vector2(42,5)),
                        LoadMap(self,
                               'Load',
                               pygame.image.load(os.path.join('images','map_editor_images','folder.png')).convert_alpha(),
                               Vector2(84,5)),
                        SwapLayer(self,
                               'Layer',
                               pygame.image.load(os.path.join('images','map_editor_images','layer_1.png')).convert_alpha(),
                               pygame.image.load(os.path.join('images','map_editor_images','layer_2.png')).convert_alpha(),
                               Vector2(124,5))
                        ]
        
        # Setup Map Canvas
        self.tile_image = pygame.image.load(os.path.join('images','terraintilesv4.png')).convert_alpha()
        self.cliff_tiles = pygame.image.load(os.path.join('images','layer_2_tiles.png')).convert_alpha()
        self.terrain_data, self.terrain_data_by_symbol = xmlreader.get_terrain_data()

        # Find where the layer 2 tiles start
        # +2 offset accounts for 0 indexing of lists
        for index, terrain in enumerate(self.terrain_data):
            self.layer2_index = index
            if terrain.layer2:
                break
        else:
            self.layer2_index = 0

        # Loads only the base terrain and not layer 2 data
        self.tile_image_catalog = [self.tile_image.subsurface(0,70*index,35,35)
                                 for index in xrange(0, self.layer2_index)]
    
        self.canvas = MapCanvas(self,50,50)

        # Counter to track scrolling on the map
        self.scroll_frames = 0
        # Counter to track holding down of mouse over resize menu
        self.resize_frames = 0
        
        # Setup Palette
        self.palette = Palette(self)

        # Setup resize menu
        self.resize_menu = ResizeMenu(self)
    
    def render_buttons(self):
        """
        # function: render_buttons
        # Purpose: Draws all the menu buttons
        """
        
        [button.render() for button in self.buttons]
        
    def render_all(self):
        """
        # function: render_all
        # Purpose: Draws all the objects on the screen
        """
        
        self.screen.fill((200,200,200))
        self.render_buttons()
        self.canvas.render_tiles()
        self.canvas.draw_grid()

        self.palette.render_palette()
        self.resize_menu.render()
        self.render_minimap()
    
        # Line dividing left/right sides of the screen
        pygame.draw.line(self.screen,(0,0,0),(200,0),(200,600))

    def render_minimap(self):
        """
        # function: render_minimap
        # Purpose: Draws the minimap for navigation
        """
        self.screen.blit(self.canvas.terrain_minimap,(6,391))
        pygame.draw.rect(self.screen,(0,0,0),(6+self.canvas.screen_shift.x,391+self.canvas.screen_shift.y,16,15),1)
        pygame.draw.rect(self.screen,(0,0,0),(5,390,101,101),1)
        
    def editor_user_input(self):
        """
        # function: editor_user_input
        # Purpose: Handles user interaction to the program
        """
        arrowkeys = False
        mouseclick = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                exit()
            # move the map with arrow keys
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                    self.cursor_arrows(event)
                    arrowkeys = True
                    self.scroll_frames = 0
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                
                # Case if position is in the palette region
                if (event.pos[0] > 5 and event.pos[1] > 60
                    and event.pos[0] < 190 and event.pos[1] < 390):
                    self.palette.click(event.pos)
                # Case if position is in the canvas region
                elif (event.pos[0] > 200 and event.pos[0] < 760
                    and event.pos[1] < 525):
                    self.canvas.left_click(event.pos)
                # Case if position is in the menu buttons region
                elif (event.pos[0] < 200 and event.pos[1] < 60):
                    [button.click() for button in self.buttons if button.check_cursor_pos(event.pos)]
                # Case if position is in the resize region
                elif (event.pos[0] > 5 and event.pos[1] > 490
                    and event.pos[0] < 190 and event.pos[1] < 590):
                    [button.click() for button in self.resize_menu.arrows if button.check_cursor_pos(event.pos)]
                    self.resize_frames = 0
                mouseclick = True
  
  
            # Right click selects the tile type under the cursor 
            if (event.type == MOUSEBUTTONDOWN and event.button == 3
                and event.pos[0] > 200 and event.pos[0] < 760
                and event.pos[1] < 525):
                self.canvas.right_click(event.pos)
                    
        # if there is not a tap detected, check if the key is being held down
        if arrowkeys == False and self.scroll_frames == 9:
            self.cursor_arrows_hold()

        if mouseclick == False and pygame.mouse.get_pressed()[0] and self.resize_frames == 9:
            mouse_position = pygame.mouse.get_pos()
            if (mouse_position[0] > 5 and mouse_position[0] < 190  
                and mouse_position[1] > 490 and mouse_position[1] < 590):
                [button.click() for button in self.resize_menu.arrows if button.check_cursor_pos(mouse_position)]
            self.resize_frames = 0
            
        # Mouse held down 
        if pygame.mouse.get_pressed()[0]:
            mouse_position = pygame.mouse.get_pos()
            
            # Set shifted position on minimap
            if (mouse_position[0] >= 6 and mouse_position[0] <= 105
                and mouse_position[1] >= 390 and mouse_position[1] <= 490):
                
                # Sets teh box in the middle of the cursor
                # Relative Position = Mouse Position - Origin + Shift of (-8,-7)
                 
                new_shift = Vector2(mouse_position) - Vector2(6,390) - Vector2(8,7)
                new_shift.x = max(0,min(new_shift.x,self.canvas.size_x-16))
                new_shift.y = max(0,min(new_shift.y,self.canvas.size_y-15))
                
                self.canvas.screen_shift.x = new_shift.x
                self.canvas.screen_shift.y = new_shift.y
                
                
            # Draw on the map
            if (mouse_position[0] > 200 and mouse_position[0] < 760
                    and mouse_position[1] < 525):
                self.canvas.left_click(pygame.mouse.get_pos())
  
    def cursor_arrows(self,event):
        """
        # Function Name: cursor_arrows
        # Purpose: allows a user to move the map around by tapping down a key
        """
        if event.key == K_LEFT and self.canvas.screen_shift.x > 0:
            self.canvas.screen_shift.x += -1
        
        elif (event.key == K_RIGHT 
              and self.canvas.screen_shift.x + 16 < self.canvas.size_x):
            self.canvas.screen_shift.x += +1
                
        if event.key == K_UP and self.canvas.screen_shift.y > 0:
            self.canvas.screen_shift.y += -1
                
        elif (event.key == K_DOWN 
              and self.canvas.screen_shift.y + 15 < self.canvas.size_y):
            self.canvas.screen_shift.y += +1

    def cursor_arrows_hold(self):
        """
        # Function Name: cursor_arrows_hold
        # Purpose: allows a user to move the map around by holding the arrow keys down
        """
        key = pygame.key.get_pressed()

        if key[K_LEFT] and self.canvas.screen_shift.x > 0:
            self.canvas.screen_shift.x += -1
            
            # Reset Frame counter to 6
            self.scroll_frames = 6
            
        elif (key[K_RIGHT]
              and self.canvas.screen_shift.x + 16 < self.canvas.size_x):
            self.canvas.screen_shift.x += +1
            
            # Reset Frame counter to 6
            self.scroll_frames = 6
                
        if key[K_UP] and self.canvas.screen_shift.y > 0:
            self.canvas.screen_shift.y += -1
                
            # Reset Frame counter to 6
            self.scroll_frames = 6
            
        elif (key[K_DOWN] 
              and self.canvas.screen_shift.y + 15 < self.canvas.size_y):
            self.canvas.screen_shift.y += +1
    
            # Reset Frame counter to 6
            self.scroll_frames = 6
            
        pygame.event.clear()
    
    def editor_loop(self):
        """
        # function: editor_loop
        # Purpose: runs the main loop of the program
        """
        
        menu_flag = True
        while menu_flag:
            # looks for event type data to select interaction
            self.editor_user_input()
            
            self.render_all()
            pygame.display.flip()
            self.scroll_frames += 1
            self.resize_frames += 1
            self.clock.tick(60)


class MapCanvas(object):
    
    def __init__(self,window,size_x,size_y):
        """
        # function: __init__
        # Purpose: creates the canvas object which displays the map
        # Inputs:  window - parent map editor system
        #          size_x,size_y - size of the map
        """
        
        self.window = window
        self.size_x = size_x
        self.size_y = size_y
        self.terrain_map = self.generate_new_map()
        self.terrain_minimap = self.generate_minimap()
        self.cliff_layer = {}
        self.screen_shift = Vector2(0,0)
    
    def generate_new_map(self):
        """
        # function: generate_new_map
        # Purpose: Creates a new map composed of all grass tiles
        """
        
        terrain_map = {}
        for x in xrange(0,self.size_x):
            for y in xrange(0,self.size_y):
                terrain_map[(x,y)] = self.window.terrain_data[1]

        self.cliff_layer = {}
        return terrain_map
    
    def generate_minimap(self):
        """
        # function: generate_minimap
        # Purpose: generates a minimap from the current set of tiles
        """
        minimap = pygame.Surface((99,99),SRCALPHA)
        for x in xrange(0,self.size_x):
            for y in xrange(0,self.size_y):
                minimap.set_at((x,y),self.terrain_map[(x,y)].color)

        return minimap
        
        

    def render_tiles(self):
        """
        # function: render_tiles
        # Purpose: Draw all the tiles
        """
        for x in xrange(0,16):
            for y in xrange(0,15):
            
                location = (self.screen_shift.x+x,self.screen_shift.y+y)
            
                self.window.screen.blit(self.window.tile_image_catalog[self.terrain_map[location].ident],
                                        (x*35+200,y*35))

            
                if location in self.cliff_layer.keys():
                    self.window.screen.blit(self.window.cliff_tiles,
                                            (x*35+200,y*35),
                                            (self.cliff_layer[location][0]*35,self.cliff_layer[location][1]*35,35,35))
                    
    
    def draw_grid(self):
        """
        # function: draw grid
        # Purpose: draws the grid over the canvas region
        """
        
        # Box around canvas
        pygame.draw.rect(self.window.screen,(0,0,0),(200,0,16*35,15*35),1)
        
        # Draw vertical lines
        for x in xrange(1,16):
            pygame.draw.line(self.window.screen,(0,0,0),(200+x*35,0),(200+x*35,15*35-1))

        # Draw horizontal lines
        for y in xrange(1,15):
            pygame.draw.line(self.window.screen,(0,0,0),(200,y*35),(759,y*35))
                
    def get_location(self,pos):
        """
        # Function: get_location
        # Purpose: Translates a mouse position over the map to a tile position
        # Inputs: pos - position (x,y) of the mouse
        """
        
        # Determine position of mouse relative to the origin of the map
        relative_vector = Vector2(pos) - Vector2(200,0)
        # Scale relative vector down
        scaled_vector = Vector2(floor(relative_vector.x/35),floor(relative_vector.y/35))
        # Accounts for the shift of the displayed map
        location = tuple(self.screen_shift + scaled_vector)
        return location
    
    def left_click(self,pos):
        """
        # Function: left_click
        # Purpose: replaces current tile under the cursor with the one selected in the palette 
        # Inputs: pos - position (x,y) of the mouse
        """
        
        location = self.get_location(pos)
        
        # Replace the currently clicked tile with the selected tile in the palette
        if not self.window.palette.layer_2:
            self.terrain_map[location] = self.window.terrain_data[self.window.palette.selected]
        else:
            self.cliff_layer[location] = self.window.palette.selected_layer2
            
            
        # Updates Minimap
        self.terrain_minimap.set_at((int(location[0]),int(location[1])),self.terrain_map[location].color)

    def right_click(self,pos):
        """
        # Function: right_click
        # Purpose: Sets the type of terrain under the cursor to be the selected one 
        # Inputs: pos - position (x,y) of the mouse
        """
        
        location = self.get_location(pos)
        
        # Replace the currently clicked tile with the selected tile in the palette
        if not self.window.palette.layer_2:
            self.window.palette.selected = self.terrain_map[location].ident
        else:
            if location in self.cliff_layer.keys():
                del self.cliff_layer[location]
    
    def load_canvas(self,filename):
        """
        # Function: load_canvas
        # Purpose: loads the canvas from a text file
        # Inputs: filename - location to load map data from
        """
        
        def str_2_tuple(coord):
            """
            Converts a string of the form '(x, y, z)' to a tuple of integers
            """
            # Splits the string by commas
            coord = string.strip(coord)
            split_string = string.split(coord[1:-1],', ')
            return tuple([int(entry) for entry in split_string])
            
        file = open(filename,'r')
        # First 2 lines correspond to size data
        self.size_x = int(file.readline())
        self.size_y = int(file.readline())
        # Load terrain data
        self.terrain_map = {}
        self.cliff_layer = {}
        
        # Reads in remaining lines terrainmap
        # Horizontal slice
        for y in xrange(0,self.size_y):
            line = file.readline()
            # Tile within horizontal slice
            for x, letter in enumerate(line):
                if letter in self.window.terrain_data_by_symbol.keys():
                    self.terrain_map[(x,y)] = self.window.terrain_data_by_symbol[letter]
        self.terrain_minimap = self.generate_minimap()

        for y in xrange(0,self.size_y):
            line = file.readline()
            # Tile within horizontal slice
            for x, tile in enumerate(string.split(line,'|')):
                # x indicates an empty tile
                if tile and tile != 'x' and tile != "x\n":
                    self.cliff_layer[(x,y)] = str_2_tuple(tile)

        # Resets shift if out of bounds
        if self.screen_shift.x + 16 >= self.size_x:
            self.screen_shift.x = self.size_x - 16
        if self.screen_shift.y + 15 >= self.size_y:
            self.screen_shift.y = self.size_y - 15
    
            
    def save_canvas(self,filename):
        """
        # Function: save_canvas
        # Purpose: saves the canvas to a text file
        # Inputs: filename - location to save map data to
        """
        
        file = open(filename,'w')
        
        # Writes map sizes
        file.write(str(self.size_x)+"\n")
        file.write(str(self.size_y)+"\n")
        
        # Writes the rest of the tiles in horizontal slices
        for y in xrange(0,self.size_y):
            line = ""
            for x in xrange(0,self.size_x):
                line += self.terrain_map[(x,y)].symbol
            line += "\n"
            file.write(line)
        
        # Writes cliff tiles
        for y in xrange(0,self.size_y):
            line = ""
            for x in xrange(0,self.size_x):
                # If there is a cliff tile present, write the tile location
                # otherwise, use the letter X to represent an unoccupied tile
                if (x,y) in self.cliff_layer.keys():
                    line += str(self.cliff_layer[(x,y)])
                else:
                    line += "x"
                # Adds a space separator between each entry
                if x < self.size_x-1:
                    line += "|"
            
            line += "\n"
            file.write(line)
        
    def resize(self,coord,value):
        """
        # Function: resize
        # Purpose: Resize the map
        # Inputs: coord = 'x' or 'y'
        #        value = 1 or -1
        """
        old_x = self.size_x
        old_y = self.size_y
        
        if coord == 'x' and ((value == 1 and self.size_x < 99) or (value == -1 and self.size_x > 25)): 
            self.size_x += value
            # Adds a column of tiles
            if value == 1:
                for y in xrange(0,self.size_y):
                    self.terrain_map[(self.size_x-1,y)] = self.window.terrain_data[1]
                    self.terrain_minimap.set_at((self.size_x-1,y),self.terrain_map[(self.size_x-1,y)].color)
            
            # Deletes a column of tiles
            elif value == -1:
                for y in xrange(0,self.size_y):
                    del self.terrain_map[(self.size_x,y)]
                    self.terrain_minimap.set_at((self.size_x,y),(0,0,0,0))
            
        elif coord == 'y' and ((value == 1 and self.size_y < 99) or (value == -1 and self.size_y > 15)): 
            self.size_y += value
            # Adds a row of tiles
            if value == 1:
                for x in xrange(0,self.size_x):
                    self.terrain_map[(x,self.size_y-1)] = self.window.terrain_data[1]
                    self.terrain_minimap.set_at((x,self.size_y-1),self.terrain_map[(x,self.size_y-1)].color)
            
            # Deletes a column of tiles
            elif value == -1:
                for x in xrange(0,self.size_x):
                    del self.terrain_map[(x,self.size_y)]
                    self.terrain_minimap.set_at((x,self.size_y),(0,0,0,0))
            
                
        # Resets shift if out of bounds
        if self.screen_shift.x + 16 >= self.size_x:
            self.screen_shift.x = self.size_x - 16
        if self.screen_shift.y + 15 >= self.size_y:
            self.screen_shift.y = self.size_y - 15
        

class Palette(object):
    
    def __init__(self,window):
        """
        # Function: __init__
        # Purpose: initializes a palette object. Controls the selection of tiles to paint
        # Inputs: window - parent map editor system
        """
        
        self.window = window
        self.selected = 0
        self.selected_layer2 = (0,1)

        # Corresponds to empty tiles on the cliff grid
        self.layer_2_prohibited = [(0,0),(1,0),(3,1)]
        # Sets to draw in layer 1 and layer 2
        self.layer_2 = False
        
    def render_palette(self):
        """
        # Function: render_palette
        # Purpose: Draws a set of tiles on the left side of the screen for the palette
        """
        if not self.layer_2:
            for index in xrange(0,self.window.layer2_index):
                self.window.screen.blit(self.window.tile_image_catalog[index],(10,65+index*35))
        else:
            self.window.screen.blit(self.window.cliff_tiles,(10,65))

        # Box around palette
        pygame.draw.rect(self.window.screen,(0,0,0),(5,60,185,530),1)
        
        # Draws a black box around selected tile
        if not self.layer_2:
            pygame.draw.rect(self.window.screen,(0,0,0),(10,65+self.selected*35,35,35),3)
        else:
            pygame.draw.rect(self.window.screen,(0,0,0),(10+self.selected_layer2[0]*35,65+self.selected_layer2[1]*35,35,35),3)
        
    
    def click(self,pos):
        """
        # Function: click
        # Purpose: Processes a registered click in the palette
        # Inputs: pos - position (x,y) of the mouse
        """
        # Checks if the click falls on one of the palette tiles
        if not self.layer_2:
            if pos[0] >= 10 and pos[0] <= 45:
                index = int(floor((pos[1] - 65)/35))
                if index >= 0 and index < len(self.window.terrain_data):
                    self.selected = index
        else:
            if (pos[0] >= 10 and pos[0] <= 185 and pos [1] >= 65 and pos[1] <= 65+self.window.cliff_tiles.get_height()):
                # Calculates which tile is selected
                index = (int(floor((pos[0] - 10)/35)),int(floor((pos[1] - 65)/35)))
                if index not in self.layer_2_prohibited:
                    self.selected_layer2 = tuple(index)
                
                
class ResizeMenu(object):
    
    def __init__(self,window):
        """
        # functioN: __init__
        # Purpose: A small menu in the bottom left corner to resize the map
        #         Max Size: (99,99)
        #         Min Size: (25,15)
        """
        self.window = window
        self.arrows = [Resize(self.window,'plus_x',
                       pygame.image.load(os.path.join('images','map_editor_images','arrow_up.png')).convert_alpha(),
                       Vector2(10,520),'x',1),
                       Resize(self.window, 'plus_y',
                       pygame.image.load(os.path.join('images','map_editor_images','arrow_up.png')).convert_alpha(),
                       Vector2(10,555),'y',1),
                       Resize(self.window, 'minus_x',
                       pygame.image.load(os.path.join('images','map_editor_images','arrow_down.png')).convert_alpha(),
                       Vector2(100,520),'x',-1),
                       Resize(self.window, 'minus_y',
                       pygame.image.load(os.path.join('images','map_editor_images','arrow_down.png')).convert_alpha(),
                       Vector2(100,555),'y',-1)
                       ]
    def render(self):
        """
        # function: render
        # Purpose: Renders the resize menu 
        """
        text_mapsize = self.window.sfont.render('Map Size',True,(0,0,0))
        
        if self.window.canvas.size_x == 99 or self.window.canvas.size_x == 25:
            text_size_x = self.window.bfont.render("X: "+str(self.window.canvas.size_x),True,(255,0,0))
        else:
            text_size_x = self.window.bfont.render("X: "+str(self.window.canvas.size_x),True,(0,0,0))

        if self.window.canvas.size_y == 99 or self.window.canvas.size_y == 15:
            text_size_y = self.window.bfont.render("Y: "+str(self.window.canvas.size_y),True,(255,0,0))
        else:
            text_size_y = self.window.bfont.render("Y: "+str(self.window.canvas.size_y),True,(0,0,0))
                                                      
        self.window.screen.blit(text_mapsize,(10,500))
        # Renders buttons
        [button.render() for button in self.arrows]
        self.window.screen.blit(text_size_x, (50,525))
        self.window.screen.blit(text_size_y, (50,560))
        
        pygame.draw.rect(self.window.screen,(0,0,0),(5,490,185,100),1)