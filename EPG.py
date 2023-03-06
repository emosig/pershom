import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from ProgrammaEPG import *
from ourPolynomial import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

# i=0
class EPGtab(tk.Frame):
    def __init__(self,master,f1,f2,points,tol1):
        super().__init__(master)
        self.f1=f1
        self.f2=f2
        self.x,self.epg,self.improper_arcs,self.titl=EPG(self.f1,self.f2,points,tol1)
        fig=EPG_plot(self.epg,self.titl)
        left_frame=ttk.Frame(self)
        left_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        canvas = FigureCanvasTkAgg(fig,master=left_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        right_frame=ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        noise_reduction_label = tk.Label(right_frame,text='Noise Reduction')
        noise_reduction_label.pack(padx=5,pady=5)
        noise_reduction_button = tk.Button(right_frame,text='Reduce')
        noise_reduction_button.pack(padx=5,pady=5)

class EPGplotter:
    def __init__(self,master):
        self.master=master
        master.title('EPGplotter')

        function_label=tk.Label(master,test='f=')
        function_label.grid(row=0,column=0,padx=5,pady=5)

        self.f1_entry=tk.Entry(master)
        self.f1_entry.grid(row=0,column=1,padx=5,pady=5)

        self.f2_entry=tk.Entry(master)
        self.f2_entry.grid(row=0,column=2,padx=5,pady=5)

        tol1_label=tk.Label(master,test='Tolerance=')
        tol1_label.grid(row=1,column=0,padx=5,pady=5)

        self.tol1_entry=tk.Entry(master)
        self.tol1_entry.grid(row=1,column=1,padx=5,pady=5)

        saveButton=tk.Button(master,test='Save to File',command=self.file_epg)
        saveButton.grid(row=2,column=0,padx=5,pady=5)

        plotButton=tk.Button(master,test='Plot the EPG',command=self.plot_epg)
        plotButton.grid(row=2,column=1,padx=5,pady=5)

        self.notebook=ttk.Notebook(master)
        self.notebook.grid(row=3,column=0,columnspan=2,padx=5,pady=5)

        self.tab_counter=0

        def file_epg():
            EPG_file(self.epg,self.titl,name='puntiEPG')

        def plot_epg():
            fig=EPG_plot(self.epg,self.titl)
            # frame = newFrameFromFig(fig,notebook)
            # notebook.add(frame,text='plot')


'''def newFrameFromFig(fig,master):
    frame = ttk.Frame(master)
    frame.pack(fill=tk.BOTH)
    canvas = FigureCanvasTkAgg(fig,master=frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return frame'''
'''
def calcEPG():
    print(f1.get(),f2.get())

    try: 
        f_1= parse(f1.get())
    except Exception as e:
        showerror(title='ERRORE', message='qualcosa è andato storto \n' + str(e))
        print(e.__traceback__)
        return

    try: 
        f_2= parse(f2.get())
    except Exception as e:
        showerror(title='ERRORE', message='qualcosa è andato storto \n' + str(e))
        print(e.__traceback__)
        return
    
    x,epg,improper_arcs,titl=EPG(f_1,f_2,200,0.001,0.1)
    
    return x,epg,improper_arcs,titl
'''
'''def plotEPG():
    # i=i+1
    x,epg,improper_arcs,titl=calcEPG()
    fig=EPG_plot(epg,titl)
    frame = newFrameFromFig(fig,notebook)
    notebook.add(frame,text='plot')

def fileEPG():
    epg,titl=calcEPG()
    EPG_file(epg,titl,name='puntiEPG')'''

root= Tk()
root.title('Extender Pareto Grid Calculation')
root.geometry('500x550+50+20')
#mainframe=ttk.Frame(root)
'''
Istruzioni=ttk.Label(root,text='Inserisci la prima funzione polinomiale in seno e coseno')
Istruzioni.pack()

f1=StringVar(value='cos(x)')
f1_entry=ttk.Entry(root, textvariable=f1)
f1_entry.pack()
f1_entry.focus()

f2=StringVar(value='sen(x)+cos(y)')
f2_entry=ttk.Entry(root, textvariable=f2)
f2_entry.pack()

PlotEPG=ttk.Button(root, command=plotEPG,text='Plot the EPG')
PlotEPG.pack()

FileEPG=ttk.Button(root, command=fileEPG,text='Save in File the EPG')
FileEPG.pack()

notebook = ttk.Notebook(root)
notebook.pack(side =TOP,fill=BOTH)
'''
#per far spuntare la finestra
root.mainloop()