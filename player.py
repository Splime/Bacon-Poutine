#player.py: A quick class for a player

import pygame
from chapMap import CMap
from action import Action

class Player:

    def __init__(self, name, pos, theMap):
        self.name = name
        self.pos = pos #pos[0] should be x, pos[1] should be y
        self.cmap = theMap
        self.img = pygame.image.load("img/map/plyr.png")
        self.action = None
    
    def update(self, msPassed, currTime):
        #Do stuff here like checking up on actions (e.g. updating position during movement)
        if self.action != None:
            if self.action.type == "movement":
                #Determine how much time has passed since the start
                minutesPassed = (currTime - self.action.startTime).seconds / 60
                self.pos = self.action.path[int(minutesPassed/Action.WALKING_SPEED)]
            if self.action.isDone(currTime):
                # if self.action.type == "movement":
                    # self.pos = self.action.path[len(self.action.path)-1]
                self.action = None
        
    def draw(self, screen):
        plyrRect = pygame.Rect(0, 0,32,32)
        plyrRect.center = self.cmap.calc_display(self.pos[0], self.pos[1])
        screen.blit(self.img, plyrRect)
        