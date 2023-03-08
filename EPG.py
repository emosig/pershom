import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from tkinter import filedialog
from ProgrammaEPG import *
from Rette import noise_reduction
from ourPolynomial import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
    
class EPGtab(tk.Frame):
    def file_epg(self):
        try:   
            filename=filedialog.asksaveasfilename(
                initialfile="epg_points.txt",
                defaultextension='.txt',
                filetypes=[ ("Tutti i file","*"),
                            ("File di Testo","*.txt"),
                            ("Python","*.py"),
                            ("Markdown","*.md"),
                            ("Javascript","*.js"),
                            ("HTML","*.html"),
                            ("CSS","*.css")])
            EPG_file(self.epg+self.improper_arcs,self.titl,name=filename)

        except Exception as e:
            print(e)

    def file_epg_refined(self):
        try:   
            filename=filedialog.asksaveasfilename(
                initialfile="epg_points.txt",
                defaultextension='.txt',
                filetypes=[ ("Tutti i file","*"),
                            ("File di Testo","*.txt"),
                            ("Python","*.py"),
                            ("Markdown","*.md"),
                            ("Javascript","*.js"),
                            ("HTML","*.html"),
                            ("CSS","*.css")])
            EPG_file(self.epg_refined,self.titl_refined,name=filename)

        except Exception as e:
            print(e)


    def reduce_noise(self):
        try: 
            self.tol2 = float(self.tol2_entry.get())
            if self.tol2 < 0: 
                    showerror(title='ERRORE', message='tol1 deve essere positiva \n')
                    return        
        except Exception as e:
            showerror(title='ERRORE', message='qualcosa è andato storto \n' + str(e))
            return
        
        try: 
            self.slope = float(self.slope_entry.get())
            if self.slope < 0: 
                    showerror(title='ERRORE', message='tol1 deve essere positiva \n')
                    return        
        except Exception as e:
            showerror(title='ERRORE', message='qualcosa è andato storto \n' + str(e))
            return

        self.x_refined,self.epg_refined,self.titl_refined = noise_reduction(self.x,self.f1,self.f2,self.tol2,self.titl,self.improper_arcs,m=self.slope)
        #self.x_refined,self.epg_refined,self.improper_arcs_refined,self.titl_refined=EPG(parse('cos(x)'),parse('sen(x)'),200,0.01)
        
        fig=EPG_plot(self.epg_refined,self.titl_refined)
        canvas = FigureCanvasTkAgg(fig,master=self.right_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self.right_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.noise_reduction_button['state']='disabled'

        TextFile2=tk.Label(self.center_frame,text='Save the points of the\n new Extended Pareto Grid\n to .txt file')
        TextFile2.pack()

        saveButton2=tk.Button(master=self.center_frame,text='Save to File',command=self.file_epg_refined)
        saveButton2.pack(padx=5,pady=5)


    def __init__(self,master,f1,f2,points,tol1):
        super().__init__(master)
        self.f1 = f1
        self.f2 = f2
        self.points = points
        self.tol1 = tol1
        self.x,self.epg,self.improper_arcs,self.titl=EPG(self.f1,self.f2,points,tol1)

        fig=EPG_plot(self.epg+self.improper_arcs,self.titl)
        self.left_frame=ttk.Frame(self)
        self.left_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        canvas = FigureCanvasTkAgg(fig,master=self.left_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self.left_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.center_frame=ttk.Frame(self)
        self.center_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.right_frame=ttk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        TextFile=tk.Label(self.center_frame,text='Save the points of the\n Extended Pareto Grid\n to .txt file')
        TextFile.pack()

        saveButton=tk.Button(master=self.center_frame,text='Save to File',command=self.file_epg)
        saveButton.pack(padx=5,pady=5)

        noise_reduction_label = tk.Label(self.center_frame,text='Reduce the noise using lines\n inserting tollerance')
        noise_reduction_label.pack(padx=5,pady=5)
        
        tol2_label = tk.Label(self.center_frame,text='Line Tolerance')
        tol2_label.pack(padx=5,pady=5)
        self.tol2_entry = tk.Entry(master = self.center_frame)
        self.tol2_entry.pack(padx=5,pady=5) 
        self.tol2_entry.insert(0,str(self.tol1/10))

        slope_label = tk.Label(self.center_frame,text='Line Slope')
        slope_label.pack(padx=5,pady=5)
        self.slope_entry = tk.Entry(master = self.center_frame)
        self.slope_entry.pack(padx=5,pady=5) 
        self.slope_entry.insert(0,str(1))


        self.noise_reduction_button = tk.Button(self.center_frame,text='Reduce',command=self.reduce_noise)
        self.noise_reduction_button.pack(padx=5,pady=5)
        

class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])


class EPGplotter(Frame):
    def plot_epg(self):
            try: 
                f1 = parse(self.f1_entry.get())
            except Exception as e:
                showerror(title='ERRORE', message='qualcosa è andato storto \n' + str(e))
                return
            try: 
                f2 = parse(self.f2_entry.get())
            except Exception as e:
                showerror(title='ERRORE', message='qualcosa è andato storto \n' + str(e))
                return
            
            try:
                tol1 = float(self.tol1_entry.get())
                if tol1 < 0: 
                    showerror(title='ERRORE', message='tol1 deve essere positiva \n')
                    return
            except Exception as e:
                showerror(title='ERRORE', message='qualcosa è andato storto \n' + str(e))
                return
            
            try:
                points = int(self.points_entry.get())
                if points <= 0: 
                    showerror(title='ERRORE', message='points deve essere positiva \n')
                    return
            except Exception as e:
                showerror(title='ERRORE', message='qualcosa è andato storto \n' + str(e))
                return

            tab = EPGtab(self.notebook,f1,f2,points,tol1)
            # tab.pack()
            self.notebook.add(tab,text=f'plot {self.tab_counter}')
            self.tab_counter+=1


    def __init__(self,master):
        super().__init__(master)
        self.master=master
        master.title('EPGplotter')
        frame=tk.Frame(master)
        frame.pack(fill=tk.X)
        
        istruzioni1='Calculate the Extended Pareto Grid of a function from the flat torus to R^2\n the admissible functions are polinomials made of trigoniometric monomials of the type\n'
        istruzioni2='r cos^a(bx+c)sen^d(ex+f)cos^g(hy+i)sen^j(ky+l)\n with a,b,c,d,e,f,g,h,i,j,k,l integer numbers, a,d,g,j>0\n'
        istruzioni=istruzioni1+istruzioni2

        instructions=tk.Label(frame,text=istruzioni)
        instructions.grid(row=0,column=0)

        function_label=tk.Label(frame,text='f: f1 =')
        function_label.grid(row=0,column=1,padx=3,pady=3)
        #function_label.pack()

        self.f1_entry=tk.Entry(frame)
        self.f1_entry.grid(row=0,column=2,padx=3,pady=3)
        #self.f1_entry.pack()
        self.f1_entry.insert(0,'cos^2(x) + 3cos(y)')

        function2_label=tk.Label(frame,text='f2 =')
        function2_label.grid(row=0,column=3,padx=3,pady=3)

        self.f2_entry=tk.Entry(frame)
        self.f2_entry.grid(row=0,column=4,padx=3,pady=3)
        #self.f2_entry.pack()
        self.f2_entry.insert(0,'sen^3(x) + 3sen^2(y)')

        points_label=tk.Label(frame,text='Points=')
        points_label.grid(row=1,column=1,padx=3,pady=3)
        #points_label.pack()

        self.points_entry=tk.Entry(frame)
        self.points_entry.grid(row=1,column=2,padx=3,pady=3)
        #self.points_entry.pack()
        self.points_entry.insert(0,'200')

        tol1_label=tk.Label(frame,text='Tolerance=')
        tol1_label.grid(row=1,column=3,padx=3,pady=3)
        #tol1_label.pack()

        self.tol1_entry=tk.Entry(frame)
        self.tol1_entry.grid(row=1,column=4,padx=3,pady=3)
        #self.tol1_entry.pack()
        self.tol1_entry.insert(0,'0.1')


        plotButton=tk.Button(frame,text='Plot the EPG',command=self.plot_epg)
        plotButton.grid(row=1,column=5,padx=3,pady=3)
        #plotButton.pack()

        self.notebook=CustomNotebook(self)
        # self.notebook=ttk.Notebook(self)

        # self.notebook.grid(row=4,column=0,columnspan=4,padx=5,pady=5)
        self.notebook.pack()

        self.tab_counter=1


#per far spuntare la finestra
root= Tk()
root.title('Extended Pareto Grid Calculation')

epgPlotter = EPGplotter(root)
epgPlotter.pack()

root.mainloop()