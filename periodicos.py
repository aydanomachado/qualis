#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cria arquivo com avaliação dos periodicos no qualis CC e Interdisciplinar

@author: Aydano Machado <aydano.machado@gmail.com>
"""
import pandas as pd
import os.path

#IndArtProg ou IndArtDP = ( 1,0*A1 + 0,85*A2 + 0,7*B1 + 0,55*B2 + 0,4*B3 + 0,25*B4 + 0,1*B5)
def qualis2num(qualis):
    if qualis == 'A1':
        return 1
    elif qualis == 'A2':
        return 0.85
    elif qualis == 'B1':
        return 0.7
    elif qualis == 'B2':
        return 0.55
    elif qualis == 'B3':
        return 0.4
    elif qualis == 'B4':
        return 0.25
    elif qualis == 'B5':
        return 0.1
    elif qualis == 'C':
        return 0
    
def trimAllColumns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trimStrings = lambda x: x.strip() if type(x) is str else x
    return df.applymap(trimStrings)

# importando arquivos qualis
qualis_cc = pd.read_csv('CAPES/qualis_cc_2017_02_18.xls', sep='\t')
qualis_eng4 = pd.read_csv('CAPES/qualis_eng4_2017_02_18.xls', sep='\t')
qualis_inter = pd.read_csv('CAPES/qualis_inter_2017_02_18.xls', sep='\t')
qualis_mpe = pd.read_csv('CAPES/qualis_mat_prob_est_2017_02_18.xls', sep='\t')
# retirando espaços antes e depois das strings
qualis_cc = trimAllColumns(qualis_cc)
qualis_eng4 = trimAllColumns(qualis_eng4)
qualis_inter = trimAllColumns(qualis_inter)
qualis_mpe = trimAllColumns(qualis_mpe)
# removendo linhas repetidas (descoberto depois que no qualis tem duplicatas de revistas)....
# removendo as que tem ISSN e Estrato iguais
qualis_cc.drop_duplicates(subset=['ISSN', 'Estrato'], inplace=True)
qualis_eng4.drop_duplicates(subset=['ISSN', 'Estrato'], inplace=True)
qualis_inter.drop_duplicates(subset=['ISSN', 'Estrato'], inplace=True)
qualis_mpe.drop_duplicates(subset=['ISSN', 'Estrato'], inplace=True)
# adicionando coluna com o valor do periódico
qualis_cc['CC'] = qualis_cc['Estrato'].apply(qualis2num)
qualis_eng4['Eng4'] = qualis_eng4['Estrato'].apply(qualis2num)
qualis_inter['Inter'] = qualis_inter['Estrato'].apply(qualis2num)
qualis_mpe['MPE'] = qualis_mpe['Estrato'].apply(qualis2num)


# importando arquivos periodicos
periodicosIC = pd.read_csv('data/PeriodicosIC1518.csv')
periodicosIC = trimAllColumns(periodicosIC)

# colocando qualis CC
periodicosIC = pd.merge(periodicosIC, qualis_cc, suffixes=('', '_CC'), on=['ISSN'], how='left')
periodicosIC = pd.merge(periodicosIC, qualis_inter, suffixes=('', '_Inter'), on=['ISSN'], how='left')

periodicosIC.drop(columns=['Título_Inter'], inplace=True)
periodicosIC.rename(columns = {'Título_IC':'Periodico'}, inplace=True)

# salvando excel com avaliações
prod_file = 'output/producaoCCeInter.xlsx'
if os.path.isfile(prod_file):
        print("Arquivo "+ prod_file + " já exite")
else:
    writer = pd.ExcelWriter(prod_file)
    periodicosIC.to_excel(writer,'Periodicos')
    writer.save()
    print("Arquivo "+ prod_file + " criado")