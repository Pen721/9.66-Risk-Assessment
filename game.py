import pygame, sys
from player import Player
from balloons import GaussianBalloons, UniformBalloons, LimitBalloons, GeometricBalloons
import argparse
# from datetime import date
from pygame.locals import *
from numpy import random

# TODO: start button on game screen
parser = argparse.ArgumentParser()
parser.add_argument("--name", default= "PENROLINE", required=True)
parser.add_argument("--gender", default = "IDK", required=True)
parser.add_argument("--age", type=int, default = 20, required=True)
parser.add_argument("--balloons", type=int, default = 10, required=True)
parser.add_argument("--course", type=int, default = 6, required=True)
parser.add_argument("--lossAversion", default = "False", required=True)
args = parser.parse_args()

N = args.balloons

#distirbutions and number of variables
DISTS = ["GAUSSIAN", "UNIFORM", "GEOMETRIC", "LIMIT"]
distribution = random.choice(DISTS)


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

player = Player(args.name, args.age, args.gender, args.course, balloons)
player.addDistributionData()
# Game Part

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

lastTimePressed = pygame.time.get_ticks()

# add START condition here 

lastTimePressed = pygame.time.get_ticks()

while currBalloonIdx < numberBalloons: # main game loop

    if currBalloonIdx % 2 == 0: # have color alternate between conseq. balloons
        BALLOON_COLOR = BLUE
    else:
        BALLOON_COLOR = RED

    max_pumps = B[currBalloonIdx]

    font = pygame.font.Font('freesansbold.ttf', 32)
    # score text
    currBalloonTxt = font.render('On Balloon #: ', True, RED, WHITE)
    currBalloonRect = currBalloonTxt.get_rect()

    currBalloonNumber = font.render(str(currBalloonIdx+1), True, BALLOON_COLOR, WHITE)
    currNumberRect = currBalloonNumber.get_rect()
    currNumberRect.center = (1.15 * SCREEN_WIDTH / 3, SCREEN_HEIGHT / 50)

    currScoreTxt = font.render('Pumps: $' + str(curr_pumps), True, BLUE, WHITE)
    currScoreRect = currScoreTxt.get_rect()
    currScoreRect.center = (1.7 * SCREEN_WIDTH / 3, SCREEN_HEIGHT / 50)

    if args.lossAversion.lower() == "false":
        totalPointsDisplayed = total_score
    else:
        totalPointsDisplayed = total_score+curr_pumps
    totalScoreTxt = font.render('Total Earned: $' + str(totalPointsDisplayed), True, RED, WHITE)
    totalScoreRect = totalScoreTxt.get_rect()
    totalScoreRect.center = (8.75 * SCREEN_WIDTH / 9, SCREEN_HEIGHT / 50)

    # instruction text
    upKeyText = font.render('Press X to Collect $', True, BLACK, WHITE)
    upKeyRect = upKeyText.get_rect()

    rightKeyText = font.render('Press space to pump', True, BLACK, WHITE)
    rightKeyRect = rightKeyText.get_rect()

    rightKeyRect.center = (15*SCREEN_WIDTH/50, SCREEN_HEIGHT / 10)
    upKeyRect.center = (7 * SCREEN_WIDTH / 8, SCREEN_HEIGHT / 10)

    for event in pygame.event.get():
        currKeyPressed = pygame.time.get_ticks()

        if event.type == QUIT: 
            pygame.quit()
            # record data
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # INC BALLOON SIZE
            curr_pumps += 1

            print("MAX PUMPS")
            print(max_pumps)
            print("CURR BALLOON")
            print(currBalloonIdx)
            print("CURR PUMPS")
            print(curr_pumps)

            if curr_pumps == max_pumps: # BALLOON POPS 
                player.addActionData(currBalloonIdx, curr_pumps, "POP", currKeyPressed-lastKeyPressed, totalPointsDisplayed) 
                curr_pumps = 0 # reset current score
                BALLOON_SIZE = 20 # reset to initial size
                currBalloonIdx+=1

            else: # PUMP BALLOON 
                BALLOON_SIZE += 5
                player.addActionData(currBalloonIdx, curr_pumps, "PUMP", currKeyPressed-lastKeyPressed, totalPointsDisplayed)

            lastKeyPressed = currKeyPressed # update logics

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x: # NEXT BALLOON
            player.addActionData(currBalloonIdx, curr_pumps, "PASS", currKeyPressed-lastKeyPressed, totalPointsDisplayed)
            lastKeyPressed = pygame.time.get_ticks()
            total_score += curr_pumps
            curr_pumps = 0
            BALLOON_SIZE = 20 # reset to initial size
            currBalloonIdx+=1
        
            lastKeyPressed = currKeyPressed # update logics

        DISPLAYSURF.fill(WHITE)  # white background
        DISPLAYSURF.blit(currBalloonTxt, currBalloonRect)
        DISPLAYSURF.blit(currBalloonNumber, currNumberRect)
        DISPLAYSURF.blit(currScoreTxt, currScoreRect)
        DISPLAYSURF.blit(totalScoreTxt, totalScoreRect)
        DISPLAYSURF.blit(rightKeyText, rightKeyRect)
        DISPLAYSURF.blit(upKeyText, upKeyRect)

        pygame.draw.circle(DISPLAYSURF, BALLOON_COLOR, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), BALLOON_SIZE)

        pygame.display.update()

player.writeData()
player.writeStringToData("TOTAL SCORE {}".format(total_score))