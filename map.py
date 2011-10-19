#Map class

import pygame
from grid import Grid

class Map:
	width = 0
	x = 0
	y = 0
	height = 0
	grid = []
	gridSize = 0
	
	def __init__(self,width,height,gridSize):
		self.gridSize = gridSize
		self.width = width
		self.height = height
		self.tempH = height
		self.tempW = width
		self.t1 = 0
		self.t2 = 0
		print "Generating map"
		while self.tempW >= self.gridSize:
			self.tempG = []
			while self.tempH >= self.gridSize:
				tempSquare = Grid(self.t1,self.t2,self.gridSize,True)
				#print "x,y: ("+ repr(self.tempW)+","+repr(self.tempH)+")"
				self.tempG.append(tempSquare)
				self.tempH -= self.gridSize
				self.t2 += self.gridSize
			self.tempW -= self.gridSize
			self.t1 += self.gridSize
			self.t2 = 0
			self.grid.append(self.tempG)
			self.tempH = height
			del self.tempG
		print "Map generated"