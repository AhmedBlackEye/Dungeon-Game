# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

#User interface
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDHT = 140
ITEM_BOX_SIZE = 80
UI_FONT = "../graphics/font/joystix.ttf"
UI_FONT_SIZE = 18

#general colors
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#eeeeee"

#ui colors
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

#upgrade menu
TEXT_COLOR_SELECTED = "#111111"
BAR_COLOR = "#EEEEEE"
BAR_COLOR_SELECTED = "#111111"
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE"

PLAYER_MENU_BG = "#c4b587"

#game durations
PLAYERS_INVULNERABILITY_DURATION = 500
PLAYER_ATTACK_COOLDOWN = 400
WEAPON_CHANGE_COOLDOWN = 200


hitbox_offset = {
    "player": -26,
    "boundary": 0
}

#player data
player_stats = {
    "lizard": {"health": 300, "energy": 80, "attack": 12, "magic": 3, "speed": 8},
    "knight": {"health": 500, "energy": 60, "attack": 14, "magic": 4, "speed": 5},
    "wizzard": {"health": 250, "energy": 60, "attack": 10, "magic": 8, "speed": 6},
    "elf": {"health": 300, "energy": 90, "attack": 12, "magic": 4, "speed": 7}

}
player_max_stats = {
    "lizard": {"health": 800, "energy": 140, "attack": 20, "magic": 14, "speed": 12},
    "knight": {"health": 800, "energy": 140, "attack": 20, "magic": 14, "speed": 12},
    "wizard": {"health": 800, "energy": 140, "attack": 20, "magic": 14, "speed": 12},
    "elf": {"health": 800, "energy": 140, "attack": 20, "magic": 14, "speed": 12}
}

players_upgrade_cost = {"health": 100, "energy": 100, "attack": 100, "magic": 150, "speed": 120}

#weapon data
weapon_data = {
    "sword": {"cooldown": 100, "damage": 15, "graphic": "../graphics/weapons/sword/full.png"},
    "lance": {"cooldown": 400, "damage": 30, "graphic": "../graphics/weapons/lance/full.png"},
    "axe": {"cooldown": 300, "damage": 20, "graphic": "../graphics/weapons/axe/full.png"},
    "rapier": {"cooldown": 50, "damage": 8, "graphic": "../graphics/weapons/rapier/full.png"},
    "sai": {"cooldown": 80, "damage": 10, "graphic": "../graphics/weapons/sai/full.png"},
}

#magic
magic_data = {
    "flame": {"strength": 5, "cost": 20, "graphic": "../graphics/particles/flame/fire.png", "sound": "../audio/Fire.wav"},
    "heal": {"strength": 20, "cost": 10, "graphic": "../graphics/particles/heal/heal.png", "sound": "../audio/heal.wav"}
}

# enemy
monster_data = {
    "chort": {"health": 70, "exp": 30, "damage": 4, "speed": 7, "resistance": 6, "attack_type": "slash", "attack_radius": 40, "notice_radius": 300, "cooldown": 200},
    "wogol": {"health": 140, "exp": 50, "damage": 6, "speed": 5, "resistance": 5, "attack_type": "slash", "attack_radius": 50, "notice_radius": 350, "cooldown": 200},
    "big_demon": {"health": 1500, "exp": 250, "damage": 12, "speed": 4, "resistance": 4, "attack_type": "slash", "attack_radius": 70, "notice_radius": 500, "cooldown": 300},
    "masked_orc": {"health": 70, "exp": 30, "damage": 4, "speed": 7, "resistance": 6, "attack_type": "slash", "attack_radius": 40, "notice_radius": 300, "cooldown": 200},
    "orc_shaman": {"health": 140, "exp": 50, "damage": 6, "speed": 5, "resistance": 5, "attack_type": "slash", "attack_radius": 50, "notice_radius": 350, "cooldown": 200},
    "ogre": {"health": 1500, "exp": 250, "damage": 12, "speed": 4, "resistance": 4, "attack_type": "slash", "attack_radius": 70, "notice_radius": 500, "cooldown": 300},
    "big_zombie": {"health": 1500, "exp": 250, "damage": 12, "speed": 4, "resistance": 4, "attack_type": "slash", "attack_radius": 70, "notice_radius": 500, "cooldown": 300}
}