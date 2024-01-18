import pygame
import pytmx
import pyscroll

from screen import Screen
from switch import Switch

class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.player = None

        self.switchs: list[Switch] | None = None
        
        self.switch_map('map0')

    def switch_map(self, map: str):
        self.tmx_data = pytmx.load_pygame(f'Pokemon/graphique/{map}.tmx')
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size()) #affichage map
        self.map_layer.zoom = 2 # zoom map
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=6)

    def add_player(self, player):
        self.group.add(player)
        self.player = player

    def update(self):
        self.group.update()
        self.group.center(self.player.rect.center) #player centre dans la carte
        self.group.draw(self.screen.get_display())