from agent import Agent
from balloons import GaussianBalloons
import matplotlib  
matplotlib.use('TkAgg')   
import matplotlib.pyplot as plt 
import random

def experiment():
    # number of experiments
    K = 30
    #number of balloons
    N = 20
    obs = []
    dists = []
    decay = 0.8
    HORIZON = 8
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
            a = Agent(o, i, decay)
            p = a.play()

            horizon[j].append(i)
            if(i==2):
                if(points[2] > points[1]):
                    print("SECOND HORIZON BETTER THAN FIRST")
                    print(dists[j])
            
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

# GAUSSIAN mean 7 std 1
# BALLOONS: [5,6,5,7,5,6,7,5,6,7]
# probs: [0.0000, 0.0000, 0.0000, 0.0013, 0.0212, 0.1352, 0.3410, 0.3426, 0.1370, 0.0217]

if __name__ == "__main__":
    # distRange()
    experiment()
    print("Everything passed")