#test.py

import pygame
from map import Map
import sys
from math import floor
from grid import Grid

class Test():
	def __init__(self):
		"""Setup the window, etc"""
		self.windowX = 1024
		self.windowY = 768
		self.startBlock = Grid(0,0,0,0)
		self.endBlock = Grid(0,0,0,0)
		self.windowName = "Grid Test"
		pygame.init()
		self.clock = pygame.time.Clock()
		self.msPassed = 0
		self.screen = pygame.display.set_mode((self.windowX, self.windowY))
		pygame.display.set_caption(self.windowName)
		pygame.mouse.set_visible(True)
		self.map = Map(640,640,32)
		self.open = pygame.image.load("img/test/open.jpg").convert()
		self.closed = pygame.image.load("img/test/closed.jpg").convert()
		self.start = pygame.image.load("img/test/start.jpg").convert()
		self.end = pygame.image.load("img/test/end.jpg").convert()
		
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
		pass
		
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
					if event.pos[0] <640 and event.pos[0] >= 0 and event.pos[1]<640 and event.pos[1]>=0:
						x = int(event.pos[0]/32)
						y = int(event.pos[1]/32)
						self.map.grid[x][y].toggle(1)
						if self.startBlock.x == self.map.grid[x][y].x and self.startBlock.y == self.map.grid[x][y].y:
							self.startBlock = Grid(0,0,0,0)
						if self.endBlock.x == self.map.grid[x][y].x and self.endBlock.y == self.map.grid[x][y].y:
							self.endBlock = Grid(0,0,0,0)
						if self.map.grid[x][y].state == 2:
							self.swap(self.map.grid[x][y],1)
						if self.map.grid[x][y].state ==3:
							self.swap(self.map.grid[x][y],-1)
				if mouse[2]:
					if event.pos[0] <640 and event.pos[0] >= 0 and event.pos[1]<640 and event.pos[1]>=0:
						x = int(event.pos[0]/32)
						y = int(event.pos[1]/32)
						self.map.grid[x][y].toggle(-1)
						if self.startBlock.x == self.map.grid[x][y].x and self.startBlock.y == self.map.grid[x][y].y:
							self.startBlock = Grid(0,0,0,0)
						if self.endBlock.x == self.map.grid[x][y].x and self.endBlock.y == self.map.grid[x][y].y:
							self.endBlock = Grid(0,0,0,0)
						if self.map.grid[x][y].state == 2:
							self.swap(self.map.grid[x][y],1)
						if self.map.grid[x][y].state ==3:
							self.swap(self.map.grid[x][y],-1)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.path_find(self.startBlock,self.finishBlock)
	
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


	def exit_game(self):
		print "Good bye"
		pygame.quit()
		sys.exit()
		
test = Test()
test.run()