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
EPS = 0.1  #quanto grosse sono le rette

#fisso valori default per la pendenza m per il tipo 1 e il punto (a,b) per il tipo 2
M = 1
A,B = 0,1

#Fisso una tolleranza per i "cluster" di punti vicini nelle rette. I cluster più grandi 
# saranno interpretati come rumore
CLUST_EPS = 0.2

#Questo è soltanto per ora per vedere che le rette sono quelle che io voglio
#In realtà noi queste intersezioni non le vorremmo vedere, sono per togliere l'errore
PLOT = False

#Intersezione con una retta di tipo 1 
#Nel linguaggio di Frosini questa è r_{(1/m-1,a)}, (1/m-1,a) \in (0,1)x\R
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

#Intersezione con un fascio di rette tipo 1
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

#Intersezione con una retta di tipo 2
def intersect_line_type2(ppc,f1,f2,k,a=A,b=B,eps=EPS):
    inter = []
    for p in ppc:
        x = f1.eval(p[0],p[1])
        y = f2.eval(p[0],p[1])
        if abs(np.sin(k)*(y-b) - np.cos(k)*(x-a)) < eps:
            if p not in inter:      #ATTENZIONE ---> FORSE VA BENE SEMPRE
                inter.append(p)
    return sorted(inter)

#Intersezione con un fascio di rette tipo 2
def intersect_sheaf_type2(x,f1,f2,a=A,b=B,eps=EPS):
    intersection_list = []
    ppc = [p for p,v in x.items() if v] #I punti pareto critici

    #k lo faccio variare in [0,pi]
    for k in np.linspace(0,np.pi,RETTE):
        line = intersect_line_type2(ppc,f1,f2,k,a,b,eps)
        if len(line)>0:
            intersection_list.append(line)

    if PLOT:
        colors = cm.rainbow(np.linspace(0,1,len(intersection_list)))
        for r,c in zip(intersection_list,colors):
            plt.scatter([f1.eval(p[0],p[1]) for p in r],[f2.eval(p[0],p[1]) for p in r],s=4,color=c)
        plt.title("Intersezione con " + str(RETTE) + " rette tipo 2 con tolleranza " + str(EPS))

    return np.array(intersection_list, dtype=object)

#Questo metodo trova i clusters 1d di punti in una retta
def line_clusters(line,f1,f2):
    clusters = []
    curr_point = line[0]
    curr_cluster = [curr_point]
#-----------------------
#FARE EVAL QUA O FARLO DOPO????
#-----------------------
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

#Metodo che dato un fascio di rette mi ritorna un fascio di liste di clusters di punti
#(quei punti vicini in ogni retta)
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

def noise_reduction(x,f1,f2,tol,oldtitle,improper_arcs):
    t1rette=intersect_sheaf_type1(x,f1,f2,sort=True)
    t1cluster=sheaf_of_clusters(t1rette,f1,f2)
    x=manage_clusters(t1cluster,x,f1,f2,tol)
    ppc = [p for p,v in x.items() if v]     #Raccolge i punti di x che sono true
    epg=[]
    for p in ppc:
        epg.append([f1.eval(p[0],p[1]),f2.eval(p[0],p[1])])
    #aggiungo gli improper arcs
    epg=epg+improper_arcs

    #titolo che avrà il plot con le info varie
    titl=oldtitle+' riduction'
    
    return x,epg,titl








