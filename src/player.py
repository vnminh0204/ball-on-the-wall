import pygame
import random
import sys
from pygame.sprite import Sprite

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 50, 50)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()