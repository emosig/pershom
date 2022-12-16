#Classe che dipinge le EPG

from myPolynomial import *
from myPlotter import *

#Variabile per salvare i punti critici in un file
TEST_IN_FILE = False

class EPG:
    #Adatto il codice di Grazia

    #CONSTRUCTOR
    def __init__(self, p1, p2, p3, f1, f2, shiftf1=0, shiftf2=0):
        #precisione per la griglia del toro
        self.torus_precision = p1
        #precisione per il calcolo dei punti critici di f1,f2
        self.crit_precision = p2
        #precisione per il calcolo dei punti pareto-critici
        self.pcrit_precision = p3
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

        #Liste di pti critici in senso classico
        self.critf1 = []
        self.critf2 = []
        #Lista di pti Pareto-critici
        self.Pareto_crit = []
        #I polinomi f1, f2 valutati nelle liste precedenti
        self.f1critf1 = []
        self.f1critf2 = []
        self.f2critf1 = []
        self.f2critf2 = []
        self.f1paretocrit = []
        self.f2paretocrit = []
        
        self.EPG = []

    #GETTERS
    def get_torus_coords(self):
        return self.torus_grid

    #Per controllare che sta calcolando bene
    def get_gradient1(self):
        return self.grf1

    def get_gradient2(self):
        return self.grf2

    #OTHER
    #Tre funzioni che calcolano f1,f2 sui punti critici di f1, f2 e paretocritici
    def eval_crit1(self):
        for c in self.critf1:
            self.f1critf1.append(self.f1.eval(c[0],c[1],self.shiftf1))
            self.f2critf1.append(self.f2.eval(c[0],c[1],self.shiftf2))

    def eval_crit2(self):
        for c in self.critf2:
            self.f1critf2.append(self.f1.eval(c[0],c[1],self.shiftf1))
            self.f2critf2.append(self.f2.eval(c[0],c[1],self.shiftf2))

    def eval_paretocrit(self):
        for c in self.Pareto_crit:
            self.f1paretocrit.append(self.f1.eval(c[0],c[1],self.shiftf1))
            self.f2paretocrit.append(self.f2.eval(c[0],c[1],self.shiftf2))

    def calc(self):
        #calcolo dei punti critici di f_1 e f_2 e i punti pareto-critici
        eps = 1/self.crit_precision
        peps = 1/self.pcrit_precision
        cr1=[]  #lista dei punti critici di f_1
        cr2=[]  #lista dei punti critici di f_2
        pcr=[]  #lista dei punti pareto-critici
        for i in range (0,self.torus_grid_len,1):
            pos = self.torus_grid[i]
            
            #(a0,a1),(b0,b1) sono i gradienti di f1, f2 rispettivamente calcolati nel punto pos della griglia
            a0,a1 = self.grf1[0].eval(pos[0],pos[1],self.shiftf1),self.grf1[1].eval(pos[0],pos[1],self.shiftf1)
            b0,b1 = self.grf2[0].eval(pos[0],pos[1],self.shiftf2),self.grf2[1].eval(pos[0],pos[1],self.shiftf2)
            
            #Controllo se il punto pos è critico per f1
            if -eps < a0 and a0 < eps and -eps < a1 and a1 < eps:
                cr1.append(pos)
            if -eps < b0 and b0 < eps and -eps < b1 and b1 < eps:
                cr2.append(pos)

            #Controllo se il punto pos è pareto-critico
            if a0 == 0 and a1 != 0:     
                if abs(b0) < peps and b1/a1 < peps:
                    pcr.append(pos)
            if a1 == 0 and a0 != 0:
                if abs(b1) < peps and b0/a0 < peps:
                    pcr.append(pos)
            if b0 == 0 and b1 != 0:
                if abs(a0) < peps and a1/b1 < peps:
                    pcr.append(pos)
            if b1 == 0 and b0 != 0:
                if abs(a1) < peps and a0/b0 < peps:
                    pcr.append(pos)
            if b0 != 0 and b1 != 0:
                if abs(a0/b0-a1/b1) < peps and (a0/b0 < peps or a1/b1 < eps):
                    pcr.append(pos)
            #Grazia non aggiunge questo ultimo if. ¿Perché?
            if a0 != 0 and a1 != 0:
                if abs(b0/a0-b1/a1) < peps and (b0/a0 < peps or b1/a1 < eps):
                    pcr.append(pos)
            

        #Salvo i punti critici e paretocritici che ho appena calcolato
        self.critf1=np.array(cr1)
        self.critf2=np.array(cr2)
        self.Pareto_crit=np.array(pcr)

        #Salvo le immagini dei punti critici e paretocritici da plottare
        self.eval_crit1()
        self.eval_crit2()
        self.eval_paretocrit()

        #plotting
        plt.scatter(self.f1critf1, self.f2critf1, alpha = 0.5, color='black')
        plt.scatter(self.f1critf2, self.f2critf2, alpha = 0.5, color='black')
        plt.scatter(self.f1paretocrit, self.f2paretocrit, s=0.3, alpha = 0.3, color='green')
        title = "Punti considerati = {}. Tolleranze = ({},{}). Shift in f1 di {}"
        plt.title(title.format(self.torus_grid_len, self.crit_precision, self.pcrit_precision, self.shiftf1))
        plt.show()

        if TEST_IN_FILE:
            doc = open("list_crit_points.txt","w")
            doc.write("CR1:" + '\n')
            for crit in cr1:
                doc.write(str(crit)+'\n')
            doc.write("CR2:" + '\n')
            for crit in cr2:
                doc.write(str(crit)+'\n')
            doc.close()


    def EPG(self):
        pass