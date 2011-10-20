#Object class

import pygame

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
        self.img = pygame.image.load(imgLocation)
        self.rect = self.img.get_rect()
        self.x = xPos
        self.y = yPos
        self.width = width
        self.height = height
        self.rect.center = (self.x,self.y)
    
    def moveToward(self,xPos,yPos):
        self.x = xPos
        self.y = yPos
        self.rect.center = (self.x,self.y)
    
    def imageTransform(self,imgLocation):
        self.location = imgLocation
        self.img = pygame.image.load(imageLocation).convert()
        
    def draw(self, screen):
        screen.blit(self.img, self.rect)