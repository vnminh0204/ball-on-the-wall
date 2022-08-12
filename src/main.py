import sys
from game import CowboyGame
from settings import *
from pygame_menu import Theme
from pygame.sprite import Sprite
import pygame_menu
import pygame
import random


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# create game instance
game = CowboyGame()

# Start the game:
startScreen = game.start()
gameStart = True
while gameStart:
    game.interface.draw_background()
    game.interface.show_text(400, 150, "Ball on the Wall", 65, COLORS["BLACK"])

    startScreen.enable()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    if startScreen.is_enabled():
        startScreen.update(events)
        startScreen.draw(DISPLAY_SCREEN)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
