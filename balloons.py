import math
import numpy as np
from numpy import random
from dist import Gaussian, Geometric, Limit, Uniform

class Balloons:
    def __init__(self, N = 10):
        self.N = N  # number of balloons
        self.current_balloon = 0 
        self.max = 10
        self.min = 0
        self.probs = np.empty(self.max - self.min, dtype=float)
        self.balloons = np.empty(self.N, dtype=float)  # balloon array w/ how many inc cause breaking

    def __str__(self):
        str = ""
        str += "{} mean {} std {}".format(self.type, self.dist.mean, self.dist.std)
        str += '\nBALLOONS: '
        for i in range(len(self.balloons)):
            str += "{}".format(self.balloons[i]) + ","
        str += " \n probs: "
        for i in range(len(self.probs)):
            str += "{0:.{1}f}".format(self.p_range(i, i+1), 4) + ", "
        str += " \n "
        str += "balloons"
        return str

    def initializeBalloons(self):
        for i in range(self.max - self.min):
            self.probs[i] = self.p_range(i, i+1)
        pop = random.choice(self.max, self.N, p=self.probs)
        pop = [i+1 for i in pop]
        self.balloons = pop

    def getBallons(self):
        return self.balloons.copy()

    def p(self, x):
        return self.dist.pdf(x)

    def p_range(self, x, y):
        return self.dist.cdf(x, y)


class GaussianBalloons(Balloons):
    def __init__(self, N = 10, mean = None, std = None, B=None):
        super().__init__(N)
        self.type = "GAUSSIAN"
        self.dist = Gaussian(N=N, mean=mean, std=std)
        if(B == None):
            self.initializeBalloons()
        else:
            self.balloons = B

class UniformBalloons(Balloons):
    def __init__(self, N = 10, umin= None, umax=None, B=None):
        super().__init__(N)
        self.type = "UNIFORM"
        self.dist = Uniform(N=N, umin=umin, umax=umax)
        if(B == None):
            self.initializeBalloons()
        else:
            self.balloons = B

class GeometricBalloons(Balloons):
    def __init__(self, N = 10, p=None, B=None):
        super().__init__(N)
        self.type = "GEOMETRIC"
        self.dist = Geometric(N=N, p=p)
        if(B == None):
            self.initializeBalloons()
        else:
            self.balloons = B
        
class LimitBalloons(Balloons):
    def __init__(self, N = 10, limit=None, B=None):
        super().__init__(N)
        self.type = "LIMIT"
        self.dist = Limit(N=N, limit=limit)
        print("LImIT DIST'")
        print(self.dist)
        self.initializeBalloons()
        if(B == None):
            self.initializeBalloons()
        else:
            self.balloons = B
        
