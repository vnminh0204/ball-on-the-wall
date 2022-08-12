import pygame
import random
import pathlib
PATH = pathlib.Path(__file__).parents[0]
from pygame.sprite import Sprite


class cowObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            PATH.joinpath("img/cow.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.x = random.randrange(100, 1000, 50)
        self.y = random.randrange(400, 530, 50)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def setPos(self, x, y):
        self.x = x
        self.y = y
