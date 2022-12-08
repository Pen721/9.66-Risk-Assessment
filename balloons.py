import math
import numpy as np
from numpy import random
from dist import Gaussian, Geometric, Limit, Uniform

class Balloons:
    def __init__(self, N = 10):
        self.N = N
        self.current_balloon = 0
        self.max = 10
        self.min = 0
        self.probs = np.array([-1] * (self.max - self.min))
        self.balloons = [-1] * N

    def __str__(self):
        str = ""
        str += self.type
        str += " \n probs: "
        for i in range(len(self.probs)):
            str += "{}".format(self.p_range(i, i+1)) + ", "
        str += " \n "
        str += "balloons"
        return str

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

class UniformBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "UNIFORM"
        self.dist = Uniform()

class GeometricBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "GEOMETRIC"
        self.dist = Geometric()
        
class LimitBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "LIMIT"
        self.dist = Limit()

balloons = GaussianBalloons()
print(balloons)
