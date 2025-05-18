from math import cos
import pygame
class tower:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.color = (255, 0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)    
        self.range = 200
        self.price = 100

class arrow_tower(tower):        
    def __init__ (self, x, y):
        super().__init__(x, y)
        self.color = (255, 0, 0)
        self.damage = 1
        self.fire_rate = 1
        self.range = 200
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.price = 75
class laser(tower):
    def __init__ (self, x, y):
        super().__init__(x, y)
        self.color = (0, 0, 255)
        self.damage = 2
        self.fire_rate = 2
        self.mag_size = 50
        self.cooldown = 4
        self.range = 200
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.price = 150

class cannon(tower):
    def __init__ (self, x, y):
        super().__init__(x, y)
        self.color = (0, 255, 0)
        self.damage = 3
        self.damage_radius = 50
        self.fire_rate = 0.50
        self.range = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.price = 200

class gun(tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0, 0, 0)
        self.damage = 1.5
        self.fire_rate = 1.5
        self.range = 250
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.price = 100
