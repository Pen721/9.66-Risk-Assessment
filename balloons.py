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
        print(np.sum(self.probs))
        pop = random.choice(self.max, self.N, p=self.probs)
        self.balloons = pop

    def getBallons(self):
        return self.balloons.copy()

    def p(self, x):
        return self.dist.pdf(x)

    def p_range(self, x, y):
        return self.dist.cdf(x, y)

class GaussianBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "GAUSSIAN"
        self.dist = Gaussian()
        self.initializeBalloons()

class UniformBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "UNIFORM"
        self.dist = Uniform()
        self.initializeBalloons()

class GeometricBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "GEOMETRIC"
        self.dist = Geometric()
        self.initializeBalloons()
        
class LimitBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "LIMIT"
        self.dist = Limit()
        self.initializeBalloons()

balloons = GaussianBalloons()
print(balloons)
