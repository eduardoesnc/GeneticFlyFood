import random
import copy
import time
from matplotlib import pyplot as plt
import numpy as np

#Função Calcular Distância
def calcDist(ponto1, ponto2):
    distPontos = ((((ponto1[0] - ponto2[0]) ** 2)+((ponto1[1] - ponto2[1]) ** 2)) ** 0.5)
    return distPontos

def setDist(lista):
    matriz = [[calcDist(lista[i], lista[j]) for j in range(len(lista))] for i in range(len(lista))]
    return matriz

def getDist(i, j, matriz):
    return matriz[i][j]

#Função que gera a primeira população
def primeiraPop(matriz, n):
    pop = []
    m = len(matriz)
    for i in range(n):
        pop.append(random.sample(range(0, m), n))
    return pop

#Função Fitness
def fitness(pop, matriz):
    somaInd = 0
    listFit = []

    for i in range(len(pop)):
        for j in range(len(pop[i]) - 1):
            somaInd += getDist(pop[i][j], pop[i][j + 1], matriz)
        somaInd += getDist(pop[i][j], pop[i][0], matriz)
        listFit.append(somaInd)
        somaInd = 0

    return listFit

# #Função seleção por torneio com elitismo
def selecao(listFit):
    pais = sorted(range(len(listFit)), key=lambda k: listFit[k])

    return pais

# Função seleção por torneio (Fazendo a competição entre 2 aleatórios)
# def selecao(fits):
#     pais = []
#     for i in range(len(fits)):
#         idx_candidato1 = random.randint(0, len(fits) - 1)
#         idx_candidato2 = random.randint(0, len(fits) - 1)
#         ganhador = idx_candidato2
#         if fits[idx_candidato1] < fits[ganhador]:
#             ganhador = idx_candidato1
#         pais.append(ganhador)
#     return pais

#Função crossover CX
def crossover(p1, p2):
    filho = copy.copy(p1)
    # quebra = random.randint(0, len(p1))

    n = random.sample(range(0, len(p1)), random.randint(1, len(p1) - 1))
    # n = p1[quebra:]
    n.sort()
    aux = []
    for i in n:
        aux.append(p1[i])
    n_ord = []
    for i in p2:
        if i in aux:
            n_ord.append(aux.index(i))
    for i in range(len(aux)):
        filho[n[i]] = aux[n_ord[i]]
    return filho

#Função mutação
def mutacao(cromossomo):
    n = len(cromossomo) - 1
    gene = random.randint(0, n)
    rand = random.randint(0, n)
    while rand == gene:
        rand = random.randint(0, n)
    # aux = cromossomo[gene]
    # cromossomo[gene] = cromossomo[rand]
    # cromossomo[rand] = aux
    cromossomo[gene], cromossomo[rand] = cromossomo[rand], cromossomo[gene]
    return cromossomo

#Função Elitismo
def elitismo(pop, listfit, qtd):
    newpop = []
    ordFit = selecao(listfit)
    for i in range(qtd):
        newpop.append(pop[ordFit[i]])
    return newpop

#Função Gerar nova população
def geraNewPop(pop, matriz, tMutacao, usarElitismo):
    newPop = []
    newFits = fitness(pop, matriz)
    i = 0
    ordFit = selecao(newFits)
    numCross = len(pop)
    while i < numCross:
        aux = ordFit[i]
        if aux == len(pop) - 1:
            newPop.append(crossover(pop[aux], pop[0]))
        else:
            newPop.append(crossover(pop[aux], pop[aux + 1]))

        if random.uniform(0, 100) <= tMutacao:
                newPop[i] = mutacao(newPop[i])
        i += 1
    if usarElitismo == True:
        for c in range(len(pop)):
            newPop.append(pop[c])
        newFits = fitness(newPop, matriz)
        newPop = elitismo(newPop, newFits, len(pop))
        ordFit = selecao(newFits)

    return newPop

#Função principal do GA
def evolucao(listEntrada, qtdGen):
    qtdGen += 1
    matrizDists = setDist(listEntrada)
    pop = primeiraPop(matrizDists, len(listEntrada))
    listFit = fitness(pop, matrizDists)
    ordFits = selecao(pop)
    menorCaminho = listFit[ordFits[0]]
    menorFits = []
    mediaFits = []
    # count = 0
    for i in range(qtdGen):

        newPop = geraNewPop(pop, matrizDists, 10, True)
        newFits = fitness(newPop, matrizDists)
        pop = newPop
        ordFits = selecao(pop)
        menorFits.append(newFits[ordFits[0]])
        mediaFits.append(sum(newFits) / len(newFits))
        if min(menorFits) < menorCaminho:
            menorCaminho = newFits[ordFits[0]]
        #     count = 0
        # elif min(menorFits) == menorCaminho:
        #     count += 1
        # if count >= 200:
        #     break
        print("geração", i,":", round(menorCaminho, 3)," média:", round(mediaFits[i], 3))
    # plt.figure()
    # plt.plot(range(gen), mediaFits, label='Caminho médio')
    # plt.plot(range(gen), menorFits, label='Caminho mínimo')
    # plt.legend()
    # plt.ylabel('Distância')
    # plt.xlabel('Gerações')
    # plt.show()
    melhorCaminho = newPop[ordFits[0]]
    print(melhorCaminho)

if __name__ == "__main__":
    with open('entrada.tsp.txt', "r") as f:
        dimension = [line.strip().split(" ") for line in f.readlines()[3:4]]
        dimension = int(dimension[0][1])
        dimension += 6 #É necessário alterar este valor para o número da linha em que aparece NODE_COORD_SECTION
    f.close()
    with open('entrada.tsp.txt', "r") as f:
        listaAux = [list(map(float, line.strip().split())) for line in f.readlines()[6:dimension]] #É necessário alterar este valor para o número da linha em que aparece NODE_COORD_SECTION
        matrizEntrada = [[x[1], x[2]] for x in listaAux]
    f.close()
    ini = time.time()
    evolucao(matrizEntrada, 2000)
    fim = time.time()
    print("Tempo gasto:", round(fim - ini, 3))