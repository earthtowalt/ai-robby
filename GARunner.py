import random
import time

import robby 
rw = robby.World(10,10)

# rw.demo(rw.strategyM)


# create robby world

# instantiate GA population (list of strategy strings) -- Jack 
# - size 200
# - crossover 1.0 (100% single point)
# - mutation: 0.005 per locus
# - actions per step: 200
# - generations: 500
# - total reward summed over 100 sessions

def generateRandomStrategy():
    return ''.join([str(random.choice(list(xrange(7)))) for i in xrange(243)])

population = [generateRandomStrategy() for i in xrange(200)]

generation_count = 500

output_file = 'GAoutput_{0}.txt'.format(time.strftime("%H-%M-%S",time.localtime()))

def runGen(strategy, steps=200, init=0.50):
    if type(strategy) is not str or len(strategy) != 243:
        raise Exception("strategy is not a string of length 243")
    for char in strategy:
        if char not in "0123456":
            raise Exception("strategy contains a bad character: '%s'" % char)
    if type(steps) is not int or steps < 1:
        raise Exception("steps must be an integer > 0")
    if type(init) is str:
        # init is a config file
        rw.load(init)
    elif type(init) in [int, float] and 0 <= init <= 1:
        # init is a can density
        rw.goto(0, 0)
        rw.distributeCans(init)
    else:
        raise Exception("invalid initial configuration")
    history = []
    cycleDetected = False
    cycleStart = 0
    reward = 0
    for i in xrange(steps):
        p = rw.getPerceptCode()
        action = robby.POSSIBLE_ACTIONS[int(strategy[p])]
        reward += rw.performAction(action)
    return reward



# loop over #generations 
for g in xrange(generation_count): 
    results = []
    # loop over population
    for strategy in population: 
        results.append((runGen(strategy), strategy))
        # -- modified demo() -- Shepard
        # create reward counter
        # loop over #actions
            # look to get percept
            # perform action and update reward

    # log and display results
    results.sort()
    
    averageFitness = sum(map(lambda x: x[0], results))
    bestFitness = results[-1][0]
    bestStrategy = results[-1][1]

    # every 10 generations, log the best performer
    if (g % 10 == 0 or g == generation_count - 1): 
        with open(output_file, 'a') as file:
            file.write("{0} {1} {2} {3}\n".format(g, averageFitness, bestFitness, bestStrategy))

    # every 20 generations, demo the best performer
    if (g % 20 == 0 or g == generation_count - 1):
        rw.demo(bestStrategy)

    # select next generation / mutate / crossover -- Jack
    # newPopulation = []
    # for p in range(len(population)):
    #     # get parents





