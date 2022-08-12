import sys
import Highscores as highscore
from settings import *
import pygame
import random
import pygame_menu
from pygame_menu import Theme


class GameInterface:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()
        self.colors = COLORS

        self.loginScreen = None
        self.registerScreen = None
        self.mainMenuScreen = None
        self.pauseScreen = None
        self.gameOverScreen = None
        self.leaderBoardScreen = None
        self.startScreen = None

        self.gameDisplay = DISPLAY_SCREEN
        self.bgImg = BG_IMAGE
        self.bgImg = pygame.transform.scale(
            self.bgImg, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.theme = THEME
        self.start_theme = START_THEME
        self.theme.widget_selection_color = pygame_menu.widgets.NoneSelection

    def draw_background(self):
        self.gameDisplay.blit(BG_IMAGE, (0, 0))

    def show_text(self, x, y, text, fontSize=26, textColor=COLORS["WHITE"], hasBox=False):
        font = pygame.font.Font('freesansbold.ttf', fontSize)
        textBox = font.render(text, True, textColor)
        if hasBox:
            box = pygame.draw.rect(
                DISPLAY_SCREEN, COLORS["ORANGE"], (x - 10, y - 5, 180, 40))
        self.gameDisplay.blit(textBox, (x, y))

    # Login Screen -----
    def drawLoginScreen(self):
        self.loginScreen = pygame_menu.Menu('Login', 600, 600,
                                            theme=self.theme)
        loginUsername = self.loginScreen.add.text_input('Username: ',
                                                        maxchar=30,
                                                        align=ALIGN,
                                                        textinput_id='username',
                                                        background_color=(0, 0, 0, 0))
        loginPassword = self.loginScreen.add.text_input('Password: ', maxchar=30, password=True,
                                                        align=ALIGN,
                                                        textinput_id='password',
                                                        background_color=(0, 0, 0, 0))
        return self.loginScreen

    # Register Screen ----
    def drawRegisterScreen(self):
        self.registerScreen = pygame_menu.Menu(
            'Register', 600, 600, theme=self.theme)
        registerUsername = self.registerScreen.add.text_input('Username: ',
                                                              maxchar=30,
                                                              align=ALIGN,
                                                              textinput_id='username',
                                                              background_color=(0, 0, 0, 0))
        registerPassword = self.registerScreen.add.text_input('Password: ',
                                                              maxchar=30,
                                                              password=True,
                                                              align=ALIGN,
                                                              textinput_id='password',
                                                              background_color=(0, 0, 0, 0))
        registerPassword2 = self.registerScreen.add.text_input('Password confirmation: ',
                                                               maxchar=30,
                                                               password=True,
                                                               align=ALIGN,
                                                               textinput_id='password2',
                                                               background_color=(0, 0, 0, 0))
        return self.registerScreen

    # mainMenuScreen ---

    def drawMainMenuScreen(self):
        self.mainMenuScreen = pygame_menu.Menu(
            'Menu', 600, 600, theme=self.theme, enabled=False)
        return self.mainMenuScreen

    # gameOverScreen ----
    def drawGameOver(self):



        self.gameOverScreen = pygame_menu.Menu('Game Over', 600, 600,
                                               theme=self.theme,
                                               enabled=False)
        return self.gameOverScreen

    def drawPauseScreen(self):
        self.pauseScreen = pygame_menu.Menu('Pause', 600, 600,
                                            theme=self.theme,
                                            enabled=False)
        return self.pauseScreen

    def drawStartScreen(self):
        self.startScreen = pygame_menu.Menu('Start', 250, 100,
                                            theme=START_THEME)
        return self.startScreen

    def drawLeaderBoard(self, is_unique=True):
        leaderboard = ""
        scores = highscore.gethighscores(is_unique)

        for n in range(len(scores)):
            leaderboard += "{0:<3}. {1:<15}: {2:<4} \n".format(
                n+1, scores[n][1], scores[n][0])

        self.leaderBoardScreen = pygame_menu.Menu('Leaderboard', 600, 600)
        self.leaderBoardScreen.clear()
        self.leaderBoardScreen.add.label(
            leaderboard, background_color=(0, 0, 0, 0))
        return self.leaderBoardScreen
