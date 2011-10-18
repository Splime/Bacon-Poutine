#introseq.py: A quick intro sequence to tell the player what's going on

import pygame
import sys

class IntroSeq():
    
    def __init__(self, scr):
        self.screen = scr
        self.intro0 = pygame.image.load("img/intro0.png").convert()
        self.timeToStay = 2000
        self.timePassed = 0
        self.doneYet = False
    
    def update(self, msPassed):
        self.timePassed += msPassed
        if self.timePassed >= self.timeToStay:
            self.doneYet = True
        
    def draw(self):
        self.screen.blit(self.intro0, pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height()))
