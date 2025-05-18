import pygame
class tower:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.color = (255, 0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    