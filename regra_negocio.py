# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 09:48:39 2022
dic_preco_atual
@author: Adhmir Renan Voltolini Gomes
"""

import pandas as pd
import numpy as np

#Função que retorna a lista das ações
def lst_nome_acoes(acoes):
    lst = []
    for i in acoes:
        j = i[0:5]
        if j not in lst:
            lst.append(j)
    return lst

def listasacoes(df_completo, periodos_disponíveis):
    periodos_disponíveis 
    data_cotacao = periodos_disponíveis
    #Coluna data em data
    df_completo['Data'] = df_completo['Data'].dt.strftime('%d/%m/%Y')
    #Colunas para listas
    colunas = list(df_completo.columns)
    #Menos a última que é a data
    lista_acoes = lst_nome_acoes(colunas[0:-1])
    #conjunto com dados visívies para o usuário
    df_disponivel = df_completo.iloc[0:periodos_disponíveis].copy()
    #datas t
    data_t = df_disponivel.iloc[-1, -1]
    #data t-1
    data_t1 = df_disponivel.iloc[-2, -1]
    #Conjunto de cotações
    df_cotacoes = df_completo.loc[:, df_completo.columns.str.endswith("FECHAMENTO")].copy()
    #Conjunto de cotações fechamento
    df_fechamento = df_completo.loc[:, df_completo.columns.str.endswith("FECHAMENTO")].copy()
    #Copia a data do conjunto completo
    df_periodo = df_completo['Data'].copy()
    #conjunto de dados com o período e as cotações
    df_ctc_fechadas = pd.concat([df_periodo,df_fechamento], 
                                axis=1,
                                ignore_index=True)
    #dicionário com todas as cotações    
    #dic_pre_cmplto = dict(zip(df_periodo,df_fechamento.values))
    #d
    df_cotacoes = df_cotacoes.iloc[data_cotacao-1:data_cotacao]   
    
    return lista_acoes, data_t, data_t1, df_ctc_fechadas, df_cotacoes, df_disponivel

def precoatual(lista_acoes, df_cotacoes):
    dic_preco_atual = dict(zip(lista_acoes, df_cotacoes.iloc[-1,:].values))
    return dic_preco_atual

def conjunto_dados(data_t1,sd_init):
 
    df_historico = pd.DataFrame(data=[[data_t1,sd_init,
                                     "",0,0,sd_init]],
                               columns=['Data','Saldo inicial','Ativo',
                                        'quantidade','preço','Saldo final'])
    
    df_hist_ordens = pd.DataFrame(data=[],columns=['Data','Saldo inicial',
                                                   'Ativo','quantidade',
                                                  'Compra','Venda','Saldo final'])
    
     
    df_ef = pd.DataFrame(data=[],columns=['data', 'Ativo','quantidade', 
                                          'preço','Valor Total','cotação atual',
                                          'Diferença','Resultado','Ganho'])
        
    df_resultado = pd.DataFrame(data=[],columns=[
                                          'Data', 
                                          'Valor UM',
                                          #'Valor Ativos',
                                          'Valor carteira', 
                                          'Saldo Final'])
    
    
    return df_historico, df_hist_ordens, df_ef, df_resultado

def objeto_acoes(acoes):
    # Cria uma lista de ações vazias
    lista_de_acoes = lst_nome_acoes(acoes)
    # Cria uma lista com os valores iguais a zero
    l_zero = [0]*len(lista_de_acoes)
    # Cria o dicionário
    dic_acoes = dict(zip(lista_de_acoes,l_zero))
    


def atualiza_periodo(lista_acoes,periodos_disponíveis, data_cotacao,
                     df_completo, df_cotacoes, df_disponivel,
                     dic_preco_atual, data_t, data_t1):

    periodos_disponíveis = periodos_disponíveis+1
    data_cotacao = periodos_disponíveis
    df_disponivel = df_completo.iloc[0:periodos_disponíveis]
    #datas t
    data_t = df_disponivel.iloc[-1, -1]
    #data t-1
    data_t1 = df_disponivel.iloc[-2, -1]
    #Conjunto de cotações
    df_cotacoes = df_completo.loc[:, df_completo.columns.str.endswith("FECHAMENTO")]
  
    df_cotacoes = df_cotacoes.loc[data_cotacao-1:data_cotacao]
    ultima_c = df_cotacoes.iloc[-1].values
    dic_preco_atual = dict(zip(lista_acoes, ultima_c))
    
    return (periodos_disponíveis,
            data_cotacao,df_cotacoes,df_disponivel, 
            dic_preco_atual,data_t, data_t1)

def limite_alavacagem(df_fixo,qdd,ativo):
     
    procurar = df_fixo[(df_fixo['Ativo']==ativo)]
    qdd_atual = procurar['quantidade'].values
    limite = qdd_atual+qdd
    
    if limite >= 0:
        retorno = 'verdadeiro'
    else:
        retorno = 'falso'
    
    return retorno
       
def limite_alavacagem_saldo(acao, dic_preco_atual, df_historico, 
                            quantidade, data_cotacao,negociacao):
     
    preco = dic_preco_atual[acao]
     
    preco = round(float(preco),2)
    
    print(data_cotacao,' ', acao,' ', preco)
    
    sinicial = float(df_historico.iloc[-1,5:6].values) # a fazer criar os demais elementos.
     
    
    if negociacao =='compra':
        sfinal = float(sinicial-(quantidade*preco))
        sfinal = round(sfinal,2)
        quantidade = np.abs(quantidade)

    else:
        sfinal = float(sinicial+(quantidade*preco))
        sfinal = round(sfinal,2)
        quantidade = quantidade*(-1)
    
    if sfinal > 0:
        retorno = 'verdadeiro'
    else:
        retorno = 'falso'
     
    return retorno
    

def comprar_ativo(acao, quantidade, dic_preco_atual,
                  df_historico, data_t, periodos_disponíveis,
                  data_cotacao, negociacao):
        
    preco = dic_preco_atual[acao]
     
    preco = round(float(preco),2)
    
    print(data_cotacao,' ', acao,' ', preco)
    
    sinicial = float(df_historico.iloc[-1,5:6].values) # a fazer criar os demais elementos.
     
    
    if negociacao =='compra':
        sfinal = float(sinicial-(quantidade*preco))
        sfinal = round(sfinal,2)
        quantidade = np.abs(quantidade)

    else:
        sfinal = float(sinicial+(quantidade*preco))
        sfinal = round(sfinal,2)
        quantidade = quantidade*(-1)
    
    print(preco,' comprar_ativo1', 'período :',data_t)
     
    df_historico = df_historico.append({'Data':data_t,
                                        'Saldo inicial':sinicial,
                                        'Ativo': acao,
                                        'quantidade': quantidade,
                                        'preço':preco,
                                        'Saldo final':sfinal}, ignore_index=True)

        
    return df_historico

def carteira(df_historico, data_t, dic_preco_atual):
    df_historico['Resultado'] = df_historico['quantidade']*df_historico['preço']
    df_cart = df_historico[(df_historico['quantidade']!=0)]
    df_cart = df_cart.groupby(['Ativo']).agg({'quantidade': 'sum',
                                              'Resultado': 'sum'})
    df_cart['Preço referência'] = df_cart['Resultado']/df_cart['quantidade']
    #df_cart = df_cart[(df_cart['quantidade']!=0)]
    df_cart = df_cart.reset_index()
    df_cart['Cotação atual'] =  df_cart['Ativo'].map(dic_preco_atual)
    df_cart['Diferença'] = df_cart['Cotação atual']-df_cart['Preço referência']
    df_cart['Resultado'] = df_cart['quantidade']*df_cart['Diferença']
    df_cart['Valor Total'] = df_cart['quantidade']*df_cart['Cotação atual'] 
    
    conditions = [
        (df_cart['Resultado'] > 0),
        (df_cart['Resultado'] < 0),
        (df_cart['Resultado'] == 0)&(df_cart['quantidade'] != 0)
        ]
    values = ['Ganho', 'Perda', 'Empate']

    df_cart['Ganho'] = np.select(conditions, values)
    df_cart['Data'] = data_t
    df_cart['Diferença'] = round(df_cart['Diferença'],2)
    df_cart['Resultado'] = round(df_cart['Resultado'],2)
    df_cart['Valor Total'] = round(df_cart['Valor Total'],2) 
    
    df_cart = df_cart[['Data','Ativo','quantidade','Preço referência', 
                       'Cotação atual','Diferença','Valor Total','Resultado','Ganho']]
    
    return df_cart

def carteiraTela(df_historico, data_t, dic_preco_atual):
    df_historico = df_historico[(df_historico['quantidade']!=0)]
    
    df_historico['Cumsum'] = df_historico.groupby(['Ativo']).agg({'quantidade': 'cumsum'})
    
    cond1 = [df_historico['Cumsum']==0,df_historico['Cumsum']!=0]
    val1 = [1,np.nan]
        
    df_historico['CumsumZero'] = np.select(cond1, val1)
    df_historico['backwardfill'] = df_historico.groupby(['Ativo'])['CumsumZero'].fillna( method='bfill')
    df_historico['backwardfill'] = df_historico['backwardfill'].replace(np.nan, 0)
     
    print(df_historico['backwardfill'])
    df_historico = df_historico[(df_historico['backwardfill']==0)]
    print(df_historico['backwardfill'])
    df_historico['Resultado'] = df_historico['quantidade']*df_historico['preço']
        
    df_cart = df_historico[(df_historico['quantidade']!=0)]
    df_cart = df_cart.groupby(['Ativo']).agg({'quantidade': 'sum',
                                              'Resultado': 'sum'})
    df_cart['Preço referência'] = df_cart['Resultado']/df_cart['quantidade']
    df_cart = df_cart[(df_cart['quantidade']!=0)]
    df_cart = df_cart.reset_index()
    df_cart['Cotação atual'] =  df_cart['Ativo'].map(dic_preco_atual)
    df_cart['Diferença'] = df_cart['Cotação atual']-df_cart['Preço referência']
    df_cart['Resultado'] = df_cart['quantidade']*df_cart['Diferença']
    df_cart['Valor Total'] = df_cart['quantidade']*df_cart['Cotação atual'] 
    conditions = [
        (df_cart['Resultado'] > 0),
        (df_cart['Resultado'] < 0),
        (df_cart['Resultado'] == 0)&(df_cart['quantidade'] != 0)
        ]
    values = ['Ganho', 'Perda', 'Empate']

    df_cart['Ganho'] = np.select(conditions, values)
    df_cart['Data'] = data_t
    
    df_cart['Diferença'] = round(df_cart['Diferença'],2)
    df_cart['Resultado'] = round(df_cart['Resultado'],2)
    df_cart['Valor Total'] = round(df_cart['Valor Total'],2) 
    
    df_cart = df_cart[['Data','Ativo','quantidade','Preço referência', 
                       'Cotação atual','Diferença','Valor Total','Resultado','Ganho']]
    
    return df_cart


# Função objetos ações.
def df_fixo(acoes, data_t,dic_preco_atual):
    # Cria uma lista de ações vazias.
    lista_de_acoes = lst_nome_acoes(acoes)
    # Cria uma lista com os valores iguais a zero.
    l_zero = [0]*len(lista_de_acoes)
    l_data = [data_t]*len(lista_de_acoes)
    # Cria o dicionário.
    dic_acoes = dict(zip(lista_de_acoes,l_zero))
    #criar um conjunto de dados com a lista de ações.
    df_fixo = pd.DataFrame(dic_acoes.items(), columns=['Ativo', 'quantidade'])
    df_fixo['preço'] = l_zero
    df_fixo['Valor Total'] = df_fixo['preço']*df_fixo['quantidade']
    df_fixo['data'] = l_data 
    df_fixo['cotação atual'] = round(df_fixo['Ativo'].map(dic_preco_atual),2)
    df_fixo['Diferença'] = round(df_fixo['cotação atual']-df_fixo['preço'],2)
    df_fixo['Resultado'] = round(df_fixo['Diferença']*df_fixo['quantidade'],2)
    df_fixo['Ganho'] = 'Empate'
    
     
    return df_fixo

 
# Função objetos ações.
def atualiza_df_fixo(df_fixo, data_t,dic_preco_atual):
    
    df_fixo['Valor Total'] = df_fixo['preço']*df_fixo['quantidade']
        
    df_fixo['cotação atual'] = df_fixo['Ativo'].map(dic_preco_atual)
    df_fixo['Diferença'] = round(df_fixo['cotação atual']-df_fixo['preço'],2)
    df_fixo['Resultado'] = round(df_fixo['Diferença']*df_fixo['quantidade'],2)
    conditions = [
        (df_fixo['Resultado'] > 0),
        (df_fixo['Resultado'] < 0),
        (df_fixo['Resultado'] == 0)&(df_fixo['quantidade'] != 0)
        ]
    values = ['Ganho', 'Perda', 'Empate']
    df_fixo['Ganho'] = np.select(conditions, values)
     
    return df_fixo

# Criar função que recebe ordens de compra e venda nao alavancada
def negociacao_na(df_fixo, ativo, quantidade, preco, tipo,data_t,dic_preco_atual):
    
    print(quantidade, 'NEGOCIAÇÃO NA')
    procurar = df_fixo[(df_fixo['Ativo']==ativo)]
    qdd_atual = procurar['quantidade'].values
    preco_atual = procurar['preço'].values
    resultado = qdd_atual*preco_atual
    valor = qdd_atual + quantidade
    total_ordem = quantidade*preco
    print('total da ordem é :', total_ordem) 
   
    if quantidade > 0 and valor >= 0: 
        conda = [(df_fixo['Ativo']==ativo),(df_fixo['Ativo']!=ativo)]
        valuea = [valor, df_fixo['quantidade']]
        df_fixo['quantidade'] = np.select(conda, valuea)
        
        condb = [(df_fixo['Ativo']==ativo),(df_fixo['Ativo']!=ativo)] 
        valueb = [(resultado+total_ordem)/(qdd_atual+quantidade), 
                  df_fixo['preço']]
        
        df_fixo['preço'] = np.select(condb, valueb)
        df_fixo['preço'] = round(df_fixo['preço'],2)
        df_fixo['Valor Total'] = round(df_fixo['preço']*df_fixo['quantidade'],2)
        df_fixo['cotação atual'] = round(df_fixo['Ativo'].map(dic_preco_atual),2)
        
        condc = [(df_fixo['Ativo']==ativo),(df_fixo['Ativo']!=ativo)] 
        valuec = [data_t,df_fixo['data']]
        df_fixo['data'] = np.select(condc, valuec)
        df_fixo['Diferença'] = round(df_fixo['cotação atual']-df_fixo['preço'],2)
        
        df_fixo['Resultado'] = round(df_fixo['Diferença']*df_fixo['quantidade'],2)  
        conditions = [
            (df_fixo['Resultado'] > 0),
            (df_fixo['Resultado'] < 0),
            (df_fixo['Resultado'] == 0)&(df_fixo['quantidade'] != 0)
            ]
        values = ['Ganho', 'Perda', 'Empate']
        df_fixo['Ganho'] = np.select(conditions, values)
        
        print('valor positivo') 
        
    elif quantidade < 0 and valor >= 0:
        
        conda = [(df_fixo['Ativo']==ativo),(df_fixo['Ativo']!=ativo)]
        valuea = [valor, df_fixo['quantidade']]
        df_fixo['quantidade'] = np.select(conda, valuea)
        df_fixo['Valor Total'] = round(df_fixo['preço']*df_fixo['quantidade'],2)
        
        condd = [(df_fixo['Ativo']==ativo),(df_fixo['Ativo']!=ativo)] 
        valued = [dic_preco_atual[ativo], df_fixo['preço']]
        df_fixo['cotação atual'] = np.select(condd, valued)
        df_fixo['cotação atual']  = round(df_fixo['cotação atual'],2)
        #df_fixo['cotação atual'] = df_fixo['Ativo'].map(dic_preco_atual)
        
        condc = [(df_fixo['Ativo']==ativo),(df_fixo['Ativo']!=ativo)] 
        valuec = [data_t,df_fixo['data']]
        df_fixo['data'] = np.select(condc, valuec)
        df_fixo['Diferença'] = round(df_fixo['cotação atual']-df_fixo['preço'],2)
        
        df_fixo['Resultado'] = round(df_fixo['Diferença']*df_fixo['quantidade'],2)
        conditions = [
            (df_fixo['Resultado'] > 0),
            (df_fixo['Resultado'] < 0),
            (df_fixo['Resultado'] == 0)&(df_fixo['quantidade'] != 0)
            ]
        values = ['Ganho', 'Perda', 'Empate']
        df_fixo['Ganho'] = np.select(conditions, values)
    else:
        print('não fez nada')
       
    df_fixo = df_fixo[['data', 'Ativo','quantidade', 'preço','Valor Total','cotação atual',
                       'Diferença','Resultado','Ganho']]    
    return df_fixo


def carteiraTela2(df_fixo, data_t, dic_preco_atual):
    df_cart = df_fixo.copy()
    df_cart['cotação atual'] = df_cart['Ativo'].map(dic_preco_atual)
    df_cart['Diferença'] =  df_cart['preço'] - df_cart['cotação atual']
    df_cart['Resultado'] = df_cart['quantidade']*df_cart['preço']
         
    conditions = [
        (df_cart['Resultado'] > 0),
        (df_cart['Resultado'] < 0),
        (df_cart['Resultado'] == 0)&(df_cart['quantidade'] != 0)
        ]
    values = ['Ganho', 'Perda', 'Empate']

    df_cart['Ganho'] = np.select(conditions, values)
    df_cart = df_cart[(df_cart['quantidade']>0)]
    
    return df_cart

    

def efeito_dis(df_ef, df_fixo): #troquei o acoes_ativas por df_fixo
    df_ef = pd.concat([df_ef, df_fixo],axis=0)
    return df_ef

def efd(df_ef):
       
    disp = df_ef.copy()
    disp = disp.sort_values(by=['Ativo','data'])
    disp['quantidade'] = disp['quantidade'].astype(float)
    disp['Ganho'] = disp['Ganho'].replace(to_replace = '0',  method='ffill')
    disp['quantidade abs'] = np.abs(disp['quantidade'])
    disp['Variação quantidade'] = disp.groupby(['Ativo'])['quantidade'].diff().fillna(0).values
    disp['Variação quantidade'] = np.abs(disp['Variação quantidade'])
    disp['total acoes'] = disp['Variação quantidade']+disp['quantidade abs']
    
    #Realizado
    cod_realizado = [(disp['quantidade abs'].shift(1)>disp['quantidade abs']),
                     (disp['quantidade abs'].shift(1)<=disp['quantidade abs'])
                     ]
    val_realizado = [disp['Variação quantidade'],0]  
    disp['Realizado'] = np.select(cod_realizado,val_realizado)
    
    #Ganho/Perda em carteria
    cond_ganho_carteira = [(disp['Ganho'] != "Perda"),
                           (disp['Ganho'] != "Ganho")]
    
    val_ganho_carteira = [(disp['total acoes']-disp['Variação quantidade']),0]
    disp['Ganho em Carteira'] = np.select(cond_ganho_carteira,val_ganho_carteira)
    
    cond_perda_carteira = [(disp['Ganho'] != "Ganho"),
                           (disp['Ganho'] != "Perda")]
    
    val_perda_carteira = [(disp['total acoes']-disp['Variação quantidade']),0]
    disp['Perda em Carteira'] = np.select(cond_perda_carteira,val_perda_carteira)
    
    # Ganhos/perdas realizadas
    condgr1 = [(disp['Ganho'] == "Ganho"),(disp['Ganho'] != "Ganho")]
    condgr2 = [(disp['Ganho'] == "Perda"),(disp['Ganho'] != "Perda")]
    
    #val_g1 = [disp['diferenca']]
    val_g1 = [disp['Realizado'],0]
    
    disp['Ganho Realizado'] = np.select(condgr1, val_g1)
    disp['Perda Realizada'] = np.select(condgr2, val_g1)
    
    
    return disp

def atualiza_periodo_dfs(df_historico, data_t,data_t1, dic_preco_atual, df_ef,
                         lista_acoes, periodos_disponíveis,data_cotacao,
                         df_completo, df_cotacoes, df_disponivel,df_resultado,df_fixo
                         ):

    lst_atual = atualiza_periodo(lista_acoes,periodos_disponíveis, data_cotacao,
                                 df_completo, df_cotacoes, df_disponivel,
                                 dic_preco_atual, data_t, data_t1)
             
            
    periodos_disponíveis = lst_atual[0] 
    data_cotacao = lst_atual[1]
    df_cotacoes = lst_atual[2]
    df_disponivel = lst_atual[3]
    dic_preco_atual = lst_atual[4]
    data_t = lst_atual[5]
    data_t1 = lst_atual[6]
    
    acoes_ativas_tela = carteiraTela(df_historico, data_t, dic_preco_atual)
    acoes_ativas = carteira(df_historico, data_t, dic_preco_atual)
    total = round(acoes_ativas_tela['Valor Total'].sum(),2)
    df_ef = efeito_dis(df_ef, df_fixo) #acoes_ativas tive que trocar para df_fixo
    
    sinicial = float(df_historico.iloc[-1,5])
    print('print valor do df_histórico[-1,-1] ',df_historico.iloc[-1,5])
    
    
    result_total = round(sinicial+float(total),2)
                                     
    df_resultado = df_resultado.append({'Data':data_t,
                                        'Valor UM':sinicial,
                                        #'Valor Ativos': valor_acoes,
                                        'Valor carteira': total,  
                                        'Saldo Final':result_total}, ignore_index=True) 
    
  

    return (acoes_ativas_tela, acoes_ativas, total, df_ef,
            periodos_disponíveis, data_cotacao,
            df_completo, df_cotacoes,df_disponivel, dic_preco_atual,
            data_t, data_t1, df_resultado)

"""
#conjunto completo
df_completo = pd.read_excel('C:/PHD/A parte/Emulador acoes/historico_acoes.xlsx')
#períodos disponíveis
periodos_disponíveis = 12
#data da cotação
data_cotacao = periodos_disponíveis

#função lista ações
l_objetosa = listasacoes(df_completo, periodos_disponíveis)
# Preencher listbox na tela
lista_acoes = l_objetosa[0]
data_t = l_objetosa[1]
data_t1 = l_objetosa[2]
df_ctc_fechadas = l_objetosa[3]
df_cotacoes = l_objetosa[4]
df_disponivel = l_objetosa[5]

#função precoatual
dic_preco_atual = precoatual(lista_acoes, df_cotacoes)

#conjuntos de dados
lista_objetob = conjunto_dados(data_t1,100000)
df_historico = lista_objetob[0]
df_hist_ordens = lista_objetob[1]
df_ef = lista_objetob[2]

# lista de ações ['PETR4', 'MGLU3', 'ITUB4', 'BBAS3', 'VALE3']
#conjunto de dados negociação, preencher treeview de histórico de negociação
df_historico = comprar_ativo("ITUB4", 1000, dic_preco_atual,
                  df_historico, data_t, periodos_disponíveis,
                  data_cotacao, 'compra')

#Atualiza os períodos, botão atualizar
lst_atualizada = atualiza_periodo_dfs(df_historico, data_t,data_t1, dic_preco_atual, 
                                      df_ef,lista_acoes, periodos_disponíveis,
                                      data_cotacao,df_completo, df_cotacoes, 
                                      df_disponivel)

#Preencher treeview após atualizar
acoes_ativas_tela = lst_atualizada[0]
#Para junção no histórico
acoes_ativas = lst_atualizada[1]
#Para adicionar resultado da carteira
total = lst_atualizada[2]
#Para concatenar a carteira e criar o efeito de disposição
df_ef = lst_atualizada[3]
#Atualizado o período disponivel ao usuário, rever uso do acento
periodos_disponíveis = lst_atualizada[4]
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
#Cria um conjunto de dados com o efeito de disposição
disp = efd(df_ef)

"""


