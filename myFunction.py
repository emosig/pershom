from re import M
import numpy as np

class Poly2var:
    #Coeffs come una matrice quadrata a_{ij} = coeff per x^i*y^j
    #Esempio: '1 0 3; 0 2 2; 0 0 1' --> x^2y^2 + 2x^2y + 2xy + 3x^2 + 1
    def __init__(self, coeffs, size = 0):
        self.coeffmat = np.matrix(coeffs)
        self.size = size

    #Lista di compenenti omogenei del polinomio // diagonali secondarie della matrice
    def get_homogenous_comps(self):
        M = self.coeffmat.getA()
        diags = [M[::-1,:].diagonal(i) for i in range(-M.shape[0]+1,M.shape[1])]
        return diags

    #itera attraverso la lista di diagonali per trovare la maggiore in grado che abbia un elemento non nullo
    def get_degree(self):
        diags = list(reversed(self.get_homogenous_comps()))
        ind = 0
        for x in diags:
            for y in x != 0:
                if y:
                    return len(diags) - 1 - ind
            ind +=1

    #derivate parziali (utilizzo size)
    def dx(self):
        n = self.size
        M = np.zeros((n,n))
        for x in range(n):
            for y in range(n-1):
                M[x,y] = (y+1)*self.coeffmat[x,y+1]
            M[x,n-1] = 0
        return M

    def dy(self):
        n = self.size
        M = np.zeros((n,n))
        for x in range(n-1):
            for y in range(n):
                M[x,y] = (x+1)*self.coeffmat[x+1,y]
                M[n-1,y] = 0
        return M





class myFunction:
    #As for now, myFuction \in \mathbb{Z}[x]
    def __init__(self, domain, f1coeffs, f2coeffs):
        self.domain = domain    #Sphere or torus
        self.f1coeffs = f1coeffs    #Finite of integers
        self.f2coeffs = f2coeffs