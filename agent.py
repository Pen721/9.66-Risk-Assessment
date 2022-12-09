# a bayesian agent that runs calculations based on distribution
from dist import Gaussian, Geometric, Uniform, Limit

class Agent():
    def __init__(self, balloons):
        #first assuming everything is gaussian
        self.max = 10
        self.min = 0

        hyp_mean = [i for i in range(self.max)]
        hyp_std = [i for i in range(1, 3+1)]

        p = 1.0/(len(hyp_mean) * len(hyp_std))
        self.balloons = balloons
        self.N = len(self.balloons)
        self.observed = [[-1, -1] for i in range(self.max)]
        self.hypothesis = {(m, std): [p, Gaussian(mean=m, std=std)] for m in hyp_mean for std in hyp_std}
        #ML could specify the hypothesis space / relative weighing of things through hierarchical learning but we assume uniform for now
       
    def pop_prob(self, index, size):
        will_pop = 0.0
        for key in self.hypothesis:
            p = self.hypothesis[key][0]
            dist = self.hypothesis[key][1]
            p_prev = 1.0
            for item in self.observed:
                bal_size = item[0]
                popped = item[1]
                if(popped): 
                    p_prev *= dist.cdf(bal_size -1, bal_size)
                else:
                    p_prev *= dist.cdf(bal_size, self.max)
            #P(will pop | haven't popped yet) = p(haven't popped | will pop) * p(will  pop) / (p(haven't popped | will pop) + p(haven't popped | won't pop))
            P_will_pop = dist.cdf(size, size+1) / dist.cdf(size, self.max)
            will_pop += P_will_pop * p * p_prev
        print("Prop will pop: ")
        print(will_pop)
        return will_pop

    def pump(self, index, size):
        will_pop = self.pop_prob(index, size)
        #we could do a better method that takes into account expected value or something in the future
        if(will_pop > 0.5):
            return False
        else:
            return True
    
    def balloonpops(self, index, size):
        if(self.balloons[index] > size):
            return False
        return True

    def play(self):
        over = False
        size = 0
        index = 0
        points = 0
        points_from_this_balloon = 0

        while(not over):
            # print("index {} size {}".format(index, size))
            if(index >= self.N):
                break

            #playing the same balloon
            if(not self.balloonpops(index, size)):
                if(size >= self.max):
                    print("REACHED MAX SIZE")
                    points += points_from_this_balloon
                    points_from_this_balloon = 0
                    #TODO: There might be a bug from the dist where all balloons pop at 10
                    index += 1
                    size = 0
                elif(self.pump(index, size)):
                    # print("PUMPED!")
                    size += 1
                    points_from_this_balloon += 1
                else:
                    print("PASSED")
                    #passed :(
                    points += points_from_this_balloon
                    points_from_this_balloon = 0
                    index +=1
                    size = 0
                    self.observed.append([size, False])
            else:
                print("POPPED")
                #balloon popss
                self.observed.append([size, True])
                index += 1
                size = 0
                points_from_this_balloon = 0
                

        print("POINTS: {}".format(points))


a = Agent([5,6,5,7,5,6,7,5,6,7])
a.play()

# GAUSSIAN mean 7 std 1
# BALLOONS: [5,6,5,7,5,6,7,5,6,7]
# probs: [0.0000, 0.0000, 0.0000, 0.0013, 0.0212, 0.1352, 0.3410, 0.3426, 0.1370, 0.0217]