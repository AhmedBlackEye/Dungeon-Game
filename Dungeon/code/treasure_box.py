import pygame as pg
from support import load_img

class Treasure(pg.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.player = player
        self.state = "closed"
        self.closed_img = load_img("../graphics/treasure/closed.png").convert_alpha()
        self.closed_img = pg.transform.scale(self.closed_img, (96, 96))
        self.open_img = load_img("../graphics/treasure/open.png").convert_alpha()
        self.open_img = pg.transform.scale(self.open_img, (96, 96))

        self.image = self.closed_img
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-8, -8)
    
    def open_treasure(self):
        self.image = self.open_img
    
