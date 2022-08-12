import pygame
import random
import sys
from pygame.sprite import Sprite

class BallSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 40, 40)

    def update(self, x, y):
        self.rect.center = (x, y)