import pygame as pg
from settings import *
from support import load_img

class UI:
    def __init__(self):
        self.display_surf = pg.display.get_surface()
        self.surf_size = self.display_surf.get_size()
        self.font= pg.font.Font(UI_FONT, UI_FONT_SIZE)

        #bar setup
        self.health_bar_rect = pg.Rect(50, 10 , HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.heart_img = load_img("../graphics/other/heart.png")
        self.heart_img = pg.transform.scale(self.heart_img, (32, 32))
        self.heart_rect = self.heart_img.get_rect(topleft = (10, 8))
        self.energy_bar_rect = pg.Rect(50, 47 , ENERGY_BAR_WIDHT, BAR_HEIGHT)
        self.energy_img = load_img("../graphics/other/energy.png")
        self.energy_img = pg.transform.scale(self.energy_img, (32, 32))
        self.energy_rect = self.energy_img.get_rect(topleft = (10, 47))
        self.coin_img = load_img("../graphics/other/coin.png")
        self.coin_img = pg.transform.scale(self.coin_img, (32, 32))
        self.coin_rect = self.coin_img.get_rect(bottomright = (self.surf_size[0] - 105, 55))
        #make weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon["graphic"]
            weapon = load_img(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        #make magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic["graphic"]
            magic = load_img(path).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        pg.draw.rect(self.display_surf, UI_BG_COLOR, bg_rect)
        ratio = current/max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        #drawing the bar
        pg.draw.rect(self.display_surf, color, current_rect)
        pg.draw.rect(self.display_surf, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.surf_size[0] - 50
        y = 50
        text_rect = text_surf.get_rect(bottomright = (x, y))

        pg.draw.rect(self.display_surf, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surf.blit(text_surf, text_rect)
        pg.draw.rect(self.display_surf, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3) #border

    def selection_box(self, left, top, has_switched_weapon):
        bg_rect = pg.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        if not has_switched_weapon:
            pg.draw.rect(self.display_surf, UI_BORDER_COLOR_ACTIVE, bg_rect)
        else:
            pg.draw.rect(self.display_surf, UI_BG_COLOR, bg_rect)

        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched_weapon):
        bg_rect = self.selection_box(10, 600, has_switched_weapon)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surf.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched_magic):
        bg_rect = self.selection_box(90, 600, has_switched_magic)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        self.display_surf.blit(magic_surf, magic_rect)
    
    def endgame(self):
        font= pg.font.Font(UI_FONT, 60)
        text_surf = font.render("YOU WON!!!", False, TEXT_COLOR)
        x = self.surf_size [0] // 2
        y = self.surf_size [1] // 2
        text_rect = text_surf.get_rect(center = (x, y))
        self.display_surf.blit(text_surf, text_rect)

    def display(self, player):
        self.display_surf.blit(self.heart_img, self.heart_rect)
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, HEALTH_COLOR)
        self.display_surf.blit(self.energy_img, self.energy_rect)
        self.show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_COLOR)
        self.display_surf.blit(self.coin_img, self.coin_rect)
        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index, player.can_switch_weapon)
        self.magic_overlay(player.magic_index, player.can_switch_magic)
