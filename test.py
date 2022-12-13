from agent import Agent
from balloons import GaussianBalloons
# number of experiments
K = 30

#number of balloons
N = 20
obs = []
dists = []
decay = 0.5
HORIZON = 8
# obs.append(GaussianBalloons(N=N, mean = 8, std = 1).getBallons())
# for i in range(K):
#     b = GaussianBalloons(N=N)
#     dists.append(b)
#     obs.append(b.getBallons())

b = [5,6,5,7,5,6,7,5,6,7]

a = Agent(b, 20, 0.5)
a.play()

# # horizon = np.array([math.floor(i / K) for i in range(K*HORIZON)])

# horizon = [[] for i in range(K)]
# points = [[] for i in range(K)]
# # points = np.array([-1 for i in range(HORIZON*K)])

# for i in range(HORIZON):
#     for j in range(K):
#         o = obs[j]
#         a = Agent(o, i, decay)
#         p = a.play()

#         horizon[j].append(i)
#         if(i==2):
#             if(points[2] > points[1]):
#                 print("SECOND HORIZON BETTER THAN FIRST")
#                 print(dists[j])
        
#         points[j].append(p)
#         # points[i*K + j] = p

# # plt.plot(horizon, points)
# for i in range(len(obs)):
#     plt.plot(horizon[i], points[i])

# # plt.xlabel('horizon')
# # plt.ylabel('points')
# # plt.title('points gained over horizons')
# # plt.savefig('graphs/Gaussian/N={}decay={}K={}.pdf'.format(N, decay, K))


# # GAUSSIAN mean 7 std 1
# # BALLOONS: [5,6,5,7,5,6,7,5,6,7]
# # probs: [0.0000, 0.0000, 0.0000, 0.0013, 0.0212, 0.1352, 0.3410, 0.3426, 0.1370, 0.0217]