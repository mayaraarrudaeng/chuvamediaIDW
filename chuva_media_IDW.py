import pandas as pd
from geopy import distance
import numpy as np

chuvas = pd.DataFrame()

#nome do arquivo que contem os dados de chuva
arquivo_chuvas = "matriz_chuva_completa.csv"
#nome do arquivo que contém as latitudes e longitudes das estações
arquivo_coord = "estacoes.csv"
#nome do arquivo que contém as latitudes e longitudes do centroide da bacia
arquivo_bacia = "centroide.csv"
# diretorio onde a matriz de chuva, as coordenadas das estacoes e coord da bacia estão salvos
diretorio_entradas = 'dados'
# diretorio para salvar a chuva media
diretorio_resultados = 'resultados'


dados_chuvas = pd.read_csv(diretorio_entradas+'/'+arquivo_chuvas, delimiter=',', decimal='.')
dados_coord = pd.read_csv(diretorio_entradas+'/'+arquivo_coord, delimiter=',', decimal='.')
dados_bacia = pd.read_csv(diretorio_entradas+'/'+arquivo_bacia, delimiter=',', decimal='.')
#print(dados_bacia)
#print(dados_coord)
chuvas = dados_chuvas
n = len(chuvas.columns)
#print(n)
col_chuvas = chuvas.iloc[:,1:n]
'''i = 0
while i <= n-2:
    if col_chuvas.iloc[:,i].isnull().sum() >= 1:
        col_chuvas.iloc[:,i].isnull()
        col_chuvas.iloc[:,i].fillna(0, inplace=True)
        #print(col_chuvas.iloc[:,i])
    else:
        pass
        i = i + 1'''
#print(col_chuvas)
chuvas.iloc[:,1:n] = col_chuvas
#print(chuvas)
#definindo a coluna data como índice
chuvas.set_index('Data', inplace=True)
#print(chuvas)

lista_estacoes = dados_coord['Codigo'].unique()

#convertendo todos os codigos das estações de float para int
lista_estacoes = list(map(int, lista_estacoes))
d = pd.DataFrame()


#print(chuvas)

centroide = (dados_bacia.iloc[0].Latitude,dados_bacia.iloc[0].Longitude)
#print(centroide)
#print(range(dados_coord.shape[0]))
for i in range(dados_coord.shape[0]):
    coord = (dados_coord.iloc[i].Latitude,dados_coord.iloc[i].Longitude)
    #print(coord)
    d.loc[i,'distance']= distance.distance(centroide,coord).km*1000
    #print(distance.distance(centroide,coord).km*1000)

#d.to_csv(diretorio_resultados+'/distancia.csv', decimal='.', index=True)
chuvas['chuva_media'] = " "

for x in range(0,len(chuvas)):
    num_tot= 0
    den_tot= 0
    for i in range(d.shape[0]):
        if np.isnan(chuvas.iloc[x,i]) == True:
            pass
        else:
            num = chuvas.iloc[x,i]/d.iloc[i,0]**2
            den = 1/(d.iloc[i,0]**2)
            num_tot +=num
            den_tot +=den
    chuvas.iloc[x,d.shape[0]] = num_tot/den_tot
#print(chuvas)

chuvas.to_csv(diretorio_resultados+'/precipitacao_media.csv', decimal='.', index=True)