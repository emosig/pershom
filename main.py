from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

from myPlotter import *
from ProgrammaEPG import *

def main():
    #parametro di testing
    t = 1
   
    if t == 0:
        #Testing della classe myPlotter

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
        f1 = parse('senx + seny')
        f2 = parse('cosx + cosy')
        EPG(f1,f2,200,0.01,0.1,True)
        d = determinant(f1,f2)
        print(d)

    elif t == 2:
        pass

    elif t == 3:
        #testing ourPolynomial
        f = parse("senx + seny")
        print(f)
        
if __name__ == "__main__":
    main()