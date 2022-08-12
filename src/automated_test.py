import unittest
import time
import numpy as np
import cv2
from unittest import result
from unittest.result import TestResult
from CameraCalibration import CameraCalibration
from security import *
from Highscores import *
from transformation import transform
import random
from cow import cowObject
from cowboy import cowBoyObject
from ball import BallSprite
from game import CowboyGame
import pygame
from DetectBallBounce import Ball
from pygame.sprite import Sprite

class TestSecurity(unittest.TestCase):
    def test_hashed_password(self):
        encode_plain_text = str("Minh").encode('utf-8')
        # Password shouldn't contain plaintext
        res = get_hashed_password(encode_plain_text)
        self.assertEqual("Minh" not in str(res), True)
        # Same password should have different hashed values because of salt
        res2 = get_hashed_password(encode_plain_text)
        self.assertNotEqual(res, res2)

    def test_password_check(self):
        password = "abcd"
        res = password_check(password)
        self.assertEqual(res, "Your password has less than 8 characters")
        password = "abcd1234"
        res = password_check(password)
        self.assertEqual(res, "Your password should have \n at least 1 symbol")
        password = "!abcdabcd"
        res = password_check(password)
        self.assertEqual(res, "Your password should have \n at least 1 digit")
        password = "!abcd1234"
        res = password_check(password)
        self.assertEqual(res, "Your password should have \n at least 1 uppercase")
        password = "!ABCD1234"
        res = password_check(password)
        self.assertEqual(res, "Your password should have \n at least 1 lowercase")
        password = "!Abcd1234"
        res = password_check(password)
        self.assertEqual(res, "Good password")
    
    def test_login_take2s(self):
        start = time.time()
        res = login("Daan", "Qwerty12!")
        end = time.time()
        t = end - start
        print(t)
        check = False
        if (t > 1.8):
            check = True
        self.assertEqual(check, True)

class TestLogin(unittest.TestCase):
    def test_login_with_correct_password(self):
        res = login("Daan", "Qwerty12!")
        self.assertEqual(res, True)
    
    def test_login_with_incorrect_password(self):
        res = login("Daan", "werty12!")
        self.assertEqual(res, False)
    
    def test_login_with_not_exist_username(self):
        res = login("ABMNBSMA", "werty12!")
        self.assertEqual(res, False)

class TestRegister(unittest.TestCase):
    def test_register_with_duplicated_username(self):
        username = "Daan"
        res, mess = register(username, "Qwerty12!", "Qwerty12!")
        self.assertEqual(res, False)
        self.assertEqual(mess, "Username already exists")

    def test_register_with_incorect_confirmpassword(self):
        username = "Daan"
        res, mess = register(username, "Qwerty12!", "Qwerty1!")
        self.assertEqual(res, False)
        self.assertEqual(mess, "Confirm password doesn't match")

    def test_register_with_new_username(self):
        username = "TestUser" + str(random.randint(0,1000))
        res, mess = register(username, "Qwerty12!", "Qwerty12!")
        self.assertEqual(res, True)
        self.assertEqual(mess, "Register successfully")

    def test_register_with_new_username(self):
        username = "TestUser" + str(random.randint(0,1000))
        res, mess = register(username, "Qwerty12!", "Qwerty12!")
        self.assertEqual(res, True)
        self.assertEqual(mess, "Register successfully")
    
class TestLeaderboard(unittest.TestCase):
    def test_high_scores(self):
        storingscores("Daan", 9999)
        scores = gethighscores()
        check = False
        for n in range(len(scores)):
            username = scores[n][1] 
            score = scores[n][0]
            if (username == "Daan") and (score == 9999):
                check = True
        self.assertEqual(check, True)

class TestHardwareSetup(unittest.TestCase):
    def test_transform(self):
        inputP = np.array([500, 500])
        cornerA = np.array([300, 400])
        cornerB = np.array([600, 350])
        cornerC = np.array([580, 730])
        cornerD = np.array([290, 700])
        corners = [cornerA, cornerB, cornerC, cornerD]
        result = transform(corners, 1280, 720, inputP)
        self.assertEqual(result[0], 880.9501187648458)
        self.assertEqual(result[1], 270.3787633538361)

    def test_camera_calibration(self):
        cc = CameraCalibration()
        self.assertEqual(cc.counter, 0)
        cc.mousePoints(cv2.EVENT_LBUTTONDOWN,1,2, 0, 0)
        self.assertEqual(cc.counter, 1)
    
    def test_detect_ball_bounce_setup(self):
        ball = Ball()
        ball.newX(None)
        self.assertEqual(ball.lived(), False)


class TestGameLogic(unittest.TestCase):
    def test_hitting_cowBoy(self):
        game = CowboyGame()
        cowBoy = cowBoyObject()
        game.hitting(cowBoy)
        self.assertEqual(game.score, 1)
        game.hitting(cowBoy)
        self.assertEqual(game.score, 2)
    
    def test_hitting_cow(self):
        game = CowboyGame()
        cow = cowObject()
        game.score = 5
        game.hitting(cow)
        self.assertEqual(game.score, 4)
        game.hitting(cow)
        self.assertEqual(game.score, 3)
        game.score = 0
        game.hitting(cow)
        self.assertEqual(game.score, 0)
    
    def test_trial_when_hitting_cowBoy(self):
        game = CowboyGame()
        game.trials = 10
        
        # trials remain if hitting cowBoy
        cowBoy = cowBoyObject()
        game.hitting(cowBoy)
        self.assertEqual(game.trials, 10)

    def test_trial_when_hitting_cow(self):
        game = CowboyGame()
        game.trials = 10

        # trials reduce if hitting cow
        cow = cowObject()
        game.hitting(cow)
        self.assertEqual(game.trials, 9)
        game.hitting(cow)
        self.assertEqual(game.trials, 8)
    
    def test_object_generation_if_equal_five(self):
        game = CowboyGame()
        target_group = pygame.sprite.Group()
        self.assertEqual(game.cowBoyCount, 0)
        self.assertEqual(game.cowCount, 0)
        game.generateObjects(target_group)
        self.assertEqual(game.cowBoyCount + game.cowCount, 5)
    
    def test_object_generation_if_cowBoy_less_than_two(self):
        game = CowboyGame()
        target_group = pygame.sprite.Group()
        cow = cowObject()
        target_group.add(cow)
        target_group.add(cow)
        game.cowCount = 2
        self.assertEqual(game.cowBoyCount, 0)
        self.assertEqual(game.cowCount, 2)
        game.generateObjects(target_group)
        check = False
        if (game.cowBoyCount >= 2):
            check = True
        self.assertEqual(check, True)
    
    def test_object_generation_if_cow_less_than_two(self):
        game = CowboyGame()
        target_group = pygame.sprite.Group()
        cowBoy = cowBoyObject()
        target_group.add(cowBoy)
        target_group.add(cowBoy)
        game.cowBoyCount = 2
        self.assertEqual(game.cowBoyCount, 2)
        self.assertEqual(game.cowCount, 0)
        game.generateObjects(target_group)
        check = False
        if (game.cowCount >= 2):
            check = True
        self.assertEqual(check, True)
    
    def test_setupgameloop(self):
        game = CowboyGame()
        game.setupNewGameLoop()
        self.assertEqual(game.score, 0)
        self.assertEqual(game.cowCount, 0)
        self.assertEqual(game.cowBoyCount, 0)

class TestOOP(unittest.TestCase):
    def test_ball(self):
        ball = BallSprite()
        ball.update(1,2)
        self.assertEqual(ball.rect.center, (1,2))
    
    def test_cowboy_setpos(self):
        cowBoy = cowBoyObject()
        cowBoy.setPos(1,2)
        self.assertEqual(cowBoy.x, 1)
        self.assertEqual(cowBoy.y, 2)
    
    def test_cow_setpos(self):
        cow = cowObject()
        cow.setPos(1,2)
        self.assertEqual(cow.x, 1)
        self.assertEqual(cow.y, 2)

if __name__ == '__main__':
    unittest.main()