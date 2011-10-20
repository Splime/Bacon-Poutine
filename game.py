#game.py: A class to handle the actual game stuff

#NOTE: To Do: keep track of actions (i.e. removed when done) and display them

import pygame
import sys
import datetime
from clickablebutton import ClickableButton
from action import Action

class Game():
    
    def __init__(self, scr, toLoad):
        self.screen = scr
        self.windowX = self.screen.get_width()
        self.windowY = self.screen.get_height()
        self.fillerFont = pygame.font.Font(None, 24)
        self.gameBG = pygame.image.load("img/game_bg.png").convert()
        self.botPanel = pygame.image.load("img/ui/bottom_panel.png").convert()
        self.topLeft = pygame.image.load("img/ui/top_left.png").convert_alpha()
        self.botPanelRect = self.botPanel.get_rect()
        self.botPanelRect.bottom = self.windowY
        self.topLeftRect = self.topLeft.get_rect()
        self.saveButton = ClickableButton("img/buttons/save80x32.png",self.windowX - 96, self.windowY - 32,80,32)
        self.timeRatio = 60
        self.actionQueue = []
        #Load or New is important here
        if toLoad != None:
            self.loadGame(toLoad)
            self.saveName = toLoad
        else:
            self.newGame()
            self.saveName = "save.txt"
    
    def newGame(self):
        #Set up the time
        self.startTime = datetime.datetime.now()
        self.currTime = self.startTime
        #Add a test action
        self.actionQueue.append( Action("testType", "Testing the Action System...", self.startTime, datetime.timedelta(minutes=10), None) )
    
    def loadGame(self, toLoad):
        print "Loading game from %s..."%toLoad
        f = open(toLoad, 'r')
        prevGameTimeLine = f.readline()
        if prevGameTimeLine == '':
            print "No File Found!"
            self.newGame()
            f.close()
            return
        prevSaveTimeLine = f.readline()
        #Maybe more error checking here?
        #Now convert to datetimes!
        prevGameTime = self.textToDateTime(prevGameTimeLine)
        prevSaveTime = self.textToDateTime(prevSaveTimeLine)
        #Calculate the new game time!
        saveTimeDiff = datetime.datetime.now() - prevSaveTime
        gameTimeDiff = saveTimeDiff * self.timeRatio
        self.currTime = prevGameTime + gameTimeDiff
        #Load Actions/Fulfill based on time passed
        aLine = f.readline()
        if aLine != "actions:\n":
            print "ERROR!"
            pygame.quit()
            sys.exit()
        aLine = f.readline()
        while aLine != "endActions\n":
            #Code goes here to check if an action completed while away from the game
            anAction = self.textToAction(aLine)
            if anAction.isDone(self.currTime) == False:
                self.actionQueue.append(anAction)
            aLine = f.readline()
        #At this point, aLine == "endActions\n"
        
        #Generate new events based on time passed?
        #TODO
        
        #End File Stuff
        f.close()
        print "Load complete!"
        
    def saveGame(self, saveDest):
        print "Saving game to %s..."%saveDest
        f = open(saveDest, 'w')
        f.write("gametime,%s\n"%self.dateTimeToText(self.currTime))
        irlTime = datetime.datetime.now()
        f.write("savetime,%s\n"%self.dateTimeToText(irlTime))
        #Actions
        f.write("actions:\n")
        for act in self.actionQueue:
            f.write(self.actionToText(act))
        f.write("endActions\n")
        #End File Stuff
        f.close()
        print "Save complete!"
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()
            #Mouse Events
            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                toSave = self.saveButton.mouse_event(event)
                if toSave:
                    self.saveGame(self.saveName)
        
    def update(self, msPassed):
        #Do something with the time:
        timeDiff = datetime.timedelta(microseconds = self.timeRatio * msPassed * 1000)
        self.currTime = self.currTime + timeDiff
        #Check if any actions have finished
        for act in self.actionQueue:
            if act.isDone(self.currTime):
                print "Removing an event"
                self.actionQueue.remove(act)
    
    def draw(self):
        self.screen.blit(self.gameBG, pygame.Rect(0, 0, self.windowX, self.windowY))
        self.screen.blit(self.botPanel, self.botPanelRect)
        self.screen.blit(self.topLeft, self.topLeftRect)
        self.saveButton.draw(self.screen)
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
        self.saveGame(self.saveName)
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
    
    def textToDateTime(self, text): #For loading datetimes
        print "The text:%s"%text
        aList = text.rstrip().split(',')
        return datetime.datetime(int(aList[1]), int(aList[2]), int(aList[3]), int(aList[4]), int(aList[5]), int(aList[6]))
    
    def dateTimeToText(self, dt): #For saving datetimes
        return "%i,%i,%i,%i,%i,%i"%(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    
    def textToDelta(self, text): #For loading deltas
        aList = text.rstrip().split(',')
        return datetime.timedelta(int(aList[1]), int(aList[2]), int(aList[3]))
    
    def deltaToText(self, dlt): #For saving deltas
        return "%i,%i,%i"%(dlt.days, dlt.seconds, dlt.microseconds)
    
    def actionToText(self, act): #For saving actions
        aStr = "%s^%s^actStart,%s^actDuration,%s^"%(act.type, act.desc, self.dateTimeToText(act.startTime), self.deltaToText(act.duration))
        #Now deal with params
        if act.params == None:
            aStr += "None"
        else:
            #TODO
            pass
        return aStr+"\n"
        
    def textToAction(self, text): #For loading actions
        aList = text.rstrip().split('^')
        #Before making our Action, deal with params
        paramarams = None
        if aList[4] != "None":
            #TODO
            pass
        return Action(aList[0], aList[1], self.textToDateTime(aList[2]), self.textToDelta(aList[3]), paramarams)
