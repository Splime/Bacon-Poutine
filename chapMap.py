#chapMap.py: A file for a (temporary?) map, used to hold different buildings

import pygame
from gridIcon import GridIcon

class CMap:
    
    #Constants for isometrification
    HORIZ_SHIFT = 60
    VERT_SHIFT = 30

    def __init__(self, width, height, targetRect):
        self.grid = []
        for i in range(height):
            aRow = []
            for j in range(width):
                aRow.append(None)
            self.grid.append(aRow)
        self.tileImg = pygame.image.load("img/map/120x61iso.png")
        self.tileX = self.tileImg.get_rect().width/2
        self.tileY = self.tileImg.get_rect().height/3 - 1
        self.targetRect = targetRect
        #Grid UI: How the player interacts with this map
        self.gridUI = []
        for i in range(height):
            aRow = []
            for j in range(width):
                thePos = self.calc_display(j, i)
                aRow.append(GridIcon("img/map/120x61iso.png", thePos[0], thePos[1], self.tileX, self.tileY))
            self.gridUI.append(aRow)
        self.selection = None
        self.selectedPos = None
        self.lastHighlight = None
    
    #A function to easily find what's at a specific location
    def get(self, x, y):
        return self.grid[y][x]
    
    def update(self, msPassed):
        pass
        
    def handle_event(self, event):
        newSelection = False
        newTile = None
        #Count down from -15,-15 to 0,0
        for i in range(len(self.gridUI)-1, -1, -1):
            aRow = self.gridUI[i]
            for j in range(len(aRow)-1, -1, -1):
                tile = aRow[j]
                result = tile.mouse_event(event)
                #If a tile gets selected, make sure we unselect the last one
                if tile.state != GridIcon.NORMAL:
                    self.lastHighlight = tile
                if result:
                    newSelection = True
                    newTile = tile
                    self.selectedPos = (j, i)
                    break
            if newSelection:
                break
        #Now unselect all but selected
        if newSelection:
            #print "New Selection!"
            if self.selection != None:
                #print "Removing old selection"
                self.selection.selected = GridIcon.UNSELECTED
            self.selection = newTile
        
    def draw(self, screen):
        for i, row in enumerate(self.gridUI):
            for j, tile in enumerate(row):
                tile.draw(screen)
    
    def path_find(self, pos1, pos2):
        thePath = []
        #Now find a path from pos1 to pos2!
        #Quick fix: go across, then down, ignore any obstacles
        horiz = 1
        if pos1[0] > pos2[0]:
            horiz = -1
        for i in range(pos1[0], pos2[0], horiz):
            thePath.append((i, pos1[1]))
        vert = 1
        if pos1[1] > pos2[1]:
            vert = -1
        for j in range(pos1[1], pos2[1], vert):
            thePath.append((pos2[0], j))
        thePath.append(pos2)
        return thePath
    
    #Helper Function, calculates display position based on x and y
    def calc_display(self, x, y):
        base_pos = (self.targetRect.width/2 + self.targetRect.left, CMap.VERT_SHIFT + self.targetRect.top) #Position for 0,0
        return (base_pos[0] + x*CMap.HORIZ_SHIFT - y*CMap.HORIZ_SHIFT, base_pos[1] + x*CMap.VERT_SHIFT + y*CMap.VERT_SHIFT)
        