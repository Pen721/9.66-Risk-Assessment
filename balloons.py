import math
import numpy as np
import random
from numpy import random

#distirbutions and number of variables
DIST = {'Gaussian': 2, 'Uniform': 2, 'Constant': 1, 'Geometric': 1}

class Balloons:
    def __init__(N = 10):
        self.N = N
        #ok maybe I should move this to out of here woops to make subclasses work
        self.distribution = random.choice(DIST.keys())
        self.current_balloon = 0
        self.max = 10
        self.min = 0

    def update(action):
        '''returns whether balloon has popped'''

    #gaussain will be cut off
    def 

class GuassianBalloon(Balloons):
    def __init__(N = 10):
        super().__init__(N)
        self.mean = random.randint(self.min, self.max)
        self.var = random.randint(3 * self.max)
        self.std = math.sqrt(self.var)
        
    def dist(x):
        return 1.0/ (self.std * math.sqrt(2 * math.pi)) * math.e ** (-1 * (x - self.m)**2 / (2 * self.var))


        
