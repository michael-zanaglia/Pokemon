import pygame


class Switch:
    def __init__(self, type: str, name: str, hitbox: pygame.Rect, port: int):
        self.hitbox = hitbox
        self.port = port
        self.name = name
        self.type = type