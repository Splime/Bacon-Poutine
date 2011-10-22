#Node class

import pygame

class Node:
    x = 0
    y = 0
    rect = 0
    width = 0
    height = 0
    name = ""
    state = 0
    G = 999999999
    F = 999999999
    H = 999999999
    parent = [0,0]
    
    #States 0 = passable, 1 = impassable, 2 = start, 3 = end 4 = path
    
    def __init__(self,x,y,width,height):
        self.rect = (x,y,width,height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def toggle(self,x):
        if x > 0:
            self.state +=1
            if self.state == 5:
                self.state = 0
        if x < 0:
            self.state -=1
            if self.state == -1:
                self.state = 4