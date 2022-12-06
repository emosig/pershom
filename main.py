from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

from myFunction_old import * #DEPRECATED
from myPlotter import *
from myPolynomial import *
from EPG import *

#M -> R^2, M toro or sfera
class Variety:
    pass

class S2(Variety):
    def __init__(self):
        pass

class Torus(Variety):
    #[0,2pi]x[0,2pi] con le relazioni quozienti del toro

    #CONSTRUCTOR
    def __init__(self, precision):
        #il più grande sia il valore di precision più punti del toro considero
        self.precision = precision
        eps = 1/precision

        #Questo salva un array di coordinate x e un array di coordinate y di punti del toro
        self.point_coords = np.mgrid[0:2*np.pi:eps, 0:2*np.pi:eps]

    #GETTERS
    def get_point_coords(self):
        return self.point_coords

    def get_point_array(self):
        #Ritorna un array di coordinate invece che due array
        c = []
        for x in self.point_coords[0]:
            for y in self.point_coords[1]:
                c.append([x,y])
        return c



def main():
    #Ho cancellato alcune prove che non servono più
    #testing
    t = 6 
   
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
        #testing parser di myPolynomial
        msg1 = "(senx)(cos^3y)+8+seny"
        msg2 = "4+(sen^2x)(cos^2y)"
        msg_errore = "4(seny)(cosx)"
        print(parse(msg1))
        print(parse(msg2))
        print(parse(msg_errore))
        #FUNZIONA :))

    elif t == 3:
        #testing la classe Torus
        t = Torus(5)
        print(t.get_point_array())

    elif t == 4:
        monomio0 = Monomial(7,0,0,0,0) #7
        h0 = HomogComp([monomio0])
        monomio11 = Monomial(1,0,1,0,0) #cosx
        monomio12 = Monomial(1,0,0,0,1) #cosy
        h1 = HomogComp([monomio11, monomio12])
        monomio3 = Monomial(1,1,0,2,0) #senx(seny)^2
        h3 = HomogComp([monomio3])

        dic = {0:h0, 1:h1, 3:h3}
        polinomio = myPolynomial(dic)
        print(polinomio)
        
        #esempi più semplici
        poli = myPolynomial({1:h1}) 

        print(poli)
        print(poli.eval(np.pi,np.pi/2))

        #plot del polinomio al variare x,y
        x = np.linspace(-np.pi, np.pi,50)
        y = np.linspace(-np.pi, np.pi,50)
        #plt.plot([poli.eval(c,0) for c in x],color='red')
        #plt.plot([poli.eval(0,c) for c in y],color='blue')
        #plt.show()
        
        #ho fatto due prove, le funzioni si plottano bene --> assumo che funzionano
        #test del gradiente

        gr = poli.gradient()
        print(gr[0])
        print(gr[1])
        plt.plot([poli.eval(c,np.pi/2) for c in x],color='red')
        plt.plot([gr[0].eval(c,0) for c in x],color='blue')

        #fin qua funziona tutto come dovrebbe :)

    elif t == 5:
        #testing della classe Pareto
        #creo dei polinomi stupidi
        monomio11 = Monomial(1,0,1,0,0) #cosx
        monomio12 = Monomial(1,0,0,0,1) #cosy
        h1 = HomogComp([monomio11, monomio12])
        f1 = myPolynomial({1:h1})
        monomio2 = Monomial(-1,1,0,0,1) #-senxcosy
        h2 = HomogComp([monomio2])
        f2 = myPolynomial({2:h2})     

        pareto = EPG(50,100,f1,f2)
        pareto.crit()

    elif t == 6:
    #continuo a testare la classe Pareto ma stavolta ho il parser
    #Ho anche aggiunto un parametro shift alle funzioni di "eval" e al costruttore di EPG
    #in modo di poter spostare leggermente le funzioni per avere punti critici di f1,f2 disgiunti
    
    #Utilizzo i polinomi di Grazia
        g1 = parse("2(cos^2x) + 4(cosy)")
        g2 = parse("sen^3x+3sen^2y")

        #testing dei polinomi shiftati
        print(g1.eval(0,0))
        shift = np.pi/4
        print(g1.eval(0,0,shift))

        pareto = EPG(50,100,g1,g2,shiftf1=shift)
        pareto.crit()


        
    plt.show()
        
        
if __name__ == "__main__":
    main()