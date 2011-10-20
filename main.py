#main.py: A simple driver class for getting the basic setup started, menus, etc

import pygame
import sys
from introseq import IntroSeq
from game import Game
from object import Object
from clickablebutton import ClickableButton

class Main():
    """Driver Class/Main Menu"""
    
    #Possible screens we're at:
    NONE = 0
    MAIN_MENU = 1
    INTRO = 2
    IN_GAME = 3
    #Add more as we add them (though these screens may have subscreens)
    
    def __init__(self):
        """Setup the window, etc"""
        self.windowX = 1024
        self.windowY = 768
        self.windowName = "Bacon Poutine"
        self.state = Main.NONE
        pygame.init()
        self.clock = pygame.time.Clock()
        self.msPassed = 0
        #Get the screen going
        self.screen = pygame.display.set_mode((self.windowX, self.windowY))
        pygame.display.set_caption(self.windowName)
        self.iconImg = pygame.image.load("img/icon.png").convert_alpha()
        pygame.display.set_icon(self.iconImg)
        pygame.mouse.set_visible(True)
        #Main Menu Stuff
        self.dudeObj = Object("img/dude.png",200,200,64,128)
        self.newButtonObj = ClickableButton("img/buttons/new_game.png",self.windowX/2, self.windowY/2+200,192,64)
        self.loadButtonObj = ClickableButton("img/buttons/load_game.png",self.windowX/2, self.windowY/2+272,192,64)
        self.menuBG = pygame.image.load("img/menu_bg.png").convert()
        self.intro = None
        self.game = None
    
    def run(self):
        """Runs the game"""
        self.state = Main.MAIN_MENU
        self.clock.tick()
        while True:
            if self.state == Main.MAIN_MENU:
                #Do our menu stuff
                self.handle_events()
                self.update()
                self.draw()
                pygame.display.flip()
            elif self.state == Main.INTRO and self.intro != None:
                self.handle_events()
                self.intro.update(self.msPassed)
                self.intro.draw()
                pygame.display.flip()
                if self.intro.doneYet:
                    print "Intro Complete!"
                    self.state = Main.IN_GAME
                    self.game = Game(self.screen, None)
            elif self.state == Main.IN_GAME and self.game != None:
                self.game.handle_events()
                self.game.update(self.msPassed)
                self.game.draw()
                pygame.display.flip()
            else:
                #Quit!
                self.exit_game()
            #Tick the clock forward
            self.msPassed = self.clock.tick(60)
    
    def handle_events(self):
        """Handles all of the input (for main menu)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game() #If close button clicked in top right
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()
            #Mouse Events
            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                newGame = self.newButtonObj.mouse_event(event)
                if newGame:
                    self.state = Main.INTRO
                    self.intro = IntroSeq(self.screen)
                loadGame = self.loadButtonObj.mouse_event(event)
                if loadGame:
                    self.state = Main.IN_GAME
                    self.game = Game(self.screen, "save.txt")
            
    def update(self):
        """Updates the menu every frame"""
        pass
        
    def draw(self):
        """Deals with drawing the menu stuff every frame"""
        self.screen.blit(self.menuBG, pygame.Rect(0, 0, self.windowX, self.windowY))
        #Buttons
        self.newButtonObj.draw(self.screen)
        self.loadButtonObj.draw(self.screen)
        self.screen.blit(self.dudeObj.img,self.dudeObj.rect)
    
    def exit_game(self):
        """Exits the game completely"""
        pygame.quit()
        sys.exit()
        
#MAIN CODEBLOCK STARTS HERE
mainMenu = Main()
mainMenu.run()