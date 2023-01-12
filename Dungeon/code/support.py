from csv import reader
from os import walk
import pygame as pg

vector = pg.math.Vector2
get_time = pg.time.get_ticks
load_img = pg.image.load
flip = pg.transform.flip

def import_csv_layout(path):
    terrain_map = []
    with open(path, 'r') as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(row)
    return terrain_map


def import_images(path):
    surf_list = []
    for data in walk(path):
        for image in data[2]:
            full_path = path + '/' + image
            surf_list.append(load_img(full_path).convert_alpha())
            
    return surf_list

def import_images_special(path):
    right_imgs = []
    left_imgs = []
    for data in walk(path):
        for image in data[2]:
            full_path = path + '/' + image
            img = load_img(full_path).convert_alpha()
            right_imgs.append(img)
            left_imgs.append(flip(img, True, False))
            
    return right_imgs, left_imgs