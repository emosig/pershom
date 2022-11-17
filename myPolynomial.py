import numpy as np

#leggere tests.ipynb

class Monomial:
    def __init__(self, r,a,b,c,d):
        self.r = r
        self.a = a
        self.b = b
        self.c = r
        self.r = r
        self.deg = a+b+c+d    #grado

    def get_degree(self):
        return self.deg
    
    #Ogni derivata parziale ritorna una somma di due monomi di grado k-1
    def dx(self):
        a = self.a
        b = self.b
        dx1 = Monomial(a*self.r,a-1,b,self.c,self.d)
        dx2 = Monomial(b*self.r,a,b-1,self.c,self.d)
        return (dx1,dx2)

    def dy(self):
        c = self.c
        d = self.d
        dy1 = Monomial(c*self.r,self.a,self.b,c-1,d)
        dy2 = Monomial(d*self.r,self.a,self.b,c,d-1)
        return (dy1,dy2)

    def eval(self,x,y):
        return self.r*(np.sin(x)**self.a)*(np.cos(x)**self.b)*(np.sin(y)**self.c)*(np.cos(y)**self.d)

class HomogComp:
    #m è una lista non vuota di Monomial
    def __init__(self, m):
        self.monomials = m
        self.deg = m[0].get_degree()
    
    def get_degree(self):
        return self.deg

    def dx(self):
        l = []      #lista di Monomial di grado k-1
        for m in self.monomials:
            pair = m.dx()
            l.append(pair[0])
            l.append(pair[1])
        dx = HomogComp(l)
        return dx

    def dy(self):
        l = []      #lista di Monomial di grado k-1
        for m in self.monomials:
            pair = m.dy()
            l.append(pair[0])
            l.append(pair[1])
        dy = HomogComp(l)
        return dy

    def eval(self,x,y):
        value = 0
        for m in self.monomials:
            value += m.eval(x,y)
        return value
    
class myPolynomial:
    #h è un dictonary non vuoto grado - comp omogenee
    def __init__(self, h):
        self.comps = h

    def dx(self):
        comps = {}
        for k in self.comps.keys():
            #Per ogni grado k derivo e aggiungo la componente omogenea derivata nella key k-1 del nuovo dictionary
            h = self.comps[k].dx()
            comps[k-1].append(h)
        dx = myPolynomial(comps)
        return dx

    def dy(self):
        comps = {}
        for k in self.comps.keys():
            #Per ogni grado k derivo e aggiungo la componente omogenea derivata nella key k-1 del nuovo dictionary
            h = self.comps[k].dy()
            comps[k-1].append(h)
        dy = myPolynomial(comps)
        return dy

    def gradient(self):
        return (self.dx(),self.dy())

    def eval(self,x,y):
        value = 0
        for k in self.comps.keys():
            value += self.comps[k].eval(x,y)
        return value


#¿Non sarebbe bello avere una funzione che dato un input di testo costruisce un polinomio?
def parse(msg):
    pass #Lo farò più avanti
