import pygame

from entity import Entity
from keylistener import KeyListener
from screen import Screen
from switch import Switch


class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__(keylistener, screen, x, y)
        self.pokedollars: int = 0

        

        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.change_map: Switch | None = None

    def update(self) -> None:
        self.check_input()
        self.check_move()
        super().update()

    def check_move(self) -> None:
        if self.animation_walk is False:
            temp_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(pygame.K_q):
                temp_hitbox.x -= 16
                self.move(temp_hitbox, "left")
            elif self.keylistener.key_pressed(pygame.K_d):
                temp_hitbox.x += 16
                self.move(temp_hitbox, "right")
            elif self.keylistener.key_pressed(pygame.K_z):
                temp_hitbox.y -= 16
                self.move(temp_hitbox, "up")
            elif self.keylistener.key_pressed(pygame.K_s):
                temp_hitbox.y += 16
                self.move(temp_hitbox, "down")

    def move(self, temp_hitbox, direction):
        if not self.check_collisions(temp_hitbox):
            self.check_collisions_switchs(temp_hitbox)
            if direction == "left":
                self.move_left()
            elif direction == "right":
                self.move_right()
            elif direction == "up":
                self.move_up()
            elif direction == "down":
                self.move_down()
        else:
            self.direction = direction

    def add_switchs(self, switchs: list[Switch]):
        self.switchs = switchs

    def check_collisions_switchs(self, temp_hitbox):
        if self.switchs:
            for switch in self.switchs:
                if switch.check_collision(temp_hitbox):
                    self.change_map = switch

    def add_collisions(self, collisions):
        self.collisions = collisions

    def check_collisions(self, temp_hitbox: pygame.Rect):
        if self.collisions:
            for collision in self.collisions:
                if temp_hitbox.colliderect(collision):
                    return True
        return False

