#gridIcon.py: A class representing the UI part of a grid square, where one is selectable
#Extends ClickableButton

import pygame
from clickablebutton import ClickableButton

class GridIcon(ClickableButton):
    
    NORMAL = 0
    HIGHLIGHT = 1
    CLICKED = 2
    
    UNSELECTED = 0
    SELECTED = 1
    
    #Constants for isometrification
    HORIZ_SHIFT = 30
    VERT_SHIFT = 15
    
    def __init__(self, imgLocation, xPos, yPos, width, height):
        ClickableButton.__init__(self, imgLocation, xPos, yPos, width, height)
        self.rect.width = self.rect.width / 2
        self.rect.center = (xPos, yPos)
        self.subrect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        self.state = GridIcon.NORMAL
        self.selected = GridIcon.UNSELECTED
    
    def mouse_event(self, event):
        results = ClickableButton.mouse_event(self, event)
        if results:
            self.selected = GridIcon.SELECTED
        return results
    
    def draw(self, screen):
        self.subrect.left = self.selected * self.rect.width
        ClickableButton.draw(self, screen)
    
    #Overwrite Existing mouse_collide!
    def mouse_collide(self, pos):
        diffX = pos[0]-self.x
        diffY = pos[1]-self.y
        if diffX > 0:
            return diffY < -.5*diffX + GridIcon.VERT_SHIFT and diffY > .5*diffX - GridIcon.VERT_SHIFT
        else:
            return diffY < .5*diffX + GridIcon.VERT_SHIFT and diffY > -.5*diffX - GridIcon.VERT_SHIFT