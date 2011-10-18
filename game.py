#game.py: A class to handle the actual game stuff

import pygame
import sys
import datetime

class Game():
    
    def __init__(self, scr):
        self.screen = scr
        self.windowX = self.screen.get_width()
        self.windowY = self.screen.get_height()
        self.fillerFont = pygame.font.Font(None, 32)
        self.gameBG = pygame.image.load("img/game_bg.png").convert()
        self.botPanel = pygame.image.load("img/ui/bottom_panel.png").convert()
        self.botPanelRect = self.botPanel.get_rect()
        self.botPanelRect.bottom = self.windowY
        #Set up the time
        self.startTime = datetime.datetime.now()
        self.currTime = self.startTime
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()
        
    def update(self, msPassed):
        #Do something with the time:
        self.currTime = datetime.datetime.now() #FILLER!
    
    def draw(self):
        self.screen.blit(self.gameBG, pygame.Rect(0, 0, self.windowX, self.windowY))
        self.screen.blit(self.botPanel, self.botPanelRect)
        #Some code to display the time and date
        timeStr = self.getTimeStr()
        timeText1 = self.fillerFont.render(timeStr, 1, (0, 0, 0))
        timeText2 = self.fillerFont.render("%i/%i/%i"%(self.currTime.month, self.currTime.day, self.currTime.year), 1, (0, 0, 0))
        timeRect1 = timeText1.get_rect()
        timeRect2 = timeText2.get_rect()
        timeRect1.center = (96, self.windowY - 96)
        timeRect2.center = (96, self.windowY - 32)
        self.screen.blit(timeText1, timeRect1)
        self.screen.blit(timeText2, timeRect2)
    
    #Copied from main.py D:
    def exit_game(self):
        """Exits the game completely"""
        print "Exiting Game"
        pygame.quit()
        sys.exit()
    
    #Here Lie the Helper Functions:
    def getTimeStr(self):
        leStr = ""
        hours = self.currTime.hour
        if hours < 10:
            leStr += "0%i"%hours
        else:
            leStr += "%i"%hours
        leStr += ":"
        mins = self.currTime.minute
        if mins < 10:
            leStr += "0%i"%mins
        else:
            leStr += "%i"%mins
        leStr += ":"
        secs = self.currTime.second
        if secs < 10:
            leStr += "0%i"%secs
        else:
            leStr += "%i"%secs
        return leStr
    