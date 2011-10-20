#A.py
from grid import Node
from map import Map
from math import fabs

class AStar():
	openList = []
	closedList = []
	pathList = []
	def __init__(self,map,start,end):
		self.map = map
		self.startNode = start
		self.endNode = end
		#self.openList.append(self.startNode)
		self.cols = len(map.grid[0])
		self.rows = len(map.grid)
		self.find_path()
		
	def find_path(self):
		self.pathList = []
		self.openList = []
		self.closedList = []
		self.startNode.G = 0
		self.startNode.H = self.manhattan(self.startNode)
		self.startNode.F = self.startNode.G + self.startNode.H
		if self.adjacent(self.startNode):
			pass
		else:
			print "No valid path from start(" + repr(self.startNode.x/32) +","+ repr(self.startNode.y/32)+")"
			return 0
		#self.openList.remove(self.startNode)
		self.closedList.append(self.startNode)
		while(self.openList.count(self.endNode) == 0):
			minF = 999999999
			self.minNode = 0
			for node in self.openList:#Find node with smallest F
				if node.F < minF:
					minF = node.F
					self.minNode = node
			self.closedList.append(self.minNode)
			self.openList.remove(self.minNode)
			while not self.adjacent(self.minNode):
				if len(self.openList) == 0:
					print "No valid path from start(" + repr(self.startNode.x/32) +","+ repr(self.startNode.y/32)+")"
					return 0
				else:
					minF = 999999999
					self.minNode = 0
					for node in self.openList:#Find node with smallest F
						if node.F < minF:
							minF = node.F
							self.minNode = node
					self.closedList.append(self.minNode)
					self.openList.remove(self.minNode)
		
		#End of loop
		tempNode = self.map.grid[self.endNode.parent[0]][self.endNode.parent[1]]
		while tempNode != self.startNode:
			self.pathList.append(tempNode)
			tempNode = self.map.grid[tempNode.parent[0]][tempNode.parent[1]]
		self.pathList.reverse()
		
	def manhattan(self,node):
		return (abs(self.endNode.x-node.x)/32 + abs(self.endNode.y-node.y)/32)*10
		
	def adjacent(self,node):
		boolean = False
		x = int(node.x/32)
		y = int(node.y/32)
		if x-1 >=0: #Take care of x-1
			if y-1 >= 0: #Take care of x-1,y-1
				if self.map.grid[x-1][y-1].state != 1: #If a passble block
					if self.closedList.count(self.map.grid[x-1][y-1]) == 0: #If not in closedList
						if self.openList.count(self.map.grid[x-1][y-1]) !=0:#If in openlist
							if self.map.grid[x][y].G + 14 < self.map.grid[x-1][y-1].G:#update existing nodes
								self.map.grid[x-1][y-1].G + 14
								self.map.grid[x-1][y-1].parent = self.map.grid[x][y]
						else:#New node found
							self.openList.append(self.map.grid[x-1][y-1])
							self.map.grid[x-1][y-1].G = self.map.grid[x][y].G + 14
							self.map.grid[x-1][y-1].H = self.manhattan(self.map.grid[x-1][y-1])
							self.map.grid[x-1][y-1].parent = [x,y]
						self.map.grid[x-1][y-1].F = self.map.grid[x-1][y-1].G + self.map.grid[x-1][y-1].H
						boolean = True
			if y+1 <= 19: #Take care of x-1,y+1
				if self.map.grid[x-1][y+1].state != 1: #If a passble block
					if self.closedList.count(self.map.grid[x-1][y+1]) == 0: #If not in closedList
						if self.openList.count(self.map.grid[x-1][y+1]) !=0:#If in openlist
							if self.map.grid[x][y].G + 14 < self.map.grid[x-1][y+1].G:#update existing nodes
								self.map.grid[x-1][y+1].G + 14
								self.map.grid[x-1][y+1].parent = self.map.grid[x][y]
						else:#New node found
							self.openList.append(self.map.grid[x-1][y+1])
							self.map.grid[x-1][y+1].G = self.map.grid[x][y].G + 14
							self.map.grid[x-1][y+1].H = self.manhattan(self.map.grid[x-1][y+1])
							self.map.grid[x-1][y+1].parent = [x,y]
						self.map.grid[x-1][y+1].F = self.map.grid[x-1][y+1].G + self.map.grid[x-1][y+1].H
						boolean = True
			if self.map.grid[x-1][y].state != 1: #Take care of y
					if self.closedList.count(self.map.grid[x-1][y]) == 0: #If not in closedList
						if self.openList.count(self.map.grid[x-1][y]) !=0:#If in openlist
							if self.map.grid[x][y].G + 14 < self.map.grid[x-1][y].G:#update existing nodes
								self.map.grid[x-1][y].G + 14
								self.map.grid[x-1][y].parent = self.map.grid[x][y]
						else:#New node found
							self.openList.append(self.map.grid[x-1][y])
							self.map.grid[x-1][y].G = self.map.grid[x][y].G + 14
							self.map.grid[x-1][y].H = self.manhattan(self.map.grid[x-1][y])
							self.map.grid[x-1][y].parent = [x,y]
						self.map.grid[x-1][y].F = self.map.grid[x-1][y].G + self.map.grid[x-1][y].H
						boolean = True
		if x+1 <= 19: #Take care of x+1
			if y-1 >= 0: #Take care of x+1,y-1
				if self.map.grid[x+1][y-1].state != 1: #If a passble block
					if self.closedList.count(self.map.grid[x+1][y-1]) == 0: #If not in closedList
						if self.openList.count(self.map.grid[x+1][y-1]) !=0:#If in openlist
							if self.map.grid[x][y].G + 14 < self.map.grid[x+1][y-1].G:#update existing nodes
								self.map.grid[x+1][y-1].G + 14
								self.map.grid[x+1][y-1].parent = self.map.grid[x][y]
						else:#New node found
							self.openList.append(self.map.grid[x+1][y-1])
							self.map.grid[x+1][y-1].G = self.map.grid[x][y].G + 14
							self.map.grid[x+1][y-1].H = self.manhattan(self.map.grid[x+1][y-1])
							self.map.grid[x+1][y-1].parent = [x,y]
						self.map.grid[x+1][y-1].F = self.map.grid[x+1][y-1].G + self.map.grid[x+1][y-1].H
						boolean = True
			if y+1 <= 19: #Take care of x+1,y+1
				if self.map.grid[x+1][y+1].state != 1: #If a passble block
					if self.closedList.count(self.map.grid[x+1][y+1]) == 0: #If not in closedList
						if self.openList.count(self.map.grid[x+1][y+1]) !=0:#If in openlist
							if self.map.grid[x][y].G + 14 < self.map.grid[x+1][y+1].G:#update existing nodes
								self.map.grid[x+1][y+1].G + 14
								self.map.grid[x+1][y+1].parent = self.map.grid[x][y]
						else:#New node found
							self.openList.append(self.map.grid[x+1][y+1])
							self.map.grid[x+1][y+1].G = self.map.grid[x][y].G + 14
							self.map.grid[x+1][y+1].H = self.manhattan(self.map.grid[x+1][y+1])
							self.map.grid[x+1][y+1].parent = [x,y]
						self.map.grid[x+1][y+1].F = self.map.grid[x+1][y+1].G + self.map.grid[x+1][y+1].H
						boolean = True
			if self.map.grid[x+1][y].state != 1: #Take care of y
					if self.closedList.count(self.map.grid[x+1][y]) == 0: #If not in closedList
						if self.openList.count(self.map.grid[x+1][y]) !=0:#If in openlist
							if self.map.grid[x][y].G + 14 < self.map.grid[x+1][y].G:#update existing nodes
								self.map.grid[x+1][y].G + 14
								self.map.grid[x+1][y].parent = self.map.grid[x][y]
						else:#New node found
							self.openList.append(self.map.grid[x+1][y])
							self.map.grid[x+1][y].G = self.map.grid[x][y].G + 14
							self.map.grid[x+1][y].H = self.manhattan(self.map.grid[x+1][y])
							self.map.grid[x+1][y].parent = [x,y]
						self.map.grid[x+1][y].F = self.map.grid[x+1][y].G + self.map.grid[x+1][y].H
						boolean = True
		if self.map.grid[x][y-1].state != 1: #If a passble block
					if self.closedList.count(self.map.grid[x][y-1]) == 0: #If not in closedList
						if self.openList.count(self.map.grid[x][y-1]) !=0:#If in openlist
							if self.map.grid[x][y].G + 14 < self.map.grid[x][y-1].G:#update existing nodes
								self.map.grid[x][y-1].G + 14
								self.map.grid[x][y-1].parent = self.map.grid[x][y]
						else:#New node found
							self.openList.append(self.map.grid[x][y-1])
							self.map.grid[x][y-1].G = self.map.grid[x][y].G + 14
							self.map.grid[x][y-1].H = self.manhattan(self.map.grid[x][y-1])
							self.map.grid[x][y-1].parent = [x,y]
						self.map.grid[x][y-1].F = self.map.grid[x][y-1].G + self.map.grid[x][y-1].H
						boolean = True
		if self.map.grid[x][y+1].state != 1: #If a passble block
					if self.closedList.count(self.map.grid[x][y+1]) == 0: #If not in closedList
						if self.openList.count(self.map.grid[x][y+1]) !=0:#If in openlist
							if self.map.grid[x][y].G + 14 < self.map.grid[x][y+1].G:#update existing nodes
								self.map.grid[x][y+1].G + 14
								self.map.grid[x][y+1].parent = self.map.grid[x][y]
						else:#New node found
							self.openList.append(self.map.grid[x][y+1])
							self.map.grid[x][y+1].G = self.map.grid[x][y].G + 14
							self.map.grid[x][y+1].H = self.manhattan(self.map.grid[x][y+1])
							self.map.grid[x][y+1].parent = [x,y]
						self.map.grid[x][y+1].F = self.map.grid[x][y+1].G + self.map.grid[x][y+1].H
						boolean = True
		return boolean