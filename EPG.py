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

def newFrameFromFig(fig,master):
    frame = ttk.Frame(master)
    frame.pack(fill=BOTH)
    canvas = FigureCanvasTkAgg(fig,master=frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    return frame

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
    
    epg,titl=EPG(f_1,f_2,200,0.001,0.1)
    
    return epg,titl

def plotEPG():
    # i=i+1
    epg,titl=calcEPG()
    fig=EPG_plot(epg,titl)
    frame = newFrameFromFig(fig,notebook)
    notebook.add(frame,text='plot')

def fileEPG():
    epg,titl=calcEPG()
    EPG_file(epg,titl,name='puntiEPG')

root= Tk()
root.title('Extender Pareto Grid Calculation')
root.geometry('500x550+50+20')
#mainframe=ttk.Frame(root)

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

#per far spuntare la finestra
root.mainloop()