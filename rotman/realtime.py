import numpy as np
import matplotlib.pyplot as plt



for i in range(1000):
    y = np.random.random()
    plt.scatter(i, y)
    plt.pause(0.05)

