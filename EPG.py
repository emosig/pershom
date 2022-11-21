#Classe che dipinge le EPG

from myPolynomial import *
from myPlotter import *

class EPG:
    #Prendo il codice di Grazia

    def __init__(self, p1, p2, f1, f2):
        #precisione per la griglia del toro
        self.torus_precision = p1
        #precisione per il calcolo del gradiente
        self.grad_precision = p2
        #i polinomi
        self.f1 = f1
        self.f2 = f2
        #i gradienti
        self.grf1 = f1.gradient()
        self.grf2 = f2.gradient()

        eps=2*np.pi/p1
        x=[]
        for i in np.arange(0,2*np.pi+eps,eps):
            for j in np.arange(0,2*np.pi+eps,eps):
                x.append([i,j])
        x=np.array(x)
        self.torus_grid = x
        self.torus_grid_len = len(x)

        #Cose da fare
        self.critf1 = []
        self.critf2 = []
        self.Pareto_critf1 = []
        self.Pareto_critf2 = []
        self.EPG = []

    def crit(self):
        #calcolo dei punti critici di f_1 e f_2 nella griglia
        cr1=[]  #lista dei punti critici di f_1
        cr2=[]  #lista dei punti critici di f_2
        for i in range (0,self.torus_grid_len,1):
            pos = self.torus_grid[i]
            a0,a1 = self.grf1[0].eval(pos[0],pos[1]),self.grf1[1].eval(pos[0],pos[1])
            b0,b1 = self.grf2[0].eval(pos[0],pos[1]),self.grf2[1].eval(pos[0],pos[1])
            if a0==0 and a1==0:
                cr1.append(pos)
            if b0==0 and b1==0:
                cr2.append(pos)
        self.critf1=np.array(cr1)
        self.critf2=np.array(cr2)

        #test
        plt.scatter([self.f1.eval(c[0],c[1]) for c in cr1],[self.f2.eval(c[0],c[1]) for c in cr1],color='red')
        plt.scatter([self.f1.eval(c[0],c[1]) for c in cr2],[self.f2.eval(c[0],c[1]) for c in cr2],color='blue')
        plt.show()
    
    def EPG(self):
        pass