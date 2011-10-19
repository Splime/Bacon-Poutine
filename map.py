#Map class

import pygame
from grid import Node

class Map:
	width = 0
	x = 0
	y = 0
	height = 0
	grid = []
	nodeSize = 0
	
	def __init__(self,width,height,nodeSize):
		self.nodeSize = nodeSize
		self.width = width
		self.height = height
		self.tempH = height
		self.tempW = width
		self.t1 = 0
		self.t2 = 0
		print "Generating map"
		while self.tempW >= self.nodeSize:
			self.tempG = []
			while self.tempH >= self.nodeSize:
				tempSquare = Node(self.t1,self.t2,self.nodeSize,True)
				#print "x,y: ("+ repr(self.tempW)+","+repr(self.tempH)+")"
				self.tempG.append(tempSquare)
				self.tempH -= self.nodeSize
				self.t2 += self.nodeSize
			self.tempW -= self.nodeSize
			self.t1 += self.nodeSize
			self.t2 = 0
			self.grid.append(self.tempG)
			self.tempH = height
			del self.tempG
		print "Map generated"