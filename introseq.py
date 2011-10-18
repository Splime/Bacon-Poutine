#introseq.py: A quick intro sequence to tell the player what's going on

import pygame
import sys

class IntroSeq():
    
    def __init__(self, scr):
        self.screen = scr
        self.intro0 = pygame.image.load("img/intro0.png").convert()
    
    def update(self):
        pass
        
    def draw(self):
        self.screen.blit(self.intro0, pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height()))
