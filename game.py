import pygame, sys
from player import Player
from balloons import GaussianBalloons, UniformBalloons, LimitBalloons, GeometricBalloons
import argparse
# from datetime import date
from pygame.locals import *
from numpy import random

# TODO: start button, time stamp, add balloon 9 on game screen
parser = argparse.ArgumentParser()
parser.add_argument("--name", default= "PENROLINE", required=True)
parser.add_argument("--gender", default = "IDK", required=True)
parser.add_argument("--age", type=int, default = 20, required=True)
parser.add_argument("--balloons", type=int, default = 10, required=True)
parser.add_argument("--course", type=int, default = 6, required=True)
args = parser.parse_args()

N = args.balloons

#distirbutions and number of variables
DISTS = ["GAUSSIAN", "UNIFORM", "GEOMETRIC", "LIMIT"]
distribution = random.choice(DISTS)

player = Player(args.name, args.gender, args.age, args.balloons, args.course, )

balloons = None
if distribution == 'GAUSSIAN':
    balloons = GaussianBalloons(N)
elif distribution == 'UNIFORM':
    balloons = UniformBalloons(N)
elif distribution == 'LIMIT':
    balloons = LimitBalloons(N)
elif distribution == 'GEOMETRIC':
    balloons = GeometricBalloons(N)
else:
    raise Exception("no distribution found ;-;???")

B = balloons.getBallons()
print(B)

# Game Part

# TODO: save data 

pygame.init()
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600
BALLOON_SIZE = 20
DISPLAYSURF = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption('Balloon Game!')
 
total_score = 0
currBalloonIdx = 0
numberBalloons = balloons.N

curr_pumps = 0 # aka player score
lastKeyPressed = 0
timeDelay = 2000 # wait 0.2 seconds between key presses

BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

# https://www.geeksforgeeks.org/python-display-text-to-pygame-window/

while currBalloonIdx < numberBalloons: # main game loop
    max_pumps = B[currBalloonIdx]

    font = pygame.font.Font('freesansbold.ttf', 32)
    # score text
    currScoreTxt = font.render('This Balloon: ' + str(curr_pumps), True, RED, WHITE)
    currScoreRect = currScoreTxt.get_rect()
    totalScoreTxt = font.render('Total Earned: ' + str(total_score), True, BLUE, WHITE)
    totalScoreRect = totalScoreTxt.get_rect()
    totalScoreRect.center = (2 * SCREEN_WIDTH / 3, SCREEN_HEIGHT / 50)

    # instruction text
    upKeyText = font.render('Up: Collect $', True, BLACK, WHITE)
    upKeyRect = upKeyText.get_rect()

    rightKeyText = font.render('Press right to pump', True, BLACK, WHITE)
    rightKeyRect = upKeyText.get_rect()

    rightKeyRect.center = (8.5*SCREEN_WIDTH/50, 5 * SCREEN_HEIGHT / 50)
    upKeyRect.center = (2.3 * SCREEN_WIDTH / 3, 5 * SCREEN_HEIGHT / 50)


    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            # record data
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT: # INC BALLOON SIZE
            # and pygame.time.get_ticks() - lastKeyPressed > timeDelay
            lastKeyPressed = pygame.time.get_ticks()
            curr_pumps += 1

            print("MAX PUMPS")
            print(max_pumps)
            print("CURR BALLOON")
            print(currBalloonIdx)
            print("CURR PUMPS")
            print(curr_pumps)

            if curr_pumps == max_pumps: # BALLOON POPS 
                # TODO - add time since last action / timestamp, going from start
                # player.addActionData(currBalloonIdx, curr_pumps, "POP", ?) # TODO - what should size be
                curr_pumps = 0 # reset current score
                BALLOON_SIZE = 20 # reset to initial size
                currBalloonIdx+=1

            else: # PUMP BALLOON 
                BALLOON_SIZE += 5
                # player.addActionData(currBalloonIdx, curr_pumps, "PUMP", ?)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP: # NEXT BALLOON
            # player.addActionData(currBalloonIdx, curr_pumps, "PASS", ?)
            lastKeyPressed = pygame.time.get_ticks()
            total_score += curr_pumps
            curr_pumps = 0
            BALLOON_SIZE = 20 # reset to initial size
            currBalloonIdx+=1

        DISPLAYSURF.fill(WHITE)  # white background
        DISPLAYSURF.blit(currScoreTxt, currScoreRect)
        DISPLAYSURF.blit(totalScoreTxt, totalScoreRect)
        DISPLAYSURF.blit(rightKeyText, rightKeyRect)
        DISPLAYSURF.blit(upKeyText, upKeyRect)

        if currBalloonIdx % 2 == 0: # have color alternate between conseq. balloons
            pygame.draw.circle(DISPLAYSURF, BLUE, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), BALLOON_SIZE)
        else:
            pygame.draw.circle(DISPLAYSURF, RED, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), BALLOON_SIZE)

        pygame.display.update()

player.writeData()