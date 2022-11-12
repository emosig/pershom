from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

from myFunction import *
from myPlotter import *

#M -> R^2, M toro or sfera
class Variety:
    pass

class S2(Variety):
    def __init__(self):
        pass

class Torus(Variety):
    #[0,1]x[0,1] con le relazioni quozienti del toro

    #CONSTRUCTOR
    def __init__(self, precision):
        #il più grande sia il valore di precision più punti del toro considero
        self.precision = precision
        eps = 1/precision

        #Questo salva un array di coordinate x e un array di coordinate y di punti del toro
        self.point_coords = np.mgrid[0:1:eps, 0:1:eps]

    #GETTERS
    def get_point_coords(self):
        return self.point_coords



def main():
    #testing
    t = 0
   
    if t == 0:
        #Basta di plottare palle! Testing della classe myPlotter

        #Con questi dati lui fa una cosa orribile
        x = [2.50, -1.23, 4.02, 3.25, -5.00, 4.40]
        y = [34, 62, -49, -22, 13, 19]

        #Con dati stupidi lui si comporta bene
        #x = [2, 1, 0, -1, -2, -3, -4, -5]
        #y = [-1, 0, 1, 2, 3, 4, 5, 6]

        plotter = myPlotter(x,y)
        plotter.plot('poly5')
        plotter.plot('sine2') #per la prima scelta di dati questo qua sembra funzionare un po' meglio

    elif t == 1:
        #testing la classe dei polinomi in x,y
        #p = Poly2var('1 2 3; 4 5 6; 7 8 9',3)
        coeffs = None
        p = Poly2var(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), 3)
        print(p.get_homogenous_comps())
        print(p.get_degree())
        p.print()

        gr = p.gradient()
        gr[0].print()
        gr[1].print()

         #testing la funzione che valuta un polinomio
        q = Poly2var(np.array([[5,1],[2,1]]))
        q.print()
        print(q.value(1,3))
        print(gr[0].value(1,0))
        print(gr[0].value(0,1))
        print(gr[0].value(0,1))

    elif t == 2:
        #testing la classe myFunction f = (f1,f2) con f1,f2 Poly2var
        #testing costruttore generale
        f1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        f2 = np.array([[5,1],[2,1]])
        f = myFunction('Torus',f1,f2)

        #Testing gradient of myFunction
        f.gradient()[0][0].print()
        f.gradient()[0][1].print()
        f.gradient()[1][0].print()
        f.gradient()[1][1].print()
        print(f.gradient_value(1,1))

    elif t == 3:
        #testing la classe Torus
        t = Torus(5)
        print(t.get_point_coords())


        
        


if __name__ == "__main__":
    main()