import pygame as pg
from settings import *
from support import vector
from menu import Menu

class Upgrade(Menu):
    def __init__(self, player):
        super().__init__(StatsItem, "upgrade")
        self.player = player
        self.attr_num = len(player.stats)
        self.attr_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.width = self.display_surf.get_size()[0] // (self.attr_num +1)
    

    def display(self):
        self.input()
        self.selection_cooldown()
        self.create_items()
        for index, item in enumerate(self.item_list):
            name = self.attr_names[index]
            value = self.player.get_value_by_index(index)
            
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surf, self.selection_index, name,value, max_value, cost)

class StatsItem:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pg.Rect(left, top, width, height)
        self.index = index
        self.font = font
    
    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        #title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + vector(0, 20))
        #cost
        cost = str(int(cost))
        cost_surf = self.font.render(cost, False, color)
        cost_rect = title_surf.get_rect(midbottom = self.rect.midbottom + vector(0, -20))
        #draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        # drawing setup
        top = self.rect.midtop + vector(0, 60)
        bottom = self.rect.midbottom - vector(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        #bar setup
        height = bottom[1] - top[1]
        ratio = (value/max_value) * height
        value_rect = pg.Rect(top[0] - 15, bottom[1]-ratio, 30, 10)
        pg.draw.line(surface, color, top, bottom, 5)
        pg.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        upgrade_attr = list(player.stats.keys())[self.index]
        upgrade_cost = players_upgrade_cost[upgrade_attr]
        if player.exp >= upgrade_cost and player.stats[upgrade_attr] != player.max_stats[upgrade_attr]:
            
            player.exp -= upgrade_cost
            player.stats[upgrade_attr] *= 1.2
            player.upgrade_cost[upgrade_attr] *= 1.4
        
        if player.stats[upgrade_attr] > player.max_stats[upgrade_attr]:
            player.stats[upgrade_attr] = player.max_stats[upgrade_attr]

    def display(self, surface, selection_num, name, value, max_value, cost):
        is_selected = self.index == selection_num
        if is_selected:
            pg.draw.rect(surface, UI_BORDER_COLOR, self.rect)
            pg.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
        else:
            pg.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
            pg.draw.rect(surface, UI_BG_COLOR, self.rect)
        self.display_names(surface, name, cost, is_selected)
        self.display_bar(surface, value, max_value, is_selected)