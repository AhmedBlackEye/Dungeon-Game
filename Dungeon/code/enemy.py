import pygame as pg
from entity import Entity
from settings import *
from support import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacles, damage_player, trigger_death_particles, add_exp):
        super().__init__(groups)
        self.sprite_type = "enemy"
        self.import_assets("monsters", monster_name)
        self.obstacle_sprites = obstacles
        self.status = "right"
        self.image = self.animations["right"][0]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)

        #monster attributes
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resisitance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.attack_type = monster_info["attack_type"]
        self.attack_cooldown = monster_info["cooldown"]
        #causing damage
        self.attacking = False
        # self.can_attack  = True
        self.attack_time = None
        #getting damage
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
        #borrowed functions
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp


    def get_player_distance_direction(self, player):
        enemy_vec = vector(self.rect.center)
        player_vec = vector(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = vector()

        return (distance, direction)

    def get_status(self, player):
        distance,direction = self.get_player_distance_direction(player)
        if distance <= self.attack_radius and not self.attacking:
            self.frame_index = 0
            self.attacking = True
            self.attack_time = get_time()
        elif distance <= self.notice_radius:
            self.status = "left" if direction.x < 0 else "right"
        elif "idle" not in self.status:
            self.status += "_idle"
        
        
    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()

            self.hit_time = get_time()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.trigger_death_particles("coin", self.rect.center)
            self.add_exp(self.exp)
            self.kill()

    def actions(self, player):
        if self.attacking:
            self.damage_player(self.attack_damage, self.attack_type)
            
        elif "idle" not in self.status:
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = vector()

    def cooldowns(self):
        current_time = get_time()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resisitance
           
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.check_death()
    
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)

        self.cooldowns()
