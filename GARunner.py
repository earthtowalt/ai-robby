import random
import time
import math

import robby 
import numpy as np
import matplotlib.pyplot as plt

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

POP_SIZE = 200
population = [generateRandomStrategy() for i in xrange(POP_SIZE)]

GENERATIONS = 1000
STEPS = 200
CANS = 0.5

output_file = 'GAoutput_{0}.txt'.format(time.strftime("%H-%M-%S",time.localtime()))
print("writing to file: " + output_file)

def runGen(strategy, steps=STEPS, init=CANS):
    rw.graphicsOff()
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
for g in xrange(GENERATIONS): 
    results = []

    # loop over population
    for strategy in population: 
        results.append((runGen(strategy, steps=STEPS, init=CANS), strategy))

    # sort the results
    results.sort(key=lambda x: x[0], reverse=True)
    # print(list(map(lambda x: x[0], results[:10])))

    # get metrics on the population
    averageFitness = sum(map(lambda x: x[0], results)) / len(results)
    bestFitness = results[0][0]
    bestStrategy = results[0][1]
    # print("best fitness: " + str(bestFitness))
    
    # get the sorted population from the results
    population = list(map(lambda x: x[1], results))

    # every 10 generations, log the best performer
    if (g % 10 == 0 or g == GENERATIONS - 1): 
        with open(output_file, 'a') as file:
            file.write("{0} {1} {2} {3}\n".format(g, averageFitness, bestFitness, bestStrategy))

    # every 20 generations, demo the best performer
    if (g % 20 == 0 or g == GENERATIONS - 1):
        rw.demo(bestStrategy, steps=STEPS, init=CANS)

    # select next generation / mutate / crossover -- Jack
    # take the top 4 from previous generation

    indicies = []
    newPopulation = population[:10]
    for p in range((len(population) - len(newPopulation)) // 2):
        # get parents

        # linear distribution
        # raw_indicies = np.array(list(reversed(range(len(population)))), dtype='float') + 1

        # exponential distribution
        # raw_indicies = np.exp((500 - np.arange(0, len(population), 1, dtype='float')) / 90) - 25

        # quadratic distribution
        raw_indicies = np.array(list(reversed(range(len(population)))), dtype='float') ** 2

        p = raw_indicies / np.sum(raw_indicies) 
        parent1, parent2 = np.random.choice(population, size=2, replace=False, p=p)

        indicies.append(population.index(parent1))
        indicies.append(population.index(parent2))

        # def randIndi(size):
        #     randNum = random.randint(0, size * (size - 1) / 2)
        #     N = math.floor(math.sqrt(2 * randNum))
        #     if (N * (N + 1) <= 2 * randNum and 2 * randNum < (N + 1) * (N + 2)):
        #         return N - 1
        #     else :
        #         return N

        # N = len(population)
        # parent1 = population[N - 1 - int(randIndi(N))]
        # parent2 = population[N - 1 - int(randIndi(N))]

        # print('parent1 index:',population.index(parent1))
        # print('parent2 index:',population.index(parent2))

        # cross the parents' Genome
        cross_point = random.randint(0, len(parent1)-1)
        child1 = parent1[:cross_point] + parent2[cross_point:]
        child2 = parent2[:cross_point] + parent1[cross_point:]

        # randomly mutate
        for i in range(len(child1)):
            if (random.random() > 0.990):
                child1 = child1[:i] + str(random.choice(list(xrange(7)))) + child1[i+1:]
            if (random.random() > 0.990):
                child2 = child2[:i] + str(random.choice(list(xrange(7)))) + child2[i+1:]

        assert(len(child1) == 243)
        assert(len(child2) == 243)
        newPopulation.append(child1)
        newPopulation.append(child2)

    population = newPopulation
    assert(len(population) == POP_SIZE)

    # show index distribution for parent selection
    # print('making histogram')
    # print('num indicies:', len(indicies))
    # plt.hist(indicies, density=True, bins=20)
    # plt.show()
    # print('made hist')
    # raw_input()




