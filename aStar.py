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
		if self.adjacent(self.startNode):
			pass
		else:
			print "No valid path (" + repr(startNode.x/32) +","+ repr(startNode.y/32)+")"
			return 0
		#self.openList.remove(self.startNode)
		self.closedList.append(self.startNode)
		while(self.openList.count(self.endNode) == 0):
			minF = self.openList[1].F
			minNode = self.openList[1]
			for node in self.openList:#Find node with smallest F
				if node.F < minF:
					minF = node.F
					minNode = node
			self.closedList.append(minNode)
			self.openList.remove(minNode)
			if self.adjacent(minNode):
				pass
			else:
				print "No valid path (" + repr(minNode.x/32) +","+ repr(minNode.y/32)+")"
				return 0
		
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
					if self.openList.count(self.map.grid[x-1][y-1]) ==0 and self.closedList.count(self.map.grid[x-1][y-1]) == 0: #If not in lists
						self.openList.append(self.map.grid[x-1][y-1])
						self.map.grid[x-1][y-1].G = self.map.grid[x][y].G + 14
						self.map.grid[x-1][y-1].H = self.manhattan(self.map.grid[x-1][y-1])
						self.map.grid[x-1][y-1].parent = [x,y]
						self.map.grid[x-1][y-1].F = self.map.grid[x-1][y-1].G + self.map.grid[x-1][y-1].H
						boolean = True
			if y+1 <= 19: #Take care of x-1,y+1
				if self.map.grid[x-1][y+1].state != 1: #If a passble block
					if self.openList.count(self.map.grid[x-1][y+1]) ==0 and self.closedList.count(self.map.grid[x-1][y+1]) == 0: #If not in lists
						self.openList.append(self.map.grid[x-1][y+1])
						self.map.grid[x-1][y+1].G = self.map.grid[x][y].G + 14
						self.map.grid[x-1][y+1].H = self.manhattan(self.map.grid[x-1][y+1])
						self.map.grid[x-1][y+1].parent = [x,y]
						self.map.grid[x-1][y+1].F = self.map.grid[x-1][y+1].G + self.map.grid[x-1][y+1].H
						boolean = True
			#Take care of y + 0
			if self.map.grid[x-1][y].state != 1: #If a passble block
					if self.openList.count(self.map.grid[x-1][y]) ==0 and self.closedList.count(self.map.grid[x-1][y]) == 0: #If not in lists
						self.openList.append(self.map.grid[x-1][y])
						self.map.grid[x-1][y].G = self.map.grid[x][y].G + 10
						self.map.grid[x-1][y].H = self.manhattan(self.map.grid[x-1][y])
						self.map.grid[x-1][y].parent = [x,y]
						self.map.grid[x-1][y].F = self.map.grid[x-1][y].G + self.map.grid[x-1][y].H
						boolean = True
		if x+1 >=0: #Take care of x+1
			if y-1 >= 0: #Take care of x+1,y-1
				if self.map.grid[x+1][y-1].state != 1: #If a passble block
					if self.openList.count(self.map.grid[x+1][y-1]) ==0 and self.closedList.count(self.map.grid[x+1][y-1]) == 0: #If not in lists
						self.openList.append(self.map.grid[x+1][y-1])
						self.map.grid[x+1][y-1].G = self.map.grid[x][y].G + 14
						self.map.grid[x+1][y-1].H = self.manhattan(self.map.grid[x+1][y-1])
						self.map.grid[x+1][y-1].parent = [x,y]
						self.map.grid[x+1][y-1].F = self.map.grid[x+1][y-1].G + self.map.grid[x+1][y-1].H
						boolean = True
			if y+1 <= 19: #Take care of x+1,y+1
				if self.map.grid[x+1][y+1].state != 1: #If a passble block
					if self.openList.count(self.map.grid[x+1][y+1]) ==0 and self.closedList.count(self.map.grid[x+1][y+1]) == 0: #If not in lists
						self.openList.append(self.map.grid[x+1][y+1])
						self.map.grid[x+1][y+1].G = self.map.grid[x][y].G + 14
						self.map.grid[x+1][y+1].H = self.manhattan(self.map.grid[x+1][y+1])
						self.map.grid[x+1][y+1].parent = [x,y]
						self.map.grid[x+1][y+1].F = self.map.grid[x+1][y+1].G + self.map.grid[x+1][y+1].H
						boolean = True
			#Take care of y = 0
			if self.map.grid[x+1][y].state != 1: #If a passble block
					if self.openList.count(self.map.grid[x+1][y]) ==0 and self.closedList.count(self.map.grid[x+1][y]) == 0: #If not in lists
						self.openList.append(self.map.grid[x+1][y])
						self.map.grid[x+1][y].G = self.map.grid[x][y].G + 10
						self.map.grid[x+1][y].H = self.manhattan(self.map.grid[x+1][y])
						self.map.grid[x+1][y].parent = [x,y]
						self.map.grid[x+1][y].F = self.map.grid[x+1][y].G + self.map.grid[x+1][y].H
						boolean = True
		#Take care of x + 0
		if self.map.grid[x][y+1].state!=1: #x,y+1
			if self.openList.count(self.map.grid[x][y+1]) == 0 and self.closedList.count(self.map.grid[x][y+1]) == 0:
				self.openList.append(self.map.grid[x][y+1])
				self.map.grid[x][y+1].G = self.map.grid[x][y].G + 10
				self.map.grid[x][y+1].H = self.manhattan(self.map.grid[x][y+1])
				self.map.grid[x][y+1].parent = [x,y]
				self.map.grid[x][y+1].F = self.map.grid[x][y+1].G + self.map.grid[x][y+1].H
				boolean = True
		if self.map.grid[x][y-1].state!=1: #x,y-1
			if self.openList.count(self.map.grid[x][y-1]) == 0 and self.closedList.count(self.map.grid[x][y-1]) == 0:
				self.openList.append(self.map.grid[x][y-1])
				self.map.grid[x][y-1].G = self.map.grid[x][y].G + 10
				self.map.grid[x][y-1].H = self.manhattan(self.map.grid[x][y-1])
				self.map.grid[x][y-1].parent = [x,y]
				self.map.grid[x][y-1].F = self.map.grid[x][y-1].G + self.map.grid[x][y-1].H
				boolean = True
		return boolean
				