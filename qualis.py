#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparação entre qualis das áreas de pesquisa no IC

@author: Aydano Machado <aydano.machado@gmail.com>
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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


# importando arquivos
qualis_cc = pd.read_csv('CAPES/qualis_cc_2017_02_18.xls', sep='\t')
qualis_eng4 = pd.read_csv('CAPES/qualis_eng4_2017_02_18.xls', sep='\t')
qualis_inter = pd.read_csv('CAPES/qualis_inter_2017_02_18.xls', sep='\t')
qualis_mpe = pd.read_csv('CAPES/qualis_mat_prob_est_2017_02_18.xls', sep='\t')
# retirando espaços antes e depois das strings
qualis_cc = trimAllColumns(qualis_cc)
qualis_eng4 = trimAllColumns(qualis_eng4)
qualis_inter = trimAllColumns(qualis_inter)
qualis_mpe = trimAllColumns(qualis_mpe)
# adicionando coluna com o valor do periódico
qualis_cc['CC'] = qualis_cc['Estrato'].apply(qualis2num)
qualis_eng4['Eng4'] = qualis_eng4['Estrato'].apply(qualis2num)
qualis_inter['Inter'] = qualis_inter['Estrato'].apply(qualis2num)
qualis_mpe['MPE'] = qualis_mpe['Estrato'].apply(qualis2num)

# pegando interseções
eng4_cc = pd.merge(qualis_eng4, qualis_cc, suffixes=('_Eng4', '_CC'), on=['ISSN'], how='inner')
inter_cc = pd.merge(qualis_inter, qualis_cc, suffixes=('_Inter', '_CC'), on=['ISSN'], how='inner')
mpe_cc = pd.merge(qualis_mpe, qualis_cc, suffixes=('_MPE', '_CC'), on=['ISSN'], how='inner')

cc_inter = pd.merge(qualis_cc, qualis_inter, suffixes=('_CC', '_Inter'), on=['ISSN'], how='inner')
eng4_inter = pd.merge(qualis_eng4, qualis_inter, suffixes=('_Eng4', '_Inter'), on=['ISSN'], how='inner')
mpe_inter = pd.merge(qualis_mpe, qualis_inter, suffixes=('_MPE', '_Inter'), on=['ISSN'], how='inner')

# calculando diferenças
eng4_cc['CC_Eng4'] = eng4_cc.apply(lambda row: row.CC - row.Eng4, axis=1)
inter_cc['CC_Inter'] = inter_cc.apply(lambda row: row.CC - row.Inter, axis=1)
mpe_cc['CC_MPE'] = mpe_cc.apply(lambda row: row.CC - row.MPE, axis=1)

cc_inter['Inter_CC'] = cc_inter.apply(lambda row: row.Inter - row.CC, axis=1)
eng4_inter['Inter_Eng4'] = eng4_inter.apply(lambda row: row.Inter - row.Eng4, axis=1)
mpe_inter['Inter_MPE'] = mpe_inter.apply(lambda row: row.Inter - row.MPE, axis=1)

# adicionando cor
'''eng4_cc['color'] = np.where(eng4_cc['CC_Eng4']<0, 'red', 'blue')
inter_cc['color'] = np.where(inter_cc['CC_Inter']<0, 'red', 'blue')
mpe_cc['color'] = np.where(mpe_cc['CC_MPE']<0, 'red', 'blue')
cc_inter['color'] = np.where(cc_inter['Inter_CC']<0, 'red', 'blue')
eng4_inter['color'] = np.where(eng4_inter['Inter_Eng4']<0, 'red', 'blue')
mpe_inter['color'] = np.where(mpe_inter['Inter_MPE']<0, 'red', 'blue')'''

# calculando estatística das diferencas
eng4_cc_desc = eng4_cc['CC_Eng4'].describe()
eng4_cc_desc.name = 'Engenharias IV'
inter_cc_desc = inter_cc['CC_Inter'].describe()
inter_cc_desc.name = 'Interdisciplinar'
mpe_cc_desc = mpe_cc['CC_MPE'].describe()
mpe_cc_desc.name = 'Mat., Prob. e Est.'
CC_desc = pd.concat([eng4_cc_desc, mpe_cc_desc, inter_cc_desc], axis=1).transpose()
CC_desc.columns.name = 'Ciência da Computação - X'

cc_inter_desc = cc_inter['Inter_CC'].describe()
cc_inter_desc.name = 'Ciência da Computação'
eng4_inter_desc = eng4_inter['Inter_Eng4'].describe()
eng4_inter_desc.name = 'Engenharias IV'
mpe_inter_desc = mpe_inter['Inter_MPE'].describe()
mpe_inter_desc.name = 'Mat., Prob. e Est.'
Inter_desc = pd.concat([eng4_inter_desc, mpe_inter_desc, cc_inter_desc], axis=1).transpose()
Inter_desc.columns.name = 'Interdisciplinar - X'

# descritivo dos qualis de cada área
n_periodicos = pd.DataFrame(columns=['nº total de periódicos', 'interseção com a CC', 'interseção com o Inter'])
n_periodicos.loc['Ciência da Computação'] = [len(qualis_cc), 'Total', len(cc_inter)]
n_periodicos.loc['Engenharias IV'] = [len(qualis_eng4), len(eng4_cc), len(eng4_inter)]
n_periodicos.loc['Interdisciplinar'] = [len(qualis_inter), len(inter_cc), 'Total']
n_periodicos.loc['Mat. Prob. e Est.'] = [len(qualis_mpe), len(mpe_cc), len(mpe_inter)]

# implementação dos gráficos
def plotCCBars():
    plt.figure(figsize=(18, 6), dpi= 80, facecolor='w', edgecolor='k')

    plt.subplot(1, 3, 1)
    plt.ylim(-1,+1)
    plt.title('Ciência da Computação')
    plt.xlabel('Periódico')
    plt.ylabel('Engenharias IV')
    y_pos = np.arange(len(eng4_cc['CC_Eng4']))
    height = eng4_cc['CC_Eng4'].sort_values()
    bar_color = np.where(height<0, 'red', 'blue')
    plt.bar(y_pos, height, color=bar_color)
    
    plt.subplot(1, 3, 2)
    plt.ylim(-1,+1)
    plt.title('Ciência da Computação')
    plt.xlabel('Periódico')
    plt.ylabel('Mat. Prob. e Est.')
    y_pos = np.arange(len(mpe_cc['CC_MPE']))
    height = mpe_cc['CC_MPE'].sort_values()
    bar_color = np.where(height<0, 'red', 'blue')
    plt.bar(y_pos, height, color=bar_color)
    
    plt.subplot(1, 3, 3)
    plt.ylim(-1,+1)
    plt.title('Ciência da Computação')
    plt.xlabel('Periódico')
    plt.ylabel('Interdisciplinar')
    y_pos = np.arange(len(inter_cc['CC_Inter']))
    height = inter_cc['CC_Inter'].sort_values()
    bar_color = np.where(height<0, 'red', 'blue')
    plt.bar(y_pos, height, color=bar_color)
    
    plt.show()
    
def plotInterBars():
    plt.figure(figsize=(18, 6), dpi= 80, facecolor='w', edgecolor='k')

    plt.subplot(1, 3, 1)
    plt.ylim(-1,+1)
    plt.title('Interdisciplinar')
    plt.xlabel('Periódico')
    plt.ylabel('Engenharias IV')
    y_pos = np.arange(len(eng4_inter['Inter_Eng4']))
    height = eng4_inter['Inter_Eng4'].sort_values()
    bar_color = np.where(height<0, 'red', 'blue')
    plt.bar(y_pos, height, color=bar_color)
    
    plt.subplot(1, 3, 2)
    plt.ylim(-1,+1)
    plt.title('Interdisciplinar')
    plt.xlabel('Periódico')
    plt.ylabel('Mat. Prob. e Est.')
    y_pos = np.arange(len(mpe_inter['Inter_MPE']))
    height = mpe_inter['Inter_MPE'].sort_values()
    bar_color = np.where(height<0, 'red', 'blue')
    plt.bar(y_pos, height, color=bar_color)
    
    plt.subplot(1, 3, 3)
    plt.ylim(-1,+1)
    plt.title('Interdisciplinar')
    plt.xlabel('Periódico')
    plt.ylabel('Ciência da Computação')
    y_pos = np.arange(len(cc_inter['Inter_CC']))
    height = cc_inter['Inter_CC'].sort_values()
    bar_color = np.where(height<0, 'red', 'blue')
    plt.bar(y_pos, height, color=bar_color)
    
    plt.show()