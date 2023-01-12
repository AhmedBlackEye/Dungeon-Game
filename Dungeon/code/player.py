import pygame as pg
from settings import *
from support import *
from entity import Entity

class Player(Entity):
	def __init__(self,player_name, pos,groups, obstacles, create_attack, destroy_attack, create_magic):
		super().__init__(groups)
		self.player_name = player_name
		self.obstacle_sprites = obstacles
		self.import_assets("player", self.player_name)
		self.image = self.animations["right"][0]
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-6, hitbox_offset["player"])
		self.status = "left"
		#damage timer
		self.vulnerable = True
		self.hurt_time = None
		#attacks
		self.attacking = False
		self.attack_time = None
		#weapon
		self.weapon_index = 0
		self.weapon_list = list(weapon_data.keys())
		self.weapon = self.weapon_list[self.weapon_index]
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		#magic
		self.magic_index = 0
		self.magic_list = list(magic_data.keys())
		self.magic = self.magic_list[self.magic_index]
		self.can_switch_magic = True
		self.magic_switch_time = None
		#stats
		self.max_stats = player_max_stats[self.player_name]
		self.stats = player_stats[self.player_name]
		self.upgrade_cost = players_upgrade_cost
		self.health = self.stats["health"]
		self.energy = self.stats["energy"]
		self.speed = self.stats["speed"]
		self.exp = 0
		#borrowed functions
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.create_magic = create_magic


	def usr_input(self):
		if not self.attacking:
			keys = pg.key.get_pressed()
			self.player_movement(keys)
			self.attacks_input(keys)
			self.magic_input(keys)
		
	def player_movement(self, keys):
		if keys[pg.K_UP]:
			self.direction.y = -1
		elif keys[pg.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pg.K_RIGHT]:
			self.direction.x = 1
			self.status = "right"
		elif keys[pg.K_LEFT]:
			self.direction.x = -1
			self.status = "left"
		else:
			self.direction.x = 0

	def attacks_input(self, keys):
		if keys[pg.K_SPACE] and not self.attacking:
			self.attacking = True
			self.attack_time = get_time()
			self.create_attack()

		if keys[pg.K_w] and self.can_switch_weapon :
			self.can_switch_weapon = False
			self.weapon_switch_time = get_time()
			self.weapon_index += 1
			if self.weapon_index == len(self.weapon_list):
				self.weapon_index = 0
			self.weapon = self.weapon_list[self.weapon_index]

	def magic_input(self, keys):
		if keys[pg.K_LCTRL] and not self.attacking:
			self.attacking = True
			self.attack_time = get_time()
			style = self.magic_list[self.magic_index]
			strength = magic_data[style]["strength"] + self.stats["magic"]
			cost = magic_data[style]["cost"]
			self.create_magic(style, strength, cost)

		if keys[pg.K_g] and self.can_switch_magic :
			self.can_switch_magic = False
			self.magic_switch_time = get_time()
			self.magic_index += 1
			if self.magic_index == len(self.magic_list):
				self.magic_index = 0
			self.magic = self.magic_list[self.magic_index]

	def get_full_weapon_damage(self):
		player_damage = self.stats["attack"]
		weapon_damage = weapon_data[self.weapon]["damage"]

		return player_damage + weapon_damage

	def get_full_magic_damage(self):
		player_damage = self.stats["attack"]
		self.magic = self.magic_list[self.magic_index]
		magic_damage = magic_data[self.magic]["strength"]

		return player_damage + magic_damage

	def energy_recovery(self):
		if self.energy < self.stats["energy"]:
			self.energy += 0.01 * self.stats["magic"]
	
	def get_value_by_index(self, index):
		return list(self.stats.values())[index]

	def get_cost_by_index(self, index):
		return list(self.upgrade_cost.values())[index]

	def cooldowns(self):
		current_time = get_time()
		if self.attacking:
			if current_time - self.attack_time >= PLAYER_ATTACK_COOLDOWN + weapon_data[self.weapon]["cooldown"]:
				self.attacking = False
				self.destroy_attack()

		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= WEAPON_CHANGE_COOLDOWN:
				self.can_switch_weapon = True
				
		if not self.can_switch_magic:
			if current_time - self.magic_switch_time >= WEAPON_CHANGE_COOLDOWN:
				self.can_switch_magic = True
		
		if not self.vulnerable:
			if current_time - self.hurt_time >= PLAYERS_INVULNERABILITY_DURATION:
				self.vulnerable = True
		
	def get_status(self):
		if self.direction == (0, 0):
			if not "idle" in self.status:
				self.status += "_idle"
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0

	def update(self):
		self.usr_input()
		self.cooldowns()
		self.get_status()
		self.energy_recovery()
		self.animate()
		self.move(self.speed)