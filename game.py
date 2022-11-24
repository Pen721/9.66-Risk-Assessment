import pygame, sys
import player
from balloons import GaussianBalloons, UniformBalloons, LimitBalloons, GeometricBalloons
import argparse
# from datetime import date
from pygame.locals import *


parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--gender", required=True)
parser.add_argument("--age", type=int, required=True)
parser.add_argument("--balloons", type=int, required=True)
args = parser.parse_args()

N = args.balloons

#distirbutions and number of variables
DISTS = ["GAUSSIAN", "UNIFORM", "GEOMETRIC", "LIMIT"]
distribution = random.choice(DISTS)

player = player(args.name, args.gender, args.age)

balloons = None
if distribution == 'GAUSSIAN':
    balloons = GaussianBalloons(N)
elif distribution == 'UNIFORM':
    balloons = UniformBalloons(N)
elif distribution == 'LIMIT':
    balloons = LimitBalloons(N)
elif distribution == 'GEOMETRIC':
    balloons = LimitBalloons(N)
else:
    raise Exception("no distribution found ;-;???")

B = balloons.getBallons()

# Game Part

# pygame.init()
# DISPLAYSURF = pygame.display.set_mode((400, 300))
# pygame.display.set_caption('Hello World!')


# while True: # main game loop
#     for event in pygame.event.get():
#          if event.type == QUIT:
#             pygame.quit()
#             #record data
#             sys.exit()
#     pygame.display.update()