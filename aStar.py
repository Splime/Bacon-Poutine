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
		self.openList.append(self.startNode)
		self.cols = len(map.grid[0])
		self.rows = len(map.grid)
		self.find_path()
		
	def find_path(self):
		self.adjacent(self.startNode)
		self.openList.remove(self.startNode)
		self.closedList.append(self.startNode)
		while(self.openList.count(self.endNode) == 0):
		
		
		
		#End of loop
		tempNode = self.endNode
		while tempNode != self.startNode:
			self.pathList.append(tempNode)
			tempNode = self.map.grid[tempNode.parent[0],tempNode.parent[1])
		self.pathList.reverse()
	def manhattan(self,node):
		return (abs(self.endNode.x-node.x)/32 + abs(self.endNode.y-node.y)/32)*10
		
	def adjacent(self,node):
		x = int(node.x/32)
		y = int(node.y/32)
		if x-1 >=0: #Take care of x-1
			if y-1 >= 0: #Take care of x-1,y-1
				if self.map.grid[x-1][y-1].state != 1: #If a passble block
					if self.openList.count(self.map.grid[x-1][y-1]) ==0 and self.closedList.count(self.map.grid[x-1][y-1]) == 0: #If not in lists
						self.openList.append(self.map.grid[x-1][y-1])
						self.map.grid[x-1][y-1].G += 14
						self.map.grid[x-1][y-1].H = self.manhattan(self.map.grid[x-1][y-1])
						self.map.grid[x-1][y-1].parent = [x,y]
			if y+1 <= 19: #Take care of x-1,y+1
				if self.map.grid[x-1][y+1].state != 1: #If a passble block
					if self.openList.count(self.map.grid[x-1][y+1]) ==0 and self.closedList.count(self.map.grid[x-1][y+1]) == 0: #If not in lists
						self.openList.append(self.map.grid[x-1][y+1])
						self.map.grid[x-1][y+1].G += 14
						self.map.grid[x-1][y+1].H = self.manhattan(self.map.grid[x-1][y+1])
						self.map.grid[x-1][y+1].parent = [x,y]
			#Take care of y + 0
			if self.map.grid[x-1][y].state != 1: #If a passble block
					if self.openList.count(self.map.grid[x-1][y]) ==0 and self.closedList.count(self.map.grid[x-1][y]) == 0: #If not in lists
						self.openList.append(self.map.grid[x-1][y])
						self.map.grid[x-1][y].G += 10
						self.map.grid[x-1][y].H = self.manhattan(self.map.grid[x-1][y])
						self.map.grid[x-1][y].parent = [x,y]
		if x+1 >=0: #Take care of x+1
			if y-1 >= 0: #Take care of x+1,y-1
				if self.map.grid[x+1][y-1].state != 1: #If a passble block
					if self.openList.count(self.map.grid[x+1][y-1]) ==0 and self.closedList.count(self.map.grid[x+1][y-1]) == 0: #If not in lists
						self.openList.append(self.map.grid[x+1][y-1])
						self.map.grid[x+1][y-1].G += 14
						self.map.grid[x+1][y-1].H = self.manhattan(self.map.grid[x+1][y-1])
						self.map.grid[x+1][y-1].parent = [x,y]
			if y+1 <= 19: #Take care of x+1,y+1
				if self.map.grid[x+1][y+1].state != 1: #If a passble block
					if self.openList.count(self.map.grid[x+1][y+1]) ==0 and self.closedList.count(self.map.grid[x+1][y+1]) == 0: #If not in lists
						self.openList.append(self.map.grid[x+1][y+1])
						self.map.grid[x+1][y+1].G += 14
						self.map.grid[x+1][y+1].H = self.manhattan(self.map.grid[x+1][y+1])
						self.map.grid[x+1][y+1].parent = [x,y]
			#Take care of y = 0
			if self.map.grid[x+1][y].state != 1: #If a passble block
					if self.openList.count(self.map.grid[x+1][y]) ==0 and self.closedList.count(self.map.grid[x+1][y]) == 0: #If not in lists
						self.openList.append(self.map.grid[x+1][y])
						self.map.grid[x+1][y].G += 10
						self.map.grid[x+1][y].H = self.manhattan(self.map.grid[x+1][y])
						self.map.grid[x+1][y].parent = [x,y]
		#Take care of x + 0
		if self.map.grid[x][y+1].state!=1: #x,y+1
			if self.openList.count(self.map.grid[x][y+1]) == 0 and self.closedList.count(self.map.grid[x][y+1]) == 0:
				self.openList.append(self.map.grid[x][y+1])
				self.map.grid[x][y+1].G += 10
				self.map.grid[x][y+1].H = self.manhattan(self.map.grid[x][y+1])
				self.map.grid[x][y+1].parent = [x,y]
		if self.map.grid[x][y-1].state!=1: #x,y-1
			if self.openList.count(self.map.grid[x][y-1]) == 0 and self.closedList.count(self.map.grid[x][y-1]) == 0:
				self.openList.append(self.map.grid[x][y-1])
				self.map.grid[x][y-1].G += 10
				self.map.grid[x][y-1].H = self.manhattan(self.map.grid[x][y-1])
				self.map.grid[x][y-1].parent = [x,y]
				