import pygame_menu
from pygame_menu import Theme
import sys
import Highscores

pygame.init()
surface = pygame.display.set_mode((1000, 600))


def showhighscores(is_unique=False):
    leaderboard = ""
    scores = Highscores.gethighscores(is_unique)
    for n in range(len(scores)):
        leaderboard += "{0:<3}. {1:<15}: {2:<4} \n".format(
            n+1, scores[n][1], scores[n][0])
    high_score_screen.clear()
    high_score_screen.add.label(leaderboard, background_color=(0, 0, 0, 0))


high_score_screen = pygame_menu.Menu("High score screen", 600, 600)
showhighscores()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if high_score_screen.is_enabled():
        high_score_screen.update(events)
        high_score_screen.draw(surface)

    pygame.display.update()
