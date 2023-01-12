import pygame as pg
from settings import *
from support import get_time, vector

class Menu:
    def __init__(self, Item, class_type):
        self.type = class_type
        self.item = Item
        self.display_surf = pg.display.get_surface()
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)
        #selection system
        self.selection_index = 0
        self.timer = None
        self.can_move = True
        self.selection_time = None
        #item dimension
        self.height = self.display_surf.get_size()[1] * 0.8

    def input(self):
        keys = pg.key.get_pressed()
        if self.can_move:
            if keys[pg.K_RIGHT] and self.selection_index < self.attr_num - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = get_time()

            elif keys[pg.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = get_time()

            elif keys[pg.K_SPACE]:
                self.can_move = False
                self.selection_time = get_time()
                if self.type == "upgrade":
                    self.item_list[self.selection_index].trigger(self.player)
                else:
                    self.item_list[self.selection_index].trigger()

    def selection_cooldown(self):
        if not self.can_move:
            current_time = get_time()
            if current_time - self.selection_time > 300:
                self.can_move = True
    
    def create_items(self):
        self.item_list = []
        full_width = self.display_surf.get_size()[0]
        increment = full_width // self.attr_num
        top = self.display_surf.get_size()[1]* 0.1

        for index in range(self.attr_num):
            left = (index * increment) + (increment - self.width) // 2
            item = self.item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)