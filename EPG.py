#Classe che dipinge le EPG

from myPolynomial import *
from myPlotter import *

class EPG:
    #Prendo il codice di Grazia

    #CONSTRUCTOR
    def __init__(self, p1, p2, f1, f2, shiftf1=0, shiftf2=0):
        #precisione per la griglia del toro
        self.torus_precision = p1
        #precisione per il calcolo del gradiente
        self.grad_precision = p2
        #i polinomi
        self.f1 = f1
        self.f2 = f2
        self.shiftf1 = shiftf1
        self.shiftf2 = shiftf2
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

    #GETTERS
    def get_torus_coords(self):
        return self.torus_grid

    def crit(self):
        #calcolo dei punti critici di f_1 e f_2 nella griglia USANDO IL PARAMETRO DI PRECISIONE
        eps = 1/self.grad_precision
        cr1=[]  #lista dei punti critici di f_1
        cr2=[]  #lista dei punti critici di f_2
        for i in range (0,self.torus_grid_len,1):
            pos = self.torus_grid[i]
            a0,a1 = self.grf1[0].eval(pos[0],pos[1],self.shiftf1),self.grf1[1].eval(pos[0],pos[1],self.shiftf1)
            b0,b1 = self.grf2[0].eval(pos[0],pos[1],self.shiftf2),self.grf2[1].eval(pos[0],pos[1],self.shiftf2)
            if -eps < a0 and a0 < eps and -eps < a1 and a1 < eps:
                cr1.append(pos)
            if -eps < b0 and b0 < eps and -eps < b1 and b1 < eps:
                cr2.append(pos)
        self.critf1=np.array(cr1)
        self.critf2=np.array(cr2)

        #test
        plt.scatter([self.f1.eval(c[0],c[1],self.shiftf1) for c in cr1],[self.f2.eval(c[0],c[1],self.shiftf1) for c in cr1],alpha = 0.5,color='red')
        plt.scatter([self.f1.eval(c[0],c[1],self.shiftf2) for c in cr2],[self.f2.eval(c[0],c[1],self.shiftf2) for c in cr2],alpha = 0.5,color='blue')
        plt.show()
        #i pti critici me li scrivo in un file perché sono in tanti
        doc = open("list_crit_points.txt","w")
        doc.write("CR1:" + '\n')
        for crit in cr1:
            doc.write(str(crit)+'\n')
        doc.write("CR2:" + '\n')
        for crit in cr2:
            doc.write(str(crit)+'\n')
        doc.close


    
    def EPG(self):
        pass