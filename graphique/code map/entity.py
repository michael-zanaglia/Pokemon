import pygame
from keylistener import KeyListener
from tool import Tool

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener: KeyListener):
        super().__init__()
        self.keylistener = keylistener
        self.sprite = pygame.image.load('C:/Users/Elfo98/OneDrive/Documenti/GitHub/Pokemon/graphique/sprite/hero_01_red_m_walk.png')
        self.image = Tool.split_image(self.sprite, 0, 0, 24, 32)
        self.position = [0,0]
        self.rect: pygame.Rect = pygame.Rect(0, 0, 24, 32)
        self.direction: str = "down"
        self.all_images = self.get_all_images()
        self.animation_index = 0
    
    def update(self):
        self.check_move()
        self.rect.topleft = self.position
        self.update_animation()
    def check_move(self):
        if self.keylistener.key_pressed(pygame.K_a):
            self.move_left()
        elif self.keylistener.key_pressed(pygame.K_d):
            self.move_right()
        elif self.keylistener.key_pressed(pygame.K_w):
            self.move_up()
        elif self.keylistener.key_pressed(pygame.K_s):
            self.move_down()

    def move_left(self):
        self.position[0] -= 1
        self.direction = "left"

    def move_right(self):
        self.position[0] += 1
        self.direction = "right"
    def move_up(self):
        self.position[1] -= 1
        self.direction = "up"
    def move_down(self):
        self.position[1] += 1
        self.direction = "down"

    def update_animation(self):
        # Incrementa l'indice dell'animazione per ottenere un effetto di movimento
        self.animation_index = (self.animation_index + 1) % len(self.all_images[self.direction])
        # Mise ajour
        self.image = self.all_images[self.direction][self.animation_index]

    def get_all_images(self):
        all_images = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }
        for i in range(4): # iteration dict
            for j, key in enumerate(all_images.keys()):
                all_images[key].append(Tool.split_image(self.sprite, i*24, j*32, 24, 32))
        return all_images
    

