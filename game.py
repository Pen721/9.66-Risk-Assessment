import pygame, sys
import player
import balloon
import argparse
# from datetime import date
from pygame.locals import *


parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--gender", required=True)
parser.add_argument("--age", type=int, required=True)
args = parser.parse_args()
# today = date.today()

player = player(args.name, args.gender, args.age)
balloons = 



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