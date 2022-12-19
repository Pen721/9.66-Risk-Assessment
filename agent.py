# a bayesian agent that runs calculations based on distribution
from dist import Gaussian, Geometric, Uniform, Limit
from balloons import *
import matplotlib  
matplotlib.use('TkAgg')   
import matplotlib.pyplot as plt  
import random
# import seaborn as sns
# sns.set()

class Agent():
    def __init__(self, balloons, horizon, decay):
        #first assuming everything is gaussian
        self.max = 10
        self.decay = decay
        self.min = 0

        hyp_mean = [i for i in range(0, self.max)]
        # hyp_mean = [1, 2, 3, 4, 5]
        hyp_std = [i for i in range(1, 3+1)]
        hyp_prob = [i * 1.0 / 10 for i in range(1,6)]
        hyp_lim = [i for i in range(1, 10)]
        hyp_int = [(umin, umax) for umin in range(1, 9) for umax in range(umin+2, 11)]

        p = 1.0/(len(hyp_mean) * len(hyp_std))
        self.balloons = balloons
        self.N = len(balloons)
        self.observed = [[-1, -1] for i in range(self.N)]

        self.hypothesis = {(m, std): [p, Gaussian(N=self.N, mean=m, std=std)] for m in hyp_mean for std in hyp_std}
        self.hypothesis.update({(prob): [p, Geometric(N=self.N, p=prob)] for prob in hyp_prob})
        self.hypothesis.update({(l): [p, Limit(N=self.N, limit=l)] for l in hyp_lim})
        self.hypothesis.update({(umin, umax): [p, Uniform(N=self.N, umin=umin, umax=umax)] for (umin, umax) in hyp_int})
        #ML could specify the hypothesis space / relative weighing of things through hierarchical learning but we assume uniform for now

        self.infiniteHorizon = False
        self.horizon = horizon
        self.memo = {}
        self.utilitymemo = {}
        self.mostlikely = None
        self.maxprob = 0
        self.lastSwitch = 0
        self.actions = []

    def total_points(self):
        points = 0
        for i in self.balloons:
            points += i - 1
        return points

    def convert_to_key(self, index, size, observation):
        # print("index {} size {} observation {}".format(index, size, observation))
        obsstring = ""
        for i in range(len(observation)):
            if(observation[i][0] != -1):
                obsstring += "{}{}".format(observation[i][0], observation[i][1])
        # print(obsstring)
        return (index, size, obsstring)

    def check_memo(self, index, size, observation):
        key = self.convert_to_key(index, size, observation)
        if(key in self.memo):
            return self.memo[key]
        return None

    def set_memo(self, index, size, observation, value):
        key = self.convert_to_key(index, size, observation)
        if(key in self.memo):
            raise Exception("huh why are we setting this again :0")
        self.memo[key] = value
       
    def pop_prob(self, index, size, observation):
        # print("POP PROB OBVSERVATION {}".format(observation))
        for i in range(index):
            if(observation[i][0] == -1):
                raise Exception("not all balloons before {} was seen, {} is empty".format(index, i))
            if(observation[i][1] != True and observation[i][1] != False):
                raise Exception("balloon wasn't popped or passed, what")

        will_pop = 0.0
        p_obv = 0

        val = self.check_memo(index, size, observation)
        
        if(val != None):
            return val
        else:
            if(size >= self.max - 1):
                #balloon guareenteed to pop at 10: potential experiment is giving vs not giving ppl this information
                return 1
            
            maxkey = None
            maxprob = 0
            maxtype = None
            # print("index {} size {} obv {}".format(index, size, observation))
            for key in self.hypothesis:
                p = self.hypothesis[key][0]
                dist = self.hypothesis[key][1]

                #current balloon observation
                p_prev = dist.cdf(size, self.max)

                for i in range(index):
                    obs = observation
                    item = obs[i]
                    bal_size = item[0]
                    popped = item[1]
                    if(popped): 
                        p_prev *= dist.cdf(bal_size -1, bal_size)
                    else:
                        p_prev *= dist.cdf(bal_size, self.max)
                # print("p_prev {}".format(p_prev))
                p_obv += p_prev
                #P(will pop | haven't popped yet) = p(haven't popped | will pop) * p(will  pop) / (p(haven't popped | will pop) + p(haven't popped | won't pop))
                p_not_popped = dist.cdf(size, self.max)

                if(p_not_popped == 0):
                    raise Exception("denominator is zero for cdf size, self.max")
                    # print("index {} size {} obv {}".format(index, size, observation))
                else:
                    P_will_pop = 1.0 * dist.cdf(size, size+1) / dist.cdf(size, self.max)
                p_dist = p_prev #*p

                if(p_dist > maxprob):
                    maxkey = key
                    maxtype = dist.type
                    maxprob = p_dist
                    self.lastSwitch = [index, size, observation]

                # print("will pop {} p_dist {}".format(P_will_pop, p_dist) )
                # print("DIST {} {} {}".format(dist.mean, dist.std, p_dist))
                # print()
                will_pop += P_will_pop * p_dist
            
            if(p_obv == 0):
                raise Exception("denominator is zero for p_obv")
                # print("index {} size {} obv {}".format(index, size, observation))
            will_pop = will_pop / p_obv
            self.mostlikely = maxkey
            self.maxprob = maxprob / p_obv
            # print("MOST LIKELY DIST: {} {} prob {}".format(maxtype, maxkey, maxprob / p_obv))
            # print("WILLPOP: {}".format(will_pop))
            self.set_memo(index, size, observation, will_pop)
            return will_pop

    def utility_key(self, index, size, score, infiniteHorizon, horizon, obs):
        obsstring = ""
        for i in range(len(obs)):
            if(obs[i][0] != -1):
                obsstring += "{}{}".format(obs[i][0], obs[i][1])
        return (index, size, score, infiniteHorizon, horizon, obsstring)

    def check_utility_memo(self, index, size, score, infiniteHorizon, horizon, obs):
        key = self.utility_key(index, size, score, infiniteHorizon, horizon, obs)
        if(key in self.utilitymemo):
            return self.utilitymemo[key]
        return None

    def set_utility_memo(self, index, size, score, infiniteHorizon, horizon, obs, value):
        key = self.utility_key(index, size, score, infiniteHorizon, horizon, obs)
        if(key in self.utilitymemo):
            raise Exception("huh why are we setting this again :0")
        self.utilitymemo[key] = value

    def pump(self, index, size, score):
        expected_utility = self.getExpectedUtility(index, size, score, self.infiniteHorizon, self.horizon, self.observed.copy())
        # if(index < 3):
        #     expected_utility = self.getExpectedUtility(index, size, score, self.infiniteHorizon, 2, self.observed.copy())
        # else:
        #     expected_utility = self.getExpectedUtility(index, size, score, self.infiniteHorizon, 2, self.observed.copy())
        # print("expected gain in utility {}".format(expected_utility))
        if(expected_utility[0] == "PUMP"):
            return True
        else:
            return False
    
    def balloonpops(self, index, size):
        if(self.balloons[index] > size):
            return False
        return True

    def play(self):
        size = 0
        index = 0
        points = 0
        points_from_this_balloon = 0

        while(True):
            # print("index {} size {}".format(index, size))
            if(index >= self.N):
                print("GAME ENDED")
                break

            #playing the same balloon
            if(not self.balloonpops(index, size)):
                if(size >= self.max):
                    # print("REACHED MAX SIZE")
                    # points += points_from_this_balloon
                    points_from_this_balloon = 0
                    #TODO: There might be a bug from the dist where all balloons pop at 10
                    index += 1
                    size = 0
                elif(self.pump(index, size, points_from_this_balloon)):
                    # print("PUMPED!")
                    self.actions.append([index, size, "PUMP", 0, points])
                    size += 1
                    points_from_this_balloon += 1
                else:
                    # print("PASSED")
                    #passed :(
                    points += points_from_this_balloon
                    points_from_this_balloon = 0
                    self.observed[index] = [size, False]
                    self.actions.append([index, size, "PASS", 0, points])
                    index +=1
                    size = 0
            else:
                # print("POPPED")
                if(size == 0):
                    print("index {} size {}".format(index, size))
                self.observed[index] = [size, True]
                self.actions.append([index, size, "POP", 0, points])
                index += 1
                size = 0
                points_from_this_balloon = 0
        print("POINTS: {}".format(points))
        return points

    def getExpectedUtility(self, index, size, score, infiniteHorizon, horizon, obs):
    #index: ranges from 0 to self.N - 1
    #size ranges from 0 to self.max
    #score ranges from 0 to self.max
    #infiniteHorizon False
    #horizon ranges from 0 to self.horizon
    #obs has self.N values, each has self.max values, and True or False (popped or not)
    # print("index {} size {} horizon {}".format(index, size, horizon))
        if(index < 0):
            raise Exception("index must be positive")
        if(score != size):
            raise Exception("score must be equal to size")
        for i in range(index):
            if(obs[i][0] == -1):
                raise Exception("not all balloons before {} was seen, {} is empty".format(index, i))
            if(obs[i][1] != True and obs[i][1] != False):
                raise Exception("balloon wasn't popped or passed, what")

        val = self.check_utility_memo(index, size, score, infiniteHorizon, horizon, obs)
        if(val != None):
            return val
        else:
            if(infiniteHorizon): 
                horizon = self.max * self.N
            
            if(horizon == 0):
                p = random.randint(0, 1)
                if p==1:
                    return ("PUMP", 0)
                if p==0:
                    return ("PASS", 0)
            elif(index >= self.N):
                return ("PASS", 0)
            elif(size == self.max - 1):
                return ("PASS", 0)
            elif(horizon == 1):
                # print("HORIZON = 1")
                will_pop = self.pop_prob(index, size, obs) 
                EU_PUMP = 1 * (1-will_pop) + (will_pop) * -1 * score
                if(EU_PUMP > 0):
                    self.set_utility_memo(index, size, score, infiniteHorizon, horizon, obs, ("PUMP", EU_PUMP))
                    return ("PUMP", EU_PUMP)
                else:
                    self.set_utility_memo(index, size, score, infiniteHorizon, horizon, obs, ("PASS", 0))
                    return ("PASS", 0)
            else:
                # print("HORIZON = {}".format(horizon))
                will_pop = self.pop_prob(index, size, obs)
                hyp_pump_not_pop = obs.copy()

                hyp_pump = obs.copy()
                hyp_pump[index] = [size + 1, True]

                decay = self.decay
            
                score_if_not = 1 + decay * self.getExpectedUtility(index, size+1, score+1, infiniteHorizon, horizon - 1, hyp_pump_not_pop)[1]
                # print("score pump not pop{}".format(score_if_not))
                score_if_pop = -score + decay * self.getExpectedUtility(index + 1, 0, 0, infiniteHorizon, horizon - 1, hyp_pump)[1]
                # print("score pump pop{}".format(score_if_pop))

                score_pump = will_pop * score_if_pop + (1-will_pop) * score_if_not
                # print("score pump {}".format(score_pump))
                hyp_pass = obs.copy()
                hyp_pass[index] = [size, False]
                score_pass = decay * self.getExpectedUtility(index + 1, 0, 0, infiniteHorizon, horizon - 1, hyp_pass)[1]
                # print("score_pass {}".format(score_pass))
                # print()
                if(score_pass > score_pump):
                    self.set_utility_memo(index, size, score, infiniteHorizon, horizon, obs, ("PASS", max(score_pump, score_pass)))
                    return ("PASS", max(score_pump, score_pass))
                else:
                    self.set_utility_memo(index, size, score, infiniteHorizon, horizon, obs, ("PUMP", max(score_pump, score_pass)))
                    return ("PUMP", max(score_pump, score_pass))

    def pointPerBalloon(self):
        points = [-1] * self.N
        
        for a in self.actions:
            for i in range(self.N):
                if(a[0] == i):
                    points[i] = a[-1]
        self.points = points
        return points

class LossAverseAgent(Agent):
    def __init__(self, balloons, horizon, decay):
        super().__init__(balloons, horizon, decay)
    

 

class NotLossAverseAgent(Agent):
    def __init__(self, balloons, horizon, decay):
        super().__init__(balloons, horizon, decay)
    
    def getExpectedUtility(self, index, size, score, infiniteHorizon, horizon, obs):
        #index: ranges from 0 to self.N - 1
        #size ranges from 0 to self.max
        #score ranges from 0 to self.max
        #infiniteHorizon False
        #horizon ranges from 0 to self.horizon
        #obs has self.N values, each has self.max values, and True or False (popped or not)
        # print("index {} size {} horizon {}".format(index, size, horizon))
        if(index < 0):
            raise Exception("index must be positive")
        if(score != size):
            raise Exception("score must be equal to size")
        for i in range(index):
            if(obs[i][0] == -1):
                raise Exception("not all balloons before {} was seen, {} is empty".format(index, i))
            if(obs[i][1] != True and obs[i][1] != False):
                raise Exception("balloon wasn't popped or passed, what")

        val = self.check_utility_memo(index, size, score, infiniteHorizon, horizon, obs)
        if(val != None):
            return val
        else:
            if(infiniteHorizon): 
                horizon = self.max * self.N
            
            if(horizon == 0):
                p = random.randint(0, 1)
                if p==1:
                    return ("PUMP", 0)
                if p==0:
                    return ("PASS", 0)
            elif(index >= self.N):
                return ("PASS", 0)
            elif(size == self.max - 1):
                return ("PASS", 0)
            elif(horizon == 1):
                will_pop = self.pop_prob(index, size, obs) 
                EU_PUMP = 0 * (1-will_pop) + (will_pop) * -1 * score
                EU_PASS = size

                if(EU_PUMP >= EU_PASS):
                    self.set_utility_memo(index, size, score, infiniteHorizon, horizon, obs, ("PUMP", EU_PUMP))
                    return ("PUMP", EU_PUMP)
                else:
                    self.set_utility_memo(index, size, score, infiniteHorizon, horizon, obs, ("PASS", 0))
                    return ("PASS", 0)
            else:
                # print("HORIZON = {}".format(horizon))
                will_pop = self.pop_prob(index, size, obs)
                hyp_pump_not_pop = obs.copy()

                hyp_pump = obs.copy()
                hyp_pump[index] = [size + 1, True]

                decay = self.decay
            
                score_if_not = 1 + decay * self.getExpectedUtility(index, size+1, score, infiniteHorizon, horizon - 1, hyp_pump_not_pop)[1]
                # print("score pump not pop{}".format(score_if_not))
                score_if_pop = -size + decay * self.getExpectedUtility(index + 1, 0, 0, infiniteHorizon, horizon - 1, hyp_pump)[1]
                # print("score pump pop{}".format(score_if_pop))

                score_pump = will_pop * score_if_pop + (1-will_pop) * score_if_not
                # print("score pump {}".format(score_pump))
                hyp_pass = obs.copy()
                hyp_pass[index] = [size, False]
                score_pass = decay * self.getExpectedUtility(index + 1, 0, score, infiniteHorizon, horizon - 1, hyp_pass)[1]
                # print("score_pass {}".format(score_pass))
                # print()
                if(score_pass > score_pump):
                    self.set_utility_memo(index, size, score, infiniteHorizon, horizon, obs, ("PASS", max(score_pump, score_pass)))
                    return ("PASS", max(score_pump, score_pass))
                else:
                    self.set_utility_memo(index, size, score, infiniteHorizon, horizon, obs, ("PUMP", max(score_pump, score_pass)))
                    return ("PUMP", max(score_pump, score_pass))

# # number of experiments
# K = 30

# #number of balloons
# N = 20
# obs = []
# dists = []
# decay = 0.5
# HORIZON = 8

# for i in range(K):
#     b = GaussianBalloons(N=N)
#     dists.append(b)
#     obs.append(b.getBallons())


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

# plt.xlabel('horizon')
# plt.ylabel('points')
# plt.title('points gained over horizons')
# plt.savefig('graphs/Gaussian/N={}decay={}K={}.pdf'.format(N, decay, K))


# # GAUSSIAN mean 7 std 1
# # BALLOONS: [5,6,5,7,5,6,7,5,6,7]
# # probs: [0.0000, 0.0000, 0.0000, 0.0013, 0.0212, 0.1352, 0.3410, 0.3426, 0.1370, 0.0217]