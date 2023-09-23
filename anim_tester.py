import pygame
import os
from sys import exit
from pygame.locals import *

from lostsky.bullet_scripts import catalog

class AnimTester(object):
    
    def __init__(self,surface):
        self.battle_bg = pygame.image.load(os.path.join('images','battlebg.jpg'))
        self.battle_panel = pygame.image.load(os.path.join('images','battlepanel2.png')).convert_alpha()
        self.battle_board = pygame.image.load(os.path.join('images','battleboard.png')).convert()
        self.battle_top = pygame.image.load(os.path.join('images','battletop.png')).convert_alpha()
        self.surface = surface
        self.clock = pygame.time.Clock()
                     
    def test_loop(self):
        
        bg = pygame.Surface(self.surface.get_size())
        
        bg.blit(self.battle_bg,(0,0))
        bg.blit(self.battle_board,(0,490))
        bg.blit(self.battle_top,(0,0))
        bg.blit(self.battle_panel, (175,290))
        bg.blit(self.battle_panel, (560,290))


        rhs_mode = False
        #for j in xrange (1,10):
        while True:

            self.surface.blit(bg,(0,0))
            
            spell_catalog = catalog.get_catalog()
            script = spell_catalog['misaki_curse'](self.surface,bg)
            
            pygame.display.update()
            self.clock.tick(60)
            
            t0 = pygame.time.get_ticks()
                
            for i in xrange(0,script.max_frames):
            
                    
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                        exit()
            
                script.clear()
                rects = script.update(t0,rhs_mode)
                
                pygame.display.update(rects)
                t0 = pygame.time.get_ticks()
                self.clock.tick(60)
            #print self.clock.get_fps()
            rhs_mode = not rhs_mode


def main():
    
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    tilesize = 35
    size_x = 24
    size_y = 18
    screen_size = (tilesize*size_x,tilesize*size_y)
    screen =  pygame.display.set_mode(screen_size,0, 32)
    
    anim_tester = AnimTester(screen)
    anim_tester.test_loop()
    
    
    
if __name__ == "__main__":
    main()
    #import cProfile as profile
    #profile.run('main()')