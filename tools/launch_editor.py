## Lost sky map movement test
import pygame
from pygame.locals import *
from map_editor.map_editor import MapEditor
import os
import Tkinter as tk

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Initiates Tk system used for file dialogs
    tk.Tk().withdraw()
    
    # Starts up Pygame
    pygame.init()
    screen_size = (800,600)
    screen =  pygame.display.set_mode(screen_size,0, 32)
    
    # Sets up editor engine
    editor_engine = MapEditor(screen)
    
    # Starts editor
    editor_engine.editor_loop()

if __name__ == "__main__":
    main()