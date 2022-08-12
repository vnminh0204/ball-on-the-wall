import pygame
import pygame_menu
import math
import sys
import pathlib
PATH = pathlib.Path(__file__).parents[0]
print(PATH)
from pygame_menu import Theme

DISPLAY_WIDTH, DISPLAY_HEIGHT = 1280, 720
COW_SIZE = (120, 120)
COWBOY_SIZE = (180, 180)

COLORS = {"BLACK": (0, 0, 0), "WHITE": (255, 255, 255), "GREY": (230, 230, 230),
          "ORANGE": (255, 165, 82), "RED": (220, 20, 60)}

DISPLAY_SCREEN = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
BG_IMAGE = pygame.image.load(PATH.joinpath("img/newbg.jpg"))
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

COW_IMAGE = pygame.image.load(PATH.joinpath("img/cow.png")).convert_alpha(DISPLAY_SCREEN)

COWBOY_IMAGE = pygame.image.load(PATH.joinpath("img/cowboy.png")).convert_alpha(DISPLAY_SCREEN)

DOT_IMAGE = pygame.image.load(PATH.joinpath("img/whitedot.png")).convert_alpha(DISPLAY_SCREEN)

THEME = Theme(background_color=COLORS["GREY"],
              title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
              title_font_color=COLORS["BLACK"],
              widget_alignment=pygame_menu.locals.ALIGN_CENTER,
              widget_background_color=COLORS["ORANGE"],
              widget_border_color=COLORS["BLACK"],
              widget_font_color=COLORS["BLACK"],
              widget_margin=(0, 20),
              title_offset=(50, 30),
              title_font_size=50,
              widget_padding=(5, 20, 5, 10),
              widget_cursor=11,
              selection_color=COLORS["BLACK"])

START_THEME = Theme(background_color=COLORS["ORANGE"],
                    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
                    title_font_color=COLORS["BLACK"],
                    widget_alignment=pygame_menu.locals.ALIGN_CENTER,
                    widget_background_color=COLORS["ORANGE"],
                    widget_border_color=COLORS["ORANGE"],
                    widget_font_color=COLORS["BLACK"],
                    widget_margin=(1, 1),
                    title_offset=(0, 0),
                    title_font_size=1,
                    widget_padding=(20, 30, 20, 30),
                    widget_cursor=0,
                    selection_color=COLORS["BLACK"])

ALIGN = pygame_menu.locals.ALIGN_LEFT

TRIALS = 3

BALLHITEVENT = pygame.USEREVENT + 1
