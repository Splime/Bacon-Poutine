#player.py: A quick class for a player

import pygame
from chapMap import CMap

class Player:

    def __init__(self, name, pos, theMap):
        self.name = name
        self.pos = pos #pos[0] should be x, pos[1] should be y
        self.cmap = theMap
        self.img = pygame.image.load("img/map/plyr.png")
        self.action = None
    
    def update(self, msPassed):
        #Do stuff here like checking up on actions (e.g. updating position during movement)
        if self.action != None and self.action.done:
            if self.action.type == "movement":
                self.pos = self.action.path[len(self.action.path)-1]
            self.action = None
        
    def draw(self, screen):
        screen.blit(self.img, pygame.Rect(self.cmap.targetRect.left+self.cmap.tileX*self.pos[0], self.cmap.targetRect.top+self.cmap.tileY*self.pos[1],self.cmap.tileX,self.cmap.tileY))
        