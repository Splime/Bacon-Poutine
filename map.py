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
		self.staticH = 0
		self.staticW = 0
		self.tempH = 0
		self.tempW = 0
		self.columns = int(self.mapHeight/self.nodeHeight)
		print "Generating map"
		for x in range(0,3):
			temp = []
			while self.tempH < self.mapHeight and self.tempW < self.mapWidth:
				tempNode = Node(self.tempW,self.tempH,54,32)
				temp.append(tempNode)
				tempNode = Node(self.tempW+27,self.tempH+16,54,32)
				temp.append(tempNode)
				self.tempH +=self.nodeHeight
				self.tempW += self.nodeWidth
			self.grid.append(temp)
			self.staticW += 27
			self.staticH -= 16
			self.tempW = self.staticW
			self.tempH = self.staticH
			
			"""
				tempNode = Node(self.w,self.h,54,32)
				temp.append(tempNode)
				tempNode = Node(self.w+27,self.h+16,54,32)
				temp.append(tempNode)
				self.h +=self.nodeHeight
				self.w += self.nodeWidth
			self.grid.append(temp)
			self.w = 27
			self.h = -16
			"""
			"""
			nodeRow = []
			for j in range(0,self.rows):
				tempNode = Node(i*self.nodeWidth,j*self.nodeHeight,self.nodeWidth,self.nodeHeight)
				nodeRow.append(tempNode)
			self.grid.append(nodeRow)
			nodeRow = []
			for j in range(0,self.rows):
				tempNode = Node(i*self.nodeWidth+self.nodeWidth/2,j*self.nodeHeight+self.nodeHeight/2,self.nodeWidth,self.nodeHeight)
				nodeRow.append(tempNode)
			self.grid.append(nodeRow)
			
			================
					#while len(self.grid) == 0 or (self.grid[-1]) != 1:
			temp = []
			while self.tempH < self.mapHeight and self.tempW < self.mapWidth:
				tempNode = Node(self.tempW,self.tempH,54,32)
				temp.append(tempNode)
				tempNode = Node(self.tempW+27,self.tempH+16,54,32)
				temp.append(tempNode)
				self.tempH +=self.nodeHeight
				self.tempW += self.nodeWidth
			self.grid.append(temp)
			self.staticW += 27
			self.staticH -= -16
			self.tempW = self.staticW
			self.tempH = self.staticH
			
			
			"""
		
		print "Map generated"