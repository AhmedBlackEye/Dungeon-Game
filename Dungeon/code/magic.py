from random import randint
from support import *
from settings import *

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            player.health = min(player.health + strength, player.stats["health"])
            player.energy -= cost
            self.animation_player.create_particles("aura", player.rect.center, groups)
            self.animation_player.create_particles("heal", player.rect.center, groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            player_direction = player.status.split('_')[0]
            pos_change_limit = TILESIZE // 3

            if player_direction == "right":
                direction = vector(1, 0)
            elif player_direction == "left":
                direction = vector(-1, 0)
            elif player_direction == "up":
                direction = vector(0, -1)
            elif player_direction == "down":
                direction = vector(0, 1) 

            for i in range(1, 6):
                if direction.x:
                    offset_x = direction.x * i * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-pos_change_limit, pos_change_limit)
                    y = player.rect.centery + randint(-pos_change_limit, pos_change_limit)
                else:
                    offset_y = direction.y * i * TILESIZE
                    x = player.rect.centerx + randint(-pos_change_limit, pos_change_limit)
                    y = player.rect.centery + offset_y + randint(-pos_change_limit, pos_change_limit)
                self.animation_player.create_particles("flame", (x, y), groups)


