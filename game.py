import pygame, sys
from player import Player
from balloons import GaussianBalloons, UniformBalloons, LimitBalloons, GeometricBalloons
import argparse
# from datetime import date
from pygame.locals import *
from numpy import random


parser = argparse.ArgumentParser()
parser.add_argument("--name", default= "PENROLINE", required=False)
parser.add_argument("--gender", default = "IDK", required=False)
parser.add_argument("--age", type=int, default = 20, required=False)
parser.add_argument("--balloons", type=int, default = 10, required=False)
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


# Game Part

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')


while True: # main game loop
    for event in pygame.event.get():
         if event.type == QUIT:
            pygame.quit()
            #record data
            sys.exit()
    pygame.display.update()