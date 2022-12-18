import random
import math
import numpy as np
import matplotlib  
matplotlib.use('TkAgg')   
import matplotlib.pyplot as plt

class Dist():
    def __init__(self):
        '''distributions'''
        self.N = 10
        self.max = 10
        self.min = 1
        self.cdfmemo = [[-1] * (self.max + 1)] * (self.max + 1)

    def unnormalizedcdf(self, x, y):
        diff = y - x
        n = 100
        prob = 0
        for e in range(int((y - x) * n)):
            x0 = x + (diff) * e/((y-x) * n)
            prob += self.pdf(x0) * (1.0/n)
        return prob

    def cdf(self, x, y):
        if(x > self.max):
            return 0
        elif(y > self.max):
            return self.cdf(x, self.max)
        elif(y < 0):
            return 0
        elif(x < 0):
            return self.cdf(0, y)
        elif(self.cdfmemo[x][y] != -1):
            return self.cdfmemo[x][y]
        else:
            self.cdfmemo[x][y] = self.unnormalizedcdf(x, y) / self.total
            return self.cdfmemo[x][y]
    
    def plotpdf(self):
        x = np.linspace(0, 10, num=10)
        y = [self.pdf(i) for i in x]

class Gaussian(Dist):
    def __init__(self, N = 10, mean = None, std = None):
        super().__init__()
        self.type = "GAUSSIAN"
        self.mean = mean 
        self.std = std

        if self.mean == None:
            self.mean = random.randint(1, 10)

        if self.std == None:
            self.std = random.randint(1, 3)
       
        self.var = self.std ** 2
        self.total = self.unnormalizedcdf(0, N)
        
    def pdf(self, x):
        return 1.0/ (self.std * math.sqrt(2 * np.pi)) * np.exp((-1 * (x - self.mean)**2) / (2 * self.var))

    def __str__(self):
        return "Gaussian mean {} std {}".format(self.mean, self.std)
    
    def shortString(self):
        return "{} {} {} {}".format(self.type, self.N, self.mean, self.std)


class Uniform(Dist):
    def __init__(self, N = 10, umin = None, umax = None):
        super().__init__()
        self.type = "UNIFORM"
        self.umax = umax
        self.umin = umin

        pairs = [(i, j) for i in range(1, 9) for j in range(i+2, 11)]
        index = np.random.randint(0, len(pairs))
        pair = pairs[index]
        if self.umax == None:
            self.umax = pair[1]
        if self.umin == None:
            self.umin = pair[0]
        self.mean = (self.umax + self.umin)/2.0
        self.var = (1.0/12)*(self.umax - self.umin)**2
        self.std = np.sqrt(self.var)
        self.total = self.unnormalizedcdf(0, self.max)

        self.plotpdf()
        print("self.total", self.total)
        
    def pdf(self, x):
        if x < self.umin:
            return 0
        if x >= self.umax: 
            return 0
        else:
            return 1/(self.umax - self.umin)

    def __str__(self):
        return "Uniform max {} min {}".format(self.umax, self.umin)

    def shortString(self):
        return "{} {} {} {}".format(self.type, self.N, self.umin, self.umax)

class Geometric(Dist):
    def __init__(self, N = 10, p = None):
        super().__init__()
        self.type = "GEOMETRIC"
        if p == None:
            self.p = random.randint(1, 5) * 1.0 / 10
        else:
            self.p = p
        self.mean = 1.0/self.p
        self.var = (1-self.p)/(self.p**2)
        self.std = np.sqrt(self.var)
        self.total = self.unnormalizedcdf(0, N)
        
    def pdf(self, x):
        return ((1 - self.p) ** math.floor(x - 1)) * self.p

    def __str__(self):
        return "Geometric p {}".format(self.p)

    def shortString(self):
        return "{} {} {}".format(self.type, self.N, self.p)
        
class Limit(Dist):
    def __init__(self, N = 10, limit = None):
        super().__init__()
        self.type = "LIMIT"
        self.limit = limit
        if limit == None:
            self.limit = random.randint(1, 9)
        self.mean = self.limit
        self.var = 0
        self.std = 0
        self.total = self.unnormalizedcdf(0, N)
        print("self.total", self.total)
        
    def pdf(self, x):
        if x < self.limit or x >= self.limit + 1: 
            return 0
        else:
            return 1
    
    def __str__(self):
        return "Limit {}".format(self.limit)
    
    def shortString(self):
        return "{} {} {}".format(self.type, self.N, self.limit)

# dist = Gaussian(mean=5, std=1)
# dist2 = Gaussian(mean = 1, std=1)
# pprev1 = dist.cdf(3, 10) * dist.cdf(3, 4)

# pprev2 = dist2.cdf(3,10) * dist2.cdf(3, 4)
# print(pprev1)
# print(pprev2)

# ptotal = pprev1 + pprev2
# print(pprev1 / ptotal)
# print(pprev2 / ptotal)
