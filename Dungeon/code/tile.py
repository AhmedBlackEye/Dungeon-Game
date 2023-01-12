import pygame as pg
from settings import *

class Tile(pg.sprite.Sprite):
	def __init__(self,pos, groups, sprite_type):
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.image = pg.Surface((TILESIZE, TILESIZE))
		y_hitbox = hitbox_offset[sprite_type]
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-6, y_hitbox)