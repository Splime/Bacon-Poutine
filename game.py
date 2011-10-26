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
from chapMap import CMap
from player import Player

class Game():

    QUIT_GAME = -2
    QUIT_TO_MENU = -1
    NORMAL = 0 #All other modes count as paused!
    POP_UP_MENU = 1
    POP_UP_QUIT = 2
    
    def __init__(self, scr, toLoad):
        self.state = Game.NORMAL
        self.quitState = Game.NORMAL
        self.screen = scr
        self.windowX = self.screen.get_width()
        self.windowY = self.screen.get_height()
        self.fillerFont = pygame.font.Font(None, 24)
        self.filler16 = pygame.font.Font(None, 16)
        self.gameBG = pygame.image.load("img/game_bg.png")
        self.gameBGTile = pygame.image.load("img/game_bg_tile.png")
        self.gameBGTileRect = self.gameBGTile.get_rect()
        self.botPanel = Object("img/ui/bottom_panel.png",512,self.windowY-64,1024,128)
        self.topLeft = Object("img/ui/top_left.png", 256,64,512,128)
        self.topLeftRect1 = pygame.Rect(0,0,128,128)
        self.topLeftRect2 = pygame.Rect(128,0,512-128,64)
        #Some UI Buttons
        self.saveButton = ClickableButton("img/buttons/save80x32.png",self.windowX - 96, self.windowY - 64,80,32)
        self.moveButton = ClickableButton("img/buttons/move_here80x32.png",352, self.windowY - 32,80,32)
        #Menu Panel
        self.menuPanel = Object("img/ui/menu.png",self.windowX/2, self.windowY/2, 212,274)
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
        #Guess what? It's a map, bitch
        self.cmapRect = pygame.Rect(0,0,480,480)
        self.cmapRect.center = (self.windowX/2, self.windowY/2-64)
        self.cmap = CMap(15,15,self.cmapRect)
        #Load or New is important here
        if toLoad != None:
            self.loadGame(toLoad)
            self.saveName = toLoad
        else:
            self.newGame()
            self.saveName = "save.txt"
    
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
        self.player = Player("Chap", (0,1), self.cmap)
        #Add test actions
        #self.actionQueue.append( Action("testType", "Poopalooping", self.startTime, datetime.timedelta(minutes=30), None) )
        #self.actionQueue.append( Action("testType", "Infecting Zombies", self.startTime, datetime.timedelta(hours=4), None) )
        #self.actionQueue.append( Action("testType", "Reticulating Splines", self.startTime, datetime.timedelta(days=7), None) )
    
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
        self.currTime = prevGameTime #+ gameTimeDiff #Disabling time passing while offline, gameplay decision
        #Now load up the player!
        playerLine = f.readline().rstrip().split('^')
        self.player = Player(playerLine[0], (int(playerLine[1]),int(playerLine[2])), self.cmap)
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
                self.player.action = anAction
            aLine = f.readline()
        #At this point, aLine == "endActions\n"

        #End File Stuff
        f.close()
        #print "Load complete!"
        
    def saveGame(self, saveDest):
        #print "Saving game to %s..."%saveDest
        f = open(saveDest, 'w')
        #Time stuff
        f.write("gametime,%s\n"%self.dateTimeToText(self.currTime))
        irlTime = datetime.datetime.now()
        f.write("savetime,%s\n"%self.dateTimeToText(irlTime))
        #Player
        f.write("%s^%i^%i\n"%(self.player.name, self.player.pos[0], self.player.pos[1]))
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
                self.state = Game.POP_UP_QUIT
                self.quitState = Game.QUIT_GAME
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
                #Deal with the movement button
                if self.cmap.selectedPos != None:
                    toMove = self.moveButton.mouse_event(event)
                    if toMove:
                        self.move_player_to_selected()
            #Dialog Menu
            elif self.state == Game.POP_UP_MENU and(event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION):
                toClose = self.closeButton.mouse_event(event)
                if toClose:
                    self.toggle_menu()
                #Save
                toSave = self.menuSaveButton.mouse_event(event)
                if toSave:
                    self.saveGame(self.saveName)
                    self.toggle_menu()
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
            if self.state == Game.NORMAL and not ((event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION) and self.mouseCollideWithUI(event.pos)):
                self.cmap.handle_event(event)
    
    def toggle_menu(self):
        """Activates a menu pop-up for saving/quitting"""
        #If the pop up is already on, deactivate
        if self.state == Game.POP_UP_MENU or self.state == Game.POP_UP_QUIT:
            self.state = Game.NORMAL
        else:
            self.state = Game.POP_UP_MENU
    
    def move_player_to_selected(self):
        """Moves the player to the currently selected grid square"""
        #Check for no selection
        if self.cmap.selectedPos == None:
            print "Ruh Roh!"
            return
        #Create a movement action for this movement
        someParams = [[self.player.pos, self.cmap.selectedPos], "walking"] #TODO: Make an actual path!
        moveAct = Action("movement", "Moving to (%i, %i)"%(self.cmap.selectedPos[0], self.cmap.selectedPos[1]), self.currTime, None, someParams)
        #Remove any previous movement actions
        for act in self.actionQueue:
            if act.type == "movement":
                self.actionQueue.remove(act)
        self.actionQueue.append(moveAct)
        self.player.action = moveAct
        
    def update(self, msPassed):
        #Do something with the time (only if unpaused):
        if self.state == Game.NORMAL:
            timeDiff = datetime.timedelta(microseconds = self.timeRatio * msPassed * 1000)
            self.currTime = self.currTime + timeDiff
            #Check if any actions have finished
            for act in self.actionQueue:
                if act.isDone(self.currTime):
                    self.actionQueue.remove(act)
        #Map stuff
        self.cmap.update(msPassed)
        #Player
        self.player.update(msPassed)
    
    def draw(self):
        #self.screen.blit(self.gameBG, pygame.Rect(0, 0, self.windowX, self.windowY))
        for x in range(self.windowX/self.gameBGTileRect.width + self.gameBGTileRect.width):
            for y in range(self.windowY/self.gameBGTileRect.height + self.gameBGTileRect.height):
                self.screen.blit(self.gameBGTile, pygame.Rect(x*self.gameBGTileRect.width, y*self.gameBGTileRect.height, self.gameBGTileRect.width, self.gameBGTileRect.height))
        #Whattup, it's a map!
        self.cmap.draw(self.screen)
        #Player
        self.player.draw(self.screen)
        #UI
        self.botPanel.draw(self.screen)
        self.topLeft.draw(self.screen)
        self.saveButton.draw(self.screen)
        if self.cmap.selectedPos != None:
            self.moveButton.draw(self.screen)
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
            txtSurf = self.filler16.render(actStr, 0, (0, 0, 0))
            txtRect = txtSurf.get_rect()
            txtRect.center = (self.windowX - 352, self.windowY - 96 + 32*counter)
            self.screen.blit(txtSurf, txtRect)
            counter += 1
        #Display Player Name
        nameStr = self.fillerFont.render(self.player.name, 1, (0, 0, 0))
        nameRect = nameStr.get_rect()
        nameRect.center = (64,64)
        self.screen.blit(nameStr, nameRect)
        #Display info about the selected tile
        if self.cmap.selectedPos == None:
            selStr = "No Tile Selected! :("
        else:
            selStr = "(%i, %i) Selected"%(self.cmap.selectedPos[0], self.cmap.selectedPos[1])
        selSurf = self.fillerFont.render(selStr, 1, (0, 0, 0))
        selRect = selSurf.get_rect()
        selRect.center = (352, self.windowY - 96)
        self.screen.blit(selSurf, selRect)
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
            leStr += "%i day(s), "%dt.days
        #print "dt.seconds/3600 = " + str(dt.seconds/3600) + " dt.seconds/60 = " + str(dt.seconds/60)
        if dt.seconds/3600 > 0:
            leStr += "%i:"%(dt.seconds/3600)
        else:
            leStr += "0:"
        if (dt.seconds/60)%60 >= 10:
            leStr += "%i"%((dt.seconds/60)%60)
        elif (dt.seconds/60)%60 > 0:
            leStr += "0%i"%((dt.seconds/60)%60)
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
        #print "dlt.days = %i, dlt.seconds = %i"%(dlt.days, dlt.seconds)
        return "%i,%i,%i"%(dlt.days, dlt.seconds, dlt.microseconds)
    
    def actionToText(self, act): #For saving actions
        aStr = "%s^%s^actStart,%s^actDuration,%s^"%(act.type, act.desc, self.dateTimeToText(act.startTime), self.deltaToText(act.duration))
        #Now deal with params
        if act.type == "testType":
            aStr += "None"
        elif act.type == "movement":
            pathStr = ""
            for tile in act.path:
                pathStr += "*%i %i"%(tile[0], tile[1])
            pathStr+="*"
            aStr += "%s&%s"%(pathStr, act.method)
        elif act.type == "scavenge":
            aStr += "None"
        elif act.type == "fortify":
            aStr += "None"
        elif act.type == "sweep":
            aStr += "None"
        return aStr+"\n"
        
    def textToAction(self, text): #For loading actions
        aList = text.rstrip().split('^')
        #Before making our Action, deal with params
        paramarams = None
        if aList[0] == "testType":
            pass
        elif aList[0] == "movement":
            paramarams = []
            paramList = aList[4].split('&')
            #First, append the path
            thePathList = paramList[0].split('*')
            thePath = []
            for tile in thePathList:
                if tile != "":
                    coords = tile.split(' ')
                    thePath.append((int(coords[0]), int(coords[1])))
            paramarams.append(thePath)
            #Then, append the method
            paramarams.append(paramList[1])
        elif aList[0] == "scavenge":
            pass
        elif aList[0] == "fortify":
            pass
        elif aList[0] == "sweep":
            pass
        return Action(aList[0], aList[1], self.textToDateTime(aList[2]), self.textToDelta(aList[3]), paramarams)
