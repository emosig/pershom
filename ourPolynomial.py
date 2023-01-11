import numpy as np

"""Costruiamo i monomi. Ogni monomio avrà un ordine interno, ovvero è della forma
r*(cos x)^a*(sen x)^b*(cos y)^c*(sen y)^d, quindi è identificato dalla tupla (r,a,b,c,d)
con r reale, a,b,c,d interi non negativi"""

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
    
    # CALCOLO DERIVATE PARZIALI
    #Ogni derivata parziale ritorna una i due monomi che poi andranno sommati seguendo le regole di derivazione del prodotto
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

    #questo non lo userei, poi servono vari shift.. poi vediamo
    def eval(self,x,y,shift):
        return self.r*(np.sin(x+shift)**self.a)*(np.cos(x+shift)**self.b)*(np.sin(y+shift)**self.c)*(np.cos(y+shift)**self.d)

"""Ora costruiamo i polinomi: ogni polinomio è una somma di monomi che noi interpretiamo 
come lista di oggetti della classe Monomial"""
class ourPolynomial:
    #CONSTRUCTOR
    #m è una lista non vuota di Monomial
    def __init__(self, m):
        self.monomials = m

    #GETTERS
    def get_monomials(self):
        return self.monomials           #questo ritorna una lista di liste (che sono i coefficienti)
    
    """per printare il polinomio in modo comodo
    trasformiamo ogni monomio in string e poi sommiamo il tutto in un'unica stringa"""
    def __str__(self):
        f = ''
        L=self.monomials
        for c in L:
            print(c)
            if c[0]>1:
                if f!='':
                    f+='+'+str(c[0])
                else:
                    f+=str(c[0])
            if c[0]==1:
                if f!='':
                    f+='+'
            if c[0]<0:
                f+=str(c[0])
            if c[1]==1:
                f+='cos(x)'
            if c[1]>1:
                f+=('cos^'+ str(c[1])+'(x)')
            if c[2]==1:
                f+='sin(x)'
            if c[2]>1:
                f+=('sin^'+ str(c[2])+'(x)')
            if c[3]==1:
                f+='cos(y)'
            if c[3]>1:
                f+=('cos^'+str(c[3])+'(y)')
            if c[4]==1:
                f+='sin(y)'
            if c[4]>1:
                f+=('sin^'+str(c[4])+'(y)')
        return f

    def dx(self):
        l = []      #lista di Monomial ognuno rappresentante le due derivate rispetto alla x derivante da ognuno dei monomi
        for m in self.monomials:
            pair = Monomial(*m).dx()        #l'* serve per passargli m come lista
            l.append(pair[0])
            l.append(pair[1])
        dx = ourPolynomial(l)
        return dx

    def dy(self):
        l = []      #lista di Monomial ognuno rappresentante le due derivate rispetto alla y derivante da ognuno dei monomi
        for m in self.monomials:
            pair = Monomial(*m).dy()        #l'* serve per passargli m come lista
            l.append(pair[0])
            l.append(pair[1])
        dy = ourPolynomial(l)
        return dy

    def gradient(self):
        return (self.dx(),self.dy())                           
    '''questo ridà un ourPolynomial'''

    def gradientCoeff(self):
        l1=[]
        l2=[]
        gradiente1=self.dx().get_monomials()
        gradiente2=self.dy().get_monomials()
        for m in gradiente1:
            l1.append(Monomial(*m.get_coeffs()).get_coeffs())       #l'* serve per passargli m.get_coeffs() come lista
        for m in gradiente2:
            l2.append(Monomial(*m.get_coeffs()).get_coeffs())       #l'* serve per passargli m.get_coeffs() come lista
        return (l1,l2)                                         
    '''questo ridà direttamente le liste'''

     #questo non lo userei 
    def eval(self,x,y,shift):
        value = 0
        for m in self.monomials:
            value += m.eval(x,y,shift)
        return value

"""COSTRUZIONE DEL PARSER: data una stringa che rappresenta una funzione polinomiale in cos x, sen x, cos y, sen y
ricaviamo i coefficieni (r,a,b,c,d) relativi a ogni monomio che compare nella stringa
In questo modo otteniamo un polinomio, ovvero un oggetto di ourPolynomial"""

'''funziona con input una stringa rappresentante un polinomio in cosx,senx(o sinx),cosy,seny(o siny)
con parentesi, con ^ con ** con np.cos ecc con tutto quello che può scrivere di sensato l'utente con shift, usando le parentesi per l'argomento delle funzioni trigonometriche, per quello secondo me bisogna fare un salto di qualità nella tecnologia che usiamo'''

def parse(poli):                                    #poli è una stringa che rappresenta un input polinomiale da parte dell'utente
    '''inizializzo il polinomio'''
    s=''                                            #stringa ausiliaria per salvare i vari coefficienti da trasformare in interi
    m=np.array([[0,0,0,0,0]])                       #lista che sarà la lista di monomi
    test=0
    
    for c in poli:                                  #[forse non serve a niente, ma] riempio m con il giusto numero di liste indicizzate a 0
        if c in ['+','-'] and poli[test-2:test] not in ['(x','(y']:
            m=np.append(m,[[0,0,0,0,0]],axis=0)
        test=test+1
    if poli[0]=='-' or (poli[0]=='(' and poli[1]=='-'):               #in questo caso ne sto mettendo uno di troppo, la tolgo (si presuppone che la stringa non inizi con +)
        m=np.delete(m,0)

    #aggiungiamo gli shift
    shift=np.array([[0,0,0,0]])                                 #lista degli shift in ogni monomio
    for mono in m[1:]:
        shift=np.append(shift,[[0,0,0,0]],axis=0)
    shift_test=0
    
    i=0                #indice per percorrere la lista m
    p=0                #indice di parità che distingue numero [posizione 0] coseno [posizione 1 e 3] e seno [posizione 2 e 4] mi dice dove mettere il coeff che ho salvato
    test=0             #conto le iterazioni, serve per controllare la s di cos
    '''riempio m e shift con i coefficienti giusti'''
    for c in poli:
        
        if c==')' and shift_test==1:                                #se ho trovato uno shift(test in fondo quando trovo x o y) lo inserisco nella lista degli shift
            if s=='+' or s=='-':
                print('ERRORE DI SINTASSI')
                return 0
            else:
                shift[i,p]=int(s)
                s=''
                shift_test=0
            p=0

        if c in ['+','-','0','1','2','3','4','5','6','7','8','9']:
            s+=c                                                    #aggiungo tutti i caratteri numerici alla stringa ausiliaria fichè finiscono i numeri, poi posiziono questo coeff nel punto giusto
            if (c in ['+','-']) and m[0,0]!=0 and (shift_test==0):  #vuol dire che ho già incontrato un monomio e ne sto incontrando un altro; assumo che l'utente non metta 0 come primo coefficiente...
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
            if m[i,p]!=0:                           #vuol dire che in quel monomio ho già inserito l'esponente relativo a quel fattore
                print('ERRORE DI SINTASSI')
                return 0     
            if s=='':                               #caso in cui ho esponente 1 e non ho scritto ^1
                m[i,p]=1
            else:
                m[i,p]=int(s)
                s=''
            if len(poli)>test+1:
                if poli[test+1] in ['+','-'] and poli[test+2] in ['0','1','2','3','4','5','6','7','8','9',')']:     #controllo se ho uno shift
                    shift_test=1
                else:
                    p=0
        if c=='y':                                  #ho trovato un fattore, cosy se p=0, seny se p=2, inserisco il coefficiente trovato nell'iterazione precedenti
            p=p+2                                   #poichè ho y incremento di 2 la posizione in cui salvare il coefficiente
            if m[i,p]!=0:                           #vuol dire che in quel monomio ho già inserito l'esponente relativo a quel fattore
                print('ERRORE DI SINTASSI')
                return 0
            if s=='':                               #caso in cui ho esponente 1 e non ho scritto ^1
                m[i,p]=1
            else:
                m[i,p]=int(s)
                s=''  
            if len(poli)>test+1:
                if poli[test+1] in ['+','-'] and poli[test+2] in ['0','1','2','3','4','5','6','7','8','9',')']:     #controllo se ho uno shift
                    shift_test=1
                else:
                    p=0         
        test=test+1
    return [m,shift]                                        #per ora ritorno la lista, perchè mi tornava comodo, altrimenti si farà return ourPolynomial(m)

'''ora voglio provare anche a mettere dei coefficienti davanti a x e y ---> ammettere cos(2x)'''

def parse2(poli):                                    #poli è una stringa che rappresenta un input polinomiale da parte dell'utente
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
    if poli[0]=='-' or (poli[0]=='(' and poli[1]=='-'):               #in questo caso ne sto mettendo uno di troppo, la tolgo (si presuppone che la stringa non inizi con +)
        m=np.delete(m,0)

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
    temp=''
    '''riempio m con i coefficienti giusti'''
    for c in poli:
        if c=='(':
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
                print('ERRORE DI SINTASSI')
                return 0
            else:
                shift[i,p]=int(s)
                s=''
                shift_test=0
            p=0

        if c in ['+','-','0','1','2','3','4','5','6','7','8','9']:
            s+=c                                                    #aggiungo tutti i caratteri numerici alla stringa ausiliaria fichè finiscono i numeri, poi posiziono questo coeff nel punto giusto
            if (c in ['+','-']) and m[0,0]!=0 and (shift_test==0):  #vuol dire che ho già incontrato un monomio e ne sto incontrando un altro; assumo che l'utente non metta 0 come primo coefficiente...
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
                    molt[i,p]=int(s+'1')
                    
                else:
                    molt[i,p]=int(s)
                s=''
                molt_test=0
            else:
                temp=s
            if m[i,p]!=0:                           #vuol dire che in quel monomio ho già inserito l'esponente relativo a quel fattore
                print('ERRORE DI SINTASSI')
                return 0     
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
                    molt[i,p]=int(s+'1')
                    
                else:
                    molt[i,p]=int(s)
                s=''
                molt_test=0
            else:
                temp=s
            if m[i,p]!=0:                           #vuol dire che in quel monomio ho già inserito l'esponente relativo a quel fattore
                print('ERRORE DI SINTASSI')
                return 0     
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
    return [m,shift,molt]                                        #per ora ritorno la lista, perchè mi tornava comodo, altrimenti si farà return ourPolynomial(m)