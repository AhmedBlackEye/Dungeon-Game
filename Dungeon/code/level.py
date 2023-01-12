import pygame as pg
from tile import Tile
from player import Player
from enemy import Enemy
from weapon import Weapon
from particle import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from treasure_box import Treasure
from ui import UI
from settings import *
from support import *
from choose_player import ChoosePlayer


class YSortCameraGroup(pg.sprite.Group):

    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_screen_cord = vector(self.display_surface.get_size()) // 2
        self.offset = vector()

        self.floor_surface = pg.image.load(
            "../graphics/tilemap/ground_1.png").convert_alpha()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        #Camera moving as player player moves by shifting the postition of sprites
        self.offset = player.rect.center - self.half_screen_cord
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        for sprite in sorted(self.sprites(),
                             key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def change_floor(self):
        self.floor_surface = pg.image.load(
            "../graphics/tilemap/ground_2.png").convert_alpha()

    def update_enemy(self, player):
        enemy_sprites = [
            sprite for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"
        ]
        for sprite in enemy_sprites:
            sprite.enemy_update(player)


class Level:

    def __init__(self):
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()
        self.attack_sprites = pg.sprite.Group()
        self.attackable_sprites = pg.sprite.Group()
        #game status
        self.map_created = False
        self.made_endgame_changes = False
        self.game_paused = False
        self.game_started = False
        self.restart = False
        self.menu = False

        self.player_name = None
        self.current_attack = None

        # user iterface
        self.ui = UI()
        #classes
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        self.choose_player = ChoosePlayer()

    @staticmethod
    def import_layouts_graphics():
        layouts = {
            "boundary": import_csv_layout("../map/map_FloorBlocks.csv"),
            "entities": import_csv_layout("../map/map_entities.csv"),
            "treasure": import_csv_layout("../map/map_treasure.csv")
        }
        return layouts

    def create_map(self):
        layouts = self.import_layouts_graphics()

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "boundary")

                        elif style == "treasure":
                            self.treasure = Treasure(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                self.player)

                        elif style == "entities":
                            if col == "296":
                                self.player = Player(self.player_name, (x, y),
                                                     [self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic)
                            else:
                                if col == "102": monster_name = "chort"
                                elif col == "313": monster_name = "wogol"
                                elif col == "329": monster_name = "big_demon"
                                elif col == "180": monster_name = "orc_shaman"
                                elif col == "170": monster_name = "ogre"
                                elif col == "146": monster_name = "masked_orc"
                                elif col == "6": monster_name = "big_zombie"
                                Enemy(monster_name, (x, y), [
                                    self.visible_sprites,
                                    self.attackable_sprites
                                ], self.obstacle_sprites, self.damage_player,
                                      self.trigger_death_particles,
                                      self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost,
                                   [self.visible_sprites])
        elif style == "flame":
            self.magic_player.flame(
                self.player, cost, [self.visible_sprites, self.attack_sprites])

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                sprite_collisions = pg.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False)
                if sprite_collisions:
                    for target_sprite in sprite_collisions:
                        target_sprite.get_damage(self.player,
                                                 attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = get_time()
            self.animation_player.create_particles(attack_type,
                                                   self.player.rect.center,
                                                   [self.visible_sprites])

    def trigger_death_particles(self, particle_type, pos):
        self.animation_player.create_particles(particle_type, pos,
                                               self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused
        self.menu = not self.menu

    def run_endgame(self):
        if not self.made_endgame_changes:
            self.visible_sprites.change_floor()
            self.treasure.open_treasure()
            self.made_endgame_changes = True
        if self.player.rect.colliderect(self.treasure.rect):
            self.game_paused = True
            self.ui.endgame()

    def check_game_status(self):
        if self.player.health <= 0:
            self.restart = True

    def check_if_game_started(self):
        if self.choose_player.chosen_player != "":
            self.player_name = self.choose_player.chosen_player
            self.game_started = True

    def run(self):
        # update and draw the game
        if self.game_started and not self.map_created:
            self.create_map()
            self.upgrade = Upgrade(self.player)
            self.map_created = True

        if not self.game_started:
            self.choose_player.display()
            self.check_if_game_started()
        else:
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)
            self.check_game_status()
            if not self.attackable_sprites:
                self.run_endgame()
            if self.game_paused and self.menu:
                self.upgrade.display()
            elif not self.game_paused:
                self.visible_sprites.update()
                self.visible_sprites.update_enemy(self.player)
                self.player_attack_logic()
