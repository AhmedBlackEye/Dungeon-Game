import pygame as pg
from support import vector, load_img

class Weapon(pg.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = "weapon"
        direction = player.status.split('_', 1)[0]
        full_path = f"../graphics/weapons/{player.weapon}/{direction}.png"
        self.image = load_img(full_path).convert_alpha()
        if direction == "right":
            self.rect = self.image.get_rect(midleft = player.rect.midright + vector(-10, 16))
        elif direction == "left":
            self.rect = self.image.get_rect(midright = player.rect.midleft + vector(10, 16))
        elif direction == "up":
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + vector(-10,10))   
        elif direction == "down":
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + vector(-10,-10))