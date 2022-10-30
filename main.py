from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

from myFunction import *

#M -> R^2, M toro or sfera
class S2:
    def __init__(self):
        pass


class Torus:
    #[0,1]x[0,1] con le relazioni quozienti del toro
    def __init__(self):
        pass

def main():
    #testing
    t = 2
   
    if t == 0:
         #plotting a5
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(projection='3d')
    
        # questo pezzo qua dipinge una palla
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = np.cos(u)*np.sin(v)
        y = np.sin(u)*np.sin(v)
        z = np.cos(v)
        ax.plot_wireframe(x, y, z, color="r")
        
        plt.show()

    elif t == 1:
        #testing la classe dei polinomi in x,y
        p = Poly2var('1 2 3; 4 5 6; 7 8 9',3)
        print(p.get_homogenous_comps())
        print(p.get_degree())
        p.print()

        gr = p.gradient()
        gr[0].print()
        gr[1].print()

         #testing la funzione che valuta un polinomio
        q = Poly2var('5 1; 2 1')
        q.print()
        print(q.value(1,3))
        print(gr[0].value(1,0))
        print(gr[0].value(0,1))
        print(gr[0].value(0,1))

    else:
        #testing la classe myFunction f = (f1,f2) con f1,f2 Poly2var
        #testing costruttore generale
        f = myFunction('stocazzo','1 2 3; 4 5 6; 7 8 9','1 2; 4 5')
        #print(f.gradient())
        f.gradient()[0][0].print()
        f.gradient()[0][1].print()
        f.gradient()[1][0].print()
        f.gradient()[1][1].print()
        
       


if __name__ == "__main__":
    main()