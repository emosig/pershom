import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from ourPolynomial import *

CLUST_MAX_ITER = 50     #Massimo di iterazioni per il clustering
CLUST_VAR_STOP = 5      #Se in una iterazione di clustering aggiungo o tolgo 
                        #meno di questa quantità di punti, mi fermo

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
    for p in x.keys():
        a=[grf_1[0].eval(p[0],p[1]),grf_1[1].eval(p[0],p[1])]
        b=[grf_2[0].eval(p[0],p[1]),grf_2[1].eval(p[0],p[1])]
        
        #la seguente condizione mi dice che ho un punto dell'insieme di Jacobi
        det = a[0]*b[1]-a[1]*b[0]

        if abs(det)<=p3:
            x[p]=Pareto_crit(a,b,p3)
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
    l=len(epg)+len(improper_arcs)
    titl='f(x,y)=(' + f1.__str__() + ',' + f2.__str__() + ')\n tol=' + str(p3) + ', grid\'s points=' + str(npunt) +', image points=' + str(l)
    
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