#Node class

import pygame

class Node:
	x = 0
	y = 0
	rect = 0
	dimension = 0
	name = ""
	passable = False
	state = 0
	G = 0
	F = 0
	H = 0
	parent = [0,0]
	
	#States 0 = passable, 1 = impassable, 2 = start, 3 = end
	
	def __init__(self,x,y,dimension,passable):
		self.rect = (x,y,dimension,dimension)
		self.x = x
		self.y = y
		self.dimension = dimension
		self.passable = passable
	
	def toggle(self,x):
		if x > 0:
			self.state +=1
			if self.state == 4:
				self.state = 0
		if x < 0:
			self.state -=1
			if self.state == -1:
				self.state = 3