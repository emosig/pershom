from ProgrammaEPG import *
from ourPolynomial import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#Modelizzo un fascio di n rette parallele (y-mx+a=0)_a che variano nel parametro a fissata una pendenza m>0

#Ci vogliono due nuovi parametri di precisione: uno per quanto "grosse" vogliamo considerare le rette e un'altro per la quantità di rette considerate. Per ora li tengo fissi:

RETTE = 100  #quantità di rette 
EPS = 0.1  #quanto grosse sono le rette

#fisso valori default per la pendenza m per il tipo 1 e il punto (a,b) per il tipo 2
M = 1

#Fisso una tolleranza per i "cluster" di punti vicini nelle rette. I cluster più grandi saranno interpretati come rumore
CLUST_EPS = 0.05

#PLOT (for testing)
PLOT = False

#Intersezione con una retta; nella notazione di Frosini questa è r_{(1/m-1,a)}, (1/m-1,a) \in (0,1)x\R
def intersect_line_type1(ppc,f1,f2,a,m=M,eps=EPS,trasl=0,sort=False):
    inter = []
    for p in ppc:
        x = f1.eval(p[0],p[1]) + trasl
        y = f2.eval(p[0],p[1])
        if abs(y-m*x - a) < eps:
            if p not in inter:
                inter.append(p)
    if sort:
        inter = sorted(inter)
    return inter

#Mi serve capire quale è il più piccolo rettangolo che contiene i punti pareto critici
def get_square(ppc,f1,f2,trasl=0):
    f1ppc = [f1.eval(p[0],p[1]) + trasl for p in ppc]
    f2ppc = [f2.eval(p[0],p[1]) for p in ppc]
    return min(f1ppc), max(f1ppc), min(f2ppc), max(f2ppc)

#Intersezione con un fascio di rette
def intersect_sheaf_type1(x,f1,f2,m=M,eps=EPS,sort=False):
    intersection_list = []  #Lista di liste: intersezione di ogni retta considerata con l'EPG
    ppc = [p for p,v in x.items() if v] #I punti pareto critici

    #Mi calcolo il rango in cui voglio fare variare a
    minx,maxx,miny,maxy = get_square(ppc,f1,f2)
    mina = maxy - m*minx
    maxa = miny - m*maxx

    #Voglio variare a \in [miny,maxy]
    for a in np.linspace(mina,maxa,RETTE):
        line = intersect_line_type1(ppc,f1,f2,a,m,eps,sort)
        if len(line)>0:
            intersection_list.append(line)
    
    if PLOT:
        colors = cm.rainbow(np.linspace(0,1,len(intersection_list)))
        for r,c in zip(intersection_list,colors):
            plt.scatter([f1.eval(p[0],p[1]) for p in r],[f2.eval(p[0],p[1]) for p in r],s=4,color=c)
        plt.title("Intersezione con " + str(RETTE) + " rette tipo 1 con tolleranza " + str(EPS))
    
    return np.array(intersection_list, dtype=object)

#Questo metodo trova i clusters 1d di punti in una retta
def line_clusters(line,f1,f2):
    clusters = []
    curr_point = line[0]
    curr_cluster = [curr_point]

    for p in line[1:]:
        #Calcolo le immagini di p e curr_point
        f1p = f1.eval(p[0],p[1])
        f2p = f2.eval(p[0],p[1])
        f1curr = f1.eval(curr_point[0],curr_point[1])
        f2curr = f2.eval(curr_point[0],curr_point[1])

        if abs(f1p - f1curr) <= CLUST_EPS and abs(f2p - f2curr) <= CLUST_EPS:
            curr_cluster.append(p)
        else:
            clusters.append(curr_cluster)
            curr_cluster = [p]
        curr_point = p
    clusters.append(curr_cluster)
    return clusters

#Metodo che dato un fascio di rette mi ritorna un fascio di liste di clusters di punti (quei punti vicini in ogni retta)
def sheaf_of_clusters(intersection_list,f1,f2):
    cluster_list = []
    for l in intersection_list:
        if len(l)>1:    #Ignoro le rette che non intersecano sufficentemente l'EPG
            cluster_list.append(line_clusters(l,f1,f2))

    if PLOT:
        #Plotto i clusters della prima retta significativa
        cl_line = cluster_list[10]      #Scelta acaso.... questo era per testare
        colors = cm.rainbow(np.linspace(0,1,len(cl_line)))
        for cl,c in zip(cl_line,colors):
            plt.scatter([f1.eval(p[0],p[1]) for p in cl],[f2.eval(p[0],p[1]) for p in cl],s=4,color=c)
        plt.title("I cluster in una delle rette del fascio con CLUST_EPS = " + str(CLUST_EPS))

    return np.array(cluster_list, dtype=object)

#Metodo per ricalcolare i punti di un cluster associato a noise con tolleranza minore
#Ad ogni iterazione riduco la tolleranza alla metà finché il cluster non diventa sufficientemente piccolo.
#Cosa vuol dire abbastanza piccolo? Si potrebbe specificare con un ulteriore parametro
#Per ora voglio ridurre i punti del cluster da 1/4 (vedere CONTROLLO alla fine del loop while)
def recalculate_cluster(cluster,x,f1,f2,tol):
    ridurre_ancora = True    #Finché non ho ridotto "abbastanza" i punti del cluster questo rimane True
    i = 0       #Questo è un counter che arriva fino a 50 per evitare che il while vada avanti per sempre
    
    grf_1=f1.gradient()
    grf_2=f2.gradient()

    while ridurre_ancora and i < CLUST_MAX_ITER:
        #Ridurre la tolleranza
        tol = tol/2
        counter = 0     #Conta quanti punti del cluster rimangono
        for p in cluster:
            a=[grf_1[0].eval(p[0],p[1]),grf_1[1].eval(p[0],p[1])]
            b=[grf_2[0].eval(p[0],p[1]),grf_2[1].eval(p[0],p[1])]
            if Pareto_crit(a,b,tol):
                counter +=1
            else:
                x[p]=False
        #CONTROLLO: HO EFFETTIVAMENTE RIDOTTO LA QUANTITÀ DI PUNTI NEL CLUSTER?
        if counter < len(cluster)/4:
            ridurre_ancora = False
        i+=1
    return i,x  #Mi serve capire quante iterazioni ha fatto

#Applica il metodo sopra per i cluster "grandi"
def manage_clusters(cluster_list,x,f1,f2,tol):

    nclusters = 0   #Quanti clusters ho ridotto.
    
    for line in cluster_list:
        for cl in line:
            #Quanto grandi sono i cluster che voglio trattare?
            if len(cl) > 50:
                iter,x = recalculate_cluster(cl,x,f1,f2,tol)
                if iter < CLUST_MAX_ITER:   #Se l'algoritmo si è fermato prima del massimo di iterazioni
                    nclusters += 1  
    
    return x

def noise_reduction(x,f1,f2,tol,oldtitle,improper_arcs,m=M):
    t1rette=intersect_sheaf_type1(x,f1,f2,m,sort=True)
    t1cluster=sheaf_of_clusters(t1rette,f1,f2)
    x=manage_clusters(t1cluster,x,f1,f2,tol)
    ppc = [p for p,v in x.items() if v]     #Raccolge i punti di x che sono true
    epg=[]
    for p in ppc:
        epg.append([f1.eval(p[0],p[1]),f2.eval(p[0],p[1])])
    #aggiungo gli improper arcs
    epg=epg+improper_arcs

    #titolo che avrà il plot con le info varie
    while oldtitle[-1] in '0123456789':
        oldtitle=oldtitle[:-1]

    l=len(epg)
    titl=oldtitle + str(l) + ' reduction'
    
    return x,epg,titl






