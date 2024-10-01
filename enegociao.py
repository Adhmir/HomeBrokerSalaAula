# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 15:24:07 2022

@author: user
"""
 

# Youtube Link da tela inicial: https://www.youtube.com/watch?v=PgLjwl6Br0k

#import tkinter as tk
from tkinter import Tk, LabelFrame, Button, Scrollbar,Label
from tkinter import filedialog, ttk, messagebox #, PhotoImage
#from PIL import ImageTk, Image
#import os
import pandas as pd

import enegociacao_ativos as en_acoes
#import regra_negocio as rn


# initalise the tkinter GUI
root = Tk()

#df_completo = pd.read_excel('C:/PHD/A parte/Emulador acoes/historico_acoes.xlsx')


root.title("emulador negociação")

root.title("Carteria de ativos")
root.iconbitmap("choice1.ico")

root.state('zoomed')
root.rowconfigure(0, weight=1) 
style = ttk.Style()
style.theme_use('clam')
# clam', 'alt', 'default', 'classic'
bkg = '#2f363b'
frg =  '#c3d2db'
btncolor = '#033454'
root.configure(bg=bkg )
#lb_tasks.configure(bg=bg, fg=fg) .configure(bg='#65A8E1')
style.configure("Treeview", background=bkg, 
                fieldbackground=bkg, foreground=frg) 


root.state('zoomed')
#root.geometry("500x500") # set the root dimensions
#root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
#root.resizable(0, 0) # makes the root window fixed in size.


#photo1 = PhotoImage(file = 'choice.ico')
root.iconbitmap('choice1.ico')
# Setting icon of master window
#root.iconphoto(False, photo1)

# Frame for open file dialog
file_frame = LabelFrame(root, text="Conjunto de dados", background=bkg)
file_frame.place(height=100, width=1200, rely=0.58, relx=0)


file_frame1 = LabelFrame(root, text="Configurações iniciais", background=bkg)
file_frame1.place(height=100, width=1200, rely=0.75, relx=0, )
 

# Buttons
button1 = Button(file_frame, text="Buscar    ",
                    bg=btncolor,fg=frg,relief='groove', font = 'time 15 bold',
                    command=lambda: File_dialog())
button1.place(rely=0.4, relx=0.10)

button2 = Button(file_frame, text="Carregar", 
                    bg=btncolor,fg=frg,relief='groove', font = 'time 15 bold',
                    command=lambda: Load_excel_data())
button2.place(rely=0.4, relx=0.20)

button3 = Button(file_frame, text="Limpar  ", 
                    bg=btncolor,fg=frg,relief='groove', font = 'time 15 bold',
                    command=lambda: clear_data())
button3.place(rely=0.4, relx=0.30)

button4 = Button(file_frame1, text="Iniciar ", 
                    bg=btncolor,fg=frg,relief='groove', font = 'time 15 bold',
                    command=lambda: novajanela())
button4.place(rely=0.2, relx=0.10)

txt1 = ttk.Entry(file_frame1, width = 10, textvariable = "",font = 'time 15 bold')
txt1.place(rely=0.4, relx=0.90)

lbper = Label(file_frame1, text ="Períodos" , width = 20,  bg=bkg,fg=frg)
lbper.place(rely=0.10, relx=0.87)

txt2 = ttk.Entry(file_frame1, width = 10, textvariable = "",font = 'time 15 bold')
txt2.place(rely=0.4, relx=0.70)

lbper1 = Label(file_frame1, text ="Saldo inicial" , width = 20,  bg=bkg,fg=frg)
lbper1.place(rely=0.10, relx=0.67)

"""
txt2 = ttk.Entry(file_frame1, width = 15, textvariable = "100000")
txt2.place(rely=0.4, relx=0.60)

lbsaldo = Label(file_frame1, text ="Saldo inicial sem pontos" , width = 20,  bg=bkg,fg=frg)
lbsaldo.place(rely=0.4, relx=0.50)
"""

# The file/file path text
label_file = ttk.Label(file_frame, text="Nenhum arquivo selecionado, clique em buscar")
label_file.place(rely=0, relx=0)

# Frame for TreeView
frame1 = LabelFrame(root, text="Conjunto de dados")
frame1.place(height=400, width=1200)


## Treeview Widget
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly = Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
treescrollx = Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget



def File_dialog():
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
    label_file["text"] = filename
    return None


def Load_excel_data():
    """If the file selected is valid this will load the file into the Treeview"""
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
        else:
            df = pd.read_excel(excel_filename)

    except ValueError:
        messagebox.showerror("Information", "Arquivo escolhido inválido")
        return None
    except FileNotFoundError:
        messagebox.showerror("Information", f"{file_path}")
        return None

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None

def pegar_dados():
    file_path = label_file["text"]
    excel_filename = r"{}".format(file_path)
    if excel_filename[-4:] == ".csv":
        df = pd.read_csv(excel_filename)
    else:
        df = pd.read_excel(excel_filename)
        return df
    

def clear_data():
    tv1.delete(*tv1.get_children())
    tv1["column"] = []
    return None

#Nova janela ADRIANA
def novajanela():
    per = txt1.get()
    saldodefinido = txt2.get()
    if saldodefinido != "":
        saldodefinido = float(saldodefinido)
    else:
        saldodefinido = 100000
        
    print('\nOperíodo do texto é igual a:', int(per))
    en_acoes.novajanela(root, pegar_dados(),per,saldodefinido) 
    #slv.novajanela(root, pegar_dados()) 
    pass


root.mainloop()