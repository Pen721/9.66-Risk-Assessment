class Dist():
    def __init__(self, type):


class Gaussian(Dist):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "GAUSSIAN"
        self.mean = random.randint(self.min, self.max)
        self.var = random.randint(1, 3 * self.max)
        self.std = math.sqrt(self.var)
        super().getprobs()
        
    def dist(self, x):
        return 1.0/ (self.std * math.sqrt(2 * math.pi)) * math.e ** (-1 * (x - self.mean)**2 / (2 * self.var))


class UniformBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "UNIFORM"
        super().getprobs()
        
    def dist(self, x):
        if x < self.min:
            return 0
        if x > self.max: 
            return 0
        else:
            return 1/(self.max - self.min)

class GeometricBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "GEOMETRIC"
        self.p = random.randint(10) * 1.0 / 10
        super().getprobs()
        
    def dist(self, x):
        return ((1 - self.p) ** math.floor(x - 1)) * self.p
        
class LimitBalloons(Balloons):
    def __init__(self, N = 10):
        super().__init__(N)
        self.type = "LIMIT"
        self.limit = random.randint(self.min, self.max)
        super().getprobs()
        
    def dist(self, x):
        if x < self.limit: 
            return 0
        if x >= self.limit and x <= self.limit + 1: 
            return 1
