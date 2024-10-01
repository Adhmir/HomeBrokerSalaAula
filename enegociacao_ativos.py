# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 13:47:18 2022

@author: Adhmir Renan Voltolini Gomes
"""


from tkinter import LabelFrame, Label, Button, OptionMenu, StringVar
from tkinter import ttk, Scrollbar, Toplevel, messagebox
#import numpy as np
#import pandas as pd
from tkinter import filedialog
import regra_negocio as rn
import grafico as gfc


def novajanela(root, df, per,saldodefinido):
        
    root1 = Toplevel(root)
    
    
    #root1 = Tk()
    
    #df = pd.read_excel('C:/PHD/A parte/Emulador acoes/historico_acoes.xlsx')
    df_completo = df.copy()
    #períodos disponíveis
    #per = '12'
    periodos_disponiveis = int(per)
    #data da cotação
    data_cotacao = periodos_disponiveis
    
    

    #função lista ações 
    # retorna:
    # [0]lista_acoes, [1]data_t, [2]data_t1, [3]df_ctc_fechadas, 
    # [4]df_cotacoes, [5]df_disponivel
    l_objetosa = rn.listasacoes(df_completo, periodos_disponiveis)
    # Preencher listbox na tela
    lista_acoes = l_objetosa[0]
    data_t = l_objetosa[1]
    data_t1 = l_objetosa[2]
    #df_ctc_fechadas = l_objetosa[3]
    df_cotacoes = l_objetosa[4]
    df_disponivel = l_objetosa[5]
    #função precoatual
    dic_preco_atual = rn.precoatual(lista_acoes, df_cotacoes)
    #conjuntos de dados
    lista_objetob = rn.conjunto_dados(data_t1,saldodefinido)
    df_historico = lista_objetob[0]
    
    """
    Novo conjunto de dados fixo para permitir apenas operações de compra
    """
    #df_fixo = rn.objeto_acoes(rn.lst_nome_acoes(df_completo.columns))
    df_fixo = rn.df_fixo(lista_acoes, data_t, dic_preco_atual)
    print(df_fixo)
    
    

    #df_hist_ordens = lista_objetob[1]
    df_ef = lista_objetob[2]
    df_resultado = lista_objetob[3]
    #Lista de lotes para compra
    Listaqdd = ['100', '200', '300', '400', '500', '600', '700', '800', '900', '1000']

    
    root1.title("Carteria de ativos")
    root1.iconbitmap("choice1.ico")
    root1.state('zoomed')
    root1.rowconfigure(0, weight=1) 
    style = ttk.Style()
    style.theme_use('clam')
    # clam', 'alt', 'default', 'classic'
    bkg = '#2f363b'
    frg =  '#c3d2db'
    btncolor = '#033454'
    root1.configure(bg=bkg )
    #lb_tasks.configure(bg=bg, fg=fg) .configure(bg='#65A8E1')
    style.configure("Treeview", background=bkg, 
                    fieldbackground=bkg, foreground=frg) 
    
    lbf = LabelFrame(root1, text= "Informações de mercado", height=100, width = 50, bg=bkg,fg=frg)  
    lbf.grid(row=0,column =0, ipady=100, ipadx=1)
    
    lbfBroker = LabelFrame(root1, text= "Emulador de ações", bg=bkg,fg=frg)  
    lbfBroker.grid(row=1,column =0) #, ipady=200)
    
    txtQdd = StringVar()
    txtQdd.set(Listaqdd[0])
    txtSel = StringVar()
    txtSel.set(lista_acoes[0])
    acao = str(txtSel.get())
    print(dic_preco_atual)
    cotacao = float(dic_preco_atual[acao])
    cotacao = round(cotacao,2)
    valortotal = round(cotacao,2)*float(txtQdd.get())

    #Essa função é necessária porque pega os valores dos option menu
    #E atualiza os label com os valores
    def ptotal(escolha):
        escolha = int(txtQdd.get())
        print(escolha)
        print('\nQuantidade: ',escolha)
        acao = str(txtSel.get())
        print(acao)
        cotacao = float(dic_preco_atual[acao])
        cotacao = round(cotacao,2)
        print('\ncotação: ',cotacao)
        valor = cotacao*escolha
        print('\nO Valor total é:',valor)
        #print(valor)
        lbCtc.config(text="Cotacao igual a : UM"+str(cotacao))
        #lbQdd.config(text="Quantidade"+str(escolha))
        valor =  "{:.2f}".format(valor)
        lbQdd.config(text="Quantidade : "+str(escolha))
        lbvTotal.config(text="Valor total: UM"+str(valor))
       
     
    
    #BtnRa = Button(lbf, text="Recomendações de Analistas", command=None, width = 30, 
    #               bg=btncolor,fg=frg,relief='groove')
    #BtnRa.grid(row=2,column =0) 
    
    def jgrafico():
        nonlocal lista_acoes, df_disponivel
        gfc.novajanela(root1, df_disponivel, txtSel, lista_acoes, ptotal)
       
   
    BtnAt = Button(lbf, text="Gráfico de Ativos", command=jgrafico, width = 30, 
                   bg=btncolor,fg=frg,relief='groove')
    BtnAt.grid(row=2,column =0)
    
    lbfBroker = LabelFrame(root1, text= "Negociações", height=200, width = 100, bg=bkg,fg=frg)  
    lbfBroker.grid(row=1,column =0, ipadx=1, ipady=79)
    
    
    lbAtv = Label(lbfBroker, text ="Selecione o Ativo" , width = 20,  bg=bkg,fg=frg)
    lbAtv.grid(row=0,column =0, columnspan =2)
    optionAtv = OptionMenu(lbfBroker, txtSel, *lista_acoes, command=ptotal)
    optionAtv.config(width=10,  bg=bkg,fg=frg,relief='groove')
    optionAtv.grid(row=1,column =0, columnspan =2)
    lbCtc = Label(lbfBroker, text ="Cotacao igual a : UM"+str(round(cotacao,2)),
                                                                     width = 20,
                                                                     bg=bkg,fg=frg)
    lbCtc.grid(row=2,column =0, columnspan =2)
    optQdd = OptionMenu(lbfBroker, txtQdd, *Listaqdd, command=ptotal)
    optQdd.config(width=10, bg=bkg,fg=frg,relief='groove')
    optQdd.grid(row=4,column =0, columnspan =2)
    lbQdd = Label(lbfBroker, text ="Selecione a quantidade" , width = 20, bg=bkg,fg=frg)
    lbQdd.grid(row=3,column =0, columnspan =2)
    lbvTotal = Label(lbfBroker, text ="Total : UM"+str(valortotal) , width = 20, bg=bkg,fg=frg)
    lbvTotal.grid(row=5,column =0, columnspan =2)
    
    lbbc = Label(lbfBroker, text ="  ",bg=bkg,fg=frg)
    lbbc.grid(row=6,column =0, columnspan = 2)
    
    
    lbf = LabelFrame(root1, text= "Carteria de ativos", height=500, width = 50, bg=bkg,fg=frg)
    lbf.grid(row=0,column =1,  ipadx=250, ipady=170 )
    
   
    ## Treeview Widget
    tv1 = ttk.Treeview(lbf)
    tv1.place(relheight=1, relwidth=1)  
    
    treescrolly = Scrollbar(lbf, orient="vertical", command=tv1.yview) 
    treescrollx = Scrollbar(lbf, orient="horizontal", command=tv1.xview)   
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) 
    treescrollx.pack(side="bottom", fill="x")  
    treescrolly.pack(side="right", fill="y")
    
    
    lbfLo = LabelFrame(root1, text= "Histórico de Ordens", height=500, width = 50, bg=bkg,fg=frg)
    lbfLo.grid(row=1,column =1,  ipadx=250, ipady=170 )
    
    ## Treeview Widget bg=btncolor,fg=frg,relief='groove'
    tv2 = ttk.Treeview(lbfLo)
    tv2.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).
    
    treescrollyLo = Scrollbar(lbfLo, orient="vertical", command=tv2.yview) 
    tv2.configure( yscrollcommand=treescrollyLo.set)
    treescrollyLo.pack(side="right", fill="y")
    
    tv2.delete(*tv2.get_children())
    tv2["column"] = []
    tv2["column"] = list(df_historico.columns)
    tv2["column"]
    tv2["show"] = "headings"
    for column in tv2["columns"]: 
        tv2.heading(column, text=column) 
        tv2.column(column, width=100, stretch=0, minwidth=5)
    df_rows = df_historico.to_numpy().tolist()  
    for row in df_rows:
        tv2.insert("", "end", values=row)
    
    #Essa função atualiza a treeview do histórico de ordens
    def atualizarTvorderm():
        nonlocal df_historico  
        
        print('  função atualizarTvorderm')
        
        tv2.delete(*tv2.get_children())
        tv2["column"] = []
        print('pegou coluna do df histórico')
        tv2["column"] = list(df_historico.columns)
        tv2["column"]
        tv2["show"] = "headings"
        for column in tv2["columns"]: 
            tv2.heading(column, text=column) 
            tv2.column(column, width=100, stretch=0, minwidth=5)
        df_rows = df_historico.to_numpy().tolist()  
        for row in df_rows:
            tv2.insert("", "end", values=row)
    
    #Essa função seleciona os valores do option menu e chama
    #A função da regra de negócio para atualizar o conjunto de
    #histórico de ordens df_historico
    def negociar_atualizatv2(negociacao): #Treeview do histórico de ordens
        nonlocal df_historico        
        ptotal('escolha')
        
        acao = txtSel.get()
        print(acao)
        qdd = txtQdd.get() 
        print(qdd)
                        
        df_historico = rn.comprar_ativo(acao, int(qdd), dic_preco_atual,
                          df_historico, data_t, periodos_disponiveis,
                          data_cotacao, negociacao)
        print('antes treeview')
        atualizarTvorderm()
        print('depois treeview')
        
    def negociar_atualizatv2_2(negociacao): #Treeview do histórico de ordens
        nonlocal df_fixo, df_historico, data_t, dic_preco_atual  
        ptotal('escolha')
        
        acao = txtSel.get()
        print(acao)
        qdd = int(txtQdd.get())
        qdd1 = int(txtQdd.get()) 
        if negociacao == 'venda':
            qdd = qdd*-1
                
        preco = float(dic_preco_atual[acao])
        #df_fixo = rn.negociacao_na(df_fixo, acao, qdd, preco, negociacao, data_t, dic_preco_atual)
        
        limite = rn.limite_alavacagem(df_fixo,qdd,acao)
        limite_saldo = rn.limite_alavacagem_saldo(acao, dic_preco_atual, df_historico, 
                                    qdd, data_cotacao,negociacao)
        if negociacao == 'venda':
            if limite == 'verdadeiro':
                df_historico = rn.comprar_ativo(acao, int(qdd1), dic_preco_atual,
                                  df_historico, data_t, periodos_disponiveis,
                                  data_cotacao, negociacao)
                df_fixo = rn.negociacao_na(df_fixo, acao, qdd, preco, negociacao, data_t, dic_preco_atual)
                #df_fixo = rn.negociacao_na(df_fixo, acao, qdd, preco, negociacao)
                print('antes treeview')
                atualizarTvorderm()
                print('depois treeview')
                
            else:
                if limite == 'falso':
                    messagebox.showerror(title='Erro', message="Não é possível vender quantidade\nmaior que possui.")
                else:
                    messagebox.showerror(title='Erro', message="Saldo insuficiente para operação.")
        else:
            if limite == 'verdadeiro' and limite_saldo == 'verdadeiro':
                df_historico = rn.comprar_ativo(acao, int(qdd1), dic_preco_atual,
                                  df_historico, data_t, periodos_disponiveis,
                                  data_cotacao, negociacao)
                df_fixo = rn.negociacao_na(df_fixo, acao, qdd, preco, negociacao, data_t, dic_preco_atual)
                #df_fixo = rn.negociacao_na(df_fixo, acao, qdd, preco, negociacao)
                print('antes treeview')
                atualizarTvorderm()
                print('depois treeview')
            else:
                if limite == 'falso':
                    messagebox.showerror(title='Erro', message="Não é possível vender quantidade\nmaior que possui.")
                else:
                    messagebox.showerror(title='Erro', message="Saldo insuficiente para operação.")
        
     
    #Essas duas funções são necessárias porque se passar a função negociar_atualizatv2
    # com o argumento 'compra' e 'venda' nos botões BtnBuy/BtnSell, será negociado ao
    # iniciar a tela e não funcionará adequadamente.
    def btn_buy():
        #negociar_atualizatv2('compra')
        negociar_atualizatv2_2('compra')
    
    def btn_sell():
        #negociar_atualizatv2('venda')
        negociar_atualizatv2_2('venda')
            
    #Botões de negociação
    BtnBuy = Button(lbfBroker, text="Comprar", command = btn_buy, 
                    height=5, width = 10,
                    bg= '#2c9406', fg=frg, relief='groove')
    BtnBuy.grid(row=6,column =0, )
    BtnSell = Button(lbfBroker, text="Vender", command= btn_sell,  
                     height=5, width = 10,
                     bg= '#a60505', fg=frg, relief='groove')
    BtnSell.grid(row=6,column =1 )  
    
    #bg=btncolor,fg=frg,relief='groove'
    lbfWllt = LabelFrame(root1, text= " Resultado das Negociações", height=300, width = 150, bg=bkg,fg=frg)  
    lbfWllt.grid(row=1,column =2,  ipadx=200, ipady=170 )
     
    #lbfAvc = LabelFrame(root1, text= "Opções", height=100, width = 10,bg=bkg,fg=frg) 
    lbfAvc = LabelFrame(root1, text= "Opções", height=10, width = 10,bg=bkg,fg=frg)  
    #lbfAvc.grid(row=0,column =2, ipadx=30, ipady=100 )
    lbfAvc.grid(row=0,column =2, ipadx=0, ipady=0 )
    
    tv3 = ttk.Treeview(lbfWllt)
    tv3.place(relheight=1, relwidth=1) 
    
    treescrolly3 = Scrollbar(lbfWllt, orient="vertical", command=tv3.yview) 
    tv3.configure( yscrollcommand=treescrolly3.set) 
    treescrolly3.pack(side="right", fill="y")
    
    
    tv3.delete(*tv3.get_children())
    tv3["column"] = []
    tv3["column"] = list(df_resultado.columns)
    tv3["column"]
    tv3["show"] = "headings"
    for column in tv3["columns"]: 
        tv3.heading(column, text=column) # let the column heading = column name
        tv3.column(column, width=100, stretch=0, minwidth=5)
    df_rows = df_resultado.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv3.insert("", "end", values=row)
    
    acoes_ativas_tela = []
    acoes_ativas = []
    total = [0.00]
    disp = []
    
    def atualiza_periodo():
        nonlocal df_historico, data_t, data_t1, dic_preco_atual, df_fixo
        nonlocal df_ef, lista_acoes, periodos_disponiveis
        nonlocal data_cotacao, df_completo, df_cotacoes, df_disponivel, df_resultado
        nonlocal acoes_ativas_tela, acoes_ativas, total, disp
        
        
        lst_atualizada = rn.atualiza_periodo_dfs(df_historico, data_t,data_t1, dic_preco_atual, 
                                              df_ef,lista_acoes, periodos_disponiveis,
                                              data_cotacao,df_completo, df_cotacoes, 
                                              df_disponivel,df_resultado,df_fixo)
        
        
         
        #Preencher treeview após atualizar
        acoes_ativas_tela = lst_atualizada[0]
        #Para junção no histórico
        acoes_ativas = lst_atualizada[1]
        #Para adicionar resultado da carteira
        total = lst_atualizada[2]
        #Para concatenar a carteira e criar o efeito de disposição
        df_ef = lst_atualizada[3]
        #Atualizado o período disponivel ao usuário, rever uso do acento
        periodos_disponiveis = lst_atualizada[4]
        #Para atualizar o n da data da cotação
        data_cotacao = lst_atualizada[5]
        #Retorna o conjunto de dados completo
        df_completo = lst_atualizada[6] 
        #Para atualizar a cotação do próximo período
        df_cotacoes = lst_atualizada[7]
        #Retorna o conjunto de dados com a adição de mais um período
        df_disponivel = lst_atualizada[8]
        #Retorna um dicionário atualizado
        dic_preco_atual = lst_atualizada[9]
        #Retorna anterior mais 1
        data_t = lst_atualizada[10]
        #Retorna a data t-1 mais um
        data_t1 = lst_atualizada[11]
        
        df_fixo = rn.atualiza_df_fixo(df_fixo, data_t, dic_preco_atual)
        #Cria um conjunto de dados com o efeito de disposição
        disp = rn.efd(df_ef)
        df_resultado = lst_atualizada[12]
        ptotal('escolha')
        
    
    def atualizatv1(): #Treeview do resultado das negociações e carteira
        nonlocal acoes_ativas_tela, df_resultado, df_fixo
               
        atualiza_periodo()
     
        #Atualiza a treeview 3 referente aos resultados    
        tv1.delete(*tv1.get_children())
        tv1["column"] = []
        tv1["column"] = list(df_fixo.columns)
        tv1["column"]
        tv1["show"] = "headings"
        for column in tv1["columns"]: 
            tv1.heading(column, text=column) # let the column heading = column name
            tv1.column(column, width=100, stretch=0, minwidth=5)
        df_rows = df_fixo.to_numpy().tolist() # turns the dataframe into a list of lists
        for row in df_rows:
            tv1.insert("", "end", values=row)
            
        tv3.delete(*tv3.get_children())
        tv3["column"] = []
        tv3["column"] = list(df_resultado.columns)
        tv3["column"]
        tv3["show"] = "headings"
        for column in tv3["columns"]: 
            tv3.heading(column, text=column) # let the column heading = column name
            tv3.column(column, width=100, stretch=0, minwidth=5)
        df_rows = df_resultado.to_numpy().tolist() # turns the dataframe into a list of lists
        for row in df_rows:
            tv3.insert("", "end", values=row)
    

    BtnAvc = Button(lbfAvc, text="Avançar", command = atualizatv1, 
                    height=5, width = 20, bg= '#2c9406',fg=frg,relief='groove')
    BtnAvc.grid(row=0,column =0)
    
    lb_vazio = Label(lbfAvc, text="    ", 
                    height=5, width = 20,  bg=bkg,fg=frg)
    lb_vazio.grid(row=0,column =1)
    
    
    def salvar():
        nonlocal disp
         
        try:
            # with block automatically closes file
            with filedialog.asksaveasfile(mode='w', 
                                          defaultextension=".xlsx") as file:
                disp.to_excel(file.name, index = False)
        except AttributeError:
            # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
            print("Ação salvar cancelada!")
         
    
    
    BtnExportar = Button(lbfAvc, text="Exportar \nCarteiras", command = salvar, 
                    height=2, width = 20, bg=btncolor,fg=frg,relief='groove')
    BtnExportar.grid(row=2,column =0)
    
    
    def salvarBoleta():
        nonlocal df_historico
        
        try:
            # with block automatically closes file
            with filedialog.asksaveasfile(mode='w', 
                                          defaultextension=".xlsx") as file:
                df_historico.to_excel(file.name, index = False)
        except AttributeError:
            # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
            print("Ação salvar cancelada!")
         
    
    
    BtnExportarBoleta = Button(lbfAvc, text="Exportar \nHistórico de ordens", command = salvarBoleta, 
                    height=2, width = 20, bg=btncolor,fg=frg,relief='groove')
    BtnExportarBoleta.grid(row=3,column =0)
    
    
    def salvarResult():
        nonlocal df_resultado
        
        try:
            # with block automatically closes file
            with filedialog.asksaveasfile(mode='w', 
                                          defaultextension=".xlsx") as file:
                df_resultado.to_excel(file.name, index = False)
        except AttributeError:
            # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
            print("Ação salvar cancelada!")
    
    
    BtnExportarBoleta = Button(lbfAvc, text="Exportar \nResultado das negociações", command = salvarResult, 
                    height=2, width = 20, bg=btncolor,fg=frg,relief='groove')
    BtnExportarBoleta.grid(row=4,column =0)
    
   
    

    
        
    root1.mainloop()
        
     