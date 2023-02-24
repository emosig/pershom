import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from scipy import optimize
import numdifftools as nd
from ourPolynomial import *

CLUST_MAX_ITER = 50     #Massimo di iterazioni per il clustering
CLUST_VAR_STOP = 5      #Se in una iterazione di clustering aggiungo o tolgo 
                        #meno di questa quantità di punti, mi fermo

#Metodo ausiliare per chiarezza nella funzione Pareto_crit. p = x[i].
def append_aux(p,f_1,f_2,ppc,f1ppc,f2ppc):
    ppc.append(p)
    f1ppc.append(f_1.eval(p[0],p[1]))
    f2ppc.append(f_2.eval(p[0],p[1]))
    return True     #Questo true è per il booleano 'aggiunto'

#Controlla se un punto è pareto-critico con tolleranza = tol
def Pareto_crit(p,a,b,f_1,f_2,ppc,f1ppc,f2ppc,tol):
    aggiunto = False    #Per evitare ripetere dei punti

    #se ho un punto critico allora è anche pareto critico (infatti verifico con tolleranza p3)
    if (abs(a[0])<=tol and abs(a[1])<=tol):
        aggiunto = append_aux(p,f_1,f_2,ppc,f1ppc,f2ppc)

    if(abs(b[0])<=tol and abs(b[1])<=tol) and not aggiunto:
        aggiunto = append_aux(p,f_1,f_2,ppc,f1ppc,f2ppc)
    
    #troviamo ora i punti dell'insieme di Jacobi che non sono critici e sono Pareto Critici
    
    if abs(a[0])<=tol and abs(a[1])>tol and not aggiunto:
        if b[1]/a[1]<=tol:                   #sarebbe lambda<=0
            aggiunto = append_aux(p,f_1,f_2,ppc,f1ppc,f2ppc)
            
    if abs(a[1])<=tol and abs(a[0])>tol and not aggiunto:
        if b[0]/a[0]<=tol:                   #sarebbe lambda<=0
            aggiunto = append_aux(p,f_1,f_2,ppc,f1ppc,f2ppc)

    if abs(b[0])<=tol and abs(b[1])>tol and not aggiunto:
        if a[1]/b[1]<=tol:                   #sarebbe lambda<=0
            aggiunto = append_aux(p,f_1,f_2,ppc,f1ppc,f2ppc)

    if abs(b[1])<=tol and abs(b[0])>tol and not aggiunto:
        if a[0]/b[0]<=tol:                   #sarebbe lambda<=0
            aggiunto = append_aux(p,f_1,f_2,ppc,f1ppc,f2ppc)

    if abs(b[0])>tol and abs(b[1])>tol and not aggiunto:
        if a[0]/b[0]<=tol and a[1]/b[1]<=tol:  #sarebbe lambda<=0
            aggiunto = append_aux(p,f_1,f_2,ppc,f1ppc,f2ppc)

    if abs(a[0])>tol and abs(a[1])>tol and not aggiunto:
        if b[0]/a[0]<=tol and b[1]/a[1]<=tol:  #sarebbe lambda<=0
            aggiunto = append_aux(p,f_1,f_2,ppc,f1ppc,f2ppc)

#definisco la funzione che calcola i punti critici e i punti pareto critici, gli do in input già i gradienti e dentro EPG decido come calcolarli
def Pareto(f_1,f_2,p1,p2,p3):
    #costruisco una griglia di p1*p1 punti sul toro [0,2pi]x[0,2pi]
    eps=2*np.pi/p1
    x=[]
    for i in np.arange(0,2*np.pi+eps,eps):
        for j in np.arange(0,2*np.pi+eps,eps):
            x.append([i,j])
    x=np.array(x)
    l=len(x)
    
    #p2=precisione per il calcolo dei punti critici
    #p3=precisione per il calcolo dei punti Pareto critici

    ppc=[]  #lista dei punti Pareto Critici
    cr1=[]  #lista dei punti critici per f_1
    cr2=[]  #lista dei punti critici per f_2
    det=[]  #lista dei determinanti (anche se non serve)
    f1ppc=[] #I punti che verrano plottati (immagini dei ppc)
    f2ppc=[]

    grf_1=f_1.gradient()
    grf_2=f_2.gradient()

    for i in range (0,l,1):
        a=[grf_1[0].eval(x[i][0],x[i][1]),grf_1[1].eval(x[i][0],x[i][1])]
        b=[grf_2[0].eval(x[i][0],x[i][1]),grf_2[1].eval(x[i][0],x[i][1])]
        
        if abs(a[0])<=p2 and abs(a[1])<=p2:       #punto critico per f_1
            cr1.append(x[i])
        if abs(b[0])<=p2 and abs(b[1])<=p2:       #punto critico per f_2
            cr2.append(x[i])
        
        det.append(a[0]*b[1]-a[1]*b[0])
        
        #la seguente condizione mi dice che ho un punto dell'insieme di Jacobi
        if abs(det[i])<=p3:
            Pareto_crit(x[i],a,b,f_1,f_2,ppc,f1ppc,f2ppc,p3)

    ppc=np.array(ppc)
    cr1=np.array(cr1)
    cr2=np.array(cr2)
    f1ppc=np.array(f1ppc)
    f2ppc=np.array(f2ppc)

    return ppc,cr1,cr2,x,f1ppc,f2ppc

def EPG(f_1,f_2,p1,p2,p3):  #Plot delle cose
    ppc,cr1,cr2,x,f1ppc,f2ppc=Pareto(f_1,f_2,p1,p2,p3)
    m='gradient'
    fig,axes=plt.subplots(1,4)
    fig.set_size_inches(28,4)
    axes[0].scatter([p[0] for p in cr1],[p[1] for p in cr1],s=8)
    axes[0].set_title('Pt crit di f_1, '+m+' con tol='+str(p2))
    axes[1].scatter([p[0] for p in cr2],[p[1] for p in cr2],s=8)
    axes[1].set_title('Pt crit di f_2, '+m+' con tol='+str(p2))
    axes[2].scatter([p[0] for p in ppc],[p[1] for p in ppc],s=0.2)
    axes[2].set_title('Pt Pareto Critici, '+m+', tol='+str(p3))
    axes[3].scatter([p for p in f1ppc],[q for q in f2ppc],s=0.2)
    axes[3].set_title('Extended Pareto Grid')

    #TESTING (mi serve per capire la quantità di punti che stiamo plottando)
    return f1ppc,f2ppc

#Mi serve capire quale è il più piccolo rettangolo che contiene i punti pareto critici
def get_square(f1ppc,f2ppc):
    return min(f1ppc), max(f1ppc), min(f2ppc), max(f2ppc)

#Metodo per ricalcolare i punti di un cluster associato a noise con tolleranza minore
#Ad ogni iterazione riduco la tolleranza alla metà finché il cluster non diventa sufficientemente piccolo.
#Cosa vuol dire abbastanza piccolo? Si potrebbe specificare con un ulteriore parametro
#Per ora voglio ridurre i punti del cluster da 1/4 (vedere CONTROLLO alla fine del loop while)
def recalculate_cluster(cluster,f_1,f_2,f1ppc,f2ppc,tol):
    ridurre_ancora = True    #Finché non ho ridotto "abbastanza" i punti del cluster questo rimane True
    decresc = True
    i = 0       #Questo è un counter che arriva fino a 50 per evitare che il while vada avanti per sempre
    
    grf_1=f_1.gradient()
    grf_2=f_2.gradient()
    old_ppc = []

    while ridurre_ancora and i < CLUST_MAX_ITER:
        #Qua decido se bisogna aumentare o ridurre la tolleranza
        if decresc:
            tol = tol/2
        else:
            tol = tol*3/2

        #Mi servono delle liste ausiliari di punti pareto-critici per controllare che sto
        #effettivamente riducendo la quantità di punti nel cluster
        temp_f1ppc = []
        temp_f2ppc = []
        temp_ppc = []

        for p in cluster:
            a=[grf_1[0].eval(p[0],p[1]),grf_1[1].eval(p[0],p[1])]       #Stessa cosa qua   
            b=[grf_2[0].eval(p[0],p[1]),grf_2[1].eval(p[0],p[1])]
            Pareto_crit(p,a,b,f_1,f_2,temp_ppc,temp_f1ppc,temp_f2ppc,tol)

        #CONTROLLO: HO EFFETTIVAMENTE RIDOTTO LA QUANTITÀ DI PUNTI NEL CLUSTER?
        #CONTROLLO: C'È UNA DIFFERENZA TROPPO GRANDE CON L'ITERAZIONE PRECEDENTE?
        if len(temp_ppc) < len(cluster)/4:
            decresc = False
            if abs(len(old_ppc)-len(temp_ppc)) < CLUST_VAR_STOP:    #Se ho variato molto poco in questa iterazione
                ridurre_ancora = False
            else:
                old_ppc = temp_ppc.copy()
        else:
            decresc = True
        i+=1
    
    return temp_f1ppc, temp_f2ppc, i    #Mi serve capire quante iterazioni ha fatto

#Applica il metodo sopra per i cluster "grandi" e plotta
def manage_clusters(cluster_list,f_1,f_2,f1ppc,f2ppc,tol):

    #Plot
    fig,axes=plt.subplots(1,2)
    fig.set_size_inches(21,6)
    axes[0].scatter([p for p in f1ppc],[q for q in f2ppc],s=0.2)
    axes[0].set_aspect('equal')
    axes[0].set_title('Vecchia Extended Pareto Grid con ' + str(len(f2ppc)) + ' punti')

    old_points = [np.array([p,q]) for p,q in zip(f1ppc,f2ppc)]
    diff_points = old_points.copy()
    nclusters = 0   #Quanti clusters ho ridotto.
    for line in cluster_list:
        for cl in line:
            #Quanto grandi sono i cluster che voglio trattare?
            if len(cl) > 50:
                temp_f1ppc, temp_f2ppc, iter = recalculate_cluster(cl,f_1,f_2,f1ppc,f2ppc,tol)
                if iter < CLUST_MAX_ITER:   #Se l'algoritmo si è fermato prima del massimo di iterazioni
                    nclusters += 1                
                    #Adesso tolgo sostituisco i cluster di dict_clusters per le versioni ridotte
                    #Sono convinto che c'è un modo migliore di fare questo però io non riesco a trovarlo
                    recalc_points = [np.array([p,q]) for p,q in zip(temp_f1ppc,temp_f2ppc)]
                    diff_points = list(set(map(tuple,diff_points)) - (set(map(tuple,cl))) - set(map(tuple,recalc_points)))

                    #Plot
                    axes[1].scatter([p[0] for p in recalc_points],[p[1] for p in recalc_points],s=0.8,color='red')

    #Plot
    axes[1].scatter([p[0] for p in diff_points],[p[1] for p in diff_points],s=0.2)
    axes[1].set_aspect('equal')
    axes[1].set_title('Nuova Extended Pareto Grid con ' + str(len(diff_points)) + ' punti')
    
    return f1ppc,f2ppc,nclusters


