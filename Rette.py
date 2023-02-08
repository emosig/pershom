#File ¿temporaneo? per le operazioni con rette/fasci di rette che vorremmo intersecare con l'EPG per noise reduction
from ProgrammaEPG import *
from ourPolynomial import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#Modelizzo 2 tipi di fasci di rette: il fascio di tipo 1 è dato da n rette 
# parallele (y-mx+a=0)_a che variano nel parametro a fissata una pendenza m,
# il fascio di tipo 2 è quello dato da n rette che passano per un punto fisso (a,b)
# date da ((a,b)+v_k(x,y))_k che variano nel parametro k dove v_k = (cosk,senk) è
# il vettore direttore della retta

#Ci vogliono due nuovi parametri di precisione: uno per quanto "grosse" vogliamo
# considerare le rette e un'altro per la quantità di rette considerate. Per ora li tengo fissi:

RETTE = 20  #quantità di rette
EPS = 0.01  #quanto grosse sono le rette

#fisso anche per ora la pendenza m per il tipo 1 e il punto (a,b) per il tipo 2
M = 1
A,B = 0,1

#Questo è soltanto per ora per vedere che le rette sono quelle che io voglio
#In realtà noi queste intersezioni non le vorremmo vedere, sono per togliere l'errore
PLOT = True

#Intersezione con una retta di tipo 1
def intersect_line_type1(f1ppc,f2ppc,a,m=M):
    inter = []
    for p,q  in zip(f1ppc,f2ppc):
        aggiunto = False
        if abs(q-m*p + a) < EPS:
            inter.append([p,q])
            aggiunto = True
        if abs(q-m*p - a) < EPS and not aggiunto:
            inter.append([p,q])
    return inter

#Intersezione con un fascio di rette tipo 1
def intersect_sheaf_type1(f1ppc,f2ppc,m=M):
    intersection_list = []  #Lista di liste: intersezione di ogni retta considerata con l'EPG

    #Mi calcolo il quadrato che voglio intersecare con le mie rette
    minx,maxx,miny,maxy = get_square(f1ppc,f2ppc)

    #Voglio variare a \in [miny,maxy]
    for a in np.linspace(miny,maxy,RETTE):
        intersection_list.append(intersect_line_type1(f1ppc,f2ppc,a,m))

    if PLOT:
        colors = cm.rainbow(np.linspace(0, 1, len(intersection_list)))
        for r,c in zip(intersection_list,colors):
            plt.scatter([p[0] for p in r],[p[1] for p in r],s=4,color=c)

    return intersection_list

#Intersezione con una retta di tipo 2
def intersect_line_type2(f1ppc,f2ppc,k,a=A,b=B):
    inter = []
    for p,q  in zip(f1ppc,f2ppc):
        if abs(np.sin(k)*(q-b) - np.cos(k)*(p-a)) < EPS:
            inter.append([p,q])
    return inter

#Intersezione con un fascio di rette tipo 2
def intersect_sheaf_type2(f1ppc,f2ppc,a=A,b=B):
    intersection_list = []

    #k lo faccio variare in [0,pi]
    for k in np.linspace(0,np.pi,RETTE):
        intersection_list.append(intersect_line_type2(f1ppc,f2ppc,k,a,b))

    if PLOT:
        colors = cm.rainbow(np.linspace(0, 1, len(intersection_list)))
        for r,c in zip(intersection_list,colors):
            plt.scatter([p[0] for p in r],[p[1] for p in r],s=4,color=c)

    return intersection_list
