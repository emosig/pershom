import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from ourPolynomial import *
from itertools import product

CLUST_MAX_ITER = 50     #Massimo di iterazioni per il clustering
CLUST_VAR_STOP = 5      #Se in una iterazione di clustering aggiungo o tolgo 
                        #meno di questa quantità di punti, mi fermo

'''
#Metodo ausiliare per chiarezza nella funzione Pareto_crit. p = x[i].
def append_aux(p,f_1,f_2,ppc,f1ppc,f2ppc):
    ppc.append(p)
    f1ppc.append(f_1.eval(p[0],p[1]))
    f2ppc.append(f_2.eval(p[0],p[1]))
    return True     #Questo true è per il booleano 'aggiunto'
'''
    
#Controlla se un punto è pareto-critico con tolleranza = tol
def Pareto_crit(p,a,b,x,tol):
    x[p] = False

    #se ho un punto critico allora è anche pareto critico (infatti verifico con tolleranza p3)
    if (abs(a[0])<=tol and abs(a[1])<=tol):
        x[p]= True
        
    if(abs(b[0])<=tol and abs(b[1])<=tol):
        x[p]= True
    
    #troviamo ora i punti dell'insieme di Jacobi che non sono critici e sono Pareto Critici
    
    if abs(a[0])<=tol and abs(a[1])>tol:
        if b[1]/a[1]<=tol:                   #sarebbe lambda<=0
            x[p]= True
            
    if abs(a[1])<=tol and abs(a[0])>tol:
        if b[0]/a[0]<=tol:                   #sarebbe lambda<=0
            x[p]= True

    if abs(b[0])<=tol and abs(b[1])>tol:
        if a[1]/b[1]<=tol:                   #sarebbe lambda<=0
            x[p]= True

    if abs(b[1])<=tol and abs(b[0])>tol:
        if a[0]/b[0]<=tol:                   #sarebbe lambda<=0
            x[p]= True

    if abs(b[0])>tol and abs(b[1])>tol:
        if a[0]/b[0]<=tol and a[1]/b[1]<=tol:  #sarebbe lambda<=0
            x[p]= True

    if abs(a[0])>tol and abs(a[1])>tol:
        if b[0]/a[0]<=tol and b[1]/a[1]<=tol:  #sarebbe lambda<=0
            x[p]= True

    return x[p]     #Return True se lo ha aggiunto

#definisco la funzione che calcola i punti critici e i punti pareto critici, gli do in input già i gradienti e dentro EPG decido come calcolarli
def Pareto(f_1,f_2,p1,p2,p3):
    #costruisco una griglia di p1*p1 punti sul toro [0,2pi]x[0,2pi]
    grid = product(np.linspace(0,2*np.pi,p1),np.linspace(0,2*np.pi,p1))
    x = {p: False for p in grid}
    '''
    eps=2*np.pi/p1
    x=[]
    for i in np.arange(0,2*np.pi+eps,eps):
        for j in np.arange(0,2*np.pi+eps,eps):
            x.append([i,j])
    x=np.array(x)
    l=len(x)
    '''
    
    #p2=precisione per il calcolo dei punti critici
    #p3=precisione per il calcolo dei punti Pareto critici

    cr1=[]  #lista dei punti critici per f_1
    cr2=[]  #lista dei punti critici per f_2
    '''
    det=[]  #lista dei determinanti (anche se non serve)
    ppc=[]  #lista dei punti Pareto Critici
    f1ppc=[] #I punti che verrano plottati (immagini dei ppc)
    f2ppc=[]
    '''

    grf_1=f_1.gradient()
    grf_2=f_2.gradient()

    '''
    for i in range (0,l,1):
        a=[grf_1[0].eval(x[i][0],x[i][1]),grf_1[1].eval(x[i][0],x[i][1])]
        b=[grf_2[0].eval(x[i][0],x[i][1]),grf_2[1].eval(x[i][0],x[i][1])]
    '''
    for p in x.keys():
        a=[grf_1[0].eval(p[0],p[1]),grf_1[1].eval(p[0],p[1])]
        b=[grf_2[0].eval(p[0],p[1]),grf_2[1].eval(p[0],p[1])]

        if abs(a[0])<=p2 and abs(a[1])<=p2:       #punto critico per f_1
            cr1.append(p)
        if abs(b[0])<=p2 and abs(b[1])<=p2:       #punto critico per f_2
            cr2.append(p)
        
        #la seguente condizione mi dice che ho un punto dell'insieme di Jacobi
        det = a[0]*b[1]-a[1]*b[0]
        if abs(det)<=p3:
            Pareto_crit(p,a,b,x,p3)


    cr1=np.array(cr1)
    cr2=np.array(cr2)
    '''
    ppc=np.array(ppc)
    f1ppc=np.array(f1ppc)
    f2ppc=np.array(f2ppc)
    '''

    return cr1,cr2,x

def EPG(f_1,f_2,p1,p2,p3):  #Plot delle cose
    cr1,cr2,x,=Pareto(f_1,f_2,p1,p2,p3)
    ppc = [p for p,v in x.items() if v]     #Raccolge i punti di x che sono true
    m='gradient'
    fig,axes=plt.subplots(1,4)
    fig.set_size_inches(28,4)
    axes[0].scatter([p[0] for p in cr1],[p[1] for p in cr1],s=8)
    axes[0].set_title('Pt crit di f_1, '+m+' con tol='+str(p2))
    axes[1].scatter([p[0] for p in cr2],[p[1] for p in cr2],s=8)
    axes[1].set_title('Pt crit di f_2, '+m+' con tol='+str(p2))
    axes[2].scatter([p[0] for p in ppc],[p[1] for p in ppc],s=0.2)
    axes[2].set_title('Pt Pareto Critici, '+m+', tol='+str(p3))
    axes[3].scatter([f_1.eval(p[0],p[1]) for p in ppc],[f_2.eval(p[0],p[1]) for p in ppc],s=0.2)
    axes[3].set_title('Extended Pareto Grid')

    #TESTING (mi serve per capire la quantità di punti che stiamo plottando)
    return x

#Mi serve capire quale è il più piccolo rettangolo che contiene i punti pareto critici
def get_square(ppc,f1,f2):
    f1ppc = [f1.eval(p[0],p[1]) for p in ppc]
    f2ppc = [f2.eval(p[0],p[1]) for p in ppc]
    return min(f1ppc), max(f1ppc), min(f2ppc), max(f2ppc)

#Metodo per ricalcolare i punti di un cluster associato a noise con tolleranza minore
#Ad ogni iterazione riduco la tolleranza alla metà finché il cluster non diventa sufficientemente piccolo.
#Cosa vuol dire abbastanza piccolo? Si potrebbe specificare con un ulteriore parametro
#Per ora voglio ridurre i punti del cluster da 1/4 (vedere CONTROLLO alla fine del loop while)
def recalculate_cluster(cluster,x,f1,f2,tol):
    ridurre_ancora = True    #Finché non ho ridotto "abbastanza" i punti del cluster questo rimane True
    decresc = True
    i = 0       #Questo è un counter che arriva fino a 50 per evitare che il while vada avanti per sempre
    
    grf_1=f1.gradient()
    grf_2=f2.gradient()
    #old_ppc = []

    while ridurre_ancora and i < CLUST_MAX_ITER:
        #Qua decido se bisogna aumentare o ridurre la tolleranza
        if decresc:
            tol = tol/2
        else:
            tol = tol*3/2

        '''
        #Mi servono delle liste ausiliari di punti pareto-critici per controllare che sto
        #effettivamente riducendo la quantità di punti nel cluster
        temp_f1ppc = []
        temp_f2ppc = []
        temp_ppc = []
        '''
        counter = 0     #Conta quanti punti del cluster rimangono
        for p in cluster:
            a=[grf_1[0].eval(p[0],p[1]),grf_1[1].eval(p[0],p[1])]
            b=[grf_2[0].eval(p[0],p[1]),grf_2[1].eval(p[0],p[1])]
            if Pareto_crit(p,a,b,x,tol):
                counter +=1

        #CONTROLLO: HO EFFETTIVAMENTE RIDOTTO LA QUANTITÀ DI PUNTI NEL CLUSTER?
        if counter < len(cluster)/4:
            ridurre_ancora = False
        '''
        ###UN'ALTRO METODO PER RIDURRE LA TOLLERANZA. NON SI VEDONO DIFFERENZE CON L'ALTRO METODO
        #CONTROLLO: C'È UNA DIFFERENZA TROPPO GRANDE CON L'ITERAZIONE PRECEDENTE?
        if len(temp_ppc) < len(cluster)/4:
            decresc = False
            if abs(len(old_ppc)-len(temp_ppc)) < CLUST_VAR_STOP:    #Se ho variato molto poco in questa iterazione
                ridurre_ancora = False
            else:
                old_ppc = temp_ppc.copy()
        else:
            decresc = True
        '''
        i+=1
    return i    #Mi serve capire quante iterazioni ha fatto

#Applica il metodo sopra per i cluster "grandi" e plotta
def manage_clusters(cluster_list,x,f1,f2,tol):
    ppc = [p for p,v in x.items() if v]
    #Plot
    fig,axes=plt.subplots(1,2)
    fig.set_size_inches(21,6)
    axes[0].scatter([f1.eval(p[0],p[1]) for p in ppc],[f2.eval(p[0],p[1]) for p in ppc],s=0.2)
    axes[0].set_aspect('equal')
    axes[0].set_title('Vecchia Extended Pareto Grid con ' + str(len(ppc)) + ' punti')

    nclusters = 0   #Quanti clusters ho ridotto.
    '''
    old_points = [np.array([p,q]) for p,q in zip(f1ppc,f2ppc)]
    diff_points = old_points.copy()
    for line in cluster_list:
        for cl in line:
            #Quanto grandi sono i cluster che voglio trattare?
            if len(cl) > 50:
                iter = recalculate_cluster(cl,x,f1,f2,tol)
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
    '''

    for line in cluster_list:
        for cl in line:
            #Quanto grandi sono i cluster che voglio trattare?
            if len(cl) > 50:
                iter = recalculate_cluster(cl,x,f1,f2,tol)
                if iter < CLUST_MAX_ITER:   #Se l'algoritmo si è fermato prima del massimo di iterazioni
                    nclusters += 1  

    #Plot
    ppc = [p for p,v in x.items() if v]     #Nuovo ppc
    axes[1].scatter([f1.eval(p[0],p[1]) for p in ppc],[f2.eval(p[0],p[1]) for p in ppc],s=0.2)
    axes[1].set_aspect('equal')
    axes[1].set_title('Nuova Extended Pareto Grid con ' + str(len(ppc)) + ' punti')            

    return nclusters


