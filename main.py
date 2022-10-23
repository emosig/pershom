from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

#M -> R^2, M torus or sphere
class S2:
    def __init__(self):
        pass


class Torus:
    def __init__(self):
        pass



def main():
    #tests

    #plotting a

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection='3d')

 
    # questo pezzo qua dipinge una palla
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    ax.plot_wireframe(x, y, z, color="r")
    
    plt.show()




if __name__ == "__main__":
    main()