#Clickable Button: has a fancy button that changes animation based on mouse stuff
#Implements Object

import pygame
import sys
from object import Object

class ClickableButton(Object):
    
    NORMAL = 0
    HIGHLIGHT = 1
    CLICKED = 2
    
    def __init__(self, imgLocation, xPos, yPos, width, height):
        Object.__init__(self, imgLocation, xPos, yPos, width, height)
        #Modify the rect to include only one of three states
        self.rect.height = self.rect.height / 3
        self.rect.center = (xPos, yPos)
        self.subrect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        self.state = ClickableButton.NORMAL
    
    def mouse_event(self, event):
        """btw, this method should return True if the button activates"""
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.state = ClickableButton.NORMAL
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = ClickableButton.CLICKED
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if self.state != ClickableButton.CLICKED:
                    self.state = ClickableButton.HIGHLIGHT
            else:
                self.state = ClickableButton.NORMAL
        return False
    
    def draw(self, screen):
        self.subrect.top = self.state * self.rect.height
        screen.blit(self.img, self.rect, self.subrect)