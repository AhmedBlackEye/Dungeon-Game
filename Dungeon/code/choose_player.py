import pygame as pg
from settings import *
from menu import Menu
from support import vector, load_img

class ChoosePlayer(Menu):
    def __init__(self):
        super().__init__(CharacterItem, "choose_player")
        self.attr_names = list(player_stats.keys())
        self.attr_num = len(self.attr_names)
        self.width = self.display_surf.get_size()[0] // (self.attr_num + 1)
        self.chosen_player = ""
        self.import_players_img()

    def import_players_img(self):
        self.item_imgs = []
        for index in range(self.attr_num):
            player_name = self.attr_names[index]
            img_path = f"../graphics/player/{player_name}/right/{player_name}_m_run_anim_f0.png"
            img = load_img(img_path).convert_alpha()
            self.item_imgs.append(img)

    def choose_player(self, name):
        self.chosen_player = name

    def display(self):
        self.display_surf.fill(PLAYER_MENU_BG)
        self.input()
        self.selection_cooldown()
        self.create_items()
        for index, item in enumerate(self.item_list):
            player_name = self.attr_names[index]
            img = self.item_imgs[index]
            item.display(self.display_surf, self.selection_index, player_name, img, self.choose_player)
    
class CharacterItem:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pg.Rect(left, top, width, height)
        self.index = index
        self.font = font
    def trigger(self):
        self.choose_player(self.player_name)
    
    def display_names(self, surface, name, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        surf = self.font.render(name, False, color)
        rect = surf.get_rect(midbottom = self.rect.midbottom + vector(0, -20))

        surface.blit(surf, rect)

    def display_img(self,img, surface):
        img = pg.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        img_rect = img.get_rect(center = self.rect.center)
        surface.blit(img, img_rect)

    def display(self, surface, selection_num, player_name, img, chosen_player):
        self.choose_player = chosen_player
        self.player_name = player_name
        is_selected = self.index == selection_num
        if is_selected:
            pg.draw.rect(surface, UI_BORDER_COLOR, self.rect)
            pg.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
        else:
            pg.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
            pg.draw.rect(surface, UI_BG_COLOR, self.rect)
        self.display_names(surface, player_name, is_selected)
        self.display_img(img, surface)