import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from ourPolynomial import *
from itertools import product
from Rette import *

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
#definisco la funzione che calcola i punti critici
def Critic(grf_1,grf_2,p1):

    eps=2*np.pi/p1
    
    grid=[]
    for i in np.arange(0,2*np.pi+eps,eps):
        for j in np.arange(0,2*np.pi+eps,eps):
            grid.append([i,j])
    
    cr1=[]  #lista dei punti critici per f_1
    cr2=[]  #lista dei punti critici per f_2

    for p in grid:
        a=[grf_1[0].eval(p[0],p[1]),grf_1[1].eval(p[0],p[1])]
        b=[grf_2[0].eval(p[0],p[1]),grf_2[1].eval(p[0],p[1])]

        if abs(a[0])<=0.001 and abs(a[1])<=0.001:       #punto critico per f_1
            cr1.append(p)
        if abs(b[0])<=0.001 and abs(b[1])<=0.001:       #punto critico per f_2
            cr2.append(p)

    cr1=np.array(cr1)
    cr2=np.array(cr2)

    return cr1,cr2

#Controlla se un punto p è pareto-critico; input: [a=gradiente di f1 calcolato in p] , [b=gradiente di f2 calcolato in p] , [tol=tolleranza nel verificare condizione]
def Pareto_crit(a,b,tol):
    test = False

    #se ho un punto critico allora è anche pareto critico (infatti verifico con tolleranza p3)
    if (abs(a[0])<=tol and abs(a[1])<=tol):
        test = True
        
    if(abs(b[0])<=tol and abs(b[1])<=tol):
        test = True 

    #troviamo ora i punti dell'insieme di Jacobi che non sono critici e sono Pareto Critici
    if abs(a[0])<=tol and abs(a[1])>tol:
        if b[1]/a[1]<=tol:                   #sarebbe lambda<=0
            test = True
            
    if abs(a[1])<=tol and abs(a[0])>tol:
        if b[0]/a[0]<=tol:                   #sarebbe lambda<=0
            test = True

    if abs(b[0])<=tol and abs(b[1])>tol:
        if a[1]/b[1]<=tol:                   #sarebbe lambda<=0
            test = True

    if abs(b[1])<=tol and abs(b[0])>tol:
        if a[0]/b[0]<=tol:                   #sarebbe lambda<=0
            test = True

    if abs(b[0])>tol and abs(b[1])>tol:
        if a[0]/b[0]<=tol and a[1]/b[1]<=tol:  #sarebbe lambda<=0
            test = True

    if abs(a[0])>tol and abs(a[1])>tol:
        if b[0]/a[0]<=tol and b[1]/a[1]<=tol:  #sarebbe lambda<=0
            test = True

    return test     #Return True se lo ha aggiunto

def Pareto(grf_1,grf_2,p1,p3):  #in input i gradienti
    #costruisco una griglia di p1*p1 punti sul toro [0,2pi]x[0,2pi]
    #grid = product(np.linspace(0,2*np.pi,p1),np.linspace(0,2*np.pi,p1))
    eps=2*np.pi/p1
    grid=[]
    for i in np.arange(0,2*np.pi+eps,eps):
        for j in np.arange(0,2*np.pi+eps,eps):
            grid.append((i,j))

    x = {p: False for p in grid}
    '''
    det=[]  #lista dei determinanti (anche se non serve)
    ppc=[]  #lista dei punti Pareto Critici
    f1ppc=[] #I punti che verrano plottati (immagini dei ppc)
    f2ppc=[]
    
    for i in range (0,l,1):
        a=[grf_1[0].eval(x[i][0],x[i][1]),grf_1[1].eval(x[i][0],x[i][1])]
        b=[grf_2[0].eval(x[i][0],x[i][1]),grf_2[1].eval(x[i][0],x[i][1])]
    '''
    for p in x.keys():
        a=[grf_1[0].eval(p[0],p[1]),grf_1[1].eval(p[0],p[1])]
        b=[grf_2[0].eval(p[0],p[1]),grf_2[1].eval(p[0],p[1])]
        
        #la seguente condizione mi dice che ho un punto dell'insieme di Jacobi
        det = a[0]*b[1]-a[1]*b[0]

        if abs(det)<=p3:
            x[p]=Pareto_crit(a,b,p3)
    '''
    ppc=np.array(ppc)
    f1ppc=np.array(f1ppc)
    f2ppc=np.array(f2ppc)
    '''
    return x

def EPG(f1,f2,p1,p3):

    npunt=p1*p1
    eps=2*np.pi/p1

    grf_1=f1.gradient()
    grf_2=f2.gradient()

    cr1,cr2=Critic(grf_1,grf_2,p1)
    x=Pareto(grf_1,grf_2,p1,p3)
    ppc = [p for p,v in x.items() if v]     #Raccolge i punti di x che sono true
    epg=[]
    for p in ppc:
        epg.append([f1.eval(p[0],p[1]),f2.eval(p[0],p[1])])
    
    improper_arcs=[]
    #aggiungo le semirette
    maxx=max([abs(p[0]) for p in epg])
    maxy=max([abs(p[1]) for p in epg])

    for p in cr1:
        f1_p=f1.eval(p[0],p[1])
        f2_p=f2.eval(p[0],p[1])
        for i in np.arange (eps, 2*maxx+1, eps):
            improper_arcs.append([f1_p,f2_p+i])
    
    for p in cr2:
        f1_p=f1.eval(p[0],p[1])
        f2_p=f2.eval(p[0],p[1])
        for i in np.arange (eps, 2*maxy+1, eps):
            improper_arcs.append([f1_p+i,f2_p])

    #titolo che avrà il plot con le info varie
    titl='f(x,y)=(' + f1.__str__() + ',' + f2.__str__() + ')\n tol=' + str(p3) + ' grid\'s points=' + str(npunt)
    
    return x,epg,improper_arcs,titl

def EPG_plot(epg,titl):
    fig,axes=plt.subplots(1,1)
    axes.scatter([p[0] for p in epg],[p[1] for p in epg],s=0.2)
    axes.set_title(titl)

    return fig

def EPG_file(epg,titl,name='puntiEPG'):
    file=open(name+'.txt', 'w')
    file.write(titl+'\n The points in the Extended Pareto Grid of f are the following: \n')
    L=[str(p)+'\n' for p in epg]
    file.writelines(L)

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
    '''
    ppc = [p for p,v in x.items() if v]
    #Plot
    fig,axes=plt.subplots(1,1)
    
    fig.set_size_inches(3,3)
    # axes[0].scatter([f1.eval(p[0],p[1]) for p in ppc],[f2.eval(p[0],p[1]) for p in ppc],s=0.2)
    # axes[0].set_aspect('equal')
    # axes[0].set_title('Vecchia Extended Pareto Grid con ' + str(len(ppc)) + ' punti')'''
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
    '''
    #Plot
    ppc = [p for p,v in x.items() if v]     #Nuovo ppc
    
    # axes[1].scatter([f1.eval(p[0],p[1]) for p in ppc],[f2.eval(p[0],p[1]) for p in ppc],s=0.2)
    # axes[1].set_aspect('equal')
    # axes[1].set_title('Nuova Extended Pareto Grid con ' + str(len(ppc)) + ' punti')          
    axes.scatter([f1.eval(p[0],p[1]) for p in ppc],[f2.eval(p[0],p[1]) for p in ppc],s=0.2)
    axes.set_title('Nuova Extended Pareto Grid con ' + str(len(ppc)) + ' punti')            
    return fig'''

    return x
    #return nclusters

def noise_reduction(x,f1,f2,tol,oldtitle,improper_arcs):
    t1rette=intersect_sheaf_type1(x,f1,f2)
    t1cluster=sheaf_of_clusters(t1rette,f1,f2)
    x=manage_clusters(t1cluster,x,f1,f2,tol)
    ppc = [p for p,v in x.items() if v]     #Raccolge i punti di x che sono true
    epg=[]
    for p in ppc:
        epg.append([f1.eval(p[0],p[1]),f2.eval(p[0],p[1])])
    #aggiungo gli improper arcs
    epg=epg+improper_arcs

    #titolo che avrà il plot con le info varie
    titl=oldtitle+'\n riduzione con metodo rette'
    
    return x,epg,titl