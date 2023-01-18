#Classe che dipinge le EPG

from ourPolynomial import *
from myPlotter import *
from scipy import signal

#Variabile che utilizzo per testare roba
TEST_IN_FILE = False
TEST_A_FEW_PLOTS = False
ANTIALIASING = True

#Metodo ausiliare per dividere una matrice in blocchi.
#Il parametro coord_matrix è per matrici di coordinate (n,n,2) come torus_matrix
def split_matrix(arr, n, coord_matrix = False):
        h = arr.shape[0]
        if coord_matrix:
            blocks = (arr.reshape(h//n, n, -1, n, 2).swapaxes(1, 2).reshape(-1, n, n, 2))
        else:
            blocks = (arr.reshape(h//n, n, -1, n).swapaxes(1, 2).reshape(-1, n, n))
        return blocks

class EPG:
    #Adatto il codice di Grazia

    #CONSTRUCTOR
    def __init__(self, p1, p2, p3, f1, f2, shiftf1=0, shiftf2=0, block_size = None):
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
        if ANTIALIASING:
            self.block_size = block_size

        eps=2*np.pi/p1
        x=[]
        for i in np.arange(0,2*np.pi+eps,eps):
            for j in np.arange(0,2*np.pi+eps,eps):
                x.append([i,j])
        x=np.array(x)

        self.torus_matrix = x.reshape((p1+1,p1+1,2))
        #Questa matrice avra True sui punti le cui immagini sto plottando
        self.torus_characteristic_matrix = np.full((p1+1,p1+1), False)

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

    #GETTERS
    def get_torus_coords(self):
        return self.torus_grid

    #Per controllare che sta calcolando bene
    def get_gradient1(self):
        return self.grf1

    def get_gradient2(self):
        return self.grf2

    #OTHER
    #Un metodo ausiliare per alleggerire calc
    #Marco i punti che sono da plottare
    def append_and_mark(self,arr,i,j):
        arr.append(self.torus_matrix[i][j])
        self.torus_characteristic_matrix[i][j] = True

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

    #Procedura di antialising con blocchi nxn
    def antialising(self, n):
        torus_blocks = split_matrix(self.torus_matrix,n,coord_matrix = True)
        char_blocks = split_matrix(self.torus_characteristic_matrix,n)
        return torus_blocks, char_blocks

    def plot(self):
        plt.scatter(self.f1critf1, self.f2critf1, alpha = 0.5, color='black')
        plt.scatter(self.f1critf2, self.f2critf2, alpha = 0.5, color='black')
        plt.scatter(self.f1paretocrit, self.f2paretocrit, s=0.3, alpha = 0.3, color='green')
        title = "Punti considerati = {}. Tolleranze = ({},{}). Shift in f1 di {}"
        shape = self.torus_matrix.shape
        plt.title(title.format(shape[0]*shape[1], self.crit_precision, self.pcrit_precision, self.shiftf1))

    #Questa serve per testare diversi parametri in una sola volta
    def plot_various(self):
        #Definisco 2 plots
        fig, axs = plt.subplots(2, 1)
        #Main plot
        axs[0].scatter(self.f1critf1, self.f2critf1, alpha = 0.5, color='black')
        axs[0].scatter(self.f1critf2, self.f2critf2, alpha = 0.5, color='black')
        axs[0].scatter(self.f1paretocrit, self.f2paretocrit, s=0.3, alpha = 0.3, color='green')
        #Savitzky-Golay filter
        yfilt = signal.savgol_filter(self.f2paretocrit, window_length=31, polyorder=3, mode="nearest")
        axs[1].scatter(self.f1critf1, self.f2critf1, alpha = 0.5, color='black')
        axs[1].scatter(self.f1critf2, self.f2critf2, alpha = 0.5, color='black')
        axs[1].scatter(self.f1paretocrit, yfilt, s=0.3, alpha = 0.3, color='green')

        #Per ora non funziona >:(

    def plot_antialising(self, torus_blocks, char_blocks):
        pass

    def calc(self):
        #calcolo dei punti critici di f_1 e f_2 e i punti pareto-critici
        eps = 1/self.crit_precision
        peps = 1/self.pcrit_precision
        cr1=[]  #lista dei punti critici di f_1
        cr2=[]  #lista dei punti critici di f_2
        pcr=[]  #lista dei punti pareto-critici
        
        for i in range (0,self.torus_precision+1,1):
            for j in range (0,self.torus_precision+1,1):
                pos = self.torus_matrix[i][j]
            
                #(a0,a1),(b0,b1) sono i gradienti di f1, f2 rispettivamente calcolati nel punto pos della griglia
                a0,a1 = self.grf1[0].eval(pos[0],pos[1],self.shiftf1),self.grf1[1].eval(pos[0],pos[1],self.shiftf1)
                b0,b1 = self.grf2[0].eval(pos[0],pos[1],self.shiftf2),self.grf2[1].eval(pos[0],pos[1],self.shiftf2)
                
                #Controllo se il punto pos è critico per f1
                if -eps < a0 and a0 < eps and -eps < a1 and a1 < eps:
                    self.append_and_mark(cr1,i,j)
                if -eps < b0 and b0 < eps and -eps < b1 and b1 < eps:
                    self.append_and_mark(cr2,i,j)

                #Controllo se il punto pos è pareto-critico
                if a0 == 0 and a1 != 0:     
                    if abs(b0) < peps and b1/a1 < peps:
                        self.append_and_mark(pcr,i,j)
                if a1 == 0 and a0 != 0:
                    if abs(b1) < peps and b0/a0 < peps:
                        self.append_and_mark(pcr,i,j)
                if b0 == 0 and b1 != 0:
                    if abs(a0) < peps and a1/b1 < peps:
                        self.append_and_mark(pcr,i,j)
                if b1 == 0 and b0 != 0:
                    if abs(a1) < peps and a0/b0 < peps:
                        self.append_and_mark(pcr,i,j)
                if b0 != 0 and b1 != 0:
                    if abs(a0/b0-a1/b1) < peps and (a0/b0 < peps or a1/b1 < eps):
                        self.append_and_mark(pcr,i,j)
                #Grazia non aggiunge questo ultimo if. ¿Perché?
                if a0 != 0 and a1 != 0:
                    if abs(b0/a0-b1/a1) < peps and (b0/a0 < peps or b1/a1 < eps):
                        self.append_and_mark(pcr,i,j)

        #Salvo i punti critici e paretocritici che ho appena calcolato
        self.critf1=np.array(cr1)
        self.critf2=np.array(cr2)
        self.Pareto_crit=np.array(pcr)

        #Salvo le immagini dei punti critici e paretocritici da plottare
        self.eval_crit1()
        self.eval_crit2()
        self.eval_paretocrit()

        if ANTIALIASING:
            #Tolgo la ultima fila e l'ultima colonna perché altrimenti i blocchi non si fanno bene
            self.torus_matrix = self.torus_matrix[:-1,:-1]
            self.torus_characteristic_matrix = self.torus_characteristic_matrix[:-1,:-1]
            blocks, char_blocks = self.antialising(self.block_size)

        #plotting
        if TEST_A_FEW_PLOTS:
            self.plot_various()
        elif ANTIALIASING:
            self.plot_antialising(blocks,char_blocks)
        else:
            self.plot()  
        
        #Ritorno le liste di punti critici per risparmiare calcoli
        return cr1,cr2

    def run(self):
        cr1,cr2 = self.calc()
        
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