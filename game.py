#game.py: A class to handle the actual game stuff

import pygame
import sys

class Game():
    
    def __init__(self, scr):
        self.screen = scr
        self.gameBG = pygame.image.load("img/game_bg.png").convert()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()
        
    def update(self, msPassed):
        pass
    
    def draw(self):
        self.screen.blit(self.gameBG, pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height()))
    
    #Copied from main.py D:
    def exit_game(self):
        """Exits the game completely"""
        print "Exiting Game"
        pygame.quit()
        sys.exit()