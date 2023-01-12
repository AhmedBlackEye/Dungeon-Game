import sys
import pygame as pg
from level import Level
from settings import *

class Game:
	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode((WIDTH,HEIGTH), pg.RESIZABLE)
		pg.display.set_caption('Dungeon')
		self.clock = pg.time.Clock()

		self.level = Level()
	
	def run(self):
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					sys.exit()
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_m:
						self.level.toggle_menu()

			self.level.run()
			if self.level.restart:
				self.level = Level()
			pg.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()