import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class myPlotter:
    #Classe per plottare i punti che diventeranno l'extended pareto grid
    #Per la regressione sto guardando questo https://machinelearningmastery.com/curve-fitting-with-python/
    #¿Che tipo di regressione è migliore?

    #CONSTRUCTOR
    def __init__(self, datax, datay):
        self.x = datax
        self.y = datay
        pass

    #Polynomial regression di grado 5
    def poly5(self,x,a,b,c,d,e,f):
            return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + f

    def poly_regr5(self):
        # curve fit
        popt, _ = curve_fit(self.poly5, self.x, self.y)
        # summarize the parameter values
        a, b, c, d, e, f = popt
        return a,b,c,d,e,f

    #Sine-quadratic regression
    def sine2(self,x,a,b,c,d):
            return a * np.sin(b - x) + c * x**2 + d

    def sine_regr2(self):
        # curve fit
        popt, _ = curve_fit(self.sine2, self.x, self.y)
        # summarize the parameter values
        a, b, c, d = popt
        return a,b,c,d


    #Funzione che plotta
    #Il parametro regr è per appliccare un metodo di curve fitting (self.poly_regr5())
    def plot(self, regr = ''):
        #la variabile fig c'è in ogni tutoriale che fa questa cosa ma io non ho capito a cosa serva
        fig, ax = plt.subplots()
        ax.scatter(self.x, self.y)
        ax.grid()

        #Questo pezzo si può scrivere più bello e più corto ma adesso devo andare a fare pranzo

        if(regr == 'poly5'):
            # define a sequence of inputs between the smallest and largest known inputs
            x_line = np.arange(min(self.x), max(self.x), 1)
            # calculate the output for the range
            a,b,c,d,e,f = self.poly_regr5()
            y_line = self.poly5(x_line, a, b, c, d, e, f)
            # create a line plot for the mapping function
            plt.plot(x_line, y_line, '--', color='red')

        elif(regr == 'sine2'):
            # define a sequence of inputs between the smallest and largest known inputs
            x_line = np.arange(min(self.x), max(self.x), 1)
            # calculate the output for the range
            a,b,c,d = self.sine_regr2()
            y_line = self.sine2(x_line, a, b, c, d)
            # create a line plot for the mapping function
            plt.plot(x_line, y_line, '--', color='red')

        #Dipingo gli assi
        ax.axhline(y=0, color='k')
        ax.axvline(x=0, color='k')

        plt.show()