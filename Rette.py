#File ¿temporaneo? per le operazioni con rette/fasci di rette che vorremmo intersecare con l'EPG per noise reduction
from ProgrammaEPG import *
from ourPolynomial import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#Modelizzo 2 tipi di fasci di rette: il fascio di tipo 1 è dato da n rette 
# parallele (y-mx+a=0)_a che variano nel parametro a fissata una pendenza m>0,
# il fascio di tipo 2 è quello dato da n rette che passano per un punto fisso (a,b)
# date da ((a,b)+v_k(x,y))_k che variano nel parametro k dove v_k = (cosk,senk) è
# il vettore direttore della retta

#Ci vogliono due nuovi parametri di precisione: uno per quanto "grosse" vogliamo
# considerare le rette e un'altro per la quantità di rette considerate. Per ora li tengo fissi:

RETTE = 100  #quantità di rette 
EPS = 0.05  #quanto grosse sono le rette

#fisso anche per ora la pendenza m per il tipo 1 e il punto (a,b) per il tipo 2
M = 1
A,B = 0,1

#Fisso una tolleranza per i "cluster" di punti vicini nelle rette. I cluster più grandi 
# saranno interpretati come rumore
CLUST_EPS = 0.05

#Questo è soltanto per ora per vedere che le rette sono quelle che io voglio
#In realtà noi queste intersezioni non le vorremmo vedere, sono per togliere l'errore
PLOT = False

#Intersezione con una retta di tipo 1 
def intersect_line_type1(f1ppc,f2ppc,a,m=M):
    inter = []
    for p,q  in zip(f1ppc,f2ppc):
        if abs(q-m*p - a) < EPS: #In realtà sto facendo 2 rette pero i punti vanno nella stessa lista
            if [p,q] not in inter:
                inter.append([p,q])
    return np.array(sorted(inter))

#Intersezione con un fascio di rette tipo 1
def intersect_sheaf_type1(f1ppc,f2ppc,m=M):
    intersection_list = []  #Lista di liste: intersezione di ogni retta considerata con l'EPG

    #Mi calcolo il rango in cui voglio fare variare a
    minx,maxx,miny,maxy = get_square(f1ppc,f2ppc)
    mina = maxy - m*minx
    maxa = miny - m*maxx

    #Voglio variare a \in [miny,maxy]
    for a in np.linspace(mina,maxa,RETTE):
        line = intersect_line_type1(f1ppc,f2ppc,a,m)
        intersection_list.append(line)
    
    if PLOT:
        colors = cm.rainbow(np.linspace(0, 1, len(intersection_list)))
        for r,c in zip(intersection_list,colors):
            plt.scatter([p[0] for p in r],[p[1] for p in r],s=4,color=c)
        plt.title("Intersezione con " + str(RETTE) + " rette tipo 1 con tolleranza " + str(EPS))
    
    return np.array(intersection_list, dtype=object)

#Intersezione con una retta di tipo 2
def intersect_line_type2(f1ppc,f2ppc,k,a=A,b=B):
    inter = []
    for p,q  in zip(f1ppc,f2ppc):
        if abs(np.sin(k)*(q-b) - np.cos(k)*(p-a)) < EPS:
            if [p,q] not in inter:
                inter.append([p,q])
    return np.array(sorted(inter))

#Intersezione con un fascio di rette tipo 2
def intersect_sheaf_type2(f1ppc,f2ppc,a=A,b=B):
    intersection_list = []

    #k lo faccio variare in [0,pi]
    for k in np.linspace(0,np.pi,RETTE):
        line = intersect_line_type2(f1ppc,f2ppc,k,a,b)
        intersection_list.append(line)

    if PLOT:
        colors = cm.rainbow(np.linspace(0, 1, len(intersection_list)))
        for r,c in zip(intersection_list,colors):
            plt.scatter([p[0] for p in r],[p[1] for p in r],s=4,color=c)
        plt.title("Intersezione con " + str(RETTE) + " rette tipo 2 con tolleranza " + str(EPS))

    return np.array(intersection_list, dtype=object)

#Questo metodo trova i clusters 1d di punti in una retta
def line_clusters(line):
    clusters = []
    curr_point = line[0]
    curr_cluster = [curr_point]
    for p in line[1:]:
        if abs(p[0]) <= abs(curr_point[0]) + CLUST_EPS and abs(p[1]) <= abs(curr_point[1]) + CLUST_EPS:
            curr_cluster.append(p)
        else:
            clusters.append(curr_cluster)
            curr_cluster = [p]
        curr_point = p
    clusters.append(curr_cluster)
    return np.array(clusters, dtype=object)

#Metodo che dato un fascio di rette mi ritorna un fascio di liste di clusters di punti
#(quei punti vicini in ogni retta)
def sheaf_of_clusters(intersection_list):
    cluster_list = []
    for l in intersection_list:
        if len(l)>1:    #Ignoro le rette che non intersecano sufficentemente l'EPG
            cluster_list.append(line_clusters(l))

    if PLOT:
        #Plotto i clusters della prima retta significativa
        cl_line = cluster_list[10]
        colors = cm.rainbow(np.linspace(0, 1, len(cl_line)))
        for cl,c in zip(cl_line,colors):
            plt.scatter([p[0] for p in cl],[p[1] for p in cl],s=4,color=c)
        plt.title("I cluster in una delle rette del fascio con CLUST_EPS = " + str(CLUST_EPS))

    return np.array(cluster_list, dtype=object)








