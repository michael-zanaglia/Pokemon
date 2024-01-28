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

        self.wallx = []

    def switch_map(self, map: str):
        self.tmx_data = pytmx.load_pygame(f'Pokemon/graphique/{map}.tmx')
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=11)

    def check_collision(self):
        # Funzione per controllare le collisioni con gli oggetti sulla mappa
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.wallx.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                print(self.wallx)

    def add_player(self, player):
        self.group.add(player)
        self.player = player

    def update(self):
        self.group.update()
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen.get_display())
