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
        self.probs = [-1] * (self.max - self.min)

    def update(action):
        '''returns whether balloon has popped'''

    def getprobs():
        for i in range(self.min, self.max):
            n = 50
            prob = 0
            for e in range(n):
                prob += self.dist(i + 1.0 * e/n) * 1.0 * e/n
            self.probs[i] = prob
        

class GuassianBalloon(Balloons):
    def __init__(N = 10):
        super().__init__(N)
        self.mean = random.randint(self.min, self.max)
        self.var = random.randint(3 * self.max)
        self.std = math.sqrt(self.var)
        super().getprobs()
        
    def dist(x):
        return 1.0/ (self.std * math.sqrt(2 * math.pi)) * math.e ** (-1 * (x - self.m)**2 / (2 * self.var))


class UniformBalloon(Balloons):
    def __init__(N = 10):
        super().__init__(N)
        super().getprobs()
        
    def dist(x):
        if x < self.min:
            return 0
        if x > self.max: 
            return 0
        else:
            return 1/(self.max - self.min)

class UniformBalloon(Balloons):
    def __init__(N = 10):
        super().__init__(N)
        super().getprobs()
        
    def dist(x):
        if x < self.min:
            return 0
        if x > self.max: 
            return 0
        else:
            return 1/(self.max - self.min)


class GeometricBalloon(Balloons):
    def __init__(N = 10):
        super().__init__(N)
        self.p = random.randint(10) * 1.0 / 10
        super().getprobs()
        
    def dist(x):
        return ((1 - self.p) ** math.floor(x - 1)) * self.p
        
class ConstantBalloon(Balloons):
    def __init__(N = 10):
        super().__init__(N)
        self.limit = random.randint(self.min, self.max)
        super().getprobs()
        
    def dist(x):
        if x < self.limit: 
            return 0
        if x >= self.limit and x <= self.limit + 1: 
            return 1



        
