"""
Tabu Search básico para o problema do caixeiro viajante (TSP)
Date: 16/11/2021
Author: André Hioki
Course: Programa de Pós-Graduação em Engenharia Elétrica - UNESP

Subject: Metaheuristica
Prof.: Rubén Augusto Romero Lazaro

Description: Desenvolvimento do algoritmo Tabu Search básico para o resolução do TSP.
A lista tabu armazena a solução inteira.
A solução vizinha se obtem trocando duas cidades (4 arcos que saem e 4 arcos que entram)
"""
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import math


def obter_valor_func_obj(x):    #função objetivo
    valor_obj = 0
    for i in range(matriz_tamanho):  #calcula o valor da função objetivo da rota original
        try:
            valor_obj += matriz_distancias[x[i], x[i + 1]]
        except:
            valor_obj += matriz_distancias[x[i], x[0]]

    return valor_obj


def plotar(rota):   #função para plotar rotas
    plt.clf()
    x = []
    y = []
    for i in range(len(rota)):
        x.append(cidade_coordenadas[rota[i],0])
        y.append(cidade_coordenadas[rota[i],1])
    plt.plot(x,y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Cidades')
    plt.draw()
    plt.pause(0.001)


"""
Inicialização
Leitura de dados, geração de matriz de distâncias e vizinhos (pares)
"""

inicio_tempo = time.time()

cidade_coordenadas = pd.read_csv('caixeiro01.csv').to_numpy()[:, 1:] #leitura do arquivo dataframe para array numpy
#print('coordenadas das cidades: ', cidade_coordenadas)
matriz_tamanho = cidade_coordenadas.shape[0]    #numero de cidades

matriz_distancias = np.zeros(shape=[matriz_tamanho, matriz_tamanho])
for i in range(matriz_tamanho):    #gerar matriz de distancias
    j = i
    while j < matriz_tamanho:
        try:
            cateto_b = (cidade_coordenadas[j, 0] - cidade_coordenadas[i, 0])**2
            cateto_c = (cidade_coordenadas[j, 1] - cidade_coordenadas[i, 1])**2
            distancia = math.sqrt(cateto_b + cateto_c)
            matriz_distancias[i, j] = distancia
            matriz_distancias[j, i] = distancia
            j +=1
        except:
            print('Há linhas que não são numeros')
            raise
            sys.exit(1)
#print('matriz de distancias: ', matriz_distancias)

rota = list(range(matriz_tamanho))  #vetor de rotas (tour) de tamanho n-cidades

#Definir todos os vizinhos em pares
vizinhos = []
#contador = 0
for i in range(matriz_tamanho-1):
    ind1 = i
    j = i
    while j < matriz_tamanho-1:
        ind2 = j + 1
        vizinhos.append((ind1, ind2)) #guarda as posições das cidades escolha
        j +=1

"""
Encontrar solução inicial através de AHC
"""

rota_AHC = [0]    #inicia na cidade 1 (posição 0)
while len(rota_AHC) < matriz_tamanho:
    atual = rota_AHC[-1]
    candidatos = dict()
    for i in range(matriz_tamanho):    #laço para ler a matriz de distancias
        if i not in rota_AHC:     #evita subtour / visitar cidades já visitadas
            candidatos[i] = matriz_distancias[atual, i]
    rota_AHC.append(min(candidatos.items(), key=lambda x: x[1])[0])
rota = rota_AHC.copy()

#Solução atual
obj = [obter_valor_func_obj(rota)]
print("Rota/tour AHC: ", rota)
print("Obj. AHC: ", obj)
print("")

melhor_rota = rota.copy()

plt.figure(1)
plt.ion()
plt.show()
"""
Tabu Search
"""

contador = 0
obj_global = sys.float_info.max
tabu = []
rota_corrente = []

while contador < 1000:

    obj_corrente = sys.float_info.max

    colecao_par = {}
    colecao_rota = {}
    for par in vizinhos:
        rota_corrente = rota.copy()
        rota_corrente[par[0]],rota_corrente[par[1]] = rota_corrente[par[1]],rota_corrente[par[0]]
        colecao_par[par] = obter_valor_func_obj(rota_corrente)
        colecao_rota[par] = rota_corrente

    colecao_par_ordenado = {}
    for w in sorted(colecao_par, key=colecao_par.get): #ordenar vizinhanças do melhor para pior com relaão ao valor da função obj.
        colecao_par_ordenado[w] = colecao_par[w]

    for z in colecao_par_ordenado:
        if (colecao_rota[z] not in tabu):
            melhor_rota = colecao_rota[z]
            tabu.append(colecao_rota[z])
            obj_corrente = colecao_par_ordenado[z]
            break
    rota = melhor_rota.copy()
    print("rota ",rota)
    obj.append(obj_corrente)
    print('Iter: ', contador)
    if obj_corrente < obj_global:
        tour = melhor_rota.copy()
        obj_global = obj_corrente
        print('Melhor obj: ', obj_global)
    else:
        print('Obj: ', obj_corrente)

    contador += 1
    plotar(rota)


###############################################
fim_tempo = time.time()

print("Valor incumbente: ", obj_global)
rota_cidade = []
for cidade in tour:
    rota_cidade.append(cidade+1)
print("Melhor rota:",rota_cidade)
print("")
print("Finished in:", fim_tempo-inicio_tempo)
plotar(tour)
plt.figure(2)
plt.plot(list(range(len(obj))), obj)
plt.xlabel('No de iterações')
plt.ylabel('Valor da função objetivo')
plt.title('Tabu Search')
plt.show()
