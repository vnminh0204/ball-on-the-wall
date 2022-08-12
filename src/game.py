import sys
import security
from ui import *
from settings import *
from CameraCalibration import CameraCalibration
from DetectBallPosition import DetectBallPosition
from pygame.sprite import Sprite
# from .ballHit import BallHit
from player import Player
from ball import *
from cow import cowObject
from cowboy import cowBoyObject
from pygame_menu import Theme
import random
import sys
import cv2
import numpy as np
import queue
import pygame
import pygame_menu
import transformation as transf
import socket
import Highscores as highscore

sys.path.append('balldetection')
sys.path.append('interface')


class CowboyGame:
    def __init__(self):

        self.isGameOver = False
        self.paused = False
        self.isLoggedIn = False

        self.interface = GameInterface()
        self.cap = None
        self.camCalibration = CameraCalibration()
        self.ballDetector = DetectBallPosition()
        self.positionQueue = queue.Queue(5)
        self.loginUsername = ""
        self.loginPassword = ""
        self.current_user = ""
        self.score = 0
        self.trials = 0

        self.cowCount = 0
        self.cowBoyCount = 0
        self.loginErrorMessage = None
        self.registerErrorMessage = None

        self.UDP_IP = "192.168.137.1"
        self.UDP_PORT = 5005

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.sock.setblocking(0)

    ################################################################################
    ####                               REDIRECT FUNCTIONS                          #
    ################################################################################
    def start(self):
        self.interface.startScreen = self.interface.drawStartScreen()
        self.interface.startScreen.add.button('Go to Login', self.goToLogin())
        return self.interface.startScreen

    def goToLogin(self):
        self.interface.loginScreen = self.interface.drawLoginScreen()
        self.interface.loginScreen.add.button('   Login    ', self.login)
        self.interface.loginScreen.add.button(
            '  Register  ', self.goToRegister())
        self.loginErrorMessage = self.interface.loginScreen.add.label(
            "Login Failed", background_color=(0, 0, 0, 0))
        self.loginErrorMessage.hide()
        return self.interface.loginScreen

    def goToRegister(self):
        self.interface.registerScreen = self.interface.drawRegisterScreen()
        self.interface.registerScreen.add.button(
            '   Register  ', self.register)
        self.interface.registerScreen.add.button(
            'Back to login', pygame_menu.events.BACK)
        self.registerErrorMessage = self.interface.registerScreen.add.label(
            "Register Successfully", background_color=(0, 0, 0, 0))
        self.registerErrorMessage.hide()
        return self.interface.registerScreen

    def goToMain(self):
        self.interface.mainMenuScreen = self.interface.drawMainMenuScreen()
        self.interface.mainMenuScreen.add.button(
            '      Play      ', self.game_loop)
        self.interface.mainMenuScreen.add.button(
            'Leaderboard', self.goToLeaderBoard())
        self.interface.mainMenuScreen.add.button(
            '     Logout     ', self.start())
        return self.interface.mainMenuScreen

    def goToLeaderBoard(self):
        self.interface.leaderBoardScreen = self.interface.drawLeaderBoard()
        self.interface.leaderBoardScreen.add.button(
            '   Back   ', pygame_menu.events.BACK)
        return self.interface.leaderBoardScreen

    def goToPause(self):
        self.interface.pauseScreen = self.interface.drawPauseScreen()
        self.interface.pauseScreen.add.button('  Continue  ', self.un_pause)
        self.interface.pauseScreen.add.button(
            'Leaderboard', self.goToLeaderBoard())
        self.interface.pauseScreen.add.button('  Quit Game  ', self.game_over)
        return self.interface.pauseScreen

    def goToGameOver(self):
        self.interface.gameOverScreen = self.interface.drawGameOver()
        self.interface.gameOverScreen.add.label(
            "Your Score: " + str(self.score), background_color=(0, 0, 0, 0))
        self.interface.gameOverScreen.add.button(
            '  Play Again  ', self.game_loop)
        self.interface.gameOverScreen.add.button(
            ' Leaderboard', self.goToLeaderBoard())
        self.interface.gameOverScreen.add.button(
            ' Back to Main ', self.goToMain())
        return self.interface.gameOverScreen

    ##################################################################
    #                           GAME FUNCTIONS                       #
    ##################################################################

    def login(self):
        if self.loginErrorMessage in self.interface.loginScreen.get_widgets():
            self.interface.loginScreen.remove_widget(self.loginErrorMessage)
        login_input = self.interface.loginScreen.get_input_data(
            recursive=False)
        login_status = security.login(
            login_input['username'], login_input['password'])
        if login_status:
            self.current_user = login_input['username']
            self.isLoggedIn = True
            self.logged_in()
        else:
            self.loginErrorMessage = self.interface.loginScreen.add.label(
                "Login Failed", background_color=(0, 0, 0, 0))

    def register(self):
        if self.registerErrorMessage in self.interface.registerScreen.get_widgets():
            self.interface.registerScreen.remove_widget(
                self.registerErrorMessage)
        register_input = self.interface.registerScreen.get_input_data(
            recursive=False)
        register_status = security.register(register_input['username'],
                                            register_input['password'],
                                            register_input['password2'])
        if register_status[0]:
            self.registerErrorMessage = self.interface.registerScreen.add.label(
                "Register Successful!", background_color=(0, 0, 0, 0))
        else:
            self.registerErrorMessage = self.interface.registerScreen.add.label(
                str(register_status[1]), background_color=(0, 0, 0, 0))

    def logged_in(self):
        mainMenuScreen = self.goToMain()
        mainMenuScreen.enable()
        while self.isLoggedIn:
            self.interface.draw_background()
            self.updateScreen(mainMenuScreen)

    def pause(self):
        self.paused = True
        pauseScreen = self.goToPause()
        pauseScreen.enable()
        while self.paused:
            self.updateScreen(pauseScreen)

    def un_pause(self):
        self.paused = False

    def game_over(self):
        self.isGameOver = True

        highscore.storingscores(self.current_user, self.score)

        gameOverScreen = self.goToGameOver()
        gameOverScreen.enable()
        while True:
            self.interface.draw_background()
            self.updateScreen(gameOverScreen)

    def updateScreen(self, screen):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.paused = False
                elif event.key == pygame.K_p:
                    pygame.quit()
                    quit()
        if screen.is_enabled():
            screen.update(events)
            screen.draw(self.interface.gameDisplay)
        pygame.display.update()

    def updateBallPos(self):
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (1280, 720))
        cv2.flip(frame, 1)
        if self.camCalibration.counter == 4:
            width, height = 1280, 720
            point1 = np.float32([self.camCalibration.circles[0], self.camCalibration.circles[1],
                                self.camCalibration.circles[2], self.camCalibration.circles[3]])
            # point2 = np.float32(
            #     [[0, 0], [width, 0], [0, height], [width, height]])
            # matrix = cv2.getPerspectiveTransform(point1, point2)
            # imgOut = cv2.warpPerspective(frame, matrix, (1280, 720))
            # cv2.imshow("dasj", imgOut)
            if (self.ballDetector.getBallPos(frame) is not None):
                x, y, r = self.ballDetector.getBallPos(frame)
                inp = np.array([x, y])
                a = transf.transform(point1, 1280, 720, inp)
                if not self.positionQueue.full():
                    self.positionQueue.put((a[0], a[1], r))
                else:
                    self.positionQueue.get()
                    self.positionQueue.put((a[0], a[1], r))
        for x in range(0, 4):
            cv2.circle(frame, (self.camCalibration.circles[x][0], self.camCalibration.circles[x][1]),
                       3, (0, 255, 0), cv2.FILLED)
        cv2.imshow("original", frame)
        cv2.setMouseCallback("original", self.camCalibration.mousePoints)
        cv2.waitKey(10)

# Game score calculation and objecs removal/generation logic
    def hitting(self, hit):
        if isinstance(hit, cowBoyObject):
            self.score += 1
            self.cowBoyCount -= 1

        elif isinstance(hit, cowObject):
            if self.score > 0:
                self.score -= 1
                self.cowCount -= 1
            self.trials -= 1
        else:
            self.trials -= 1

    def generateObjects(self, target_group):
        while len(target_group) < 5:
            if self.cowBoyCount < 2:
                new_target = cowBoyObject()
                hits = pygame.sprite.spritecollide(
                    new_target, target_group, False)
                if len(hits) > 0:
                    continue
                else:
                    target_group.add(new_target)
                    self.cowBoyCount += 1
            elif self.cowCount < 2:
                new_target = cowObject()
                hits = pygame.sprite.spritecollide(
                    new_target, target_group, False)
                if len(hits) > 0:
                    continue
                else:
                    target_group.add(new_target)
                    self.cowCount += 1
            else:
                new_target = random.choice([cowBoyObject(), cowObject()])
                hits = pygame.sprite.spritecollide(
                    new_target, target_group, False)
                if len(hits) > 0:
                    continue
                else:
                    target_group.add(new_target)
                    if isinstance(new_target, cowObject):
                        self.cowCount += 1
                    else:
                        self.cowBoyCount += 1
    
    def setupNewGameLoop(self):
        self.trials = TRIALS
        self.score = 0
        self.cowBoyCount = 0
        self.cowCount = 0

    def game_loop(self):
        inGame = True
        self.setupNewGameLoop()

        player = Player()
        player_group = pygame.sprite.Group()
        player_group.add(player)
        target_group = pygame.sprite.Group()
        dot_group = pygame.sprite.Group()

        ball = BallSprite()

        self.cap = cv2.VideoCapture(0)

        while inGame:

            self.generateObjects(target_group)

            if (self.getBallBounce()):
                ballBounceEvent = pygame.event.Event(
                    pygame.USEREVENT, customType=1)
                pygame.event.post(ballBounceEvent)

            self.updateBallPos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.type == pygame.K_p:
                    self.pause()

                #  # temporary event, to be replaced with signal?
                elif event.type == pygame.USEREVENT and event.customType == 1:
                    #     # get position of last member in queue
                    #     # check sprite collide.
                    # print(list(self.positionQueue.queue))
                    if not self.positionQueue.empty():
                        # print(self.positionQueue.queue[-1])
                        # minRPos = -1
                        # minR = 100
                        # print("Radius")
                        # for i in range(1,2):
                        #     print(self.positionQueue.queue[i][2])
                        #     dt = dot(self.positionQueue.queue[i][0], self.positionQueue.queue[i][1], i)
                        #     dot_group.add(dt)
                        #     if self.positionQueue.queue[i][2] < minR:
                        #         minR = self.positionQueue.queue[i][2]
                        #         minRPos = i
                        # print("End Radius")
                        prefferedPos = min(len(self.positionQueue.queue)-1, 1)
                        ball.update(
                            self.positionQueue.queue[prefferedPos][0], self.positionQueue.queue[prefferedPos][1])
                        self.positionQueue.queue.clear()

                        hits = pygame.sprite.spritecollide(
                            ball, target_group, True)
                        if len(hits) == 0:
                            self.trials -= 1
                        else:
                            for hit in hits:
                                self.hitting(hit)
                #     # TODO - Remove the BallHit Sprite which is collide in queue
                #     # TODO - Checking the objects collision of target_group to update score

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    hits = pygame.sprite.spritecollide(
                        player, target_group, True)

                    for hit in hits:
                        self.hitting(hit)
            # display background
            self.interface.draw_background()
            # show Title
            self.interface.show_text(
                460, 50, "Ball on the Wall", 55, COLORS["BLACK"])
            # show score box
            self.interface.show_text(
                1000, 120, "My Score: " + str(self.score), hasBox=True)
            # show trials counter
            if self.trials > 0:
                self.interface.show_text(
                    120, 120, "Trials No: " + str(self.trials), hasBox=True)
            else:
                target_group.empty()
                with self.positionQueue.mutex:
                    self.positionQueue.queue.clear()

                cv2.destroyAllWindows()
                self.game_over()

            target_group.update()
            target_group.draw(self.interface.gameDisplay)
            player_group.update()
            dot_group.update()
            dot_group.draw(self.interface.gameDisplay)
            # player.update()
            # self.ballHit_group.update()

            pygame.display.flip()

    def getBallBounce(self):
        try:
            data = self.sock.recv(1024)
        except socket.error as e:
            return False
        return True


#--------#
# NOTES:
#------------------------------------------#
# When the ball is detected hit:
# - Create a sprite list for all ball hits
# - Adding it to the Sprite group
#
# - Post the Event to pygame.event
#------------------------------------------#

class dot(pygame.sprite.Sprite):
    def __init__(self, posX, posY, num):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(PATH.joinpath(
            "img/dot"+str(num+1)+".png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.x = posX
        self.y = posY
        self.rect = self.image.get_rect(center=(self.x, self.y))
