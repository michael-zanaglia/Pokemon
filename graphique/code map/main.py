import pygame
from menu import Menu_game

pygame.init()

if __name__ == "__main__":
    menu = Menu_game()#agg menu
    menu.run()