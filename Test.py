#test.py

import pygame
from map import Map
import sys

class Test():
	def __init__(self):
		"""Setup the window, etc"""
		self.windowX = 1024
		self.windowY = 768
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
		
	def run(self):
		self.clock.tick()
		while True:
			#self.handle_events()
			#self.update()
			self.draw()
			pygame.display.flip()
		else:
			self.exit_game()
		self.msPassed = self.clock.tick(60)
	
	def handle_events(self):
		pass
	
	def update(self):
		pass
	
	def draw(self):
		for x in self.map.grid:
			for y in x:
				#print "x,y: ("+ repr(y.x)+","+repr(y.y)+")"
				if y.passable:
					self.screen.blit(self.open,y.rect)
				else:
					self.screen.blit(self.closed,y.rect)
	
	def exit_game(self):
		pygame.quit()
		sys.exit()
		
test = Test()
test.run()