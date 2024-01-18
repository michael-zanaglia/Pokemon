import pygame
from pygame.locals import *
import sys
import time
from keylistener import KeyListener
from tool import Tool

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener: KeyListener):
        super().__init__()
        self.keylistener = keylistener
        self.sprite = pygame.image.load('Pokemon/graphique/sprite/hero_01_red_m_walk.png')
        self.image = Tool.split_image(self.sprite, 0, 0, 24, 32)
        self.position = [0, 0]
        self.rect: pygame.Rect = pygame.Rect(0, 0, 24, 32)
        self.all_images = self.get_all_images()
        self.animation_index = 0
        self.animation_delay = 100  # 1000 milliseconds (1 second)
        self.last_animation_time = 1
        self.image = self.all_images['down'][self.animation_index]

    def update(self):
        self.check_move()
        self.rect.topleft = self.position
        self.update_move()

    def check_move(self):
        if self.keylistener.key_pressed(pygame.K_a):
            self.move("left")
        elif self.keylistener.key_pressed(pygame.K_d):
            self.move("right")
        elif self.keylistener.key_pressed(pygame.K_w):
            self.move("up")
        elif self.keylistener.key_pressed(pygame.K_s):
            self.move("down")
                

    def update_move(self, ):
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_animation_time) >= self.animation_delay:
            if self.keylistener.key_pressed(pygame.K_a):
                self.animation_index = (self.animation_index + 1) % len(self.all_images["left"])
                self.image = self.all_images["left"][self.animation_index]
                self.last_animation_time = current_time
            if self.keylistener.key_pressed(pygame.K_d):
                self.animation_index = (self.animation_index + 1) % len(self.all_images["right"])
                self.image = self.all_images["right"][self.animation_index]
                self.last_animation_time = current_time
            if self.keylistener.key_pressed(pygame.K_w):
                self.animation_index = (self.animation_index + 1) % len(self.all_images["up"])
                self.image = self.all_images["up"][self.animation_index]
                self.last_animation_time = current_time
            if self.keylistener.key_pressed(pygame.K_s):
                self.animation_index = (self.animation_index + 1) % len(self.all_images["down"])
                self.image = self.all_images["down"][self.animation_index]
                self.last_animation_time = current_time

    def move(self, direction):
        if direction == 'left':
            self.position[0] -= 1
        elif direction == 'right':
            self.position[0] += 1
        elif direction == 'up':
            self.position[1] -= 1
        elif direction == 'down':
            self.position[1] += 1

    def get_all_images(self):
        all_images = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }
        for i in range(4):  # iteration dict
            for j, key in enumerate(all_images.keys()):
                all_images[key].append(Tool.split_image(self.sprite, i * 24, j * 32, 24, 32))
        return all_images