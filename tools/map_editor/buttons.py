import tkFileDialog
import pygame
from pygame.locals import *

class Button(object):
    
    def __init__(self,window,name,image,location):
        """
        # function: __init__
        # Purpose: creates a button
        # Inputs:  window - parent map editor system
        #          name - displayed name of the button
        #          image - image to use as an icon (32x32)
        #          location - pixel location of the button (top left corner)         
        """
 
        self.image = image
        self.name = name
        self.location = location
        self.window = window
    
    def render(self):
        """
        # function: render
        # Purpose: draws the button and name
        """
 
        # Draw image
        self.window.screen.blit(self.image,self.location)

        # Draw box around it
        pygame.draw.rect(self.window.screen, (0,0,0),(self.location.x,self.location.y,32,32),1)

        # Draw name of button
        text_name = self.window.sfont.render(self.name,True,(0,0,0))
        self.window.screen.blit(text_name,(self.location.x+16-(text_name.get_width()/2),self.location.y + 35))

    def check_cursor_pos(self,pos):
        """
        # function: check_cursor_pos
        # Purpose: checks if the cursor is currently over the button
        # Inputs: pos - position (x,y) of the mouse
        # Outputs: True if cursor is over button, False otherwise
        """
        # Checks if the cursor is over the button
        if (pos[0] >= self.location.x and pos[0] <= self.location.x + self.image.get_width()
            and pos[1] >= self.location.y and pos[1] <= self.location.y + self.image.get_height()):
            return True
        else:
            return False
        
    def click(self):
        """
        # function: click
        # Purpose: does nothing for the base class
        """
        pass
    
class NewMap(Button):
    
    def __init__(self,window,name,image,location):
        """
        # function: __init__
        # Purpose: creates the new map button
        """
        Button.__init__(self,window,name,image,location)

    def click(self):
        """
        # function: click
        # Purpose: when clicked, clears the map and restores it to a blank one with only grass
        """
        print "Clearing map."
        # Resets the map to blank grass tiles
        self.window.canvas.terrain_map = self.window.canvas.generate_new_map()

        self.window.canvas.terrain_minimap = self.window.canvas.generate_minimap()

class SaveMap(Button):
    
    def __init__(self,window,name,image,location):
        """
        # function: __init__
        # Purpose: creates the save map button
        """
        Button.__init__(self,window,name,image,location)

    def click(self):
        """
        # function: click
        # Purpose: when clicked, asks the user to select a file to save the data to
        """
        
        print "Saving map."
        filename = tkFileDialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text file','.txt')],initialdir='maps')
        pygame.event.clear()
        if filename:
            self.window.canvas.save_canvas(filename)
        pygame.event.clear()

            
class LoadMap(Button):
    
    def __init__(self,window,name,image,location):
        """
        # function: __init__
        # Purpose: creates the load map button
        """
        
        Button.__init__(self,window,name,image,location)

    def click(self):
        """
        # function: click
        # Purpose: when clicked, asks the user to select a file to load map data from
        """
        
        print "Loading map."
        # Resets the map to blank grass tiles
        filename = tkFileDialog.askopenfilename(defaultextension='.txt', filetypes=[('Text file','.txt')],initialdir='maps')
        pygame.event.clear()
        if filename:
            self.window.canvas.load_canvas(filename)
        pygame.event.clear()

class SwapLayer(Button):
    def __init__(self,window,name,layer_1_image,layer_2_image,location):
        """
        # function: __init__
        # Purpose: creates the load map button
        """
        
        Button.__init__(self,window,name,layer_1_image,location)
        self.layer_1_image = layer_1_image
        self.layer_2_image = layer_2_image
        
    def render(self):
        """
        # function: render
        # Purpose: draws the button only
        """
 
        # Draw image
        if self.window.palette.layer_2:
            self.window.screen.blit(self.layer_2_image,self.location)
        else:
            self.window.screen.blit(self.layer_1_image,self.location)

        # Draw box around it
        pygame.draw.rect(self.window.screen, (0,0,0),(self.location.x,self.location.y,32,32),1)

        # Draw name of button
        text_name = self.window.sfont.render(self.name,True,(0,0,0))
        self.window.screen.blit(text_name,(self.location.x+16-(text_name.get_width()/2),self.location.y + 35))

    def click(self):
        self.window.palette.layer_2 = not self.window.palette.layer_2


class Resize(Button):
    
    def __init__(self,window,name,image,location,coord,direction):
        """
        # function: __init__
        # Purpose: creates a resize button
        # Inputs: coord = 'x' or 'y'
        #         direction = +1 or -1
        """
        Button.__init__(self,window,name,image,location)
        self.coord = coord
        self.direction = direction
    
    def render(self):
        """
        # function: render
        # Purpose: draws the button only
        """
 
        # Draw image
        self.window.screen.blit(self.image,self.location)

        # Draw box around it
        pygame.draw.rect(self.window.screen, (0,0,0),(self.location.x,self.location.y,32,32),1)

    
    def click(self):
        """
        # function: click
        # Purpose: when clicked, changes the canvas size
        """
        self.window.canvas.resize(self.coord,self.direction)

