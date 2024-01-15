import pygame

from screen import Screen
from map import Map
from entity import Entity
from keylistener import KeyListener
class Game:
    def __init__(self):
        self.running = True
        self.screen = Screen()
        self.map = Map(self.screen)
        self.keylistener = KeyListener()
        self.player = Entity(self.keylistener)
        self.map.add_player(self.player)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_keys(event.key)
            elif event.type == pygame.KEYUP:
                self.keylistener.clear(event.key)

    def run(self):
        while self.running:
            self.handle_input()
            self.map.update()
            self.screen.update()