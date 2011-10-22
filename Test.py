#test.py

import pygame
from map import Map
import sys
from math import floor, tan, radians
from grid import Node
from aStar import AStar

class Test():
	def __init__(self):
		"""Setup the window, etc"""
		self.windowX = 1024
		self.windowY = 768
		self.startBlock = Node(0,0,0,0)
		self.endBlock = Node(0,0,0,0)
		self.windowName = "Path finding Test"
		pygame.init()
		self.clock = pygame.time.Clock()
		self.msPassed = 0
		self.screen = pygame.display.set_mode((self.windowX, self.windowY))
		pygame.display.set_caption(self.windowName)
		pygame.mouse.set_visible(True)
		self.map = Map(540,512,54,32)
		self.open = pygame.image.load("img/test/openIso.png")
		self.closed = pygame.image.load("img/test/closedIso.png")
		self.start = pygame.image.load("img/test/startIso.png")
		self.end = pygame.image.load("img/test/endIso.png")
		self.path = pygame.image.load("img/test/pathIso.png")
		
	def run(self):
		self.clock.tick()
		while True:
			self.handle_events()
			self.update()
			self.draw()
			pygame.display.flip()
		else:
			self.exit_game()
		self.msPassed = self.clock.tick(60)
	
	def path_find(self,start,finish):
		print "Path finding started from ("+repr(start.x/32)+","+repr(start.y/32)+") to ("+repr(finish.x/32)+","+repr(finish.y/32)+")"
		
	def swap(self,setSpecial,x):
		if x > 0: #change start
			self.startBlock.state = 0
			self.startBlock = setSpecial
		if x < 0: #change end
			self.endBlock.state = 0
			self.endBlock = setSpecial
	
	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.exit_game()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse = pygame.mouse.get_pressed()
				if mouse[0]:
					#print "("+repr(event.pos[0])+","+repr(event.pos[1])+")"
					yPosition = int(floor((tan(radians(30)) * event.pos[0] + event.pos[1] + 16)/32))#Find position on y axis
					xPosition = -1 *int(floor((tan(radians(-30)) * event.pos[0] + event.pos[1] + 16)/32))#Find position on x axis
					print "Square: ("+repr(xPosition)+","+repr(yPosition)+")"
					#print len(self.map.grid)
					#print len(self.map.grid[0])
					x = xPosition
					y = yPosition
					self.map.grid[x][y-1].toggle(1)
					"""
					if self.startBlock.x == self.map.grid[x][y].x and self.startBlock.y == self.map.grid[x][y].y:
						self.startBlock = Node(0,0,0,0)
					if self.endBlock.x == self.map.grid[x][y].x and self.endBlock.y == self.map.grid[x][y].y:
						self.endBlock = Node(0,0,0,0)
					if self.map.grid[x][y].state == 2:
						self.swap(self.map.grid[x][y],1)
					if self.map.grid[x][y].state ==3:
						self.swap(self.map.grid[x][y],-1)
					"""
				if mouse[2]:
					x = xPosition
					y = yPosition
					self.map.grid[x][y].toggle(-1)
					if self.startBlock.x == self.map.grid[x][y].x and self.startBlock.y == self.map.grid[x][y].y:
						self.startBlock = Node(0,0,0,0)
					if self.endBlock.x == self.map.grid[x][y].x and self.endBlock.y == self.map.grid[x][y].y:
						self.endBlock = Node(0,0,0,0)
					if self.map.grid[x][y].state == 2:
						self.swap(self.map.grid[x][y],1)
					if self.map.grid[x][y].state ==3:
						self.swap(self.map.grid[x][y],-1)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					path = AStar(self.map,self.startBlock,self.endBlock)
					for node in path.pathList:
						node.state = 4
	
	def update(self):
		pass
	
	def draw(self):
		for x in self.map.grid:
			for y in x:
				#print "x,y: ("+ repr(y.x)+","+repr(y.y)+")"
				if y.state ==0:
					self.screen.blit(self.open,y.rect)
				elif y.state == 1:
					self.screen.blit(self.closed,y.rect)
				elif y.state ==2 :
					self.screen.blit(self.start,y.rect)
				elif y.state == 3:
					self.screen.blit(self.end,y.rect)
				elif y.state == 4:
					self.screen.blit(self.path,y.rect)


	def exit_game(self):
		print "Good bye"
		pygame.quit()
		sys.exit()
		
test = Test()
test.run()