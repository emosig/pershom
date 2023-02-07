import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from scipy import optimize
import numdifftools as nd
from ourPolynomial import *

#definisco la funzione che calcola i punti critici e i punti pareto critici, gli do in input già i gradienti e dentro EPG decido come calcolarli
def Pareto(f_1,f_2,p1,p2,p3,metodo):
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
    
    if metodo==True:
        grf_1=f_1.gradient()
        grf_2=f_2.gradient()

    for i in range (0,l,1):
        if metodo==False:
            a=nd.Gradient(f_1)(x[i])
            b=nd.Gradient(f_2)(x[i])
        if metodo==True:
            a=[grf_1[0].eval(x[i][0],x[i][1]),grf_1[1].eval(x[i][0],x[i][1])]
            b=[grf_2[0].eval(x[i][0],x[i][1]),grf_2[1].eval(x[i][0],x[i][1])]
        
        if abs(a[0])<=p2 and abs(a[1])<=p2:       #punto critico per f_1
            cr1.append(x[i])
        if abs(b[0])<=p2 and abs(b[1])<=p2:       #punto critico per f_2
            cr2.append(x[i])
        
        det.append(a[0]*b[1]-a[1]*b[0])
        
        #la seguente condizione mi dice che ho un punto dell'insieme di Jacobi
        if abs(det[i])<=p3:

            #se ho un punto critico allora è anche pareto critico (infatti verifico con tolleranza p3)
            if (abs(a[0])<=p3 and abs(a[1])<=p3):
                ppc.append(x[i])
            if(abs(b[0])<=p3 and abs(b[1])<=p3):
                ppc.append(x[i])
            
            #troviamo ora i punti dell'insieme di Jacobi che non sono critici e sono Pareto Critici
            
            if abs(a[0])<=p3 and abs(a[1])>p3:
                if b[1]/a[1]<=p3:                   #sarebbe lambda<=0
                    ppc.append(x[i])
                    
            if abs(a[1])<=p3 and abs(a[0])>p3:
                if b[0]/a[0]<=p3:                   #sarebbe lambda<=0
                    ppc.append(x[i])

            if abs(b[0])<=p3 and abs(b[1])>p3:
                if a[1]/b[1]<=p3:                   #sarebbe lambda<=0
                    ppc.append(x[i])

            if abs(b[1])<=p3 and abs(b[0])>p3:
                if a[0]/b[0]<=p3:                   #sarebbe lambda<=0
                    ppc.append(x[i])

            if abs(b[0])>p3 and abs(b[1])>p3:
                if a[0]/b[0]<=p3 or a[1]/b[1]<=p3:  #sarebbe lambda<=0
                    ppc.append(x[i])

            if abs(a[0])>p3 and abs(a[1])>p3:
                if b[0]/a[0]<=p3 or b[1]/a[1]<=p3:  #sarebbe lambda<=0
                    ppc.append(x[i])

    ppc=np.array(ppc)
    cr1=np.array(cr1)
    cr2=np.array(cr2)
    return ppc,cr1,cr2,x

def EPG(f_1,f_2,p1,p2,p3,metodo):  #gli argomenti sono ourPolynomial
    ppc,cr1,cr2,x=Pareto(f_1,f_2,p1,p2,p3)
    m='nd.gradient'
    if metodo==True:
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

    else:
        fig,axes=plt.subplots(1,4)
        fig.set_size_inches(28,4)
        axes[0].scatter([p[0] for p in cr1],[p[1] for p in cr1],s=8)
        axes[0].set_title('Pt crit di f_1, '+m+' con tol='+str(p2))
        axes[1].scatter([p[0] for p in cr2],[p[1] for p in cr2],s=8)
        axes[1].set_title('Pt crit di f_2, '+m+' con tol='+str(p2))
        axes[2].scatter([p[0] for p in ppc],[p[1] for p in ppc],s=0.2)
        axes[2].set_title('Pt Pareto Critici, '+m+', tol='+str(p3))
        axes[3].scatter([f_1(p) for p in ppc],[f_2(p) for p in ppc],s=0.2)
        axes[3].set_title('Extended Pareto Grid')