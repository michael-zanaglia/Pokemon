# import pygame
# from keylistener import KeyListener
# from tool import Tool

# class Entity(pygame.sprite.Sprite):
#     def __init__(self, keylistener: KeyListener):
#         super().__init__()
#         self.keylistener = keylistener
#         self.sprite = pygame.image.load('Pokemon/graphique/sprite/hero_01_red_m_walk.png')
#         self.image = Tool.split_image(self.sprite, 0, 0, 24, 32)
#         self.position = [0,0]
#         self.rect: pygame.Rect = pygame.Rect(0, 0, 24, 32)
#         # self.direction: str = "down"
#         self.all_images = self.get_all_images()
#         # self.animation_index = 0
    
#     def update(self):
#         self.check_move()
#         self.rect.topleft = self.position
#         # self.update_animation()
    
#     def check_move(self):
#         if self.keylistener.key_pressed(pygame.K_a):
#             self.start_press_time = pygame.time.get_ticks()
#             self.move_left()
#             if self.press_duration >= 1000:
#                 self.change_horizontal_animation("left")
#         elif self.keylistener.key_pressed(pygame.K_d):
#             self.start_press_time = pygame.time.get_ticks()
#             self.move_right()
#             if self.press_duration >= 1000:
#                 self.change_horizontal_animation("right")
#         elif self.keylistener.key_pressed(pygame.K_w):
#             self.start_press_time = pygame.time.get_ticks()
#             self.move_up()
#             if self.press_duration >= 1000:
#                 self.change_horizontal_animation("up")
#         elif self.keylistener.key_pressed(pygame.K_s):
#             self.start_press_time = pygame.time.get_ticks()
#             self.move_down()
#             if self.press_duration >= 1000:
#                 self.change_horizontal_animation("down")
#         else:
#             self.start_press_time = 0

#         if self.start_press_time:
#             self.press_duration = pygame.time.get_ticks() - self.start_press_time
#         else:
#             self.press_duration = 0

#         # Cambia animazione in orizzontale dopo 1 secondi di pressione
    
#     def change_horizontal_animation(self, plus):
#         # Cambia l'animazione in orizzontale qui
#         # Ad esempio, cambia l'immagine o l'indice dell'animazione
#         self.image = self.all_images[f'{plus}'][1]
#         if self.press_duration >= 2000:
#             self.image_res(f"{plus}")

#     def image_res(self, direct):
#         self.image = self.all_images[f"{direct}"][0]
#     # def check_move(self):
#     #     if self.keylistener.key_pressed(pygame.K_a):
#     #         self.move_left()
#     #     elif self.keylistener.key_pressed(pygame.K_d):
#     #         self.move_right()
#     #     elif self.keylistener.key_pressed(pygame.K_w):
#     #         self.move_up()
#     #     elif self.keylistener.key_pressed(pygame.K_s):
#     #         self.move_down()

#     def move_left(self):
#         self.position[0] -= 1
#         self.image = self.all_images['left'][0]

#     def move_right(self):
#         self.position[0] += 1
#         self.image = self.all_images['right'][0]
#     def move_up(self):
#         self.position[1] -= 1
#         self.image = self.all_images['up'][1]
#     def move_down(self):
#         self.position[1] += 1
#         self.image = self.all_images['down'][1]

#     # def update_animation(self):
#     #     # Incrementa l'indice dell'animazione per ottenere un effetto di movimento
#     #     self.animation_index = (self.animation_index + 1) % len(self.all_images[self.direction])
#     #     # Mise ajour
#     #     self.image = self.all_images[self.direction][self.animation_index]

#     def get_all_images(self):
#         all_images = {
#             "down": [],
#             "left": [],
#             "right": [],
#             "up": []
#         }
#         for i in range(4): # iteration dict
#             for j, key in enumerate(all_images.keys()):
#                 all_images[key].append(Tool.split_image(self.sprite, i*24, j*32, 24, 32))
#         return all_images
    

import pygame
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
        self.start_press_time = 0
        self.press_duration = 0

    def update(self):
        self.check_move()
        self.rect.topleft = self.position

    def check_move(self):
        self.press_duration = pygame.time.get_ticks() - self.start_press_time

        if self.keylistener.key_pressed(pygame.K_a):
            self.start_press_time = pygame.time.get_ticks()
            self.move_left()
        elif self.keylistener.key_pressed(pygame.K_d):
            self.start_press_time = pygame.time.get_ticks()
            self.move_right()
        elif self.keylistener.key_pressed(pygame.K_w):
            self.start_press_time = pygame.time.get_ticks()
            self.move_up()
        elif self.keylistener.key_pressed(pygame.K_s):
            self.start_press_time = pygame.time.get_ticks()
            self.move_down()
        else:
            self.start_press_time = 0

        # Cambia animazione in orizzontale dopo 1 secondo di pressione
        if self.press_duration >= 1000:
            self.change_horizontal_animation()

    def change_horizontal_animation(self):
        direction = None

        if self.keylistener.key_pressed(pygame.K_a):
            direction = "left"
        elif self.keylistener.key_pressed(pygame.K_d):
            direction = "right"
        
        if direction:
            self.image_res(direction)

    def image_res(self, direct):
        self.image = self.all_images[direct][0]

    def move_left(self):
        self.position[0] -= 1
        self.image = self.all_images['left'][0]

    def move_right(self):
        self.position[0] += 1
        self.image = self.all_images['right'][0]

    def move_up(self):
        self.position[1] -= 1
        self.image = self.all_images['up'][1]

    def move_down(self):
        self.position[1] += 1
        self.image = self.all_images['down'][1]

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
