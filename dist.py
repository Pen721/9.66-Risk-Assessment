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
        self.min = 0
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
        if(self.cdfmemo[x][y] != -1):
            return self.cdfmemo[x][y]
        else:
            self.cdfmemo[x][y] = self.unnormalizedcdf(x, y) / self.total
            return self.cdfmemo[x][y]

class Gaussian(Dist):
    def __init__(self, N = 10, mean = None, std = None):
        super().__init__()
        self.type = "GAUSSIAN"

        self.mean = mean 
        self.std = std

        if self.mean == None:
            self.mean = random.randint(0, 10)

        if self.std == None:
            self.std = random.randint(1, 3)
       
        self.var = self.std ** 2
        self.total = self.unnormalizedcdf(0, N)
        
    def pdf(self, x):
        return 1.0/ (self.std * math.sqrt(2 * np.pi)) * np.exp((-1 * (x - self.mean)**2) / (2 * self.var))

    def __str__(self):
        return "Gaussian mean {} std {}".format(self.mean, self.std)


class Uniform(Dist):
    def __init__(self, N = 10, max = None, min = None):
        super().__init__()
        self.type = "UNIFORM"
        self.max = max
        self.min = min

        if self.max == None:
            self.max = random.randint(2, 10)
        if self.min == None:
            self.min = random.randint(0, self.max - 2)
        
        self.mean = (self.max + self.min)/2.0
        self.var = (1.0/12)*(self.max - self.min)**2
        self.total = self.unnormalizedcdf(0, N)
        print("self.total", self.total)
        
    def pdf(self, x):
        if x < self.min:
            return 0
        if x > self.max: 
            return 0
        else:
            return 1/(self.max - self.min)

    def __str__(self):
        return "Uniform max {} min {}".format(self.max, self.min)

class Geometric(Dist):
    def __init__(self, N = 10, p = None):
        super().__init__()
        self.type = "GEOMETRIC"
        if p == None:
            self.p = random.randint(1, 9) * 1.0 / 10
        else:
            self.p = p
        self.mean = 1.0/self.p
        self.var = (1-self.p)/(self.p**2)
        self.total = self.unnormalizedcdf(0, N)
        
    def pdf(self, x):
        return ((1 - self.p) ** math.floor(x - 1)) * self.p

    def __str__(self):
        return "Geometric p {}".format(self.p)
        
class Limit(Dist):
    def __init__(self, N = 10, limit = None):
        super().__init__()
        self.type = "LIMIT"
        self.limit = limit
        if limit == None:
            self.limit = random.randint(0, 10)
        self.mean = self.limit
        self.var = 0
        self.total = self.unnormalizedcdf(0, N)
        print("self.total", self.total)
        
    def pdf(self, x):
        if x < self.limit or x >= self.limit + 1: 
            return 0
        else:
            return 1
    
    def __str__(self):
        return "Limit {}".format(self.limit)

# dist = Gaussian(mean=6, std=4)
# print(dist)
# print(dist.cdf(0, 10))
# plt.plot(data)
# plt.show()
