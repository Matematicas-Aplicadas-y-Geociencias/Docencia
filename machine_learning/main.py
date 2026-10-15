import numpy as np
import matplotlib.pyplot as plt
def main():
    # myDictionary = {
    #     "Time": t,
    #     "Position": x,
    #     "Position_Unit": "m",
    #     "Time_Unit": "s",
    #     "Position_Absolute_Uncertainty": 0.05,
    #     "Time_Absolute_Absolute_Uncertainty": 0.01,
    #     "Position_Probability_Density": "Pearson_IV",
    #     "Scale": "Cardinal",
    #     "RangeMax": 0.4,
    #     "RangeMin": 0.1,
    # }
    t= np.arange(0,4*np.pi, 0.1)
    x1 = np.sin(t)
    x2 = np.cos(t)
    x3 = -np.sin(t)
    x4 = t**2
    C = np.corrcoef([x1,x2,x3,x4])

    plt.imshow(C, aspect="auto")
    plt.xlabel("Index")
    plt.xticks(range(0,4), ["x1","x2","x3","x4"])
    plt.yticks(range(0,4), ["x1","x2","x3","x4"])
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    main()
