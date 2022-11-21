import numpy as np

#Exception raised when constructing a polynomial with None coefficients and None size.
class EmptyMatrixError(Exception):
    pass

#Exception raised when constructing a polynomial with undesired matrix.
class PolySizeError(Exception):

    def __init__(self, value):
        self.value = value
 
    # __str__ is to print() the value
    def __str__(self):
        return(repr(self.value))
    pass

#Exception raised when constructing a polynomial and given a non-square matrix of coefficients.
class PolyNonSquareError(PolySizeError):

    #usare costruttore della superclasse oppure uno nuovo con 2 argomenti? 
    def __init__(self, value):
        super(PolySizeError, self).__init__(value)
    pass

class Poly2var:
    #Classe per i polinomi in x,y
    #I coefficienti li salvo come una matrice quadrata a_{ij} = coeff per x^i*y^j
    #Esempio: '1 0 3; 0 2 2; 0 0 1' <--> x^2y^2 + 2x^2y + 2xy + 3x^2 + 1

    #1-11 Oggi mi sono reso conto che la classe numpy.matrix è deprecated.
    #Bisogna utilizzare invece la classe numpy.ndarray

    #CONSTRUCTOR
    def __init__(self, coeffs, size = 0):
        self.size = size
        #Throws different exceptions if there was a problem constructing the matrix
        try:
            if size == 0 and coeffs.size == 0: 
                    raise EmptyMatrixError()

            #initalize a zero polynomial (null matrix)
            elif size != 0 and coeffs.size == 0:
                    self.coeffmat = np.zeros((size,size))

            #nonzero polynomial
            else:
                self.coeffmat = coeffs
                self.size = coeffs.shape[0]

        except EmptyMatrixError:
            print('Provide either a size for the matrix or a sequence of coefficients')
        except PolyNonSquareError:
            print('The coefficient matrix given is not square')
        except PolySizeError as error:
            print('The coefficient matrin given is not of dimension 2 but ', error.value)

    #GETTERS
    def get_size(self):
        return self.size

    #Lista di compenenti omogenei del polinomio // diagonali secondarie della matrice
    def get_homogenous_comps(self):
        M = self.coeffmat
        diags = [M[::-1,:].diagonal(i) for i in range(-M.shape[0]+1,M.shape[1])]
        return diags

    #Itera attraverso la lista di diagonali per trovare la maggiore in grado che abbia un elemento non nullo
    def get_degree(self):
        diags = list(reversed(self.get_homogenous_comps()))
        ind = 0
        for x in diags:
            for y in x != 0:
                if y:
                    return len(diags) - 1 - ind
            ind +=1

    #SETTERS
    def set_elem(self,i,j, value):
        self.coeffmat[i,j] = value

    #OTHER FUNCTIONS
    def value(self,x,y):
        mat = self.coeffmat
        val = 0
        s = self.size
        for i in range(s):
            for j in range(s):
                #Per qualche ragione che non ho mai capito bisogna trasporre la matrice mat
                val += mat[j,i]*(x**i)*(y**j)
        return val

    #derivate parziali (ritorna un Poly2var)
    def dx(self):
        n = self.size
        M = Poly2var(np.array([]),n)
        for x in range(n):
            for y in range(n-1):
                M.set_elem(x,y,(y+1)*self.coeffmat[x,y+1])
            M.set_elem(x,n-1,0)
        return M

    def dy(self):
        n = self.size
        M = Poly2var(np.array([]),n)
        for x in range(n-1):
            for y in range(n):
                M.set_elem(x,y,(x+1)*self.coeffmat[x+1,y])
                M.set_elem(n-1,y,0)
        return M

    def gradient(self):
        return (self.dx(),self.dy())

    def print(self):
        print(self.coeffmat)




class myFunction:
    #As for now, myFuction \in \mathbb{Z}[x]
    #For functions on the sfere i will need polynomials in x,y,z... Poly3var?

    #CONSTRUCTOR
    def __init__(self, *inp):
        self.domain = inp[0]    #Sphere or torus
        if len(inp) == 3 and isinstance(inp[1],np.ndarray) and isinstance(inp[2],np.ndarray):
            self.f1 = Poly2var(inp[1])
            self.f2 = Poly2var(inp[2])
        elif len(inp) == 5 and isinstance(inp[3],np.ndarray) and isinstance(inp[4],np.ndarray):
            self.sizef1 = inp[1]
            self.sizef1 = inp[2]
            self.f1 = Poly2var(inp[3],inp[1])
            self.f2 = Poly2var(inp[4],inp[2])

    #GETTERS
    def getf1(self):
        return self.f1
    
    def getf2(self):
        return self.f2

    #OTHER FUNCTIONS
    #Ritorna il gradiente come coppia di matrici (polinomi in x,y)
    def gradient(self):
        return (self.f1.gradient(), self.f2.gradient())
    
    #Valuta il gradiente
    def gradient_value(self,x,y):
        gr = self.gradient()
        nabla0 = (gr[0][0].value(x,y), gr[0][1].value(x,y))
        nabla1 = (gr[1][0].value(x,y), gr[1][1].value(x,y))
        return (nabla0, nabla1)