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