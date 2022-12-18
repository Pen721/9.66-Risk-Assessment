#player class, 
from datetime import datetime
from dist import *

class Player:
    def __init__(self, name, age, gender, course, balloons, lossAversion, exp, seenGraphs):
        self.fileName = None
        self.name = name
        self.age = age
        self.gender = gender
        self.balloons = balloons #number of balloons, N
        self.N = balloons.N
        self.dist = balloons.dist
        self.pops = balloons.getBallons()
        self.course = course
        self.actions = [] #stores actions of player over time
        self.lossAversion = lossAversion
        self.now = None
        self.exp=exp
        self.folder = "data/exp{}/".format(self.exp)
        self.seenGraphs = seenGraphs

    def nextBalloon(self, timeStamp, ):
        '''update actions'''

    def addAir(self, ):
        '''update actions'''

    def toString(self, ):
        pass

    def writeData(self):
       '''store player data some where so we can retrieve and analyze'''
       self.setFileName()
       print("WRITING DATA")
       print(self.actions)
       f = open("{}{}".format(self.folder, self.fileName), "a")
       for i in self.actions:
           f.write("{} {} {} {} {}\n".format(i[0], i[1], i[2], i[3], i[4]))
       f.close()

    def writeStringToData(self, string):
        self.setFileName()
        f = open("{}{}".format(self.folder, self.fileName), "a")
        f.write(string)
        f.close()
    
    def addActionData(self, index, size, action, time, score):
        'index and size of of the balloon -> if we are on the first balloon and its size 3, it would be index 0 size 3, action is either a string of PUMP or PASS, time is the time since the last action (optional)'
        'totalPoints is defined in accordance with lossAversion settings (so whatever is on screen)'
        self.actions.append([index, size, action, time, score])
    
    def setFileName(self):
        now = datetime.now()
        self.now = now
        if(self.fileName == None):
            self.fileName = "{}_{}_{}_{}_{}_{}_{}.txt".format(self.name, self.age, self.gender, self.N, self.course, now.strftime("%Y-%m-%d_%H:%M"), self.balloons.dist.shortString())

    def playerinfotostring(self):
        return "{} {} {} {} {} {} {} {} {}".format(self.name, self.age, self.gender, self.N, self.course, self.now.strftime("%Y-%m-%d_%H:%M"), self.balloons.dist.shortString(), self.lossAversion, self.seenGraphs)

    def addDistributionData(self):
        self.setFileName()
        f = open("{}{}".format(self.folder, self.fileName), "a")

        dist = self.balloons.dist

        f.write(self.playerinfotostring())
        f.write('\n')
        for i in self.pops:
            f.write("{},".format(i))
        f.write("\n")