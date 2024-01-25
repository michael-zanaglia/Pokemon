import pygame
from menu_game import Menu_gamex
from screen import Screen
from map import Map
from entity import Entity
from keylistener import KeyListener
pygame.init()
class Game:
    def __init__(self):
        self.running = True
        self.screen = Screen()
        self.map = Map(self.screen)
        self.keylistener = KeyListener()
        self.player = Entity(self.keylistener)
        self.map.add_player(self.player)
        self.menu = Menu_gamex()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_keys(event.key)
                if event.type == pygame.K_LSHIFT:
                    self.menu.menu_game()
            elif event.type == pygame.KEYUP:
                self.keylistener.clear(event.key)

    def run(self):
        while self.running:
            self.handle_input()
            self.map.update()
            self.screen.update()

def start_game():
    pygame.init()
    game = Game()
    game.run()