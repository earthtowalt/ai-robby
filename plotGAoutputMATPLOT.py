import matplotlib.pyplot as plt
import numpy as np

fname = 'GAoutput_00-00-04.txt'

with open(fname, 'r') as file:
    lines = file.readlines()
    x = [int(line.split()[0]) for line in lines]
    y = [int(line.split()[2]) for line in lines]
    avg = [int(line.split()[1]) for line in lines]

    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.plot(x, y, label="best")
    plt.plot(x, avg, label="average")
    plt.grid(axis='y')
    plt.title('Score vs Generation Number\n'+fname)

    plt.yticks(np.arange(-500, 501, 100.0))
    
    plt.legend()
    # xticks = range(0, int(max(x)), 10)
    # yticks = range(int(min(y+avg)), int(max(y+avg)), 10)
    # plt.xticks(xticks, xticks)
    # plt.yticks(yticks, yticks)

plt.show()