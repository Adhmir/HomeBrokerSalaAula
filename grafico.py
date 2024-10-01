 
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:30:33 2022

@author: Adhmir Renan Voltolini Gomes
"""

#import matplotlib
#matplotlib.use('TKAgg')


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure

from tkinter import Label, Button, OptionMenu
from tkinter import   Toplevel, Frame, ttk

import pandas as pd

#import matplotlib.pyplot as plt


def novajanela(root, df_grafico, txtSel, ListaAtivos, ptotal):
           
    SVariable = Toplevel(root)
    SVariable.iconbitmap('choice1.ico')
    SVariable.title("Gráficos dos ativos")
    #SVariable.geometry("900x600") 
    SVariable.state('zoomed')
    
    
    style = ttk.Style()
    style.theme_use('clam')
    # clam', 'alt', 'default', 'classic'
    bkg = '#2f363b'
    frg =  '#c3d2db'
    btncolor = '#033454'
    SVariable.configure(bg=bkg )
    
    lbAtv = Label(SVariable, text ="Selecione o Ativo" , width = 20, bg=bkg, fg=frg)
    lbAtv.grid(row=0,column =0)
    optionAtv = OptionMenu(SVariable, txtSel, *ListaAtivos, command=ptotal)
    optionAtv.config(width=10, bg=bkg,fg=frg,relief='groove')  
    optionAtv.grid(row=0,column =1)

    def graph():
        #col = str(df.columns[5][:5])
        col = str(txtSel.get())
        df = df_grafico.copy()
        #print(col+'_Min')
        dfa = df[[col+'_MINIMO',col+'_ABERTURA',col+'_FECHAMENTO',col+'_MAXIMO']]
        dfa.set_index(df['Data'])
        dfa.columns = [ 'low','open','close','high']
        prices = dfa.copy()
        #create figure
        f = Figure(figsize=(12,6), dpi=100)
        a = f.add_subplot(111)
        #a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
               
        #plt.figure()
        #define width of candlestick elements
        width = .2
        width2 = .02
        #define up and down prices
        up = prices[prices.close>=prices.open]
        down = prices[prices.close<prices.open]
        #define colors to use
        col1 = 'steelblue'
        col2 = 'black'
        #plot up prices
        a.bar(up.index,up.close-up.open,width,bottom=up.open,color=col1)
        a.bar(up.index,up.high-up.close,width2,bottom=up.close,color=col1)
        a.bar(up.index,up.low-up.open,width2,bottom=up.open,color=col1)
        #plot down prices
        a.bar(down.index,down.close-down.open,width,bottom=down.open,color=col2)
        a.bar(down.index,down.high-down.open,width2,bottom=down.open,color=col2)
        a.bar(down.index,down.low-down.close,width2,bottom=down.close,color=col2)
        #rotate x-axis tick labels
        #a.xticks(rotation=45, ha='right')
        #display candlestick chart
        nperiodo =list(pd.Series(range(0,len(df)))) #df['Data']
        dnperiodo =list(df['Data']) #df['Data']
        a.set_xticks(nperiodo,dnperiodo, rotation=20) #a.xticks(nperiodo)
       
        #g = plt.show()
        
        canvas = FigureCanvasTkAgg(f, master = SVariable)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2,column=1, columnspan =3)
        
        toolbarFrame = Frame(SVariable)
        toolbarFrame.grid(row=4,column=1) 
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        
         
       
        #return g
    
    Btngrafico = Button(SVariable, text="Carregar", command=graph, width= 30,
                        bg=btncolor, fg=frg,relief='groove')
    Btngrafico.grid(row=1,column=1)
    