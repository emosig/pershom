import numpy as np

#leggere tests.ipynb

class Monomial:
    #CONSTRUCTOR
    def __init__(self,r,a,b,c,d):
        self.r = r
        if r == 0:
            self.a = 0
            self.b = 0
            self.c = 0
            self.d = 0
            self.deg = 0
        else:
            self.a = a
            self.b = b
            self.c = c
            self.d = d
            self.deg = a+b+c+d    #grado

    #GETTERS
    def get_degree(self):
        return self.deg
    
    def get_coeffs(self):
        return [self.r,self.a,self.b,self.c,self.d]
    
    #OTHER
    #Ogni derivata parziale ritorna una somma di due monomi di grado k-1
    def dx(self):
        a = self.a
        b = self.b
        dx1 = Monomial(a*self.r,a-1,b+1,self.c,self.d) 
        dx2 = Monomial(-b*self.r,a+1,b-1,self.c,self.d)
        return (dx1,dx2)

    def dy(self):
        c = self.c
        d = self.d
        dy1 = Monomial(c*self.r,self.a,self.b,c-1,d+1)
        dy2 = Monomial(-d*self.r,self.a,self.b,c+1,d-1)
        return (dy1,dy2)

    def eval(self,x,y):
        return self.r*(np.sin(x)**self.a)*(np.cos(x)**self.b)*(np.sin(y)**self.c)*(np.cos(y)**self.d)

class HomogComp:
    #CONSTRUCTOR
    #m è una lista non vuota di Monomial
    def __init__(self, m):
        self.monomials = m
        self.deg = m[0].get_degree()

    #GETTERS
    def get_monomials(self):
        return self.monomials
    
    def get_degree(self):
        return self.deg

    #OTHER
    #per printare il polinomio in modo comodo
    def __str__(self):
        p = ''
        for m in self.monomials:
            coeffs = m.get_coeffs()
            #trasformo il monomio in string
            if coeffs[0] != 0:
                strlist = []
                if coeffs[0] != 1:
                    strlist.append(str(coeffs[0]))
                if coeffs[1] != 0:
                    if coeffs[1] == 1:
                        coeffs[1] = ''
                    strlist.append('sin^' + str(coeffs[1]) + 'x ')
                if coeffs[2] != 0:
                    if coeffs[2] == 1:
                        coeffs[2] = ''
                    strlist.append('cos^' + str(coeffs[2]) + 'x ')
                if coeffs[3] != 0:
                    if coeffs[3] == 1:
                        coeffs[3] = ''
                    strlist.append('sin^' + str(coeffs[3]) + 'y ')
                if coeffs[4] != 0:
                    if coeffs[4] == 1:
                        coeffs[4] = ''
                    strlist.append('cos^' + str(coeffs[4]) + 'y ')
                strlist.append('+ ')
                p += str().join(strlist)
        return p.removesuffix('+ ')

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
    #BISOGNA creare delle eccecioni per controllare che non mi stanno passando delle
    #componenti omogenee con il grado sbagliato

    #CONSTRUCTOR
    #h è un dictonary non vuoto grado - comp omogenee
    def __init__(self, h):
        self.comps = h

    #OTHER
    #per printare il polinomio in modo comodo
    def __str__(self):
        p = ''
        for k in self.comps.keys():
            for m in self.comps[k].get_monomials():
                coeffs = m.get_coeffs()
                #trasformo il monomio in string
                if coeffs[0] != 0:
                    strlist = []
                    if coeffs[0] != 1:
                        strlist.append(str(coeffs[0]))
                    if coeffs[1] != 0:
                        if coeffs[1] == 1:
                            coeffs[1] = ''
                        strlist.append('sin^' + str(coeffs[1]) + 'x ')
                    if coeffs[2] != 0:
                        if coeffs[2] == 1:
                            coeffs[2] = ''
                        strlist.append('cos^' + str(coeffs[2]) + 'x ')
                    if coeffs[3] != 0:
                        if coeffs[3] == 1:
                            coeffs[3] = ''
                        strlist.append('sin^' + str(coeffs[3]) + 'y ')
                    if coeffs[4] != 0:
                        if coeffs[4] == 1:
                            coeffs[4] = ''
                        strlist.append('cos^' + str(coeffs[4]) + 'y ')
                    strlist.append('+ ')
                    p += str().join(strlist)
        return p.removesuffix('+ ')

    def dx(self):
        comps = {}
        for k in self.comps.keys():
            #Per ogni grado k derivo e aggiungo la componente omogenea derivata nella key k-1 del nuovo dictionary
            h = self.comps[k].dx()
            #comps[k-1].append(h)
            comps[k-1] = h
        dx = myPolynomial(comps)
        return dx

    def dy(self):
        comps = {}
        for k in self.comps.keys():
            #Per ogni grado k derivo e aggiungo la componente omogenea derivata nella key k-1 del nuovo dictionary
            h = self.comps[k].dy()
            #comps[k-1].append(h)
            comps[k-1] = h
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
    monomi = []
    #Separo per monomi
    msg = msg.split("+")
    for mono in msg:
        if len(mono) == 1:
            #È un termine indipendente
            monomi.append(Monomial((int(mono)),0,0,0,0))
        else:
            #Separo il monomio in fattori
            mono = mono.split("(")
            a,b,c,d = 0
            r = 1
            for f in mono:
                l = len(f)
                if f[l-1] == ")":
                    f = f[:-1]
                if l == 1:
                    r = int(f[0])
                if f[l-2] == "x":
                    pass
    #WORK IN PROGRESS
    
                

    #testing
    for mono in monomi:
        print(mono)
