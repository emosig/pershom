from ProgrammaEPG import *
from Rette import *
from itertools import combinations, product

PLOT = True

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
        pairsofpairs = combinations(list(combinations(intersection,2)),2)
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

#Intersezione  r_{(a,b)} \cap (\Gamma(f) \cup \Gamma(g))
def intersect_line_2EPG(a,b,eps,f1ppc,f2ppc,g1ppc,g2ppc):
    #Retta r_{(a,b)}
    m=(1-a)/a       #Sto considerando a \neq 0, 1
    #Se la retta non interseca i rettangoli che contengono gli EPG non faccio niente
    fminx,fmaxx,fminy,fmaxy = get_square(f1ppc,f2ppc)
    gminx,gmaxx,gminy,gmaxy = get_square(g1ppc,g2ppc)
    xf = (fmaxy +b)/m + b
    xg = (gmaxy +b)/m + b
    if fminx <= xf <= fmaxx:
        interf = intersect_line_type1(f1ppc,f2ppc,b,m,eps)
    else:
        interf = []
    if gminx <= xg <= gmaxx:
        interg = intersect_line_type1(g1ppc,g2ppc,b,m,eps)
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
def special_set(C,tolx,toly,eps,f1ppc,f2ppc,g1ppc,g2ppc):
    sp=[]
    #Griglia di tolx*toly punti. Escludo i valori a=0,a=1
    grid = product(np.linspace(0+eps/100,1-eps/100,tolx),np.linspace(-C,C,toly))
    for i,j in grid:
        if isSpecial(intersect_line_2EPG(i,j,eps,f1ppc,f2ppc,g1ppc,g2ppc),i,eps):
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





#TESTING
if __name__ == "__main__":
    intersection = np.array([np.array([0,0]),np.array([0,1]),np.array([0.001,0.004]),
                             np.array([2,3]),np.array([2.001,7]),np.array([-1,7.001])])
    a = 0.2

    pairsofpairs = combinations(list(combinations(intersection,2)),2)
    for p,q in pairsofpairs:
        print(p)
        print(q)
        print(' --- ')


    isSpecial(intersection,a,0.05)




