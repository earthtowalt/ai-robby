import robby, time
rw = robby.World(10,10)
rw.graphicsOff()

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


re = 0.0
for i in xrange(100000):
    re = re + runGen(rw.strategyM)
re = re / 100000
print re