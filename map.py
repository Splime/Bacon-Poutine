#Map class

import pygame
from grid import Node

class Map:
	width = 0
	x = 0
	y = 0
	height = 0
	grid = []
	
	def __init__(self,mapWidth,mapHeight,nodeWidth,nodeHeight):
		self.mapWidth = mapWidth
		self.mapHeight = mapHeight
		self.nodeWidth = nodeWidth
		self.nodeHeight = nodeHeight
		self.rows = int(self.mapWidth/self.nodeWidth)
		self.columns = int(self.mapHeight/self.nodeHeight)
		print "Generating map"
		for i in range(0,self.columns):
			nodeRow = []
			for j in range(0,self.rows):
				tempNode = Node(i*self.nodeWidth,j*self.nodeHeight,self.nodeWidth,self.nodeHeight)
				nodeRow.append(tempNode)
				tempNode = Node(i*self.nodeWidth+self.nodeWidth/2,j*self.nodeHeight+self.nodeHeight/2,self.nodeWidth,self.nodeHeight)
				nodeRow.append(tempNode)
			self.grid.append(nodeRow)
			
		"""
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
		"""