# MOD 5 - Project Team 30: Ball On the Wall
![Game Background](/src/img/newbg.jpg)

### Team members:
- Ho Hoang Phuoc
- Jan van Zwol
- Tran Duc Duc
- Daan Velthuis
- Marjolein Bolten
- Vo Nhat Minh

# I. Abstractions - Project Overview:
---
<p>
TODO - write down some overview about the project in here
</p>
<br/>

# II. Hardware - Installations:
---
## 1. RasberryPi: 
> - 2 x RaspberryPi 4 Model B (4GB RAM/8GB RAM)
> - 2 x SD Card (32GB)

- To set up for RaspberryPi, follow the following link:
    > [Setting up RaspberryPi](https://automaticaddison.com/how-to-install-ubuntu-and-raspbian-on-your-raspberry-pi-4/)

- After setting up, using ```sudo reboot``` to reboot the Pi. 
---

## 2. Cameras:
> 1 x PiCamera V2 (side camera): 
- `Usage:` Use for detecting ball bounce
- To set up for the camera, follow the following link:
  > [Install and setup Camera Module](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
- To Configure Raspberry Pi camera, we use:
    ```
    sudo raspi-config
    ```
    - Go to **Interfacing Options** and press **Enter**.
    - Select **Camera** and press **Enter** to enable the camera
- Change the `resolution`, go to **Advanced Options**, select a suitable screen resolution and press **Enter**.

> 1 x Computer Webcam(front camera): 
- `Usage:` Use for calibrate the screen and detect the position of the ball on screen.
------

# III. Software and External Library:

## 1. Prerequisites:
- Fistly, make sure the Pi has been updated and upgraded all required packages. We check it by using:
    ```
    sudo apt update
    sudo apt upgrade
    ```
## 2. Install Python3 and Python packages:
- To install python in Raspberry Pi, use:
    ```
    sudo apt install python3
    ```
- Then, check the pip version and python version using:
    ```
    python3 --version
    pip3 --version
    ```
    > **Notes**: Make sure the *`python version is 3.7.7 or greater`*
- Upgrade pip3 to the latest version, using:
    ```
    sudo -H pip3 install --upgrade pip
    ```
### 2.1. Install Bcrypt :
- `Bcrypt` is a Python package, used for hashing the input password of the user before sending to the database.

- To install Bcrypt in Pi, use:
  ```
  pip3 install bcrypt
  ```
### 2.2. Install Psycopg2:
- `Psycopg2` is a Python package used for connecting Python with the database, so that user data can be store and updated in the database.

- To install `Psycopg2`, use:
    ```
    pip3 install psycopg2
    ```
### 2.3. Install Coverage:
- `Coverage` is a Python package, which used for unit testing and checking code coverage.
- To install `Coverage`, use:
    ```
    pip3 install coverage
    ```
### 2.4. Install Pygame and pygame_menu:
- `Pygame` is a python library, which is used for creating a game with Python. To install `Pygame`, use:
    ```
    pip3 install pygame
    ```
- `Pygame_menu` is used for creating pygame interfaces, as well as creating some menu screen for triggering events. To install `Pygame_menu`, use:
    ```
    pip3 install pygame_menu
    ```
## 3. Install OpenCV:
- To `install OpenCV` and `Set up Real-time Video for OpenCV`, we follow the instruction from the link:

    - [Install OpenCV](https://pimylifeup.com/raspberry-pi-opencv/)

    - [Set Up Real-Time Video Using OpenCV](https://automaticaddison.com/how-to-set-up-real-time-video-using-opencv-on-raspberry-pi-4/)
---
# IV. Gameplay

## 1. Setup the Game

- Firstly, we need to set up 2 cameras to the correct position:
  - Side camera (PiCamera): set to the side of screen
  - Front camera(Webcam): set to the front of the screen, where it can see the entire screen.

- Then, connect 2 cameras via an ethernet cable so that it will transmiting the signal to each other.

## 2. Login and Play:

### a) Login and Register:
  - To play the game, first user need to login/register via the register page.
  - Once the user has logged in, click play to start the game 
### b) Play the game:
  - In order to play the game:
    -  Firstly, `connect with a projector`: which will show the game screen
    -  Secondly, `calibrating the screen`: choosing 4 point of game screen clockwise for calibration
    -  Then, `prepare a ball` to throw.

The demo of how to set up and play the game is in the following link:
[Ball on the Wall - Setup & Gameplay](https://youtu.be/AxwdQX19n3s)

# V. Testing with coverage
## 1. Setup

- First, we need to disable (comment out) the UDP and IP address in game.py line 52-27 and the condition if (self.getBallBounce()) in game.py line 298

## 2. Run test
- Use command ```coverage run automated_test.py``` to run the test

## 3. Test report
- Use command ```coverage report -i``` after running the test to see the test's report