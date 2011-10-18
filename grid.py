#Grid class

import pygame

class Grid:
	x = 0
	y = 0
	rect = 0
	dimension = 0
	name = ""
	passable = False
	
	def __init__(self,x,y,dimension,passable):
		self.rect = (x,y,dimension,dimension)
		self.x = x
		self.y = y
		self.dimension = dimension
		self.passable = passable