import pygame, sys
from player import Player
from balloons import GaussianBalloons, UniformBalloons, LimitBalloons, GeometricBalloons
import argparse
# from datetime import date
from pygame.locals import *
from numpy import random


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

player = Player(args.name, args.gender, args.age)

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

pygame.init()
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 300
BALLOON_SIZE = 20
DISPLAYSURF = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption('Hello World!')
 
total_score = 0
currBalloonIdx = 0
numberBalloons = balloons.N

curr_pumps = 0 # aka player score
lastKeyPressed = 0
timeDelay = 2000 # wait 0.2 seconds between key presses

while currBalloonIdx < numberBalloons: # main game loop
    max_pumps = B[currBalloonIdx]
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            # record data
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT: # INC BALLOON SIZE
            print("MAX PUMPS")
            print(max_pumps)
            # and pygame.time.get_ticks() - lastKeyPressed > timeDelay
            lastKeyPressed = pygame.time.get_ticks()
            curr_pumps += 1

            if curr_pumps == max_pumps: # BALLOON POPS 
                curr_pumps = 0
                BALLOON_SIZE += 5

            else: # PUMP BALLOON 
                BALLOON_SIZE = 20 # reset to initial size
                currBalloonIdx+=1

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP: # NEXT BALLOON
            lastKeyPressed = pygame.time.get_ticks()
            total_score += curr_pumps
            curr_pumps = 0
            BALLOON_SIZE = 20 # reset to initial size
            currBalloonIdx+=1

        DISPLAYSURF.fill((255, 255, 255))  # white background
        pygame.draw.circle(DISPLAYSURF, (0, 0, 255), (SCREEN_HEIGHT/2, SCREEN_WIDTH/2), BALLOON_SIZE)

        pygame.display.update()
