import pygame as pg
from math import sin
from support import *

class Entity(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.direction = vector()
        self.frame_index = 0
        self.animation_speed = 0.15

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.horizontal_collsion()
        self.hitbox.y += self.direction.y * speed
        self.vertical_collision()
        self.rect.center = self.hitbox.center

    def horizontal_collsion(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.x > 0:
                    self.hitbox.right = sprite.hitbox.left
                elif self.direction.x < 0:
                    self.hitbox.left = sprite.hitbox.right
    
    def vertical_collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.y > 0:
                    self.hitbox.bottom = sprite.hitbox.top
                elif self.direction.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom
        
    def wave_value(self):
        value = sin(get_time())
        
        return 255 if value >= -0.5 else 0

    def import_assets(self, entity_type, entity_name):
        character_path = f"../graphics/{entity_type}/{entity_name}/"
        
        self.animations = {
            "left": [], "right": [],
            "right_idle": [], "left_idle": []
            }
        for key in ["right", "right_idle"]:
            key2 = key.replace("right", "left")
            self.animations[key], self.animations[key2] = import_images_special(character_path + key)

    def animate(self):
        temp = self.status.split("_")
        if temp[-1] != "attack":
            animation = self.animations[self.status]
        else:
            animation = self.animations[temp[0] + "_idle"]
        self.frame_index += self.animation_speed
        if self.frame_index > len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        alpha = 255 if self.vulnerable else self.wave_value()
        self.image.set_alpha(alpha)
