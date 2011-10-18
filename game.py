#game.py: A class to handle the actual game stuff

import pygame
import sys
import datetime

class Game():
    
    def __init__(self, scr, toLoad):
        self.screen = scr
        self.windowX = self.screen.get_width()
        self.windowY = self.screen.get_height()
        self.fillerFont = pygame.font.Font(None, 24)
        self.gameBG = pygame.image.load("img/game_bg.png").convert()
        self.botPanel = pygame.image.load("img/ui/bottom_panel.png").convert()
        self.botPanelRect = self.botPanel.get_rect()
        self.botPanelRect.bottom = self.windowY
        self.timeRatio = 60
        #Load or New is important here
        if toLoad != None:
            self.loadGame(toLoad)
        else:
            self.newGame()
    
    def newGame(self):
        #Set up the time
        self.startTime = datetime.datetime.now()
        self.currTime = self.startTime
    
    def loadGame(self, toLoad):
        print "Loading is not yet enabled! Starting a new game anyway..."
        self.newGame()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()
        
    def update(self, msPassed):
        #Do something with the time:
        timeDiff = datetime.timedelta(microseconds = self.timeRatio * msPassed * 1000)
        self.currTime = self.currTime + timeDiff        
    
    def draw(self):
        self.screen.blit(self.gameBG, pygame.Rect(0, 0, self.windowX, self.windowY))
        self.screen.blit(self.botPanel, self.botPanelRect)
        #Some code to display the time and date
        timeStr = self.getTimeStr()
        timeText1 = self.fillerFont.render(timeStr, 1, (0, 0, 0))
        timeText2 = self.fillerFont.render("%i/%i/%i"%(self.currTime.month, self.currTime.day, self.currTime.year), 1, (0, 0, 0))
        timeRect1 = timeText1.get_rect()
        timeRect2 = timeText2.get_rect()
        timeRect1.center = (32, self.windowY - 96)
        timeRect2.center = (128, self.windowY - 96)
        self.screen.blit(timeText1, timeRect1)
        self.screen.blit(timeText2, timeRect2)
    
    #Copied from main.py D:
    def exit_game(self):
        """Exits the game completely"""
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
        return leStr
    