import numpy as np

"""Costruiamo i monomi. Ogni monomio avrà un ordine interno, ovvero è della forma ordinata
r*(cos x)^a*(sen x)^b*(cos y)^c*(sen y)^d, quindi è identificato dalla tupla (r,a,b,c,d)
con r reale, a,b,c,d interi non negativi"""

class Monomial:
    #CONSTRUCTOR
    def __init__(self,r,a,b,c,d,shift_a,shift_b,shift_c,shift_d,molt_a,molt_b,molt_c,molt_d):
        self.r = r
        if r == 0:
            self.a = 0
            self.b = 0
            self.c = 0
            self.d = 0
            self.shift_a = 0
            self.shift_b = 0
            self.shift_c = 0
            self.shift_d = 0
            self.molt_a = 1
            self.molt_b = 1
            self.molt_c = 1
            self.molt_d = 1
        else:
            self.a = a
            self.b = b
            self.c = c
            self.d = d
            self.shift_a = shift_a
            self.shift_b = shift_b
            self.shift_c = shift_c
            self.shift_d = shift_d
            self.molt_a = molt_a
            self.molt_b = molt_b
            self.molt_c = molt_c
            self.molt_d = molt_d

    #GETTERS
    
    def get_coeffs(self):
        return [self.r,self.a,self.b,self.c,self.d]
    def get_shifts(self):
        return [self.shift_a,self.shift_b,self.shift_c,self.shift_d]
    def get_molts(self):
        return [self.molt_a,self.molt_b,self.molt_c,self.molt_d]

    #valutazione di un monomio in un punto (x,y)
    def eval(self,x,y):
        return self.r*(np.cos(self.molt_a*x+self.shift_a)**self.a)*(np.sin(self.molt_b*x+self.shift_b)**self.b)*(np.cos(self.molt_c*y+self.shift_c)**self.c)*(np.sin(self.molt_d*y+self.shift_d)**self.d)
    
    # CALCOLO DERIVATE PARZIALI
    #Ogni derivata parziale ritorna una i due monomi che poi andranno sommati seguendo le regole di derivazione del prodotto
    def dx(self):
        if self.molt_a!=self.molt_b or self.shift_a!=self.shift_b:
            dx11 = Monomial(self.a*self.r,self.a-1,self.b,self.c,self.d,self.shift_a,self.shift_b,self.shift_c,self.shift_d,self.molt_a,self.molt_b,self.molt_c,self.molt_d)
            dx12 = Monomial(-self.molt_a,0,1,0,0,0,self.shift_a,0,0,1,self.molt_a,1,1)

            dx21 = Monomial(self.b*self.r,self.a,self.b-1,self.c,self.d,self.shift_a,self.shift_b,self.shift_c,self.shift_d,self.molt_a,self.molt_b,self.molt_c,self.molt_d)
            dx22 = Monomial(self.molt_b,1,0,0,0,self.shift_b,0,0,0,self.molt_b,1,1,1)
            
            dx2 = ProductMonomial([dx21,dx22])
            dx1 = ProductMonomial([dx11,dx12])
        else:
            dx1 = Monomial(-self.molt_a*self.a*self.r,self.a-1,self.b+1,self.c,self.d,self.shift_a,self.shift_b,self.shift_c,self.shift_d,self.molt_a,self.molt_b,self.molt_c,self.molt_d) 
            dx2 = Monomial(self.molt_b*self.b*self.r,self.a+1,self.b-1,self.c,self.d,self.shift_a,self.shift_b,self.shift_c,self.shift_d,self.molt_a,self.molt_b,self.molt_c,self.molt_d)

        return (dx1,dx2)

    def dy(self):
        if self.molt_c!=self.molt_d or self.shift_c!=self.shift_d:
            dy11 = Monomial(self.c*self.r,self.a,self.b,self.c-1,self.d,self.shift_a,self.shift_b,self.shift_c,self.shift_d,self.molt_a,self.molt_b,self.molt_c,self.molt_d)
            dy12 = Monomial(-self.molt_c,0,0,0,1,0,0,0,self.shift_c,1,1,1,self.molt_c)        
            
            dy21 = Monomial(self.d*self.r,self.a,self.b,self.c,self.d-1,self.shift_a,self.shift_b,self.shift_c,self.shift_d,self.molt_a,self.molt_b,self.molt_c,self.molt_d)
            dy22 = Monomial(self.molt_d,0,0,1,0,0,0,self.shift_d,0,1,1,self.molt_d,1)

            dy1 = ProductMonomial([dy11,dy12])
            dy2 = ProductMonomial([dy21,dy22])
        
        else:
            dy1 = Monomial(-self.molt_c*self.c*self.r,self.a,self.b,self.c-1,self.d+1,self.shift_a,self.shift_b,self.shift_c,self.shift_d,self.molt_a,self.molt_b,self.molt_c,self.molt_d) 
            dy2 = Monomial(self.molt_d*self.d*self.r,self.a,self.b,self.c+1,self.d-1,self.shift_a,self.shift_b,self.shift_c,self.shift_d,self.molt_a,self.molt_b,self.molt_c,self.molt_d)

        return (dy1,dy2)

    def __str__(self):
        f=''
        c=self.get_coeffs()+self.get_shifts()+self.get_molts()  #c è una lista di 13 numeri (1 coeff direttore[0], 4 esponenti[1,2,3,4], 4 schift[5,6,7,8], 4 moltiplicatori[9,10,11,12])
        if c[0]>1:
            f+='+'+str(c[0])
        if c[0]==1:
            f+='+'
        if c[0]==-1:
            f+='-'
        if c[0]<-1:
            f+=str(c[0])
        
        if c[1]==1:
            if c[9]==0:
                raise Exception('ERRORE DI SINTASSI')
            if c[9]==1:
                if c[5]>0:
                    f+='cos(x+'+str(c[5])+')'
                if c[5]==0:
                    f+='cos(x)'
                if c[5]<0:
                    f+='cos(x'+str(c[5])+')'
            else:
                if c[5]>0:
                    f+='cos('+str(c[9])+'x+'+str(c[5])+')'
                if c[5]==0:
                    f+='cos('+str(c[9])+'x)'
                if c[5]<0:
                    f+='cos('+str(c[9])+'x'+str(c[5])+')'
        if c[1]>1:
            if c[9]==0:
                raise Exception('ERRORE DI SINTASSI')
            if c[9]==1:
                if c[5]>0:
                    f+='cos^'+ str(c[1])+'(x+'+str(c[5])+')'
                if c[5]==0:
                    f+='cos^'+ str(c[1])+'(x)'
                if c[5]<0:
                    f+='cos^'+ str(c[1])+'(x'+str(c[5])+')'
            else:
                if c[5]>0:
                    f+='cos^'+ str(c[1])+'('+str(c[9])+'x+'+str(c[5])+')'
                if c[5]==0:
                    f+='cos^'+ str(c[1])+'('+str(c[9])+'x)'
                if c[5]<0:
                    f+='cos^'+ str(c[1])+'('+str(c[9])+'x'+str(c[5])+')'
        if c[1]<0:
            raise Exception('ERRORE DI SINTASSI')

        if c[2]==1:
            if c[10]==0:
                raise Exception('ERRORE DI SINTASSI')
            if c[10]==1:
                if c[6]>0:
                    f+='sin(x+'+str(c[6])+')'
                if c[6]==0:
                    f+='sin(x)'
                if c[6]<0:
                    f+='sin(x'+str(c[6])+')'
            else:
                if c[6]>0:
                    f+='sin('+str(c[10])+'x+'+str(c[6])+')'
                if c[6]==0:
                    f+='sin('+str(c[10])+'x)'
                if c[6]<0:
                    f+='sin('+str(c[10])+'x'+str(c[6])+')'
        if c[2]>1:
            if c[10]==0:
                raise Exception('ERRORE DI SINTASSI')
            if c[10]==1:
                if c[5]>0:
                    f+='sin^'+ str(c[2])+'(x+'+str(c[6])+')'
                if c[5]==0:
                    f+='sin^'+ str(c[2])+'(x)'
                if c[5]<0:
                    f+='sin^'+ str(c[2])+'(x'+str(c[6])+')'
            else:
                if c[5]>0:
                    f+='sin^'+ str(c[2])+'('+str(c[10])+'x+'+str(c[6])+')'
                if c[5]==0:
                    f+='sin^'+ str(c[2])+'('+str(c[10])+'x)'
                if c[5]<0:
                    f+='sin^'+ str(c[2])+'('+str(c[10])+'x'+str(c[6])+')'
        if c[2]<0:
            raise Exception('ERRORE DI SINTASSI')

        if c[3]==1:
            if c[11]==0:
                raise Exception('ERRORE DI SINTASSI')
            if c[11]==1:
                if c[7]>0:
                    f+='cos(y+'+str(c[7])+')'
                if c[5]==0:
                    f+='cos(y)'
                if c[5]<0:
                    f+='cos(y'+str(c[7])+')'
            else:
                if c[5]>0:
                    f+='cos('+str(c[11])+'y+'+str(c[7])+')'
                if c[5]==0:
                    f+='cos('+str(c[11])+'y)'
                if c[5]<0:
                    f+='cos('+str(c[11])+'y'+str(c[7])+')'
        if c[3]>1:
            if c[11]==0:
                raise Exception('ERRORE DI SINTASSI')
            if c[11]==1:
                if c[7]>0:
                    f+='cos^'+ str(c[3])+'(y+'+str(c[7])+')'
                if c[7]==0:
                    f+='cos^'+ str(c[3])+'(y)'
                if c[7]<0:
                    f+='cos^'+ str(c[3])+'(y'+str(c[7])+')'
            else:
                if c[7]>0:
                    f+='cos^'+ str(c[3])+'('+str(c[11])+'y+'+str(c[7])+')'
                if c[7]==0:
                    f+='cos^'+ str(c[3])+'('+str(c[11])+'y)'
                if c[7]<0:
                    f+='cos^'+ str(c[3])+'('+str(c[11])+'y'+str(c[7])+')'
        if c[3]<0:
            raise Exception('ERRORE DI SINTASSI')

        if c[4]==1:
            if c[12]==0:
                raise Exception('ERRORE DI SINTASSI')
            if c[12]==1:
                if c[8]>0:
                    f+='sin(y+'+str(c[8])+')'
                if c[8]==0:
                    f+='sin(y)'
                if c[8]<0:
                    f+='sin(y'+str(c[8])+')'
            else:
                if c[8]>0:
                    f+='sin('+str(c[12])+'y+'+str(c[8])+')'
                if c[8]==0:
                    f+='sin('+str(c[12])+'y)'
                if c[8]<0:
                    f+='sin('+str(c[12])+'y'+str(c[8])+')'
        if c[4]>1:
            if c[12]==0:
                raise Exception('ERRORE DI SINTASSI')
            if c[12]==1:
                if c[8]>0:
                    f+='sin^'+str(c[4])+'(y+'+str(c[8])+')'
                if c[8]==0:
                    f+='sin^'+str(c[4])+'(y)'
                if c[8]<0:
                    f+='sin^'+str(c[4])+'(y'+str(c[8])+')'
            else:
                if c[8]>0:
                    f+='sin^'+str(c[4])+'('+str(c[12])+'y+'+str(c[8])+')'
                if c[8]==0:
                    f+='sin^'+str(c[4])+'('+str(c[12])+'y)'
                if c[8]<0:
                    f+='sin^'+str(c[4])+'('+str(c[12])+'y'+str(c[8])+')'
        if c[4]<0:
            raise Exception('ERRORE DI SINTASSI')
        
        return f

class ProductMonomial:
    #CONSTRUCTOR
    #m è una lista non vuota di Monomial di cui prenderemo il prodotto
    def __init__(self, m):
        self.monos = m

    def eval(self,x,y):
        value=1
        for mono in self.monos:
            value=value*mono.eval(x,y)
        return value

    def __str__(self):
        f=''
        for mono in self.monos:
            if f=='':
                f+=mono.__str__()
            else:
                if mono.__str__()[0]=='-':
                    f+=mono.__str__()[1:]
                    temp=f[1:]
                    if f[0]=='-':
                        f='+' + temp
                    else:
                        f='-' + temp
                if mono.__str__()[0]=='+':
                        f+=mono.__str__()[1:]

        return f


"""Ora costruiamo i polinomi: ogni polinomio è una somma di monomi che noi interpretiamo 
come lista di oggetti della classe Monomial"""
class ourPolynomial:
    #CONSTRUCTOR
    #m è una lista non vuota di Monomial e ProductMonomial di cui prenderemo la somma
    def __init__(self, m):
        self.monomials = m

    #GETTERS
    def get_monomials(self):
        return self.monomials
    
    """per printare il polinomio in modo comodo
    trasformiamo ogni monomio in string e poi sommiamo il tutto in un'unica stringa"""
    def __str__(self):
        f = ''
        for mono in self.monomials:
            if mono.__str__()!='':
                if f=='' and  mono.__str__()=='+':                     
                    f+='1'
                if f=='' and  mono.__str__()[0]=='+' and  mono.__str__()!='+':                     
                    f+=mono.__str__()[1:]
                else:
                    f+=mono.__str__()
        return f

    def dx(self):
        l = []      #lista di Monomial ognuno rappresentante le due derivate rispetto alla x derivante da ognuno dei monomi
        for m in self.monomials:
            pair = m.dx()
            l.append(pair[0])               #pair[0] è un Monomial
            l.append(pair[1])               #pair[1] è un Monomial
        dx = ourPolynomial(l)               #quindi l è una lista di Monomial
        return dx

    def dy(self):
        l = []      #lista di Monomial ognuno rappresentante le due derivate rispetto alla y derivante da ognuno dei monomi
        for m in self.monomials:
            pair = m.dy()
            l.append(pair[0])               #pair[0] è un Monomial
            l.append(pair[1])               #pair[1] è un Monomial
            dy = ourPolynomial(l)           #quindi l è una lista di Monomial
        return dy

    def gradient(self):
        return [self.dx(),self.dy()]
    '''questo ridà una lista con due ourPolynomial'''

    def eval(self,x,y):
        value = 0
        for m in self.monomials:
            value += m.eval(x,y)
        return value

"""COSTRUZIONE DEL PARSER: data una stringa che rappresenta una funzione polinomiale in cos e sen con argomenti (a_1*x+b_1) e (a_2*y+b_2)
ricaviamo i coefficieni (r,a,b,c,d) relativi a ogni monomio che compare nella stringa
In questo modo otteniamo un polinomio, ovvero un oggetto di ourPolynomial"""

'''funziona con input una stringa rappresentante un polinomio in cosx,senx(o sinx),cosy,seny(o siny) eccetera
con parentesi, con ^ con ** con np.cos ecc con tutto quello che può scrivere di sensato l'utente con shift
usando le parentesi per l'argomento delle funzioni trigonometriche'''
#ora voglio provare anche a mettere dei coefficienti davanti a x e y ---> ammettere cos(2x)
def parse(poli):                                    #poli è una stringa che rappresenta un input polinomiale da parte dell'utente
    '''inizializzo il polinomio'''
    s=''                                            #stringa ausiliaria per salvare i vari coefficienti da trasformare in interi
    m=np.array([[0,0,0,0,0]])                       #lista che sarà la lista di monomi
    test=0
    shift_test=0

    for c in poli:                                 #[forse non serve a niente, ma] riempio m con il giusto numero di liste indicizzate a 0
        if c in ['x','y']:
            if len(poli)>test+1:
                if poli[test+1] in ['+','-'] and poli[test+2] in ['0','1','2','3','4','5','6','7','8','9',')']:     #controllo se ho uno shift
                    shift_test=1
        if c in ['+','-'] and shift_test==0:
            m=np.append(m,[[0,0,0,0,0]],axis=0)
        elif c in ['+','-'] and shift_test==1:
            shift_test=0
        test=test+1
    if poli[0] in '+-' or (poli[0]=='(' and poli[1] in '-+'):               #in questo caso ne sto mettendo uno di troppo, la tolgo
        m=np.delete(m,0,0)

    #aggiungiamo gli shift
    shift=np.array([[0,0,0,0]])                                #lista degli shift per ogni monomio
    molt=np.array([[1,1,1,1]])                                 #lista dei coeff che moltiplicano x e y per ogni monomio
    for mono in m[1:]:
        shift=np.append(shift,[[0,0,0,0]],axis=0)
        molt=np.append(molt,[[1,1,1,1]],axis=0)
    
    shift_test=0       #test che mi dice se il prossimo coefficiente numerico che troverò sarò uno shift
    molt_test=0        #test che mi dice se il prossimo coefficiente numerico che troverò sarò un moltiplicatore di x o y
    i=0                #indice per percorrere la lista m
    p=0                #indice di parità che distingue numero [posizione 0] coseno [posizione 1 e 3] e seno [posizione 2 e 4] mi dice dove mettere il coeff che ho salvato
    test=0             #conto le iterazioni, serve per controllare la s di cos
    test2=0
    temp=''            #serve per salvare l'esponente di seno e coseno in caso ci sia un coeff davanti a x,y

    '''riempio m con i coefficienti giusti'''
    for c in poli:
        if c=='(':
            if poli[test-1] in ['s','n']:
                temp='1'
            if poli[test-1] not in ['s','n','0','1','2','3','4','5','6','7','8','9']:
                raise Exception('ERRORE DI SINTASSI')
            test2=test
            for c in poli[test+1:]:
                if c in ['-','0','1','2','3','4','5','6','7','8','9'] and molt_test==0:
                    test2=test2+1
                else:
                    if test2>test and poli[test2+1] in ['x','y']:
                        molt_test=1                                 #vuol dire che troverò un coefficiente moltiplicativo di x o y
                        test2=0
                    elif molt_test!=1:
                        molt_test=2                                 #vuol dire che non troverò un coefficiente moltilpicativo di x o y
            if molt_test==2:
                molt_test=0

        if molt_test==1 and temp=='':
            temp=s
            s=''

        if c==')' and shift_test==1:                                #se ho trovato uno shift(test in fondo quando trovo x o y) lo inserisco nella lista degli shift
            if s=='+' or s=='-':
                raise Exception('ERRORE DI SINTASSI')
            else:
                shift[i,p-1]=int(s)
                s=''
                shift_test=0
            p=0

        if c in ['+','-','0','1','2','3','4','5','6','7','8','9']:
            s+=c                                                    #aggiungo tutti i caratteri numerici alla stringa ausiliaria fichè finiscono i numeri, poi posiziono questo coeff nel punto giusto
            if (c in ['+','-']) and m[0,0]!=0 and shift_test==0:  #vuol dire che ho già incontrato un monomio e ne sto incontrando un altro; assumo che l'utente non metta 0 come primo coefficiente...
                i=i+1                                               #quindi incremento l'indice che scorre m

        if c=='c':                              #ho incontrato un coseno (o risp a x o risp a y )
            if s in ['+','-']:                  #vuol dire che sono a inizio polinomio e ho cos o -cos
                m[i,p]=int(s+'1')
                s=''
            elif s!='' and s[0] in ['+','-']:   #vuol dire che sono a inizio monomio, quindi salvo in posizione 0 (p=0) il coeffisciente che ho salvato in s                
                m[i,p]=int(s)
                s=''
            elif m[0,0]==0:                     #per salvare il primissimo coeff, che se è positivo non ha + davanti; assumo che l'utente non metta 0 come primo coefficiente...
                if s=='':
                    m[i,p]=1
                else:
                    m[i,p]=int(s)
                    s=''
            p=1
        if c=='s':                              
            if poli[test-2]!='c':                   #ho un seno (o risp a x o risp a y), il test True vuol dire che non è la s di cos
                if s in['+','-']:                   #vuol dire che sono a inizio polinomio e ho sen o -sen
                    m[i,p]=int(s+'1')
                    s=''
                elif s!='' and s[0] in ['+','-']:   #vuol dire che sono a inizio monomio, quindi salvo in posizione 0 (qui p=0) il coeffisciente che ho salvato in s
                    m[i,p]=int(s)
                    s=''
                elif m[0,0]==0:                     #per salvare il primissimo coeff; assumo che l'utente non metta 0 come primo coefficiente..
                    if s=='':
                        m[i,p]=1
                    else:                           
                        m[i,p]=int(s)
                        s=''
                p=2

        if c=='x':                                  #ho trovato un fattore, cosx se p=0, senx se p=2, inserisco il coefficiente trovato nell'iterazione precedenti
            if molt_test==1:                        #vuol dir che il numero che ho appena salvato in s è un coefficiente moltiplicativo di x
                if s in ['+','-']:
                    molt[i,p-1]=int(s+'1')
                else:
                    molt[i,p-1]=int(s)
                s=''
                molt_test=0
            else:
                temp=s
            if m[i,p]!=0:                           #vuol dire che in quel monomio ho già inserito l'esponente relativo a quel fattore
                raise Exception('ERRORE DI SINTASSI')
            if temp=='':                               #caso in cui ho esponente 1 e non ho scritto ^1
                m[i,p]=1
            else:
                m[i,p]=int(temp)
                s=''
            temp=''
            if len(poli)>test+1:
                if poli[test+1] in ['+','-'] and poli[test+2] in ['0','1','2','3','4','5','6','7','8','9',')']:     #controllo se ho uno shift
                    shift_test=1
                else:
                    p=0
        if c=='y':                                  #ho trovato un fattore, cosy se p=0, seny se p=2, inserisco il coefficiente trovato nell'iterazione precedenti
            p=p+2                                   #poichè ho y incremento di 2 la posizione in cui salvare il coefficiente
            if molt_test==1:                        #vuol dir che il numero che ho appena salvato in s è un coefficiente moltiplicativo di x
                if s in ['+','-']:
                    molt[i,p-1]=int(s+'1')                    
                else:
                    molt[i,p-1]=int(s)
                s=''
                molt_test=0
            else:
                temp=s
            if m[i,p]!=0:                           #vuol dire che in quel monomio ho già inserito l'esponente relativo a quel fattore
                raise Exception('ERRORE DI SINTASSI')     
            if temp=='':                               #caso in cui ho esponente 1 e non ho scritto ^1
                m[i,p]=1
            else:
                m[i,p]=int(temp)
                s=''
            temp=''
            if len(poli)>test+1:
                if poli[test+1] in ['+','-'] and poli[test+2] in ['0','1','2','3','4','5','6','7','8','9',')']:     #controllo se ho uno shift
                    shift_test=1
                else:
                    p=0     
        test=test+1
    size=np.size(m,0)
    l=[]
    for i in np.arange(0,size,1):
        l.append(Monomial(*list(np.append(np.append(m[i],shift[i]),molt[i]))))

    polinomio=ourPolynomial(l)

    return polinomio