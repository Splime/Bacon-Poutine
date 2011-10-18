#main.py: A simple driver class for getting the basic setup started, menus, etc

import pygame
import sys

class Main():
    """Driver Class/Main Menu"""
    
    #Possible screens we're at:
    NONE = 0
    MAIN_MENU = 1
    IN_GAME = 2
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
        pygame.mouse.set_visible(True)
        #Main Menu Stuff
        self.menuBG = pygame.image.load("img/menu_bg.png").convert()
        self.playButtonImg = pygame.image.load("img/buttons/play.png").convert()
        self.playButtonRect = self.playButtonImg.get_rect()
        self.playButtonRect.center = (self.windowX/2, self.windowY/2)
    
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
            #TODO
            
    def update(self):
        """Updates the menu every frame"""
        pass
        
    def draw(self):
        """Deals with drawing the menu stuff every frame"""
        self.screen.blit(self.menuBG, pygame.Rect(0, 0, self.windowX, self.windowY))
        #Buttons
        self.screen.blit(self.playButtonImg, self.playButtonRect)
    
    def exit_game(self):
        """Exits the game completely"""
        pygame.quit()
        sys.exit()
        
#MAIN CODEBLOCK STARTS HERE
mainMenu = Main()
mainMenu.run()