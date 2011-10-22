#game.py: A class to handle the actual game stuff

import pygame
import sys
import datetime
from clickablebutton import ClickableButton
from action import Action
from map import Map
from grid import Node
from aStar import AStar
from object import Object
from math import floor, tan, radians

class Game():

    QUIT_GAME = -2
    QUIT_TO_MENU = -1
    NORMAL = 0
    POP_UP_MENU = 1
    POP_UP_QUIT = 2
    
    def __init__(self, scr, toLoad):
        self.state = Game.NORMAL
        self.quitState = Game.NORMAL
        self.screen = scr
        self.windowX = self.screen.get_width()
        self.windowY = self.screen.get_height()
        self.fillerFont = pygame.font.Font(None, 24)
        self.gameBG = pygame.image.load("img/game_bg.png")
        self.botPanel = Object("img/ui/bottom_panel.png",512,self.windowY-64,1024,128)
        self.topLeft = Object("img/ui/top_left.png", 256,64,512,128)
        self.topLeftRect1 = pygame.Rect(0,0,128,128)
        self.topLeftRect2 = pygame.Rect(128,0,512-128,64)
        #Menu Panel
        self.menuPanel = Object("img/ui/menu.png",self.windowX/2, self.windowY/2, 212,274)
        self.saveButton = ClickableButton("img/buttons/save80x32.png",self.windowX - 96, self.windowY - 64,80,32)
        self.closeButton = ClickableButton("img/buttons/close.png", self.menuPanel.rect.right-13, self.menuPanel.rect.top+13,17,17)
        self.menuSaveButton = ClickableButton("img/buttons/save_game.png", self.menuPanel.x, self.menuPanel.rect.top+88,192,64)
        self.menuMenuButton = ClickableButton("img/buttons/quit_menu.png", self.menuPanel.x, self.menuPanel.rect.top+160,192,64)
        self.menuQuitButton = ClickableButton("img/buttons/quit_desktop.png", self.menuPanel.x, self.menuPanel.rect.top+232,192,64)
        #Quit Dialog Panel
        self.quitPanel = Object("img/ui/quit_menu.png",self.windowX/2, self.windowY/2, 212,274)
        self.saveButton = ClickableButton("img/buttons/save80x32.png",self.windowX - 96, self.windowY - 64,80,32)
        #Use the same close button
        self.saveQuitButton = ClickableButton("img/buttons/save_quit.png", self.menuPanel.x, self.menuPanel.rect.top+88,192,64)
        self.quitWOSaveButton = ClickableButton("img/buttons/quit_wo_save.png", self.menuPanel.x, self.menuPanel.rect.top+160,192,64)
        self.cancelButton = ClickableButton("img/buttons/cancel.png", self.menuPanel.x, self.menuPanel.rect.top+232,192,64)
        #More variables
        self.timeRatio = 60
        self.actionQueue = []
        #Load or New is important here
        if toLoad != None:
            self.loadGame(toLoad)
            self.saveName = toLoad
        else:
            self.newGame()
            self.saveName = "save.txt"
        #Guess what? It's a map, bitch
        self.startBlock = Node(0,0,0,0)
        self.endBlock = Node(0,0,0,0)
        self.map = Map(540,128,54,32)
        self.open = pygame.image.load("img/test/openIso.png")
        self.closed = pygame.image.load("img/test/closedIso.png")
        self.start = pygame.image.load("img/test/startIso.png")
        self.end = pygame.image.load("img/test/endIso.png")
        self.path = pygame.image.load("img/test/pathIso.png")
    
    #More Map code
    def swap(self,setSpecial,x):
        if x > 0: #change start
            self.startBlock.state = 0
            self.startBlock = setSpecial
        if x < 0: #change end
            self.endBlock.state = 0
            self.endBlock = setSpecial
    
    def newGame(self):
        #Set up the time
        self.startTime = datetime.datetime.now()
        self.currTime = self.startTime
        #Add test actions
        self.actionQueue.append( Action("testType", "Testing the Action System...", self.startTime, datetime.timedelta(minutes=10), None) )
        self.actionQueue.append( Action("testType", "Testing the Action System Again...", self.startTime, datetime.timedelta(minutes=20), None) )
        self.actionQueue.append( Action("testType", "Testing the Action System Yet Again...", self.startTime, datetime.timedelta(minutes=15), None) )
        self.actionQueue.append( Action("testType", "Testing the Action System Againnnnnn...", self.startTime, datetime.timedelta(minutes=30), None) )
    
    def loadGame(self, toLoad):
        #print "Loading game from %s..."%toLoad
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
        #print "Load complete!"
        
    def saveGame(self, saveDest):
        #print "Saving game to %s..."%saveDest
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
        #print "Save complete!"
    
    def mouseCollideWithUI(self, pt):
        return self.botPanel.rect.collidepoint(pt) or self.topLeftRect1.collidepoint(pt) or self.topLeftRect2.collidepoint(pt)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.toggle_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle_menu()
                if event.key == pygame.K_F5:
                    self.saveGame(self.saveName)
            #Mouse Events
            elif self.state == Game.NORMAL and(event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION):
                toSave = self.saveButton.mouse_event(event)
                if toSave:
                    self.saveGame(self.saveName)
                    self.toggle_menu()
            #Dialog Menu
            elif self.state == Game.POP_UP_MENU and(event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION):
                toClose = self.closeButton.mouse_event(event)
                if toClose:
                    self.toggle_menu()
                #Save
                toSave = self.menuSaveButton.mouse_event(event)
                if toSave:
                    self.saveGame(self.saveName)
                #Main Menu
                toMenu = self.menuMenuButton.mouse_event(event)
                if toMenu:
                    self.quitState = Game.QUIT_TO_MENU
                    self.state = Game.POP_UP_QUIT
                #Quit Game
                toQuit = self.menuQuitButton.mouse_event(event)
                if toQuit:
                    self.quitState = Game.QUIT_GAME
                    self.state = Game.POP_UP_QUIT
            #Quit Dialog
            elif self.state == Game.POP_UP_QUIT and(event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION):
                toClose = self.closeButton.mouse_event(event)
                toCancel = self.cancelButton.mouse_event(event)
                if toClose or toCancel:
                    self.toggle_menu()
                #Save & Quit
                toSave = self.saveQuitButton.mouse_event(event)
                if toSave:
                    self.saveGame(self.saveName)
                    self.state = self.quitState
                #Quit w/o Save
                toQuit = self.quitWOSaveButton.mouse_event(event)
                if toQuit:
                    self.state = self.quitState
            #Map stuff (from test.py)
            if self.state == Game.NORMAL and not (event.type == pygame.MOUSEBUTTONDOWN and self.mouseCollideWithUI(event.pos)):
                self.map_stuff(event)
    
    def toggle_menu(self):
        """Activates a menu pop-up for saving/quitting"""
        #If the pop up is already on, deactivate
        if self.state == Game.POP_UP_MENU or self.state == Game.POP_UP_QUIT:
            self.state = Game.NORMAL
        else:
            self.state = Game.POP_UP_MENU
    
    def map_stuff(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                #print "("+repr(event.pos[0])+","+repr(event.pos[1])+")"
                yPosition = int(floor((tan(radians(30)) * event.pos[0] + event.pos[1] + 16)/32))#Find position on y axis
                xPosition = -1 *int(floor((tan(radians(-30)) * event.pos[0] + event.pos[1] + 16)/32))#Find position on x axis
                print "Square: ("+repr(xPosition)+","+repr(yPosition)+")"
                #print len(self.map.grid)
                #print len(self.map.grid[0])
                x = xPosition
                y = yPosition
                self.map.grid[x][y-1].toggle(1)
                """
                if self.startBlock.x == self.map.grid[x][y].x and self.startBlock.y == self.map.grid[x][y].y:
                    self.startBlock = Node(0,0,0,0)
                if self.endBlock.x == self.map.grid[x][y].x and self.endBlock.y == self.map.grid[x][y].y:
                    self.endBlock = Node(0,0,0,0)
                if self.map.grid[x][y].state == 2:
                    self.swap(self.map.grid[x][y],1)
                if self.map.grid[x][y].state ==3:
                    self.swap(self.map.grid[x][y],-1)
                """
            if mouse[2]:
                x = xPosition
                y = yPosition
                self.map.grid[x][y].toggle(-1)
                if self.startBlock.x == self.map.grid[x][y].x and self.startBlock.y == self.map.grid[x][y].y:
                    self.startBlock = Node(0,0,0,0)
                if self.endBlock.x == self.map.grid[x][y].x and self.endBlock.y == self.map.grid[x][y].y:
                    self.endBlock = Node(0,0,0,0)
                if self.map.grid[x][y].state == 2:
                    self.swap(self.map.grid[x][y],1)
                if self.map.grid[x][y].state ==3:
                    self.swap(self.map.grid[x][y],-1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                path = AStar(self.map,self.startBlock,self.endBlock)
                for node in path.pathList:
                    node.state = 4
        
    def update(self, msPassed):
        #Do something with the time:
        timeDiff = datetime.timedelta(microseconds = self.timeRatio * msPassed * 1000)
        self.currTime = self.currTime + timeDiff
        #Check if any actions have finished
        for act in self.actionQueue:
            if act.isDone(self.currTime):
                self.actionQueue.remove(act)
    
    def draw(self):
        self.screen.blit(self.gameBG, pygame.Rect(0, 0, self.windowX, self.windowY))
        #Whattup, it's a map!
        for x in self.map.grid:
            for y in x:
                if y.state ==0:
                    self.screen.blit(self.open,y.rect)
                elif y.state == 1:
                    self.screen.blit(self.closed,y.rect)
                elif y.state ==2 :
                    self.screen.blit(self.start,y.rect)
                elif y.state == 3:
                    self.screen.blit(self.end,y.rect)
                elif y.state == 4:
                    self.screen.blit(self.path,y.rect)
        #UI
        self.botPanel.draw(self.screen)
        self.topLeft.draw(self.screen)
        self.saveButton.draw(self.screen)
        #Some code to display the time and date
        timeStr = self.getTimeStr(self.currTime)
        timeText1 = self.fillerFont.render(timeStr, 1, (0, 0, 0))
        timeText2 = self.fillerFont.render("%i/%i/%i"%(self.currTime.month, self.currTime.day, self.currTime.year), 1, (0, 0, 0))
        timeRect1 = timeText1.get_rect()
        timeRect2 = timeText2.get_rect()
        timeRect1.center = (32, self.windowY - 96)
        timeRect2.center = (128, self.windowY - 96)
        self.screen.blit(timeText1, timeRect1)
        self.screen.blit(timeText2, timeRect2)
        #A quick display for the actions we have (active ones only)
        counter = 0
        for index, act in enumerate(self.actionQueue):
            if counter >= 3:
                break
            if act.isStarted(self.currTime) == False:
                continue
            actStr = "%s : %s to go"%(act.desc, self.getDeltaStr(act.timeRemaining(self.currTime)))
            txtSurf = self.fillerFont.render(actStr, 1, (0, 0, 0))
            txtRect = txtSurf.get_rect()
            txtRect.center = (512, self.windowY - 96 + 32*index)
            self.screen.blit(txtSurf, txtRect)
            counter += 1
        #Pop-Up Menu
        if self.state == Game.POP_UP_MENU:
            #draw some menu stuff
            self.menuPanel.draw(self.screen)
            self.closeButton.draw(self.screen)
            self.menuSaveButton.draw(self.screen)
            self.menuMenuButton.draw(self.screen)
            self.menuQuitButton.draw(self.screen)
        #Quit Dialog
        if self.state == Game.POP_UP_QUIT:
            #draw some menu stuff
            self.quitPanel.draw(self.screen)
            self.closeButton.draw(self.screen)
            self.saveQuitButton.draw(self.screen)
            self.quitWOSaveButton.draw(self.screen)
            self.cancelButton.draw(self.screen)
    
    #Copied from main.py D:
    def exit_game(self):
        """Exits the game completely"""
        self.state = Game.QUIT_GAME
    
    #Here Lie the Helper Functions:
    def getTimeStr(self, aTime):
        leStr = ""
        hours = aTime.hour
        if hours < 10:
            leStr += "0%i"%hours
        else:
            leStr += "%i"%hours
        leStr += ":"
        mins = aTime.minute
        if mins < 10:
            leStr += "0%i"%mins
        else:
            leStr += "%i"%mins
        return leStr
        
    def getDeltaStr(self, dt):
        leStr = ""
        if dt.days > 0:
            leStr += "%i days,"%dt.days
        if dt.seconds/3600 > 0:
            leStr += "%i:"%(dt.seconds/3600)
        else:
            leStr += "0:"
        if dt.seconds/60 >= 10:
            leStr += "%i"%(dt.seconds/60)
        elif dt.seconds/60 > 0:
            leStr += "0%i"%(dt.seconds/60)
        else:
            leStr += "00"
        return leStr
    
    def textToDateTime(self, text): #For loading datetimes
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
