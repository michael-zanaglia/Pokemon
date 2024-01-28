import pygame
from pygame.locals import *
from keylistener import KeyListener
from tool import Tool

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener: KeyListener):
        super().__init__()
        self.keylistener = keylistener
        self.sprite = pygame.image.load('Pokemon/graphique/sprite/hero_01_red_m_walk.png')
        self.image = Tool.split_image(self.sprite, 0, 0, 24, 32)
        self.position = [125, 180]
        self.rect: pygame.Rect = pygame.Rect(0, 0, 24, 32)
        self.all_images = self.get_all_images()
        self.animation_index = 0
        self.animation_delay = 75
        self.last_animation_time = 1
        self.image = self.all_images['down'][self.animation_index]
        
    def update(self):
        self.check_move()
        self.rect.topleft = self.position
        self.update_move()
    

    def check_move(self):
        keys = pygame.key.get_pressed()
        direction = [0, 0]
        if keys[pygame.K_a]:
            direction[0] -= 1
        if keys[pygame.K_d]:
            direction[0] += 1
        if keys[pygame.K_w]:
            direction[1] -= 1
        if keys[pygame.K_s]:
            direction[1] += 1

        # Controllo per evitare il movimento diagonale
        if direction[0] != 0 and direction[1] != 0:
            if abs(direction[0]) > abs(direction[1]):
                direction[1] = 0
            else:
                direction[0] = 0

        if direction[0] != 0 or direction[1] != 0:
            self.move(direction)
        

    def update_move(self):
        current_time = pygame.time.get_ticks()
        keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
        directions = ["left", "right", "up", "down"]

        if (current_time - self.last_animation_time) >= self.animation_delay:
            for key, direction in zip(keys, directions):
                if self.keylistener.key_pressed(key):
                    self.animation_index = (self.animation_index + 1) % len(self.all_images[direction])
                    self.image = self.all_images[direction][self.animation_index]
                    self.last_animation_time = current_time
            

    def move(self, direction):
        self.position[0] += direction[0]
        self.position[1] += direction[1]

    def get_all_images(self):
        all_images = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }
        for i in range(4):
            for j, key in enumerate(all_images.keys()):
                all_images[key].append(Tool.split_image(self.sprite, i * 24, j * 32, 24, 32))
        return all_images
