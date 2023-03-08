from ProgrammaEPG import *
from Rette import *
from itertools import combinations, product

PLOT = False

#Modulo per il calcolo del special set. Voglio parametrizzare le rette r_{(a,b)}
# e vedere per qualli a,b intersecano due EPG date verificando una condizione

#PER ORA SOLTANTO a \in (0,1), CIOÈ a DIVERSO DA 0,1

#Le rette r_{(a,b)} li posso vedere come le nostre rette di tipo 1 y=mx+a'
#mettendo a = 1/m+1, b = a'

#a è il parametro della retta r_{(a,b)}, intersection è r_{(a,b)} \cap (Unione delle due EPG)
#eps viene usato come tolleranza per due cose diverse, ma per ora lasciamo stare
#Ritorna true se (a,b) è Special e anche la coppia alfa, beta che lo rende Special
def isSpecial(intersection, a, eps):
    if len(intersection) > 1:
        #Lista di coppie di coppie di punti in intersection escludendo le cose che vogliamo escludere (fidati)
        pairsofpairs = combinations(list(product(intersection,intersection)),2)

        if a < 1/2:     #In questo caso guardo la coordinata [0] dei punti
            for alfa,beta in pairsofpairs:  #Alfa, beta sono coppie di punti (P,Q)
                if abs(beta[0][0] - beta[1][0]) > eps:
                    r = abs(alfa[0][0] - alfa[1][0])/abs(beta[0][0] - beta[1][0])
                    if 0.5 - eps < r < 0.5 + eps or 1 - eps < r < 1 + eps or 2 - eps < r < 2 + eps:
                        return True
                elif abs(alfa[0][0] - alfa[1][0]) > eps:
                    r = abs(beta[0][0] - beta[1][0])/abs(alfa[0][0] - alfa[1][0])
                    if 0.5 - eps < r < 0.5 + eps or 1 - eps < r < 1 + eps or 2 - eps < r < 2 + eps:
                        return True
        else:           #In questo caso guardo la coordinata [1] dei punti. Analogo a quello prima
            for alfa,beta in pairsofpairs:
                if abs(beta[0][1] - beta[1][1]) > eps:
                    r = abs(alfa[0][1] - alfa[1][1])/abs(beta[0][1] - beta[1][1])
                    if 0.5 - eps < r < 0.5 + eps or 1 - eps < r < 1 + eps or 2 - eps < r < 2 + eps:
                        return True
                elif abs(alfa[0][1] - alfa[1][1]) > eps:
                    r = abs(beta[0][1] - beta[1][1])/abs(alfa[0][1] - alfa[1][1])
                    if 0.5 - eps < r < 0.5 + eps or 1 - eps < r < 1 + eps or 2 - eps < r < 2 + eps:
                        return True
    return False

#Funzione per intersecare con i half-lines
#somma_epg è l'unione di due epg con i half-lines, forse una di loro già traslata
def intersect_line_2EPG_image(a,b,eps,somma_epg):
    #Retta r_{(a,b)}
    m=(1-a)/a       #Sto considerando a \neq 0, 1
    #Interseco con la retta r_{(a,b)}
    inter = []
    for p in somma_epg:
        if abs(p[1]-m*p[0] - b) < eps:
            if p not in inter:
                inter.append(p)
    return np.array(inter)

#Intersezione  r_{(a,b)} \cap (\Gamma(f) \cup \Gamma(g))
def intersect_line_2EPG(a,b,eps,xf,f1,f2,xg,g1,g2,trasl=0):
    #Retta r_{(a,b)}
    m=(1-a)/a       #Sto considerando a \neq 0, 1
    #I punti paretocritici
    ppcf = [p for p,v in xf.items() if v]
    ppcg = [p for p,v in xg.items() if v]
    #Se la retta non interseca i rettangoli che contengono gli EPG non faccio niente
    fminx,fmaxx,fminy,fmaxy = get_square(ppcf,f1,f2,trasl)
    gminx,gmaxx,gminy,gmaxy = get_square(ppcg,g1,g2)
    xf = (fmaxy +b)/m + b
    xg = (gmaxy +b)/m + b
    if fminx <= xf <= fmaxx:
        interf = intersect_line_type1(ppcf,f1,f2,b,m,eps,trasl)
    else:
        interf = []
    if gminx <= xg <= gmaxx:
        interg = intersect_line_type1(ppcg,g1,g2,b,m,eps)
    else:
        interg = []
    
    #Concatenate da errore quando li passo una lista vuota quindi faccio questa cosa
    if len(interf)>0 and len(interg)>0:
        return np.concatenate((interf,interg))
    elif len(interf)>0:
        return interf
    elif len(interg)>0:
        return interg
    else:
        return np.array([])

    
#Special set dentro il rettangolo (0,1)x[-C,C]
#tolx,toly sono i parametri per costruire la griglia di punti sul rettangolo
def special_set(C,tolx,toly,eps,xf,f1,f2,xg,g1,g2,trasl=0):
    sp=[]
    #Griglia di tolx*toly punti. Escludo i valori a=0,a=1
    grid = product(np.linspace(0+eps/100,1-eps/100,tolx),np.linspace(-C,C,toly))
    for i,j in grid:
        if isSpecial(intersect_line_2EPG(i,j,eps,xf,f1,f2,xg,g1,g2,trasl),i,eps):
            sp.append([i,j])

    #Plotting
    if PLOT:
        plt.scatter([p[0] for p in sp],[p[1] for p in sp],s=0.6)
        plt.axhline(y=C, color='r', linestyle='-')
        plt.axhline(y=-C, color='r', linestyle='-')
        plt.title('Special set calcolato su ' + str(tolx*toly) + ' punti con epsilon=' + str(eps))
        plt.xlabel('a')
        plt.ylabel('b')
    return np.array(sp)


def special_set_image(C,tolx,toly,eps,somma_epg):
    sp=[]
    #Griglia di tolx*toly punti. Escludo i valori a=0,a=1
    grid = product(np.linspace(0+eps/100,1-eps/100,tolx),np.linspace(-C,C,toly))
    for i,j in grid:
        if isSpecial(intersect_line_2EPG_image(i,j,eps,somma_epg),i,eps):
            sp.append([i,j])

    #Plotting
    if PLOT:
        plt.scatter([p[0] for p in sp],[p[1] for p in sp],s=0.6)
        plt.axhline(y=C, color='r', linestyle='-')
        plt.axhline(y=-C, color='r', linestyle='-')
        plt.title('Special set calcolato su ' + str(tolx*toly) + ' punti con epsilon=' + str(eps))
        plt.xlabel('a')
        plt.ylabel('b')
    return np.array(sp)


