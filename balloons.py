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
        print(*self.probs, sep = ", ")

    def __str__(self):
        str = ""
        str += self.type
        str += " \n probs: "
        for i in range(len(self.probs)):
            str += self.probs[i] + ", "
        str += " \n "
        str += "balloons"
        str += self.balloons[i]
        return 

    def getBallons(self):
        return self.balloons.copy()

    def getprobs(self):
        print('getting probs ;_')
        totalprobs = 0
        for i in range(self.min, self.max):
            n = 50
            prob = 0
            for e in range(n):
                prob += self.dist(i + 1.0 * e/n) * 1.0 * e/n
            self.probs[i] = prob
            totalprobs += prob
        
        for i in range(len(self.probs)):
            self.probs[i] /= totalprobs

class GaussianBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "GAUSSIAN"
        self.dist = Gaussian()
        super().getprobs()


class UniformBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "UNIFORM"
        self.dist = Uniform()
        super().getprobs()

class GeometricBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "GEOMETRIC"
        self.dist = Geometric()
        super().getprobs()
        
class LimitBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "LIMIT"
        self.dist = Limit()
        super().getprobs()



        
