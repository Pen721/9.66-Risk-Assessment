#player class, 
from datetime import datetime

class Player:
    def __init__(self, name, age, gender, balloons, course, time = None):
        self.name = name
        self.age = age
        self.gender = gender
        self.balloons = balloons
        self.actions = [] #stores actions of player over time

    def nextBalloon(self, timeStamp, ):
        '''update actions'''

    def addAir(self, ):
        '''update actions'''

    def toString(self, ):
        pass

    def writeData(self):
       '''store player data some where so we can retrieve and analyze'''
       now = datetime.now()
       f = open("data/{}_{}_{}_{}.txt".format(self.name, self.age, self.gender, now.strftime("%Y-%m-%d_%H:%M")), "w")
       for i in self.actions:
           f.write("{} {} {} {} \n".format(i[0], i[1], i[2], i[3]))
       f.close()
    
    def addActionData(self, index, size, action, time):
        'index and size of of the balloon -> if we are on the first balloon and its size 3, it would be index 0 size 3, action is either a string of PUMP or PASS, time is the time since the last action (optional)'
        self.actions.append([index, size, action, time])