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
    K = 30
    #number of balloons
    N = 10
    obs = []
    distname = []
    dists = []
    decay = 1
    HORIZON = 2
    dists = []
    for i in range(K):
        DISTS = ["GAUSSIAN", "UNIFORM", "GEOMETRIC", "LIMIT"]
        distribution = "GAUSSIAN"
        balloons = None
        if distribution == 'GAUSSIAN':
            balloons = GaussianBalloons(N)
        # elif distribution == 'UNIFORM':
        #     balloons = UniformBalloons(N)
        # elif distribution == 'LIMIT':
        #     balloons = LimitBalloons(N)
        # elif distribution == 'GEOMETRIC':
        #     balloons = GeometricBalloons(N)

        distname.append(distribution)
        dists.append(balloons)
        balloons = balloons.getBallons()
        obs.append(balloons)

    # horizon = [[] for i in range(K)]
    # points = [[] for i in range(K)]
    # points = np.array([-1 for i in range(HORIZON*K)])
    points = []

    avg = 0
    for j in range(K):
        o = obs[j]
        a = Agent(o, 2, decay)
        a.play()
        running = o.copy()
        for i in range(1, len(running)):
            running[i] += running[i-1]
        p = a.pointPerBalloon().copy()
        for i in range(len(balloons)):
            p[i] = p[i] * 100.0/running[i]
        points.append(p)
        avg+=p[-1]

    # for i in range(HORIZON):
    #     for j in range(K):
    #         o = obs[j]
    #         a = LossAverseAgent(o, i, decay)
    #         p = a.play()

    #         horizon[j].append(i)
    #         # if(i==2):
    #         #     if(points[2] > points[1]):
    #         #         print("SECOND HORIZON BETTER THAN FIRST")
    #         #         print(dists[j])
            
    #         points[j].append(p * 100.0 / a.total_points())
            # points[i*K + j] = p
    x = [i for i in range(10)]
    # plt.plot(horizon, points)
    for i in range(K):
        plt.plot(x, points[i], label='{}'.format(distname[i]))

    plt.xlabel('horizon')
    plt.ylabel('points')
    plt.legend(loc='upper right')
    plt.title('percentage of points gained over time with horizon=2')
    plt.savefig('graphs/horizon=2.pdf')


    avg/= len(points)
    print("FINAL AVERAGE PERCENTAGE POINT FROM VARYING: {}".format(avg))

def testDistribution():
    # number of experiments
    K = 30
    #number of balloons
    N = 10
    obs = []
    distname = []
    dists = []
    decay = 1
    HORIZON = 2
    dists = []
    for i in range(K):
        DISTS = ["GAUSSIAN", "UNIFORM", "GEOMETRIC", "LIMIT"]
        distribution = "GAUSSIAN"
        balloons = None
        if distribution == 'GAUSSIAN':
            balloons = GaussianBalloons(N)
        # elif distribution == 'UNIFORM':
        #     balloons = UniformBalloons(N)
        # elif distribution == 'LIMIT':
        #     balloons = LimitBalloons(N)
        # elif distribution == 'GEOMETRIC':
        #     balloons = GeometricBalloons(N)

        distname.append(distribution)
        dists.append(balloons)
        balloons = balloons.getBallons()
        obs.append(balloons)

    # horizon = [[] for i in range(K)]
    # points = [[] for i in range(K)]
    # points = np.array([-1 for i in range(HORIZON*K)])
    points = []

    avg = 0
    for j in range(K):
        o = obs[j]
        a = Agent(o, 2, decay)
        a.play()
        running = o.copy()
        for i in range(1, len(running)):
            running[i] += running[i-1]
        p = a.pointPerBalloon().copy()
        for i in range(len(balloons)):
            p[i] = p[i] * 100.0/running[i]
        points.append(p)
        avg+=p[-1]

    x = [i for i in range(10)]
    # plt.plot(horizon, points)
    for i in range(K):
        plt.plot(x, points[i], label='{}'.format(distname[i]))

    plt.xlabel('horizon')
    plt.ylabel('points')
    plt.legend(loc='upper right')
    plt.title('percentage of points gained over time with horizon=2')
    plt.savefig('graphs/horizon=2.pdf')


    avg/= len(points)
    print("FINAL AVERAGE PERCENTAGE POINT FROM VARYING: {}".format(avg))

def horizontwo():
    obs = [0, 1, 2, 3, 4, 5, 6, 7]
    decay = []
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
    decays = [0.9, 1]

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

    # decay = [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    horizon = 7
    decays = [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]

    x = [i for i in range(horizon)]
    human = [14 for i in range(horizon)]
    y = [[] for i in range(len(decays))]

    for i in range(len(decays)):
        for h in range(horizon):
            a = Agent(obs, h, decays[i])
            y[i].append(a.play())
            print(y)
            # print(a.mostlikely)
            # print(a.lastSwitch)

    for i in range(len(y)):
        plt.plot(x, y[i], label='agent score, horizon={}, decay {}'.format(i, round(decays[i], 1)))

    # plt.plot(x, human, '--', label='human score')
    plt.legend(loc='upper left')
    plt.xlabel('horizon')
    plt.ylabel('points')
    plt.title('agent points with varying horizon'.format(obs))
    plt.savefig('graphs/all-hyp/horizons.pdf')
    plt.clf()

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
    aavg = 0
    avg = [0] * 10 
    n_players = 0 
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r') as f: # open in readonly mode
            if(filename == ".DS_Store"):
                continue
            # n_players += 1
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
                n_players+=1
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

            if(disttype == "GAUSSIAN"):
                print(avg)
                total = 0.0
                for i in obs:
                    total += i
                aavg += score / total

            for i in range(2, len(filestring) - 1):
                action = filestring[i].split()
                [index, size, action, time, score] = action
                player.addActionData(int(index), int(size), action, int(time), int(score))

            pper = player.pointPerBalloon()
            for i in range(len(pper)):
                avg[i] += pper[i]
            f.close()
            # GamePlayGraphSingleAgent(player)
            diff(player)
    avg = aavg / n_players
    print("AVG: {}".format(avg))

def diff(player):
    diffs = 0
    pop = player.pops.copy()
    total = 0
    for i in pop:
        total+=i
    p = player.pointPerBalloon()

    a = Agent(pop, 2, 1)
    a.play()
    ap = a.pointPerBalloon()

    for i in range(len(pop)):
        if(p[i] == 0 and ap[i] == 0):
            diffs +=0
        if(p[i] == 0):
            diffs += pop[i] - ap[i]
        elif(ap[i] == 0):
            diffs += pop[i] - ap[i]

    print(p)
    print(ap)
    print(diffs)
    print(diffs / total)
    
def avgGraph(p, player):
    #assumes player and agent have already played
    horizon = [1, 2, 3]
    decay = [0.9, 1.0]

    x = [i for i in range(player.N)]
    maxpoints = player.pops.copy()
    print(maxpoints)

    for i in range(1, len(p)):
        maxpoints[i] += maxpoints[i-1]
    
    for h in horizon:
        for d in decay:
            ap = getAgentPoints(player.pops, h, d)
            plt.plot(x, ap, label='agent score h={} d={}'.format(h, d))
    plt.plot(x, p, label='avg player score')
    plt.plot(x, maxpoints, '--', label='theoretical max score')

    plt.legend(loc='upper left')
    plt.xlabel('balloon index')
    plt.ylabel('points')
    plt.title('points gained over time')
    # plt.savefig('data/gameplay/{} AGENT.pdf'.format(player.playerinfonotime()))
    plt.savefig('data/gameplay/a2 vgPlayerScore.pdf'.format(player.playerinfonotime(), h, d))
    plt.clf()

def generateGamePlayGraph(player):
    #assumes player and agent have already played
    horizon = [1, 2, 3, 4, 5, 6, 7]
    decay = [0.9, 1.0]

    x = [i for i in range(player.N)]
    maxpoints = player.pops.copy()
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
    # plt.savefig('data/gameplay/justhuman/{}.pdf'.format(player.playerinfonotime()))
    plt.savefig('data/gameplay/allhyp/{} AGENT H={} decay={}.pdf'.format(player.playerinfonotime(), h, d))
    plt.clf()

def GamePlayGraphSingleAgent(player):
    #assumes player and agent have already played
    x = [i for i in range(player.N)]
    maxpoints = player.pops.copy()
    p = player.pointPerBalloon()

    for i in range(1, len(p)):
        maxpoints[i] += maxpoints[i-1]
    
    ap = getAgentPoints(player.pops, 2, 1)
    plt.plot(x, ap, label='agent score')
    plt.plot(x, p, label='player score')
    plt.plot(x, maxpoints, '--', label='theoretical max score')

    plt.legend(loc='upper left')
    plt.xlabel('balloon index')
    plt.ylabel('points')
    plt.title('points gained over time')
    plt.savefig('data/gameplay/allhyp/{} AGENT varying horizon'.format(player.playerinfonotime()))
    plt.clf()

def getAgentPoints(obs, h, d):
    print(obs)
    print(h)
    print(d)

    agent = Agent(obs, h, d)
    agent.play()
    agentp = agent.pointPerBalloon().copy()
    return agentp



# def compareplayertoAgent(player, agent):
    

# GAUSSIAN mean 7 std 1
# BALLOONS: [5,6,5,7,5,6,7,5,6,7]
# probs: [0.0000, 0.0000, 0.0000, 0.0013, 0.0212, 0.1352, 0.3410, 0.3426, 0.1370, 0.0217]

if __name__ == "__main__":
    # experiment()
    readData(2)
    # a = Agent([6] * 10, 3, 0.9)
    # a.play()
    # a.play()
    # print(a.actions)
    # do your stuff
    # distRange()
    # experiment()
    # readPlayer(1, )
    # print("Everything passed")
