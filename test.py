from agent import Agent, LossAverseAgent, NotLossAverseAgent
from balloons import GaussianBalloons, UniformBalloons, LimitBalloons, GeometricBalloons
from dist import Gaussian, Limit, Uniform, Geometric
import matplotlib  
matplotlib.use('TkAgg')   
import matplotlib.pyplot as plt 
import random
import numpy as np
from dist import Gaussian, Geometric, Uniform, Limit
import math
import os
from player import Player

def experiment():
    # number of experiments
    K = 1
    #number of balloons
    N = 20
    obs = []
    dists = []
    decay = 0.5
    HORIZON = 12
    for i in range(K):
        b = GaussianBalloons(N=N)
        dists.append(b)
        obs.append(b.getBallons())

    # b = [5,6,5,7,5,6,7,5,6,7]

    # a = Agent(b, 20, 0.5)
    # a.play()

    # horizon = np.array([math.floor(i / K) for i in range(K*HORIZON)])

    horizon = [[] for i in range(K)]
    points = [[] for i in range(K)]
    # points = np.array([-1 for i in range(HORIZON*K)])

    for i in range(HORIZON):
        for j in range(K):
            o = obs[j]
            a = LossAverseAgent(o, i, decay)
            p = a.play()

            horizon[j].append(i)
            # if(i==2):
            #     if(points[2] > points[1]):
            #         print("SECOND HORIZON BETTER THAN FIRST")
            #         print(dists[j])
            
            points[j].append(p * 100.0 / a.total_points())
            # points[i*K + j] = p

    # plt.plot(horizon, points)
    for i in range(K):
        plt.plot(horizon[i], points[i])

    plt.xlabel('horizon')
    plt.ylabel('points')
    plt.title('percentage of points gained over horizons, N={} decay={}'.format(N, decay))
    plt.savefig('graphs/Gaussian/N={}decay={}K={}.pdf'.format(N, decay, K))

def horizontwo():
    obs = [1, 3, 2]
    decay = 1
    a = Agent(obs, 1, decay)
    b = Agent(obs, 2, decay)

    # a.getExpectedUtility(0, 0, 0, False, 1, [[-1, -1] for i in range(len(obs))])
    # b.getExpectedUtility(0, 0, 0, False, 2, [[-1, -1] for i in range(len(obs))])
    b.play()
    print(b.memo)

def distRange():
    b = GaussianBalloons(N=70, mean=10, std = 3)
    print(b.getBallons())
    c = GaussianBalloons(N=70, mean=0, std = 3)
    print(c.getBallons())

def getAgent():
    #human score 24
    #gaussian mean 7 std 2 I think
    obs = [1,5,5,4,1,6,7,5,4,7]
    decay = 1
    horizon = 8
    decays = [0.1, 0.3, 0.5, 0.7, 0.9, 1]

    x = [i for i in range(horizon)]
    human = [14 for i in range(horizon)]
    y = [[] for i in range(len(decays))]

    for i in range(len(decays)):
        for j in range(horizon):
            a = Agent(obs, j, decays[i])
            y[i].append(a.play())
            print(j, decays[i], a.mostlikely)
            print(a.lastSwitch)

    for i in range(len(y)):
        plt.plot(x, y[i], label='agent score, decay={}'.format(round(1-decays[i], 1)))

    plt.plot(x, human, '--', label='human score')
    plt.legend(loc='upper right')
    plt.xlabel('horizon')
    plt.ylabel('points')
    plt.title('agent points gained over decision horizons'.format(obs))
    plt.savefig('graphs/Gaussian/{}.pdf'.format(obs))

def getSingleAgent():
    #human score 24
    #gaussian mean 7 std 2 I think
    obs = [1,5,5,4,1,6,7,5,4,7]
    decay = 1
    horizon = 12
    decays = [1]

    x = [i for i in range(horizon)]
    human = [14 for i in range(horizon)]
    y = [[] for i in range(len(decays))]

    for i in range(len(decays)):
        a = Agent(obs, 5, decays[i])
        y[i].append(a.play())
        print(y[i])
        print(a.mostlikely)
        print(a.lastSwitch)

    # for i in range(len(y)):
    #     plt.plot(x, y[i], label='agent score, varying horizon'.format(round(1-decays[i], 1)))

    # plt.plot(x, human, '--', label='human score')
    # plt.legend(loc='upper right')
    # plt.xlabel('horizon')
    # plt.ylabel('points')
    # plt.title('agent points with varying horizon'.format(obs))
    # plt.savefig('graphs/Gaussian/26horizon.pdf')

def makeGraphs():
    dist = Geometric()
    x = np.linspace(1, 11, num=100)
    y = [dist.cdf(math.floor(i-1), math.floor(i)) for i in x]
    plt.title("example balloon distribution")
    plt.plot(x, y)
    plt.ylabel('probability balloon pops at size x')
    plt.xlabel('balloon size')
    plt.savefig("dists/{}.pdf".format(dist.shortString()))

def readPlayer():
    p = Player(self, "GEN", 0, "N", 0, 10, True, 0, False)
    p.getPlayerFromFile(1)


def readData(exp):
    folder = os.path.join(os.getcwd(), "data/exp{}".format(exp))

    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r') as f: # open in readonly mode
            if(filename == ".DS_Store"):
                continue
            # print(filename)
            filestring = f.readlines()
            # print(filestring)

            diststring = filestring[0].split()
            # print(diststring)
            [name, age, gender, N, course, time] = diststring[:6]
            course = int(course)
            disttype = diststring[6]

            N = int(diststring[7])
            if(disttype == "GAUSSIAN"):
                mean = int(diststring[8])
                std = int(diststring[9])
                dist = Gaussian(N, mean, std)
                balloons = GaussianBalloons(N, mean, std)
            elif(disttype == "UNIFORM"):
                umin = int(diststring[8])
                umax = int(diststring[9])
                dist = Uniform(N, umin, umax)
                balloons = UniformBalloons(N, umin, umax)
            elif(disttype=="LIMIT"):
                limit = int(diststring[8])
                dist = Limit(N, limit)
                balloons = LimitBalloons(N, limit)
            elif(disttype=="GEOMETRIC"):
                p = float(diststring[8])
                dist = Geometric(N, p)
                balloons = GeometricBalloons(N, p)
            else:
                raise Exception("UNKNOWN DISTRIBUTION {}".format(disttype))
            lossAversion = eval(diststring[-2])
            seenGraphs = eval(diststring[-1])
            # print(lossAversion, seenGraphs)

            obs = filestring[1].split(",")[:-1]
            obs = [int(i) for i in obs]
            # print(obs)
            balloons.setBalloons(obs)
            player = Player(name, age, gender, course, balloons, lossAversion, exp, seenGraphs, time=time)

            score = int(filestring[-1].split()[-1])
            player.finalScore = score

            for i in range(2, len(filestring) - 1):
                action = filestring[i].split()
                [index, size, action, time, score] = action
                player.addActionData(int(index), int(size), action, int(time), int(score))

            # print(player)
            f.close()
            generateGamePlayGraph(player)

def generateGamePlayGraph(player):
    #assumes player and agent have already played
    horizon = [1, 2, 3]
    decay = [1, 0.9]

    x = [i for i in range(player.N)]
    maxpoints = player.pops
    print(maxpoints)
    p = player.pointPerBalloon()

    for i in range(1, len(p)):
        maxpoints[i] += maxpoints[i-1]
    
    for h in horizon:
        for d in decay:
            ap = getAgentPoints(player.pops, h, d)
            plt.plot(x, ap, label='agent score h={} d={}'.format(h, d))
    plt.plot(x, p, label='player score')
    plt.plot(x, maxpoints, '--', label='theoretical max score')

    plt.legend(loc='upper left')
    plt.xlabel('balloon index')
    plt.ylabel('points')
    plt.title('points gained over time')
    plt.savefig('data/gameplay/{} AGENT H={} decay={}.pdf'.format(player.playerinfonotime(), h, d))
    plt.clf()

def getAgentPoints(obs, h, d):
    agent = Agent(obs, h, d)
    agent.play()
    agentp = agent.pointPerBalloon().copy()
    return agentp

# GAUSSIAN mean 7 std 1
# BALLOONS: [5,6,5,7,5,6,7,5,6,7]
# probs: [0.0000, 0.0000, 0.0000, 0.0013, 0.0212, 0.1352, 0.3410, 0.3426, 0.1370, 0.0217]

if __name__ == "__main__":
    # readData(2)
    # readData(3)
    a = Agent([1,1,3,2,2,2,1,1,1,3], 4, 0.9)
    a.play()
    print(a.actions)
    # do your stuff
    # distRange()
    # experiment()
    # readPlayer(1, )
    # print("Everything passed")
