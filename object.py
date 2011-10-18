#Object class

import pygame
import sys
from introseq import IntroSeq


class Object:
    location = ""
    img = 0
    rect = 0
    x = 0
    y = 0
    width = 0
    height = 0
    
    def __init__(self,imgLocation,xPos,yPos,width,height):
        self.location = imgLocation
        self.img = pygame.image.load(imgLocation).convert()
        self.rect = self.img.get_rect()
        self.x = xPos
        self.y = yPos
        self.width = width
        self.height = height
        self.rect.center = (self.x,self.y)