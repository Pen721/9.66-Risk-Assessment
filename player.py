#player class, 
from datetime import datetime

class Player:
    def __init__(self, name, age, gender, time = None):
        self.name = name
        self.age = age
        self.gender = gender
        # self.time = time
        self.actions = [[0, 0, "PUMP", 0.3], [0, 1, "PUMP", 0.4]] #stores actions of player over time

    def nextBalloon(self, timeStamp, ):
        '''update actions'''

    def addAir(self, ):
        '''update actions'''

    def toString(self, ):
        pass

    def writeData(self):
       '''store player data some where so we can retrieve and analyze'''
       now = datetime.now()
       print(now.strftime("%d_%m_%Y_%H:%M:%S"))
       f = open("data/{}_{}_{}_{}.txt".format(self.name, self.age, self.gender, now.strftime("%Y-%m-%d_%H:%M")), "w")
       for i in self.actions:
           f.write("{} {} {} {} \n".format(i[0], i[1], i[2], i[3]))
       f.close()

p = Player("Jenny", 23, "M")
p.writeData()