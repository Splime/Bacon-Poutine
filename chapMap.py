#chapMap.py: A file for a (temporary?) map, used to hold different buildings

import pygame

class CMap:

    def __init__(self, width, height):
        self.grid = []
        for i in range(height):
            aRow = []
            for j in range(width):
                aRow.append(None)
            self.grid.append(aRow)
        self.tileImg = pygame.image.load("img/map/32sq.png")
    
    #A function to easily find what's at a specific location
    def get(self, x, y):
        return self.grid[y][x]
    
    def update(self, msPassed):
        pass
        
    def handle_event(self, event):
        pass
        
    def draw(self, screen, targetRect):
        for i, row in enumerate(self.grid):
            for j, tile in enumerate(row):
                if tile == None:
                    screen.blit(self.tileImg, pygame.Rect(targetRect.left+j*32, targetRect.top+i*32, 32, 32))